---
title: "Copilot Session Checkpoint: Sprint 11 Evaluation and Report"
type: source
created: 2026-03-22
last_verified: 2026-04-21
source_hash: "7947d08e9a063fe0b24b8984da65f96b90179927fffc01c1f05927569f503763"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-11-evaluation-and-report-5b560f0f.md
quality_score: 100
concepts:
  - holdout-evaluator-module-nba-ml-engine
  - lstm-gating-mechanism-nba-ml-engine
  - feature-alignment-for-feature-selection-models
related:
  - "[[LSTM Gating Mechanism in NBA ML Engine]]"
  - "[[Feature Alignment for Models with Feature Selection]]"
  - "[[NBA ML Engine]]"
  - "[[Durable Copilot Session Checkpoint]]"
  - "[[Homelab]]"
tier: archive
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard, machine-learning, evaluation, feature-alignment, lstm-gating]
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: validated
---

# Copilot Session Checkpoint: Sprint 11 Evaluation and Report

## Summary

The user requested a full Sprint 11 cycle for their NBA ML Engine project: create a branch, plan based on Sprint 10's next steps (priorities 1-5), implement evaluation infrastructure, deploy to homelab, run comprehensive backtesting/evaluation on all 9 stat categories, and generate a detailed report. The approach was: implement code changes (LSTM gating, holdout evaluator module, CLI command), deploy to Docker on the homelab server, run full evaluation on 25,884 test games, fix a feature alignment bug discovered during evaluation, re-run evaluation, run prop bet backtesting, and write a comprehensive sprint 11 report.

## Key Points

- Sprint 11 branch created (`feature/sprint-11-evaluation`)
- LSTM gating (USE_LSTM config flag)
- Holdout evaluator module with 3 evaluation modes
- CLI evaluate command
- 11 new tests (52 total passing)
- Deployed to homelab (Docker image rebuilt twice)

## Execution Snapshot

**Files created in nba-ml-engine repo:**
- `src/evaluation/holdout_evaluator.py` — 700+ line evaluation module (holdout metrics, calibration, permutation importance)
- `src/evaluation/__init__.py` — Package init (empty)
- `tests/test_evaluator.py` — 11 tests for evaluation dataclasses and formatting
- `tasks/PROGRESS-sprint11.md` — Sprint 11 progress tracker (completed)
- `docs/reports/sprint11-evaluation-calibration.md` — Sprint 11 report (245 lines)

**Files modified:**
- `config.py` — Added `USE_LSTM = os.getenv("USE_LSTM", "false").lower() == "true"`
- `src/training/trainer.py` — Added conditional LSTM import: `if config.USE_LSTM: from src.models.lstm_model import LSTMModel; MODEL_CLASSES.append(LSTMModel)`
- `main.py` — Added `evaluate` CLI command with 5 options, updated docstring

**Commits on `feature/sprint-11-evaluation`:**
- `f0f2a09` — Sprint 11: LSTM gating, holdout evaluator, CLI evaluate command
- `3f2fe90` — fix: align features for models trained with feature selection
- `9fdaafb` — docs: Sprint 11 evaluation report and progress tracker

**Work completed:**
- [x] Sprint 11 branch created (`feature/sprint-11-evaluation`)
- [x] LSTM gating (USE_LSTM config flag)
- [x] Holdout evaluator module with 3 evaluation modes
- [x] CLI evaluate command
- [x] 11 new tests (52 total passing)
- [x] Deployed to homelab (Docker image rebuilt twice)
- [x] Fixed feature alignment bug for feature-selected models
- [x] Full 9-stat holdout evaluation on 25,884 test games
- [x] Calibration analysis on production models
- [x] Feature group permutation importance analysis
- [x] Backtest analysis (1,355 bets)
- [x] Sprint 11 report written
- [x] All pushed to GitHub
- [ ] Create PR and merge to main
- [ ] Final deploy from merged main
- [ ] Update lessons.md if applicable

Current state: Branch `feature/sprint-11-evaluation` has 3 commits pushed to origin. API is running the fixed code (built from branch). All evaluation data collected and report written. Just need PR → merge → final deploy.

## Technical Details

- **Two repos**: homelab (`/home/jbl/projects/homelab`) manages Docker compose; nba-ml-engine (`/home/jbl/projects/nba-ml-engine`) is the ML codebase
- **Docker compose invocation**: `docker compose -f compose/compose.nba-ml.yml --env-file .env` from homelab dir
- **Feature alignment bug**: Models trained with feature selection (stl: 246/383, blk: 200/383, fg_pct: 236/383, ft_pct: 248/383) expect only their selected feature columns. XGBoost/LightGBM/Ridge/RF error on wrong feature count, but CatBoost handles extra features internally. Fixed with `_align_features()` that filters X to `model.feature_names`.
- **Feature matrix**: 95,271 rows × 417 columns (383 feature columns). Test set: 25,884 rows.
- **Data split**: train: 56,924 (<2023-10-24), val: 12,463 (2023-10-24..2024-10-22), test: 25,884 (>=2024-10-22)
- **Evaluation performance optimization**: `run_full_evaluation` builds features once and passes via `_prebuilt` parameter to avoid 3× rebuild (~60s each)
- **Calibration method**: Uses residual-based percentiles from `calibrate_intervals()`. Coverage at q10-q90 empirically matches ~80% for most stats.
- **Permutation importance**: Shuffles all features in a group simultaneously, measures MSE increase. 3 repeats averaged. All Sprint 10 feature groups show <0.3% importance — marginal.
- **Backtest uses stored predictions**: The backtester compares predictions from the `predictions` table against `game_logs` actuals and `prop_lines`. It does NOT rebuild features.
- **BLK/FG_PCT/FT_PCT have no production model in registry** — calibration/importance limited to stats with registered production models. These need re-registration after next retrain.
- **LSTM model files still exist on disk** (lstmmodel.pkl ~1.6MB each × 9 stats) but LSTM is not in MODEL_CLASSES and USE_LSTM defaults to false
- **Server**: beelink-gti13, Ubuntu 22.04, user jbl. Docker containers: nba-ml-db, nba-ml-mlflow, nba-ml-api, nba-ml-dashboard, nba-ml-scheduler
- **Killing Docker processes**: Container lacks `kill` binary. Use `docker exec python -c "import os; os.kill(PID, 9)"` instead Key evaluation findings:
- Strong predictors: pts (R²=0.508), ast (R²=0.506), reb (R²=0.449)
- Moderate: fg3m (R²=0.325), tov (R²=0.293)
- Weak: blk (R²=0.215), stl (R²=0.106), fg_pct (R²=0.099), ft_pct (R²=0.061)
- Calibration: 5/6 well-calibrated, STL under-calibrated at 76.8%
- Prop betting alpha: BLK (68.6%), STL (66.7%), FG3M (56.0%); PTS/AST losing (46.9%)
- Feature groups: minutes_trend (+0.26% for ast), matchup (+0.12% for reb) show most signal; target_encoding/injury_return/b2b_fatigue show no signal

## Important Files

- `/home/jbl/projects/nba-ml-engine/src/evaluation/holdout_evaluator.py`
- Core Sprint 11 deliverable — 700+ line evaluation module
- 3 modes: `evaluate_holdout()`, `evaluate_calibration()`, `evaluate_feature_groups()`
- `_align_features()` helper (critical fix for feature-selected models)
- `_prebuilt` parameter optimization to avoid rebuilding features 3×
- `format_report_table()` for CLI output, `save_report_json()` for programmatic use
- FEATURE_GROUPS dict defines Sprint 10's 6 feature groups for permutation importance

- `/home/jbl/projects/nba-ml-engine/config.py`
- Added `USE_LSTM` flag at line ~118 (after USE_WARMSTART)
- All config flags: USE_WALK_FORWARD_CV, USE_QUANTILE_REGRESSION, USE_OPTUNA, USE_RECENCY_WEIGHTS, USE_FEATURE_SELECTION, USE_TARGET_ENCODING, USE_WARMSTART, USE_LSTM

- `/home/jbl/projects/nba-ml-engine/src/training/trainer.py`
- MODEL_CLASSES defined at lines 68-75 (6 models, no LSTM)
- Conditional LSTM append at lines 77-79 (if config.USE_LSTM)
- `_smart_impute()` used by evaluator (imported)

- `/home/jbl/projects/nba-ml-engine/main.py`
- `evaluate` CLI command added after `prune` command (~line 298)
- Options: --stat, --production-only, --no-importance, --no-calibration, --save-json

- `/home/jbl/projects/nba-ml-engine/docs/reports/sprint11-evaluation-calibration.md`
- Sprint 11 report (245 lines) with holdout results, calibration, feature importance, backtest, next steps

- `/home/jbl/projects/nba-ml-engine/tests/test_evaluator.py`
- 11 tests covering StatEvalResult, CalibrationResult, FormatReportTable, FeatureGroupImportance

- `/home/jbl/projects/nba-ml-engine/src/evaluation/backtester.py`
- Pre-existing backtester (562 lines) — used for prop bet P&L analysis
- Uses stored predictions from DB, not feature rebuilding

- `/home/jbl/projects/nba-ml-engine/src/training/splitter.py`
- `expanding_window_split()` — walk-forward CV already implemented
- `date_split()` — current default split mode

- `/home/jbl/projects/homelab/compose/compose.nba-ml.yml`
- Docker compose for NBA ML stack (not modified in Sprint 11)

## Next Steps

**Remaining work:**
1. **Create PR and merge** — `gh pr create` for `feature/sprint-11-evaluation`, then merge to main
2. **Final deploy from main** — Rebuild Docker image from merged main, restart container
3. **Verify services healthy** — curl health endpoints
4. **Update SQL todos to done** — Mark c1-report, c2-progress, c3-pr-merge as done
5. **Mark task complete** — Call task_complete with summary

**Immediate next action:**
- Run `cd /home/jbl/projects/nba-ml-engine && gh pr create --title "Sprint 11: Evaluation, Calibration & Pipeline Hardening" --body "..." --base main`
- Then `gh pr merge <PR#> --merge --delete-branch`
- Rebuild API image from main: `cd /home/jbl/projects/homelab && docker compose -f compose/compose.nba-ml.yml --env-file .env build --no-cache nba-ml-api`
- Restart and verify

## Related Wiki Pages

- [[LSTM Gating Mechanism in NBA ML Engine]]
- [[Feature Alignment for Models with Feature Selection]]
- [[NBA ML Engine]]
- [[Durable Copilot Session Checkpoint]]
- [[Homelab]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-11-evaluation-and-report-5b560f0f.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-22 |
| URL | N/A |
