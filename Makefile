.PHONY: help install install-dev test lint format clean build publish docker-build docker-run

help:
	@echo "FLAMEHAVEN FileSearch - Makefile Commands"
	@echo "=========================================="
	@echo "install          - Install package"
	@echo "install-dev      - Install with development dependencies"
	@echo "install-api      - Install with API server dependencies"
	@echo "install-all      - Install all dependencies"
	@echo "test             - Run tests"
	@echo "test-cov         - Run tests with coverage"
	@echo "test-integration - Run integration tests"
	@echo "lint             - Run linters"
	@echo "format           - Format code"
	@echo "clean            - Clean build artifacts"
	@echo "build            - Build package"
	@echo "publish-test     - Publish to TestPyPI"
	@echo "publish          - Publish to PyPI"
	@echo "docker-build     - Build Docker image"
	@echo "docker-run       - Run Docker container"
	@echo "server           - Start API server"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

install-api:
	pip install -e ".[api]"

install-all:
	pip install -e ".[all]"

test:
	pytest -v

test-cov:
	pytest --cov=flamehaven_filesearch --cov-report=html --cov-report=term

test-integration:
	pytest -v -m integration

lint:
	flake8 flamehaven_filesearch/ tests/ examples/
	black --check flamehaven_filesearch/ tests/ examples/
	isort --check-only flamehaven_filesearch/ tests/ examples/

format:
	black flamehaven_filesearch/ tests/ examples/
	isort flamehaven_filesearch/ tests/ examples/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish-test: build
	python -m twine upload --repository testpypi dist/*

publish: build
	python -m twine upload dist/*

docker-build:
	docker build -t flamehaven-filesearch:latest .

docker-run:
	docker run -d -p 8000:8000 \
		-e GEMINI_API_KEY=$(GEMINI_API_KEY) \
		--name flamehaven-api \
		flamehaven-filesearch:latest

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

server:
	uvicorn flamehaven_filesearch.api:app --reload --host 0.0.0.0 --port 8000

server-prod:
	uvicorn flamehaven_filesearch.api:app --host 0.0.0.0 --port 8000 --workers 4
