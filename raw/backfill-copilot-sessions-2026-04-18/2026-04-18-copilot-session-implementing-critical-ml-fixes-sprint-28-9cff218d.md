---
title: "Copilot Session Checkpoint: Implementing critical ML fixes sprint 28"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard]
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Implementing critical ML fixes sprint 28
**Session ID:** `e3ec590c-a745-4a37-8b1e-1c4d7ca88b89`
**Checkpoint file:** `/home/jbl/.copilot/session-state/e3ec590c-a745-4a37-8b1e-1c4d7ca88b89/checkpoints/001-implementing-critical-ml-fixes.md`
**Checkpoint timestamp:** 2026-03-27T00:53:21.332780Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user is implementing Phase 1 of the Prioritized Remediation Roadmap from Sprint 27 of the NBA ML Engine project, which addresses critical ML correctness issues identified in a comprehensive ML system review. The work covers 6 fixes: early stopping on gradient boosting models (M1), calibration leakage fix (M3), Kelly bet sizing bug (E1), zero-fill imputation visibility (I1), composite edge capping, and dashboard duplicate predictions fix. I'm following the "execute-sprint-from-report" skill workflow on the homelab server (beelink-gti13) in server mode.
</overview>

<history>
1. User asked to execute sprint skill for Sprint 27 — validate sections 1-2 of comprehensive ML review, create new sprint report
   - Read comprehensive-ml-review_0324.md (719 lines, 12 sections covering all system layers)
   - Launched 3 parallel explore agents to validate Section 1 (Data Pipeline), Section 2 (Feature Engineering), and Sections 3-12
   - Section 1: All 12 issues confirmed DONE (Sprint 16 primary, Sprint 18 QA enhancements)
   - Section 2: All 7 issues confirmed DONE (Sprint 19 primary, Sprint 21/22 follow-ups)
   - Sections 3-12: 1 done (I2 classifier fix in Sprint 26), 7 partial, 42 open
   - Created Sprint 27 report at docs/reports/sprint27-ml-review-remediation-plan.md with 5-phase roadmap
   - Created progress tracker at tasks/PROGRESS-sprint27-ml-review-remediation-0327.md
   - Committed and pushed to branch `feature/sprint-27-ml-review-remediation-plan`

2. User asked to implement Phase 1 of the remediation roadmap + fix dashboard duplicate predictions
   - Created branch `feature/sprint-28-critical-ml-fixes` from main
   - Launched 6 parallel explore agents to investigate all code changes needed
   - Set up SQL todo tracking for 9 tasks with dependencies
   - Implemented all 6 fixes (details below)
   - Fixed XGBoost early stopping: `early_stopping_rounds` must be set via `set_params()` on XGBoost 3.2.0 (not fit kwargs)
   - Fixed indentation error in predictor.py where edit accidentally consumed the for-loop header
   - All 168 Python tests pass (excluding pre-existing `test_notifications.py` failure due to missing `apprise` module)
   - TypeScript type-check passes clean
   - Built both Docker images (`nba-ml-api`, `nba-ml-dashboard`) with `--no-cache`
   - Deployed containers successfully
   - API health check returns `{"status":"ok"}`
   - Dashboard overview endpoint verification in progress (JSON parsing issue with curl output, needs retry)
</history>

<work_done>
Files modified:
- `src/models/xgboost_model.py`: Added `import config`, early stopping via `set_params(early_stopping_rounds=config.EARLY_STOPPING_ROUNDS)` for both main model and quantile models (when eval_set present)
- `src/models/lightgbm_model.py`: Added `import config`, early stopping via `lgb.early_stopping()` callback + `lgb.log_evaluation(period=0)` for both main and quantile models
- `src/models/catboost_model.py`: Added `import config`, early stopping via `fit_kwargs["early_stopping_rounds"]` for main model
- `src/models/over_under_model.py`: Fixed calibration leakage — changed from `combined_X/combined_y` (train+val) to `X_train/y_train` only. Removed `X_val is not None` guard (calibration now always uses 3-fold CV on train data)
- `src/evaluation/backtester.py`: Fixed Kelly sizing — added `kelly_bet_list` captured inside the sequential loop instead of post-loop recalculation using final bankroll
- `src/inference/predictor.py`: Replaced silent `fillna(0)` with logged imputation at 4 locations (`_align_frame_to_model_features`, `predict_player`, `predict_all_active`, `shadow_predict`). Added NaN counting, column identification, and percentage logging before zero-filling
- `src/applications/prop_finder.py`: Capped `abs_edge` at 1.0 before composite edge blending (`min(abs_edge, 1.0)`)
- `dashboard-ui/server/src/index.ts`: Increased SQL LIMIT from 10 to 30 for best_predictions query; added TypeScript dedup logic using Set to filter by `player_name-stat_name` key, then `.slice(0, 10)`
- `dashboard-ui/src/pages/DashboardPage.tsx`: Fixed React key to use index (`key={...idx}`) instead of `source` to prevent duplicate key warnings

Files created (Sprint 27):
- `docs/reports/sprint27-ml-review-remediation-plan.md`: Comprehensive remediation plan with validated sections 1-2 and 5-phase roadmap
- `tasks/PROGRESS-sprint27-ml-review-remediation-0327.md`: Sprint 27 progress tracker

Work completed:
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
</work_done>

<technical_details>
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
- **Composite edge cap**: `abs_edge` can exceed 1.0 (e.g., predicted=50, line=10 → edge=400%). Capped at 1.0 before blending with classifier probability. Formula: `composite_edge = 0.6 * min(abs_edge, 1.0) + 0.4 * clf_directional`.

SQL todo tracking in session DB:
- 9 todos created with dependencies: early-stopping, calibration-leakage, kelly-sizing, zero-fill, composite-edge-cap, dashboard-dupes (all DONE), tests (DONE), deploy (IN_PROGRESS), sprint-report (PENDING)
</technical_details>

<important_files>
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
</important_files>

<next_steps>
Remaining work:
1. **Verify dashboard dedup live** — The BFF overview endpoint curl failed to parse. Need to retry: `curl -s http://localhost:3080/api/overview | jq '.best_predictions | length'` and verify 0 duplicates
2. **Check container logs** — Verify both containers started cleanly: `docker logs nba-ml-api --tail 20` and `docker logs nba-ml-dashboard --tail 20`
3. **Verify composite edge cap** — Check `/prop-edges` endpoint for any `composite_edge > 1.0`
4. **Git commit sprint 28** — Stage all modified files, commit with descriptive message + Co-authored-by trailer
5. **Write sprint 28 report** — `docs/reports/sprint28-critical-ml-fixes.md` following repo sprint report style (title, date, branch, objective, executive summary, changes, validation, lessons, next steps)
6. **Create sprint 28 progress tracker** — `tasks/PROGRESS-sprint28-critical-ml-fixes-0327.md`
7. **Push branch** — `git push -u origin feature/sprint-28-critical-ml-fixes`
8. **Merge to main** — After verification, merge sprint 28 branch
9. **Update lessons.md** — Add lesson about XGBoost 3.2.0 early stopping API change

Immediate next action:
- Retry dashboard verification with proper curl/jq command
- Then proceed to commit, report, and push
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
