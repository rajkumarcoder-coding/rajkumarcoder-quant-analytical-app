FROM python:3.11-slim

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/backend


# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies (no venv inside container)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Docker-safe defaults (can be overridden via .env)
ENV HOST=0.0.0.0
ENV PORT=8000
ENV RELOAD=false

# Start backend via your entrypoint
CMD ["python", "starts.py"]
