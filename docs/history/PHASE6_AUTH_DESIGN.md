# Phase 6: API Authentication & Authorization (v1.2.0)

**Status:** Design Phase
**Date:** 2025-11-16
**Target:** Complete authentication system for v1.2.0

---

## 1. Architecture Overview

### 1.1 Authentication Flow

```
Client Request
    ↓
Extract API Key from Authorization: Bearer <key>
    ↓
Validate Key in Database
    ↓
Load User/Key Context (rate limits, permissions)
    ↓
Execute Route with User Context
    ↓
Record Audit Log (request_id, api_key_id, duration)
    ↓
Response with request_id header
```

### 1.2 Database Schema

**Table: api_keys**
```sql
CREATE TABLE api_keys (
  id TEXT PRIMARY KEY,                          -- UUID
  name TEXT NOT NULL,                           -- User-friendly name
  key_hash TEXT NOT NULL UNIQUE,                -- SHA256 of actual key
  user_id TEXT NOT NULL,                        -- User identifier
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  last_used DATETIME,
  expires_at DATETIME,                          -- Optional expiration
  is_active BOOLEAN DEFAULT TRUE,
  rate_limit_per_minute INTEGER DEFAULT 100,
  permissions TEXT,                             -- JSON: ["upload", "search", "delete"]
  metadata TEXT                                 -- JSON: custom data
);

CREATE TABLE api_key_usage (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  api_key_id TEXT NOT NULL,
  request_id TEXT NOT NULL,
  endpoint TEXT,
  method TEXT,
  status_code INTEGER,
  duration_ms INTEGER,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(api_key_id) REFERENCES api_keys(id)
);
```

---

## 2. New Modules

### 2.1 `auth.py` - API Key Management

```python
class APIKeyManager:
    """Manage API keys: generate, validate, revoke"""

    def generate_key(self, user_id: str, name: str) -> str:
        """Generate new API key and return plain text (show only once)"""

    def validate_key(self, key: str) -> Optional[APIKeyInfo]:
        """Validate API key and return metadata"""

    def revoke_key(self, key_id: str) -> bool:
        """Revoke API key"""

    def list_keys(self, user_id: str) -> List[APIKeyInfo]:
        """List all keys for user (without secret)"""
```

### 2.2 `security.py` - FastAPI Dependencies

```python
async def get_current_api_key(request: Request) -> APIKeyInfo:
    """Extract and validate API key from Authorization header"""

async def require_permission(permission: str):
    """Check if current key has permission"""
```

### 2.3 `audit.py` - Audit Logging

```python
def log_api_request(api_key_id: str, request_id: str, endpoint: str,
                    duration_ms: int, status_code: int):
    """Record API request in audit log"""
```

---

## 3. API Changes

### 3.1 Protected Routes (Require API Key)

- ✅ `POST /api/upload/single` → requires "upload" permission
- ✅ `POST /api/upload/multiple` → requires "upload" permission
- ✅ `POST /api/search` → requires "search" permission
- ✅ `DELETE /api/stores/{name}` → requires "delete" permission
- ✅ `POST /api/stores` → requires "store_create" permission

### 3.2 Public Routes (No Auth Required)

- ✅ `GET /health` → Public health check
- ✅ `GET /docs` → OpenAPI docs
- ✅ `GET /metrics` → Public metrics (deprecated, use /prometheus)
- ✅ `GET /prometheus` → Prometheus metrics

### 3.3 New Admin Routes (Require Auth)

- 🆕 `POST /api/admin/keys` → Create new API key
- 🆕 `GET /api/admin/keys` → List user's API keys
- 🆕 `DELETE /api/admin/keys/{key_id}` → Revoke API key
- 🆕 `GET /api/admin/usage` → Usage statistics
- 🆕 `GET /api/admin/dashboard` → Admin dashboard (HTML)

---

## 4. Implementation Phases

### Phase 4a: API Key Management (2 hours)
- [ ] Create `auth.py` with APIKeyManager
- [ ] Create database schema
- [ ] Implement key generation and hashing
- [ ] Write tests for API key generation

### Phase 4b: Authentication Middleware (2 hours)
- [ ] Create `security.py` with FastAPI dependencies
- [ ] Create `audit.py` for audit logging
- [ ] Add authentication middleware to protected routes
- [ ] Write tests for key validation

### Phase 4c: Admin API (1.5 hours)
- [ ] Implement admin endpoints
- [ ] Add usage statistics tracking
- [ ] Update metrics to track per-key usage
- [ ] Write integration tests

### Phase 4d: Database & Persistence (1 hour)
- [ ] Create SQLite database file
- [ ] Add migrations
- [ ] Test database operations

### Phase 4e: Documentation (1 hour)
- [ ] Update README with authentication
- [ ] Add security guide
- [ ] Add API key management guide
- [ ] Update CHANGELOG

---

## 5. Example Usage

### Generate API Key (Admin)

```bash
curl -X POST http://localhost:8000/api/admin/keys \
  -H "Authorization: Bearer admin-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Production Upload",
    "permissions": ["upload", "search"],
    "rate_limit_per_minute": 50
  }'

Response:
{
  "id": "key_abc123",
  "key": "sk_live_xxxxxxxxxxxxxxxxxxx",  // Shown only once!
  "created_at": "2025-11-16T10:00:00Z"
}
```

### Use API Key (Client)

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Authorization: Bearer sk_live_xxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the vacation policy?"}'

Response:
{
  "status": "success",
  "answer": "...",
  "request_id": "uuid-here"
}
```

### Check Usage (Admin)

```bash
curl http://localhost:8000/api/admin/usage \
  -H "Authorization: Bearer admin-key"

Response:
{
  "total_requests": 1234,
  "total_uploads": 45,
  "total_searches": 1189,
  "by_key": {
    "key_abc123": {
      "requests": 1000,
      "last_used": "2025-11-16T10:30:00Z"
    }
  }
}
```

---

## 6. Security Considerations

### 6.1 Key Storage
- Keys stored as SHA256 hash in database
- Plain key shown only once on creation
- No recovery mechanism (user must regenerate)

### 6.2 Rate Limiting
- Per-key rate limiting (not just per IP)
- Can set custom limits per key
- Rate limit exceeded → 429 response

### 6.3 Audit Trail
- Every authenticated request logged
- Includes: api_key_id, request_id, endpoint, duration
- Retention: 90 days (configurable)

### 6.4 Permissions
- Granular permissions: upload, search, delete, admin
- Can restrict keys to specific operations
- Default: all permissions

---

## 7. Backward Compatibility

**v1.1.0 Behavior:**
- All endpoints public (no auth required)
- Works for quick prototypes

**v1.2.0 Breaking Change:**
- Protected endpoints now require API key
- Migration path: Generate "legacy" key with full permissions
- Documentation: Clear upgrade guide

**Mitigation:**
- Provide `flamehaven-legacy-key` for v1.1.0 compatibility
- Environment variable: `FLAMEHAVEN_LEGACY_MODE=true` (disables auth)
- Clear deprecation notice (v1.2.0)

---

## 8. Testing Strategy

**Unit Tests:**
- API key generation/validation
- Permission checking
- Rate limit calculations

**Integration Tests:**
- Protected endpoint access
- Rate limiting enforcement
- Audit logging

**End-to-End Tests:**
- Full authentication flow
- Key management workflow
- Admin dashboard

---

## 9. Timeline

| Phase | Task | Duration | Target Date |
|-------|------|----------|-------------|
| 4a | API Key Management | 2h | Today |
| 4b | Authentication | 2h | Today |
| 4c | Admin API | 1.5h | Today |
| 4d | Database | 1h | Today |
| 4e | Documentation | 1h | Today |
| Test | Comprehensive testing | 2h | Today |
| **Total** | **Phase 6** | **~9.5h** | **Today** |

---

## 10. Success Criteria

- ✅ All protected endpoints require valid API key
- ✅ API keys can be created/revoked via admin API
- ✅ Per-key rate limiting works correctly
- ✅ Audit log records all authenticated requests
- ✅ Tests pass with 90%+ coverage
- ✅ Documentation updated
- ✅ Zero security vulnerabilities (bandit scan)
- ✅ SIDRCE score maintained (≥0.88)

---

**Next Step:** Start Phase 4a - API Key Management implementation
