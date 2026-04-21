---
title: "Copilot Session Checkpoint: Pipeline Resilience Fixes, Dashboard Metrics Investigation"
type: source
created: 2026-04-12
last_verified: 2026-04-21
source_hash: "e46b28ceb3142b4379144f0651127cee40410b71fb087908b377ab58ca92a883"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-pipeline-resilience-fixes-dashboard-metrics-inve-3ea0d6d8.md
quality_score: 100
concepts:
  - pipeline-resilience-in-machine-learning-systems
  - dashboard-metrics-consistency-and-hit-rate-discrepancy-analysis
  - mlflow-resilience-and-fallback-mechanisms-in-model-training
related:
  - "[[Pipeline Resilience in Machine Learning Systems]]"
  - "[[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]"
  - "[[MLflow Resilience and Fallback Mechanisms in Model Training]]"
  - "[[NBA ML Prediction Pipeline]]"
  - "[[Odds API]]"
  - "[[Homelab]]"
tier: hot
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, dashboard, mlflow, pipeline-resilience, nba-ml-pipeline, dashboard-metrics, model-fallback]
checkpoint_class: durable-debugging
retention_mode: retain
knowledge_state: validated
---

# Copilot Session Checkpoint: Pipeline Resilience Fixes, Dashboard Metrics Investigation

## Summary

The user reported three dashboard issues: (1) props showing stale data from April 7 instead of today April 12 (fallback state), (2) hit rate discrepancy between props history P&L page and backtesting page, and (3) requested a deep dive on accuracy of metrics across the dashboard with fixes. Investigation revealed three cascading pipeline failures: missing ensemble model artifacts, MLflow DNS resolution failure during training, and Odds API 401 unauthorized errors. I'm implementing resilience fixes (model fallback loading, MLflow failover) and auditing dashboard metric computations.

## Key Points

- Diagnosed props fallback root cause (missing ensemble models → only pts+stl predictions)
- Diagnosed hit rate discrepancy (different bet populations, 100% agreement on same data)
- Diagnosed training failure (MLflow DNS resolution during container restart)
- Diagnosed prop fetching failure (Odds API 401 Unauthorized)
- Implemented predictor model fallback loading
- Implemented MLflow resilience in trainer

## Execution Snapshot

**Files created:**
- `tests/test_pipeline_resilience.py`: 9 tests for fallback loading, MLflow resilience, hit rate consistency

**Files modified:**
- `src/inference/predictor.py`: Added `_FALLBACK_ORDER` class variable and `_try_fallback_model()` method to Predictor class. When production model artifact is missing, tries CatBoost > XGBoost > LightGBM > Ridge from same stat directory. Called from `_load_production_models()` on artifact-not-found
- `src/training/trainer.py`: Added `_mlflow_available` flag and `_ensure_mlflow()` function that tests MLflow connectivity and falls back to local file tracking. Replaced 3 direct `mlflow.set_tracking_uri()` calls in `train_minutes_model()`, `train_pipeline()`, and classifier training

**Files deployed to container (hot-patched, not yet rebuilt):**
- `docker cp` of predictor.py and trainer.py to nba-ml-api container

**Work completed:**
- [x] Diagnosed props fallback root cause (missing ensemble models → only pts+stl predictions)
- [x] Diagnosed hit rate discrepancy (different bet populations, 100% agreement on same data)
- [x] Diagnosed training failure (MLflow DNS resolution during container restart)
- [x] Diagnosed prop fetching failure (Odds API 401 Unauthorized)
- [x] Implemented predictor model fallback loading
- [x] Implemented MLflow resilience in trainer
- [x] Wrote and passed 9 tests
- [x] Deployed fixes and generated 5,160 predictions for today
- [x] Verified dashboard now shows today's date (not fallback)
- [ ] Full dashboard metrics accuracy audit (IN PROGRESS — was beginning when compacted)
- [ ] Document/fix hit rate labeling discrepancy between history and backtest pages
- [ ] Git commit changes
- [ ] Rebuild Docker containers for permanent deployment
- [ ] Address Odds API 401 (user action needed)
- [ ] Trigger full retrain to get proper ensemble models
- [ ] Sprint report and lessons

Git state: On branch `fix/pipeline-resilience-dashboard-metrics`, uncommitted changes

## Technical Details

- Weekly retrain (Apr 12 16:00 UTC) failed at Step 1 because MLflow DNS couldn't resolve `nba-ml-mlflow` — container was restarting at that exact time. Training aborted with exit code 1 after 5m9s of retries
- Previous retrain (Apr 11) partially completed: saved base models (catboost, xgboost, etc.) for all stats but ensemble assembly (`ensemblemodel.pkl`) only succeeded for pts and fg3m. Likely OOM-killed during ensemble assembly (known: needs 14GB+)
- Odds API key returning 401 Unauthorized on all requests — no new prop lines from DK/FD sources since April 4-5. Only SGO sources still working (SGO_FD has 1 PRA line for today) **Model registry vs disk state:**
- DB `model_registry` table has `is_production=true` entries for ALL stats with valid artifact paths
- But on disk (`/app/models/` volume), only `pts/ensemblemodel.pkl` and `fg3m/ensemblemodel.pkl` exist
- All stats have their individual base models (catboostmodel.pkl, xgboostmodel.pkl, etc.) on disk
- stl's production model is CatBoostModel (not ensemble), so it was always working **Hit rate computation — two systems that agree:**
- History P&L: `prop_line_snapshots` (settled_at IS NOT NULL) + `prediction_blend` CTE → `result === modelDir` string comparison
- Backtest: `mv_backtest_summary` from `prop_lines + predictions + game_logs` → `(predicted > line AND actual > line) OR (predicted < line AND actual < line)`
- **THEY AGREE 100%** when computed on same data (tested on 6,328 overlapping rows). The ~1% overall difference (51.46% vs 52.52%) is purely from different bet populations (3,360 vs 9,483)
- History has fewer bets because it requires `prop_line_snapshots` with settlement; Backtest requires `game_logs` actual stats **Container networking:**
- nba-ml-scheduler is on `compose_default` network (NOT `nba-ml` network) — uses docker exec so this doesn't affect training DNS
- nba-ml-api and nba-ml-mlflow are both on `nba-ml,proxy` networks
- MLflow is reachable NOW (tested: HTTP 200), was transiently unavailable during training **Data state (April 12, 2026):**
- 14 games scheduled today
- 5,160 predictions for today (all 10 stats × 516 players + PRA)
- Only 1 prop line for today (PRA from SGO_FD)
- Prop sources: DK dead since Apr 4, FD dead since Apr 5, SGO_DK dead since Apr 10, SGO_FD working but sparse
- Backtest matview: 9,483 total bets, 52.5% overall hit rate **Key gotchas discovered:**
- `_ensure_mlflow()` needs `mlflow.search_experiments(max_results=1)` as connectivity check — `set_tracking_uri` alone doesn't make a network call
- The `prediction_blend` CTE (used in history endpoint) may produce different predicted values than raw `predictions` table (used in backtest)
- Prop line dedup differs: history uses `ROW_NUMBER() OVER (PARTITION BY player_id, game_date, stat_name ORDER BY ABS(predicted - line) ASC)` then JS dedup by player_name|stat_name|game_date keeping highest confidence; Backtest uses `DISTINCT ON (player_id, game_date, stat_name) ORDER BY ABS(predicted - line) ASC`
- BFF has 2-minute TTL cache on history endpoint, 5-minute cache on backtest **Unanswered questions:**
- Why did the Apr 11 training save ensemble.pkl for pts and fg3m but not for reb, ast, blk, tov? Was it OOM, timeout, or a bug in ensemble assembly?
- Is the Odds API key expired or quota exhausted? User needs to check/renew
- Should history and backtest use the same data source for consistency?
- What does `prediction_blend` CTE actually do vs raw predictions?

## Important Files

- `src/inference/predictor.py`
- Core prediction engine, loads models and generates predictions
- MODIFIED: Added `_FALLBACK_ORDER` list and `_try_fallback_model()` method after line 135
- Key: `_load_production_models()` (line 84-136), `_try_fallback_model()` (new, ~line 138-168), `predict_player()` (line ~170)

- `src/training/trainer.py`
- Training orchestrator for all models
- MODIFIED: Added `_mlflow_available` flag and `_ensure_mlflow()` function (lines ~44-67), replaced 3 `mlflow.set_tracking_uri()` calls at lines ~327, ~445, ~968
- Key: `_ensure_mlflow()` (new), `train_minutes_model()` (~line 325), `train_pipeline()` (~line 440), classifier training (~line 965)

- `tests/test_pipeline_resilience.py`
- CREATED: 9 tests covering fallback loading, MLflow resilience, hit rate consistency
- TestPredictorFallback (5 tests), TestMLflowResilience (2 tests), TestHitRateConsistency (2 tests)

- `dashboard-ui/server/src/index.ts` (~2000+ lines)
- BFF server with ALL dashboard API endpoints
- NOT YET MODIFIED but needs audit
- `getFeaturedPropSlate()` at line 308-332: determines which date to show
- `/api/props` at line 598-723: today's props
- `/api/props/history` at line 726-1070: history P&L with settlement from prop_line_snapshots
- `/api/backtest` at line 1336-1393: backtest from mv_backtest_summary
- `/api/dashboard` starting around line 367: overview with hit_rate_trend from mv_daily_hit_rates
- `PREDICTION_BLEND_CTE` and `PROP_CONFIDENCE_SQL` used throughout

- `scripts/optimize_db.py`
- Materialized view definitions including mv_backtest_summary
- Key for understanding backtest data computation

- `~/projects/homelab/compose/compose.nba-ml.yml`
- Docker compose with scheduler (Ofelia) cron jobs, volume mounts, network config
- Models volume: `${HOMELAB_BASE}/data/nba-ml/models:/app/models`
- Scheduler jobs: pipeline-daily (07:00 UTC), props-refresh (22:00 UTC), predict-refresh (22:15 UTC), weekly-retrain (Sunday 16:00 UTC)

## Next Steps

**Remaining work:**
1. **Full dashboard metrics audit** (was actively starting this) — need to check:
- `/api/dashboard` overview endpoint hit_rate_trend (uses mv_daily_hit_rates)
- `/api/prop-hit-rate` proxy endpoint
- Cross-check all hit rate computations across pages
- Verify PRA composite stat handling is correct everywhere
- Check if confidence scores are consistent across endpoints
- Check `PREDICTION_BLEND_CTE` vs raw predictions table
2. **Document/fix hit rate labeling** — the 51.46% vs 52.52% discrepancy is from different populations. Either:
- Add clear labels ("Settled Props: X%" vs "All Predictions: Y%")
- Or reconcile to use same data source
3. **Git commit** the predictor fallback and MLflow resilience changes
4. **Rebuild Docker containers** — currently hot-patched via docker cp, need proper rebuild
5. **Tell user about Odds API 401** — API key needs renewal/checking, this is why only 1 prop shows
6. **Trigger full retrain** — MLflow is back up, need to retrain to get proper ensemble models
7. **Sprint report** and lessons in tasks/lessons.md

**Immediate next actions:**
- Complete the dashboard metrics audit by reading all hit-rate-computing endpoints
- Query the dashboard overview endpoint to see what it returns
- Check if `PREDICTION_BLEND_CTE` adds any transformation vs raw predictions
- Git commit the working changes
- Present full findings to user with recommended actions (API key, retrain, labeling)

**Blockers:**
- Odds API 401 — user must check/renew API key for full prop line coverage
- Missing ensemble models — need full retrain (hours) for proper models; fallback is working but uses simpler models

## Related Wiki Pages

- [[Pipeline Resilience in Machine Learning Systems]]
- [[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]
- [[MLflow Resilience and Fallback Mechanisms in Model Training]]
- [[NBA ML Prediction Pipeline]]
- [[Odds API]]
- [[Homelab]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-pipeline-resilience-fixes-dashboard-metrics-inve-3ea0d6d8.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-04-12 |
| URL | N/A |
