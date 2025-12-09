.PHONY: help install dev lint format typecheck test run clean

{%- if values.packageManager == "uv" %}
PYTHON := uv run python
PYTEST := uv run pytest
RUFF := uv run ruff
MYPY := uv run mypy
PIP := uv pip
{%- elif values.packageManager == "poetry" %}
PYTHON := poetry run python
PYTEST := poetry run pytest
RUFF := poetry run ruff
MYPY := poetry run mypy
PIP := poetry
{%- else %}
PYTHON := python
PYTEST := pytest
RUFF := ruff
MYPY := mypy
PIP := pip
{%- endif %}

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
{%- if values.packageManager == "poetry" %}
	poetry install
{%- else %}
	$(PIP) install -e .
{%- endif %}

dev: ## Install dev dependencies
{%- if values.packageManager == "poetry" %}
	poetry install --with dev
{%- else %}
	$(PIP) install -e ".[dev]"
{%- endif %}

lint: ## Run linting
	$(RUFF) check src tests

format: ## Format code
	$(RUFF) format src tests
	$(RUFF) check --fix src tests

typecheck: ## Run type checking
	$(MYPY) src

test: ## Run tests
	$(PYTEST) tests -v

test-security: ## Run security tests only
	$(PYTEST) tests/test_security.py -v

run: ## Run the agent (use PROJECT_DIR=./my_project)
	$(PYTHON) -m src.main --project-dir $(or $(PROJECT_DIR),./output)

run-limited: ## Run with limited iterations (use PROJECT_DIR and MAX_ITER)
	$(PYTHON) -m src.main --project-dir $(or $(PROJECT_DIR),./output) --max-iterations $(or $(MAX_ITER),5)

clean: ## Clean build artifacts
	rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache
	rm -rf *.egg-info build dist
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

check: lint typecheck test ## Run all checks
