from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html

from app.routes import router
from app.docs import get_openapi_pt, get_openapi_en

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

# ==============================
# CORS - React Frontend
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/openapi.json", include_in_schema=False)
def openapi_pt():
    return get_openapi_pt(app)


@app.get("/openapi-en.json", include_in_schema=False)
def openapi_en():
    return get_openapi_en(app)


@app.get("/docs", include_in_schema=False)
def swagger_pt():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Stress Platform API (PT-BR)",
    )


@app.get("/docs/en", include_in_schema=False)
def swagger_en():
    return get_swagger_ui_html(
        openapi_url="/openapi-en.json",
        title="Stress Platform API (English)",
    )