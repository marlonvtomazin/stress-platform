from pathlib import Path
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from fastapi.responses import FileResponse

from app.models import ExecutionRequest
from app.runner import run_script
from app.services.execution_service import (
    list_executions,
    get_execution,
    get_execution_file,
)

router = APIRouter()

# Pasta onde os uploads ficam armazenados
SCRIPTS_DIR = Path("/scripts")


# ==========================================================
# Upload de Script
# ==========================================================

@router.post("/scripts/upload")
async def upload_script(file: UploadFile = File(...)):
    execution_id = str(uuid.uuid4())[:8]

    execution_folder = SCRIPTS_DIR / execution_id
    execution_folder.mkdir(parents=True, exist_ok=True)

    script_path = execution_folder / file.filename

    with open(script_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "execution_id": execution_id,
        "filename": file.filename,
        "path": str(script_path),
    }


# ==========================================================
# Executa um teste
# ==========================================================

@router.post(
    "/executions/{execution_id}/run",
    summary="Executar teste k6",
    description="Executa um script k6 previamente enviado para a plataforma."
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
# Lista todas as execuções
# ==========================================================

@router.get("/executions")
def get_executions():
    return list_executions()


# ==========================================================
# Detalhes de uma execução
# ==========================================================

@router.get("/executions/{execution_id}")
def get_execution_details(execution_id: str):
    execution = get_execution(execution_id)

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execução não encontrada."
        )

    return execution


# ==========================================================
# Download do HTML Report
# ==========================================================

@router.get(
    "/executions/{execution_id}/report/html",
    summary="Download HTML Report",
    description="Retorna o relatório HTML gerado automaticamente pelo k6-reporter."
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

@router.get("/executions/{execution_id}/report/summary")
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

@router.get("/executions/{execution_id}/logs/stdout")
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

@router.get("/executions/{execution_id}/logs/stderr")
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

@router.get("/executions/{execution_id}/report/metadata")
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