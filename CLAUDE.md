# CLAUDE.md - AI Assistant Guide for FLAMEHAVEN FileSearch

This document provides comprehensive guidance for AI assistants (like Claude) working on the FLAMEHAVEN FileSearch codebase. It covers the project structure, development workflows, conventions, and best practices.

**Last Updated**: 2025-11-16
**Project Version**: v1.1.0
**Status**: Production-Ready

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Development Environment Setup](#development-environment-setup)
4. [Code Architecture](#code-architecture)
5. [Development Workflow](#development-workflow)
6. [Code Conventions](#code-conventions)
7. [Testing Guidelines](#testing-guidelines)
8. [Security Practices](#security-practices)
9. [Common Tasks](#common-tasks)
10. [Troubleshooting](#troubleshooting)

---

## Project Overview

**FLAMEHAVEN FileSearch** is an open-source semantic document search system powered by Google Gemini API. It enables RAG (Retrieval-Augmented Generation) based search across PDF, DOCX, TXT, and MD files with natural language queries.

### Key Features
- **Semantic Search**: Natural language queries with AI-powered answers
- **Multi-Format Support**: PDF, DOCX, TXT, MD files up to 50MB
- **Source Citations**: Every answer links back to source documents
- **Store Management**: Organize documents into separate collections
- **Dual Interface**: Python SDK + REST API with Swagger UI
- **Production Features** (v1.1.0):
  - LRU caching with TTL (99% faster on cache hits)
  - Rate limiting (protection against abuse)
  - Prometheus metrics (monitoring & observability)
  - OWASP security headers
  - Structured JSON logging
  - Request tracing with X-Request-ID

### Tech Stack
- **Language**: Python 3.8+
- **API Framework**: FastAPI 0.121.1+
- **AI Provider**: Google Gemini API (gemini-2.5-flash)
- **Document Processing**: PyPDF2, python-docx
- **Caching**: cachetools (LRU with TTL)
- **Monitoring**: Prometheus, psutil
- **Testing**: pytest, pytest-cov, pytest-asyncio
- **Code Quality**: black, isort, flake8, mypy

---

## Repository Structure

```
RAG-Filesearch/
├── flamehaven_filesearch/       # Main package
│   ├── __init__.py             # Package exports
│   ├── core.py                 # Core FlamehavenFileSearch class
│   ├── api.py                  # FastAPI REST API (v1.1.0)
│   ├── config.py               # Configuration management
│   ├── cache.py                # LRU caching with TTL
│   ├── metrics.py              # Prometheus metrics collector
│   ├── middlewares.py          # Request ID, security headers, logging
│   ├── validators.py           # Input validation (XSS, SQL injection, path traversal)
│   ├── exceptions.py           # Custom exceptions
│   └── logging_config.py       # JSON logging configuration
│
├── tests/                      # Test suite
│   ├── test_core.py           # Core functionality tests
│   ├── test_api.py            # API endpoint tests
│   ├── test_api_integration.py # Integration tests
│   ├── test_security.py       # Security tests
│   ├── test_performance.py    # Performance benchmarks
│   └── test_edge_cases.py     # Edge case tests
│
├── examples/                   # Usage examples
│   ├── basic_usage.py         # Basic SDK usage
│   └── api_example.py         # API client example
│
├── .github/workflows/          # CI/CD pipelines
│   ├── ci.yml                 # Main CI pipeline
│   ├── security.yml           # Security scanning
│   ├── publish.yml            # PyPI publishing
│   └── secrets.yml            # Secrets scanning
│
├── pyproject.toml             # Project metadata & dependencies
├── Makefile                   # Development tasks
├── Dockerfile                 # Container image
├── docker-compose.yml         # Docker Compose setup
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── .pre-commit-config.yaml    # Pre-commit hooks
│
├── README.md                  # User documentation
├── CONTRIBUTING.md            # Contribution guidelines
├── SECURITY.md                # Security policy & CVE fixes
├── CHANGELOG.md               # Version history
├── UPGRADING.md               # Migration guides
└── RELEASE_NOTES.md           # Release announcements
```

### File Descriptions

#### Core Package Files
- **`core.py`**: Main `FlamehavenFileSearch` class with methods for store management, file uploads, and semantic search
- **`api.py`**: FastAPI application with endpoints for upload, search, store management, and metrics
- **`config.py`**: Configuration dataclass with validation and environment variable loading
- **`cache.py`**: LRU cache implementation with TTL for search results
- **`metrics.py`**: Prometheus metrics collection for monitoring
- **`middlewares.py`**: Request ID tracking, security headers, and request logging
- **`validators.py`**: Input validation to prevent XSS, SQL injection, and path traversal attacks
- **`exceptions.py`**: Custom exception hierarchy with standardized error responses
- **`logging_config.py`**: JSON and development logging configurations

#### Key Configuration Files
- **`pyproject.toml`**: Project metadata, dependencies, tool configurations (black, isort, mypy, pytest)
- **`Makefile`**: Common development tasks (install, test, lint, format, build, docker)
- **`.env.example`**: Template for required environment variables (GEMINI_API_KEY, etc.)
- **`.pre-commit-config.yaml`**: Pre-commit hooks for code quality

---

## Development Environment Setup

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (get free at https://makersuite.google.com/app/apikey)
- Git

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/flamehaven01/Flamehaven-Filesearch.git
cd Flamehaven-Filesearch

# Install with all dependencies
make install-all
# OR manually:
pip install -e ".[dev,api]"

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run tests to verify setup
make test
```

### Environment Variables

Required:
- `GEMINI_API_KEY` or `GOOGLE_API_KEY`: Your Google Gemini API key

Optional (with defaults):
- `ENVIRONMENT`: `production` (JSON logs) or `development` (readable logs)
- `DATA_DIR`: `./data` - Document storage location
- `MAX_FILE_SIZE_MB`: `50` - Maximum file size
- `MAX_SOURCES`: `5` - Number of source citations
- `DEFAULT_MODEL`: `gemini-2.5-flash` - Gemini model to use
- `HOST`: `0.0.0.0` - API server host
- `PORT`: `8000` - API server port
- `WORKERS`: `1` - Number of worker processes

---

## Code Architecture

### Component Overview

```
┌──────────────────────────────────────────────────────┐
│                   Client Layer                       │
│         (Python SDK / REST API / CLI)                │
└───────────────────┬──────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────────┐
│               FastAPI Application                     │
│  ┌────────────────────────────────────────────────┐  │
│  │ Middlewares (Request ID, Security, Logging)    │  │
│  └────────────────────┬───────────────────────────┘  │
│                       ▼                               │
│  ┌────────────────────────────────────────────────┐  │
│  │ Validators (Filename, Size, Query)             │  │
│  └────────────────────┬───────────────────────────┘  │
│                       ▼                               │
│  ┌────────────────────────────────────────────────┐  │
│  │ Rate Limiter (10/min uploads, 100/min search)  │  │
│  └────────────────────┬───────────────────────────┘  │
│                       ▼                               │
│  ┌────────────────────────────────────────────────┐  │
│  │ Cache Layer (LRU with 1hr TTL)                 │  │
│  └────────────────────┬───────────────────────────┘  │
└────────────────────────┼──────────────────────────────┘
                         ▼
┌──────────────────────────────────────────────────────┐
│          FlamehavenFileSearch Core                    │
│  ┌────────────────────────────────────────────────┐  │
│  │ Store Management (create, list, delete)        │  │
│  └────────────────────┬───────────────────────────┘  │
│                       ▼                               │
│  ┌────────────────────────────────────────────────┐  │
│  │ File Upload & Processing (PDF, DOCX, TXT, MD) │  │
│  └────────────────────┬───────────────────────────┘  │
│                       ▼                               │
│  ┌────────────────────────────────────────────────┐  │
│  │ Google Gemini API Integration                  │  │
│  │ (Embeddings + RAG Generation)                  │  │
│  └────────────────────┬───────────────────────────┘  │
└────────────────────────┼──────────────────────────────┘
                         ▼
┌──────────────────────────────────────────────────────┐
│           Storage & Monitoring                        │
│  ┌────────────┐  ┌────────────┐  ┌────────────────┐  │
│  │ File Store │  │ Gemini API │  │ Prometheus     │  │
│  │ (local FS) │  │ (remote)   │  │ Metrics        │  │
│  └────────────┘  └────────────┘  └────────────────┘  │
└──────────────────────────────────────────────────────┘
```

### Key Classes and Modules

#### `FlamehavenFileSearch` (core.py)
Main class for document search operations.

**Key Methods**:
- `create_store(name: str)`: Create a new document store
- `list_stores()`: List all available stores
- `delete_store(name: str)`: Delete a store
- `upload_file(file_path: str, store: str)`: Upload and index a document
- `search(query: str, store: str, max_sources: int)`: Perform semantic search

**Dependencies**:
- Google Gemini API client (google-genai SDK)
- Config for configuration management
- Local file system for document storage

#### `Config` (config.py)
Configuration dataclass with validation.

**Key Attributes**:
- `api_key`: Gemini API key
- `max_file_size_mb`: File size limit (default: 50MB)
- `default_model`: Gemini model (default: gemini-2.5-flash)
- `temperature`: Model temperature (default: 0.5)
- `max_sources`: Number of sources to return (default: 5)

**Key Methods**:
- `validate(require_api_key: bool)`: Validate configuration
- `to_dict()`: Convert to dictionary (masks API key)
- `from_env()`: Create from environment variables

#### FastAPI Application (api.py)
REST API server with production-ready features.

**Endpoints**:
- `POST /upload`: Upload file(s) to a store
- `GET /search`: Search documents with natural language
- `GET /stores`: List all stores
- `POST /stores`: Create a new store
- `DELETE /stores/{name}`: Delete a store
- `GET /metrics`: Service metrics with cache stats
- `GET /prometheus`: Prometheus metrics endpoint

**Middlewares** (applied in order):
1. `RequestLoggingMiddleware`: Logs all requests with duration
2. `SecurityHeadersMiddleware`: Adds OWASP security headers
3. `RequestIDMiddleware`: Generates X-Request-ID for tracing

**Rate Limits** (per IP):
- Upload: 10/min (single), 5/min (multiple)
- Search: 100/min
- Store management: 20/min
- Monitoring: 100/min

---

## Development Workflow

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make code changes**
   - Follow code conventions (see below)
   - Add type hints for all functions
   - Update docstrings

3. **Write tests**
   ```bash
   # Add tests in tests/test_*.py
   # Run tests
   make test
   ```

4. **Format and lint**
   ```bash
   # Auto-format code
   make format

   # Check for issues
   make lint
   ```

5. **Commit changes**
   ```bash
   git add .
   git commit -m "Add: your feature description"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   # Open Pull Request on GitHub
   ```

### Common Makefile Commands

```bash
make help              # Show all available commands
make install           # Install package only
make install-dev       # Install with dev dependencies
make install-api       # Install with API dependencies
make install-all       # Install all dependencies

make test              # Run all tests
make test-cov          # Run tests with coverage report
make test-integration  # Run integration tests only

make lint              # Run all linters (flake8, black, isort)
make format            # Auto-format code (black, isort)

make clean             # Clean build artifacts
make build             # Build distribution packages
make docker-build      # Build Docker image
make docker-run        # Run Docker container

make server            # Start API server (development)
make server-prod       # Start API server (production)
```

### Running the API Server

```bash
# Development mode (auto-reload)
make server
# OR
uvicorn flamehaven_filesearch.api:app --reload --host 0.0.0.0 --port 8000

# Production mode (multiple workers)
make server-prod
# OR
uvicorn flamehaven_filesearch.api:app --host 0.0.0.0 --port 8000 --workers 4

# Access interactive docs at: http://localhost:8000/docs
```

---

## Code Conventions

### Python Style

- **Formatter**: `black` (88 char line length)
- **Import sorting**: `isort` (black profile)
- **Linting**: `flake8`
- **Type checking**: `mypy`

### Naming Conventions

- **Classes**: PascalCase (e.g., `FlamehavenFileSearch`, `Config`)
- **Functions/Methods**: snake_case (e.g., `create_store`, `upload_file`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_FILE_SIZE_MB`)
- **Private members**: Leading underscore (e.g., `_use_native_client`)

### Type Hints

Always use type hints for function signatures:

```python
from typing import Dict, List, Optional

def search(
    self,
    query: str,
    store: str = "default",
    max_sources: int = 5
) -> Dict[str, Any]:
    """Search documents with natural language query."""
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def upload_file(self, file_path: str, store: str = "default") -> Dict[str, str]:
    """
    Upload a document to the specified store.

    Args:
        file_path: Path to the file to upload
        store: Name of the store (default: "default")

    Returns:
        Dictionary with upload status and file metadata

    Raises:
        FileNotFoundError: If the file doesn't exist
        FileSizeExceededError: If file exceeds size limit
    """
    ...
```

### Commit Messages

Use conventional commit format:

- `Add: new feature` - New functionality
- `Fix: bug fix` - Bug fixes
- `Update: improvement` - Improvements to existing features
- `Refactor: code refactoring` - Code restructuring
- `Docs: documentation` - Documentation changes
- `Test: test changes` - Test additions/modifications
- `CI: CI/CD changes` - Pipeline changes

Examples:
```
Add: LRU cache with TTL for search results
Fix: path traversal vulnerability in file upload
Update: increase rate limit for search endpoint
Refactor: extract validation logic to validators.py
Docs: add API examples to README
Test: add integration tests for caching
CI: add security scanning workflow
```

---

## Testing Guidelines

### Test Structure

```
tests/
├── test_core.py           # Unit tests for core functionality
├── test_api.py            # API endpoint tests
├── test_api_integration.py # Integration tests
├── test_security.py       # Security tests
├── test_performance.py    # Performance benchmarks
└── test_edge_cases.py     # Edge case tests
```

### Running Tests

```bash
# All tests
pytest

# Unit tests only (no integration)
pytest -m "not integration"

# With coverage report
pytest --cov=flamehaven_filesearch --cov-report=html

# Specific test file
pytest tests/test_core.py -v

# Specific test function
pytest tests/test_core.py::TestConfig::test_config_creation -v
```

### Writing Tests

Use pytest conventions:

```python
import pytest
from flamehaven_filesearch import Config, FlamehavenFileSearch

class TestConfig:
    """Test Configuration class"""

    def test_config_creation(self):
        """Test basic config creation"""
        config = Config(api_key="test-key")
        assert config.api_key == "test-key"
        assert config.max_file_size_mb == 50

    def test_config_validation_fails(self):
        """Test config validation fails without API key"""
        config = Config(api_key=None)
        with pytest.raises(ValueError, match="API key required"):
            config.validate(require_api_key=True)
```

### Test Markers

Use pytest markers to categorize tests:

```python
@pytest.mark.integration
def test_full_workflow():
    """Integration test for complete workflow"""
    ...

@pytest.mark.slow
def test_large_file_upload():
    """Test uploading large files"""
    ...
```

Run specific marker tests:
```bash
pytest -m integration      # Only integration tests
pytest -m "not slow"       # Skip slow tests
```

### Coverage Requirements

- **Minimum coverage**: 80% for new code
- **Critical paths**: 100% coverage for security-critical code (validators, sanitization)
- Coverage report: Generated in `htmlcov/index.html`

---

## Security Practices

### Input Validation

**Always validate user inputs** using the validators in `validators.py`:

```python
from flamehaven_filesearch.validators import (
    FilenameValidator,
    SearchQueryValidator,
    FileSizeValidator
)

# Validate filename (prevents path traversal)
FilenameValidator.validate(filename)

# Validate search query (prevents XSS/SQL injection)
SearchQueryValidator.validate(query)

# Validate file size
FileSizeValidator.validate(file_size_bytes, max_size_mb=50)
```

### Path Traversal Protection

**Always sanitize filenames** using `os.path.basename()`:

```python
import os

# NEVER use user input directly in file paths
safe_filename = os.path.basename(file.filename)

# Block hidden files
if not safe_filename or safe_filename.startswith('.'):
    raise HTTPException(status_code=400, detail="Invalid filename")
```

### Rate Limiting

Rate limits are enforced per IP address:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/upload")
@limiter.limit("10/minute")
async def upload_file(...):
    ...
```

### Security Headers

All responses include OWASP-recommended security headers (configured in `middlewares.py`):

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000`
- `Content-Security-Policy: default-src 'self'`
- `Referrer-Policy: strict-origin-when-cross-origin`

### API Key Security

**Never commit API keys to git**:

- Store in `.env` file (gitignored)
- Load via environment variables
- Mask in logs: `config.to_dict()` returns `api_key: "***"`

### Known Vulnerabilities

**Fixed in v1.1.0**:
- ✅ CVE-2025-XXXX: Path traversal in file upload (CRITICAL)
- ✅ CVE-2024-47874: Starlette DoS vulnerability (CRITICAL)
- ✅ CVE-2025-54121: Starlette multipart parsing DoS (CRITICAL)

See `SECURITY.md` for full details.

---

## Common Tasks

### Adding a New API Endpoint

1. **Define endpoint in api.py**:
```python
@app.get("/new-endpoint")
@limiter.limit("100/minute")
async def new_endpoint(
    param: str = Query(..., description="Parameter description"),
    request: Request = None,
    request_id: str = Depends(get_request_id)
):
    """Endpoint description"""
    try:
        # Implementation
        result = do_something(param)
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in new_endpoint", exc_info=True, extra={
            "request_id": request_id,
            "param": param
        })
        raise HTTPException(status_code=500, detail=str(e))
```

2. **Add tests in tests/test_api.py**:
```python
def test_new_endpoint(client):
    """Test new endpoint"""
    response = client.get("/new-endpoint?param=value")
    assert response.status_code == 200
    assert "result" in response.json()
```

3. **Update documentation**: Add endpoint to README.md API reference

### Adding a New Configuration Option

1. **Add to Config class (config.py)**:
```python
@dataclass
class Config:
    new_option: int = 100  # Default value

    def validate(self, require_api_key: bool = False) -> bool:
        # Add validation if needed
        if self.new_option <= 0:
            raise ValueError("new_option must be positive")
        return True
```

2. **Add environment variable support**:
```python
@classmethod
def from_env(cls) -> "Config":
    return cls(
        new_option=int(os.getenv("NEW_OPTION", "100"))
    )
```

3. **Update .env.example**:
```bash
# New feature configuration
NEW_OPTION=100
```

4. **Add tests**:
```python
def test_config_new_option(self):
    config = Config(new_option=200)
    assert config.new_option == 200
```

### Adding Prometheus Metrics

1. **Define metric in metrics.py**:
```python
from prometheus_client import Counter, Histogram

new_metric = Counter(
    'flamehaven_new_metric_total',
    'Description of metric',
    ['label1', 'label2']
)

class MetricsCollector:
    @staticmethod
    def record_new_metric(label1: str, label2: str):
        new_metric.labels(label1=label1, label2=label2).inc()
```

2. **Use metric in code**:
```python
MetricsCollector.record_new_metric(label1="value1", label2="value2")
```

3. **Verify metric in /prometheus endpoint**

### Adding a New Validator

1. **Create validator class in validators.py**:
```python
class NewValidator:
    """Validator for new input type"""

    INVALID_PATTERNS = [...]

    @classmethod
    def validate(cls, value: str) -> None:
        """Validate input value"""
        if not value:
            raise ValueError("Value cannot be empty")

        for pattern in cls.INVALID_PATTERNS:
            if pattern in value:
                raise ValueError(f"Invalid pattern: {pattern}")
```

2. **Add tests in tests/test_security.py**:
```python
def test_new_validator_valid():
    NewValidator.validate("valid-value")  # Should not raise

def test_new_validator_invalid():
    with pytest.raises(ValueError):
        NewValidator.validate("invalid-value")
```

3. **Use validator in API endpoints**:
```python
from flamehaven_filesearch.validators import NewValidator

@app.post("/endpoint")
async def endpoint(value: str):
    NewValidator.validate(value)
    ...
```

---

## Troubleshooting

### Common Issues

#### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'flamehaven_filesearch'`

**Solution**:
```bash
# Reinstall package in editable mode
pip install -e ".[dev,api]"
```

#### API Key Issues

**Problem**: `ValueError: API key required for remote mode`

**Solution**:
```bash
# Check environment variable
echo $GEMINI_API_KEY

# Set in current session
export GEMINI_API_KEY="your-key-here"

# Or add to .env file
echo "GEMINI_API_KEY=your-key-here" >> .env
```

#### Test Failures

**Problem**: Tests fail with API errors

**Solution**:
```bash
# Run unit tests only (skip integration tests that require API)
pytest -m "not integration"

# Set test API key
export GEMINI_API_KEY="test-key"
```

#### Rate Limit Errors

**Problem**: HTTP 429 Too Many Requests

**Solution**:
- Wait for rate limit window to reset (check `Retry-After` header)
- Reduce request frequency
- For testing: Adjust rate limits in `api.py`

#### File Upload Errors

**Problem**: File upload fails with path traversal error

**Solution**:
- Ensure filename doesn't contain `..`, `/`, or `\`
- Don't use hidden files (starting with `.`)
- Use `os.path.basename()` to sanitize filenames

### Debug Mode

Enable debug logging:

```bash
# Set environment variable
export FLAMEHAVEN_DEBUG=1

# Or in .env
ENVIRONMENT=development

# Start server
make server
```

View detailed logs:
```bash
# Tail logs
tail -f logs/flamehaven.log

# Or check console output in development mode
```

### Performance Issues

**Cache not working?**
- Check cache stats at `/metrics` endpoint
- Verify cache TTL and size in `cache.py`
- Clear cache: Restart the server

**Slow searches?**
- Check Gemini API latency
- Verify network connectivity
- Monitor Prometheus metrics at `/prometheus`

**High memory usage?**
- Check number of cached items at `/metrics`
- Reduce cache size: Set `cache_max_size` in config
- Check for memory leaks: Run with profiler

---

## Additional Resources

### Documentation
- **README.md**: User-facing documentation
- **CONTRIBUTING.md**: Contribution guidelines
- **SECURITY.md**: Security policy and vulnerability fixes
- **CHANGELOG.md**: Version history and changes
- **UPGRADING.md**: Migration guides between versions

### External Links
- **Google Gemini API**: https://ai.google.dev/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Prometheus**: https://prometheus.io/docs/

### Getting Help
- **Issues**: https://github.com/flamehaven01/Flamehaven-Filesearch/issues
- **Discussions**: https://github.com/flamehaven01/Flamehaven-Filesearch/discussions
- **Email**: info@flamehaven.space

---

## AI Assistant Best Practices

### When Working on This Codebase

1. **Always read relevant files first**
   - Check existing implementation before suggesting changes
   - Review tests to understand expected behavior
   - Read docstrings and type hints

2. **Follow existing patterns**
   - Match the coding style of surrounding code
   - Use the same validation patterns
   - Follow the existing error handling approach

3. **Security first**
   - Always validate user inputs
   - Never trust file paths from users
   - Use validators from `validators.py`
   - Add security tests for new features

4. **Write comprehensive tests**
   - Add unit tests for new functions
   - Add integration tests for workflows
   - Test error cases and edge cases
   - Aim for 80%+ coverage

5. **Document changes**
   - Update docstrings for modified functions
   - Add comments for complex logic
   - Update README if user-facing changes
   - Add CHANGELOG entry for releases

6. **Use type hints**
   - Add type hints to all new functions
   - Use `Optional`, `List`, `Dict` from typing
   - Run mypy to check types

7. **Format and lint**
   - Run `make format` before committing
   - Run `make lint` to check for issues
   - Fix all linting errors

8. **Consider backwards compatibility**
   - Don't break existing API contracts
   - Add deprecation warnings before removing features
   - Document breaking changes in UPGRADING.md

### Code Review Checklist

Before suggesting code changes, verify:

- ✅ Code follows existing style and conventions
- ✅ All functions have type hints and docstrings
- ✅ Input validation is present for user data
- ✅ Tests are written and passing
- ✅ Security implications are considered
- ✅ Error handling is appropriate
- ✅ Logging is added for important events
- ✅ Documentation is updated if needed
- ✅ No secrets or API keys in code
- ✅ Performance impact is acceptable

---

## Version History

- **v1.1.0** (2025-11-13): Production-ready with caching, rate limiting, monitoring
- **v1.0.0**: Initial release with core file search capabilities

**Current Status**: Production-ready, actively maintained

---

**Document Maintained By**: FLAMEHAVEN Team
**For AI Assistants**: This document is designed to help you understand and work effectively with the FLAMEHAVEN FileSearch codebase. Always prioritize security, testing, and code quality when making changes.
