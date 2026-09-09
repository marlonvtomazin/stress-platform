RUN_EXECUTION_DOCS = {
    "tags": ["Executions"],
    "summary": "Executar teste k6",
    "description": """
    Executa um script **k6** previamente enviado para a plataforma.

    ### Como funciona

    1. Faça upload do script utilizando `POST /scripts/upload`.
    2. Utilize o `execution_id` retornado no upload.
    3. Informe a configuração do teste no corpo da requisição.

    ### Tipos de execução suportados

    - **VUs constantes:** `vus` + `duration`.
    - **Ramp-up/Ramp-down:** `stages`.
    """,
    "responses": {
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
}

RERUN_EXECUTION_DOCS = {
    "tags": ["Executions"],
    "summary": "Reexecutar teste",
    "description": """
    Executa novamente um teste utilizando o mesmo script e a mesma configuração da execução original.

    ### Como funciona

    1. Localiza o `metadata.json` da execução.
    2. Copia o script original para uma nova execução.
    3. Cria um novo `execution_id`.
    4. Executa o teste novamente com os mesmos parâmetros (`vus`, `duration` ou `stages`).

    O histórico da execução original é preservado.
""",
    "responses": {
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
}

LIST_EXECUTIONS_DOCS = {
    "tags": ["Executions"],
    "summary": "Listar execuções",
    "description": """
    Retorna todas as execuções disponíveis na plataforma.
    
    ### Ordenação
    
    As execuções são retornadas da **mais recente para a mais antiga** com base no campo `started_at`.
    
    ### Informações retornadas
    
    Cada item da lista contém um resumo da execução, ideal para exibição em tabelas e dashboards.
    """,
        "responses": {
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
}

GET_EXECUTION_DOCS = {
    "tags": ["Executions"],
    "summary": "Detalhes da execução",
    "description": """
    Retorna todas as informações de uma execução específica.

    ### Informações retornadas

    - Dados gerais da execução (`test_name`, `application`, `environment`).
    - Status da execução (`SUCCESS`, `THRESHOLD_FAILED` ou `ERROR`).
    - Configuração utilizada (`vus`, `duration` ou `stages`).
    - Resumo das métricas coletadas pelo k6.
    - Lista de arquivos gerados e disponibilidade dos artifacts para download.
    """,
    "responses": {
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
}

DELETE_EXECUTION_DOCS = {
    "tags": ["Executions"],
    "summary": "Excluir execução",
    "description": """
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
    "responses": {
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
}
