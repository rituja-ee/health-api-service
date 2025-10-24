# Health Service
A simple health service built using Fast-API which give basic system metrics and health status.

# API Endpoints
## GET /health
Returns health status of the system.
### Response
```json
{
  "status": "healthy",
  "cpu_percent": 8.2,
  "memory_percent": 66.6,
  "disk_percent": 2.8,
  "timestamp": "2025-10-07T19:26:38.154041"
}
```
## GET /metrics
Returns application metrics of the system.
### Response
```json
{
  "cpu": {
    "percent": 10.9,
    "cores": 12,
    "load_avg": [1.96435546875, 1.78662109375, 1.69140625],
    "load_avg_percent": [16.36962890625, 14.8885091145833, 14.0950520833333]
  },
  "memory": {
    "total": 25769803776,
    "available": 9048162304,
    "percent": 64.9
  },
  "disk": {
    "total": 494384795648,
    "used": 12039315456,
    "free": 417580486656,
    "percent": 2.8
  }
}
```

# Getting Started
## Pre-requisite
- Python - 3.11.9
- Poetry - 2.2.1

## Dependencies
- Fast API
- uvicorn
- psutil
- pytest
- httpx
- black
- flake8

## Installation
1. Clone the repository
```bash 
git clone https://github.com/rituja-ee/health-api-service.git
cd health-api-service
```

2. Install dependencies
```bash
poetry install --no-root
```

# How to run
1. Run the application
```bash 
poetry run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
2. Run the tests 
```bash 
poetry run pytest -v
```
3. Run the formatting
#### To check formatting (without changing files):
```bash
poetry run black --check .
```

#### To auto-format:
```bash
poetry run black .
```

4. Run the linting
```bash
poetry run flake8
```

# Project Structure
```
health-api-service/
├── app/
│   ├── __init__.py
│   ├── main.py             # Main FastAPI 
├── tests/                  # Unit tests directory
│   ├── __init__.py
│   └── test_health_api.py  # Health endpoint tests
├── .gitignore
├── .python-version         # Python version for this repository
├── poetry.lock             # Poetry dependency management
├── pyproject.toml          # Project configuration requirements
└── README.md               # This file
```

# Deployment Workflow
| Stage        | Description                                                                   |
| ------------ | ----------------------------------------------------------------------------- |
| **Checkout** | Retrieves source code from the repository.                                    |
| **Build**    | Sets up Python, installs Poetry, and project dependencies.     |
| **Lint**     | Runs code format and lint checks using **Black** and **Flake8**.              |
| **Test**     | Executes unit tests with **pytest**, generates coverage reports (XML). |
| **Deploy**   | Deploys the FastAPI app to the target environment (customizable).             |
| **Verify**   | Performs a `curl` check against `/health` to ensure deployment success.       |
