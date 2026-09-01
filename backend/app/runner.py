from pathlib import Path
from datetime import datetime, timezone
import subprocess
import shutil

from app.models import ExecutionRequest
from app.metadata import create_metadata

# Upload dos scripts
SCRIPTS_DIR = Path("/scripts")

# Histórico das execuções
EXECUTIONS_DIR = Path("/executions")

# HTML Reporter
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
    Executa um teste k6 e salva todos os artefatos em:

    /executions/{execution_id}
    """

    # -------------------------------
    # Pasta do upload
    # -------------------------------

    upload_folder = SCRIPTS_DIR / execution_id

    if not upload_folder.exists():
        raise FileNotFoundError(
            f"Pasta do upload não encontrada: {upload_folder}"
        )

    # -------------------------------
    # Pasta da execução
    # -------------------------------

    execution_folder = EXECUTIONS_DIR / execution_id
    execution_folder.mkdir(parents=True, exist_ok=True)

    report_folder = execution_folder / "report"
    report_folder.mkdir(exist_ok=True)

    # -------------------------------
    # Procura o script enviado
    # -------------------------------

    script_files = [
        file
        for file in upload_folder.glob("*.js")
        if file.name != "k6-reporter.bundle.js"
    ]

    if not script_files:
        raise FileNotFoundError(
            f"Nenhum script encontrado em {upload_folder}"
        )

    original_script = script_files[0]
    execution_script = execution_folder / original_script.name

    shutil.copy(original_script, execution_script)

    # -------------------------------
    # Copia o HTML Reporter
    # -------------------------------

    shutil.copy(
        REPORTER_SOURCE,
        execution_folder / "k6-reporter.bundle.js",
    )

    # -------------------------------
    # Injeta handleSummary
    # -------------------------------

    script_content = execution_script.read_text(
        encoding="utf-8"
    )

    if "handleSummary" not in script_content:
        script_content = (
            REPORTER_IMPORT
            + "\n\n"
            + script_content.rstrip()
            + "\n\n"
            + HANDLE_SUMMARY
        )

        execution_script.write_text(
            script_content,
            encoding="utf-8",
        )

    # -------------------------------
    # Comando k6
    # -------------------------------

    command = [
        "k6",
        "run",
        str(execution_script),

        "-o",
        "influxdb",

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

    if config.vus and config.duration:
        command.extend(["--vus", str(config.vus)])
        command.extend(["--duration", config.duration])

    # -------------------------------
    # Executa
    # -------------------------------

    started_at = datetime.now(timezone.utc)

    process = subprocess.run(
        command,
        cwd=execution_folder,
        capture_output=True,
        text=True,
    )

    finished_at = datetime.now(timezone.utc)

    # -------------------------------
    # Logs
    # -------------------------------

    (execution_folder / "stdout.log").write_text(
        process.stdout,
        encoding="utf-8",
    )

    (execution_folder / "stderr.log").write_text(
        process.stderr,
        encoding="utf-8",
    )

    # Remove o bundle temporário
    reporter_copy = execution_folder / "k6-reporter.bundle.js"

    if reporter_copy.exists():
        reporter_copy.unlink()

    # -------------------------------
    # Metadata
    # -------------------------------

    metadata = create_metadata(
        execution_id=execution_id,
        config=config,
        execution_folder=execution_folder,
        exit_code=process.returncode,
        started_at=started_at,
        finished_at=finished_at,
    )

    # -------------------------------
    # Retorno da API
    # -------------------------------

    return {
        "execution_id": execution_id,
        "status": metadata["status"],
        "exit_code": process.returncode,

        "summary_path": str(
            execution_folder / "summary.json"
        ),

        "report_path": str(
            report_folder / "report.html"
        ),

        "metadata_path": str(
            execution_folder / "metadata.json"
        ),

        "stdout": process.stdout,
        "stderr": process.stderr,
    }