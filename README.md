# FLAMEHAVEN FileSearch

> **Your documents. Searchable in minutes. No infrastructure needed.**

<div align="center">

**로컬 문서를 RAG로 즉시 검색하고 싶을 때**

[![CI/CD](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)](https://github.com/flamehaven01/Flamehaven-Filesearch)
[![Latest Version](https://img.shields.io/badge/Version-v1.2.0-blue)](CHANGELOG.md)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

[🚀 3분 안에 시작](#-3분-안에-시작) • [📖 문서](DEPLOYMENT_GUIDE_v1.2.0.md) • [🎯 로드맵](#-로드맵) • [🤝 기여](CONTRIBUTING.md)

</div>

---

## 🎯 문제: 당신의 상황

```
✗ 로컬에 있는 PDF, Word, 텍스트 문서들을 빠르게 검색하고 싶다
✗ CloudFlare, Pinecone 같은 외부 서비스에 데이터를 올리고 싶지 않다
✗ 복잡한 설정 없이 "지금 당장" 시작하고 싶다
✗ 비용을 최소화하면서 프로덕션 수준의 검색을 원한다
```

---

## ✅ 해결책: FLAMEHAVEN FileSearch

```
✓ 5분 안에 로컬 RAG 검색 엔진 구성
✓ 100% 자체 호스팅 (데이터는 항상 당신 것)
✓ Docker 한 줄로 배포
✓ Gemini의 무료 티어 활용 (월 1500개 쿼리까지 무료)
✓ v1.2.0: 엔터프라이즈급 인증 & 멀티유저 지원
```

---

## ⚡ 3분 안에 시작

### 1️⃣ Docker로 실행 (설정 없음)

```bash
docker run -d \
  -e GEMINI_API_KEY="your_api_key" \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  flamehaven-filesearch:1.2.0

# 3초 후 http://localhost:8000에서 접근 가능
```

### 2️⃣ 첫 번째 검색 (cURL)

```bash
# API 키 생성 (선택사항, v1.2.0)
curl -X POST http://localhost:8000/api/admin/keys \
  -H "X-Admin-Key: admin_key_here" \
  -H "Content-Type: application/json" \
  -d '{"name":"MyKey","permissions":["upload","search"]}'

# → 응답: {"key":"sk_live_xxx..."}

# 파일 업로드
curl -X POST http://localhost:8000/api/upload/single \
  -H "Authorization: Bearer sk_live_xxx..." \
  -F "file=@example.pdf" \
  -F "store=documents"

# 검색 실행
curl -X POST http://localhost:8000/api/search \
  -H "Authorization: Bearer sk_live_xxx..." \
  -H "Content-Type: application/json" \
  -d '{"query":"이 문서에서 핵심 주요 내용은?","store":"documents"}'

# → 응답:
# {
#   "answer": "문서의 핵심 내용은 ...",
#   "sources": [
#     {"file": "example.pdf", "page": 3, "excerpt": "..."}
#   ]
# }
```

### 3️⃣ Python 코드로 사용

```python
from flamehaven_filesearch import FlamehavenFileSearch, FileSearchConfig

# 설정
config = FileSearchConfig(
    google_api_key="your_gemini_key",
    environment="offline"  # 또는 "remote"
)

# 초기화
searcher = FlamehavenFileSearch(config)

# 문서 저장소 생성
searcher.create_store("my_documents")

# 파일 업로드
searcher.upload_file("path/to/document.pdf", "my_documents")

# 검색
result = searcher.search("이 문서의 요약은?", "my_documents")
print(f"답변: {result['answer']}")
print(f"출처: {result['sources']}")
```

---

## 🎁 주요 기능

### 기본 기능 (v1.1.0+)

| 기능 | 설명 | 이점 |
|-----|------|------|
| **📄 다중 형식 지원** | PDF, DOCX, MD, TXT (최대 50MB) | 모든 문서 타입 지원 |
| **🔍 의미론적 검색** | AI 기반 자연어 쿼리 | "키워드" 검색보다 훨씬 정확함 |
| **📎 출처 표시** | 답변과 함께 원본 문서 링크 | 신뢰성 & 투명성 보장 |
| **🗂️ 저장소 관리** | 문서들을 컬렉션으로 구성 | 조직화된 검색 |
| **🔌 Python SDK + REST API** | 통합하기 쉬운 2가지 방식 | 유연한 통합 |
| **⚡ LRU 캐싱** | 1시간 TTL, 1000개 항목 | 캐시 히트 시 <10ms |
| **📊 Prometheus 메트릭** | 17개 모니터링 지표 | 운영 가시성 |
| **🛡️ 보안 헤더** | OWASP 준수 | 엔터프라이즈 보안 |

### 새 기능 (v1.2.0) - 엔터프라이즈급

| 기능 | 설명 | 사용 시나리오 |
|-----|------|-------------|
| **🔐 API 키 인증** | Bearer 토큰 기반 접근 제어 | 멀티유저 환경 |
| **🔑 키 관리 API** | 키 생성, 조회, 해제 | 프로그래매틱 관리 |
| **📋 감사 로깅** | 모든 요청 기록 | 컴플라이언스 |
| **👤 사용자별 레이트 리밋** | 키별 커스텀 한도 | 공정한 리소스 배분 |
| **🏢 어드민 대시보드** | 웹 UI로 키 관리 | 사용자 친화적 운영 |
| **📦 배치 검색** | 1-100개 쿼리 한 번에 | 고속 대량 검색 |
| **💾 Redis 캐시** | 분산 캐싱 지원 | 멀티 워커 배포 |

---

## 🚀 설치 옵션

### 옵션 1: Pip (로컬 개발)

```bash
# 기본 설치
pip install flamehaven-filesearch

# REST API 포함
pip install flamehaven-filesearch[api]

# Redis 캐싱 포함
pip install flamehaven-filesearch[api,redis]
```

### 옵션 2: Docker (권장 - 프로덕션)

```bash
# 이미지 빌드
docker build -t flamehaven-filesearch:1.2.0 .

# 실행
docker run -d \
  -e GEMINI_API_KEY="your_key" \
  -e FLAMEHAVEN_ADMIN_KEY="your_admin_key" \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  flamehaven-filesearch:1.2.0
```

### 옵션 3: Docker Compose (+ Redis)

```bash
# docker-compose.yml 복사하고
docker-compose up -d

# 자동으로 API + Redis 시작
```

### 옵션 4: Kubernetes

```bash
# 매니페스트 적용
kubectl apply -f k8s/

# StatefulSet으로 높은 가용성 확보
```

---

## 🏗️ 아키텍처

```
┌─────────────────┐
│   Client Apps   │
│  (Python/cURL)  │
└────────┬────────┘
         │
    ┌────▼─────────────────────┐
    │  REST API (FastAPI)       │
    │  Authentication (v1.2.0)  │
    └────┬────────────┬─────────┘
         │            │
    ┌────▼──┐    ┌────▼──────────┐
    │ Cache │    │ File Search   │
    │(Redis/│    │  Engine       │
    │ LRU)  │    │               │
    └───────┘    └────┬──────────┘
                      │
                 ┌────▼──────────┐
                 │ Google Gemini │
                 │ (Embeddings + │
                 │  Generation)  │
                 └───────────────┘
```

**데이터 흐름:**
1. 파일 업로드 → 청킹 & 임베딩 생성 → SQLite 저장
2. 검색 쿼리 → 캐시 확인 → Gemini로 답변 생성
3. 응답 → 출처와 함께 반환

---

## 📊 성능

| 작업 | 응답 시간 | 처리량 |
|-----|----------|--------|
| 캐시 히트 검색 | <10ms | N/A |
| 캐시 미스 검색 | 500ms-3s | 2+ req/s |
| 파일 업로드 | 1-5s | 1+ file/s |
| 배치 검색 (10개) | 2-5s | 1+ batch/s |
| 헬스 체크| <1ms | 1000+ req/s |

**비용 절감:** 캐싱으로 Gemini API 호출 **40-60% 감소**

---

## 🛡️ 보안 (v1.2.0)

```
┌─ API 키 인증 (Bearer 토큰)
│  ├─ SHA256 해싱 (평문 저장 안 함)
│  ├─ 권한 제어 (upload, search, stores, delete)
│  └─ 자동 해제/만료
│
├─ 감사 로깅
│  ├─ 모든 요청 기록
│  ├─ Request ID 추적
│  └─ 사용자별 통계
│
├─ 레이트 리밋
│  ├─ 엔드포인트별 리밋
│  └─ API 키별 커스텀 리밋
│
└─ 보안 헤더
   ├─ X-Content-Type-Options: nosniff
   ├─ X-Frame-Options: DENY
   └─ Strict-Transport-Security
```

---

## 📈 로드맵

### v1.x - 안정화 & 확장 (진행 중)

- ✅ v1.1.0: 캐싱, 메트릭, 보안 헤더
- ✅ v1.2.0: API 인증, 대시보드, 배치 검색, Redis
- 🚧 v1.2.1: 개선된 관리자 인증, Redis UI, 암호화
- 📋 v1.3.0: OAuth2/OIDC, 키 로테이션, 빌링

### v2.x - 고급 기능 (계획)

- 📦 벡터DB 플러그인 (Weaviate, Pinecone)
- 🌍 다국어 지원 (한글, 중국어, 일본어)
- 🔗 데이터 커넥터 (Google Drive, Dropbox, S3)
- ⚙️ 커스텀 임베딩 모델
- 🎨 향상된 UI/대시보드

---

## 🤝 기여

### 좋은 첫 이슈 (Good First Issues)

```
좋은 이슈를 찾고 계신가요?

[easy] README 다국어 번역 (한글 ✓ → 일본어, 중국어)
[easy] 문서 예시 추가 (동영상 튜토리얼)
[easy] Docker 예시 개선
[easy] GitHub Actions 배지 추가
[easy] 성능 벤치마크 문서화

찾아보기: github.com/flamehaven01/Flamehaven-Filesearch/issues?q=label:"good first issue"
```

### 기여 프로세스

1. Fork & Clone
2. Feature branch 생성: `git checkout -b feature/your-feature`
3. 커밋: `git commit -m "feat: 설명"`
4. Push: `git push origin feature/your-feature`
5. Pull Request 생성

[자세한 기여 가이드](CONTRIBUTING.md)

---

## 🚀 배포 가이드

### 로컬 개발

```bash
# 1. 저장소 클론
git clone https://github.com/flamehaven01/Flamehaven-Filesearch.git
cd Flamehaven-Filesearch

# 2. 의존성 설치
pip install -e ".[api]"

# 3. Gemini API 키 설정
export GEMINI_API_KEY="your_key"
export FLAMEHAVEN_ADMIN_KEY="admin_key"

# 4. 실행
python -m flamehaven_filesearch.api

# 5. 접근
# http://localhost:8000/admin/dashboard
```

### 프로덕션 배포

- **Docker:** [DEPLOYMENT_GUIDE_v1.2.0.md](DEPLOYMENT_GUIDE_v1.2.0.md) 참조
- **Kubernetes:** K8s 매니페스트 포함
- **Docker Compose:** 자동 Redis 포함

---

## 📚 문서

| 문서 | 설명 |
|-----|------|
| [RELEASE_NOTES_v1.2.0.md](RELEASE_NOTES_v1.2.0.md) | v1.2.0 새 기능 & 마이그레이션 |
| [DEPLOYMENT_GUIDE_v1.2.0.md](DEPLOYMENT_GUIDE_v1.2.0.md) | Docker, K8s, 모니터링 |
| [SECURITY.md](SECURITY.md) | 보안 기능 & API 키 관리 |
| [CHANGELOG.md](CHANGELOG.md) | 전체 변경 이력 |
| [API Reference](http://localhost:8000/docs) | 대화형 API 문서 (Swagger UI) |

---

## ❓ FAQ

### Q: 데이터는 어디에 저장되나요?
**A:** 100% 로컬. `/app/data` 디렉토리(또는 설정한 위치)에 SQLite와 파일이 저장됩니다.

### Q: Gemini API 비용은?
**A:**
- 무료 티어: 월 1500개 요청까지 무료
- 유료: $0.075/1M 입력 토큰, $0.3/1M 출력 토큰
- 캐싱 덕분에 실제 비용은 40-60% 절감

### Q: 멀티유저 지원을 하나요?
**A:** v1.2.0부터 API 키 인증으로 멀티유저 지원. 각 사용자마다 다른 권한 할당 가능.

### Q: 다른 LLM(OpenAI, Claude)를 사용할 수 있나요?
**A:** 현재는 Gemini만 지원. v2.0에 플러그인 아키텍처 예정.

### Q: 얼마나 큰 문서까지 지원하나요?
**A:** 파일당 최대 50MB. 청킹 알고리즘이 자동으로 처리.

### Q: 오프라인에서 작동하나요?
**A:** 부분적으로. 임베딩 생성에는 인터넷 필요(Gemini 호출). 이후 검색은 로컬 캐시 사용 가능.

---

## 📞 지원

- **Issues:** [GitHub Issues](https://github.com/flamehaven01/Flamehaven-Filesearch/issues)
- **Discussions:** [GitHub Discussions](https://github.com/flamehaven01/Flamehaven-Filesearch/discussions)
- **Email:** info@flamehaven.space

---

## 📄 라이선스

MIT License - [LICENSE](LICENSE) 참조

---

## 🙏 감사합니다!

이 프로젝트에 기여해주신 모든 분들께 감사합니다.

⭐ 이 프로젝트가 도움이 되셨다면 Star를 눌러주세요!

---

<div align="center">

**Made with ❤️ by FLAMEHAVEN**

[GitHub](https://github.com/flamehaven01/Flamehaven-Filesearch) • [Website](https://flamehaven.space) • [Twitter](https://twitter.com/flamehaven)

</div>
