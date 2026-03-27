.PHONY: help install shell test test-unit test-integration test-performance test-security test-all coverage lint format type-check clean

help:
	@echo "Test Automation Framework - Using Poetry"
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "  make install          - Install dependencies and setup virtual environment"
	@echo "  make shell            - Activate virtual environment"
	@echo "  make test             - Run all tests (parallel)"
	@echo "  make test-unit        - Run unit tests"
	@echo "  make test-integration - Run integration tests"
	@echo "  make test-performance - Run performance tests"
	@echo "  make test-security    - Run security tests"
	@echo "  make test-all         - Run all test types with full output"
	@echo "  make coverage         - Generate coverage report"
	@echo "  make lint             - Run code linters (flake8)"
	@echo "  make format           - Format code (black, isort)"
	@echo "  make type-check       - Run type checker (mypy)"
	@echo "  make clean            - Remove build artifacts and cache files"
	@echo ""

install:
	@echo "Installing dependencies..."
	poetry install
	@echo "✓ Installation complete"
	@echo ""
	@echo "Next: run 'make shell' to activate virtual environment"

shell:
	poetry shell

test:
	poetry run pytest -v --tb=short -n auto

test-unit:
	poetry run pytest tests/test_unit.py -v --tb=short

test-integration:
	poetry run pytest tests/test_integration.py -v --tb=short

test-performance:
	poetry run pytest tests/test_performance.py -v --tb=short

test-security:
	poetry run pytest tests/test_security.py -v --tb=short

test-all:
	poetry run pytest tests/ -v --tb=long

coverage:
	poetry run pytest --cov=. --cov-report=html --cov-report=term
	@echo "✓ Coverage report generated in htmlcov/index.html"

lint:
	@echo "Running flake8..."
	poetry run flake8 core adapters utils tests

format:
	@echo "Running black..."
	poetry run black .
	@echo "Running isort..."
	poetry run isort .
	@echo "✓ Code formatted"

type-check:
	poetry run mypy core adapters utils

clean:
	@echo "Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name *.egg-info -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ htmlcov/
	@echo "✓ Cleanup complete"
