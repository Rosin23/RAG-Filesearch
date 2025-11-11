# Dockerfile for SovDef FileSearch Lite API
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY sovdef_filesearch_lite/ ./sovdef_filesearch_lite/
COPY setup.py pyproject.toml README.md LICENSE ./

# Install package
RUN pip install -e ".[api]"

# Create temp directory for uploads
RUN mkdir -p /tmp/uploads

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run API server
CMD ["uvicorn", "sovdef_filesearch_lite.api:app", "--host", "0.0.0.0", "--port", "8000"]
