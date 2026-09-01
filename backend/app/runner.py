from pathlib import Path
import subprocess
import shutil

from app.models import ExecutionRequest

SCRIPTS_DIR = Path("/scripts")
REPORTER_SOURCE = Path("/app/resources/k6-reporter.bundle.js")

REPORTER_IMPORT = (
    'import { htmlReport } from "./k6-reporter.bundle.js";'
)

HANDLE_SUMMARY = """
export function handleSummary(data) {
  return {
    "summary.json": JSON.stringify(data, null, 2),
    "report/report.html": htmlReport(data),
  };
}
"""


def run_script(execution_id: str, config: ExecutionRequest):
    """
    Executa um teste k6 e salva:
      - stdout.log
      - stderr.log
      - summary.json
      - report/report.html
    """

    execution_folder = SCRIPTS_DIR / execution_id

    if not execution_folder.exists():
        raise FileNotFoundError(
            f"Pasta da execução não encontrada: {execution_folder}"
        )

    report_folder = execution_folder / "report"
    report_folder.mkdir(exist_ok=True)

    # Localiza o script enviado (qualquer .js, exceto o reporter)
    script_files = [
        f for f in execution_folder.glob("*.js")
        if f.name != "k6-reporter.bundle.js"
    ]

    if not script_files:
        raise FileNotFoundError(
            f"Nenhum script encontrado em {execution_folder}"
        )

    execution_script = script_files[0]

    # Copia o reporter para a pasta da execução
    shutil.copy(REPORTER_SOURCE, execution_folder / "k6-reporter.bundle.js")

    # Injeta htmlReport + handleSummary automaticamente
    script_content = execution_script.read_text(encoding="utf-8")

    if "handleSummary" not in script_content:
        script_content = (
            REPORTER_IMPORT
            + "\n\n"
            + script_content.rstrip()
            + "\n\n"
            + HANDLE_SUMMARY
        )

        execution_script.write_text(script_content, encoding="utf-8")

    command = [
        "k6",
        "run",
        str(execution_script),

        # Continua enviando métricas ao InfluxDB
        "-o",
        "influxdb",

        # Tags globais
        "--tag",
        f"execution_id={execution_id}",
        "--tag",
        f"application={config.application}",
        "--tag",
        f"environment={config.environment}",
        "--tag",
        f"test_name={config.test_name}",
        "--tag",
        "platform=stress-platform",
    ]

    # Caso o script não tenha stages e o usuário envie VUs/Duração
    if config.vus and config.duration:
        command.extend(["--vus", str(config.vus)])
        command.extend(["--duration", config.duration])

    process = subprocess.run(
        command,
        cwd=execution_folder,
        capture_output=True,
        text=True,
    )

    (execution_folder / "stdout.log").write_text(
        process.stdout,
        encoding="utf-8",
    )

    (execution_folder / "stderr.log").write_text(
        process.stderr,
        encoding="utf-8",
    )

    # Remove o reporter temporário
    reporter_copy = execution_folder / "k6-reporter.bundle.js"
    if reporter_copy.exists():
        reporter_copy.unlink()

    return {
        "execution_id": execution_id,
        "exit_code": process.returncode,
        "stdout": process.stdout,
        "stderr": process.stderr,
        "summary_path": str(execution_folder / "summary.json"),
        "report_path": str(report_folder / "report.html"),
    }