# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-11

### Added
- Initial release of SovDef FileSearch Lite
- Core `SovDefLite` class for file search and retrieval
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

## [Unreleased]

### Planned for v1.1.0
- [ ] Caching layer for repeated queries
- [ ] Rate limiting
- [ ] Authentication/API keys
- [ ] Enhanced file type support
- [ ] Batch search operations
- [ ] Export search results
- [ ] WebSocket support for streaming
- [ ] Admin dashboard

### Future Enhancements
- Standard tier with advanced features
- Compliance features (GDPR, SOC2)
- Custom model fine-tuning
- Advanced analytics
- Multi-language support
- On-premise deployment options
