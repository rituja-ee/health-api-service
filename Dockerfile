# ---------- Stage 1: Builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies for Poetry and build tools
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=2.2.1
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION
ENV PATH="/root/.local/bin:$PATH"

# Copy only necessary files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-interaction --no-root

# ---------- Stage 2: Runtime ----------
FROM python:3.11-slim

WORKDIR /app

# Create a non-root user
RUN useradd -m appuser

# Copy dependencies from builder
COPY --from=builder /root/.cache/pypoetry /root/.cache/pypoetry
COPY --from=builder /app /app

# Copy the application code
COPY app ./app

# Install runtime dependencies
RUN pip install --no-cache-dir fastapi uvicorn psutil

# Expose the port
EXPOSE 8000

# Set non-root user
USER appuser

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Start FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
