from pathlib import Path
from datetime import datetime
import json

from app.models import ExecutionRequest

def get_execution_status(exit_code: int) -> str:
    """
    Traduz o exit code do k6 para um status da plataforma.
    """

    if exit_code == 0:
        return "SUCCESS"

    # k6 retorna 99 quando algum threshold falha.
    if exit_code == 99:
        return "THRESHOLD_FAILED"

    return "ERROR"


def create_metadata(
    execution_id: str,
    config: ExecutionRequest,
    execution_folder: Path,
    exit_code: int,
    started_at: datetime,
    finished_at: datetime,
):
    
    
    """
    Lê o summary.json gerado pelo k6 e cria o metadata.json da execução.
    """

    summary_path = execution_folder / "summary.json"

    summary = {}

    if summary_path.exists():
        with open(summary_path, "r", encoding="utf-8") as file:
            summary = json.load(file)

    metrics = summary.get("metrics", {})

    metadata = {
        "execution_id": execution_id,

        "test_name": config.test_name,
        "application": config.application,
        "environment": config.environment,

        "status": get_execution_status(exit_code),

        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),

        "duration_seconds": round(
            (finished_at - started_at).total_seconds(),
            2,
        ),

        "exit_code": exit_code,

        "config": {
            "vus": config.vus,
            "duration": config.duration,
            "stages": (
                [stage.model_dump() for stage in config.stages]
                if config.stages
                else None
            ),
        },

        "summary": {
            "total_requests": metrics.get("http_reqs", {})
                .get("values", {})
                .get("count"),

            "error_rate": round(
                metrics.get("http_req_failed", {})
                .get("values", {})
                .get("rate", 0) * 100,
                2,
            ),

            "avg_response_time": round(
                metrics.get("http_req_duration", {})
                .get("values", {})
                .get("avg", 0),
                2,
            ),

            "p90": round(
                metrics.get("http_req_duration", {})
                .get("values", {})
                .get("p(90)", 0),
                2,
            ),

            "p95": round(
                metrics.get("http_req_duration", {})
                .get("values", {})
                .get("p(95)", 0),
                2,
            ),

            "max_response_time": round(
                metrics.get("http_req_duration", {})
                .get("values", {})
                .get("max", 0),
                2,
            ),
        },

        "files": {
            "script": next(
                execution_folder.glob("*.js")
            ).name,

            "summary": "summary.json",
            "stdout": "stdout.log",
            "stderr": "stderr.log",
            "report": "report/report.html",
        },
    }

    metadata_path = execution_folder / "metadata.json"

    with open(metadata_path, "w", encoding="utf-8") as file:
        json.dump(
            metadata,
            file,
            indent=2,
            ensure_ascii=False,
        )

    return metadata