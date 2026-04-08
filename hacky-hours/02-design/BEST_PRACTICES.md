# Engineering Best Practices — Fanstatsy Foosball

## Overview

This document defines the engineering standards for the project. Since this is both a production tool and a learning portfolio, code quality matters doubly — it needs to work reliably AND demonstrate professional engineering practices to anyone reviewing the repo.

These aren't aspirational — they're the bar. Every PR, every module, every design doc follows these standards.

---

## Project Structure

```
fanstatsy-foosball/
├── hacky-hours/                  # Framework docs (design, roadmap, backlog)
├── docs/                         # Design artifacts for features and epics
│   ├── templates/                # Reusable templates (PRD, TDD, ERD, etc.)
│   ├── epics/                    # Design docs organized by epic
│   └── decisions/                # Architecture Decision Records
├── notebooks/                    # Jupyter notebooks — exploration and learning
│   ├── 01-foundations/           # Stats, EDA, basic concepts
│   ├── 02-feature-engineering/   # Feature development and analysis
│   ├── 03-modeling/              # Model experiments
│   └── 04-analysis/             # Weekly league analysis, blog drafts
├── src/
│   └── fanstatsy/               # Production Python package
│       ├── __init__.py
│       ├── ingestion/           # Data source connectors
│       ├── transforms/          # dbt-adjacent Python transforms
│       ├── features/            # Feature computation
│       ├── models/              # ML model training and inference
│       ├── applications/        # Draft sim, lineup advisor, blog gen
│       ├── notifications/       # Email and SMS via AWS
│       └── utils/               # Shared utilities (config, logging)
├── dbt/                         # dbt project
│   ├── models/
│   │   ├── staging/             # stg_* models
│   │   ├── intermediate/        # int_* models
│   │   ├── core/                # dim_* and fct_* models
│   │   └── features/            # feat_* models
│   ├── tests/                   # dbt data tests
│   └── dbt_project.yml
├── infra/                       # AWS CDK / CloudFormation
│   ├── stacks/
│   └── app.py
├── tests/                       # Python tests (mirrors src/ structure)
│   ├── unit/
│   │   ├── ingestion/
│   │   ├── transforms/
│   │   ├── features/
│   │   ├── models/
│   │   ├── applications/
│   │   └── notifications/
│   ├── integration/
│   └── model_validation/
├── data/                        # Local data (gitignored)
│   ├── raw/
│   ├── processed/
│   └── models/
├── configs/                     # Configuration files
│   ├── scoring.yaml             # League scoring settings
│   ├── league.yaml              # League connection info
│   └── notifications.yaml       # SMS/email settings
├── .github/
│   ├── workflows/               # CI/CD pipelines
│   │   ├── ci.yml               # Lint, type check, test, coverage gate
│   │   ├── deploy.yml           # Deploy to AWS on release
│   │   └── dbt.yml              # dbt test on data model changes
│   ├── ISSUE_TEMPLATE/          # Issue templates for bugs, features, epics
│   ├── PULL_REQUEST_TEMPLATE.md # PR template
│   └── CODEOWNERS               # Review assignments
├── .env                         # Secrets (gitignored)
├── .gitignore
├── pyproject.toml               # Package definition and dependencies
├── Makefile                     # Common commands
└── README.md
```

### Key Principles

- **`notebooks/` is for exploration, `src/` is for production.** Code starts in notebooks. Once a concept is proven and understood, it gets refactored into `src/` as a clean module.
- **`docs/` is for design artifacts.** PRDs, TDDs, ERDs live here, organized by epic. Templates ensure consistency.
- **`data/` is always gitignored.** Raw data is fetched by ingestion scripts, never committed.
- **`configs/` holds non-secret configuration.** Scoring rules, league settings, notification preferences. Committed to the repo.
- **`.env` holds secrets.** API keys, ESPN credentials, AWS credentials. Never committed.
- **`tests/` mirrors `src/`.** Every module in `src/fanstatsy/` has a corresponding test directory.

---

## Design Culture

### Principle

No significant work starts without a design artifact. Design docs are how we think through problems before writing code, and how we communicate what was decided and why.

### When to Write a Design Doc

| Work Size | Design Artifact | Example |
|-----------|----------------|---------|
| **Epic** | Full PRD + TDD + ERD (if data changes) | "Draft Simulation Engine" |
| **Feature** | TDD (may reference parent epic's PRD) | "Add rolling PPG feature computation" |
| **Task** | GitHub Issue with acceptance criteria | "Write unit tests for PPG calculator" |
| **Bug fix** | GitHub Issue with repro steps | "Fantasy points miscalculated for half-PPR" |

### Design Doc Templates

All templates live in `docs/templates/`. Every design doc starts from a template — never from a blank page.

#### PRD Template (Product Requirements Document)

```markdown
# PRD: [Epic Name]

## Status
Draft | In Review | Approved | Superseded

## The Ask
What is the stakeholder/user need this addresses? Why does this matter?
What does success look like?

## Background
Context needed to understand this epic. Link to relevant PRODUCT_OVERVIEW
sections, prior work, or external references.

## Requirements

### Must Have (MVP)
- [ ] Requirement 1
- [ ] Requirement 2

### Should Have (V1)
- [ ] Requirement 3

### Nice to Have (V2+)
- [ ] Requirement 4

## Non-Requirements
What is explicitly out of scope and why.

## Open Questions
Unresolved decisions that need input before or during implementation.

## References
- Links to related design docs, issues, notebooks, external resources
```

#### TDD Template (Technical Design Document)

```markdown
# TDD: [Feature/Epic Name]

## Status
Draft | In Review | Approved | Superseded

## The Task
What engineering work is being done? Link to parent PRD if applicable.

## Context
What exists today? What are the relevant design constraints?
Link to ARCHITECTURE.md, DATA_MODEL.md, or other design docs.

## Proposed Approach

### Architecture
How does this fit into the existing system? Include diagrams (Mermaid).

### Data Model Changes
New tables, columns, or transformations. Include ERD if applicable.

### API / Interface Changes
New functions, CLI commands, or endpoints. Include signatures.

### Dependencies
New packages or services required. License check against LICENSING.md.

## Alternatives Considered
What other approaches were evaluated? Why were they rejected?

## Testing Strategy
How will this be tested? What edge cases are covered?

## Rollout Plan
How will this be deployed? Any migration steps?

## The Deliverable
What specifically ships when this is done?
- [ ] Deliverable 1
- [ ] Deliverable 2

## References
- Links to PRD, issues, notebooks, external resources
```

#### ERD Template

```markdown
# ERD: [Data Change Name]

## Context
What data model change is being made and why?

## Current State
Mermaid ERD of affected tables before the change.

## Proposed State
Mermaid ERD of affected tables after the change.

## Migration
How existing data will be transformed. Any backfill needed?

## Impact
Which dbt models, feature tables, or ML pipelines are affected?
```

### Design Doc Workflow

1. **Create** the design doc from a template in `docs/epics/<epic-name>/`
2. **Draft** the content — fill in all sections, flag open questions
3. **Review** — create a PR for the design doc itself (Claude reviews your docs, you review Claude's)
4. **Approve** — merge the design doc PR, update status to "Approved"
5. **Implement** — create implementation issues that link back to the design doc
6. **Update** — if implementation reveals design changes, update the doc and note the change

### Future Integration

Design artifacts currently live in `docs/`. In the future, this may integrate with Notion, Linear, or a similar tool for richer collaboration and tracking. The file-based approach is the starting point.

---

## Ticket Grooming and Work Management

### Hierarchy

```
Epic
 └── Feature
      └── Task
           └── Sub-task (if needed)
```

### Epic

An epic is a large body of work that delivers a major capability. It has a PRD and usually a TDD.

**GitHub representation:** GitHub Milestone + a tracking Issue with checklist of features.

Example: "Draft Simulation Engine"

### Feature

A feature is a user-facing capability within an epic. It may have its own TDD if sufficiently complex.

**GitHub representation:** GitHub Issue with `feature` label, linked to the epic milestone.

Example: "Player ranking engine with confidence intervals"

### Task

A task is a discrete unit of implementation work within a feature. It should be completable in one PR.

**GitHub representation:** GitHub Issue with `task` label, linked to the feature issue.

Example: "Implement rolling PPG calculation with configurable window"

### Issue Quality Standards

Every GitHub Issue must include:

**For features:**
- Clear title describing the capability
- Link to parent epic and design doc
- Acceptance criteria as a checklist
- Labels: `feature`, priority level, epic label
- Assigned to milestone

**For tasks:**
- Clear title describing the work
- Link to parent feature issue
- Acceptance criteria as a checklist
- Estimated scope (S/M/L)
- Labels: `task`, priority level, epic label

**For bugs:**
- Clear title describing the symptom
- Steps to reproduce
- Expected vs. actual behavior
- Environment details
- Severity label

### GitHub Projects Board

Use GitHub Projects (free for public repos) with a Kanban board:

| Column | Purpose |
|--------|---------|
| **Backlog** | Groomed issues waiting to be picked up |
| **Ready** | Issues with all prerequisites met, ready to start |
| **In Progress** | Currently being worked on (limit: 2-3 items) |
| **In Review** | PR open, awaiting review |
| **Done** | Merged and verified |

Automation rules:
- Issue created → Backlog
- PR opened → In Review
- PR merged → Done
- Issue closed → Done

---

## Test-Driven Development (TDD)

### The Red-Green-Refactor Cycle

Every piece of production code in `src/` follows TDD:

1. **Red** — Write a failing test that defines the expected behavior
2. **Green** — Write the minimum code to make the test pass
3. **Refactor** — Clean up the code while keeping tests green

This is not optional. Tests come first.

### What TDD Looks Like in Practice

```python
# Step 1: RED — write the test first (it will fail)
# tests/unit/features/test_rolling_stats.py

def test_rolling_ppg_returns_average_of_last_n_games():
    """Rolling PPG for window=3 should average the last 3 games."""
    player_stats = pd.DataFrame({
        "player_id": ["p1"] * 5,
        "week": [1, 2, 3, 4, 5],
        "fantasy_points": [10.0, 20.0, 15.0, 25.0, 10.0],
    })
    result = compute_rolling_ppg(player_stats, window=3)
    # Week 3: avg(10, 20, 15) = 15.0
    # Week 4: avg(20, 15, 25) = 20.0
    # Week 5: avg(15, 25, 10) = 16.67
    assert result.iloc[2] == pytest.approx(15.0)
    assert result.iloc[3] == pytest.approx(20.0)
    assert result.iloc[4] == pytest.approx(16.67, abs=0.01)


def test_rolling_ppg_returns_nan_for_insufficient_data():
    """Weeks before the window is full should return NaN."""
    player_stats = pd.DataFrame({
        "player_id": ["p1"] * 3,
        "week": [1, 2, 3],
        "fantasy_points": [10.0, 20.0, 15.0],
    })
    result = compute_rolling_ppg(player_stats, window=3)
    assert pd.isna(result.iloc[0])
    assert pd.isna(result.iloc[1])
    assert result.iloc[2] == pytest.approx(15.0)


# Step 2: GREEN — write the minimum code to pass
# src/fanstatsy/features/rolling_stats.py

def compute_rolling_ppg(player_stats: pd.DataFrame, window: int = 3) -> pd.Series:
    """Compute rolling average fantasy points per game."""
    return player_stats["fantasy_points"].rolling(window=window).mean()


# Step 3: REFACTOR — clean up (add validation, docstring, etc.)
```

### Coverage Requirements

- **Target: 100% on `src/`** — every line of production code is covered by at least one test
- **CI gate: coverage must not decrease** — PRs that drop coverage are blocked
- **Tool: `pytest-cov`** with coverage report in CI output
- **Notebooks are excluded** from coverage requirements
- **`infra/` CDK code** has its own coverage target (may be lower initially as we learn)

### Coverage Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = "--cov=src/fanstatsy --cov-report=term-missing --cov-fail-under=100"

[tool.coverage.run]
source = ["src/fanstatsy"]
omit = ["src/fanstatsy/__main__.py"]

[tool.coverage.report]
fail_under = 100
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.",
]
```

### What Gets Tested

| Layer | Coverage | Notes |
|-------|----------|-------|
| `src/fanstatsy/` | 100% (CI enforced) | All production code |
| `dbt/` | dbt tests (not pytest coverage) | Data quality, not line coverage |
| `notebooks/` | Not covered | Exploration code, not production |
| `infra/` | Best effort | CDK stacks, snapshot tests |
| `tests/` | N/A | Tests don't test themselves |

---

## Pull Request Standards

### PR Review Model

| PR Author | Reviewer | Process |
|-----------|----------|---------|
| You | Claude | Claude reviews for design alignment, test coverage, code quality, security |
| Claude | You | You review for correctness, understanding, learning value |

Every PR gets reviewed. No exceptions. This is a portfolio project — every merged PR should demonstrate professional engineering.

### PR Template

```markdown
## The Ask
<!-- What stakeholder/user need does this address? Link to design doc or issue. -->

## The Task
<!-- What engineering work was done? What approach was taken? -->

## The Deliverable
<!-- What specifically ships in this PR? -->

### Changes
- Change 1
- Change 2

### Alternatives Considered
<!-- What other approaches were evaluated? Why this one? -->

## Test Plan
- [ ] Unit tests pass (`make test`)
- [ ] Coverage gate passes (100% on src/)
- [ ] dbt tests pass (if data model changes)
- [ ] Manually tested: [describe what you tested]

## Screenshots / Examples
<!-- If applicable — CLI output, notebook renders, visualizations -->

## References
- Design doc: [link]
- Issue: #XX
- Related PRs: #YY
```

### PR Quality Rules

1. **Title is descriptive** — not "fix stuff" or "updates". Use conventional commit format: `feat: add draft simulator ranking engine`
2. **Description tells a complete story** — someone reading the PR should understand the problem, approach, and solution without reading the code
3. **Every PR links to an Issue** — no orphan PRs
4. **Every PR links to a design doc** if the work is part of an epic or feature
5. **Test plan is filled in** — not just "tests pass" but what was specifically validated
6. **Small, focused PRs** — one feature or fix per PR. If a PR touches more than ~400 lines (excluding tests), consider splitting it
7. **Screenshots for visual changes** — CLI output, notebook renders, charts

---

## CI/CD Pipeline

### CI — Runs on Every PR

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: pip install -e ".[dev]"
      - name: Lint (ruff)
        run: ruff check src/ tests/
      - name: Format check (black)
        run: black --check src/ tests/
      - name: Type check (mypy)
        run: mypy src/
      - name: Tests with coverage
        run: pytest --cov=src/fanstatsy --cov-report=term-missing --cov-fail-under=100
      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: htmlcov/
```

### CI Gates (all must pass to merge)

| Gate | Tool | Threshold |
|------|------|-----------|
| Lint | ruff | Zero warnings |
| Format | black | All files formatted |
| Type check | mypy (strict) | Zero errors |
| Tests | pytest | All pass |
| Coverage | pytest-cov | 100% on `src/` — no decrease allowed |
| dbt tests | dbt test | All pass (when data models change) |

### CD — Runs on Release

```yaml
# .github/workflows/deploy.yml (to be built with CDK learning)
name: Deploy

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy Lambda functions
        run: make deploy
      # ... CDK deploy steps
```

### GitHub Releases

- Every milestone completion → tagged release → GitHub Release with changelog
- Managed via `/hacky-hours sync` which reads CHANGELOG.md and publishes
- Release notes should be detailed and human-readable

---

## Python Standards

### Version and Environment

- **Python 3.11+** — use modern features (match statements, type hints, tomllib)
- **Virtual environment** — use `venv` or `conda`. Document setup in README.
- **`pyproject.toml`** — single source of truth for package metadata, dependencies, and tool configs

### Code Style

- **Formatter:** `black` — no debates about style, just run it
- **Linter:** `ruff` — fast, catches common issues, replaces flake8/isort/pyflakes
- **Type checker:** `mypy` in strict mode (see Type System section below)
- **Docstrings:** Google style. Required on all public functions and classes in `src/`.

```python
def compute_rolling_ppg(
    player_stats: pd.DataFrame,
    window: int = 3,
) -> pd.Series:
    """Compute rolling average fantasy points per game.

    Args:
        player_stats: DataFrame with columns [player_id, week, fantasy_points],
            sorted by week ascending.
        window: Number of games to average over.

    Returns:
        Series of rolling PPG values aligned to input index.
    """
```

### Type System

**Strict typing is enforced.** Every function in `src/` must have full type annotations on all parameters and return values.

```toml
# pyproject.toml
[tool.mypy]
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_any_generics = true
disallow_untyped_defs = true
check_untyped_defs = true
```

**Rules for `Any`:**
- `Any` is allowed only when interfacing with third-party libraries that don't provide type stubs (e.g., some ESPN API responses)
- Every use of `Any` must include a comment explaining why: `# type: ignore[...] — espn_api returns untyped dict`
- If you find yourself reaching for `Any` more than once for the same library, write a typed wrapper
- Never use `Any` for laziness — if you know the type, annotate it

**Common patterns:**

```python
from typing import TypeAlias

# Define type aliases for complex types used repeatedly
PlayerStats: TypeAlias = pd.DataFrame  # columns: player_id, week, fantasy_points
FeatureVector: TypeAlias = dict[str, float]
ModelPrediction: TypeAlias = dict[str, float]  # {player_id: projected_points}

# Use Protocol for duck typing where needed
from typing import Protocol

class DataSource(Protocol):
    def fetch(self, season: int, week: int) -> pd.DataFrame: ...
    def validate(self, df: pd.DataFrame) -> None: ...
```

### Naming Conventions

| Thing | Convention | Example |
|-------|-----------|---------|
| Files and modules | snake_case | `player_features.py` |
| Functions | snake_case | `compute_rolling_ppg()` |
| Classes | PascalCase | `DraftSimulator` |
| Constants | UPPER_SNAKE | `DEFAULT_WINDOW_SIZE` |
| DataFrames | descriptive noun | `player_stats`, `weekly_features` |
| Models | descriptive with version | `player_projection_v1` |
| Type aliases | PascalCase | `PlayerStats`, `FeatureVector` |

### Import Order

Enforced by `ruff`:

1. Standard library
2. Third-party packages
3. Local imports

```python
import os
from pathlib import Path

import pandas as pd
import torch
from espn_api.football import League

from fanstatsy.features import compute_rolling_ppg
from fanstatsy.utils.config import load_scoring_config
```

### Docstring Requirements

**Required on:**
- All public functions and methods in `src/`
- All classes in `src/`
- All modules (module-level docstring)

**Must include:**
- One-line summary
- Args section with type and description for each parameter
- Returns section with type and description
- Raises section if the function raises exceptions

**Not required on:**
- Private functions (prefixed with `_`) — still encouraged
- Test functions — test name should be descriptive enough
- Notebook code

### Error Handling

- **Fail loudly for data quality issues.** If the raw data doesn't match expected schema, stop the pipeline — don't silently produce garbage features.
- **Retry transient failures.** Network requests to ESPN or web scraping can fail intermittently. Retry with backoff.
- **Never catch and silence exceptions** in production code. Log the error and re-raise, or handle it explicitly.
- **Custom exception classes** for domain-specific errors:

```python
# src/fanstatsy/exceptions.py

class FanstatsyError(Exception):
    """Base exception for all Fanstatsy errors."""

class DataQualityError(FanstatsyError):
    """Raised when data fails validation checks."""

class IngestionError(FanstatsyError):
    """Raised when a data source fails to respond or returns unexpected data."""

class ModelError(FanstatsyError):
    """Raised when model training or inference fails."""
```

### Validation

- **Validate at boundaries** — where data enters the system (ingestion) and where it exits (notifications, API responses)
- **Use Pydantic for structured data validation** where appropriate (config files, API responses)
- **dbt tests validate transformations** — don't duplicate in Python what dbt already checks
- **Assert preconditions** in functions that depend on specific data shapes:

```python
def compute_features(player_stats: pd.DataFrame) -> pd.DataFrame:
    """Compute player features from game stats.

    Args:
        player_stats: Must contain columns [player_id, week, fantasy_points].

    Raises:
        DataQualityError: If required columns are missing or data is empty.
    """
    required = {"player_id", "week", "fantasy_points"}
    missing = required - set(player_stats.columns)
    if missing:
        raise DataQualityError(f"Missing required columns: {missing}")
    if player_stats.empty:
        raise DataQualityError("Cannot compute features on empty DataFrame")
```

---

## Notebook Conventions

Notebooks serve two purposes: **learning** and **portfolio display**. Both require more structure than "just run cells." Notebooks are **not** subject to test coverage or type checking requirements.

### Structure

Every notebook should follow this pattern:

```markdown
# Title — What This Notebook Explores

## Context
What question are we answering? What concept are we learning?

## Setup
Imports, data loading, configuration.

## Exploration / Analysis
The actual work — with Markdown cells explaining each step.

## Findings
What did we learn? What decisions does this inform?

## Next Steps
What to explore next, or what to productionize from this.
```

### Rules

1. **Restart and run all** before committing — notebooks must execute top to bottom without errors
2. **No secrets in notebooks** — load from `.env` using `python-dotenv`
3. **Markdown cells explain the "why"** — not just what the code does, but why you're doing it and what the results mean
4. **Clear outputs before committing** when outputs contain league member data or are excessively large
5. **Name notebooks with a number prefix** for ordering: `01_eda_player_stats.ipynb`

### Notebook → Production Pipeline

When a notebook concept is proven:

1. Write tests first (TDD) for the behavior you want in production
2. Extract the core logic into a function in `src/fanstatsy/`
3. Make the tests pass
4. The notebook becomes documentation — it shows the thinking that led to the production code
5. Link from the notebook to the production module: "This analysis led to `src/fanstatsy/features/rolling_stats.py`"

---

## Git Workflow

### Branching

- **`main`** — always working, always deployable. Protected branch — no direct pushes.
- **`feat/<name>`** — new features (e.g., `feat/draft-simulator`)
- **`fix/<name>`** — bug fixes
- **`learn/<name>`** — learning notebooks and experiments (e.g., `learn/linear-regression`)
- **`infra/<name>`** — infrastructure changes (CDK, CI/CD)
- **`docs/<name>`** — design docs and documentation

### Commit Messages

Use conventional commits — these play nicely with changelogs and are widely recognized:

```
feat: add rolling PPG feature computation
fix: correct fantasy points calculation for half-PPR
docs: add EDA notebook for QB stats
learn: explore linear regression for player projection
infra: add RDS Postgres stack via CDK
data: update ingestion script for 2026 season data
test: add unit tests for feature engineering
refactor: extract data validation into shared module
```

### PR Workflow

1. Create a branch from `main`
2. Write design doc (if epic/feature-level work)
3. Write tests first (TDD)
4. Implement to make tests pass
5. Run `make test-all` locally
6. Push and open a PR using the PR template
7. Review (Claude reviews yours, you review Claude's)
8. All CI gates must pass
9. Merge to `main`
10. Close linked issues

---

## Configuration Management

### Three Levels of Config

| Level | Where | Committed? | Example |
|-------|-------|-----------|---------|
| **Secrets** | `.env` | No | ESPN credentials, AWS keys |
| **Environment-specific** | `configs/*.yaml` | Yes | Scoring rules, league ID, notification settings |
| **Code defaults** | `src/fanstatsy/utils/config.py` | Yes | Default window sizes, model hyperparameters |

### Loading Config

```python
# Always load secrets from environment, never hardcode
import os
from dotenv import load_dotenv

load_dotenv()

ESPN_LEAGUE_ID = os.environ["ESPN_LEAGUE_ID"]
ESPN_S2 = os.environ["ESPN_S2"]  # ESPN auth cookie
ESPN_SWID = os.environ["ESPN_SWID"]  # ESPN auth cookie
```

### .gitignore Must Include

```
# Secrets
.env
.env.*

# Local data
data/

# Model artifacts (large files)
*.pkl
*.pt
*.joblib

# Python
__pycache__/
*.pyc
.venv/
venv/

# Jupyter
.ipynb_checkpoints/

# OS
.DS_Store

# IDE
.vscode/
.idea/
```

---

## ML Experiment Tracking

### Why Track Experiments

When you're trying different model architectures, hyperparameters, and feature sets, you need to know what you tried, what worked, and why. Without tracking, you'll lose track of which combination produced your best model.

### Approach

Start simple, add tooling as complexity grows:

| Phase | Method | When to move on |
|-------|--------|-----------------|
| **Phase 1** | Notebook markdown cells documenting each experiment | When you have more than ~10 experiments |
| **Phase 2** | MLflow (local) — logs params, metrics, artifacts | When you need to compare runs systematically |
| **Phase 3** | MLflow on AWS or Weights & Biases free tier | When you want cloud tracking and team-ready tooling |

### What to Track for Every Experiment

- **Data:** what data was used (date range, feature set version)
- **Model:** algorithm, architecture, hyperparameters
- **Metrics:** accuracy metric(s) appropriate to the task
- **Artifacts:** trained model file, feature importance plots
- **Outcome:** what you learned, whether to pursue further

---

## Dependency Management

### Principles

- **Pin versions** in `pyproject.toml` for reproducibility
- **Minimize dependencies** — every package is a maintenance burden
- **Check license compatibility** before adding (see LICENSING.md) — this is an MIT-licensed project
- **Separate dev dependencies** from production: `[project.optional-dependencies] dev = [...]`

### Core Dependencies (expected)

| Package | Purpose |
|---------|---------|
| `pandas` | Data manipulation |
| `numpy` | Numerical computing |
| `duckdb` | Local analytics database |
| `dbt-duckdb` | Data transformations |
| `nfl_data_py` | NFL historical data |
| `espn_api` | ESPN Fantasy league data |
| `scikit-learn` | Classical ML models |
| `torch` | Deep learning (PyTorch) |
| `xgboost` or `lightgbm` | Gradient boosting |
| `plotly` | Interactive visualizations |
| `matplotlib` / `seaborn` | Static visualizations |
| `jupyter` | Notebooks |
| `boto3` | AWS SDK |
| `aws-cdk-lib` | Infrastructure as code |
| `pydantic` | Data validation |
| `tenacity` | Retry logic |

### Dev Dependencies

| Package | Purpose |
|---------|---------|
| `pytest` | Testing |
| `pytest-cov` | Coverage reporting |
| `black` | Code formatting |
| `ruff` | Linting |
| `mypy` | Type checking (strict) |
| `python-dotenv` | Load .env files |
| `pre-commit` | Git hook management |

---

## Makefile

A `Makefile` provides common commands so you don't have to remember exact invocations:

```makefile
.PHONY: setup test lint format ingest dbt-run dbt-test train serve

setup:
	python -m venv .venv
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
```

---

## Pre-commit Hooks

Use `pre-commit` to catch issues before they're committed:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.4.0
    hooks:
      - id: black
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-added-large-files
        args: [--maxkb=500]
      - id: detect-private-key
      - id: check-merge-conflict
      - id: end-of-file-fixer
      - id: trailing-whitespace
```

This automatically:
- Formats code with black
- Lints with ruff
- Blocks large files from being committed (catches model artifacts)
- Detects private keys accidentally staged
- Cleans up whitespace

---

## Logging

### Principles

- Use Python's `logging` module, not `print()`
- Log at appropriate levels: `DEBUG` for development, `INFO` for pipeline progress, `WARNING` for recoverable issues, `ERROR` for failures
- Include context in log messages: what was being processed, key identifiers

```python
import logging

logger = logging.getLogger(__name__)

def ingest_player_stats(season: int) -> pd.DataFrame:
    logger.info("Ingesting player stats for season %d", season)
    # ... work ...
    logger.info("Ingested %d player stat records", len(df))
    return df
```

### Pipeline Logging

Data pipelines should log:
- Start and end of each stage
- Record counts at each stage (helps catch data quality issues)
- Any data quality warnings (unexpected nulls, schema changes)
- Total runtime
