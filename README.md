# Stress Platform

Stress Platform is a local web application for running and monitoring **k6 stress tests** using Docker. It provides a simple interface to manage test executions while storing metrics in InfluxDB and visualizing them in Grafana.

## Architecture

The application is composed of four Docker containers:

| Service | Description |
|--------|-------------|
| Frontend | React + Vite application for interacting with the platform. |
| Backend | FastAPI API responsible for managing test executions. |
| InfluxDB | Time series database that stores k6 metrics. |
| Grafana | Dashboard application connected to InfluxDB for real-time metrics visualization. |

## Project Structure

```text
stress-platform/
├── backend/
├── frontend/
├── grafana/
│   └── provisioning/
├── executions/
├── scripts/
├── docker-compose.yml
├── .env.example
└── README.md
```

## Requirements

- Docker
- Docker Compose

## Getting Started

1. Clone the repository.

2. Create the environment file.

```bash
cp .env.example .env
```

3. Start the application.

```bash
docker compose up --build
```

## Available Services

| Service | URL |
|--------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8080 |
| API Documentation (Swagger) | http://localhost:8080/docs |
| Grafana | http://localhost:3001 |
| InfluxDB | http://localhost:8086 |

## Default Credentials

### Grafana

| Field | Value |
|------|-------|
| Username | `admin` |
| Password | `admin123` |

### InfluxDB

| Field | Value |
|------|-------|
| Username | `admin` |
| Password | `admin123` |
| Organization | `stress-platform` |
| Bucket | `k6-stress-tests` |

## Current Version (V1)

The current version includes:

- Docker Compose environment.
- React frontend.
- FastAPI backend.
- InfluxDB 2.7 initialized automatically.
- Grafana 12 initialized automatically.
- Persistent Docker volumes for Grafana and InfluxDB.

## Next Steps

The next development phase will add:

- k6 installation in the backend container.
- Script upload endpoint.
- Test execution API.
- Automatic metric ingestion into InfluxDB.
- Execution history.
- HTML report generation and download.