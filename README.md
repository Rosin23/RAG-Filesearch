# 🔥 FLAMEHAVEN FileSearch

**Open‑source semantic document search you can self‑host in minutes.**

[![CI/CD](https://github.com/flamehaven01/Flamehaven-Filesearch/actions/workflows/ci.yml/badge.svg)](https://github.com/flamehaven01/Flamehaven-Filesearch/actions)
[![PyPI](https://img.shields.io/pypi/v/flamehaven-filesearch.svg)](https://pypi.org/project/flamehaven-filesearch/)
[![Python Versions](https://img.shields.io/pypi/pyversions/flamehaven-filesearch.svg)](https://pypi.org/project/flamehaven-filesearch/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

<table>
  <tr>
    <td width="33%">
      <strong>TL;DR</strong><br />
      Lightweight RAG stack (FastAPI + Google Gemini). Upload docs, ask questions, get cited answers. 100% self-hosted & MIT licensed.
    </td>
    <td width="33%">
      <strong>Core Features</strong>
      <ul>
        <li>PDF / DOCX / TXT / MD ingestion (50&nbsp;MB lite cap)</li>
        <li>Python SDK + REST API with Swagger UI</li>
        <li>Store lifecycle (create, list, delete) + source citations</li>
      </ul>
    </td>
    <td width="33%">
      <strong>Install</strong>
      <pre><code>pip install flamehaven-filesearch[api]
export GEMINI_API_KEY="..."
flamehaven-api
      </code></pre>
    </td>
  </tr>
</table>

> Need architecture diagrams, cookbook recipes, or advanced deployment notes? Check the [Wiki](https://github.com/flamehaven01/Flamehaven-Filesearch/wiki).

---

## 📌 Key Features

- **Plug-and-play RAG** – Bring your Gemini key, upload docs, start asking questions.
- **Transparent + auditable** – MIT license, SQLite/file storage, traceable sources.
- **FastAPI server + SDK parity** – Same engine powers CLI, REST, and unit tests.
- **Production-friendly defaults** – Env-based config, Dockerfile, CI badges, logging.
- **Extensible hooks** – Drop-in store adapters or response post-processors.

---

## ⚡ Quick Start

`ash
pip install flamehaven-filesearch[api]
export GEMINI_API_KEY="your-google-gemini-key"
python - <<'PY'
from flamehaven_filesearch import FlamehavenFileSearch
fs = FlamehavenFileSearch()
fs.upload_file("handbook.pdf")
result = fs.search("Summarize onboarding steps")
print(result["answer"])
print(result["sources"])
PY
`

### Run the API server

`ash
flamehaven-api        # entrypoint installed via [api] extra
# or uvicorn flamehaven_filesearch.api:app --reload
`

Open http://localhost:8000/docs for interactive Swagger UI.

### Minimal REST flow

`ash
curl -X POST "http://localhost:8000/upload" -F "file=@report.pdf"
curl "http://localhost:8000/search?q=key+findings&store=default"
`

---

## 🐳 Docker Deployment

`ash
git clone https://github.com/flamehaven01/Flamehaven-Filesearch.git
cd Flamehaven-Filesearch
export GEMINI_API_KEY="..."
docker build -t flamehaven-filesearch .
docker run -e GEMINI_API_KEY -p 8000:8000 \
  -v D:\Sanctum\Flamehaven-Filesearch/data:/app/data flamehaven-filesearch
`

- Mount data/ if you want persistent stores.
- Use FLAMEHAVEN_CONFIG env or .env file for additional overrides.

---

## ⚙️ Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| GEMINI_API_KEY / GOOGLE_API_KEY | required | Gemini credentials for upload/search. |
| MAX_FILE_SIZE_MB | 50 | Lite tier upload limit. |
| UPLOAD_TIMEOUT_SEC | 60 | Upload watchdog. |
| DEFAULT_MODEL | gemini-2.5-flash | Generation model. |
| MAX_OUTPUT_TOKENS | 1024 | Gemini response size. |
| MAX_SOURCES | 5 | Number of cited documents. |
| DATA_DIR | ./data | Local store persistence path. |

See [lamehaven_filesearch/config.py](flamehaven_filesearch/config.py) for the full data class and env mapping.

---

## 📊 Benchmarks

| Operation | Avg Time | Environment |
|-----------|----------|-------------|
| Store creation | ~1s | Ubuntu 22.04, 2 vCPU, 4GB RAM, SSD |
| Upload 10&nbsp;MB PDF | ~5s | Same VM, local disk |
| Search query | ~2s | Gemini 2.5 Flash, 5 cited sources |
| Batch upload (3×5MB) | ~12s | Sequential upload, Python SDK |

> Detailed methodology + raw numbers: [Benchmarks wiki page](https://github.com/flamehaven01/Flamehaven-Filesearch/wiki/Benchmarks).

---

## 🛣️ Roadmap

Roadmap items live in GitHub for transparency:

- [Project board](https://github.com/orgs/flamehaven01/projects?query=Flamehaven-Filesearch)
- [Roadmap issues](https://github.com/flamehaven01/Flamehaven-Filesearch/issues?q=is%3Aopen+label%3Aroadmap)

Highlights in progress:

- Caching layer + rate limiting (v1.1)
- Batch search & WebSocket streaming
- Multi-language, analytics dashboard (v2.0)

---

## 🤝 Contributing

1. Fork & create a feature branch.
2. pip install -e .[dev,api]
3. pytest tests/ (or make test) before opening a PR.
4. Follow [CONTRIBUTING.md](CONTRIBUTING.md) for style, release notes, and checklist.

help wanted + good first issue labels mark low-barrier contributions.

---

## 📬 Support & Links

- Bugs & features: [GitHub Issues](https://github.com/flamehaven01/Flamehaven-Filesearch/issues)
- Q&A / patterns: [Discussions](https://github.com/flamehaven01/Flamehaven-Filesearch/discussions)
- Docs & cookbooks: [Wiki](https://github.com/flamehaven01/Flamehaven-Filesearch/wiki)
- Email: dev@Flamehaven.ai

---

## 📄 License

MIT License © 2025 Flamehaven Team. See [LICENSE](LICENSE) for details.

---

<div align="center">
If this project helps you, ⭐ the repo and tell us what you build!
</div>
