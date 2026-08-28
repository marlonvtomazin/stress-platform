from fastapi import APIRouter, UploadFile, File
from app.executor import save_script

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Stress Test Platform API"}


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.get("/executions")
def executions():
    return []


@router.post("/executions/upload")
async def upload_script(file: UploadFile = File(...)):
    result = save_script(file.filename, await file.read())

    return {
        "message": "Script uploaded successfully",
        **result
    }