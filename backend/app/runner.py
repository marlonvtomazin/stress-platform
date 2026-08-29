from pathlib import Path
import subprocess
import os

from app.models import ExecutionRequest

SCRIPTS_DIR = Path("/scripts")


def build_command(
    execution_id: str,
    script: Path,
    config: ExecutionRequest,
):
    command = [
        "k6",
        "run",
        str(script),
        "-o",
        "influxdb",
        "--tag", f"execution_id={execution_id}",
        "--tag", f"application={config.application}",
        "--tag", f"environment={config.environment}",
        "--tag", f"test_name={config.test_name}",
        "--tag", "platform=stress-platform",
    ]

    # Constant VUs + Duration
    if config.vus and config.duration:
        command.extend(["--vus", str(config.vus)])
        command.extend(["--duration", config.duration])

    # Ramping stages (Sprint 3 já preparado)
    elif config.stages:
        command.extend(["--vus", "1"])

        for stage in config.stages:
            command.extend([
                "--stage",
                f"{stage.duration}:{stage.target}",
            ])

    return command


def run_script(
    execution_id: str,
    config: ExecutionRequest,
):
    execution_path = SCRIPTS_DIR / execution_id

    js_files = list(execution_path.glob("*.js"))

    if not js_files:
        raise FileNotFoundError("No JavaScript file found.")

    script = js_files[0]

    command = build_command(execution_id, script, config)

    # Passa as variáveis do InfluxDB para o processo do k6
    env = os.environ.copy()

    process = subprocess.run(
        command,
        env=env,
        capture_output=True,
        text=True,
    )

    (execution_path / "stdout.log").write_text(process.stdout)
    (execution_path / "stderr.log").write_text(process.stderr)

    return {
        "execution_id": execution_id,
        "exit_code": process.returncode,
        "stdout": process.stdout,
        "stderr": process.stderr,
    }