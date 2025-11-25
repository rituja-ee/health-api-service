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
- minikube

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
1. Run the application without containers
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

# Docker Setup
## Build Image
```bash
docker build -t health-api-service:latest .
```

## Run the container
```bash
docker run -d -p 8000:8000 health-api-service:latest
```

## Verify
```bash
curl http://localhost:8000/health
```

# Kubernetes Setup
## Start k8s
```bash
minikube start
```

## Apply manifest/configs files
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Change the namespace
```bash
kubectl config set-context --current --namespace=health-api
```

## Create tunnel
```bash
minikube tunnel
```

## Verify service is running
```bash
Hit the url in browser http://127.0.0.1:8000
```

# Helm Setup
## Create docker-secrets in the cluster
```bash
kubectl create secret docker-registry dockerhub-secret \
  --namespace health-api \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username="DOCKERHUB_USERNAME" \
  --docker-password="DOCKERHUB_TOKEN" \
  --docker-email="dummy@example.com"
```

## Apply helm changes
```bash
helm upgrade --install health-api ./health-api \\n  --namespace h
```

## Verify pods are running
```bash
kubectl get pods -n health-api
```

## Port forward to access service
```bash
kubectl port-forward svc/health-api 8000:8000 -n health-api &
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
├── .github/workflows                  
│   ├── ci.yaml
├── k8s/                  
│   ├── deployment.yaml
│   └── namespace.yaml
│   └── service.yaml  
│   └── configmap.yaml  
│   └── dockerhub-sercret.yaml  
├── .gitignore
├── .python-version         # Python version for this repository
├── poetry.lock             # Poetry dependency management
├── pyproject.toml          # Project configuration requirements
├── Dockerfile              # Dockerfile for containerize the application
└── README.md               # This file
```

# Deployment Workflow
| Stage        | Description                                                                   |
| ------------ | ----------------------------------------------------------------------------- |
| **Checkout** | Retrieves source code from the repository.                                    |
| **Lint**     | Runs code format and lint checks using **Black** and **Flake8**.              |
| **Test**     | Executes unit tests with **pytest**, generates coverage reports (XML). |
| **Build**    | Build the application, create a docker image and push the image to docker hub.     |
| **Deploy**   | Pull docker image from docker hub and run the container.             |
| **Verify**   | Performs a `curl` check against `/health` to ensure deployment success.       |
