# Fanstatsy Foosball

A data-driven fantasy football ML system — and a data science learning path disguised as a competitive edge.

## What Is This?

Fanstatsy Foosball (fan + stats + fantasy) is a Python-based machine learning project that uses NFL and ESPN Fantasy data to:

- **Simulate drafts** and rank players by statistical value (VORP)
- **Optimize weekly lineups** using ML-powered player projections
- **Send recommendations** via SMS and email with statistical reasoning
- **Generate blog posts** with data-driven league analysis and beautiful charts

It's also a structured curriculum for learning data science and ML engineering from the ground up, using fantasy football as the applied domain.

## Who Is This For?

This project was built by a senior data engineer / software engineer leveling up into AI/ML. Every milestone teaches a concept — from exploratory data analysis and linear regression through gradient boosting, neural networks, and cloud deployment.

If you're an engineer who's built data pipelines but never built the models, this might be interesting to you too.

## Project Status

**Currently:** Planning complete. Build starting.

See the [Roadmap](hacky-hours/03-roadmap/ROADMAP.md) for the full 21-milestone curriculum.

## Tech Stack

| Layer | Tools |
|-------|-------|
| **Language** | Python 3.11+ |
| **Data** | nfl_data_py, espn_api, DuckDB, dbt |
| **ML** | scikit-learn, XGBoost, PyTorch |
| **Visualization** | Plotly, matplotlib, seaborn |
| **Cloud** | AWS (Lambda, RDS, SES, SNS, SageMaker, CDK) |
| **CI/CD** | GitHub Actions, pytest, ruff, black, mypy |

## Project Structure

```
fanstatsy-foosball/
├── hacky-hours/          # Planning docs (ideation, design, roadmap, backlog)
├── docs/                 # Design artifacts (PRDs, TDDs, ERDs)
├── notebooks/            # Jupyter notebooks (learning + exploration)
├── src/fanstatsy/        # Production Python package
├── dbt/                  # dbt transformation project
├── infra/                # AWS CDK infrastructure
├── tests/                # Test suite (100% coverage target)
├── configs/              # Non-secret configuration
└── data/                 # Local data lake (gitignored)
```

## Getting Started

> Setup instructions will be added once the project scaffold is built (Milestone 1).

## Design Documents

The full design lives in [`hacky-hours/02-design/`](hacky-hours/02-design/):

- [Architecture](hacky-hours/02-design/ARCHITECTURE.md) — system overview, data flow, infrastructure
- [Data Model](hacky-hours/02-design/DATA_MODEL.md) — ERD, table schemas, feature tables
- [Business Logic](hacky-hours/02-design/BUSINESS_LOGIC.md) — scoring, draft sim, lineup optimizer, notifications
- [Best Practices](hacky-hours/02-design/BEST_PRACTICES.md) — TDD, CI/CD, PR standards, typing, design culture
- [Security & Privacy](hacky-hours/02-design/SECURITY_PRIVACY.md) — credentials, anonymization, threat model
- [Licensing](hacky-hours/02-design/LICENSING.md) — MIT license, dependency audit

## License

MIT — see [LICENSE](LICENSE) for details.
