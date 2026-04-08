# Changelog — Fanstatsy Foosball

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-04-07

### M1: Project Foundation

- Python project scaffold: pyproject.toml, src/fanstatsy/ package, Makefile, .env.example
- CI pipeline: GitHub Actions with black, ruff, mypy, pytest + 100% coverage gate
- Pre-commit hooks: black, ruff, private key detection, large file check
- GitHub setup: issue templates (bug, feature, epic), PR template, branch protection, Projects board
- Design doc templates: PRD, TDD, ERD in docs/templates/
- Fantasy points scoring engine with TDD (first production function + 4 test cases)
- Custom exception hierarchy: FanstatsyError, DataQualityError, IngestionError, ModelError
