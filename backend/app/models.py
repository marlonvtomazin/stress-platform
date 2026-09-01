from pydantic import BaseModel, Field
from typing import List, Optional


class Stage(BaseModel):
    duration: str = Field(
        description="Tempo de duração da etapa.",
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
        description="Ambiente da execução.",
        examples=["benchmark"]
    )

    vus: Optional[int] = Field(
        default=None,
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
        description="Ramp-up / Ramp-down do teste."
    )