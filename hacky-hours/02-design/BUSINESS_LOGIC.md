# Business Logic — Fanstatsy Foosball

## Overview

This document defines the rules, calculations, and domain-specific behavior that drive the system. "Business logic" here means: how fantasy football scoring works, how the draft simulator makes decisions, how the lineup advisor ranks players, and when/how notifications fire.

---

## Fantasy Scoring Engine

### Purpose

Calculate fantasy points for any player in any game, using the scoring rules from your specific ESPN league.

### How It Works

Fantasy scoring assigns point values to real NFL statistics. Different leagues use different scoring formats — the three most common are:

| Format | Key Difference |
|--------|---------------|
| **Standard** | Receptions are worth 0 points — rewards big plays over volume |
| **Half-PPR** | Each reception is worth 0.5 points — balances volume and big plays |
| **PPR** (Points Per Reception) | Each reception is worth 1.0 point — rewards high-target receivers |

The scoring format changes which players are most valuable. In PPR leagues, a wide receiver who catches 8 passes for 60 yards (8 + 6 = 14 points) is more valuable than one who catches 3 passes for 90 yards (3 + 9 = 12 points). In standard scoring, it's the opposite (6 vs 9 points).

### Scoring Rules

Scoring configuration is loaded from ESPN at the start of each season and stored in `configs/scoring.yaml`. The engine never hardcodes point values.

**Default scoring reference (may differ from your league):**

| Category | Stat | Typical Points |
|----------|------|---------------|
| **Passing** | Passing yard | 0.04 (1 pt per 25 yards) |
| | Passing TD | 4 |
| | Interception thrown | -2 |
| | 300+ yard bonus | 0 (league-dependent) |
| **Rushing** | Rushing yard | 0.1 (1 pt per 10 yards) |
| | Rushing TD | 6 |
| | 100+ yard bonus | 0 (league-dependent) |
| **Receiving** | Receiving yard | 0.1 (1 pt per 10 yards) |
| | Receiving TD | 6 |
| | Reception (PPR) | 1.0 / 0.5 / 0.0 |
| **Turnovers** | Fumble lost | -2 |
| **Kicking** | FG made (0-39) | 3 |
| | FG made (40-49) | 4 |
| | FG made (50+) | 5 |
| | FG missed | -1 |
| | Extra point made | 1 |
| **Defense/ST** | Sack | 1 |
| | Interception | 2 |
| | Fumble recovery | 2 |
| | Defensive TD | 6 |
| | Safety | 2 |
| | Points allowed tiers | Varies (0 pts allowed = 10 pts, etc.) |

### Calculation Logic

```
fantasy_points = sum(stat_value * points_per_stat for each stat)
```

The engine:
1. Loads scoring config from `configs/scoring.yaml`
2. Maps each player's game stats to the scoring rules
3. Computes total fantasy points
4. Stores all three formats (std, half-PPR, PPR) in `fct_player_games` for flexibility

### Edge Cases

- **Negative points are real.** A QB who throws 3 interceptions and no TDs can score negative. The model must handle this.
- **Players on bye weeks** score 0 (they don't play). This is different from a player who played and scored 0.
- **Injured players** who are active but leave early may have partial stats.
- **Stat corrections** — the NFL occasionally corrects stats after the game. Re-run scoring if corrections affect your league week.

---

## Draft Simulator

### Purpose

Simulate thousands of draft scenarios to identify optimal draft strategies and player values, then provide real-time guidance during the live draft.

### Draft Formats

| Format | How It Works |
|--------|-------------|
| **Snake draft** | Teams pick in order (1→12), then reverse (12→1), repeat. Pick position matters — early picks get top talent, late picks get two picks close together. |
| **Auction draft** | Every team has a budget (typically $200). Any player can be nominated, and teams bid. Strategy is about budget management. |

Your league's format will be read from ESPN settings.

### Pre-Draft: Player Valuation

**Value Over Replacement Player (VORP)** — the key concept for draft strategy.

A player's fantasy value isn't their raw projected points — it's how much better they are than the *next available player at their position*. A QB who scores 20 PPG isn't valuable if every QB scores 18 PPG. A tight end who scores 12 PPG is extremely valuable if the next best TE scores 6 PPG.

```
VORP = Player's projected PPG - Replacement-level PPG for that position
```

Replacement level = the projection of the best unrostered player at that position (typically the player ranked around position_count × number_of_teams).

This is one of the first statistical concepts we'll build and learn — it's foundational to draft strategy.

### Pre-Draft: Simulation Engine

The simulator runs mock drafts to test strategies:

1. **Input:** Player projections, league settings (teams, roster slots, scoring), draft format
2. **Simulate other teams' picks** using a combination of:
   - ADP (Average Draft Position) from public mock drafts — what "average" drafters do
   - Position-need logic — teams tend to fill roster holes
   - Randomness — real drafts are unpredictable
3. **Your strategy** — configurable:
   - "Best available VORP" (always take highest value)
   - "Position target" (e.g., force RB in rounds 1-2)
   - "Zero RB" (punt on RB early, load up on WR/TE)
   - Custom rules
4. **Output:** For each simulation — your final roster, projected season total, win probability
5. **Aggregate:** Over thousands of simulations — which strategies produce the best outcomes?

### Live Draft: Real-Time Advisor

During the actual draft (90-second pick clock):

1. **Poll ESPN API** every 3-5 seconds to detect new picks
2. **Update available player pool** — remove drafted players
3. **Recalculate VORP** for all remaining players given current state
4. **Display on dashboard:**
   - Top 5 recommended picks ranked by VORP
   - Your current roster and positional needs
   - "Reach alert" — flag if a player is being drafted much earlier than their projection
   - "Steal alert" — flag players still available well past their projected pick
5. **Must respond within seconds** — all calculations are pre-computed and filtered, not computed from scratch

### Draft Dashboard Requirements

- Local web app (Streamlit or Flask)
- Auto-refreshes when new picks are detected
- Shows: your pick position, time until your pick, recommended picks, roster so far
- Works on a second screen while you draft on ESPN on your primary screen
- No AI agent making decisions — the math is pre-computed, you choose

---

## Lineup Advisor

### Purpose

Every week during the NFL season, decide which players from your roster to start and which to bench. The right lineup decision can be the difference between winning and losing a matchup.

### How Lineup Decisions Work

A fantasy roster has limited starting slots:

| Slot | Count (typical) | Notes |
|------|-----------------|-------|
| QB | 1 | Quarterback |
| RB | 2 | Running backs |
| WR | 2 | Wide receivers |
| TE | 1 | Tight end |
| FLEX | 1 | Can be RB, WR, or TE — your choice |
| K | 1 | Kicker |
| DST | 1 | Defense/Special Teams |
| BN | 6-7 | Bench (don't score points) |

Each week, you choose which players fill each slot. Players on your bench don't score.

### Weekly Decision Pipeline

**Timeline:** Games are typically Sunday 1pm, Sunday 4pm, Sunday night, Monday night. Lineup locks at each game's kickoff.

**Pipeline runs mid-week (Wednesday-Thursday):**

1. **Ingest latest data:**
   - Injury reports (Wednesday, Thursday, Friday practice reports)
   - News and depth chart changes
   - Updated opponent defensive stats
   - Weather forecasts for outdoor games

2. **Generate player projections for the week:**
   - Run the projection model for each player on your roster
   - Factor in matchup (opponent defense quality vs. this position)
   - Adjust for injuries (downgrade questionable players, zero out players marked Out)
   - Adjust for weather (outdoor games with high wind reduce passing value)

3. **Optimize starting lineup:**
   - This is a constrained optimization problem: maximize total projected points while respecting roster slot rules
   - The FLEX slot makes this interesting — should you start a 3rd RB or a 3rd WR?
   - Handle uncertainty: if a player is "questionable," consider the expected value (projection × probability of playing)

4. **Generate recommendation with reasoning:**
   - For each start/sit decision, explain why
   - Show the projected point differential
   - Flag high-uncertainty decisions ("this is a coin flip — here's why")
   - Show confidence level

### Recommendation Example

```
Week 5 Lineup Recommendation
Generated: Wednesday, Oct 7, 2026

START                          BENCH
QB: [Player A] — 19.2 proj    QB: [Player B] — 14.1 proj
  Reason: Faces 28th-ranked      Reason: Faces #3 pass D,
  pass D, 3-game uptrend         road game, high wind

RB: [Player C] — 15.8 proj    RB: [Player E] — 8.2 proj
RB: [Player D] — 14.1 proj      Reason: Backup role, <40% snaps

WR: [Player F] — 16.5 proj
WR: [Player G] — 13.9 proj

FLEX: [Player H] (RB) — 12.7 proj
  Decision: Start [H] over [Player I] (WR, 11.9 proj)
  Confidence: 62% — close call, monitor Friday injury report

⚠️ Watch: [Player F] was limited in Wednesday practice (ankle)
   → If downgraded to Doubtful Friday, swap in [Player I]
   → I'll send an updated recommendation Friday evening

Projected team total: 121.4 points
Opponent projected: 108.7 points
Win probability: 68%
```

### Re-check Triggers

The advisor runs again if:
- A starter's injury status changes (especially Friday/Saturday updates)
- A key player is ruled Out
- Significant news breaks (trade, benching, coaching change)

---

## Notification System

### Purpose

Push lineup recommendations and alerts to your phone (SMS) and email so you never miss a deadline or critical update.

### Notification Types

| Type | Channel | When | Priority |
|------|---------|------|----------|
| **Weekly recommendation** | Email + SMS | Wednesday evening | Normal |
| **Injury update** | SMS | When a starter's status changes Fri-Sun | High |
| **Final lineup reminder** | SMS | Sunday 10am (3 hrs before kickoff) | High |
| **Lineup lock warning** | SMS | 30 min before any game with your starter | Critical |
| **Weekly recap** | Email | Monday evening after MNF | Normal |
| **Draft prep ready** | Email | When pre-season models are trained | Normal |

### SMS Content Rules

SMS messages are short (160 chars for a single segment). Be concise:

```
🏈 INJURY ALERT: [Player A] (WR) downgraded to Doubtful.
Swap in [Player B] at FLEX.
Proj: +3.2 pts. Set lineup by 1pm Sun.
```

### Email Content Rules

Emails include full analysis with charts and reasoning. Use HTML formatting. Link to the full blog post or notebook if available.

### Infrastructure

| Component | Service | Free Tier |
|-----------|---------|-----------|
| Email sending | AWS SES | 200/day from Lambda |
| SMS sending | AWS SNS | 100 SMS/month |
| Scheduling | AWS EventBridge (cron) | Free |
| Processing | AWS Lambda | 1M requests/month |

### Notification Logic

```
WEEKLY SCHEDULE (during NFL season):
  Wednesday 8pm ET → Run projection pipeline → Send weekly recommendation
  Friday 6pm ET    → Check injury updates → Send update if starters affected
  Sunday 10am ET   → Final lineup check → Send reminder with any last changes
  Sunday 12:30pm ET → Lock warning for 1pm games
  Monday 11pm ET   → After MNF → Send weekly recap

DRAFT SEASON:
  When models finish training → Send "draft prep ready" email with link to dashboard
```

---

## Lineup Optimization Algorithm

### The Problem

Given:
- N players on your roster, each with a projected score for this week
- Roster slot constraints (1 QB, 2 RB, 2 WR, 1 TE, 1 FLEX, 1 K, 1 DST)
- FLEX can be filled by RB, WR, or TE

Find: the assignment of players to slots that maximizes total projected points.

### Why This Isn't Trivial

The FLEX slot creates a combinatorial problem. Without FLEX, you'd just pick the best player at each position. With FLEX, you need to consider: is it better to start your 3rd-best RB or your 3rd-best WR?

Example: Your RBs project at 18, 15, 12. Your WRs project at 17, 14, 11.
- If FLEX = RB3 (12): Total = 18+15+12+17+14 = 76
- If FLEX = WR3 (11): Total = 18+15+17+14+11 = 75
- RB3 in FLEX wins by 1 point

With more players and uncertainty, this gets more interesting.

### Approach

For a roster of this size, brute-force enumeration of valid lineups is fast enough (there aren't that many combinations). No need for fancy optimization solvers. But this is a great opportunity to learn about:

- **Integer linear programming** — the "textbook" way to solve lineup optimization
- **Constraint satisfaction** — a broader framework for problems with rules
- **Expected value under uncertainty** — when projections have confidence intervals

We'll start with the simple approach and layer in more sophisticated methods as learning progresses.

---

## Waiver Wire / Free Agent Logic (V1)

### Purpose

During the season, players can be picked up from the free agent pool ("waiver wire"). Identifying which available players are undervalued is a weekly opportunity.

### Logic

1. **Scan free agent pool** via ESPN API
2. **Project each available player's** upcoming weeks (not just this week — look 2-3 weeks ahead)
3. **Compare to your weakest starter** at each position
4. **Flag pickups where:** available player's projection > your worst starter's projection by a meaningful margin
5. **Include in weekly recommendation email**

### Waiver Priority Considerations

Most leagues use a waiver priority system (worst record gets first pick). Recommendations should note whether a pickup is worth "burning" a high waiver priority on vs. waiting for free agency (after waivers clear).

---

## Blog / Report Generation

### Purpose

Produce weekly data-driven analysis of your fantasy league that's interesting, visual, and educational. Content angle: "football stats from someone learning football through data."

### Weekly Report Content

| Section | What It Covers |
|---------|---------------|
| **Matchup Recap** | How each matchup played out vs. projections. Who over/under-performed? |
| **MVP of the Week** | Highest-scoring player in the league. What happened statistically? |
| **Biggest Bust** | Biggest gap between projection and actual. What went wrong? |
| **Waiver Wire Gems** | Available players who outperformed rostered players |
| **Trend Watch** | Players trending up or down over the last 3 weeks |
| **Model Accuracy** | How good were the projections this week? Running accuracy tracker |
| **Next Week Preview** | Key matchups, injury situations, bye weeks to watch |

### Visualization Standards

- **Interactive charts** (Plotly) for the blog version
- **Static charts** (matplotlib/seaborn) for email and social media
- **Consistent color palette** — define team colors and a project color scheme
- **Accessible** — colorblind-safe palettes, alt text for images, clear labels
- Every chart must have a title, axis labels, and a one-sentence takeaway

### Publishing Pipeline

1. Analysis runs in a Jupyter notebook (automated or manual)
2. Notebook exports to HTML and/or Markdown
3. Push to GitHub Pages (or chosen blog platform)
4. Link included in the weekly recap email

---

## DraftKings Integration (V2+)

### Purpose

Use the same projection models to make small, legal bets on DraftKings daily fantasy contests.

### Key Differences from Season-Long Fantasy

| Aspect | Season-Long (ESPN) | Daily (DraftKings) |
|--------|-------------------|-------------------|
| Roster | Fixed for the season (with trades/waivers) | New lineup every week/day |
| Constraint | Position slots | Position slots + salary cap ($50,000) |
| Objective | Win your league over 17 weeks | Win individual contests |
| Scoring | League-specific | DraftKings-specific (usually half-PPR with bonuses) |

### Salary Cap Optimization

DraftKings assigns each player a salary. You must build a lineup under $50,000. This turns lineup optimization into a **knapsack problem** — maximize projected points subject to a budget constraint.

This is a harder optimization problem than the ESPN lineup advisor and a great opportunity to learn about:
- Knapsack algorithms
- Integer linear programming (using `scipy` or `PuLP`)
- Stochastic optimization (accounting for projection uncertainty)

### Risk Management

- **Strict bankroll limits** — define a maximum weekly spend before starting
- **Track all bets and outcomes** in the database
- **Never chase losses** — automated stop-loss if weekly losses exceed threshold
- This is for learning and fun, not income

### Not In Scope for V1

This entire section is V2+. The projection models and feature pipeline built for V1 are reusable — DraftKings just adds a salary constraint and a different scoring system.
