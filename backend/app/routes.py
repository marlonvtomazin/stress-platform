from pathlib import Path
from typing import List
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from fastapi.responses import FileResponse

from app.models import ExecutionRequest
from app.runner import run_script
from app.services.execution_service import (
    list_executions,
    get_execution,
    get_execution_file,
    rerun_execution,
    delete_execution,
)

from app.models import (
    ExecutionRequest,
    ScriptUploadResponse,
    ExecutionResponse,
    ExecutionListItem,
    ExecutionDetailsResponse,
)

router = APIRouter()

# Pasta onde os uploads ficam armazenados
SCRIPTS_DIR = Path("/scripts")


# ==========================================================
# Upload de Script
# ==========================================================

@router.post(
    "/scripts/upload",
    response_model=ScriptUploadResponse,
    tags=["Scripts"],
    summary="Upload de script k6",
    description="""
Envia um script **k6** (`.js`) para a plataforma.

### Fluxo

1. Gera um `execution_id`.
2. Salva o script em `/scripts/{execution_id}`.
3. Retorna o `execution_id` para execução do teste.
""",
    responses={
        200: {
            "description": "Script enviado com sucesso.",
            "content": {
                "application/json": {
                    "example": {
                        "execution_id": "a6a104d0",
                        "filename": "benchmark.js",
                        "message": "Script uploaded successfully."
                    }
                }
            }
        },
        400: {
            "description": "Arquivo inválido. Apenas scripts .js são aceitos."
        }
    }
)
async def upload_script(file: UploadFile = File(...)):
    if not file.filename.endswith(".js"):
        raise HTTPException(
            status_code=400,
            detail="Apenas arquivos .js são aceitos."
        )
    execution_id = str(uuid.uuid4())[:8]

    execution_folder = SCRIPTS_DIR / execution_id
    execution_folder.mkdir(parents=True, exist_ok=True)

    script_path = execution_folder / file.filename

    with open(script_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "execution_id": execution_id,
        "filename": file.filename,
        "message": "Script uploaded successfully."
    }


# ==========================================================
# Executa um teste
# ==========================================================

@router.post(
    "/executions/{execution_id}/run",
    response_model=ExecutionResponse,
    tags=["Executions"],
    summary="Executar teste k6",
    description="""
Executa um script **k6** previamente enviado para a plataforma.

### Como funciona

1. Faça upload do script utilizando `POST /scripts/upload`.
2. Utilize o `execution_id` retornado no upload.
3. Informe a configuração do teste no corpo da requisição.

### Tipos de execução suportados

- **VUs constantes:** `vus` + `duration`.
- **Ramp-up/Ramp-down:** `stages`.
""",
    responses={
        200: {
            "description": "Teste executado com sucesso.",
            "content": {
                "application/json": {
                    "example": {
                        "execution_id": "a6a104d0",
                        "status": "THRESHOLD_FAILED",
                        "exit_code": 99,
                        "duration_seconds": 122.08,
                        "summary": {
                            "total_requests": 223,
                            "error_rate": 21.52,
                            "avg_response_time": 746.88,
                            "p90": 950.42,
                            "p95": 1302.01,
                            "max_response_time": 19457.02
                        }
                    }
                }
            }
        },
        404: {
            "description": "Script não encontrado para o execution_id informado."
        },
        400: {
            "description": "Configuração da execução inválida."
        }
    }
)
def execute_script(
    execution_id: str,
    request: ExecutionRequest = Body(
        openapi_examples={
            "constant_vus": {
                "summary": "Teste com VUs constantes",
                "description": "10 usuários virtuais durante 2 minutos.",
                "value": {
                    "test_name": "Benchmark QuickPizza - 2 minutos",
                    "application": "quickpizza",
                    "environment": "benchmark",
                    "vus": 10,
                    "duration": "2m"
                }
            },
            "ramp_test": {
                "summary": "Teste em rampa",
                "description": "Ramp-up de 10 até 100 VUs e depois ramp-down.",
                "value": {
                    "test_name": "Ramp Test API Login",
                    "application": "login-api",
                    "environment": "homolog",
                    "stages": [
                        {"duration": "1m", "target": 10},
                        {"duration": "2m", "target": 50},
                        {"duration": "2m", "target": 100},
                        {"duration": "1m", "target": 0}
                    ]
                }
            }
        }
    )
):
    upload_folder = SCRIPTS_DIR / execution_id

    if not upload_folder.exists():
        raise HTTPException(
            status_code=404,
            detail="Script não encontrado."
        )

    return run_script(execution_id, request)

# ==========================================================
# Reexecuta um teste
# ==========================================================

@router.post(
    "/executions/{execution_id}/rerun",
    response_model=ExecutionResponse,
    tags=["Executions"],
    summary="Reexecutar teste",
    description="""
Executa novamente um teste utilizando o mesmo script e a mesma configuração da execução original.

### Como funciona

1. Localiza o `metadata.json` da execução.
2. Copia o script original para uma nova execução.
3. Cria um novo `execution_id`.
4. Executa o teste novamente com os mesmos parâmetros (`vus`, `duration` ou `stages`).

O histórico da execução original é preservado.
""",
    responses={
        200: {
            "description": "Nova execução criada com sucesso.",
            "content": {
                "application/json": {
                    "example": {
                        "execution_id": "6d1834d1",
                        "original_execution_id": "a6a104d0",
                        "status": "SUCCESS",
                        "exit_code": 0,
                        "duration_seconds": 120.43,
                        "summary": {
                            "total_requests": 1189,
                            "error_rate": 1.82,
                            "avg_response_time": 172.45,
                            "p90": 193.87,
                            "p95": 205.16,
                            "max_response_time": 691.23
                        }
                    }
                }
            }
        },
        400: {
            "description": "A execução não possui configuração válida para rerun."
        },
        404: {
            "description": "Execução não encontrada."
        }
    }
)
def rerun_script(execution_id: str):
    execution = get_execution(execution_id)

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execução não encontrada."
        )

    return rerun_execution(execution_id)


# ==========================================================
# Lista todas as execuções
# ==========================================================

@router.get(
    "/executions",
    response_model=List[ExecutionListItem],
    tags=["Executions"],
    summary="Listar execuções",
    description="""
Retorna todas as execuções disponíveis na plataforma.

### Ordenação

As execuções são retornadas da **mais recente para a mais antiga** com base no campo `started_at`.

### Informações retornadas

Cada item da lista contém um resumo da execução, ideal para exibição em tabelas e dashboards.
""",
    responses={
        200: {
            "description": "Lista de execuções retornada com sucesso.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "execution_id": "6d1834d1",
                            "test_name": "QuickPizza Benchmark - 2 minutos",
                            "application": "quickpizza",
                            "environment": "benchmark",
                            "status": "SUCCESS",
                            "started_at": "2026-09-04T00:24:10Z",
                            "finished_at": "2026-09-04T00:26:12Z",
                            "duration_seconds": 122.3,
                            "total_requests": 1189,
                            "error_rate": 1.82,
                            "avg_response_time": 172.45,
                            "p95": 205.16
                        },
                        {
                            "execution_id": "a6a104d0",
                            "test_name": "Benchmark QuickPizza - 2 minutos",
                            "application": "quickpizza",
                            "environment": "benchmark",
                            "status": "THRESHOLD_FAILED",
                            "started_at": "2026-09-04T00:03:11Z",
                            "finished_at": "2026-09-04T00:05:13Z",
                            "duration_seconds": 122.08,
                            "total_requests": 223,
                            "error_rate": 21.52,
                            "avg_response_time": 746.88,
                            "p95": 1302.01
                        }
                    ]
                }
            }
        }
    }
)
def get_executions():
    return list_executions()


# ==========================================================
# Detalhes de uma execução
# ==========================================================

@router.get(
    "/executions/{execution_id}",
    response_model=ExecutionDetailsResponse,
    tags=["Executions"],
    summary="Detalhes da execução",
    description="""
Retorna todas as informações de uma execução específica.

### Informações retornadas

- Dados gerais da execução (`test_name`, `application`, `environment`).
- Status da execução (`SUCCESS`, `THRESHOLD_FAILED` ou `ERROR`).
- Configuração utilizada (`vus`, `duration` ou `stages`).
- Resumo das métricas coletadas pelo k6.
- Lista de arquivos gerados e disponibilidade dos artifacts para download.
""",
    responses={
        200: {
            "description": "Detalhes da execução retornados com sucesso.",
            "content": {
                "application/json": {
                    "example": {
                        "execution_id": "a6a104d0",
                        "test_name": "QuickPizza Benchmark - 2 minutos",
                        "application": "quickpizza",
                        "environment": "benchmark",
                        "status": "THRESHOLD_FAILED",
                        "started_at": "2026-09-04T00:03:11Z",
                        "finished_at": "2026-09-04T00:05:13Z",
                        "duration_seconds": 122.08,
                        "exit_code": 99,
                        "config": {
                            "vus": 3,
                            "duration": "2m",
                            "stages": None
                        },
                        "summary": {
                            "total_requests": 223,
                            "error_rate": 21.52,
                            "avg_response_time": 746.88,
                            "p90": 950.42,
                            "p95": 1302.01,
                            "max_response_time": 19457.02
                        },
                        "files": {
                            "script": "benchmark.js",
                            "summary": "summary.json",
                            "stdout": "stdout.log",
                            "stderr": "stderr.log",
                            "report": "report/report.html"
                        },
                        "artifacts": {
                            "html_report": {
                                "available": True,
                                "endpoint": "/executions/a6a104d0/report/html"
                            },
                            "summary": {
                                "available": True,
                                "endpoint": "/executions/a6a104d0/report/summary"
                            },
                            "metadata": {
                                "available": True,
                                "endpoint": "/executions/a6a104d0/report/metadata"
                            },
                            "stdout": {
                                "available": True,
                                "endpoint": "/executions/a6a104d0/logs/stdout"
                            },
                            "stderr": {
                                "available": True,
                                "endpoint": "/executions/a6a104d0/logs/stderr"
                            }
                        }
                    }
                }
            }
        },
        404: {
            "description": "Execução não encontrada."
        }
    }
)
def get_execution_details(execution_id: str):
    execution = get_execution(execution_id)

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execução não encontrada."
        )

    return execution

# ==========================================================
# Exclui uma execução
# ==========================================================

@router.delete(
    "/executions/{execution_id}",
    tags=["Executions"],
    summary="Excluir execução",
    description="""
Remove uma execução da plataforma.

### O que é removido

- `metadata.json`
- `summary.json`
- `stdout.log`
- `stderr.log`
- `report/report.html`
- Script original armazenado em `/scripts/{execution_id}`.

A operação é permanente e não pode ser desfeita.
""",
    responses={
        200: {
            "description": "Execução removida com sucesso.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Execution deleted successfully.",
                        "execution_id": "a6a104d0"
                    }
                }
            }
        },
        404: {
            "description": "Execução não encontrada."
        }
    }
)
def remove_execution(execution_id: str):
    execution = get_execution(execution_id)

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execução não encontrada."
        )

    return delete_execution(execution_id)


# ==========================================================
# Download do HTML Report
# ==========================================================

@router.get(
    "/executions/{execution_id}/report/html",
    tags=["Reports"],
    summary="Download HTML Report",
    description="""
Baixa o relatório HTML gerado automaticamente pelo **k6-reporter**.

### Conteúdo do relatório

O HTML Report contém um resumo visual da execução, incluindo:

- Tempo de resposta.
- Throughput.
- Error Rate.
- Checks.
- Métricas do k6.

O arquivo pode ser aberto diretamente no navegador.
""",
    responses={
        200: {
            "description": "HTML Report encontrado e retornado com sucesso."
        },
        404: {
            "description": "HTML Report não encontrado para esta execução."
        }
    }
)
def download_html_report(execution_id: str):
    report = get_execution_file(execution_id, "report")

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="HTML Report não encontrado."
        )

    return FileResponse(
        path=report,
        media_type="text/html",
        filename=f"{execution_id}-report.html",
    )


# ==========================================================
# Download do Summary JSON
# ==========================================================

@router.get(
    "/executions/{execution_id}/report/summary",
    tags=["Reports"],
    summary="Download Summary JSON",
    description="""
Baixa o arquivo `summary.json` gerado pelo k6 ao final da execução.

### Conteúdo do arquivo

O summary contém todas as métricas calculadas pelo k6, incluindo:

- Requests.
- Response Time.
- Percentis (P90/P95).
- Error Rate.
- Checks.
- Métricas customizadas.
""",
    responses={
        200: {
            "description": "Summary JSON encontrado e retornado com sucesso."
        },
        404: {
            "description": "Summary JSON não encontrado para esta execução."
        }
    }
)
def download_summary(execution_id: str):
    summary = get_execution_file(execution_id, "summary")

    if summary is None:
        raise HTTPException(
            status_code=404,
            detail="Summary não encontrado."
        )

    return FileResponse(
        path=summary,
        media_type="application/json",
        filename=f"{execution_id}-summary.json",
    )


# ==========================================================
# Download do stdout.log
# ==========================================================

@router.get(
    "/executions/{execution_id}/logs/stdout",
    tags=["Logs"],
    summary="Download stdout.log",
    description="""
Baixa o arquivo `stdout.log` gerado durante a execução do teste.

### Conteúdo do arquivo

O `stdout.log` contém a saída padrão do k6, incluindo:

- Informações da execução.
- Progresso do teste.
- Resumo final do k6.
- Mensagens informativas e métricas exibidas no terminal.
""",
    responses={
        200: {
            "description": "stdout.log encontrado e retornado com sucesso."
        },
        404: {
            "description": "stdout.log não encontrado para esta execução."
        }
    }
)
def download_stdout(execution_id: str):
    stdout = get_execution_file(execution_id, "stdout")

    if stdout is None:
        raise HTTPException(
            status_code=404,
            detail="stdout.log não encontrado."
        )

    return FileResponse(
        path=stdout,
        media_type="text/plain",
        filename=f"{execution_id}-stdout.log",
    )


# ==========================================================
# Download do stderr.log
# ==========================================================

@router.get(
    "/executions/{execution_id}/logs/stderr",
    tags=["Logs"],
    summary="Download stderr.log",
    description="""
Baixa o arquivo `stderr.log` gerado durante a execução do teste.

### Conteúdo do arquivo

O `stderr.log` contém mensagens de erro e avisos produzidos pelo k6, como:

- Falhas de execução.
- Erros de importação de módulos.
- Problemas de conexão.
- Thresholds e mensagens de warning.
""",
    responses={
        200: {
            "description": "stderr.log encontrado e retornado com sucesso."
        },
        404: {
            "description": "stderr.log não encontrado para esta execução."
        }
    }
)
def download_stderr(execution_id: str):
    stderr = get_execution_file(execution_id, "stderr")

    if stderr is None:
        raise HTTPException(
            status_code=404,
            detail="stderr.log não encontrado."
        )

    return FileResponse(
        path=stderr,
        media_type="text/plain",
        filename=f"{execution_id}-stderr.log",
    )


# ==========================================================
# Download do metadata.json
# ==========================================================

@router.get(
    "/executions/{execution_id}/report/metadata",
    tags=["Reports"],
    summary="Download Metadata JSON",
    description="""
Baixa o arquivo `metadata.json` da execução.

### Conteúdo do arquivo

O metadata reúne todas as informações da execução em um único documento:

- Informações gerais do teste.
- Configuração utilizada (`vus`, `duration` ou `stages`).
- Status da execução.
- Resumo das métricas.
- Arquivos gerados.
""",
    responses={
        200: {
            "description": "Metadata JSON encontrado e retornado com sucesso."
        },
        404: {
            "description": "Metadata JSON não encontrado para esta execução."
        }
    }
)
def download_metadata(execution_id: str):
    metadata = get_execution_file(execution_id, "metadata")

    if metadata is None:
        raise HTTPException(
            status_code=404,
            detail="metadata.json não encontrado."
        )

    return FileResponse(
        path=metadata,
        media_type="application/json",
        filename=f"{execution_id}-metadata.json",
    )