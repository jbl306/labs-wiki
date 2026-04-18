---
title: "Copilot Session Checkpoint: Sprint 55 planning and exploration"
type: text
captured: 2026-04-18T01:37:38.386572Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard]
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint 55 planning and exploration
**Session ID:** `e9f38af4-e9d9-4c6f-b1e2-d74af067eaf0`
**Checkpoint file:** `/home/jbl/.copilot/session-state/e9f38af4-e9d9-4c6f-b1e2-d74af067eaf0/checkpoints/001-sprint-55-planning-and-explora.md`
**Checkpoint timestamp:** 2026-04-14T11:31:20.057788Z
**Exported:** 2026-04-18T01:37:38.386572Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user is running Sprint 55 of the NBA ML Engine project, implementing ALL items from the comprehensive ML review report (`docs/reports/comprehensive-ml-review_0413.md`). This is a massive sprint covering 7 critical issues, 12 high-priority improvements, 8 removals, and 8 additions. The approach is organized into 6 parallel workstreams (code cleanup, critical ML fixes, edge optimization, training pipeline, feature engineering, monitoring). We're on the server environment (hostname `beelink-gti13`) with direct access to nba-ml containers.
</overview>

<history>
1. User requested updating `docs/reports/comprehensive-ml-review_0413.md` after weekly training completed
   - Gathered training results from MLflow API (all 9 stats trained successfully April 14 03:46-05:58 UTC)
   - Queried production DB for 30-day hit rates via `mv_daily_hit_rates`
   - Found: Overall hit rate dropped 53.2% → 52.0% (below vig breakeven), PTS MAE improved 7.46 → 5.08, ECE worsened to 0.37-0.41
   - Made 11 surgical edits to the report: updated executive summary, hit rate table, resolved C5/ensemble status, updated C1/PTS diagnosis, updated H2/ECE, updated architecture grades, roadmap, key metrics, and summary
   - Key insight: calibration (not model accuracy) is now the #1 bottleneck

2. User requested committing and pushing changes
   - Committed as `7a91c67` on `main` branch with descriptive message
   - Pushed to `origin/main` successfully

3. User invoked `execute-sprint-from-report` skill to implement ALL items from the ML review
   - Loaded skill, confirmed server environment (beelink-gti13, containers local)
   - Determined this is Sprint 55 (latest was Sprint 54)
   - Created branch `feature/sprint-55-ml-review-implementation`
   - Ran data quality gate: 138 TZ mismatches (historical/known), 0 zero-lines, props fresh from April 13 — non-blocking
   - Launched two parallel explore agents to map the codebase
   - Created progress tracker at `tasks/PROGRESS-sprint55-ml-review-implementation-0414.md`
   - Created session plan at plan.md
   - Both explore agents completed with comprehensive results (see Technical Details)
   - **No implementation code has been written yet** — we were about to begin implementation when compaction occurred
</history>

<work_done>
Files updated:
- `docs/reports/comprehensive-ml-review_0413.md`: Updated with post-retrain metrics (committed + pushed to main as 7a91c67)
- `tasks/PROGRESS-sprint55-ml-review-implementation-0414.md`: Created progress tracker (uncommitted, on feature branch)

Work completed:
- [x] Update ML review report with post-retrain data
- [x] Commit and push report updates
- [x] Create sprint branch `feature/sprint-55-ml-review-implementation`
- [x] Run data quality gate (passed)
- [x] Deep codebase exploration (both agents completed)
- [x] Create progress tracker
- [x] Create implementation plan
- [ ] WS-A: Code cleanup & dead code removal (NOT STARTED)
- [ ] WS-B: Critical ML fixes (NOT STARTED)
- [ ] WS-C: Edge & threshold optimization (NOT STARTED)
- [ ] WS-D: Training pipeline improvements (NOT STARTED)
- [ ] WS-E: Feature engineering (NOT STARTED)
- [ ] WS-F: Monitoring & infrastructure (NOT STARTED)

Current state: On branch `feature/sprint-55-ml-review-implementation` (created from main at 7a91c67). Only the progress tracker file exists as uncommitted. All exploration is done — we have exact line numbers and patterns for every change needed. Ready to begin implementation.
</work_done>

<technical_details>
## Environment
- Hostname: `beelink-gti13` (server mode — operate directly)
- Containers: nba-ml-api, nba-ml-db, nba-ml-mlflow, nba-ml-scheduler, nba-ml-dashboard all running
- Env vars at `~/projects/homelab/.env`, deploy with `docker compose --env-file .env -f compose/compose.nba-ml.yml`
- Python 3.12, venv at `.venv/bin/python`, tests via `.venv/bin/python -m pytest`

## Current Production Model Metrics (April 14 retrain)
| Stat | MAE | R² | Features |
|------|-----|-----|----------|
| PTS | 5.084 | 0.500 | 308 |
| REB | 2.056 | 0.443 | 308 |
| AST | 1.502 | 0.503 | 308 |
| STL | 0.774 | 0.104 | 308 |
| BLK | 0.576 | 0.208 | 308 |
| TOV | 1.002 | 0.288 | 308 |
| FG3M | 0.968 | 0.321 | 308 |
| FG_PCT | 0.146 | 0.102 | 308 |
| FT_PCT | 0.207 | 0.063 | 308 |

## Current 30-Day Hit Rates
- Overall: 52.0% (BELOW 52.4% vig breakeven)
- STL: 64.9%, BLK: 55.4%, FG3M: 54.1%, AST: 51.9%, REB: 51.2%, PTS: 50.0%, PRA: 44.6%
- ECE: 0.3719 in-sample, 0.4055 OOS (3-day)

## Codebase Exploration Results (Critical Implementation Details)

### C2: Calibration Data Leakage (over_under_model.py:97-107)
- `CalibratedClassifierCV(xgb.XGBClassifier(**self.params), method="isotonic", cv=3)` trains on X_train, y_train
- Uses internal 3-fold CV which provides SOME protection, but the same data is used for both base model training and calibration fitting
- Fix: Reserve 20% held-out calibration set

### C3: XGBoost Early Stopping (xgboost_model.py:55-67)
- Line 61: `self.model.set_params(early_stopping_rounds=config.EARLY_STOPPING_ROUNDS)` — sets on model object
- Line 62: `fit_kwargs["eval_set"] = [(X_val, y_val)]` — eval_set IS passed to fit
- Line 67: `self.model.fit(X_train, y_train, **fit_kwargs)`
- NOTE: In newer XGBoost sklearn API, `set_params(early_stopping_rounds=...)` DOES work (it's a constructor param). Need to verify the XGBoost version to confirm if this is actually broken or if the report's concern is outdated.

### C4: Zero-Fill Locations
- `ensemble.py:140-147`: Per-model alignment fills missing cols with `0.0`
- `minutes_model.py:112-115`: Column-by-column `X[col] = 0`
- `predictor.py:270-279`: Global `X.fillna(0)` with logging
- `trainer.py:118-141`: `_smart_impute()` ALREADY does context-aware imputation (lag→ffill+0, rolling/EWMA→median, season→median, else→0). The issue is that predictor.py and ensemble.py don't use this smart imputation at inference time.

### Ensemble Weights (ensemble.py:95-105)
- Uses inverse-MAE from LAST fold only (most recent data)
- Fix: Average inverse-MAE across ALL folds

### Config Key Values
- `CLASSIFIER_STATS = ["stl", "blk", "fg3m", "reb", "tov"]` (line 155) — need to add "ast", "pts"
- `TARGET_STATS = ["pts", "reb", "ast", "stl", "blk", "tov", "fg_pct", "ft_pct", "fg3m"]` (line 73)
- `PIPELINE_SKIP_STATS = "fg_pct,ft_pct"` (line 117) — already skips these in pipeline mode
- `STALE_MODEL_DAYS = 30` (line 168)
- `MIN_EDGE_THRESHOLD = 0.005` (line 190), `MIN_CONFIDENCE_THRESHOLD = 0.55` (line 191)
- `ENSEMBLE_WEIGHT_MODE = "recent_performance"` (line 161)
- `EARLY_STOPPING_ROUNDS = 50` (line 93)

### Dead Code Removal Details
- **VIF Pruning** (config:136): Safe to remove. Entire `src/features/collinearity.py` (144 lines) + config flags + trainer.py:506-516 conditional. Tests at tests/test_analyze_features.py:122-195.
- **Target Encoding** (config:140): Safe to remove. builder.py:113-114 + builder.py:808-835. holdout_evaluator.py:42-45 references won't break.
- **B2B Fatigue** (config:143): ⚠️ REQUIRES CARE. minutes_model.py:36 hardcodes `b2b_second_game, b2b_fatigue, rest_category`. Must update minutes_model.py feature list BEFORE removing builder function.
- **Injury Return** (config:144): ⚠️ REQUIRES CARE. minutes_model.py:35 hardcodes `games_since_absence, is_ramping_up`. Same coordination needed.
- **Ridge Meta-Learner** (config:161): Ridge always trained (ensemble.py:92), prediction switches on ENSEMBLE_WEIGHT_MODE. Safe to remove the toggle and hardcode recent_performance.
- **Streamlit Dashboard** (dashboard/): 2 files (app.py 3272 lines, yahoo_fantasy.py 391 lines). Entirely dead — replaced by dashboard-ui/.

### Game Context Features (builder.py:1370-1430)
- `_add_game_line_features()` ALREADY EXISTS and adds: line_spread, line_total, line_implied_team_total
- opp_pace, team_pace, pace_x_usage interaction terms ALREADY EXIST
- A1 may already be mostly done — need to verify these features actually flow into PTS model predictions

### Training Pipeline (trainer.py)
- `_smart_impute()` at lines 118-141 — context-aware imputation exists for training but not inference
- `_register_best_model()` at lines 858-966 — 4 guardrails: degradation >10% MSE, negative R², hit rate < 52.4%, vig gate
- No `gc.collect()` calls exist. No parallel training implemented.
- Pipeline: Minutes → Stats → Classifiers → Calibration, wrapped in 12h timeout

### Calibration (calibration.py)
- `fit_per_stat_calibrators()` at lines 326-430: isotonic per stat, min 50 samples
- `refresh_calibrators()` at lines 479-570: 60-day rolling, queries predictions + snapshots
- Per-stat calibrators saved at `models/calibrators/per_stat/{stat}_calibrator.pkl`

### Edge Optimizer (edge_optimizer.py:145-200+)
- Sweeps 0-20% in 0.5% steps with walk-forward CV
- Kelly sizing with 25% fractional Kelly
- No stat-specific absolute edge CAPS exist (only minimums)

### Predictor Edge Filter (predictor.py:410-418)
- BOTH percentage AND absolute thresholds must pass
- `passes_edge_filter()` returns True only if `edge_pct >= pct_threshold AND edge_abs >= abs_threshold`

### OOM Issues
- predict-refresh and health-check both exit code 137 (OOM killed) — API container needs more memory for inference
- Training completed without OOM in ~9 hours

### PRA Stat
- `pra` appears in config.py:237 (STAT_LINE_FLOORS) and line 318 (some exclusion list) 
- Not in TARGET_STATS — it's a combo prop (Points+Rebounds+Assists) from SGO
- Shows 44.6% hit rate, dragging overall numbers — should be excluded or investigated

## Unresolved Questions
- Is XGBoost early stopping actually broken? `set_params()` works in newer sklearn API. Need to check XGBoost version.
- Should Ridge model (R2) be removed entirely or just the weight mode toggle (R7)? Report suggests removing Ridge but it may still contribute to ensemble diversity.
- PRA: Is it being bet on through prop matching, or just tracked? Need to check if it flows through predictions or just prop_lines.
</technical_details>

<important_files>
- `docs/reports/comprehensive-ml-review_0413.md`
   - Source of all sprint tasks, updated with post-retrain metrics
   - Already committed to main (7a91c67)

- `tasks/PROGRESS-sprint55-ml-review-implementation-0414.md`
   - Sprint progress tracker with all workstream checklists
   - Created but uncommitted on feature branch

- `config.py`
   - Central configuration: TARGET_STATS (line 73), CLASSIFIER_STATS (line 155), feature flags (lines 136-150), edge thresholds (lines 190-238), ENSEMBLE_WEIGHT_MODE (line 161), STALE_MODEL_DAYS (line 168)
   - Many changes needed: add AST/PTS to CLASSIFIER_STATS, remove dead flags, update thresholds

- `src/models/over_under_model.py`
   - Calibration data leakage at lines 97-107 (C2 fix)
   - Need held-out calibration set

- `src/models/xgboost_model.py`
   - Early stopping at lines 55-67 (C3 fix)
   - Need to verify if set_params actually works with current XGBoost version

- `src/models/ensemble.py`
   - Weight computation lines 95-105 (H6 fix — avg across all folds)
   - Zero-fill lines 140-147 (C4 fix)
   - Weight mode toggle lines 49, 165-170 (R7 simplify)
   - Ridge meta-learner line 92 (R2 evaluate)

- `src/models/minutes_model.py`
   - Feature list lines 22-38 — hardcodes b2b_fatigue and injury_return features (must update before R5/R6)
   - Zero-fill lines 107-116 (C4 fix)

- `src/inference/predictor.py`
   - Zero-fill at lines 270-279 (C4 fix — use smart imputation)
   - Edge filter at lines 410-418 (C7 — add caps; H12 — raise minimums)
   - Minutes gating needed (H5)
   - Confidence gating needed (H11)

- `src/training/trainer.py`
   - Smart impute lines 118-141 (need to extract for reuse at inference)
   - Model promotion lines 858-966
   - Pipeline orchestration lines 1069-1160 (H8 — add gc.collect)
   - VIF pruning import lines 506-516 (R3 remove)

- `src/features/builder.py`
   - Target encoding lines 113-114, 808-835 (R4 remove)
   - B2B fatigue lines 103-104, 838-867 (R5 remove)
   - Injury return lines 107-108, 904-960 (R6 remove)
   - Game context features lines 1370-1430 (A1 — already mostly exists)

- `src/features/collinearity.py`
   - Entire module (144 lines) — VIF pruning dead code (R3 remove entirely)

- `src/evaluation/calibration.py`
   - Per-stat calibrators lines 326-430
   - refresh_calibrators lines 479-570

- `src/evaluation/edge_optimizer.py`
   - Threshold sweep lines 145-200+ (C7 — add stat-specific caps)

- `dashboard/`
   - Old Streamlit dashboard (app.py 3272 lines, yahoo_fantasy.py 391 lines) — R8 remove entirely

- `src/notifications/dispatcher.py`
   - Existing notification infrastructure for A3 (hit rate alerting)
</important_files>

<next_steps>
## Remaining Work (ALL of Sprint 55 implementation)

### Immediate Next Steps (begin implementation):

1. **WS-A: Code Cleanup** (do first — reduces codebase before other changes):
   - Remove `dashboard/` directory (R8)
   - Remove VIF pruning: delete `src/features/collinearity.py`, remove config flags (config.py:136-137), remove conditional import (trainer.py:506-516), remove tests
   - Remove target encoding: delete function (builder.py:808-835), remove conditional call (builder.py:113-114), remove config flag (config.py:140)
   - Remove B2B fatigue: update minutes_model.py:36 FIRST to remove feature refs, then delete function (builder.py:838-867), remove config flag (config.py:143)
   - Remove injury return: update minutes_model.py:35 FIRST, then delete function (builder.py:904-960), remove config flag (config.py:144)
   - Simplify ensemble weight mode: remove ENSEMBLE_WEIGHT_MODE toggle, hardcode recent_performance (config.py:161, ensemble.py)
   - Remove FG_PCT/FT_PCT from TARGET_STATS (R1) — or just ensure PIPELINE_SKIP_STATS handles them
   - Evaluate Ridge model contribution (R2)

2. **WS-B: Critical ML Fixes**:
   - C2: Fix calibration in over_under_model.py — split X_train into train/calibration sets
   - C3: Verify XGBoost version and fix early stopping if needed
   - C4: Extract `_smart_impute()` from trainer.py for reuse in predictor.py and ensemble.py at inference time

3. **WS-C: Edge & Threshold Optimization**:
   - C7: Add stat-specific absolute edge CAPS (max edge) in predictor.py
   - H5: Add minutes gating in predictor.py (suppress if predicted_minutes < 15)
   - H10: Add "ast", "pts" to CLASSIFIER_STATS in config.py
   - H11: Add confidence gating in predictor.py (require P > 0.55)
   - H12: Consider raising edge minimums in config.py

4. **WS-D: Training Pipeline**:
   - H6: Fix ensemble weights to average across all CV folds (ensemble.py)
   - H8: Add gc.collect() between stats in trainer.py pipeline, consider float32
   - H9: Add hard cutoff at 45 days in predictor.py (fall back to baseline)

5. **WS-E: Feature Engineering**:
   - A1/C1: Verify game context features already flow into PTS predictions — they may already exist via builder.py

6. **WS-F: Monitoring & Infrastructure**:
   - C6: Check/renew Odds API key in homelab .env
   - A3: Add automated hit rate alerting to health-check command
   - H4: Add feature importance DB tracking post-training
   - A6: Add basic ML pipeline test suite

7. **Post-implementation**:
   - Run full test suite
   - Deploy to homelab
   - Verify predictions generate correctly
   - Write sprint results report
   - Update lessons.md
   - Create PR and merge

### Deferred to Sprint 56 (document in results report):
- H1: Per-stat model architecture redesign
- H2: Full recalibration (needs post-C2 retrain)
- H3: Walk-forward threshold validation
- H7: Prop source quality tracking
- A2: Prop line movement features (needs opening line data collection)
- A4: Per-player performance tracking
- A5: Live model monitoring dashboard
- A7: Model rollback mechanism
- A8: Bankroll management integration

### Blockers/Questions:
- Need to verify XGBoost version before deciding on C3 fix approach
- Need to check if PRA is being actively bet on or just tracked
- Odds API key status for C6 — need to check homelab .env
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
