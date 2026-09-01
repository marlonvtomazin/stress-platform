FROM python:3.12-slim

WORKDIR /app

# Instala k6 v2.2.0
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    ca-certificates \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://dl.k6.io/key.gpg | gpg --dearmor -o /etc/apt/keyrings/k6-archive-keyring.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" \
       > /etc/apt/sources.list.d/k6.list \
    && apt-get update \
    && apt-get install -y k6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Recursos (HTML Reporter)
COPY resources ./resources

RUN mkdir -p /scripts

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]