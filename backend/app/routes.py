from fastapi import APIRouter

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