UPLOAD_SCRIPT_DOCS = {
    "tags": ["Scripts"],
    "summary": "Upload de script k6",
    "description": """
    Envia um script **k6** (`.js`) para a plataforma.

    ### Fluxo

    1. Gera um `execution_id`.
    2. Salva o script em `/scripts/{execution_id}`.
    3. Retorna o `execution_id` para execução do teste.
    """,
    "responses": {
        200: {
            "description": "Script enviado com sucesso."
        },
        400: {
            "description": "Arquivo inválido."
        }
    }
}