# Contributing to SovDef FileSearch Lite

Thank you for considering contributing to SovDef FileSearch Lite!

## Getting Started

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/SovDef-FileSearch-Lite.git
   cd SovDef-FileSearch-Lite
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev,api]"
   ```

4. Set up environment:
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

## Development Workflow

### Code Style

We use:
- **black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run formatters:
```bash
black sovdef_filesearch_lite/ tests/ examples/
isort sovdef_filesearch_lite/ tests/ examples/
```

Run linters:
```bash
flake8 sovdef_filesearch_lite/ tests/ examples/
mypy sovdef_filesearch_lite/
```

### Testing

Run tests:
```bash
# All tests
pytest

# Unit tests only (no integration)
pytest -m "not integration"

# With coverage
pytest --cov=sovdef_filesearch_lite --cov-report=html

# Specific test file
pytest tests/test_core.py -v
```

### Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Add tests for new functionality

4. Run tests and linters:
   ```bash
   pytest
   black --check .
   flake8 .
   ```

5. Commit your changes:
   ```bash
   git add .
   git commit -m "Add: your feature description"
   ```

6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

7. Open a Pull Request

## Commit Message Format

Use conventional commits format:

- `Add: new feature`
- `Fix: bug fix`
- `Update: improvement to existing feature`
- `Refactor: code refactoring`
- `Docs: documentation changes`
- `Test: test additions or changes`
- `CI: CI/CD changes`

## Pull Request Process

1. Update README.md if needed
2. Update tests
3. Ensure CI passes
4. Request review from maintainers
5. Address feedback

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the project

## Questions?

Open an issue or discussion on GitHub!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
