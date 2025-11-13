# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-11-11

### 🎉 FLAMEHAVEN File Search Tool - Official Release!

**Major Announcement:** Initial release of FLAMEHAVEN FileSearch - the FLAMEHAVEN File Search Tool is now open source!

### Added
- Core `FlamehavenFileSearch` class for file search and retrieval
- Support for PDF, DOCX, MD, TXT files
- File upload with basic validation (max 50MB in Lite tier)
- Search with automatic citation (max 5 sources)
- FastAPI-based REST API server
- Multiple endpoint support:
  - POST /upload - Single file upload
  - POST /upload-multiple - Batch file upload
  - POST /search - Search with full parameters
  - GET /search - Simple search queries
  - GET /stores - List all stores
  - POST /stores - Create new store
  - DELETE /stores/{name} - Delete store
  - GET /health - Health check
  - GET /metrics - Service metrics
- Configuration management via environment variables
- Docker support with Dockerfile and docker-compose.yml
- CI/CD pipeline with GitHub Actions
- Comprehensive test suite (pytest)
- Code quality tools (black, flake8, isort, mypy)
- PyPI packaging with pyproject.toml
- Full documentation and examples

### Features
- Google Gemini 2.5 Flash integration
- Automatic grounding with source citations
- Driftlock validation (banned terms, length checks)
- Multiple store management
- Batch file operations
- Configurable model parameters
- Error handling and validation
- CORS support
- Health checks and metrics

### Documentation
- Comprehensive README with quick start guide
- API documentation (OpenAPI/Swagger)
- Usage examples (library and API)
- Contributing guidelines
- License (MIT)

## [1.1.0] - 2025-11-13

### 🚀 Major Upgrade: Security, Performance, and Production Readiness

**SIDRCE Score**: 0.94 (Certified) - Up from 0.842

This release represents a comprehensive upgrade to production-ready status with critical security fixes, performance optimization, and enterprise-grade monitoring.

### 🔒 Security (Phase 1 & 3)

#### Fixed
- **CRITICAL**: Path traversal vulnerability in file upload endpoints (CVE-2025-XXXX)
  - Added `os.path.basename()` sanitization to prevent directory traversal attacks
  - Block hidden files and empty filenames
  - Reject attack vectors: `../../etc/passwd`, `.env`, malicious filenames
- **CRITICAL**: Starlette CVE-2024-47874 and CVE-2025-54121
  - Upgraded FastAPI 0.104.0 → 0.121.1
  - Upgraded Starlette 0.38.6 → 0.49.3
  - Fixed DoS vulnerabilities in multipart parsing
- Fixed ImportError: Replaced deprecated `google-generativeai` with `google-genai>=0.2.0`
- Fixed offline mode API key enforcement (conditional validation)

#### Added
- Rate limiting with slowapi
  - Uploads: 10/minute (single), 5/minute (multiple)
  - Search: 100/minute
  - Store management: 20/minute
  - Monitoring: 100/minute
- Request ID tracing
  - X-Request-ID header support
  - UUID generation for all requests
  - Request ID in logs and error responses
- OWASP-compliant security headers
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - X-XSS-Protection: 1; mode=block
  - Strict-Transport-Security
  - Content-Security-Policy
  - Referrer-Policy
  - Permissions-Policy
- Comprehensive input validation
  - FilenameValidator: Path traversal prevention
  - FileSizeValidator: Size limit enforcement
  - SearchQueryValidator: XSS/SQL injection detection
  - ConfigValidator: Type and range validation
  - MimeTypeValidator: Whitelist enforcement

### ⚡ Performance (Phase 4)

#### Added
- LRU caching with TTL (1000 items, 1-hour TTL)
  - Cache hit: <10ms response (99% faster than 2-3s API calls)
  - Cache miss tracking and statistics
  - SHA256 cache key generation
  - Expected 40-60% reduction in Gemini API costs
- Structured JSON logging
  - CustomJsonFormatter with service metadata
  - Request ID injection in all log records
  - Environment-aware (JSON for production, readable for development)
  - Log aggregation compatibility (ELK, Splunk, Datadog)

### 📊 Monitoring (Phase 4)

#### Added
- Prometheus metrics (17 metrics total)
  - HTTP: `http_requests_total`, `http_request_duration_seconds`, `active_requests`
  - Uploads: `file_uploads_total`, `file_upload_size_bytes`, `file_upload_duration_seconds`
  - Search: `search_requests_total`, `search_duration_seconds`, `search_results_count`
  - Cache: `cache_hits_total`, `cache_misses_total`, `cache_size`
  - Rate limiting: `rate_limit_exceeded_total`
  - Errors: `errors_total` (by type and endpoint)
  - System: `system_cpu_usage_percent`, `system_memory_usage_percent`, `system_disk_usage_percent`
  - Stores: `stores_total`
- New `/prometheus` endpoint for metrics export
- Enhanced `/metrics` endpoint with cache statistics
- MetricsCollector helper class
- RequestMetricsContext for automatic request timing

### 🎯 Error Handling (Phase 3)

#### Added
- Standardized exception hierarchy (14 custom exception classes)
  - FileSearchException base class
  - FileSizeExceededError, InvalidFilenameError, EmptySearchQueryError
  - RateLimitExceededError, ServiceUnavailableError, etc.
- Structured error responses
  - Error code, message, status code, details, request ID, timestamp
- Enhanced error handlers
  - FileSearchException handler
  - HTTPException handler
  - General exception handler with logging

### 🤖 Automation (Phase 2)

#### Added
- GitHub Actions security workflow
  - Bandit (SAST), Safety (dependency scanner), Trivy, CodeQL
  - Daily scheduled scans at 2 AM UTC
  - SARIF output to GitHub Security Dashboard
  - Fail on HIGH severity findings
- GitHub Actions secrets scanning
  - Gitleaks, TruffleHog, custom patterns
  - Environment file validation
  - Full git history scanning
- Pre-commit hooks
  - Code formatting (black, isort)
  - Linting (flake8)
  - Security scanning (bandit, gitleaks)
  - Custom security checks
  - 90% coverage validation
- Comprehensive test suites
  - Security tests (27 tests): Path traversal, input validation, API key handling
  - Edge case tests (34 tests): Boundary conditions, Unicode, concurrency
  - Performance tests (15 tests): Response time, throughput, scalability
  - Integration tests (20+ tests): Request tracing, security headers, rate limiting
- Golden baseline for drift detection
  - Dependencies baseline
  - Security posture
  - SIDRCE metrics (0.87 → 0.94)
  - Validation commands
  - Rollback procedures

### 📝 Documentation

#### Added
- LICENSE file (MIT License, restored after deletion)
- PHASE1_COMPLETION_SUMMARY.md
- PHASE2_COMPLETION_SUMMARY.md
- PHASE3_COMPLETION_SUMMARY.md
- PHASE4_COMPLETION_SUMMARY.md
- .golden_baseline.json
- .pre-commit-config.yaml

#### Changed
- README.md: Updated with v1.1.0 features
- API documentation: Enhanced with rate limits and new endpoints
- CLI help: Comprehensive feature list

### 🔧 Technical Improvements

#### Changed
- API rewrite (661 lines → 910 lines)
  - Integrated caching throughout
  - Metrics collection on all endpoints
  - Enhanced error handling
  - Improved logging
- Enhanced health endpoint
  - System metrics (CPU, memory, disk)
  - Uptime formatting
  - Searcher initialization status
  - ISO 8601 timestamps

#### Dependencies
- Added: `slowapi>=0.1.9` (rate limiting)
- Added: `psutil>=5.9.0` (system metrics)
- Added: `python-json-logger>=2.0.0` (structured logging)
- Added: `cachetools>=5.3.0` (LRU caching)
- Added: `prometheus-client>=0.19.0` (metrics)
- Added: `requests>=2.31.0` (Docker health checks)
- Added: `bandit>=1.7.0`, `safety>=3.0.0` (security scanning)
- Updated: `fastapi>=0.121.1` (CVE fixes)
- Updated: `google-genai>=0.2.0` (replaced deprecated package)

### 📈 Impact

- **Performance**: 99% latency reduction on cache hits
- **Cost**: 40-60% reduction in Gemini API costs
- **Security**: Zero CRITICAL vulnerabilities, all CVEs patched
- **Observability**: Comprehensive metrics and structured logging
- **Reliability**: 90% test coverage, automated quality gates
- **Production Readiness**: Enterprise-grade features

### 🔄 Migration from v1.0.0

See [UPGRADING.md](UPGRADING.md) for detailed migration guide.

**Breaking Changes**: None (fully backward compatible)

**Recommended Actions**:
1. Update dependencies: `pip install -U flamehaven-filesearch[api]`
2. Configure environment: `ENVIRONMENT=production` (default)
3. Set up Prometheus scraping: See PHASE4_COMPLETION_SUMMARY.md
4. Review rate limits: Adjust if needed for your use case

---

## [Unreleased]

### Planned for v1.2.0
- [ ] Authentication/API keys
- [ ] Enhanced file type support
- [ ] Batch search operations
- [ ] Export search results
- [ ] WebSocket support for streaming
- [ ] Admin dashboard
- [ ] Redis cache for multi-worker deployments

### Future Enhancements
- Standard tier with advanced features
- Compliance features (GDPR, SOC2)
- Custom model fine-tuning
- Advanced analytics
- Multi-language support
- On-premise deployment options
