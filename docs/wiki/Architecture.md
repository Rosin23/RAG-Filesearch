# Architecture Overview

Flamehaven FileSearch balances simplicity with production-grade safeguards. This
document describes the moving parts so you can extend the system confidently.

---

## 1. High-Level Diagram

```
          ┌───────────────┐        ┌─────────────┐
Request → │ FastAPI Router│ ─────> │ Middleware  │ ──┐
          └───────────────┘        └─────────────┘   │
                                                     ▼
                                                ┌─────────────┐
                                                │ Endpoints   │
                                                │ (upload,    │
                                                │  search,    │
                                                │  metrics)   │
                                                └─────┬───────┘
                                                      │
                                                      ▼
                           ┌────────────────┐   ┌─────────────┐
                           │ FlamehavenFile │   │ Cache Layer │
                           │ Search (core)  │   │ (TTLCache)  │
                           └────────────────┘   └─────────────┘
                                 │                        │
                                 ▼                        ▼
                          ┌────────────┐        ┌────────────────┐
                          │ google-    │        │ Local fallback │
                          │ genai SDK  │        │ store          │
                          └────────────┘        └────────────────┘
```

---

## 2. FastAPI Layer

### Middlewares (`flamehaven_filesearch/middlewares.py`)

1. **RequestIDMiddleware** – injects `request.state.request_id`, propagates
   `X-Request-ID`.
2. **SecurityHeadersMiddleware** – OWASP-compliant headers (`CSP`, `HSTS`,
   `X-Frame-Options`, etc.).
3. **RequestLoggingMiddleware** – structured logging with timing data.
4. **CORSHeadersMiddleware** – handles preflight and wildcard origins.

The order matters: logging wraps the request to capture final status codes.

### Rate Limiting

- SlowAPI `Limiter` uses `rate_limit_key()` which appends the
  `PYTEST_CURRENT_TEST` marker to avoid cross-test collisions.
- Custom handler records Prometheus metrics before returning standard 429
  response.

---

## 3. Core Search Engine

`FlamehavenFileSearch` (in `core.py`) abstracts Gemini vs fallback behavior:

- **Remote Mode** – When `google-genai` is available, files are uploaded to
  Google File Search stores; queries call `models.generate_content`.
- **Local Fallback** – For offline tests, documents are stored in an in-memory
  list. Search returns text snippets around the query.

Responsibilities:

- Store creation/deletion.
- File validation (size, extension) before upload.
- Search post-processing (driftlock: min/max answer length, banned terms).

---

## 4. Validation & Error Handling

- `validators.py` includes classes for filenames, file size, search queries,
  configuration values, and MIME types. Exceptions raised here inherit from
  `FileSearchException`.
- `exceptions.py` defines strongly typed errors (`InvalidFilenameError`,
  `ServiceUnavailableError`, etc.) so endpoints can convert them to HTTP
  responses using `exception_to_response`.
- FastAPI exception handlers ensure consistent JSON payloads across libraries
  (`HTTPException`, `RequestValidationError`, `FileSearchException`, fallback).

---

## 5. Caching Strategy

- Search responses are cached via `cachetools.TTLCache` keyed by query,
  store name, and generation parameters.
- `get_search_cache()` lazily instantiates the cache, enabling dependency
  injection in tests.
- Metrics record hits vs misses to guide tuning.

Future enhancements can plug in Redis or Memcached by re-implementing the cache
interface and updating `get_search_cache`.

---

## 6. Metrics & Observability

`flamehaven_filesearch/metrics.py` registers Prometheus collectors:

- HTTP request counters & histograms.
- File upload/search counters with status labels.
- Cache hits/misses and size gauges.
- System resource gauges (CPU, memory, disk) powered by `psutil`.

`RequestMetricsContext` is a context manager used by middlewares to record
latency per route.

---

## 7. Logging

Two modes (via `ENVIRONMENT`):

- **Production (default)** – JSON logs with `service`, `version`, `request_id`,
  `environment`. Friends with ELK, Datadog, Splunk.
- **Development** – Human-readable format with timestamp and request ID.

`CustomJsonFormatter` normalizes records and injects metadata.

---

## 8. Storage & File Lifecycle

1. Uploaded file saved to temporary directory.
2. Validated via `validate_upload_file`.
3. Passed to `FlamehavenFileSearch.upload_file()` which either uploads to Gemini
   or stores content locally.
4. Temporary directory cleaned up (even on errors, thanks to `finally` block).

---

## 9. Testing Strategy

- Unit tests cover edge cases (`tests/test_edge_cases.py`), security checks,
  integration flows, and performance assertions.
- Additional suites target logging, exceptions, CLI workflows, and validators.
- CI runs `pytest` across Python 3.8–3.12, enforces coverage ≥ 90%.
- Secret scanners (`gitleaks`, `trufflehog`) protect the history.

---

## 10. Extensibility

Ideas for extending the architecture:

- **Authentication** – Add FastAPI dependencies to require API tokens.
- **External Cache** – Replace TTLCache with Redis for multi-instance caching.
- **Async file ingestion** – Offload uploads to Celery or Cloud Tasks.
- **Custom embeddings** – Swap Gemini File Search for a self-hosted vector store.

Understanding the existing structure will make large changes (e.g., switching to
a different LLM provider) straightforward—swap the core client while keeping
FastAPI surface compatible.
