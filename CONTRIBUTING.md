# Contributing to FLAMEHAVEN FileSearch

Thank you for considering contributing to FLAMEHAVEN FileSearch! This project is built and improved by the community.

## Ways to Contribute

### 1. Bug Reports

Found a bug? Please report it on [GitHub Issues](https://github.com/flamehaven01/Flamehaven-Filesearch/issues).

**Effective bug report template:**

```markdown
## Bug Description
[Clear and concise description]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Expected vs Actual result]

## Environment
- OS: [Windows/Mac/Linux]
- Python: [version]
- flamehaven-filesearch: [version]

## Error Logs
[Output/Stack trace]

## Additional Context
[Screenshots, configuration, etc]
```

### 2. Feature Requests

Want to suggest a new feature?

**Before submitting:**
- Check [Roadmap](README.md#-roadmap) for planned features
- Search [Discussions](https://github.com/flamehaven01/Flamehaven-Filesearch/discussions) for similar requests

### 3. Code Contributions

#### Good First Issues

Perfect for newcomers - look for issues labeled:
- **good first issue** - Recommended for first-time contributors
- **documentation** - Documentation improvements
- **bug** - Small bugs with clear requirements
- **refactor** - Small refactoring tasks

#### Step-by-Step Guide

1. **Fork the Repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/Flamehaven-Filesearch.git
   cd Flamehaven-Filesearch
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   git checkout -b fix/your-bug-fix
   ```

3. **Set Up Development Environment**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Implement & Test**
   ```bash
   pytest tests/ -v
   black flamehaven_filesearch/
   isort flamehaven_filesearch/
   flake8 flamehaven_filesearch/
   ```

5. **Commit Changes**
   ```bash
   git commit -m "feat: description"
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Open PR on GitHub
   - Wait for CI/CD tests
   - Address review feedback
   - Merge!

---

## Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Scopes:** `auth`, `api`, `cache`, `docs`, `test`

**Examples:**
```bash
feat(auth): add API key rotation
fix(cache): fix Redis connection timeout
docs: add Kubernetes deployment guide
```

---

## Testing Requirements

All new features must include tests:

```python
# tests/test_my_feature.py
import pytest

class TestMyFeature:
    def test_basic_functionality(self):
        result = my_function("input")
        assert result == "expected"

    def test_edge_case(self):
        with pytest.raises(ValueError):
            my_function(None)
```

**Requirements:**
- Minimum 90% code coverage
- All existing tests must pass
- New features should aim for 100% coverage

---

## Code Review Criteria

Your PR will be evaluated on:

### Code Quality
- PEP 8 compliant
- Type hints included
- Comments for complex logic
- No dead code
- DRY principle followed

### Testing
- Tests for new features included
- All existing tests pass
- 90%+ code coverage
- Edge cases tested

### Documentation
- Docstrings for functions/classes
- README updated (if needed)
- CHANGELOG updated
- Major changes explained

### Compatibility
- Python 3.8+ support
- Works on Windows, Mac, Linux
- Docker compatible

---

## Development Setup

### Quick Start

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/Flamehaven-Filesearch.git
cd Flamehaven-Filesearch

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dev dependencies
pip install -e ".[dev]"

# Verify with tests
pytest tests/ -v
```

---

## Getting Help

- **Questions:** [GitHub Discussions](https://github.com/flamehaven01/Flamehaven-Filesearch/discussions)
- **Bugs:** [GitHub Issues](https://github.com/flamehaven01/Flamehaven-Filesearch/issues)
- **Documentation:** [README.md](README.md)
- **API Docs:** http://localhost:8000/docs (when running)

---

## License

By contributing, you agree your work will be licensed under [MIT License](LICENSE).

---

**Thank you for contributing! 🙏**
