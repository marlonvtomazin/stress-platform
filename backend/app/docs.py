from fastapi.openapi.utils import get_openapi

OPENAPI_TAGS = [
    {
        "name": "Scripts",
        "description": "Upload e gerenciamento de scripts k6.",
    },
    {
        "name": "Executions",
        "description": "Execução, reexecução, consulta e remoção de testes de performance.",
    },
    {
        "name": "Reports",
        "description": "Download dos artefatos gerados pelo k6 (HTML Report, Summary e Metadata).",
    },
    {
        "name": "Logs",
        "description": "Download dos logs gerados durante a execução do teste.",
    },
]


def get_openapi_pt(app):
    schema = get_openapi(
        title="Stress Platform API",
        version="1.0.0-alpha",
        description="""
API para gerenciamento e execução de testes de performance utilizando k6.

## Funcionalidades

- Upload de scripts k6.
- Execução de testes.
- Reexecução (Rerun).
- Histórico de execuções.
- Download de HTML Report, Summary e Logs.
- Integração com Grafana e InfluxDB.
""",
        routes=app.routes,
        tags=OPENAPI_TAGS,
    )

    return schema


def get_openapi_en(app):
    schema = get_openapi(
        title="Stress Platform API",
        version="1.0.0-alpha",
        description="API for managing and running k6 performance tests.",
        routes=app.routes,
        tags=OPENAPI_TAGS,  # por enquanto reutiliza as mesmas tags
    )

    return schema