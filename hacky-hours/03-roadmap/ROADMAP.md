# Roadmap — Fanstatsy Foosball

## How This Roadmap Works

This roadmap is a **curriculum disguised as a product roadmap**. Each milestone teaches data science and ML concepts through the applied domain of fantasy football.

### Two Tracks

Every milestone has work on two parallel tracks:

- **Track A (Claude builds)** — Infrastructure, scaffolding, boilerplate. Stuff the user already knows (DE/SWE) or that isn't where the learning value is. Claude builds efficiently so the user can focus on what matters. Claude explains what was built and why.
- **Track B (You learn)** — Data science, statistics, ML concepts, and applied fantasy football work. Every task teaches something. Claude guides early on, then progressively hands the wheel to the user.

Track A shrinks as the project progresses. By the mid-point, the user is doing most of the work with Claude reviewing and validating.

### Session Size

Each milestone targets **5-7 one-hour evening sessions**. The user has a full-time job — every session should feel like meaningful progress.

### Timeline

| Period | Milestones | What's Live |
|--------|-----------|-------------|
| **Apr–Jun 2026** | M1–M6 | Foundation + first ML model |
| **Jul–Aug 2026** | M7–M9 | Draft tools ready |
| **Late Aug 2026** | **DRAFT DAY** | Dashboard on second screen |
| **Sep 2026** | M10–M12 | Weekly pipeline + notifications live |
| **Oct 2026–Jan 2027** | M13–M15 | Blog, waiver wire, model monitoring |
| **Post-season 2027** | M16+ | Advanced ML, DraftKings, NBA |

---

## MVP — "Data-Driven Draft Day"

**Core question:** Can you walk into draft day with a statistical edge over your family?

**Outcome:** Model-powered player rankings, a simulation-tested strategy, and a real-time dashboard on your second screen during the live draft.

---

### M1: Project Foundation (~5 sessions)

**What you learn:** TDD workflow, CI/CD pipeline anatomy, how professional Python projects are structured.

**What ships:** A fully configured repo with CI, tests, linting, and GitHub Projects board.

| Task | Track | Description |
|------|-------|-------------|
| Python project scaffold | A | pyproject.toml, src/fanstatsy/ package, Makefile, .gitignore, .env.example |
| CI pipeline | A | GitHub Actions: ruff, black, mypy, pytest with 100% coverage gate |
| Pre-commit hooks | A | black, ruff, detect-private-key, check-added-large-files |
| GitHub setup | A | Issue templates (bug, feature, epic), PR template (Ask/Task/Deliverable), branch protection on main, Projects board |
| Design doc templates | A | PRD, TDD, ERD templates in docs/templates/ |
| LICENSE file | A | MIT license at project root |
| First TDD cycle | B | Write a failing test, make it pass, refactor — learn the red-green-refactor rhythm with a simple utility function |
| Understand the scaffold | B | Review what Claude built, ask questions, understand why each piece exists |

---

### M2: Data Ingestion (~6 sessions)

**What you learn:** Working with sports data APIs, Parquet file format, data validation, schema-first thinking.

**What ships:** Ingestion pipelines for NFL historical data and ESPN league data, writing to a local data lake.

| Task | Track | Description |
|------|-------|-------------|
| Ingestion module scaffold | A | Base classes, consistent interface, config loading, error handling with tenacity retry |
| nfl_data_py connector | A/B | Fetch historical player stats, rosters, draft picks. **You explore the data in a notebook first**, then Claude helps productionize |
| espn_api connector | A/B | Connect to your ESPN league, fetch rosters, matchups, scores. **You set up your ESPN credentials and explore what data is available** |
| Parquet I/O layer | A | Write and read Parquet files with schema validation |
| Data validation | B | Learn about data quality — what can go wrong? Write validation checks for ingested data |
| Notebook: explore the raw data | B | Your first real DS notebook — load the data, look at shapes, spot issues, understand what you're working with |
| Config management | A | configs/league.yaml, configs/scoring.yaml, .env for secrets |

**Concept spotlight:** *What is Parquet and why do data engineers use it instead of CSV?* (Columnar storage, compression, schema enforcement — concepts you'll use throughout your career.)

---

### M3: Storage & Transforms (~6 sessions)

**What you learn:** DuckDB for analytics, dbt for data transformation, dimensional modeling, data testing.

**What ships:** A dbt project with staging and core models. Clean, tested, query-ready data.

| Task | Track | Description |
|------|-------|-------------|
| DuckDB setup | A | Database initialization, connection management, integration with Parquet data lake |
| dbt project scaffold | A | dbt_project.yml, profiles.yml, dbt-duckdb adapter config |
| stg_* staging models | B | **You write the SQL** — clean and rename raw source columns. Claude reviews. |
| dim_* dimension models | B | **You design** dim_players, dim_teams, dim_positions. Learn slowly changing dimensions. |
| fct_player_games | B | **You build** the central fact table joining players, games, and stats. Calculate fantasy points using league scoring config. |
| fct_fantasy_matchups | B | Your league's matchup history — join ESPN data into a clean fact table |
| Anonymization | A | Automated owner name replacement at ingestion time |
| dbt tests | B | **You write** uniqueness, not-null, accepted_values tests. Learn why data testing matters. |
| Scoring engine | B | **You implement** the fantasy points calculation. Configurable from ESPN settings. TDD — tests first. |

**Concept spotlight:** *Why dimensional modeling?* Stars and snowflakes — how fact tables and dimension tables work together to make analytics fast and intuitive. Your DE background makes this easier, but the DS perspective on it is new.

---

### M4: Exploratory Data Analysis (~7 sessions)

**What you learn:** Descriptive statistics, distributions, correlations, hypothesis testing, data visualization. This is your first pure data science milestone.

**What ships:** A series of notebooks answering "what makes a good fantasy player?" with data.

| Task | Track | Description |
|------|-------|-------------|
| Notebook: distributions | B | **You explore:** What does the distribution of fantasy points look like? Is it normal? Skewed? How does it differ by position? Learn: mean, median, standard deviation, histograms. |
| Notebook: correlations | B | **You explore:** What stats correlate with fantasy points? Does target share predict WR scoring? Do rushing attempts predict RB scoring? Learn: correlation coefficients, scatter plots, what correlation ≠ causation means. |
| Notebook: year-over-year consistency | B | **You explore:** How consistent are players year to year? If a player scored well last year, how likely are they to repeat? Learn: autocorrelation, regression to the mean. |
| Notebook: positional value | B | **You explore:** Which positions are most valuable? Where is the biggest gap between top and replacement level? This directly feeds VORP later. Learn: percentiles, rank distributions. |
| Notebook: hypothesis testing | B | **You explore:** Is home field advantage real in fantasy? Do players perform differently after bye weeks? Learn: t-tests, p-values, statistical significance. |
| Notebook: visualization practice | B | **You build:** Beautiful, publication-quality charts with Plotly and matplotlib. Learn: chart types, when to use each, accessible color palettes. |
| Synthesis notebook | B | **You write:** A summary notebook pulling together findings. What did you learn that will shape your model design? |

**Concept spotlight:** *The difference between "interesting" and "useful."* A correlation might be statistically significant but too small to improve predictions. Learning to distinguish signal from noise is the core skill of data science.

**Progressive independence:** This milestone is 100% you. Claude guides the questions and validates your analysis, but you write every line and interpret every chart.

---

### M5: Feature Engineering (~6 sessions)

**What you learn:** Feature design, rolling windows, normalization, the concept of information leakage, train/test philosophy.

**What ships:** feat_player_weekly and feat_player_draft tables in dbt, ready for ML.

| Task | Track | Description |
|------|-------|-------------|
| Feature design session | B | **You decide** which features to build based on your EDA findings. What signals did you discover? Which ones are actionable? |
| Rolling window features | B | **You implement** rolling averages (3, 5, 10 game windows) in SQL/dbt. Learn: why window size matters, handling edge cases (start of season). |
| Trend features | B | **You calculate** slopes and trends. Is this player getting better or worse? Learn: simple linear trend over a window. |
| Team and matchup features | B | **You build** opponent defensive rankings, points-allowed-by-position. Learn: relative metrics vs. absolute. |
| Situational features | B | **You encode** injury status, home/away, weather, bye weeks. Learn: categorical encoding, feature interactions. |
| dbt feature models | A/B | Wire your feature logic into dbt feat_* models. Claude helps with dbt patterns, you write the SQL. |
| Information leakage notebook | B | **Critical lesson:** Learn why you can't use future data to predict the past. Understand train/test splits and why features must be computed BEFORE the game being predicted. |

**Concept spotlight:** *Information leakage* — the #1 mistake in applied ML. If your training data accidentally includes information from the future (like using a player's final stats to predict their stats), your model will look amazing in testing and fail completely in production. This mistake is subtle and common.

---

### M6: First ML Model (~7 sessions)

**What you learn:** Supervised learning, linear regression, loss functions, overfitting, cross-validation, evaluation metrics. Your first real ML model.

**What ships:** A baseline player projection model with measured accuracy, and the knowledge to explain how it works.

| Task | Track | Description |
|------|-------|-------------|
| Notebook: what is supervised learning? | B | **You learn:** The concept of learning from labeled data. Inputs (features) → output (fantasy points). What makes this different from traditional programming. |
| Model training harness | A | Reusable train/evaluate/predict code in src/. Data loading, splitting, evaluation framework. |
| Notebook: linear regression from scratch | B | **You build** a simple linear regression conceptually — understand the math (y = mx + b, but with many x's). Learn: what "fitting" means, what the coefficients represent. |
| Notebook: train your first model | B | **You train** a linear regression using scikit-learn on your features. Predict fantasy points. See how it does. |
| Notebook: overfitting | B | **You break things on purpose.** Train on all the data, test on the same data — looks great! Now test on held-out data — oops. Learn: why this happens, how to prevent it. |
| Notebook: cross-validation | B | **You implement** k-fold cross-validation. Get a more honest estimate of model performance. Learn: bias-variance tradeoff in plain terms. |
| Notebook: evaluation metrics | B | **You learn:** RMSE, MAE, R² — what do they mean in fantasy football terms? "My model is off by an average of X fantasy points per week." |
| Productionize the baseline | A/B | Move the trained model into src/fanstatsy/models/. Write tests. Save the model artifact. Claude helps with structure, you understand every line. |

**Concept spotlight:** *The baseline model is sacred.* Every future model gets compared against this one. If XGBoost can't beat linear regression, the complexity isn't worth it. Most of the value in ML comes from good features, not fancy algorithms.

**Progressive independence:** Claude walks you through concepts in sessions 1-3, then steps back. By session 6-7, you're training, evaluating, and interpreting on your own.

---

### M7: Better Models (~6 sessions)

**What you learn:** Ensemble methods, gradient boosting (XGBoost), feature importance, hyperparameter tuning, when complexity helps vs. hurts.

**What ships:** An improved projection model, with evidence showing whether it actually beats the baseline.

| Task | Track | Description |
|------|-------|-------------|
| Experiment tracking setup | A | MLflow local setup (or structured notebook tracking) for comparing model runs |
| Notebook: decision trees | B | **You learn** how a single decision tree works — visual, intuitive. Understand the tree structure. Then see why one tree overfits. |
| Notebook: random forests | B | **You learn** the ensemble idea — many weak trees averaging into a strong prediction. Train one, compare to linear regression. |
| Notebook: XGBoost | B | **You learn** gradient boosting — trees that learn from each other's mistakes. Train XGBoost, compare to everything so far. |
| Notebook: feature importance | B | **You analyze** which features XGBoost relies on most. Does this match your EDA intuition? Surprising findings? |
| Notebook: hyperparameter tuning | B | **You learn** what hyperparameters are (knobs you turn to control the model). Try grid search and random search. See diminishing returns. |
| Model comparison report | B | **You write** a structured comparison: linear regression vs. random forest vs. XGBoost. Which wins? By how much? Is the complexity worth it? |
| Productionize the winner | A/B | Update the model in src/ with the best performer. Version it. Update tests. |

**Concept spotlight:** *Diminishing returns in model complexity.* Going from linear regression to XGBoost might improve accuracy by 15%. Going from XGBoost to a deep neural network might improve it by 2%. Knowing when to stop is as important as knowing how to start.

---

### M8: Draft Intelligence (~7 sessions)

**What you learn:** VORP (Value Over Replacement Player), positional scarcity, Monte Carlo simulation, strategy testing through simulation.

**What ships:** Draft simulation engine and VORP-based player rankings for your league's draft.

| Task | Track | Description |
|------|-------|-------------|
| Notebook: VORP from scratch | B | **You implement** VORP — your first domain-specific statistical concept. Calculate replacement level for each position. Rank players by VORP instead of raw projections. See how the rankings change. |
| Simulation framework | A | Draft simulation engine scaffolding — configurable league settings, turn order, roster constraints |
| Notebook: modeling other drafters | B | **You build** a simple model of how other people draft — using ADP data and position-need logic. Not perfect, but good enough to simulate realistic drafts. |
| Draft simulation engine | B | **You wire together** VORP rankings + other-drafter model + your strategy into a simulation loop. Run 1,000 mock drafts. |
| Notebook: strategy analysis | B | **You analyze** simulation results. Which draft strategy (best VORP, position targets, zero-RB) produces the best outcomes? Learn: Monte Carlo simulation, confidence intervals on results. |
| Pre-draft player rankings | B | **You generate** your final player rankings for draft day. VORP-based, position-adjusted, with confidence intervals. |
| Draft prep report | B | **You create** a polished draft prep document — your cheat sheet. Rankings, strategy notes, sleepers, busts. Portfolio-quality. |

**Concept spotlight:** *Monte Carlo simulation* — answering "what's likely to happen?" by running thousands of random scenarios. This technique is used everywhere from finance to physics. Fantasy football is a surprisingly good domain for learning it.

---

### M9: Draft Dashboard (~5 sessions)

**What you learn:** Building real-time web applications, API polling, building UIs for data, operating under time pressure (90-second clock).

**What ships:** A live draft dashboard (Streamlit) that polls your ESPN draft and surfaces real-time recommendations.

| Task | Track | Description |
|------|-------|-------------|
| Streamlit app scaffold | A | App structure, layout, auto-refresh, styling |
| ESPN draft polling | A/B | **You test** the espn_api draft endpoints. Understand how the draft state updates. Claude helps with polling logic. |
| Real-time ranking engine | B | **You wire** your VORP rankings to update as players are drafted. Available player pool shrinks, VORP recalculates. |
| Dashboard UI | A/B | Display: recommended picks, roster so far, positional needs, reach/steal alerts. Claude builds layout, you define what to show. |
| Dry run testing | B | **You test** the dashboard against a completed draft (replay mode). Verify it would have given good advice. Fix issues. |

**Concept spotlight:** *The value of pre-computation.* During a 90-second clock, you can't train a model. Everything must be pre-computed — the dashboard just filters and displays. This is a real-world constraint in production ML systems.

**MVP COMPLETE — you're ready for draft day.**

---

## V1 — "Win the Season"

**Core question:** Can you make better weekly decisions than your competition, every week, for 17 weeks?

---

### M10: Weekly Projections (~6 sessions)

**What you learn:** Time series concepts, recency weighting, adapting models mid-season, matchup-specific predictions.

**What ships:** Automated weekly player projection pipeline.

| Task | Track | Description |
|------|-------|-------------|
| Weekly data refresh pipeline | A | Automated ingestion of latest stats, injuries, matchups after each week |
| Notebook: recency and weighting | B | **You learn** why recent performance matters more than season averages. Explore exponential weighting. |
| Notebook: matchup adjustments | B | **You build** matchup-specific projections — adjust player projections based on opponent defensive quality |
| Weekly projection pipeline | A/B | Productionize the weekly model run. Claude scaffolds, you write the projection logic. |
| Projection testing | B | **You validate** predictions against actual results from completed weeks. How good are your projections? |
| Model retraining strategy | B | **You decide** when to retrain — every week? Every 4 weeks? Learn about concept drift. |

---

### M11: Lineup Optimization (~6 sessions)

**What you learn:** Optimization algorithms, constraint satisfaction, expected value under uncertainty.

**What ships:** Automated lineup optimizer that respects roster constraints and handles the FLEX slot.

| Task | Track | Description |
|------|-------|-------------|
| Notebook: the optimization problem | B | **You formalize** the lineup problem — objective function, constraints, the FLEX complication |
| Brute-force optimizer | B | **You implement** enumeration of valid lineups for your roster size. It's fast enough — learn why. |
| Notebook: integer linear programming | B | **You learn** ILP — the "textbook" approach. Implement with scipy. Compare results to brute force. |
| Uncertainty handling | B | **You learn** expected value — when a player is "questionable," how do you value them? Probability × projection. |
| Lineup reasoning engine | B | **You build** the explanation layer — for each start/sit, generate the "why" in plain language |
| Productionize | A/B | Wire into src/fanstatsy/applications/. Tests. Output format for notifications. |

---

### M12: Notifications & Cloud (~7 sessions)

**What you learn:** AWS services (SES, SNS, Lambda, EventBridge), CDK infrastructure as code, cloud deployment.

**What ships:** SMS + email recommendations on a weekly schedule, fully deployed on AWS.

| Task | Track | Description |
|------|-------|-------------|
| AWS account setup | A/B | Configure IAM, billing alerts, CLI profiles. **You do this** — it's your account and your learning. |
| CDK project scaffold | A | CDK app structure, first stack definition |
| SES email setup | A/B | Verify your email, send a test notification. **You configure** the AWS console parts. |
| SNS SMS setup | A/B | Confirm your phone number, send a test SMS. |
| Lambda function | A/B | Deploy the weekly projection + lineup optimizer as a Lambda. Claude helps with packaging, you understand the deployment. |
| EventBridge scheduling | A/B | Cron schedule for weekly pipeline runs. Learn how cloud scheduling works. |
| End-to-end test | B | **You verify** the full pipeline: data refresh → projection → optimization → notification hits your phone. |

---

### M13: Waiver Wire Advisor (~5 sessions)

**What you learn:** Multi-week lookahead projections, opportunity cost, roster construction strategy.

**What ships:** Weekly free agent recommendations included in your notification email.

| Task | Track | Description |
|------|-------|-------------|
| Free agent data pipeline | A | Fetch available players from ESPN API |
| Multi-week projection | B | **You extend** your projection model to look 2-3 weeks ahead, not just this week |
| Opportunity cost analysis | B | **You build** the comparison: available player vs. your weakest starter. Is the upgrade worth burning waiver priority? |
| Waiver recommendations | B | Integrate into the weekly notification email |
| Notebook: waiver strategy | B | **You analyze** historical waiver pickups — which ones would have been worth it? |

---

### M14: Blog & Storytelling (~6 sessions)

**What you learn:** Data visualization best practices, storytelling with data, publishing pipelines.

**What ships:** Weekly blog posts with beautiful charts on GitHub Pages.

| Task | Track | Description |
|------|-------|-------------|
| GitHub Pages setup | A | Static site scaffold, theme, deployment from repo |
| Visualization style guide | B | **You define** your chart style — colors, fonts, chart types for different data |
| Weekly report template | A/B | Notebook template with sections: recap, MVP, bust, trends, model accuracy, preview |
| Notebook: first blog post | B | **You write** your first data-driven league analysis. Charts, narrative, takeaways. |
| Publishing pipeline | A | Notebook → HTML → GitHub Pages. Automated or one-command. |
| Cross-posting | B | Export to Markdown for Medium/Substack. Build your content presence. |

---

### M15: Model Monitoring (~5 sessions)

**What you learn:** Model drift, accuracy tracking over time, feedback loops, when to retrain.

**What ships:** A monitoring dashboard tracking prediction accuracy vs. actual results.

| Task | Track | Description |
|------|-------|-------------|
| Accuracy tracking pipeline | A/B | After each week, compare projections to actuals. Store results. |
| Monitoring dashboard | A/B | Simple dashboard (notebook or Streamlit) showing weekly accuracy trends |
| Notebook: model drift analysis | B | **You analyze** — is your model getting worse over time? Which positions? Which situations? |
| Retraining trigger | B | **You decide** and implement criteria for when to retrain the model |
| Season retrospective | B | **You write** an end-of-season analysis — how good were the models? What would you change? Portfolio-quality writeup. |

**V1 COMPLETE — you've run a data-driven fantasy season.**

---

## V2+ — "Level Up & Expand"

These milestones happen post-season. Order is flexible — pick what's most interesting.

### M16: PyTorch Deep Learning (~7 sessions)

**What you learn:** Neural network fundamentals, backpropagation, custom architectures, GPU training.

| Task | Track | Description |
|------|-------|-------------|
| Notebook: neural network from scratch | B | Build a simple neural network conceptually — neurons, layers, activation functions |
| Notebook: PyTorch basics | B | Tensors, autograd, building a model in PyTorch |
| Notebook: train a player projection NN | B | Train a neural network on your fantasy data. Compare to XGBoost. |
| Notebook: architecture experiments | B | Try different architectures — deeper, wider, dropout, batch norm. What helps? |
| Productionize | A/B | Best PyTorch model into src/, with tests and model versioning |

### M17: Cloud ML — SageMaker (~5 sessions)

**What you learn:** Cloud training, model registry, MLOps fundamentals.

| Task | Track | Description |
|------|-------|-------------|
| SageMaker setup | A/B | CDK stack for SageMaker, training job configuration |
| Cloud training run | B | Train your model on SageMaker instead of locally. Understand the tradeoffs. |
| Model registry | A/B | Version models in S3. Track which model was trained on what data. |
| Comparison | B | Local vs. cloud training — when does cloud make sense? |

### M18: Model Serving API (~5 sessions)

**What you learn:** API design, Lambda cold starts, inference optimization, production ML serving.

| Task | Track | Description |
|------|-------|-------------|
| API design | B | Define endpoints: /predict, /rankings, /lineup |
| Lambda packaging | A | Package model + inference code for Lambda deployment |
| API Gateway | A/B | REST API in front of Lambda via CDK |
| Performance testing | B | Measure latency, cold starts. Optimize if needed. |

### M19: DraftKings Optimizer (~7 sessions)

**What you learn:** Knapsack problem, integer linear programming, stochastic optimization, bankroll management.

| Task | Track | Description |
|------|-------|-------------|
| DraftKings API integration | A | Connect to DraftKings contest and salary data |
| Salary cap optimizer | B | Knapsack problem — maximize points under $50K constraint. ILP with PuLP. |
| Stochastic optimization | B | Account for projection uncertainty in lineup construction |
| Bankroll management | B | Build automated limits and tracking |

### M20: NBA Extension (~6 sessions)

**What you learn:** Domain transfer, data source abstraction, how ML generalizes across domains.

| Task | Track | Description |
|------|-------|-------------|
| NBA data sources | A/B | Find and integrate NBA equivalents of nfl_data_py |
| Adapter pattern | B | Abstract the pipeline so it works for multiple sports |
| NBA feature engineering | B | What features matter in basketball? Different sport, different signals. |
| NBA model | B | Train and evaluate. How well does your approach transfer? |

### M21: Ensemble Mastery (~5 sessions)

**What you learn:** Model stacking, blending, voting, when ensembles help vs. hurt.

| Task | Track | Description |
|------|-------|-------------|
| Notebook: ensemble theory | B | Why combining models can be better than any single model |
| Stacking implementation | B | Train a meta-model on top of your existing models' predictions |
| Blending experiments | B | Try different combination strategies. Measure improvement. |
| Production ensemble | A/B | Best ensemble approach into production pipeline |
