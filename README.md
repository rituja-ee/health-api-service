# Health Service
Give basic system metrics and health status

# Pre-requisite
- Python - 3.11.9
- Poetry - 2.2.1

# Dependencies
- Fast API
- uvicorn
- psutil
- pytest

# How to run
1. Run the application using - `poetry run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
2. Run the tests using - `poetry run pytest -v`
