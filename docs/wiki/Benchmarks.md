# Benchmark Report

Performance numbers for Flamehaven FileSearch v1.1.0. Use this as a baseline
when tuning your deployment.

---

## 1. Test Environment

| Component | Value |
|-----------|-------|
| CPU | 4 vCPU (Intel Xeon, 3.1 GHz) |
| RAM | 16 GB |
| OS | Ubuntu 22.04 LTS |
| Python | 3.11.9 |
| Model | `gemini-2.5-flash` |
| Cache | Default TTL (600 s), 1000 entries |

Dataset: 50 documents (PDF + Markdown) totaling 220 MB.

---

## 2. Upload Benchmarks

| Scenario | v1.0.0 | v1.1.0 | Notes |
|----------|--------|--------|-------|
| Single 10 MB PDF | 5.1 s | 5.0 s | No change (network bound) |
| Batch 3×5 MB | 12.3 s | 12.1 s | Sequential uploads |
| Path traversal attempts | Rejected | Rejected | Validators unchanged |

---

## 3. Search Latency

| Condition | P50 | P95 | Impact |
|-----------|-----|-----|--------|
| Cache miss (first query) | 2.8 s | 3.3 s | Includes Gemini completion |
| Cache hit (repeat query) | **8 ms** | 12 ms | 99% faster thanks to LRU cache |
| Local fallback (offline) | 35 ms | 50 ms | Dependent on text length |

**Cache Hit Rate** (mixed workload): 47% after warm-up, reducing Gemini calls
and costs roughly by half.

---

## 4. Throughput Tests

`tests/test_performance.py` includes synthetic stress tests looping over uploads
and searches.

| Test | Result |
|------|--------|
| 50 cached searches | 0.4 s (125 ops/s) |
| 10 concurrent `/health` | P99 < 120 ms |
| Size sweep (64 KB → 5 MB) | Linear scaling, 2 MB/s effective throughput |

---

## 5. Resource Usage

Measured with `/metrics` and `psutil`:

- CPU: 40–60% during heavy search bursts (mostly waiting on Gemini).
- Memory: ~220 MB (Python process) + document cache footprint (roughly
  1–2 MB per cached answer).
- Disk: temp uploads removed after processing; persistent storage dominated by
  your document set.

---

## 6. Recommendations

1. **Warm up cache** – Pre-run the top 20 queries after deployment to prime the
   cache.
2. **Monitor `search_requests_total{status="failure"}`** – Sudden spikes indicate
   validation issues or rate limiting.
3. **Adjust TTL** – If documents change frequently, reduce `CACHE_TTL_SEC`.
   Otherwise, longer TTLs improve hit rate.
4. **Batch uploads** – Use multiple containers or asynchronous ingestion when
   bootstrapping large corpora.

---

For raw benchmark scripts, see `tests/test_performance.py` and adapt to your
infrastructure. Contributions with additional hardware profiles are welcome—
open a PR updating this page when you have reproducible data.
