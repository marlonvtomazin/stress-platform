from typing import List, Optional

from pydantic import BaseModel, Field


class Stage(BaseModel):
    duration: str = Field(
        description="Duração da etapa do teste.",
        examples=["1m"]
    )

    target: int = Field(
        description="Quantidade de VUs alvo da etapa.",
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
        description="Quantidade fixa de usuários virtuais.",
        examples=[10]
    )

    duration: Optional[str] = Field(
        default=None,
        description="Duração do teste quando usar VUs constantes.",
        examples=["2m"]
    )

    stages: Optional[List[Stage]] = Field(
        default=None,
        description="Configuração de ramp-up/ramp-down do teste."
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