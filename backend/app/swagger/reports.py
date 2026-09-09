HTML_REPORT_DOCS = {
    "tags": ["Reports"],
    "summary": "Download HTML Report",
    "description": """
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
    "responses": {
        200: {
            "description": "HTML Report encontrado e retornado com sucesso."
        },
        404: {
            "description": "HTML Report não encontrado para esta execução."
        }
    }
}

SUMMARY_REPORT_DOCS = {
    "tags": ["Reports"],
    "summary": "Download Summary JSON",
    "description": """
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
    "responses": {
        200: {
            "description": "Summary JSON encontrado e retornado com sucesso."
        },
        404: {
            "description": "Summary JSON não encontrado para esta execução."
        }
    }
}

METADATA_REPORT_DOCS = {
    "tags": ["Reports"],
    "summary": "Download Metadata JSON",
    "description": """
    Baixa o arquivo `metadata.json` da execução.

    ### Conteúdo do arquivo

    O metadata reúne todas as informações da execução em um único documento:

    - Informações gerais do teste.
    - Configuração utilizada (`vus`, `duration` ou `stages`).
    - Status da execução.
    - Resumo das métricas.
    - Arquivos gerados.
    """,
    "responses": {
        200: {
            "description": "Metadata JSON encontrado e retornado com sucesso."
        },
        404: {
            "description": "Metadata JSON não encontrado para esta execução."
        }
    }
}