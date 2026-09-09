STDOUT_LOG_DOCS = {
    "tags": ["Logs"],
    "summary": "Download stdout.log",
    "description": """
    Baixa o arquivo `stdout.log` gerado durante a execução do teste.

    ### Conteúdo do arquivo

    O `stdout.log` contém a saída padrão do k6, incluindo:

    - Informações da execução.
    - Progresso do teste.
    - Resumo final do k6.
    - Mensagens informativas e métricas exibidas no terminal.
    """,
    "responses": {
        200: {
            "description": "stdout.log encontrado e retornado com sucesso."
        },
        404: {
            "description": "stdout.log não encontrado para esta execução."
        }
    }
}

STDERR_LOG_DOCS = {
    "tags": ["Logs"],
    "summary": "Download stderr.log",
    "description": """
    Baixa o arquivo `stderr.log` gerado durante a execução do teste.

    ### Conteúdo do arquivo

    O `stderr.log` contém mensagens de erro e avisos produzidos pelo k6, como:

    - Falhas de execução.
    - Erros de importação de módulos.
    - Problemas de conexão.
    - Thresholds e mensagens de warning.
    """,
    "responses": {
        200: {
            "description": "stderr.log encontrado e retornado com sucesso."
        },
        404: {
            "description": "stderr.log não encontrado para esta execução."
        }
    }
}