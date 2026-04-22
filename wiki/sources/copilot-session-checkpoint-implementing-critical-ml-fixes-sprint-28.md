---
title: "Copilot Session Checkpoint: Implementing Critical ML Fixes Sprint 28"
type: source
created: 2026-03-27
last_verified: 2026-04-21
source_hash: "1544a9390c8a215aeb38b788d3103fd5a18163dc8ce9182c4c6fc36fbb638e43"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-implementing-critical-ml-fixes-sprint-28-9cff218d.md
quality_score: 90
concepts:
  - early-stopping-in-gradient-boosting-models
  - calibration-leakage-fix-in-machine-learning-pipelines
  - kelly-bet-sizing-bug-fix-in-sequential-betting-simulations
  - dashboard-duplicate-predictions-fix-in-ml-systems
related:
  - "[[Early Stopping in Gradient Boosting Models]]"
  - "[[Calibration Leakage Fix in Machine Learning Pipelines]]"
  - "[[Kelly Bet Sizing Bug Fix in Sequential Betting Simulations]]"
  - "[[Dashboard Duplicate Predictions Fix in ML Systems]]"
  - "[[NBA ML Engine]]"
  - "[[Homelab]]"
tier: archive
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard, betting, bug fixes, model training, calibration, machine learning, gradient boosting]
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: validated
---

# Copilot Session Checkpoint: Implementing Critical ML Fixes Sprint 28

## Summary

The user is implementing Phase 1 of the Prioritized Remediation Roadmap from Sprint 27 of the NBA ML Engine project, which addresses critical ML correctness issues identified in a comprehensive ML system review. The work covers 6 fixes: early stopping on gradient boosting models (M1), calibration leakage fix (M3), Kelly bet sizing bug (E1), zero-fill imputation visibility (I1), composite edge capping, and dashboard duplicate predictions fix. I'm following the "execute-sprint-from-report" skill workflow on the homelab server (beelink-gti13) in server mode.

## Key Points

- CRITICAL-M1: Early stopping on XGBoost, LightGBM, CatBoost
- CRITICAL-M3: Calibration leakage fix in OverUnderClassifier
- CRITICAL-E1: Kelly bet sizing bug fix
- I1: Zero-fill imputation now logs warnings (visibility fix)
- Composite edge capped at 1.0
- Dashboard duplicate predictions fix (SQL + TS dedup + React key)

## Execution Snapshot

**Files modified:**
- `src/models/xgboost_model.py`: Added `import config`, early stopping via `set_params(early_stopping_rounds=config.EARLY_STOPPING_ROUNDS)` for both main model and quantile models (when eval_set present)
- `src/models/lightgbm_model.py`: Added `import config`, early stopping via `lgb.early_stopping()` callback + `lgb.log_evaluation(period=0)` for both main and quantile models
- `src/models/catboost_model.py`: Added `import config`, early stopping via `fit_kwargs["early_stopping_rounds"]` for main model
- `src/models/over_under_model.py`: Fixed calibration leakage — changed from `combined_X/combined_y` (train+val) to `X_train/y_train` only. Removed `X_val is not None` guard (calibration now always uses 3-fold CV on train data)
- `src/evaluation/backtester.py`: Fixed Kelly sizing — added `kelly_bet_list` captured inside the sequential loop instead of post-loop recalculation using final bankroll
- `src/inference/predictor.py`: Replaced silent `fillna(0)` with logged imputation at 4 locations (`_align_frame_to_model_features`, `predict_player`, `predict_all_active`, `shadow_predict`). Added NaN counting, column identification, and percentage logging before zero-filling
- `src/applications/prop_finder.py`: Capped `abs_edge` at 1.0 before composite edge blending (`min(abs_edge, 1.0)`)
- `dashboard-ui/server/src/index.ts`: Increased SQL LIMIT from 10 to 30 for best_predictions query; added TypeScript dedup logic using Set to filter by `player_name-stat_name` key, then `.slice(0, 10)`
- `dashboard-ui/src/pages/DashboardPage.tsx`: Fixed React key to use index (`key={...idx}`) instead of `source` to prevent duplicate key warnings

**Files created (Sprint 27):**
- `docs/reports/sprint27-ml-review-remediation-plan.md`: Comprehensive remediation plan with validated sections 1-2 and 5-phase roadmap
- `tasks/PROGRESS-sprint27-ml-review-remediation-0327.md`: Sprint 27 progress tracker

**Work completed:**
- [x] CRITICAL-M1: Early stopping on XGBoost, LightGBM, CatBoost
- [x] CRITICAL-M3: Calibration leakage fix in OverUnderClassifier
- [x] CRITICAL-E1: Kelly bet sizing bug fix
- [x] I1: Zero-fill imputation now logs warnings (visibility fix)
- [x] Composite edge capped at 1.0
- [x] Dashboard duplicate predictions fix (SQL + TS dedup + React key)
- [x] 168/168 Python tests pass
- [x] TypeScript type-check passes
- [x] Docker images built (nba-ml-api, nba-ml-dashboard)
- [x] Containers deployed and running
- [ ] Live verification of dashboard dedup (in progress — API health OK, BFF endpoint needs retry)
- [ ] Sprint 28 report not yet written
- [ ] Git commit not yet made for sprint 28 changes
- [ ] Progress tracker for sprint 28 not yet created

## Technical Details

- **Environment**: Server mode on `beelink-gti13` (homelab). Python 3.12.3 via `.venv/bin/python`. XGBoost 3.2.0, LightGBM 4.6.0, CatBoost 1.2.10.
- **XGBoost 3.2.0 early stopping**: `early_stopping_rounds` is NOT a `fit()` kwarg anymore. Must use `model.set_params(early_stopping_rounds=N)` before calling `fit()`. The config value `EARLY_STOPPING_ROUNDS = 50` exists at config.py line 93.
- **LightGBM 4.6.0 early stopping**: Uses callback API: `lgb.early_stopping(N, verbose=False)` + `lgb.log_evaluation(period=0)` to suppress output.
- **CatBoost 1.2.10**: `early_stopping_rounds` works as a direct `fit()` kwarg (CatBoost parameter name).
- **Dashboard duplicates root cause**: `prediction_blend` CTE groups by `(player_id, game_date, stat_name)` producing 1 row per player/stat, but `prop_lines` table has 1 row per `(player_id, game_date, stat_name, source)`. The JOIN fans out when multiple sportsbooks have lines for the same player/stat. Fixed with TS-level dedup (simpler than SQL DISTINCT ON with complex template literals).
- **Calibration leakage**: The old code concatenated train+val data before fitting `CalibratedClassifierCV`. Fix: use only `X_train, y_train` with internal 3-fold CV. Removed the `X_val is not None` guard so calibration runs even without validation data.
- **Kelly bug**: `kelly_bet` column was recalculated AFTER the bankroll loop using `current_bankroll` (which at that point held the FINAL bankroll value). Fix: capture `bet_amount` in `kelly_bet_list` inside the loop.
- **Zero-fill approach**: Pragmatic — kept `fillna(0)` but added visibility via WARNING-level logging with NaN counts, percentages, and affected column names. Did NOT change behavior (breaking change risk too high for production). `_align_frame_to_model_features` now also logs when filling missing model-expected columns with 0.
- **Pre-existing test failure**: `tests/test_notifications.py` fails due to missing `apprise` module — not installed in the venv. This is unrelated to sprint 28 changes.
- **Homelab compose**: Services built from `~/projects/homelab` with `--env-file .env -f compose/compose.nba-ml.yml`. Source-built services: `nba-ml-api` (Dockerfile), `nba-ml-dashboard` (Dockerfile.dashboard-react). Build context is `${NBA_ML_ENGINE_PATH}` = `../../nba-ml-engine`.
- **Composite edge cap**: `abs_edge` can exceed 1.0 (e.g., predicted=50, line=10 → edge=400%). Capped at 1.0 before blending with classifier probability. Formula: `composite_edge = 0.6 * min(abs_edge, 1.0) + 0.4 * clf_directional`. SQL todo tracking in session DB:
- 9 todos created with dependencies: early-stopping, calibration-leakage, kelly-sizing, zero-fill, composite-edge-cap, dashboard-dupes (all DONE), tests (DONE), deploy (IN_PROGRESS), sprint-report (PENDING)

## Important Files

- `src/models/xgboost_model.py`
- XGBoost model with early stopping. Added `import config` and `set_params(early_stopping_rounds=...)` at lines ~58-62 (main) and ~87-91 (quantile)
- `src/models/lightgbm_model.py`
- LightGBM model with early stopping via callbacks. Lines ~54-60 (main) and ~82-88 (quantile)
- `src/models/catboost_model.py`
- CatBoost model with early stopping. Line ~51 added `early_stopping_rounds` to fit_kwargs
- `src/models/over_under_model.py`
- Binary classifier for prop bets. Calibration leakage fix at lines ~95-109. Changed from combined train+val to train-only
- `src/evaluation/backtester.py`
- Kelly bet sizing fix at lines ~425-450. `kelly_bet_list` captured inside loop
- `src/inference/predictor.py`
- Zero-fill visibility fix. `_align_frame_to_model_features` at lines ~56-73 logs missing columns. `predict_player` at ~132-142, `predict_all_active` at ~206-215, `shadow_predict` at ~441-449 all log NaN counts
- `src/applications/prop_finder.py`
- Composite edge cap at lines ~155-168. `min(abs_edge, 1.0)` before blending
- `dashboard-ui/server/src/index.ts`
- BFF dedup fix. SQL LIMIT 30 at line ~338. TS dedup filter at lines ~414-423 using Set
- `dashboard-ui/src/pages/DashboardPage.tsx`
- React key fix at line ~118. Uses index instead of source
- `docs/reports/sprint27-ml-review-remediation-plan.md`
- Sprint 27 report with full remediation roadmap. Validates sections 1-2, catalogs 42 open issues across sections 3-12
- `config.py`
- `EARLY_STOPPING_ROUNDS = 50` at line 93 (pre-existing, now used by all 3 GBM models)

## Next Steps

**Remaining work:**
1. **Verify dashboard dedup live** — The BFF overview endpoint curl failed to parse. Need to retry: `curl -s http://localhost:3080/api/overview | jq '.best_predictions | length'` and verify 0 duplicates
2. **Check container logs** — Verify both containers started cleanly: `docker logs nba-ml-api --tail 20` and `docker logs nba-ml-dashboard --tail 20`
3. **Verify composite edge cap** — Check `/prop-edges` endpoint for any `composite_edge > 1.0`
4. **Git commit sprint 28** — Stage all modified files, commit with descriptive message + Co-authored-by trailer
5. **Write sprint 28 report** — `docs/reports/sprint28-critical-ml-fixes.md` following repo sprint report style (title, date, branch, objective, executive summary, changes, validation, lessons, next steps)
6. **Create sprint 28 progress tracker** — `tasks/PROGRESS-sprint28-critical-ml-fixes-0327.md`
7. **Push branch** — `git push -u origin feature/sprint-28-critical-ml-fixes`
8. **Merge to main** — After verification, merge sprint 28 branch
9. **Update lessons.md** — Add lesson about XGBoost 3.2.0 early stopping API change

**Immediate next action:**
- Retry dashboard verification with proper curl/jq command
- Then proceed to commit, report, and push

## Related Wiki Pages

- [[Early Stopping in Gradient Boosting Models]]
- [[Calibration Leakage Fix in Machine Learning Pipelines]]
- [[Kelly Bet Sizing Bug Fix in Sequential Betting Simulations]]
- [[Dashboard Duplicate Predictions Fix in ML Systems]]
- [[NBA ML Engine]]
- [[Homelab]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-implementing-critical-ml-fixes-sprint-28-9cff218d.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-27 |
| URL | N/A |
