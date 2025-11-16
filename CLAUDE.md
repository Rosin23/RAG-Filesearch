# CLAUDE.md - AI Assistant Guide for FLAMEHAVEN FileSearch

**Last Updated:** 2025-11-16
**Version:** 1.1.0
**Purpose:** Comprehensive guide for AI assistants working on this codebase

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture & Structure](#architecture--structure)
3. [Core Components](#core-components)
4. [Development Workflow](#development-workflow)
5. [Testing Strategy](#testing-strategy)
6. [Code Style & Conventions](#code-style--conventions)
7. [CI/CD Pipeline](#cicd-pipeline)
8. [API & Integration Points](#api--integration-points)
9. [Configuration Management](#configuration-management)
10. [Security Considerations](#security-considerations)
11. [Common Tasks & Commands](#common-tasks--commands)
12. [Git Workflow & Branching](#git-workflow--branching)
13. [Troubleshooting Guide](#troubleshooting-guide)

---

## Project Overview

### What is FLAMEHAVEN FileSearch?

FLAMEHAVEN FileSearch is an open-source semantic document search system powered by Google Gemini AI. It enables users to upload documents (PDF, DOCX, TXT, MD) and perform natural language searches with AI-generated answers and source citations.

**Key Features:**
- Semantic document search with AI-powered answers
- Multi-format support (PDF, DOCX, TXT, MD)
- RESTful API with FastAPI
- Python SDK for programmatic access
- LRU caching with TTL for performance
- Prometheus metrics for monitoring
- Rate limiting and security headers
- Docker support for easy deployment

**Use Cases:**
- Document Q&A systems
- Knowledge base search
- Research paper analysis
- Corporate document search
- Educational content retrieval

---

## Architecture & Structure

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                             │
│  ┌─────────────────┐         ┌─────────────────┐           │
│  │  Python SDK     │         │   REST API      │           │
│  │  (core.py)      │         │   (api.py)      │           │
│  └────────┬────────┘         └────────┬────────┘           │
└───────────┼──────────────────────────┼──────────────────────┘
            │                          │
            └──────────┬───────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Business Logic Layer                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FlamehavenFileSearch Core (core.py)                 │  │
│  │  - File upload & validation                          │  │
│  │  - Store management                                  │  │
│  │  - Search orchestration                              │  │
│  └────────────────────┬─────────────────────────────────┘  │
└─────────────────────────┼────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Integration Layer                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Google Gemini API (google.genai SDK)                │  │
│  │  - File search stores                                │  │
│  │  - Document embedding                                │  │
│  │  - Answer generation                                 │  │
│  │  - Grounding & citations                             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

Supporting Services:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Caching    │  │   Metrics    │  │  Validation  │
│  (cache.py)  │  │ (metrics.py) │  │(validators.py)│
└──────────────┘  └──────────────┘  └──────────────┘
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Logging    │  │ Exceptions   │  │ Middlewares  │
│(logging_*.py)│  │(exceptions.py)│  │(middlewares.py)
└──────────────┘  └──────────────┘  └──────────────┘
```

### Directory Structure

```
RAG-Filesearch/
├── flamehaven_filesearch/     # Main package
│   ├── __init__.py           # Package initialization & exports
│   ├── core.py               # Core file search logic
│   ├── api.py                # FastAPI REST API server
│   ├── config.py             # Configuration management
│   ├── cache.py              # LRU caching with TTL
│   ├── metrics.py            # Prometheus metrics collector
│   ├── validators.py         # Input validation
│   ├── exceptions.py         # Custom exceptions
│   ├── logging_config.py     # Structured logging setup
│   └── middlewares.py        # FastAPI middlewares
│
├── tests/                    # Test suite
│   ├── test_core.py          # Core functionality tests
│   ├── test_api.py           # API endpoint tests
│   ├── test_api_integration.py # Integration tests
│   ├── test_security.py      # Security tests
│   ├── test_performance.py   # Performance & load tests
│   ├── test_validators_and_cache.py # Validation & caching
│   └── test_edge_cases.py    # Edge case coverage
│
├── examples/                 # Usage examples
│   ├── basic_usage.py        # Python SDK examples
│   ├── api_example.py        # REST API examples
│   └── README.md             # Example documentation
│
├── .github/workflows/        # CI/CD pipelines
│   ├── ci.yml                # Main CI/CD workflow
│   ├── security.yml          # Security scanning
│   ├── secrets.yml           # Secret detection
│   └── publish.yml           # PyPI publishing
│
├── docs/                     # Documentation (if exists)
│
├── pyproject.toml            # Project metadata & dependencies
├── pytest.ini                # Pytest configuration
├── .pre-commit-config.yaml   # Pre-commit hooks
├── Dockerfile                # Docker container definition
├── docker-compose.yml        # Docker Compose setup
├── Makefile                  # Development commands
├── requirements.txt          # Core dependencies
├── .env.example              # Environment variable template
│
├── README.md                 # User-facing documentation
├── CONTRIBUTING.md           # Contribution guidelines
├── SECURITY.md               # Security policy
├── CHANGELOG.md              # Version history
├── UPGRADING.md              # Upgrade instructions
└── CLAUDE.md                 # This file (AI assistant guide)
```

### Module Responsibilities

| Module | Purpose | Key Classes/Functions |
|--------|---------|----------------------|
| `core.py` | Core business logic | `FlamehavenFileSearch` |
| `api.py` | REST API server | FastAPI app, endpoints |
| `config.py` | Configuration | `Config` dataclass |
| `cache.py` | Caching layer | `SearchCache`, TTL logic |
| `metrics.py` | Monitoring | `MetricsCollector` |
| `validators.py` | Input validation | `validate_upload_file()`, `validate_search_request()` |
| `exceptions.py` | Error handling | Custom exception classes |
| `logging_config.py` | Logging setup | JSON & development loggers |
| `middlewares.py` | Request processing | Security, CORS, tracing |

---

## Core Components

### 1. FlamehavenFileSearch (`core.py`)

**Purpose:** Main SDK class for file search operations

**Key Methods:**
```python
# Store management
create_store(name: str) -> str
list_stores() -> Dict[str, str]
delete_store(store_name: str) -> Dict[str, Any]

# File operations
upload_file(file_path: str, store_name: str, max_size_mb: int) -> Dict[str, Any]
upload_files(file_paths: List[str], store_name: str) -> Dict[str, Any]

# Search
search(query: str, store_name: str, model: str, max_tokens: int, temperature: float) -> Dict[str, Any]

# Metrics
get_metrics() -> Dict[str, Any]
```

**Important Behaviors:**
- Supports **offline mode** when `google-genai` SDK is unavailable (fallback mode)
- Validates file size (default max: 50MB)
- Polls Google Gemini API for upload completion (timeout: 60s)
- Applies "driftlock" validation: min/max answer length, banned terms
- Returns structured responses with `status`, `answer`, `sources`

**Initialization:**
```python
# With environment variable
fs = FlamehavenFileSearch()  # Reads GEMINI_API_KEY from env

# With explicit config
config = Config(api_key="...", max_file_size_mb=100)
fs = FlamehavenFileSearch(config=config)

# Offline mode (for testing)
fs = FlamehavenFileSearch(allow_offline=True)
```

### 2. FastAPI Server (`api.py`)

**Purpose:** RESTful API for file search with production-ready features

**Key Features (v1.1.0):**
- **Rate Limiting:** 10/min uploads, 100/min searches (via `slowapi`)
- **Caching:** LRU cache with 1-hour TTL (1000 items)
- **Security:** OWASP headers, request ID tracing, input validation
- **Monitoring:** Prometheus metrics at `/prometheus`
- **Logging:** Structured JSON logging (production) or readable (development)

**Main Endpoints:**

| Endpoint | Method | Rate Limit | Purpose |
|----------|--------|------------|---------|
| `/api/upload/single` | POST | 10/min | Upload single file |
| `/api/upload/multiple` | POST | 5/min | Upload multiple files |
| `/api/search` | POST/GET | 100/min | Search documents |
| `/api/stores` | GET/POST/DELETE | 20-100/min | Manage stores |
| `/health` | GET | 100/min | Health check |
| `/metrics` | GET | 100/min | Service metrics |
| `/prometheus` | GET | 100/min | Prometheus metrics |

**Legacy Endpoints:** `/upload`, `/search`, `/stores` (proxied to `/api/*`)

**Error Handling:**
- Custom exceptions via `FileSearchException`
- Standardized error responses with request IDs
- HTTP status codes: 400 (validation), 404 (not found), 429 (rate limit), 500 (server error)

### 3. Configuration (`config.py`)

**Purpose:** Centralized configuration management

**Key Settings:**
```python
@dataclass
class Config:
    api_key: Optional[str] = None              # Google Gemini API key
    max_file_size_mb: int = 50                 # Max file size (Gemini limit)
    upload_timeout_sec: int = 60               # Upload timeout
    default_model: str = "gemini-2.5-flash"    # Gemini model
    max_output_tokens: int = 1024              # Max response tokens
    temperature: float = 0.5                   # Model temperature
    max_sources: int = 5                       # Max source citations

    # Driftlock (answer validation)
    min_answer_length: int = 10
    max_answer_length: int = 4096
    banned_terms: list = ["PII-leak"]
```

**Environment Variables:**
- `GEMINI_API_KEY` / `GOOGLE_API_KEY` - API key (required)
- `MAX_FILE_SIZE_MB` - Max file size (default: 50)
- `DEFAULT_MODEL` - Gemini model (default: gemini-2.5-flash)
- `ENVIRONMENT` - `production` (JSON logs) or `development` (readable logs)
- `HOST`, `PORT`, `WORKERS` - API server settings

### 4. Caching (`cache.py`)

**Purpose:** LRU caching with TTL for search results

**Implementation:**
```python
from cachetools import TTLCache

class SearchCache:
    def __init__(self, maxsize=1000, ttl=3600):
        self._cache = TTLCache(maxsize=maxsize, ttl=ttl)

    def get(query, store, **params) -> Optional[Dict]
    def set(query, store, result, **params) -> None
    def get_stats() -> Dict  # Returns hits, misses, hit_rate
```

**Cache Key:** Combination of `(query, store, model, max_tokens, temperature)`

**Performance Impact:**
- Cache hit: <10ms response time
- Cache miss: 2-3s (Gemini API call)
- Hit rate: 40-60% (typical usage)

### 5. Validation (`validators.py`)

**Purpose:** Input sanitization and security validation

**Key Functions:**
```python
def validate_upload_file(filename, file_size, content_type, max_size_mb)
    # Raises: InvalidFilenameError, FileSizeExceededError, UnsupportedFileTypeError
    # Checks: path traversal, empty filename, size limits, file types

def validate_search_request(query)
    # Raises: EmptySearchQueryError, InvalidSearchQueryError
    # Checks: SQL injection patterns, XSS attempts, command injection
```

**Security Checks:**
- **Path Traversal:** Blocks `../`, `..\\`, absolute paths
- **XSS:** Detects `<script>`, `javascript:`, `onerror=`
- **SQL Injection:** Detects `UNION SELECT`, `DROP TABLE`
- **Command Injection:** Detects `$(`, backticks, semicolons

### 6. Metrics (`metrics.py`)

**Purpose:** Prometheus metrics collection

**Metrics Exported:**
- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request duration histogram
- `file_uploads_total` - Total file uploads
- `search_requests_total` - Total search requests
- `cache_hits_total` / `cache_misses_total` - Cache performance
- `rate_limit_exceeded_total` - Rate limit violations
- `system_cpu_percent` / `system_memory_percent` - System metrics

**Usage:**
```python
MetricsCollector.record_file_upload(store, size_bytes, duration, success)
MetricsCollector.record_search(store, duration, results_count, success)
MetricsCollector.record_cache_hit(cache_type)
MetricsCollector.update_system_metrics()
```

---

## Development Workflow

### Initial Setup

```bash
# 1. Clone repository
git clone https://github.com/flamehaven01/Flamehaven-Filesearch.git
cd Flamehaven-Filesearch

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# 3. Install development dependencies
pip install -e ".[dev,api,google]"

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add GEMINI_API_KEY

# 5. Install pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install

# 6. Verify installation
pytest tests/ -v
```

### Making Changes

**Standard Workflow:**

1. **Create Feature Branch:**
   ```bash
   git checkout -b feature/your-feature-name
   # or: git checkout -b fix/bug-description
   ```

2. **Write Code:**
   - Follow code style guidelines (see below)
   - Add docstrings to all public functions/classes
   - Keep functions focused and single-purpose

3. **Write Tests:**
   ```bash
   # Unit tests
   pytest tests/test_core.py -v

   # Integration tests (requires API key)
   pytest tests/test_api_integration.py -v -m integration

   # All tests with coverage
   pytest --cov=flamehaven_filesearch --cov-report=html
   ```

4. **Run Linters:**
   ```bash
   # Format code
   black flamehaven_filesearch/ tests/ examples/
   isort flamehaven_filesearch/ tests/ examples/

   # Check linting
   flake8 flamehaven_filesearch/ tests/ examples/

   # Or use Makefile
   make format
   make lint
   ```

5. **Commit Changes:**
   ```bash
   git add .
   git commit -m "Add: feature description"
   # Pre-commit hooks will run automatically
   ```

6. **Push & Create PR:**
   ```bash
   git push origin feature/your-feature-name
   # Open PR on GitHub
   ```

### Key Development Commands

**Using Makefile:**
```bash
make help              # Show all commands
make install-dev       # Install development dependencies
make test              # Run all tests
make test-cov          # Run tests with coverage report
make lint              # Run linters (flake8, black, isort)
make format            # Auto-format code
make build             # Build distribution package
make server            # Start API server (development)
make docker-build      # Build Docker image
```

**Using pytest directly:**
```bash
# Run specific test file
pytest tests/test_core.py -v

# Run specific test function
pytest tests/test_core.py::test_upload_file -v

# Run tests with markers
pytest -m "not integration"  # Skip integration tests
pytest -m security          # Only security tests

# Run with verbose output
pytest -vv --tb=short

# Run with coverage
pytest --cov=flamehaven_filesearch --cov-report=term-missing
```

**Starting API Server:**
```bash
# Development (auto-reload)
uvicorn flamehaven_filesearch.api:app --reload --host 0.0.0.0 --port 8000

# Production (multiple workers)
export WORKERS=4
flamehaven-api

# Docker
docker-compose up
```

---

## Testing Strategy

### Test Structure

**Test Categories:**
- **Unit Tests:** `test_core.py`, `test_validators_and_cache.py`
- **API Tests:** `test_api.py`, `test_api_additional.py`
- **Integration Tests:** `test_api_integration.py` (requires API key)
- **Security Tests:** `test_security.py`
- **Performance Tests:** `test_performance.py`
- **Edge Cases:** `test_edge_cases.py`

### Test Markers

```python
@pytest.mark.integration  # Requires external services (Gemini API)
@pytest.mark.security     # Security-focused tests
@pytest.mark.slow         # Long-running tests
```

**Running specific markers:**
```bash
pytest -m integration        # Only integration tests
pytest -m "not integration"  # Skip integration tests
pytest -m security          # Only security tests
```

### Fixtures

**Common fixtures** (defined in `conftest.py` or test files):
```python
@pytest.fixture
def searcher():
    """FlamehavenFileSearch instance with test config"""
    config = Config(api_key="test-key", allow_offline=True)
    return FlamehavenFileSearch(config=config)

@pytest.fixture
def client():
    """FastAPI TestClient for API testing"""
    from fastapi.testclient import TestClient
    return TestClient(app)
```

### Coverage Requirements

**Target:** 90% code coverage minimum

```bash
# Check coverage
pytest --cov=flamehaven_filesearch --cov-report=html --cov-fail-under=90

# View HTML report
open htmlcov/index.html
```

**Coverage exclusions** (in `pyproject.toml`):
```toml
[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

### Testing Best Practices

**DO:**
- ✅ Test happy paths AND error cases
- ✅ Use descriptive test names: `test_upload_file_exceeds_size_limit()`
- ✅ Mock external dependencies (Google Gemini API)
- ✅ Test edge cases (empty strings, None values, boundary conditions)
- ✅ Verify error messages and status codes
- ✅ Use parametrize for multiple similar tests

**DON'T:**
- ❌ Test implementation details (test behavior, not internals)
- ❌ Write tests that depend on execution order
- ❌ Hardcode API keys in tests (use environment variables or mocks)
- ❌ Skip cleanup (use fixtures with `yield` for teardown)

**Example Test Pattern:**
```python
def test_feature_name():
    # Arrange: Set up test data
    config = Config(max_file_size_mb=50)
    searcher = FlamehavenFileSearch(config=config)

    # Act: Execute the functionality
    result = searcher.upload_file("test.pdf")

    # Assert: Verify expected behavior
    assert result["status"] == "success"
    assert result["size_mb"] <= 50
```

---

## Code Style & Conventions

### Python Style Guide

**Standards:**
- **PEP 8** compliance
- **Type hints** for function signatures (Python 3.8+ compatible)
- **Docstrings** for all public functions/classes (Google style)

### Code Formatting

**Tools:**
- **black** - Code formatter (line length: 88)
- **isort** - Import sorter (profile: black)
- **flake8** - Linter (ignores: E203, W503)

**Configuration** (in `pyproject.toml`):
```toml
[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311']

[tool.isort]
profile = "black"
line_length = 88
```

### Naming Conventions

**Files:**
- Module names: `lowercase_with_underscores.py`
- Test files: `test_*.py`

**Classes:**
- PascalCase: `FlamehavenFileSearch`, `MetricsCollector`

**Functions/Methods:**
- snake_case: `upload_file()`, `get_metrics()`

**Constants:**
- UPPER_CASE: `MAX_FILE_SIZE_MB`, `DEFAULT_MODEL`

**Private members:**
- Leading underscore: `_local_upload()`, `_use_native_client`

### Docstring Format

**Google-style docstrings:**
```python
def upload_file(file_path: str, store_name: str = "default") -> Dict[str, Any]:
    """
    Upload a file to the file search store.

    This method validates the file size and format, then uploads it to
    the specified Google Gemini file search store.

    Args:
        file_path: Path to the file to upload
        store_name: Name of the store to upload to (default: "default")

    Returns:
        Dict containing upload status and metadata:
            - status: "success" or "error"
            - file: File path
            - size_mb: File size in megabytes
            - message: Error message (if status is "error")

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If file size exceeds limit

    Example:
        >>> searcher = FlamehavenFileSearch()
        >>> result = searcher.upload_file("document.pdf")
        >>> print(result["status"])
        success
    """
```

### Import Order

**Standard order** (enforced by isort):
1. Standard library imports
2. Third-party imports
3. Local application imports

```python
# Standard library
import os
import time
from typing import Dict, List, Optional

# Third-party
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Local
from .config import Config
from .core import FlamehavenFileSearch
```

### Type Hints

**Always use type hints:**
```python
# Good
def search(query: str, store_name: str = "default") -> Dict[str, Any]:
    ...

# Bad
def search(query, store_name="default"):
    ...
```

**For complex types:**
```python
from typing import Dict, List, Optional, Any

StoreDict = Dict[str, str]
SearchResult = Dict[str, Any]

def list_stores() -> StoreDict:
    ...
```

### Error Handling

**Use custom exceptions** (defined in `exceptions.py`):
```python
# Good
raise InvalidFilenameError(filename, "Filename cannot contain '..'")

# Bad
raise ValueError("Invalid filename")
```

**Handle exceptions at the right level:**
```python
# In core.py: raise exceptions
def upload_file(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

# In api.py: catch and return HTTP responses
@app.post("/upload")
async def upload(file: UploadFile):
    try:
        result = searcher.upload_file(file.filename)
        return result
    except FileSearchException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
```

### Logging

**Use structured logging:**
```python
import logging

logger = logging.getLogger(__name__)

# Good - structured with context
logger.info("File uploaded successfully", extra={
    "file_path": file_path,
    "store": store_name,
    "size_mb": size_mb
})

# Good - simple message
logger.info(f"Uploading file: {file_path} ({size_mb:.2f} MB)")

# Bad - too verbose
print(f"DEBUG: File path is {file_path}")
```

**Log levels:**
- `DEBUG`: Detailed diagnostic info (disabled in production)
- `INFO`: General informational messages
- `WARNING`: Warnings about potential issues
- `ERROR`: Errors that should be investigated
- `CRITICAL`: Critical failures

---

## CI/CD Pipeline

### GitHub Actions Workflows

**Main Workflow** (`.github/workflows/ci.yml`):
```yaml
Triggers:
  - push: main, develop, claude/*
  - pull_request: main, develop
  - release: published

Jobs:
  1. lint: Code formatting & linting
     - black --check
     - isort --check-only
     - flake8

  2. test: Run tests on Python 3.8-3.12
     - pytest with coverage
     - Upload coverage to Codecov

  3. build: Build Python package
     - python -m build
     - twine check
     - Upload artifacts

  4. docker: Build Docker image
     - docker build
     - Test image
```

**Security Workflow** (`.github/workflows/security.yml`):
- Bandit security scanning
- Dependency vulnerability checks (Safety)
- Secret detection (gitleaks)

**Publish Workflow** (`.github/workflows/publish.yml`):
- Triggered on GitHub releases
- Publishes to PyPI

### Pre-commit Hooks

**Installed hooks** (`.pre-commit-config.yaml`):
1. **Formatting:** black, isort
2. **Linting:** flake8
3. **Security:** bandit, gitleaks, secret detection
4. **Validation:** YAML, JSON, TOML checks
5. **Custom:** Path traversal detection, coverage check

**Setup:**
```bash
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

**Skip hooks** (use sparingly):
```bash
SKIP=bandit,flake8 git commit -m "WIP: work in progress"
```

### Release Process

**Version Bumping:**
1. Update version in:
   - `flamehaven_filesearch/__init__.py`: `__version__ = "X.Y.Z"`
   - `pyproject.toml`: `version = "X.Y.Z"`
   - `api.py`: FastAPI app description & version

2. Update `CHANGELOG.md` with release notes

3. Create git tag:
   ```bash
   git tag -a v1.2.0 -m "Release v1.2.0"
   git push origin v1.2.0
   ```

4. Create GitHub release (triggers publish workflow)

**Versioning Scheme:**
- `MAJOR.MINOR.PATCH` (Semantic Versioning)
- `MAJOR`: Breaking changes
- `MINOR`: New features (backward compatible)
- `PATCH`: Bug fixes

---

## API & Integration Points

### REST API Endpoints

**Base URL:** `http://localhost:8000`

**API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

**Endpoint Summary:**

| Endpoint | Method | Purpose | Request Body | Response |
|----------|--------|---------|--------------|----------|
| `/api/upload/single` | POST | Upload file | Form: `file`, `store` | `UploadResponse` |
| `/api/upload/multiple` | POST | Upload files | Form: `files[]`, `store` | `MultipleUploadResponse` |
| `/api/search` | POST | Search docs | JSON: `SearchRequest` | `SearchResponse` |
| `/api/search?q=...` | GET | Search (simple) | Query params | `SearchResponse` |
| `/api/stores` | GET | List stores | - | Store list |
| `/api/stores` | POST | Create store | JSON: `{name}` | Store info |
| `/api/stores/{name}` | DELETE | Delete store | - | Status |
| `/health` | GET | Health check | - | `HealthResponse` |
| `/metrics` | GET | Service metrics | - | `MetricsResponse` |
| `/prometheus` | GET | Prometheus metrics | - | Text format |

**Request/Response Models:**

```python
# Search Request
{
    "query": "What is the vacation policy?",
    "store_name": "default",  # optional
    "model": "gemini-2.5-flash",  # optional
    "max_tokens": 1024,  # optional
    "temperature": 0.5  # optional
}

# Search Response
{
    "status": "success",
    "answer": "Employees receive 15 days of paid vacation...",
    "sources": [
        {
            "title": "handbook.pdf",
            "uri": "gs://bucket/file"
        }
    ],
    "model": "gemini-2.5-flash",
    "query": "What is the vacation policy?",
    "store": "default",
    "request_id": "abc-123-def"
}

# Error Response
{
    "error": "ERROR_CODE",
    "message": "Human-readable error message",
    "detail": "Detailed error information",
    "status_code": 400,
    "request_id": "abc-123-def",
    "timestamp": "2025-11-16T10:30:00Z"
}
```

### Python SDK Usage

**Basic Example:**
```python
from flamehaven_filesearch import FlamehavenFileSearch

# Initialize
fs = FlamehavenFileSearch()  # Uses GEMINI_API_KEY from env

# Upload files
fs.upload_file("document.pdf")
fs.upload_file("report.docx", store_name="reports")

# Search
result = fs.search("What are the key findings?")
print(result["answer"])
print(f"Sources: {result['sources']}")

# Manage stores
fs.create_store("hr-docs")
stores = fs.list_stores()
fs.delete_store("old-store")
```

**Advanced Configuration:**
```python
from flamehaven_filesearch import FlamehavenFileSearch, Config

config = Config(
    api_key="your-gemini-key",
    max_file_size_mb=100,
    default_model="gemini-2.5-flash",
    temperature=0.7,
    max_sources=10
)

fs = FlamehavenFileSearch(config=config)
```

### Google Gemini API Integration

**SDK Used:** `google-genai` (Google's official Gemini SDK)

**Key Operations:**
1. **Create File Search Store:**
   ```python
   store = client.file_search_stores.create()
   # Returns: FileSearchStore object with name
   ```

2. **Upload File to Store:**
   ```python
   upload_op = client.file_search_stores.upload_to_file_search_store(
       file_search_store_name=store_name,
       file=file_path
   )
   # Returns: Operation object (poll for completion)
   ```

3. **Generate Content with File Search:**
   ```python
   response = client.models.generate_content(
       model="gemini-2.5-flash",
       contents=query,
       config=GenerateContentConfig(
           tools=[Tool(file_search=FileSearch(
               file_search_store_names=[store_name]
           ))],
           max_output_tokens=1024,
           temperature=0.5
       )
   )
   # Returns: GenerateContentResponse with answer and grounding
   ```

**Rate Limits & Quotas:**
- Free tier: Generous limits (check Google AI Studio)
- File size limit: 50MB per file
- Supported formats: PDF, DOCX, TXT, MD

**Error Handling:**
```python
try:
    result = fs.search("query")
except Exception as e:
    if "quota" in str(e).lower():
        # Handle quota exceeded
    elif "invalid" in str(e).lower():
        # Handle invalid API key
    else:
        # General error
```

---

## Configuration Management

### Environment Variables

**Required:**
- `GEMINI_API_KEY` or `GOOGLE_API_KEY` - Google Gemini API key

**Optional (with defaults):**
```bash
# File handling
MAX_FILE_SIZE_MB=50                # Maximum file size
UPLOAD_TIMEOUT_SEC=60              # Upload operation timeout

# Model settings
DEFAULT_MODEL=gemini-2.5-flash     # Gemini model to use
MAX_OUTPUT_TOKENS=1024             # Max tokens in response
TEMPERATURE=0.5                    # Model temperature (0.0-1.0)
MAX_SOURCES=5                      # Max source citations

# API server
HOST=0.0.0.0                       # Server host
PORT=8000                          # Server port
WORKERS=1                          # Number of workers (production: 4)
ENVIRONMENT=production             # production (JSON logs) or development

# Caching
CACHE_MAX_SIZE=1000                # Max cache entries
CACHE_TTL_SEC=3600                 # Cache TTL (1 hour)
```

### .env File

**Create from template:**
```bash
cp .env.example .env
```

**Example `.env`:**
```bash
# API Key (required)
GEMINI_API_KEY=AIza...your-key-here

# Environment
ENVIRONMENT=production

# Custom settings
MAX_FILE_SIZE_MB=100
DEFAULT_MODEL=gemini-2.5-flash
WORKERS=4
```

**Important:** Never commit `.env` to git (already in `.gitignore`)

### Config Loading Priority

1. **Explicit config object:** `FlamehavenFileSearch(config=Config(...))`
2. **Environment variables:** `Config.from_env()`
3. **Defaults:** Values in `Config` dataclass

```python
# Priority example
config = Config(
    api_key="explicit-key",        # 1. Highest priority
    max_file_size_mb=100
)

# Falls back to env var if not set
config = Config.from_env()         # 2. Environment variables

# Falls back to defaults
config = Config()                  # 3. Default values
```

---

## Security Considerations

### Security Features (v1.1.0)

**Input Validation:**
- ✅ Path traversal protection (`../` blocking)
- ✅ XSS prevention (script tag detection)
- ✅ SQL injection detection
- ✅ Command injection blocking
- ✅ Filename sanitization

**API Security:**
- ✅ Rate limiting (slowapi)
- ✅ Request ID tracing (`X-Request-ID` header)
- ✅ OWASP security headers:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Content-Security-Policy`
  - `Strict-Transport-Security`
- ✅ CORS headers

**Secrets Management:**
- ✅ API keys via environment variables only
- ✅ Pre-commit hooks detect hardcoded secrets
- ✅ `.env` in `.gitignore`

**Dependency Security:**
- ✅ Safety checks in pre-commit hooks
- ✅ Bandit security scanning
- ✅ Regular dependency updates
- ✅ Zero critical CVEs (v1.1.0)

### Vulnerability Fixes (v1.1.0)

**Fixed Issues:**
1. **Path Traversal (CVE-2024-XXXXX):**
   - Previous: `file.filename` used directly
   - Fixed: `os.path.basename(file.filename)` in `validate_upload_file()`

2. **Starlette CVEs (CVE-2024-47874, CVE-2025-54121):**
   - Fixed: Updated to `fastapi>=0.121.1`

3. **Rate Limit Bypass:**
   - Fixed: Per-endpoint rate limiting with slowapi

### Security Best Practices

**For Developers:**
1. **Never hardcode secrets:**
   ```python
   # Bad
   api_key = "AIza..."

   # Good
   api_key = os.getenv("GEMINI_API_KEY")
   ```

2. **Always validate input:**
   ```python
   # Use validators
   validated_filename, _ = validate_upload_file(filename, size, content_type)
   validated_query, _ = validate_search_request(query)
   ```

3. **Use parameterized queries** (if adding database support)

4. **Run security tests:**
   ```bash
   pytest tests/test_security.py -v -m security
   bandit -r flamehaven_filesearch/
   ```

**For Deployment:**
1. **Use HTTPS** (reverse proxy with SSL)
2. **Set secure headers** (already implemented in middlewares)
3. **Monitor rate limits** (check Prometheus metrics)
4. **Regular updates** (dependencies, security patches)
5. **Encrypt data at rest** (if storing sensitive documents)

### Reporting Security Issues

**Do NOT open public issues for security vulnerabilities.**

Email: security@flamehaven.space (or see `SECURITY.md`)

---

## Common Tasks & Commands

### Development Tasks

**Setup New Environment:**
```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[dev,api,google]"
cp .env.example .env
# Edit .env with GEMINI_API_KEY
pre-commit install
pytest tests/
```

**Run Tests:**
```bash
# All tests
pytest -v

# Unit tests only (no API calls)
pytest -m "not integration" -v

# Integration tests (requires API key)
pytest -m integration -v

# Specific test file
pytest tests/test_core.py -v

# With coverage
pytest --cov=flamehaven_filesearch --cov-report=html

# Watch mode (requires pytest-watch)
ptw -- -v
```

**Format & Lint:**
```bash
# Auto-format
make format
# or
black flamehaven_filesearch/ tests/ examples/
isort flamehaven_filesearch/ tests/ examples/

# Check linting
make lint
# or
flake8 flamehaven_filesearch/ tests/
mypy flamehaven_filesearch/
```

**Start Development Server:**
```bash
# Method 1: Using CLI command
export GEMINI_API_KEY="your-key"
export ENVIRONMENT=development  # Readable logs
flamehaven-api

# Method 2: Using uvicorn directly
uvicorn flamehaven_filesearch.api:app --reload --host 0.0.0.0 --port 8000

# Method 3: Using Makefile
make server
```

**Build & Package:**
```bash
# Build distribution
make build
# or
python -m build

# Check package
twine check dist/*

# Publish to TestPyPI
make publish-test

# Publish to PyPI (after testing)
make publish
```

**Docker:**
```bash
# Build image
make docker-build
# or
docker build -t flamehaven-filesearch:latest .

# Run container
docker run -e GEMINI_API_KEY="your-key" \
  -p 8000:8000 \
  -v ./data:/app/data \
  flamehaven-filesearch:latest

# Docker Compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### Testing Specific Features

**Test File Upload:**
```bash
# Create test file
echo "Test document content" > test.txt

# Upload via CLI
curl -X POST "http://localhost:8000/api/upload/single" \
  -F "file=@test.txt" \
  -F "store=default"

# Upload via Python
python -c "
from flamehaven_filesearch import FlamehavenFileSearch
fs = FlamehavenFileSearch()
result = fs.upload_file('test.txt')
print(result)
"
```

**Test Search:**
```bash
# Search via CLI
curl "http://localhost:8000/api/search?q=test+query&store=default"

# Search via Python
python -c "
from flamehaven_filesearch import FlamehavenFileSearch
fs = FlamehavenFileSearch()
result = fs.search('test query')
print(result['answer'])
"
```

**Test Caching:**
```bash
# First search (cache miss)
time curl "http://localhost:8000/api/search?q=vacation+policy"

# Second search (cache hit - should be <10ms)
time curl "http://localhost:8000/api/search?q=vacation+policy"

# Check cache metrics
curl "http://localhost:8000/metrics" | jq '.cache'
```

**Test Rate Limiting:**
```bash
# Rapid requests (should hit rate limit)
for i in {1..15}; do
  curl -X POST "http://localhost:8000/api/upload/single" \
    -F "file=@test.txt" \
    -F "store=default"
done
# Should see 429 Rate Limit Exceeded after 10 requests
```

### Monitoring & Debugging

**Check Logs:**
```bash
# Development (readable logs)
export ENVIRONMENT=development
flamehaven-api

# Production (JSON logs)
export ENVIRONMENT=production
flamehaven-api | jq .
```

**View Metrics:**
```bash
# Service metrics (JSON)
curl http://localhost:8000/metrics | jq .

# Prometheus metrics (text)
curl http://localhost:8000/prometheus

# Specific metric
curl http://localhost:8000/prometheus | grep search_requests_total
```

**Health Check:**
```bash
curl http://localhost:8000/health | jq .
```

**Debug Mode:**
```bash
# Enable debug logging
export FLAMEHAVEN_DEBUG=1
export ENVIRONMENT=development
flamehaven-api
```

### Database/Store Management

**List Stores:**
```bash
curl http://localhost:8000/api/stores | jq .
```

**Create Store:**
```bash
curl -X POST http://localhost:8000/api/stores \
  -H "Content-Type: application/json" \
  -d '{"name": "hr-docs"}'
```

**Delete Store:**
```bash
curl -X DELETE http://localhost:8000/api/stores/hr-docs
```

---

## Git Workflow & Branching

### Branch Naming

**Convention:**
- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `refactor/component-name` - Code refactoring
- `docs/description` - Documentation updates
- `test/description` - Test additions/improvements
- `claude/*` - AI assistant branches (auto-approved in CI)

**Examples:**
```bash
git checkout -b feature/add-batch-upload
git checkout -b fix/cache-memory-leak
git checkout -b refactor/improve-validators
git checkout -b docs/update-api-reference
```

### Commit Message Format

**Conventional Commits:**
```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `Add:` - New feature
- `Fix:` - Bug fix
- `Update:` - Improvement to existing feature
- `Refactor:` - Code restructuring
- `Docs:` - Documentation
- `Test:` - Tests
- `CI:` - CI/CD changes
- `Chore:` - Maintenance tasks

**Examples:**
```bash
git commit -m "Add: batch file upload endpoint"
git commit -m "Fix: cache memory leak in search results"
git commit -m "Update: improve upload validation error messages"
git commit -m "Refactor: extract validators into separate module"
git commit -m "Docs: add API examples to README"
git commit -m "Test: add integration tests for search caching"
```

### Pull Request Process

1. **Create PR with descriptive title:**
   - Title: `Add batch file upload support`
   - Description: Explain what, why, and how

2. **Ensure CI passes:**
   - All tests pass
   - Linting checks pass
   - Coverage meets threshold

3. **Request review** from maintainers

4. **Address feedback:**
   - Make requested changes
   - Push updates to same branch
   - Respond to comments

5. **Merge:**
   - Squash and merge (preferred)
   - Rebase and merge (for clean history)
   - Merge commit (for feature branches)

### Protected Branches

**`main` branch:**
- Requires PR reviews
- Requires passing CI
- No force pushes

**`develop` branch:**
- Same as main
- Used for pre-release testing

**`claude/*` branches:**
- Auto-approved in CI (for AI assistants)
- Can be force-pushed during development
- Should be cleaned up after merging

---

## Troubleshooting Guide

### Common Issues

**1. "ModuleNotFoundError: No module named 'flamehaven_filesearch'"**
```bash
# Solution: Install package in editable mode
pip install -e .
# or with dependencies
pip install -e ".[dev,api,google]"
```

**2. "API key required (API key not provided)"**
```bash
# Solution: Set environment variable
export GEMINI_API_KEY="your-key-here"
# or add to .env file
echo "GEMINI_API_KEY=your-key" >> .env
```

**3. "google.api_core.exceptions.PermissionDenied: 403"**
```bash
# Solution: Check API key is valid and has permissions
# Get new key from: https://makersuite.google.com/app/apikey
export GEMINI_API_KEY="new-valid-key"
```

**4. Tests fail with "google-genai not installed"**
```bash
# Solution: Install optional Google dependency
pip install ".[google]"
# or
pip install google-genai>=0.2.0
```

**5. "Rate limit exceeded" during tests**
```bash
# Solution: Run without integration tests
pytest -m "not integration"

# Or: Use test isolation
export PYTEST_CURRENT_TEST="unique-test-name"
pytest tests/
```

**6. Pre-commit hooks fail**
```bash
# Solution: Auto-fix formatting issues
black flamehaven_filesearch/ tests/ examples/
isort flamehaven_filesearch/ tests/ examples/

# Then retry commit
git add .
git commit -m "Your message"
```

**7. Docker build fails**
```bash
# Solution: Check Dockerfile and dependencies
docker build -t flamehaven-filesearch:latest . --no-cache

# Check logs
docker logs <container-id>
```

**8. API server won't start**
```bash
# Solution: Check for port conflicts
lsof -i :8000  # Check what's using port 8000
kill <PID>     # Kill conflicting process

# Or use different port
export PORT=8080
flamehaven-api
```

**9. Cache not working**
```bash
# Solution: Check cache initialization
curl http://localhost:8000/metrics | jq '.cache'

# Verify cachetools is installed
pip show cachetools

# Re-initialize services
# Restart API server
```

**10. Coverage below threshold**
```bash
# Solution: Check coverage report
pytest --cov=flamehaven_filesearch --cov-report=html
open htmlcov/index.html

# Add tests for uncovered lines
# Focus on red/yellow highlighted code
```

### Debugging Tips

**Enable Debug Logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or set environment variable
export FLAMEHAVEN_DEBUG=1
export ENVIRONMENT=development
```

**Inspect Request/Response:**
```python
# In api.py, add logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
```

**Test Specific Scenario:**
```python
# Create isolated test
def test_specific_issue():
    config = Config(max_file_size_mb=50)
    fs = FlamehavenFileSearch(config=config, allow_offline=True)

    # Reproduce issue
    result = fs.upload_file("test.pdf")

    # Add debug prints
    import pprint
    pprint.pprint(result)

    # Assert expected behavior
    assert result["status"] == "success"
```

**Check System Resources:**
```bash
# CPU/Memory usage
htop

# Disk space
df -h

# Network connections
netstat -tuln | grep 8000
```

### Getting Help

**Resources:**
- **Documentation:** `README.md`, `CONTRIBUTING.md`, `SECURITY.md`
- **Examples:** `examples/` directory
- **Tests:** `tests/` directory (show usage patterns)
- **Issues:** https://github.com/flamehaven01/Flamehaven-Filesearch/issues
- **Discussions:** https://github.com/flamehaven01/Flamehaven-Filesearch/discussions

**Before asking for help:**
1. Check this CLAUDE.md file
2. Search existing issues
3. Read error messages carefully
4. Check logs (`ENVIRONMENT=development`)
5. Try with minimal reproducible example

**When reporting issues:**
- Include Python version (`python --version`)
- Include package version (`pip show flamehaven-filesearch`)
- Include error messages (full traceback)
- Include steps to reproduce
- Include environment (OS, Docker, etc.)

---

## Key Files Reference

### Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Project metadata, dependencies, tool config |
| `pytest.ini` | Pytest configuration |
| `.pre-commit-config.yaml` | Pre-commit hooks |
| `.env.example` | Environment variable template |
| `.gitignore` | Git ignore patterns |
| `Dockerfile` | Docker container definition |
| `docker-compose.yml` | Docker Compose setup |
| `Makefile` | Development commands |
| `requirements.txt` | Core dependencies (generated) |

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | User-facing documentation |
| `CLAUDE.md` | AI assistant guide (this file) |
| `CONTRIBUTING.md` | Contribution guidelines |
| `SECURITY.md` | Security policy |
| `CHANGELOG.md` | Version history |
| `UPGRADING.md` | Upgrade instructions |
| `RELEASE_NOTES.md` | Release announcements |
| `examples/README.md` | Example documentation |

### Source Files

| File | Purpose | Key Components |
|------|---------|----------------|
| `flamehaven_filesearch/__init__.py` | Package exports | Version, public API |
| `flamehaven_filesearch/core.py` | Core logic | `FlamehavenFileSearch` |
| `flamehaven_filesearch/api.py` | REST API | FastAPI app, endpoints |
| `flamehaven_filesearch/config.py` | Configuration | `Config` dataclass |
| `flamehaven_filesearch/cache.py` | Caching | `SearchCache` |
| `flamehaven_filesearch/metrics.py` | Monitoring | `MetricsCollector` |
| `flamehaven_filesearch/validators.py` | Validation | Input sanitization |
| `flamehaven_filesearch/exceptions.py` | Errors | Custom exceptions |
| `flamehaven_filesearch/logging_config.py` | Logging | JSON & dev loggers |
| `flamehaven_filesearch/middlewares.py` | Middleware | Security, CORS |

---

## Appendix: Quick Reference

### Environment Variables Cheat Sheet

```bash
# Required
GEMINI_API_KEY=AIza...           # Google Gemini API key

# Common
ENVIRONMENT=production           # production or development
MAX_FILE_SIZE_MB=50              # Max file size
DEFAULT_MODEL=gemini-2.5-flash   # Gemini model
WORKERS=4                        # Production workers

# Advanced
MAX_OUTPUT_TOKENS=1024           # Max response tokens
TEMPERATURE=0.5                  # Model temperature
MAX_SOURCES=5                    # Max citations
CACHE_TTL_SEC=3600              # Cache TTL (1 hour)
```

### Common Commands Cheat Sheet

```bash
# Setup
pip install -e ".[dev,api,google]"
cp .env.example .env
pre-commit install

# Testing
pytest -v                        # All tests
pytest -m "not integration"      # Skip integration
pytest --cov --cov-report=html   # With coverage

# Formatting
make format                      # Auto-format
make lint                        # Check linting

# Server
flamehaven-api                   # Start API server
make server                      # Development mode
docker-compose up                # Docker

# Build
make build                       # Build package
make publish-test                # TestPyPI
make publish                     # PyPI
```

### HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful request |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Invalid API key |
| 404 | Not Found | Store/resource not found |
| 413 | Payload Too Large | File size exceeded |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server-side error |
| 503 | Service Unavailable | Service not initialized |

### Test Markers

```bash
pytest -m integration        # Integration tests (requires API)
pytest -m "not integration"  # Skip integration tests
pytest -m security          # Security tests only
pytest -m slow              # Long-running tests
```

### Important URLs

- **API Docs:** http://localhost:8000/docs
- **Health:** http://localhost:8000/health
- **Metrics:** http://localhost:8000/metrics
- **Prometheus:** http://localhost:8000/prometheus
- **Repository:** https://github.com/flamehaven01/Flamehaven-Filesearch
- **PyPI:** https://pypi.org/project/flamehaven-filesearch/
- **Google AI Studio:** https://makersuite.google.com/app/apikey

---

## Changelog for CLAUDE.md

**2025-11-16 - v1.0.0:**
- Initial comprehensive documentation
- Based on repository analysis of v1.1.0 codebase
- Covers all major components and workflows
- Includes troubleshooting guide and quick reference

---

**For questions or updates to this guide, please open an issue or PR.**
