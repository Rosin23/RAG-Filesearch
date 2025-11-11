# Examples

This directory contains example code demonstrating how to use SovDef FileSearch Lite.

## Available Examples

### 1. Basic Usage (`basic_usage.py`)

Demonstrates core library functionality:
- Initializing SovDefLite
- Creating stores
- Uploading files
- Searching for information
- Managing stores
- Getting metrics

**Run:**
```bash
export GEMINI_API_KEY="your-api-key"
python examples/basic_usage.py
```

**What it covers:**
- Store creation and management
- Single file upload
- Search with citations
- Metrics collection

### 2. API Client (`api_example.py`)

Shows how to interact with the SovDef API server:
- Using the API client class
- Uploading files via HTTP
- Searching via REST API
- Managing stores via API
- Error handling

**Prerequisites:**
```bash
# Terminal 1: Start API server
export GEMINI_API_KEY="your-api-key"
uvicorn sovdef_filesearch_lite.api:app --reload

# Terminal 2: Run example
python examples/api_example.py
```

**What it covers:**
- API client implementation
- File upload (single and multiple)
- Search (POST and GET methods)
- Store operations
- Health checks and metrics

## Quick Start Examples

### Minimal Example (3 lines)

```python
from sovdef_filesearch_lite import SovDefLite

searcher = SovDefLite(api_key="your-key")
searcher.upload_file("document.pdf")
result = searcher.search("What are the key points?")
print(result['answer'])
```

### API Example (curl)

```bash
# Upload
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf"

# Search
curl "http://localhost:8000/search?q=key+points"
```

## Creating Your Own Examples

### Template Structure

```python
from sovdef_filesearch_lite import SovDefLite
import os

# 1. Setup
api_key = os.getenv("GEMINI_API_KEY")
searcher = SovDefLite(api_key=api_key)

# 2. Upload
result = searcher.upload_file("your_file.pdf")
print(f"Upload: {result['status']}")

# 3. Search
answer = searcher.search("your question")
print(f"Answer: {answer['answer']}")
print(f"Sources: {len(answer['sources'])}")
```

## Common Use Cases

### 1. Document Q&A

```python
# Upload technical documentation
searcher.upload_file("api_docs.pdf", store_name="docs")

# Ask questions
answer = searcher.search("How do I authenticate?", store_name="docs")
```

### 2. Research Paper Analysis

```python
# Upload multiple papers
papers = ["paper1.pdf", "paper2.pdf", "paper3.pdf"]
searcher.upload_files(papers, store_name="research")

# Find related work
answer = searcher.search(
    "What methodologies do these papers use?",
    store_name="research"
)
```

### 3. Legal Document Search

```python
# Upload contracts
searcher.upload_file("contract.pdf", store_name="legal")

# Search for clauses
answer = searcher.search(
    "What are the termination clauses?",
    store_name="legal",
    temperature=0.1  # Lower temperature for factual queries
)
```

### 4. Multi-Store Organization

```python
# Create separate stores
searcher.create_store("technical")
searcher.create_store("business")
searcher.create_store("legal")

# Upload to appropriate stores
searcher.upload_file("architecture.pdf", store_name="technical")
searcher.upload_file("business_plan.pdf", store_name="business")
searcher.upload_file("terms.pdf", store_name="legal")

# Search in specific context
tech_answer = searcher.search("system architecture", store_name="technical")
biz_answer = searcher.search("revenue model", store_name="business")
```

## Testing Examples

Before running examples:

1. Set API key:
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```

2. Prepare test files:
   - Create a sample PDF, DOCX, or TXT file
   - Update file paths in examples

3. Run examples:
   ```bash
   python examples/basic_usage.py
   ```

## Need Help?

- Check the main [README](../README.md)
- Review [API documentation](http://localhost:8000/docs)
- Open an [issue](https://github.com/flamehaven01/SovDef-FileSearch-Lite/issues)

## Contributing Examples

Have a useful example? Submit a PR!

1. Create a descriptive `.py` file
2. Add comments explaining each step
3. Update this README
4. Test your example
5. Submit PR
