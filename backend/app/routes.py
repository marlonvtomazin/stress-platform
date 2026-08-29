from fastapi import APIRouter, UploadFile, File, HTTPException

from app.executor import save_script
from app.models import ExecutionRequest
from app.runner import run_script

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Stress Platform API"}


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.get("/executions")
def executions():
    return []


@router.post("/executions/upload")
async def upload_script(file: UploadFile = File(...)):
    if not file.filename.endswith(".js"):
        raise HTTPException(
            status_code=400,
            detail="Only .js k6 scripts are supported.",
        )

    result = save_script(file.filename, await file.read())

    return {
        "message": "Script uploaded successfully",
        **result,
    }


@router.post("/executions/{execution_id}/run")
def run_execution(
    execution_id: str,
    request: ExecutionRequest,
):
    try:
        return run_script(execution_id, request)

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )