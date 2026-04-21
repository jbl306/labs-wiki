---
title: "Copilot Session Checkpoint: Sprint 13 Model Improvements Code"
type: source
created: 2026-03-23
last_verified: 2026-04-21
source_hash: "9583aca364f19d189456564e8242665d819c8e046298a36e6032014ff646bea6"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-13-model-improvements-code-5db17c4d.md
quality_score: 100
concepts:
  - minutes-prediction-sub-model
  - edge-threshold-optimizer-with-kelly-criterion
  - dynamic-ensemble-weighting
  - binary-over-under-classifier
related:
  - "[[Minutes Prediction Sub-Model]]"
  - "[[Dynamic Ensemble Weighting]]"
  - "[[MinutesModel]]"
  - "[[OverUnderClassifier]]"
  - "[[Edge Optimizer]]"
  - "[[EnsembleModel]]"
  - "[[Homelab]]"
  - "[[NBA ML Engine]]"
tier: archive
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard, nba, model improvements, sports betting, machine learning, xgboost, ensemble learning]
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: validated
---

# Copilot Session Checkpoint: Sprint 13 Model Improvements Code

## Summary

The user is building an NBA ML prediction engine with a React dashboard. This session focuses on Sprint 13 model improvements: creating a minutes prediction sub-model, edge threshold optimizer with Kelly criterion, dynamic ensemble weighting, and binary over/under classifiers. The approach is to implement all code changes first, skip training (weekly retrain runs tonight), then deploy, validate, and generate a sprint report.

## Key Points

- Phase 1: Minutes Prediction Sub-Model (1a through 1e code — 1f needs training)
- Phase 2: Edge Threshold Optimizer (2a, 2b, 2c, 2d code — 2e needs running)
- Phase 3: Dynamic Ensemble Weighting (3a, 3b, 3c code — 3d needs training comparison)
- Phase 4: Binary Over/Under Classifier (4a, 4b, 4c, 4d code — 4e needs eval)
- All imports validated working
- Prior context (from compaction): Built NBA ML Engine across sprints 9-12. Created React dashboard replacing Streamlit monolith. Fixed numerous deployment issues. Added Rankings page with 7 tabs. Optimized slow API endpoints by replacing LATERAL joins with regular JOINs (rankings: 22.5s→0.7s, backtest: 9s→0.19s). Added server-side TTL caching. All committed and deployed.

## Execution Snapshot

**Files created:**
- `src/models/minutes_model.py` (5,207 bytes) — MinutesModel class + get_minutes_feature_columns() helper
- `src/models/over_under_model.py` (9,077 bytes) — OverUnderClassifier + prepare_classifier_data()
- `src/evaluation/edge_optimizer.py` (8,210 bytes) — optimize_thresholds(), kelly_bet_size(), walk-forward CV

**Files modified:**
- `config.py` — Added 5 new config flags: USE_MINUTES_MODEL, USE_OVER_UNDER_CLASSIFIER, CLASSIFIER_STATS, ENSEMBLE_WEIGHT_MODE, USE_OPTIMIZED_THRESHOLDS + OPTIMIZED_EDGE_THRESHOLDS
- `src/models/ensemble.py` — Added weight_mode, performance_weights, inverse-MAE weighting, dual-mode predict(), updated save/load
- `src/training/trainer.py` — Added imports, train_minutes_model(), _register_minutes_model(), train_over_under_classifiers()
- `src/features/builder.py` — Added _add_predicted_minutes() function, called in build_features() before conditional groups
- `src/inference/predictor.py` — Added MinutesModel to _MODEL_CLASS_MAP, added get_edge_threshold() method

**Work completed:**
- [x] Phase 1: Minutes Prediction Sub-Model (1a through 1e code — 1f needs training)
- [x] Phase 2: Edge Threshold Optimizer (2a, 2b, 2c, 2d code — 2e needs running)
- [x] Phase 3: Dynamic Ensemble Weighting (3a, 3b, 3c code — 3d needs training comparison)
- [x] Phase 4: Binary Over/Under Classifier (4a, 4b, 4c, 4d code — 4e needs eval)
- [x] All imports validated working
- [ ] Phase 6: Training speed optimization (not started)
- [ ] Phase 5: Retrain, deploy, validate, report (blocked on retrain — runs tonight)

Current state: All code is written and import-validated. Docker container still has old code. Branch `feature/sprint-13-model-improvements` has NOT been committed yet.

## Technical Details

- Two repos: `homelab` (/home/jbl/projects/homelab) manages Docker compose; `nba-ml-engine` (/home/jbl/projects/nba-ml-engine) is the ML + dashboard codebase
- BFF pattern: Express server at dashboard-ui/server/ proxies some calls to FastAPI and queries PostgreSQL directly
- Docker: multi-stage build, port 8501, Caddy reverse proxy
- Python runs inside Docker container `nba-ml-api` — no local python available **Sprint 13 Design Decisions:**
- Minutes model trains FIRST since its predictions become features for stat models
- MinutesModel uses XGBoost with shallower trees (max_depth=5) and lower learning rate (0.03) — appropriate for the more predictable minutes target
- get_minutes_feature_columns() filters ~400 features down to ~40 minutes-relevant patterns (starter status, rest, pace, usage, game lines)
- Predicted minutes added as feature in builder.py via _add_predicted_minutes() — gracefully falls back to 0.0 if no production minutes model exists
- Edge optimizer uses walk-forward CV (not in-sample) to avoid overfitting thresholds — expanding window with n_folds=3
- Kelly criterion uses fractional Kelly (25%) for conservative sizing: f* = 0.25 * (bp - q) / b
- Dynamic ensemble: inverse-MAE weights computed from LAST fold only (most recent data) for recency bias
- OverUnderClassifier is NOT a BaseModel subclass — it's supplemental, takes regression predictions + line as extra features
- Isotonic calibration via CalibratedClassifierCV for better probability estimates **DB Schema Facts (learned hard way in prior sprints):**
- game_logs.player_id joins to players.id (auto-increment PK), NOT players.nba_api_id
- Column is players.active (not is_active)
- game_logs has no id column
- predictions has NO actual_value column — must JOIN game_logs with CASE expression
- pg NUMERIC/ROUND returns strings — must use numericRow() helper in BFF
- TimescaleDB doesn't support CONCURRENTLY in CREATE INDEX **Config flag locations in config.py:**
- USE_MINUTES_MODEL: line 123
- USE_OVER_UNDER_CLASSIFIER: line 126
- CLASSIFIER_STATS: line 128
- ENSEMBLE_WEIGHT_MODE: line 134
- USE_OPTIMIZED_THRESHOLDS: line 176 **Key Performance Data (from prior optimization):**
- Rankings: 22.5s → 0.7s → 1ms (cached)
- Backtest: 9s → 0.19s → 1ms (cached)
- Dashboard: 3.1s → 1.3s → 1ms (cached)
- Server-side cache: cached() helper with TTL in dashboard-ui/server/src/index.ts **Deployment:** ```bash cd /home/jbl/projects/homelab && docker compose -f compose/compose.nba-ml.yml --env-file .env build --no-cache nba-ml-dashboard && docker compose -f compose/compose.nba-ml.yml --env-file .env up -d nba-ml-dashboard ``` For API container: `docker compose -f compose/compose.nba-ml.yml --env-file .env build --no-cache nba-ml-api && up -d nba-ml-api` **Node.js:** v20.20.1 via nvm. Must source: `export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"` **Training pipeline concern:** User explicitly said training takes too long. Current: 9 stats × 6 models × Optuna tuning = many hours. Need to optimize: parallel stat training, lighter Optuna, smarter early stopping.

## Important Files

- `src/models/minutes_model.py` (NEW, 5.2KB)
- MinutesModel class for predicting player minutes
- get_minutes_feature_columns() filters to ~40 minutes-relevant features
- _MINUTES_FEATURE_PATTERNS defines which features are minutes-relevant

- `src/models/over_under_model.py` (NEW, 9KB)
- OverUnderClassifier — XGBoost binary classifier with isotonic calibration
- prepare_classifier_data() — joins features/predictions/prop_lines/actuals
- NOT a BaseModel subclass — supplemental to regression

- `src/evaluation/edge_optimizer.py` (NEW, 8.2KB)
- optimize_thresholds() — walk-forward CV threshold sweep per stat
- kelly_bet_size() — fractional Kelly (25%) position sizing
- format_optimized_thresholds() — converts results to config dict

- `src/models/ensemble.py` (MODIFIED)
- Added weight_mode ("ridge" vs "recent_performance")
- Added performance_weights (inverse-MAE from last fold)
- Dual-mode predict() — Ridge meta-learner or weighted average
- Updated save/load to persist new fields

- `src/training/trainer.py` (MODIFIED, ~730 lines)
- Added train_minutes_model() (~90 lines, before train_all)
- Added _register_minutes_model() helper
- Added train_over_under_classifiers() (~100 lines, after train_all)
- New imports: MinutesModel, OverUnderClassifier

- `src/features/builder.py` (MODIFIED, ~1350 lines)
- Added _add_predicted_minutes() function
- Called in build_features() before conditional feature groups
- Graceful fallback to 0.0 if no production minutes model exists

- `config.py` (MODIFIED, ~190 lines)
- Line 123: USE_MINUTES_MODEL
- Line 126: USE_OVER_UNDER_CLASSIFIER
- Line 128: CLASSIFIER_STATS
- Line 134: ENSEMBLE_WEIGHT_MODE
- Line 175-177: USE_OPTIMIZED_THRESHOLDS, OPTIMIZED_EDGE_THRESHOLDS

- `src/inference/predictor.py` (MODIFIED)
- Added MinutesModel to _MODEL_CLASS_MAP
- Added get_edge_threshold() method for optimized per-stat thresholds

- `dashboard-ui/server/src/index.ts` (~750 lines)
- Express BFF with cached() helper, all API endpoints
- LATERAL joins replaced with regular JOINs, server-side TTL cache

## Next Steps

**Immediate (was working on when compacted):**
1. **Phase 6: Training speed optimization** — Not yet started. Need to:
- Add parallel stat training via concurrent.futures.ProcessPoolExecutor
- Add `PIPELINE_MODE` config flag for lighter Optuna settings (fewer trials, shorter timeout)
- Add early termination in Optuna if no improvement for N trials
- Consider reducing walk-forward CV folds from 5 to 3 for pipeline mode
- Document training time estimates in config comments

2. **Run existing tests** to verify nothing is broken:
```bash
docker exec nba-ml-api python -m pytest tests/ -v
```

3. **Commit all Sprint 13 code** to the branch with descriptive message

4. **Deploy API container** (rebuild nba-ml-api with new code):
```bash
docker compose -f compose/compose.nba-ml.yml --env-file .env build --no-cache nba-ml-api && up -d nba-ml-api
```

5. **Validate deployment** — check API starts, imports work, no crashes

6. After tonight's retrain completes:
- Run holdout evaluation (5b)
- Run prop bet backtest (5c)
- Validate all dashboard endpoints (5d)
- Generate sprint 13 report (5e)
- Update docs (5f)

**SQL Todo Status:**
- 6 in_progress (1a, 1c, 2a, 3a, 4a, 6a)
- 1 blocked (5a-retrain-all — runs tonight)
- Remaining pending with dependencies
- Need to mark completed phases as done in SQL

## Related Wiki Pages

- [[Minutes Prediction Sub-Model]]
- [[Dynamic Ensemble Weighting]]
- [[MinutesModel]]
- [[OverUnderClassifier]]
- [[Edge Optimizer]]
- [[EnsembleModel]]
- [[Homelab]]
- [[NBA ML Engine]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-13-model-improvements-code-5db17c4d.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-23 |
| URL | N/A |
