---
title: "Copilot Session Checkpoint: Retrained Models, Deploying Improvements"
type: source
created: 2026-03-18
last_verified: 2026-04-21
source_hash: "2dd27a20077564eb88e056625dfe5cd1c2c8abd76362bdf39f21f0b3da93e67f"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-retrained-models-deploying-improvements-59ba9a6c.md
quality_score: 90
concepts:
  - nba-ml-prediction-platform-sprint-workflow
  - ensemblemodel-stacking-meta-learner
  - stat-specific-edge-thresholds-in-prediction-filtering
  - homelab-server-deployment-architecture-nba-ml-platform
related:
  - "[[NBA ML Prediction Platform Sprint Workflow]]"
  - "[[EnsembleModel Stacking Meta-Learner]]"
  - "[[Homelab Server Deployment Architecture for NBA ML Platform]]"
  - "[[EnsembleModel]]"
  - "[[Homelab]]"
  - "[[NBA ML Engine]]"
  - "[[Docker]]"
tier: archive
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, dashboard, docker, machine learning, ensemble learning, nba ml, deployment]
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: validated
---

# Copilot Session Checkpoint: Retrained Models, Deploying Improvements

## Summary

The user requested a full sprint on their NBA ML prediction platform: create a new GitHub branch, implement improvements from 4 existing plan documents, deploy to their homelab server, retrain all 9 prediction categories, evaluate model performance, and document everything in a progress tracker. We're working directly on the homelab server (beelink-gti13) which runs Docker containers for the full stack (TimescaleDB, MLflow, FastAPI API, Streamlit dashboard, Ofelia scheduler).

## Key Points

- Branch created and pushed
- Code changes committed (edge thresholds, mobile CSS, per-stat hit rate)
- Docker containers rebuilt and deployed
- All 9 categories retrained successfully
- User requested: Open new branch, create progress tracker, implement all tasks, deploy, retrain, evaluate, document
- Found 4 existing plan docs in `docs/plan/`: dashboard-model-improvements, dashboard-ux-overhaul, fix-enhance, ml-audit

## Execution Snapshot

**Files modified:**
- `config.py`: Added STAT_EDGE_THRESHOLDS dict, EXCLUDED_PROP_STATS list (lines ~111-130)
- `dashboard/app.py`: Enhanced mobile CSS (lines ~570-615), added load_edge_hit_rate_by_stat() function (~line 900), filtered FG%/FT% from edge hit rate query, committed timezone changes
- `src/evaluation/backtester.py`: Updated edge filtering to use stat-specific thresholds and exclude percentage stats (lines ~163-180)

**Git commits on `feature/dashboard-model-improvements`:**
1. `9250746` - feat(dashboard): timezone-aware queries using ET for game dates
2. `9030e8c` - feat: stat-specific edge thresholds, mobile CSS, per-stat hit rate

Branch pushed to: `origin/feature/dashboard-model-improvements`

**Training results (all 9 categories retrained 2026-03-18):**

| Stat   | Best Model     | Val MSE  | Test MSE |
|--------|---------------|----------|----------|
| pts    | EnsembleModel | 43.7283  | 41.6886  |
| reb    | EnsembleModel | 7.2081   | 6.8723   |
| ast    | EnsembleModel | 4.0881   | 3.8014   |
| stl    | EnsembleModel | 0.9273   | 0.9852   |
| blk    | RidgeModel    | 0.7250   | 0.6214   |
| tov    | EnsembleModel | 1.6718   | 1.6400   |
| fg_pct | EnsembleModel | 0.0349   | 0.0368   |
| ft_pct | EnsembleModel | 0.0644   | 0.0665   |
| fg3m   | EnsembleModel | 1.7397   | 1.7232   |

**Current state:**
- [x] Branch created and pushed
- [x] Code changes committed (edge thresholds, mobile CSS, per-stat hit rate)
- [x] Docker containers rebuilt and deployed
- [x] All 9 categories retrained successfully
- [ ] Generate predictions with new models (predict --store)
- [ ] Run backtester evaluation
- [ ] Create progress tracker markdown
- [ ] Update documentation
- [ ] Final push to GitHub

SQL todos table has 13 items tracked. Status: commit-timezone ✓, new-branch ✓, move-crossyear ✓, add-overview-charts ✓, mobile-css ✓, fix-edge-hitrate ✓, gamelog-freshness ✓, edge-thresholds ✓, deploy ✓, retrain (in_progress), evaluate (pending), progress-tracker (pending), push-github (pending).

## Technical Details

- **We ARE the homelab**: hostname is beelink-gti13, Docker containers run locally. No SSH needed.
- **Feature mismatch error**: The scheduler's predict step was failing with "feature_names mismatch" because trained models expected old feature set but builder produces 307 columns now. Retraining fixed this.
- **Homelab compose**: Located at `/home/jbl/projects/homelab/compose/compose.nba-ml.yml`, uses `${NBA_ML_ENGINE_PATH}` env var pointing to the source repo. Builds from Dockerfile directly.
- **Container architecture**: nba-ml-db (TimescaleDB), nba-ml-mlflow (tracking), nba-ml-api (FastAPI + training), nba-ml-dashboard (Streamlit), nba-ml-scheduler (Ofelia cron)
- **Scheduler runs**: pipeline-daily at 14:00 UTC (10AM ET), props-refresh at 19:00 UTC, predict-refresh at 19:30 UTC
- **Database state**: 95,004 feature rows, game logs up to 2026-03-17, prop_lines from 2026-03-16 to 2026-03-18 (1,961 rows), predictions 9,108 rows (old, need refresh)
- **Edge hit rate data**: Only 1 day of historical data (March 16, 354 bets at 8% threshold, 55.9% hit rate). Chart will populate as more days accumulate.
- **Test suite**: 30 tests collected, 28 pass, 2 fail due to pre-existing libgomp.so.1 missing (LightGBM native lib not installed on host — only works in Docker container)
- **EnsembleModel**: Stacking meta-learner using 3-fold CV over XGBoost + LightGBM + RandomForest + Ridge. Best performer for 8/9 stats. RidgeModel won for blk.
- **LSTM underperforms**: val_mse 2-3x worse than other models across all stats. Early stops at epochs 10-12.
- **Git remote**: `git@github.com:jbl306/nba-ml-engine.git`
- **Dashboard timezone**: Uses America/New_York, with `DASHBOARD_TODAY_SQL` for ET-aware date queries
- **pandas FutureWarning**: DataFrameGroupBy.apply on home/away rolling features triggers deprecation warning — cosmetic, not breaking

## Important Files

- `config.py`
- Central configuration for all settings
- Added STAT_EDGE_THRESHOLDS (per-stat edge thresholds), EXCLUDED_PROP_STATS (fg_pct, ft_pct excluded)
- TARGET_STATS defined at line ~69: ["pts", "reb", "ast", "stl", "blk", "tov", "fg_pct", "ft_pct", "fg3m"]
- Lines ~111-130: new edge threshold config

- `dashboard/app.py` (3,113+ lines)
- Main Streamlit dashboard, single-file app
- Key functions: render_overview (L1475), render_seasons (L1937), render_props (L1723), load_edge_hit_rate (L865), load_edge_hit_rate_by_stat (~L900)
- Mobile CSS at lines ~570-615
- inject_styles() contains all CSS

- `src/evaluation/backtester.py` (436+ lines)
- Backtesting engine comparing predictions vs actuals
- run_backtest() is the main function (~L68)
- Updated edge filtering at ~L163-180 to use stat-specific thresholds
- BacktestResult dataclass holds all metrics

- `src/training/trainer.py`
- Training orchestrator: train_all() trains all models for all stats
- MODEL_CLASSES: XGBoost, LightGBM, RandomForest, Ridge, Ensemble, LSTM
- Logs to MLflow, registers best models

- `/home/jbl/projects/homelab/compose/compose.nba-ml.yml`
- Homelab Docker Compose for all NBA ML services
- Uses NBA_ML_ENGINE_PATH env var for build context
- Ofelia scheduler labels for cron jobs

- `docs/plan/plan_dashboard-model-improvements_0318.md`
- Primary plan doc for this sprint: 6 phases covering dashboard improvements and model tuning
- Phases 1-2 were already implemented, 3-6 addressed in this sprint

- `main.py`
- CLI entry point with commands: init, ingest, train, predict, serve, dashboard, pipeline, backtest
- pipeline command runs 7-step daily process

## Next Steps

**Remaining work:**
1. **Generate predictions** with newly trained models: `docker exec nba-ml-api python main.py predict --store`
2. **Run backtester evaluation** across all 9 categories to measure hit rate, P&L, ROI
3. **Create progress tracker markdown** (`tasks/progress_dashboard-model-improvements_0318.md`) with training results and evaluation metrics
4. **Update documentation** (README, relevant docs files if needed)
5. **Final git push** to sync GitHub repo

**Immediate next actions:**
- Run `docker exec nba-ml-api python main.py predict --store` to generate fresh predictions with the new models
- Run backtester via Python in the container: iterate over each stat, run backtest, collect results
- Write the progress tracker with all evaluation data
- Commit progress tracker and push to GitHub
- Mark all SQL todos as done

**Open questions:**
- The backtester only has ~3 days of prop_lines data (March 16-18), so evaluation will be limited. More meaningful evaluation will accumulate over time.
- Should consider running `python main.py pipeline` to do a full pipeline refresh (ingest + predict) rather than just predict

## Related Wiki Pages

- [[NBA ML Prediction Platform Sprint Workflow]]
- [[EnsembleModel Stacking Meta-Learner]]
- [[Homelab Server Deployment Architecture for NBA ML Platform]]
- [[EnsembleModel]]
- [[Homelab]]
- [[NBA ML Engine]]
- [[Docker]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-retrained-models-deploying-improvements-59ba9a6c.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-18 |
| URL | N/A |
