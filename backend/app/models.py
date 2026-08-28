from pydantic import BaseModel
from typing import List, Optional


class Stage(BaseModel):
    duration: str
    target: int


class ExecutionRequest(BaseModel):
    test_name: str
    application: str
    environment: str

    vus: Optional[int] = None
    duration: Optional[str] = None

    stages: Optional[List[Stage]] = None