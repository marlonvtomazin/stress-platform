from typing import List, Optional

from pydantic import BaseModel, Field

# ==========================================================
# REQUEST MODELS
# ==========================================================

class Stage(BaseModel):
    duration: str = Field(
        description="Duração da etapa do teste.",
        examples=["1m"]
    )

    target: int = Field(
        ge=0,
        description="Quantidade de usuários virtuais (VUs) ao final da etapa.",
        examples=[50]
    )


class ExecutionRequest(BaseModel):
    test_name: str = Field(
        description="Nome amigável da execução.",
        examples=["Benchmark QuickPizza - 2 minutos"]
    )

    application: str = Field(
        description="Aplicação ou sistema testado.",
        examples=["quickpizza"]
    )

    environment: str = Field(
        description="Ambiente onde o teste será executado.",
        examples=["benchmark"]
    )

    vus: Optional[int] = Field(
        default=None,
        ge=1,
        description="Quantidade fixa de usuários virtuais.",
        examples=[10]
    )

    duration: Optional[str] = Field(
        default=None,
        description="Duração do teste quando utilizar VUs constantes.",
        examples=["2m"]
    )

    stages: Optional[List[Stage]] = Field(
        default=None,
        description="Lista de etapas para execução em ramp-up/ramp-down."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "test_name": "Benchmark QuickPizza - 2 minutos",
                "application": "quickpizza",
                "environment": "benchmark",
                "vus": 10,
                "duration": "2m"
            }
        }
    }


# ==========================================================
# RESPONSE MODELS
# ==========================================================

class ScriptUploadResponse(BaseModel):
    execution_id: str = Field(
        description="Identificador único da execução.",
        examples=["a6a104d0"]
    )

    filename: str = Field(
        description="Nome do script enviado.",
        examples=["benchmark.js"]
    )

    message: str = Field(
        description="Mensagem de sucesso.",
        examples=["Script uploaded successfully."]
    )


class ExecutionSummary(BaseModel):
    total_requests: int = Field(
        description="Quantidade total de requisições executadas.",
        examples=[1189]
    )

    error_rate: float = Field(
        description="Percentual de requisições com falha.",
        examples=[1.82]
    )

    avg_response_time: float = Field(
        description="Tempo médio de resposta (ms).",
        examples=[172.45]
    )

    p90: float = Field(
        description="Percentil 90 do tempo de resposta (ms).",
        examples=[193.87]
    )

    p95: float = Field(
        description="Percentil 95 do tempo de resposta (ms).",
        examples=[205.16]
    )

    max_response_time: float = Field(
        description="Maior tempo de resposta registrado (ms).",
        examples=[691.23]
    )


class ExecutionResponse(BaseModel):
    execution_id: str = Field(
        description="Identificador da execução criada.",
        examples=["6d1834d1"]
    )

    status: str = Field(
        description="Status final da execução.",
        examples=["SUCCESS"]
    )

    exit_code: int = Field(
        description="Código de saída retornado pelo k6.",
        examples=[0]
    )

    duration_seconds: float = Field(
        description="Tempo total da execução em segundos.",
        examples=[120.43]
    )

    summary: ExecutionSummary


class ExecutionListItem(BaseModel):
    execution_id: str = Field(examples=["6d1834d1"])

    test_name: str = Field(
        examples=["QuickPizza Benchmark - 2 minutos"]
    )

    application: str = Field(examples=["quickpizza"])

    environment: str = Field(examples=["benchmark"])

    status: str = Field(examples=["SUCCESS"])

    started_at: str = Field(
        description="Data e hora de início da execução.",
        examples=["2026-09-04T00:24:10Z"]
    )

    finished_at: str = Field(
        description="Data e hora de término da execução.",
        examples=["2026-09-04T00:26:12Z"]
    )

    duration_seconds: float = Field(examples=[122.30])

    total_requests: int = Field(examples=[1189])

    error_rate: float = Field(examples=[1.82])

    avg_response_time: float = Field(examples=[172.45])

    p95: float = Field(examples=[205.16])


class ExecutionConfig(BaseModel):
    vus: Optional[int] = Field(
        default=None,
        description="Quantidade de usuários virtuais utilizada na execução.",
        examples=[10]
    )

    duration: Optional[str] = Field(
        default=None,
        description="Duração da execução.",
        examples=["2m"]
    )

    stages: Optional[List[Stage]] = Field(
        default=None,
        description="Ramp-up/Ramp-down utilizado na execução."
    )


class ExecutionFiles(BaseModel):
    script: str = Field(
        examples=["benchmark.js"]
    )

    summary: str = Field(
        examples=["summary.json"]
    )

    stdout: str = Field(
        examples=["stdout.log"]
    )

    stderr: str = Field(
        examples=["stderr.log"]
    )

    report: str = Field(
        examples=["report/report.html"]
    )


class Artifact(BaseModel):
    available: bool = Field(
        description="Indica se o arquivo está disponível para download.",
        examples=[True]
    )

    endpoint: str = Field(
        description="Endpoint para download do artifact.",
        examples=["/executions/a6a104d0/report/html"]
    )


class ExecutionArtifacts(BaseModel):
    html_report: Artifact
    summary: Artifact
    metadata: Artifact
    stdout: Artifact
    stderr: Artifact


class ExecutionDetailsResponse(BaseModel):
    execution_id: str

    test_name: str

    application: str

    environment: str

    status: str

    started_at: str

    finished_at: str

    duration_seconds: float

    exit_code: int

    config: ExecutionConfig

    summary: ExecutionSummary

    files: ExecutionFiles

    artifacts: ExecutionArtifacts