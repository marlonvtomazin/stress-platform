from pathlib import Path
from typing import List
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from fastapi.responses import FileResponse

from app.models import ExecutionRequest
from app.runner import run_script
from app.services.execution_service import (
    list_executions,
    get_execution,
    get_execution_file,
    rerun_execution,
    delete_execution,
)

from app.models import (
    ExecutionRequest,
    ScriptUploadResponse,
    ExecutionResponse,
    ExecutionListItem,
    ExecutionDetailsResponse,
)

from app.swagger.scripts import UPLOAD_SCRIPT_DOCS
from app.swagger.executions import (
    RUN_EXECUTION_DOCS,
    RERUN_EXECUTION_DOCS,
    LIST_EXECUTIONS_DOCS,
    GET_EXECUTION_DOCS,
    DELETE_EXECUTION_DOCS,
)
from app.swagger.reports import (
    HTML_REPORT_DOCS,
    SUMMARY_REPORT_DOCS,
    METADATA_REPORT_DOCS,
)
from app.swagger.logs import (
    STDOUT_LOG_DOCS,
    STDERR_LOG_DOCS,
)

router = APIRouter()

# Pasta onde os uploads ficam armazenados
SCRIPTS_DIR = Path("/scripts")


# ==========================================================
# Upload de Script
# ==========================================================

@router.post(
    "/scripts/upload",
    response_model=ScriptUploadResponse,
    **UPLOAD_SCRIPT_DOCS,
)
async def upload_script(file: UploadFile = File(...)):
    if not file.filename.endswith(".js"):
        raise HTTPException(
            status_code=400,
            detail="Apenas arquivos .js são aceitos."
        )
    execution_id = str(uuid.uuid4())[:8]

    execution_folder = SCRIPTS_DIR / execution_id
    execution_folder.mkdir(parents=True, exist_ok=True)

    script_path = execution_folder / file.filename

    with open(script_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "execution_id": execution_id,
        "filename": file.filename,
        "message": "Script uploaded successfully."
    }


# ==========================================================
# Executa um teste
# ==========================================================

@router.post(
    "/executions/{execution_id}/run",
    response_model=ExecutionResponse,
    **RUN_EXECUTION_DOCS,
)
def execute_script(
    execution_id: str,
    request: ExecutionRequest = Body(
        openapi_examples={
            "constant_vus": {
                "summary": "Teste com VUs constantes",
                "description": "10 usuários virtuais durante 2 minutos.",
                "value": {
                    "test_name": "Benchmark QuickPizza - 2 minutos",
                    "application": "quickpizza",
                    "environment": "benchmark",
                    "vus": 10,
                    "duration": "2m"
                }
            },
            "ramp_test": {
                "summary": "Teste em rampa",
                "description": "Ramp-up de 10 até 100 VUs e depois ramp-down.",
                "value": {
                    "test_name": "Ramp Test API Login",
                    "application": "login-api",
                    "environment": "homolog",
                    "stages": [
                        {"duration": "1m", "target": 10},
                        {"duration": "2m", "target": 50},
                        {"duration": "2m", "target": 100},
                        {"duration": "1m", "target": 0}
                    ]
                }
            }
        }
    )
):
    upload_folder = SCRIPTS_DIR / execution_id

    if not upload_folder.exists():
        raise HTTPException(
            status_code=404,
            detail="Script não encontrado."
        )

    return run_script(execution_id, request)

# ==========================================================
# Reexecuta um teste
# ==========================================================

@router.post(
    "/executions/{execution_id}/rerun",
    response_model=ExecutionResponse,
    **RERUN_EXECUTION_DOCS,
)
def rerun_script(execution_id: str):
    execution = get_execution(execution_id)

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execução não encontrada."
        )

    return rerun_execution(execution_id)


# ==========================================================
# Lista todas as execuções
# ==========================================================

@router.get(
    "/executions",
    response_model=List[ExecutionListItem],
    **LIST_EXECUTIONS_DOCS
)
def get_executions():
    return list_executions()


# ==========================================================
# Detalhes de uma execução
# ==========================================================

@router.get(
    "/executions/{execution_id}",
    response_model=ExecutionDetailsResponse,
    **GET_EXECUTION_DOCS,
)
def get_execution_details(execution_id: str):
    execution = get_execution(execution_id)

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execução não encontrada."
        )

    return execution

# ==========================================================
# Exclui uma execução
# ==========================================================

@router.delete(
    "/executions/{execution_id}",
    **DELETE_EXECUTION_DOCS,
)
def remove_execution(execution_id: str):
    execution = get_execution(execution_id)

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execução não encontrada."
        )

    return delete_execution(execution_id)


# ==========================================================
# Download do HTML Report
# ==========================================================

@router.get(
    "/executions/{execution_id}/report/html",
    **HTML_REPORT_DOCS,
)
def download_html_report(execution_id: str):
    report = get_execution_file(execution_id, "report")

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="HTML Report não encontrado."
        )

    return FileResponse(
        path=report,
        media_type="text/html",
        filename=f"{execution_id}-report.html",
    )


# ==========================================================
# Download do Summary JSON
# ==========================================================

@router.get(
    "/executions/{execution_id}/report/summary",
    **SUMMARY_REPORT_DOCS,
)
def download_summary(execution_id: str):
    summary = get_execution_file(execution_id, "summary")

    if summary is None:
        raise HTTPException(
            status_code=404,
            detail="Summary não encontrado."
        )

    return FileResponse(
        path=summary,
        media_type="application/json",
        filename=f"{execution_id}-summary.json",
    )


# ==========================================================
# Download do stdout.log
# ==========================================================

@router.get(
    "/executions/{execution_id}/logs/stdout",
    **STDOUT_LOG_DOCS,
)
def download_stdout(execution_id: str):
    stdout = get_execution_file(execution_id, "stdout")

    if stdout is None:
        raise HTTPException(
            status_code=404,
            detail="stdout.log não encontrado."
        )

    return FileResponse(
        path=stdout,
        media_type="text/plain",
        filename=f"{execution_id}-stdout.log",
    )


# ==========================================================
# Download do stderr.log
# ==========================================================

@router.get(
    "/executions/{execution_id}/logs/stderr",
    **STDERR_LOG_DOCS
)
def download_stderr(execution_id: str):
    stderr = get_execution_file(execution_id, "stderr")

    if stderr is None:
        raise HTTPException(
            status_code=404,
            detail="stderr.log não encontrado."
        )

    return FileResponse(
        path=stderr,
        media_type="text/plain",
        filename=f"{execution_id}-stderr.log",
    )


# ==========================================================
# Download do metadata.json
# ==========================================================

@router.get(
    "/executions/{execution_id}/report/metadata",
    **METADATA_REPORT_DOCS
)
def download_metadata(execution_id: str):
    metadata = get_execution_file(execution_id, "metadata")

    if metadata is None:
        raise HTTPException(
            status_code=404,
            detail="metadata.json não encontrado."
        )

    return FileResponse(
        path=metadata,
        media_type="application/json",
        filename=f"{execution_id}-metadata.json",
    )