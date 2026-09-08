from fastapi.openapi.utils import get_openapi


def get_openapi_pt(app):
    return get_openapi(
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
    )


def get_openapi_en(app):
    # Por enquanto reaproveita o schema em português.
    # Na Sprint 5 vamos traduzir summaries e descriptions.
    return get_openapi_pt(app)