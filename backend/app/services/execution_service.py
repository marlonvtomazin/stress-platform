from pathlib import Path
import json

import shutil
import uuid

from app.models import ExecutionRequest, Stage
from app.runner import run_script

EXECUTIONS_DIR = Path("/executions")
SCRIPTS_DIR = Path("/scripts")


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
                "status": metadata.get("status", "ERROR"),
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
    Retorna os detalhes completos de uma execução.
    """

    execution_folder = EXECUTIONS_DIR / execution_id
    metadata_file = execution_folder / "metadata.json"

    if not metadata_file.exists():
        return None

    with open(metadata_file, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    metadata["artifacts"] = {
        "html_report": (execution_folder / "report" / "report.html").exists(),
        "summary": (execution_folder / "summary.json").exists(),
        "metadata": metadata_file.exists(),
        "stdout": (execution_folder / "stdout.log").exists(),
        "stderr": (execution_folder / "stderr.log").exists(),
    }

    return metadata


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

def rerun_execution(execution_id: str):
    """
    Reexecuta um teste utilizando o mesmo script e configuração
    da execução original.
    """

    execution_folder = EXECUTIONS_DIR / execution_id
    metadata_file = execution_folder / "metadata.json"

    if not metadata_file.exists():
        raise FileNotFoundError("Execução não encontrada.")

    with open(metadata_file, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    # Novo ID para a nova execução
    new_execution_id = uuid.uuid4().hex[:8]

    # Cria a pasta do novo script
    new_script_folder = SCRIPTS_DIR / new_execution_id
    new_script_folder.mkdir(parents=True, exist_ok=True)

    # Copia o script da execução original
    script_name = metadata["files"]["script"]

    shutil.copy(
        execution_folder / script_name,
        new_script_folder / script_name,
    )

    # Reconstrói o ExecutionRequest usando o metadata
    request = ExecutionRequest(
        test_name=metadata["test_name"],
        application=metadata["application"],
        environment=metadata["environment"],
        vus=metadata["config"]["vus"],
        duration=metadata["config"]["duration"],
        stages=(
            [Stage(**stage) for stage in metadata["config"]["stages"]]
            if metadata["config"]["stages"]
            else None
        ),
    )

    # Executa normalmente
    result = run_script(new_execution_id, request)

    # Guarda a referência da execução original
    result["original_execution_id"] = execution_id

    return result

def delete_execution(execution_id: str):
    """
    Remove todos os arquivos de uma execução e o script enviado.
    """

    execution_folder = EXECUTIONS_DIR / execution_id
    script_folder = SCRIPTS_DIR / execution_id

    if not execution_folder.exists():
        raise FileNotFoundError("Execução não encontrada.")

    # Remove os artefatos da execução
    shutil.rmtree(execution_folder)

    # Remove o script original (caso exista)
    if script_folder.exists():
        shutil.rmtree(script_folder)

    return {
        "message": "Execution deleted successfully.",
        "execution_id": execution_id,
    }