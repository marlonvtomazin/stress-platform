from pathlib import Path
import json

EXECUTIONS_DIR = Path("/executions")


def list_executions():
    executions = []

    if not EXECUTIONS_DIR.exists():
        return executions

    for execution_folder in EXECUTIONS_DIR.iterdir():
        if not execution_folder.is_dir():
            continue

        metadata_file = execution_folder / "metadata.json"

        if not metadata_file.exists():
            continue

        try:
            with open(metadata_file, "r", encoding="utf-8") as file:
                metadata = json.load(file)

            summary = metadata.get("summary", {})

            executions.append({
                "execution_id": metadata.get("execution_id", execution_folder.name),
                "test_name": metadata.get("test_name", "Sem nome"),
                "application": metadata.get("application", "-"),
                "environment": metadata.get("environment", "-"),
                "status": metadata.get("status", "UNKNOWN"),
                "started_at": metadata.get("started_at"),
                "finished_at": metadata.get("finished_at"),
                "duration_seconds": metadata.get("duration_seconds", 0),

                "total_requests": summary.get("total_requests", 0),
                "error_rate": summary.get("error_rate", 0),
                "avg_response_time": summary.get("avg_response_time", 0),
                "p95": summary.get("p95", 0),
            })

        except Exception as e:
            print(f"Erro lendo {metadata_file}: {e}")

    executions.sort(
        key=lambda execution: execution.get("started_at") or "",
        reverse=True,
    )

    return executions


def get_execution(execution_id: str):
    """
    Retorna o metadata completo de uma execução.
    """

    metadata_file = EXECUTIONS_DIR / execution_id / "metadata.json"

    if not metadata_file.exists():
        return None

    with open(metadata_file, "r", encoding="utf-8") as file:
        return json.load(file)


def execution_exists(execution_id: str):
    return (EXECUTIONS_DIR / execution_id).exists()


def get_execution_file(execution_id: str, file_type: str):
    """
    Retorna o caminho físico dos arquivos da execução.
    """

    execution_folder = EXECUTIONS_DIR / execution_id

    files = {
        "summary": execution_folder / "summary.json",
        "stdout": execution_folder / "stdout.log",
        "stderr": execution_folder / "stderr.log",
        "report": execution_folder / "report" / "report.html",
        "metadata": execution_folder / "metadata.json",
    }

    file_path = files.get(file_type)

    if file_path is None or not file_path.exists():
        return None

    return file_path