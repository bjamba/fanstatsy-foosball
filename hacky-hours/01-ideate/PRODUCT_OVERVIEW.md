# Product Overview — Fanstatsy Foosball

## Who

The primary user is the author — a senior DE/SWE leveling up into AI/ML engineering through hands-on project work. This project serves double duty as a competitive fantasy football tool and a data science learning path / portfolio piece.

Secondary audience: recruiters and hiring managers evaluating the portfolio, and eventually content consumers (blog readers, other fantasy players interested in a data-driven approach).

## What

A Python ML project that progresses from exploration → model building → production deployment. The learning and building are the same activity — concepts get explored in Jupyter notebooks, then productionized into deployed tools.

**Forms it takes:**
- **Jupyter notebooks** — exploration, learning, portfolio display (show thinking alongside code)
- **Python packages** — production pipelines for data ingestion, feature engineering, model training
- **Deployed services** — models served on AWS/GCP for real-time use during the season
- **CLI tools** — automation for draft simulations and lineup optimization
- **Blog content** — weekly data-driven analysis of league performance, generated from stats

**Core capabilities:**
1. Historical and real-time NFL/fantasy player data ingestion
2. Statistical analysis and feature engineering
3. ML models for player projection and valuation (PyTorch)
4. Draft simulation engine
5. Lineup optimization and automation (ESPN integration)
6. Blog/report generation from weekly stats
7. Extensible to other fantasy leagues (NBA, etc.)

## Where

- **Local development** — notebooks and pipeline development
- **AWS/GCP** — model training, serving, and scheduled pipelines (free tier + small spend with existing AWS credits)
- **ESPN** — fantasy league platform (data source and lineup management)
- **GitHub** — public repo as portfolio, potential content platform (GitHub Pages or similar for blog)

## When

- **Now through summer 2026** — learning foundations, building data pipelines, training initial models
- **Late summer 2026** — draft simulation tools ready for NFL draft prep
- **Fall 2026 – early 2027** — season tools live: lineup optimization, weekly blog posts, model refinement
- **Post-season** — extend to NBA or other leagues; refine portfolio presentation
- Learning and building happen on the same timeline — not sequential

## Why

The author has spent their career building the data infrastructure that feeds ML models but has never built the models themselves. This project bridges that gap using a domain (fantasy football) that provides real stakes, clear feedback loops, and enough complexity to learn the full ML lifecycle.

**Problems it solves:**
1. No consistent, data-driven approach to fantasy draft picks and lineup decisions
2. Can't compete on organic football knowledge — but can compete on data and automation
3. No portfolio evidence of ML capability despite adjacent experience
4. Gap between DE/SWE skills and the AI/ML engineer identity needed for career growth

**Why it matters:** The NFL season is a fixed deadline with a clear win condition — forcing real delivery, not endless tinkering.

## Constraints & Values

### Licensing
- **Open source** (MIT or similar) — this is a portfolio and potential content project
- Public visibility is a feature, not a risk

### Privacy
- League data can be in the repo, but **anonymize real names** of league members
- Player stats are public data — no concerns there
- No credentials or API keys in the repo (use environment variables / config files)

### Infrastructure
- AWS and GCP free tiers as primary, with small paid spend OK (existing AWS credits available)
- Cloud work is itself a learning opportunity — every deployment should teach infrastructure concepts
- Prefer managed services where they exist on free tier (SageMaker free tier, Vertex AI notebooks, etc.)
- Local development as the primary workspace; cloud for training at scale and serving

### Values
- **Learning over speed** — take the time to understand what's being built, don't just ship black boxes
- **Ship over perfection** — but every shipped thing should be understood
- **Data over intuition** — the whole point is removing emotion from decisions
- **Accessible knowledge** — blog posts and notebooks should be understandable to others on the same journey
