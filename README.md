# SovDef FileSearch Lite 🔍

[![CI/CD](https://github.com/flamehaven01/SovDef-FileSearch-Lite/actions/workflows/ci.yml/badge.svg)](https://github.com/flamehaven01/SovDef-FileSearch-Lite/actions)
[![PyPI version](https://badge.fury.io/py/sovdef-filesearch-lite.svg)](https://badge.fury.io/py/sovdef-filesearch-lite)
[![Python Versions](https://img.shields.io/pypi/pyversions/sovdef-filesearch-lite.svg)](https://pypi.org/project/sovdef-filesearch-lite/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**MVP용 경량 파일 검색 시스템**
Google File Search 수준의 편의성 + 기본 품질 보장

---

## 🎯 Features

- **5분 내 배포**: 간단한 API로 즉시 시작
- **Google Gemini 기반**: 최신 AI 모델로 정확한 답변 생성
- **자동 Citation**: 모든 답변에 출처 자동 첨부
- **RESTful API**: FastAPI 기반 프로덕션 레디 서버
- **경량화**: Lite 티어로 빠른 시작, 필요시 Standard로 업그레이드
- **Docker 지원**: 컨테이너 배포 가능

---

## 🚀 Quick Start

### Installation

```bash
# Core library only
pip install sovdef-filesearch-lite

# With API server
pip install sovdef-filesearch-lite[api]

# Development tools
pip install sovdef-filesearch-lite[dev]
```

### Basic Usage (Library)

```python
from sovdef_filesearch_lite import SovDefLite
import os

# Set API key
os.environ["GEMINI_API_KEY"] = "your-api-key"

# Initialize
searcher = SovDefLite()

# Upload file
result = searcher.upload_file("my_document.pdf")
print(f"Upload: {result['status']}")

# Search
answer = searcher.search("What are the key findings?")
print(f"Answer: {answer['answer']}")
print(f"Sources: {answer['sources']}")
```

**That's it! 5 lines to complete file search system.**

---

## 📡 API Server

### Start Server

```bash
# Set environment variable
export GEMINI_API_KEY="your-api-key"

# Start server
uvicorn sovdef_filesearch_lite.api:app --reload
```

Server runs on `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

### API Endpoints

#### 1. Upload File

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf" \
  -F "store=default"
```

#### 2. Search

```bash
# POST method
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the key findings?",
    "store_name": "default"
  }'

# GET method (simple)
curl "http://localhost:8000/search?q=key+findings&store=default"
```

#### 3. Upload Multiple Files

```bash
curl -X POST "http://localhost:8000/upload-multiple" \
  -F "files=@doc1.pdf" \
  -F "files=@doc2.pdf" \
  -F "store=research"
```

#### 4. Manage Stores

```bash
# List stores
curl "http://localhost:8000/stores"

# Create store
curl -X POST "http://localhost:8000/stores" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-store"}'

# Delete store
curl -X DELETE "http://localhost:8000/stores/my-store"
```

#### 5. Health & Metrics

```bash
# Health check
curl "http://localhost:8000/health"

# Metrics
curl "http://localhost:8000/metrics"
```

---

## 🐳 Docker Deployment

### Build & Run

```bash
# Build image
docker build -t sovdef-filesearch-lite .

# Run container
docker run -d \
  -p 8000:8000 \
  -e GEMINI_API_KEY="your-api-key" \
  --name sovdef-api \
  sovdef-filesearch-lite
```

### Docker Compose

```yaml
version: '3.8'

services:
  sovdef-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - MAX_FILE_SIZE_MB=50
      - DEFAULT_MODEL=gemini-2.5-flash
    volumes:
      - ./uploads:/tmp/uploads
    restart: unless-stopped
```

Run with: `docker-compose up -d`

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | **Required** |
| `MAX_FILE_SIZE_MB` | Maximum file size | 50 |
| `UPLOAD_TIMEOUT_SEC` | Upload timeout | 60 |
| `DEFAULT_MODEL` | Gemini model | gemini-2.5-flash |
| `MAX_OUTPUT_TOKENS` | Max response tokens | 1024 |
| `TEMPERATURE` | Model temperature | 0.5 |
| `MAX_SOURCES` | Max citation sources | 5 |

### Programmatic Configuration

```python
from sovdef_filesearch_lite import SovDefLite, Config

config = Config(
    api_key="your-api-key",
    max_file_size_mb=100,
    default_model="gemini-2.5-flash",
    temperature=0.7,
    max_sources=10
)

searcher = SovDefLite(config=config)
```

---

## 📚 Advanced Usage

### Multiple Stores

```python
# Create separate stores for different projects
searcher.create_store("research")
searcher.create_store("legal")

# Upload to specific stores
searcher.upload_file("paper.pdf", store_name="research")
searcher.upload_file("contract.pdf", store_name="legal")

# Search in specific stores
answer = searcher.search("patent claims", store_name="legal")
```

### Batch Upload

```python
files = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
result = searcher.upload_files(files, store_name="default")

print(f"Uploaded: {result['success']}/{result['total']}")
```

### Custom Model Parameters

```python
answer = searcher.search(
    query="Summarize the main points",
    model="gemini-2.5-flash",
    max_tokens=2048,
    temperature=0.3
)
```

---

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=sovdef_filesearch_lite --cov-report=html

# Run specific test
pytest tests/test_core.py -v
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   SovDef FileSearch Lite                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐         ┌──────────────┐            │
│  │   FastAPI    │────────▶│  SovDefLite  │            │
│  │   Server     │         │     Core     │            │
│  └──────────────┘         └──────┬───────┘            │
│         │                         │                    │
│         │                         ▼                    │
│         │                 ┌──────────────┐            │
│         │                 │    Config    │            │
│         │                 └──────────────┘            │
│         │                         │                    │
│         ▼                         ▼                    │
│  ┌─────────────────────────────────────────┐          │
│  │       Google Gemini File Search         │          │
│  │         (gemini-2.5-flash)              │          │
│  └─────────────────────────────────────────┘          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Components

1. **Core Library** (`sovdef_filesearch_lite/core.py`)
   - SovDefLite class
   - File upload & validation
   - Search & retrieval
   - Store management

2. **API Server** (`sovdef_filesearch_lite/api.py`)
   - FastAPI application
   - RESTful endpoints
   - Error handling
   - CORS support

3. **Configuration** (`sovdef_filesearch_lite/config.py`)
   - Environment-based config
   - Validation
   - Driftlock settings

---

## 🎯 Tier Comparison

### Lite (Current)

- ✅ File upload (PDF, DOCX, MD, TXT)
- ✅ Max file size: 50MB
- ✅ Basic validation
- ✅ Google File Search integration
- ✅ Citation support (max 5 sources)
- ✅ Fast deployment (5 minutes)

### Standard (Upgrade Path)

- ✅ All Lite features
- ✅ Max file size: 200MB
- ✅ Advanced validation (SCRIPTORIA)
- ✅ Compliance features
- ✅ Enhanced caching
- ✅ Custom grounding
- ✅ Priority support

**Upgrade when:**
- Monthly queries > 10,000
- Need compliance features
- Require larger files
- Need advanced customization

---

## 🔒 Security

- **No PII Storage**: Files processed but not stored long-term
- **API Key Protection**: Keys only in environment variables
- **Driftlock**: Banned term filtering
- **Input Validation**: File size, type, encoding checks
- **CORS**: Configurable for production

---

## 🐛 Troubleshooting

### Common Issues

**1. API Key Not Found**
```bash
# Set environment variable
export GEMINI_API_KEY="your-key"

# Or in Python
import os
os.environ["GEMINI_API_KEY"] = "your-key"
```

**2. Upload Timeout**
```python
config = Config(upload_timeout_sec=120)  # Increase timeout
```

**3. File Too Large**
```python
searcher.upload_file("large.pdf", max_size_mb=100)
```

**4. Store Not Found**
```python
# Create store first
searcher.create_store("my-store")
searcher.upload_file("doc.pdf", store_name="my-store")
```

---

## 📈 Performance

### Benchmarks (Lite Tier)

| Operation | Time | Notes |
|-----------|------|-------|
| File Upload (10MB) | ~5s | Including validation |
| Search Query | ~2s | With 5 sources |
| Store Creation | ~1s | One-time operation |

### Optimization Tips

1. **Batch uploads**: Use `upload_files()` for multiple files
2. **Store reuse**: Create stores once, reuse for multiple files
3. **Cache results**: Implement application-level caching
4. **Async operations**: Use FastAPI's async capabilities

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Development Setup

```bash
# Clone repo
git clone https://github.com/flamehaven01/SovDef-FileSearch-Lite.git
cd SovDef-FileSearch-Lite

# Install with dev dependencies
pip install -e ".[dev,api]"

# Run tests
pytest

# Format code
black sovdef_filesearch_lite/
isort sovdef_filesearch_lite/

# Lint
flake8 sovdef_filesearch_lite/
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🔗 Links

- **PyPI**: https://pypi.org/project/sovdef-filesearch-lite/
- **GitHub**: https://github.com/flamehaven01/SovDef-FileSearch-Lite
- **Documentation**: [GitHub Wiki](https://github.com/flamehaven01/SovDef-FileSearch-Lite/wiki)
- **Issues**: https://github.com/flamehaven01/SovDef-FileSearch-Lite/issues

---

## 🙏 Acknowledgments

- Built on [Google Gemini API](https://ai.google.dev/)
- Powered by [FastAPI](https://fastapi.tiangolo.com/)
- Inspired by [Google File Search](https://blog.google/technology/developers/file-search-gemini-api/)

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/flamehaven01/SovDef-FileSearch-Lite/issues)
- **Discussions**: [GitHub Discussions](https://github.com/flamehaven01/SovDef-FileSearch-Lite/discussions)
- **Email**: dev@sovdef.ai

---

**Made with ❤️ by SovDef Team**
