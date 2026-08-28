from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Stress Test Platform",
    version="0.1.0"
)

app.include_router(router)