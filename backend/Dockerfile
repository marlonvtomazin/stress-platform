# ---------- Stage 1 - Build xk6 ----------
FROM golang:1.25 AS xk6-builder

RUN go install go.k6.io/xk6/cmd/xk6@latest

RUN xk6 build v2.2.0 \
    --with github.com/grafana/xk6-output-influxdb

# ---------- Stage 2 - FastAPI ----------
FROM python:3.12-slim

WORKDIR /app

# Copia o binário do k6 compilado
COPY --from=xk6-builder /go/k6 /usr/bin/k6

# Dependências do sistema
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código da aplicação
COPY app ./app

# Pastas da plataforma
RUN mkdir -p /scripts /executions

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]