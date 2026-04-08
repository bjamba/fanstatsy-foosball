.PHONY: setup test lint format check dbt-run dbt-test test-all validate-models ingest train serve

setup:
	python3 -m venv .venv
	.venv/bin/pip install -e ".[dev]"
	.venv/bin/pre-commit install

test:
	.venv/bin/pytest tests/unit tests/integration -v --cov=src/fanstatsy --cov-report=term-missing --cov-fail-under=100

validate-models:
	.venv/bin/pytest tests/model_validation -v

dbt-run:
	cd dbt && dbt run

dbt-test:
	cd dbt && dbt test

test-all: test dbt-test validate-models

lint:
	.venv/bin/ruff check src/ tests/
	.venv/bin/mypy src/

format:
	.venv/bin/black src/ tests/
	.venv/bin/ruff check --fix src/ tests/

check: format lint test

ingest:
	.venv/bin/python -m fanstatsy.ingestion.run_all

train:
	.venv/bin/python -m fanstatsy.models.train

serve:
	.venv/bin/python -m fanstatsy.applications.serve
