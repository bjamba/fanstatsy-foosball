# Licensing — Fanstatsy Foosball

## Project License

**MIT License** — chosen because this is a personal portfolio project and open-source learning tool. MIT is the most permissive common license: anyone can use, copy, modify, and distribute the code with minimal restrictions.

### What MIT Means in Practice

- Anyone can see, fork, and use your code (that's the point — portfolio visibility)
- Anyone can build on it, even commercially
- You retain copyright — your name stays on it
- The only requirement for others: include the MIT license text if they redistribute
- No warranty — you're not liable if someone uses it and something goes wrong

### License File

A `LICENSE` file with the MIT license text must exist at the project root before the first public release.

---

## Dependency Compatibility

MIT is compatible with almost every open-source license. But we should still verify each dependency, because:

- A **GPL-licensed** dependency would require the entire project to be GPL (more restrictive than MIT)
- A **proprietary/commercial** dependency might restrict redistribution
- Some packages have **non-commercial** clauses that could conflict with future DraftKings integration

### Dependency License Audit

Check before adding any new dependency. Run:

```bash
pip-licenses --format=table --with-system
```

Or check PyPI/GitHub for each package's license.

### Current Dependencies — License Status

| Package | License | Compatible with MIT? | Notes |
|---------|---------|---------------------|-------|
| `pandas` | BSD-3 | Yes | |
| `numpy` | BSD-3 | Yes | |
| `duckdb` | MIT | Yes | |
| `dbt-core` | Apache 2.0 | Yes | |
| `dbt-duckdb` | Apache 2.0 | Yes | |
| `nfl_data_py` | MIT | Yes | |
| `espn_api` | MIT | Yes | Unofficial ESPN API wrapper |
| `scikit-learn` | BSD-3 | Yes | |
| `torch` (PyTorch) | BSD-3 | Yes | |
| `xgboost` | Apache 2.0 | Yes | |
| `lightgbm` | MIT | Yes | |
| `plotly` | MIT | Yes | |
| `matplotlib` | PSF (BSD-compatible) | Yes | |
| `seaborn` | BSD-3 | Yes | |
| `jupyter` | BSD-3 | Yes | |
| `boto3` | Apache 2.0 | Yes | |
| `aws-cdk-lib` | Apache 2.0 | Yes | |
| `pydantic` | MIT | Yes | |
| `tenacity` | Apache 2.0 | Yes | |
| `pytest` | MIT | Yes | Dev dependency |
| `black` | MIT | Yes | Dev dependency |
| `ruff` | MIT | Yes | Dev dependency |
| `mypy` | MIT | Yes | Dev dependency |
| `streamlit` | Apache 2.0 | Yes | For draft dashboard |
| `flask` | BSD-3 | Yes | Alternative to Streamlit |

**Status: All current expected dependencies are MIT-compatible.**

### Red Flags to Watch For

When evaluating a new dependency, reject or flag if:

| License | Issue |
|---------|-------|
| GPL v2/v3 | Copyleft — would require the whole project to be GPL |
| AGPL | Even stricter than GPL — network use triggers copyleft |
| SSPL | Server Side Public License — restrictive for cloud deployment |
| CC-BY-NC | Non-commercial — would block DraftKings integration |
| Proprietary | May restrict redistribution or require payment |
| No license | Legally ambiguous — treat as "all rights reserved" |

**If a dependency has a problematic license:** look for an alternative package with a permissive license first. If no alternative exists, document the tradeoff in an ADR and discuss before adding.

---

## Data Licensing

### NFL Data

- **Play-by-play data** via `nfl_data_py`: sourced from publicly available NFL data. `nfl_data_py` is MIT-licensed. The underlying data is factual (not copyrightable) but sourced from NFL game data.
- **ESPN Fantasy API**: ESPN's Terms of Service govern usage. The `espn_api` package is an unofficial wrapper. Usage for personal, non-commercial purposes (your own league) is generally fine. If this project ever becomes commercial, re-evaluate ESPN data usage.
- **Web-scraped data** (injury reports, news): factual data is not copyrightable, but respect `robots.txt` and rate limits. Don't hammer servers.

### Your Analysis and Models

- **Your code** is MIT-licensed — anyone can use it
- **Your trained models** are your work product — the model weights are not committed to the repo (gitignored), so they remain private
- **Your blog posts and analysis** — consider a Creative Commons license (e.g., CC-BY-4.0) for written content if you want to share it openly while retaining attribution

---

## Third-Party API Terms

| Service | Terms to Respect | Link |
|---------|-----------------|------|
| ESPN | No official public API; unofficial usage for personal league data is common and tolerated | N/A (unofficial) |
| AWS | Standard AWS Customer Agreement; free tier limits apply | https://aws.amazon.com/free/ |
| DraftKings (V2+) | API terms if/when they provide public access; gambling regulations by jurisdiction | TBD |
| NFL data sources | Factual data, respect rate limits and robots.txt | Varies |

---

## Before First Public Release

- [ ] `LICENSE` file (MIT) exists at project root
- [ ] All dependencies audited for license compatibility (table above is current)
- [ ] `espn_api` usage reviewed — no terms of service violations
- [ ] Blog content license chosen (suggest CC-BY-4.0)
- [ ] No GPL or AGPL dependencies in the dependency tree (check transitive deps too)

### Checking Transitive Dependencies

A package you depend on may itself depend on a GPL-licensed package. Check the full dependency tree:

```bash
pip-licenses --format=table --with-system --order=license
```

This shows every installed package and its license, including transitive dependencies. Run this before each release.
