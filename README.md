# 🚀 Stress Platform

Stress Platform is a local web application for executing, managing and monitoring **k6 load/stress tests** using Docker, FastAPI, InfluxDB and Grafana.

The platform allows you to upload k6 scripts, execute them through an API, automatically store execution artifacts (`summary.json`, `report.html`, logs, metadata), send metrics to InfluxDB and visualize everything in Grafana.

Current version: **v0.3 Alpha (Sprint 3)**

---

## ✨ Features

* ✅ Upload k6 scripts.
* ✅ Execute tests through FastAPI.
* ✅ Automatic metrics ingestion into **InfluxDB 2.7**.
* ✅ Grafana dashboard filtered by `execution_id`.
* ✅ Automatic generation of:

  * `summary.json`
  * `report/report.html`
  * `stdout.log`
  * `stderr.log`
  * `metadata.json`
* ✅ Execution history API.
* ✅ Download execution artifacts.

---

# 🏗️ Architecture

The application is composed of four Docker containers.

| Service      | Description                                            |
| ------------ | ------------------------------------------------------ |
| **Frontend** | React + Vite interface.                                |
| **Backend**  | FastAPI API responsible for uploads and k6 executions. |
| **InfluxDB** | Stores all k6 metrics.                                 |
| **Grafana**  | Dashboard for visualization and analysis.              |

---

## Execution Flow

```text
Upload Script (.js)
        │
        ▼
POST /scripts/upload
        │
        ▼
/scripts/{execution_id}/benchmark.js
        │
        ▼
POST /executions/{execution_id}/run
        │
        ▼
Runner (k6)
        │
        ├── Metrics → InfluxDB
        ├── summary.json
        ├── report/report.html
        ├── stdout.log
        ├── stderr.log
        └── metadata.json
        │
        ▼
/executions/{execution_id}/
```

---

# 📁 Project Structure

```text
stress-platform/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes.py
│   │   ├── runner.py
│   │   ├── metadata.py
│   │   ├── models.py
│   │   └── services/
│   │       └── execution_service.py
│   ├── resources/
│   │   └── k6-reporter.bundle.js
│   └── Dockerfile
│
├── frontend/
│
├── grafana/
│   └── provisioning/
│
├── scripts/
│   └── {execution_id}/
│       └── benchmark.js
│
├── executions/
│   └── {execution_id}/
│       ├── benchmark.js
│       ├── metadata.json
│       ├── summary.json
│       ├── stdout.log
│       ├── stderr.log
│       └── report/
│           └── report.html
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

# 🛠️ Requirements

* Docker Desktop
* Docker Compose

---

# ▶️ Getting Started

## 1. Clone the repository

```bash
git clone <repository-url>
cd stress-platform
```

## 2. Create the environment file

```bash
cp .env.example .env
```

## 3. Start the application

```bash
docker compose up --build
```

## 4. Rebuild only the backend

```bash
docker compose up --build -d backend
```

---

# 🌐 Available Services

| Service     | URL                        |
| ----------- | -------------------------- |
| Frontend    | http://localhost:3000      |
| Backend API | http://localhost:8080      |
| Swagger     | http://localhost:8080/docs |
| Grafana     | http://localhost:3001      |
| InfluxDB    | http://localhost:8086      |

---

# 🔑 Default Credentials

## Grafana

| Field    | Value      |
| -------- | ---------- |
| Username | `admin`    |
| Password | `admin123` |

## InfluxDB

| Field        | Value             |
| ------------ | ----------------- |
| Username     | `admin`           |
| Password     | `admin123`        |
| Organization | `stress-platform` |
| Bucket       | `k6-stress-tests` |

---

# ⚙️ k6 Integration

The backend executes **k6 v2.2.0** inside the backend container.

Metrics are sent using the **InfluxDB v1 compatibility API** (`-o influxdb`).

Current environment variables:

```env
K6_INFLUXDB_ADDR=http://influxdb:8086
K6_INFLUXDB_DB=k6-stress-tests
K6_INFLUXDB_USERNAME=admin
K6_INFLUXDB_PASSWORD=admin123
```

Every execution automatically sends these tags:

| Tag          | Example                          |
| ------------ | -------------------------------- |
| execution_id | a6a104d0                         |
| application  | quickpizza                       |
| environment  | benchmark                        |
| test_name    | Benchmark QuickPizza - 2 minutos |
| platform     | stress-platform                  |

These tags are used by Grafana to filter dashboards.

---

# 📤 API Endpoints

## Upload Script

**POST**

```http
POST /scripts/upload
```

Content-Type:

```
multipart/form-data
```

Field:

| Field | Type       |
| ----- | ---------- |
| file  | File (.js) |

### Example Response

```json
{
  "execution_id": "a6a104d0",
  "filename": "benchmark.js",
  "path": "/scripts/a6a104d0/benchmark.js"
}
```

---

## Execute Script

**POST**

```http
POST /executions/{execution_id}/run
```

### Payload — Constant VUs (2 minutes)

```json
{
  "test_name": "Benchmark QuickPizza - 2 minutos",
  "application": "quickpizza",
  "environment": "benchmark",
  "vus": 10,
  "duration": "2m"
}
```

### Payload — Constant VUs (5 minutes)

```json
{
  "test_name": "Benchmark QuickPizza - 5 minutos",
  "application": "quickpizza",
  "environment": "benchmark",
  "vus": 20,
  "duration": "5m"
}
```

### Payload — Ramp Test

```json
{
  "test_name": "Ramp Test API Login",
  "application": "login-api",
  "environment": "homolog",
  "stages": [
    {
      "duration": "1m",
      "target": 10
    },
    {
      "duration": "2m",
      "target": 50
    },
    {
      "duration": "2m",
      "target": 100
    },
    {
      "duration": "1m",
      "target": 0
    }
  ]
}
```

> If the uploaded script already defines `options.stages`, they take precedence over `vus` and `duration`.

### Success Response

```json
{
  "execution_id": "a6a104d0",
  "status": "SUCCESS",
  "exit_code": 0,
  "summary_path": "/executions/a6a104d0/summary.json",
  "report_path": "/executions/a6a104d0/report/report.html",
  "metadata_path": "/executions/a6a104d0/metadata.json"
}
```

---

## List Executions

**GET**

```http
GET /executions
```

### Response

```json
[
  {
    "execution_id": "a6a104d0",
    "test_name": "Benchmark QuickPizza - 2 minutos",
    "application": "quickpizza",
    "environment": "benchmark",
    "status": "FAILED",
    "started_at": "2026-09-01T23:03:04.501366+00:00",
    "finished_at": "2026-09-01T23:05:09.096981+00:00",
    "duration_seconds": 124.6,
    "total_requests": 1191,
    "error_rate": 20.49,
    "avg_response_time": 163.84,
    "p95": 200.82
  }
]
```

---

## Execution Details

**GET**

```http
GET /executions/{execution_id}
```

### Response

```json
{
  "execution_id": "a6a104d0",
  "test_name": "Benchmark QuickPizza - 2 minutos",
  "application": "quickpizza",
  "environment": "benchmark",
  "status": "FAILED",
  "started_at": "2026-09-01T23:03:04.501366+00:00",
  "finished_at": "2026-09-01T23:05:09.096981+00:00",
  "duration_seconds": 124.6,
  "exit_code": 99,
  "summary": {
    "total_requests": 1191,
    "error_rate": 20.49,
    "avg_response_time": 163.84,
    "p90": 196.11,
    "p95": 200.82,
    "max_response_time": 248.57
  },
  "files": {
    "script": "benchmark.js",
    "summary": "summary.json",
    "stdout": "stdout.log",
    "stderr": "stderr.log",
    "report": "report/report.html"
  }
}
```

---

# 📥 Download Execution Artifacts

| Endpoint                        | Description             |
| ------------------------------- | ----------------------- |
| `GET /executions/{id}/report`   | Download HTML Report.   |
| `GET /executions/{id}/summary`  | Download summary.json.  |
| `GET /executions/{id}/metadata` | Download metadata.json. |
| `GET /executions/{id}/stdout`   | Download stdout.log.    |
| `GET /executions/{id}/stderr`   | Download stderr.log.    |

Example:

```http
GET /executions/a6a104d0/report
```

Returns:

```
Content-Type: text/html
```

---

# 📊 Execution Artifacts

Each execution stores its complete history.

```text
executions/
└── a6a104d0/
    ├── benchmark.js
    ├── metadata.json
    ├── summary.json
    ├── stdout.log
    ├── stderr.log
    └── report/
        └── report.html
```

## metadata.json

Stores execution metadata and summarized metrics.

```json
{
  "execution_id": "a6a104d0",
  "test_name": "Benchmark QuickPizza - 2 minutos",
  "application": "quickpizza",
  "environment": "benchmark",
  "status": "FAILED",
  "duration_seconds": 124.6,
  "summary": {
    "total_requests": 1191,
    "error_rate": 20.49,
    "avg_response_time": 163.84,
    "p95": 200.82
  }
}
```

## summary.json

Native k6 summary containing all metrics.

Examples:

* Requests
* Checks
* Thresholds
* P90 / P95
* HTTP metrics
* Iterations
* VUs

## report.html

Generated automatically using **k6-reporter**.

Contains:

* Overview
* Checks
* Thresholds
* Request metrics
* Percentiles
* Charts
* Timing breakdown

---

# 📈 Grafana Dashboard

The Grafana dashboard is automatically populated using InfluxDB.

## Dashboard Variables

| Variable       | Description            |
| -------------- | ---------------------- |
| `bucket`       | InfluxDB bucket.       |
| `execution_id` | Filters one execution. |

## Dashboard Panels

### Execution Information

* Test Name
* Application
* Environment

### Performance Overview

* Active VUs
* Throughput (req/s)
* Response Time
* Failed Requests/sec

### Summary Stats

* Total Requests
* Error Rate
* Average Response Time
* P90
* P95
* P99

### Request Breakdown

Grouped by:

* Request Name
* HTTP Status
* Total Requests
* Average Response Time
* Max Response Time

---

# 📦 InfluxDB Measurements

The dashboard currently uses these measurements:

| Measurement         | Description            |
| ------------------- | ---------------------- |
| `http_req_duration` | Response time metrics. |
| `http_reqs`         | Request counters.      |
| `http_req_failed`   | Error rate metric.     |
| `vus`               | Active virtual users.  |
| `vus_max`           | Configured VUs.        |
| `checks`            | Check results.         |
| `iterations`        | Iteration counter.     |

---

# 🧪 Example Benchmark Script

```javascript
import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  thresholds: {
    http_req_duration: ["p(95)<500"],
    http_req_failed: ["rate<0.20"],
  },
};

const BASE_URL = "https://quickpizza.grafana.com";

export default function () {
  const response = http.get(`${BASE_URL}/`);

  check(response, {
    "status esperado": (r) => r.status === 200,
  });

  sleep(1);
}
```

The runner automatically injects:

* HTML Report (`handleSummary`)
* Summary export
* Execution tags

No changes are required in user scripts.

---

# 📝 Execution Status

Current implementation:

| Status  | Description                                       |
| ------- | ------------------------------------------------- |
| SUCCESS | k6 finished with exit code `0`.                   |
| FAILED  | One or more thresholds failed (`exit_code != 0`). |

> Planned improvement: introduce `THRESHOLD_FAILED` and `ERROR` as separate execution states.

---

# 🔄 Development Workflow

### Upload a script

```bash
POST /scripts/upload
```

### Execute it

```bash
POST /executions/{execution_id}/run
```

### Open Grafana

```
http://localhost:3001
```

Select the `execution_id` variable.

### Download the report

```bash
GET /executions/{execution_id}/report
```

---

# 🚧 Roadmap

## ✅ Sprint 2

* Upload API.
* k6 Runner.
* InfluxDB integration.
* Grafana Dashboard.
* HTML Report generation.
* Summary generation.

## ✅ Sprint 3 (Current)

* Execution metadata.
* Execution history.
* Artifact download endpoints.
* Execution service.

## 🔜 Sprint 3.5

* Execution comparison.
* Dashboard deep link.
* Execution details endpoint improvements.

## 🔜 Sprint 4

* React UI for execution history.
* Compare executions screen.
* S3 artifact storage.
* PostgreSQL persistence.
* `xk6-output-influxdb` support (InfluxDB v2 native API).

---

# 👨‍💻 Technologies

| Technology     | Version |
| -------------- | ------- |
| Python         | 3.12    |
| FastAPI        | Latest  |
| k6             | 2.2.0   |
| InfluxDB       | 2.7     |
| Grafana        | 12.0.2  |
| React          | Vite    |
| Docker Compose | v2      |

---

# 📌 Current Project Version

**Stress Platform v0.3 Alpha**

A complete local platform for uploading, executing, monitoring and storing k6 stress test executions with Grafana dashboards and downloadable HTML reports.
