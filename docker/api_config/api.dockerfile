# syntax = docker/dockerfile:1.4

# Build stage
FROM python:3.11-alpine AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create and set working directory
WORKDIR /app

# Install system dependencies (Alpine-specific)
RUN apk update && apk upgrade \
    && apk add --no-cache \
        gcc \
        python3-dev \
        musl-dev \
        libffi-dev \
        openssl-dev \
        build-base \
        libc6-compat \
    && rm -rf /var/cache/apk/*

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Install poetry and dependencies
RUN pip install --no-cache-dir poetry==1.7.1 \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Production stage
FROM python:3.11-alpine

LABEL maintainer="suporte@efscode.com.br"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    PATH="/app/.local/bin:${PATH}"

# Create non-root user
RUN addgroup -S app && \
    adduser -S -G app -h /app app && \
    mkdir -p /app/src && \
    chown -R app:app /app

# Set working directory
WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder --chown=app:app /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=app:app src/ src/

# Switch to non-root user
USER app

# Expose port (adjust if needed)
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "/app/src"]
