# Dockerfile for Documentation Quality Analyzer
# Multi-stage build for smaller final image

FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user for security
RUN useradd -m -u 1000 analyzer && \
    mkdir -p /app && \
    chown -R analyzer:analyzer /app

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY --chown=analyzer:analyzer requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=analyzer:analyzer doc_analyzer.py .
COPY --chown=analyzer:analyzer test_analyzer.py .
COPY --chown=analyzer:analyzer config.yaml .

# Switch to non-root user
USER analyzer

# Create directories for outputs
RUN mkdir -p /app/reports /app/docs_input

# Default command shows help
CMD ["python", "doc_analyzer.py", "--help"]
