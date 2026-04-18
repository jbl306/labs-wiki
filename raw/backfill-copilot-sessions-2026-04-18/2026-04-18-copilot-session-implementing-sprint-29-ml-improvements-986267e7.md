---
title: "Copilot Session Checkpoint: Implementing Sprint 29 ML improvements"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard]
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Implementing Sprint 29 ML improvements
**Session ID:** `e3ec590c-a745-4a37-8b1e-1c4d7ca88b89`
**Checkpoint file:** `/home/jbl/.copilot/session-state/e3ec590c-a745-4a37-8b1e-1c4d7ca88b89/checkpoints/002-implementing-sprint-29-ml-impr.md`
**Checkpoint timestamp:** 2026-03-27T11:29:20.793601Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user is executing a multi-sprint workflow for the NBA ML Engine project on their homelab server (beelink-gti13). Starting from Sprint 27's comprehensive ML review, they've completed Sprint 28 (critical ML fixes) and Sprint 29 (training, evaluation, and inference improvements). The work follows the "execute-sprint-from-report" skill workflow — implementing changes, testing, deploying to Docker on the homelab, verifying live, writing reports, and pushing to GitHub. Sprint 27 and 28 branches have been merged to main; Sprint 29 is committed but not yet pushed or merged.
</overview>

<history>
1. User asked to validate sections 1-2 of comprehensive ML review and create Sprint 27 remediation plan
   - Validated Section 1 (Data Pipeline): all 12 issues DONE (Sprint 16/18)
   - Validated Section 2 (Feature Engineering): all 7 issues DONE (Sprint 19/21/22)
   - Cataloged Sections 3-12: 1 done, 7 partial, 42 open
   - Created Sprint 27 report with 5-phase remediation roadmap
   - Committed and pushed branch `feature/sprint-27-ml-review-remediation-plan`

2. User asked to implement Phase 1 of remediation roadmap + fix dashboard duplicate predictions (Sprint 28)
   - Implemented 6 fixes: early stopping on GBMs, calibration leakage, Kelly bet sizing, zero-fill visibility, composite edge cap, dashboard dedup
   - All 168 tests passed, deployed to homelab, verified live
   - Wrote Sprint 28 report, committed, pushed, merged to main

3. User asked to implement high/medium/low priority items from Sprint 28 next steps (excluding retraining), and merge Sprint 27/28 branches to main (Sprint 29)
   - Merged Sprint 27 branch to main (Sprint 28 was already merged)
   - Created branch `feature/sprint-29-ml-training-and-evaluation`
   - Launched 5 parallel explore agents — 4 hit rate limits, 1 (apprise) succeeded
   - Manually explored codebase for all 8 work items
   - Installed apprise and shap dependencies
   - Implemented walk-forward CV model selection in trainer
   - Implemented Optuna with walk-forward CV folds
   - Added SHAP-based feature selection (with GBT fallback)
   - Created CLV tracker module and API endpoint
   - Added vig-adjusted hit rate to backtester
   - Created calibration analysis module and API endpoint
   - Added stale model detection to Predictor and /models endpoint
   - Confirmed prediction intervals already fully implemented (no changes needed)
   - All 186 tests pass (18 notification tests restored by apprise fix)
   - Built both Docker images with --no-cache
   - First deploy had 500 error on /models — missing `import config` in server.py
   - Fixed import, rebuilt API image, redeployed
   - Verified all endpoints live: /health, /models (with staleness), /evaluation/clv, /evaluation/calibration, dashboard dedup
   - Committed Sprint 29 code changes
   - Wrote Sprint 29 report at `docs/reports/sprint29-ml-training-and-evaluation.md`
   - **NOT YET**: progress tracker, lessons.md update, push to remote, merge to main
</history>

<work_done>
Files created (Sprint 29):
- `src/evaluation/clv_tracker.py`: CLV analysis module — joins predictions with settled prop_line_snapshots
- `src/evaluation/calibration.py`: Confidence calibration module — reliability diagrams, ECE, MCE
- `docs/reports/sprint29-ml-training-and-evaluation.md`: Sprint 29 report

Files modified (Sprint 29):
- `config.py`: Added `STALE_MODEL_DAYS = 30` and `USE_CV_MODEL_SELECTION = true`
- `requirements.txt`: Added `shap>=0.45.0`
- `src/training/trainer.py`: Walk-forward CV returns results dict, model selection uses cv_avg_val_mse, deferred registration, CV folds passed to tuner
- `src/training/tuner.py`: `tune_model()` accepts `cv_folds` param, objective averages MSE across folds
- `src/training/feature_selector.py`: Added `_get_shap_importances()` with TreeExplainer, fallback to GBT
- `src/evaluation/backtester.py`: Added `vig_adjusted_hit_rate`, `breakeven_hit_rate` to BacktestResult with implied probability computation
- `src/inference/predictor.py`: Stale model detection in `_load_production_models()` — checks age vs threshold, logs WARNING
- `src/api/server.py`: Added `import config`, ModelInfo with trained_at/age_days/is_stale, new `/evaluation/clv` and `/evaluation/calibration` endpoints

Files created (Sprint 28, already committed):
- `docs/reports/sprint28-critical-ml-fixes.md`
- `tasks/PROGRESS-sprint28-critical-ml-fixes-0327.md`

Work completed:
- [x] Sprint 27 & 28 branches merged to main
- [x] Walk-forward CV for model selection (M2)
- [x] Optuna with walk-forward CV folds (M4)
- [x] SHAP-based feature selection (M5)
- [x] CLV tracking + vig-adjusted hit rate (E2)
- [x] Confidence calibration analysis (E3)
- [x] Stale model detection (I2)
- [x] Prediction intervals in API (I3) — confirmed already implemented
- [x] Apprise dependency fix — 186/186 tests pass
- [x] Docker images built and deployed
- [x] All endpoints verified live
- [x] Sprint 29 code committed (`2ac0e4a`)
- [x] Sprint 29 report written
- [ ] Sprint 29 progress tracker not yet created
- [ ] lessons.md not yet updated for Sprint 29
- [ ] Sprint 29 branch not yet pushed to remote
- [ ] Sprint 29 branch not yet merged to main
</work_done>

<technical_details>
- **Environment**: Server mode on `beelink-gti13` (homelab). Python 3.12.3 via `.venv/bin/python`. XGBoost 3.2.0, LightGBM 4.6.0, CatBoost 1.2.10.
- **Walk-forward CV integration**: `_run_walk_forward_cv()` was refactored from `-> None` to `-> dict[str, dict[str, dict[str, float]]]` to return CV metrics. Model registration is deferred until after CV completes when `USE_CV_MODEL_SELECTION=true`. The `_register_best_model()` fallback chain is: `cv_avg_val_mse` → `val_mse` → `test_mse` → `train_mse`.
- **Optuna CV folds**: Tuner builds folds by calling `expanding_window_split(df)` in the trainer and constructing `(X_train, y_train, X_val, y_val)` tuples with `_smart_impute` applied. Passed as `cv_folds` to `tune_model()`.
- **SHAP**: Uses `shap.TreeExplainer` on a GradientBoostingRegressor. Subsamples to 500 rows for speed. Falls back to `feature_importances_` on any exception. Only applies to low-R² stats (stl, blk, fg_pct, ft_pct).
- **Missing import bug**: `/models` endpoint returned 500 because `server.py` didn't import `config`. Added `import config` to server.py imports. This required a second API image rebuild.
- **CLV live data**: 1,426 settled predictions, 58.2% hit rate, +$917.94 P&L, +6.4% ROI. Points (64.2% hit) and assists (58.7%) are strongest; blocks (51.3%) is underwater.
- **Calibration**: ECE=0.36 is high — edge-based confidence (|predicted - line| / line) doesn't map linearly to win probability. Classifier probability may be a better signal.
- **Prediction intervals**: Already fully implemented — quantile models in LightGBM/XGBoost, `predict_with_uncertainty()`, `confidence_low/high` in DB and API. No changes needed.
- **Stale model threshold**: `STALE_MODEL_DAYS = 30` (env configurable). Checks `entry.trained_at` with timezone awareness (handles naive datetimes by assuming UTC).
- **Homelab deployment**: Services built from `~/projects/homelab` with `--env-file .env -f compose/compose.nba-ml.yml`. API on port 8000, dashboard BFF on port 8501. Source context is `${NBA_ML_ENGINE_PATH}`.
- **SQL todo tracking**: Session DB has 10 todos, 8 done, 1 in_progress (sprint-report), 1 pending (sprint-report depends on tests-and-deploy which is done).
- **XGBoost 3.2.0 early stopping** (from Sprint 28): Must use `model.set_params(early_stopping_rounds=N)`, not fit() kwarg.
- **Dashboard dedup** (from Sprint 28): TS-level dedup with Set keyed by `player_name-stat_name`, SQL LIMIT 30 → slice to 10 after dedup.
</technical_details>

<important_files>
- `src/training/trainer.py`
   - Core training orchestrator. Walk-forward CV now returns metrics dict and drives model selection.
   - Changed `_run_walk_forward_cv()` return type, added CV fold construction for tuner, deferred model registration, updated `_register_best_model()` with cv_avg_val_mse support.
   - Key sections: lines ~420-440 (fold construction), ~555-580 (deferred registration), ~566-650 (CV function), ~652-730 (model selection)

- `src/training/tuner.py`
   - Optuna hyperparameter tuner. Now accepts cv_folds for multi-fold objective.
   - Added `cv_folds` parameter to `tune_model()`, updated objective function to average MSE across folds.

- `src/training/feature_selector.py`
   - Feature selection for low-R² stats. Now uses SHAP TreeExplainer with GBT fallback.
   - Added `_get_shap_importances()`, updated `select_features_for_stat()` and `get_feature_importance_report()`.

- `src/evaluation/clv_tracker.py` (NEW)
   - CLV analysis from settled prop_line_snapshots. `compute_clv()` returns daily P&L, per-stat breakdown, hit rate, ROI.

- `src/evaluation/calibration.py` (NEW)
   - Reliability diagram computation. `compute_calibration()` returns ECE, MCE, per-bin breakdown. `compute_calibration_from_backtest()` for integration.

- `src/evaluation/backtester.py`
   - Added vig-adjusted metrics: `breakeven_hit_rate`, `vig_adjusted_hit_rate` computed from American odds implied probability.

- `src/inference/predictor.py`
   - Stale model detection in `_load_production_models()`. Checks age vs `config.STALE_MODEL_DAYS`, logs WARNING.

- `src/api/server.py`
   - Added `import config`. ModelInfo extended with trained_at/age_days/is_stale. New endpoints: `/evaluation/clv`, `/evaluation/calibration`. Updated `/models` endpoint.

- `config.py`
   - Added `STALE_MODEL_DAYS = 30`, `USE_CV_MODEL_SELECTION = true`.

- `requirements.txt`
   - Added `shap>=0.45.0`.

- `docs/reports/sprint29-ml-training-and-evaluation.md` (NEW)
   - Sprint 29 report with all changes, validation, CLV findings, calibration observations, and next steps.

- `docs/reports/sprint28-critical-ml-fixes.md`
   - Sprint 28 report (committed in previous session segment).

- `docs/reports/sprint27-ml-review-remediation-plan.md`
   - Sprint 27 remediation roadmap — the source plan for Sprints 28-29.
</important_files>

<next_steps>
Remaining work:
1. **Create Sprint 29 progress tracker** — `tasks/PROGRESS-sprint29-ml-training-and-evaluation-0327.md`
2. **Update lessons.md** — Add lessons for: missing import config in server.py, SHAP subsample strategy, calibration ECE interpretation
3. **Commit docs** — Stage progress tracker and lessons, commit
4. **Push branch** — `git push -u origin feature/sprint-29-ml-training-and-evaluation`
5. **Merge to main** — `git checkout main && git merge feature/sprint-29-ml-training-and-evaluation && git push origin main`
6. **Update SQL todos** — Mark sprint-report as done

Immediate next action:
- Create progress tracker, update lessons.md, commit, push, and merge to main
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
