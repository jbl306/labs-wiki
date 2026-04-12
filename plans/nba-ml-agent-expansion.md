# NBA-ML Engine — Agent Expansion Plan

> Goal: Add specialized Copilot CLI agents to nba-ml-engine that directly increase prediction hit rate and close the gap to consistent profitability.

## Current State

- **1 agent exists**: `nba-ml-pipeline` — covers pipeline ops, monitoring, debugging
- **1 skill exists**: `execute-sprint-from-report` — orchestrates sprint execution
- **Hit rate**: 53.2% overall; STL/BLK/FG3M profitable, PTS/REB/AST underwater
- **ECE**: 0.36 (target < 0.20) — calibration is the #1 accuracy bottleneck
- **Known bugs**: 8 critical issues from Sprint 47 audit directly hurting accuracy
- **Features**: ~326 engineered, but gaps in game script, fatigue modeling, and interaction tuning

## Gap Analysis

The existing pipeline agent is an **ops generalist** — it runs commands and diagnoses failures. It doesn't have the specialized knowledge to:

1. **Design and validate calibration fixes** (statistical expertise needed)
2. **Explore and evaluate new features** (ML experimentation workflow)
3. **Systematically fix data quality bugs** (multi-step debugging with SQL validation)
4. **Run controlled experiments** (A/B test designs, significance testing)

## Proposed Agents (4 new)

### 1. `model-calibration` — Calibration & Edge Optimization Agent

**Why**: The inverse edge-accuracy problem (high confidence = low hit rate) is the single biggest accuracy blocker. ECE of 0.36 means the model's confidence scores are nearly meaningless. Fixing calibration alone could add 2-3% hit rate on mid-edge bets.

**Scope**:
- Isotonic regression / Platt scaling per-stat (not one-size-fits-all)
- Edge threshold optimization (current 2% is too high; 0.5% bets are most profitable)
- Confidence interval calibration (stl/blk need wider percentiles: 7-93% vs 10-90%)
- Negative prediction clamping (must happen BEFORE CI calculation, not after)
- Vig-adjusted model selection (replace R² with 52.4% breakeven hit rate as promotion gate)
- Daily calibration refresh (60-day rolling isotonic refit, not just post-retrain)

**Key commands**: `evaluate`, `backtest`, `predict`, direct SQL for hit rate queries

**Success metric**: ECE < 0.20, hit rate > 54% across all profitable stats

---

### 2. `feature-lab` — Feature Engineering & Experimentation Agent

**Why**: The feature space (326 features) hasn't been systematically expanded since Sprint 27. Game script, lineup context, and advanced interaction features are missing. Feature importance analysis shows diminishing returns from current features — new signal sources needed.

**Scope**:
- Game script features (blowout detection → reduced minutes; close game → star usage up)
- Lineup-based features (on/off court impact, 2-man/3-man lineup stats)
- Fatigue modeling (back-to-back, 3-in-4, travel distance, altitude)
- Season phase features (pre/post All-Star, playoff push, tank mode)
- Interaction feature auto-tuning via Optuna (home × opp_drtg is static currently)
- Feature ablation studies (systematically remove features to find noise)
- Per-stat feature selection (different top-20 features for STL vs PTS)

**Key commands**: `train` with feature flags, `backtest` for A/B comparison, `evaluate`

**Success metric**: Find 3+ new features with >0.5% hit rate improvement per stat in backtests

---

### 3. `data-quality` — Data Pipeline & Quality Agent

**Why**: 4 of the 8 Sprint 47 critical bugs are data quality issues. Bad data silently poisons predictions — timezone misalignment alone affects 10-15% of evening game predictions. The pipeline agent handles ops but doesn't validate data correctness.

**Scope**:
- Game lines timezone fix (Eastern conversion before date extraction)
- Prop line defaults (NULL instead of 0.0 for missing lines)
- Alt-line contamination (DISTINCT ON with source column in BFF)
- Duplicate snapshot prevention (upsert pattern for PropLineSnapshot)
- Prop line freshness monitoring (alert if lines > 6 hours old at prediction time)
- Data validation assertions (automated checks between ingest and predict steps)
- Silent failure elimination (upgrade DEBUG → INFO/WARNING for all error paths)
- Stale stat cleanup (remove fg_pct/ft_pct from pipeline mode — no prop lines exist)

**Key commands**: `ingest`, `psql` queries, `docker logs`, data validation scripts

**Success metric**: Zero data-corruption errors in 30-day window; correct timezone on 100% of game lines

---

### 4. `backtest-lab` — Backtesting & Performance Regression Agent

**Why**: No automated performance regression testing exists. After every model change or feature addition, someone must manually run backtests and interpret results. This agent codifies the evaluation workflow and prevents accuracy regressions from reaching production.

**Scope**:
- Automated pre-deployment backtesting (any model change triggers validation)
- Per-stat performance tracking (separate hit rate trends for each of 9 stats)
- Edge bucket analysis automation (0-1%, 1-2%, 2-3%, 3-5%, 5%+ buckets)
- Statistical significance testing for A/B experiments (minimum bet count, chi-squared)
- Drawdown monitoring (alert if any stat drops below breakeven for 3+ consecutive days)
- CLV (Closing Line Value) tracking per model version
- Shadow mode orchestration (run candidate model alongside production, compare)
- Kelly criterion validation (verify sizing doesn't exceed bankroll risk limits)

**Key commands**: `backtest`, `evaluate`, `compare` (model versions), MLflow API

**Success metric**: Catch 100% of accuracy regressions before production deployment

---

## Agent Interaction Map

```
                    ┌─────────────────────┐
                    │  nba-ml-pipeline     │
                    │  (existing - ops)    │
                    └─────────┬───────────┘
                              │ triggers
               ┌──────────────┼──────────────┐
               ▼              ▼              ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ data-quality  │ │model-calibr. │ │ feature-lab  │
    │ fix → validate│ │tune → eval   │ │ explore→test │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │                │                │
           └────────────────┼────────────────┘
                            ▼
                   ┌──────────────┐
                   │ backtest-lab │
                   │ validate all │
                   └──────────────┘
```

**Workflow**: Pipeline agent detects issues → delegates to specialist → backtest-lab validates before production.

## Impact Projection

| Agent | Expected Hit Rate Δ | Confidence | Effort |
|-------|---------------------|------------|--------|
| model-calibration | +2-3% | High (known bugs) | Medium |
| data-quality | +1-2% | High (known bugs) | Low-Medium |
| feature-lab | +1-2% | Medium (experimental) | High |
| backtest-lab | prevents -2% regressions | High | Medium |
| **Combined** | **+4-7% (to ~57-60%)** | **Medium-High** | |

At 57%+ overall hit rate, ALL stats become profitable against -110 vig (52.4% breakeven).

## Priority Order

1. **data-quality** — fastest wins, fixes known bugs corrupting predictions today
2. **model-calibration** — biggest single accuracy improvement, addresses #1 bottleneck
3. **backtest-lab** — prevents future regressions, enables safe experimentation
4. **feature-lab** — highest ceiling but most experimental; needs backtest-lab first

## Implementation Notes

- All agents go in `nba-ml-engine/agents/`
- Update `.github/copilot-instructions.md` agent table
- Each agent includes diagnostic playbooks specific to its domain
- Feedback loop: all agents write to `tasks/lessons.md`
- Agents reference Sprint 47 audit doc for specific bug details
