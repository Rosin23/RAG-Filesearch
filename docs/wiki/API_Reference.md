# API Reference

All endpoints return JSON unless otherwise noted. Default base URL:
`http://localhost:8000`.

---

## Authentication

Current version operates on trust within your network. For public deployments,
place the API behind an API gateway or enable an authenticating reverse proxy.

---

## Rate Limits

| Endpoint | Limit | Notes |
|----------|-------|-------|
| `/api/upload/single`, `/upload` | `10/minute` | Applies per IP (SlowAPI) |
| `/api/upload/multiple`, `/upload-multiple` | `5/minute` | Heavy operation |
| `/api/search` (GET/POST) | `100/minute` | Caching mitigates load |
| `/metrics`, `/prometheus`, `/health`, `/` | `100/minute` | Observability |

Adjust via environment variables (see `Configuration.md`).

---

## Endpoints

### `GET /`

Returns service metadata.

```json
{
  "name": "FLAMEHAVEN FileSearch API",
  "version": "1.1.0",
  "description": "...",
  "docs": "/docs",
  "health": "/health"
}
```

### `GET /health`

Detailed health check.

```json
{
  "status": "healthy",
  "version": "1.1.0",
  "uptime_seconds": 123.45,
  "uptime_formatted": "2m 3s",
  "searcher_initialized": true,
  "system": {
    "cpu_percent": 12.5,
    "memory_percent": 42.1,
    "disk_percent": 71.2
  }
}
```

### `POST /api/upload/single`

| Key | Type | Description |
|-----|------|-------------|
| `file` | `multipart/form-data` | File to ingest |
| `store` | `form field` | Optional store name (default `default`) |

Response:

```json
{
  "status": "success",
  "store": "default",
  "file": "handbook.pdf",
  "size_mb": 1.23,
  "request_id": "..."
}
```

Errors:

- `400` (invalid filename, size exceeded)
- `503` (service unavailable)

### `POST /api/upload/multiple`

Accepts `files[]`. Returns array of per-file statuses plus summary counts.
Legacy alias: `POST /upload-multiple`.

### `POST /api/search`

Body (`application/json`):

```json
{
  "query": "What is our vacation policy?",
  "store_name": "default",
  "model": null,
  "max_tokens": null,
  "temperature": null
}
```

Response:

```json
{
  "status": "success",
  "answer": "Employees receive ...",
  "sources": [
    {"title": "handbook.pdf", "uri": "gs://...", "page": 5}
  ],
  "model": "gemini-2.5-flash",
  "query": "What is our vacation policy?",
  "store": "default",
  "request_id": "..."
}
```

Possible status codes:

| Code | Meaning |
|------|---------|
| `200` | Answer found (may be from cache) |
| `400` | Invalid query / parameters |
| `404` | Store not found |
| `500` | Unexpected error |

### `GET /api/search`

Convenience endpoint using query string (`?q=...&store=...`). Same response
shape.

### Store Management

| Endpoint | Description |
|----------|-------------|
| `POST /api/stores` | Create store (`{"name": "default"}`) |
| `GET /api/stores` | List stores |
| `DELETE /api/stores/{store}` | Delete store |
| Legacy aliases (`/stores`, `/stores/{store}`, `/stores` via POST) remain for backward compatibility. |

### Metrics & Monitoring

- `GET /metrics` – JSON payload containing store counts, config snapshot, cache
  stats, system metrics.
- `GET /prometheus` – Exposes Prometheus text format (see
  `docs/wiki/Production_Deployment.md`).

### Error Format

All errors follow:

```json
{
  "error": "VALIDATION_ERROR",
  "message": "Invalid filename: ...",
  "detail": "...",
  "status_code": 400,
  "request_id": "abc-123",
  "timestamp": "2025-11-14T07:13:22Z"
}
```

### Legacy Endpoints

- `/upload` → `/api/upload/single`
- `/upload-multiple` → `/api/upload/multiple`
- `/search` → `/api/search` (GET)
- `/stores` → `/api/stores`

These remain for older SDKs but new integration should prefer the `/api/*`
namespace.

---

## SDK Usage Recap

Python SDK is a thin wrapper over the same endpoints:

```python
from flamehaven_filesearch import FlamehavenFileSearch

fs = FlamehavenFileSearch()
fs.upload_file("handbook.pdf")
result = fs.search("vacation policy")
```

Under the hood it configures `FlamehavenFileSearch.config` and calls the same
validation logic, so configuration options are identical.

---

For OpenAPI schema, open `/openapi.json` or visit `/docs` (Swagger UI) /
`/redoc`.
