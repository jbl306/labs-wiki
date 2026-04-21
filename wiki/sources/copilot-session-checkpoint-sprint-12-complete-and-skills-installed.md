---
title: "Copilot Session Checkpoint: Sprint 12 Complete and Skills Installed"
type: source
created: 2026-03-22
last_verified: 2026-04-21
source_hash: "9abff5d56824e0f4fae96781e1391fb0dbad2aaf59efa4bd9dfe557ce4eed23d"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-12-complete-and-skills-installed-48a02b58.md
quality_score: 100
concepts:
  - sprint-12-nba-ml-engine-code-cleanup-feature-tuning
  - per-stat-calibration-fixes-residual-persistence-model-save-load
  - walk-forward-stability-analysis-backtesting-nba-ml-engine
  - nodejs-installation-nvm-global-taste-skill-installation
related:
  - "[[Sprint 12 NBA ML Engine Code Cleanup and Feature Tuning]]"
  - "[[Per-Stat Calibration Fixes and Residual Persistence in Model Save/Load]]"
  - "[[Walk-Forward Stability Analysis and Backtesting in NBA ML Engine]]"
  - "[[Node.js Installation via nvm and Global Taste-Skill Package Installation]]"
  - "[[NBA ML Engine]]"
  - "[[Node Version Manager (nvm)]]"
  - "[[Taste-Skill Package]]"
  - "[[Homelab]]"
tier: archive
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard, nba, machine-learning, feature-engineering, skill-installation, nodejs, model-calibration, ai-agents]
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: validated
---

# Copilot Session Checkpoint: Sprint 12 Complete and Skills Installed

## Summary

The user requested a full Sprint 12 cycle for their NBA ML Engine project: plan from Sprint 11's 6 priorities, implement code cleanup (LSTM removal, feature pruning, prop bet filtering, calibration fixes), deploy to homelab Docker, retrain models, run comprehensive evaluation/backtesting, and generate a detailed report. Additionally, the user asked to install Node.js via nvm and add the taste-skill package globally via npx. The approach was: implement code changes in phases, deploy iteratively to Docker, retrain affected models, run evaluation and walk-forward analysis, write a comprehensive report, merge via PR, and handle the skill installation.

## Key Points

- Sprint 12 branch created and merged (PR #10)
- LSTM fully removed from codebase
- Feature groups made individually tunable via config flags
- PTS/AST excluded from prop bets
- Per-stat calibration percentiles (STL q7/q93, BLK q8/q92)
- Residuals persisted in all model save/load methods

## Execution Snapshot

**Files created in nba-ml-engine repo:**
- `docs/reports/sprint12-cleanup-tuning.md` — 344-line Sprint 12 report with holdout eval, walk-forward, backtest, analysis per category, 6 next-step priorities

**Files modified:**
- `config.py` — Removed USE_LSTM; added USE_B2B_FATIGUE, USE_INJURY_RETURN, USE_MINUTES_TREND, USE_SEASON_PHASE, USE_MATCHUP; changed USE_TARGET_ENCODING default to false; updated EXCLUDED_PROP_STATS to include pts,ast; added STAT_CALIBRATION_PERCENTILES
- `src/features/builder.py` — Gated all 6 feature groups behind individual config flags
- `src/models/base.py` — calibrate_intervals() accepts stat_name for per-stat overrides
- `src/models/{catboost,xgboost,lightgbm,random_forest,ridge}_model.py` and `src/models/ensemble.py` — All 6 models now persist `_residuals` array in save/load
- `src/training/trainer.py` — Removed LSTM conditional import, passes stat_name to calibrate_intervals
- `src/inference/predictor.py` — Removed LSTM import and class map entry
- `dashboard/app.py` — Removed LSTM model family mapping
- `README.md` — Removed LSTM refs, added CatBoost, updated test count, added feature flags to config table

**Files deleted:**
- `src/models/lstm_model.py` — 309 lines removed entirely

**Commits on main (merged via PR #10):**
- `46679db` — Sprint 12: remove LSTM, tunable feature groups, filter PTS/AST props
- `1b3b1fe` — fix: per-stat calibration percentiles, persist residuals in all models
- `7451709` — docs: Sprint 12 report, README updates

**System changes:**
- nvm installed at `~/.nvm` with Node.js v20.20.1
- 7 taste-skills installed globally at `~/.agents/skills/`

**Work completed:**
- [x] Sprint 12 branch created and merged (PR #10)
- [x] LSTM fully removed from codebase
- [x] Feature groups made individually tunable via config flags
- [x] PTS/AST excluded from prop bets
- [x] Per-stat calibration percentiles (STL q7/q93, BLK q8/q92)
- [x] Residuals persisted in all model save/load methods
- [x] BLK, FG_PCT, STL retrained with updated features
- [x] All 9 production models registered
- [x] Full holdout evaluation on 25,998 test games
- [x] Walk-forward stability analysis (4 folds × 9 stats)
- [x] Prop bet backtest with PTS/AST excluded
- [x] Sprint 12 report written
- [x] README and docs updated
- [x] PR #10 merged, final deploy from main
- [x] Node.js 20 installed via nvm
- [x] 7 taste-skills installed globally
- [ ] find-skills prompt still pending (interactive shell still open)

Current state: API running on main with all Sprint 12 changes. 9 models loaded. All evaluation data collected.

## Technical Details

- **Two repos**: homelab (`/home/jbl/projects/homelab`) manages Docker compose; nba-ml-engine (`/home/jbl/projects/nba-ml-engine`) is the ML codebase
- **Docker compose invocation**: `docker compose -f compose/compose.nba-ml.yml --env-file .env` from homelab dir
- **Target column naming**: Targets are `next_pts`, `next_reb`, etc. — NOT `pts_target`. This caused an empty walk-forward result on first attempt.
- **Feature matrix**: 95,385 rows × 406 columns (was 417, reduced by 11 dead features). Test set: 25,998 rows (2024-10-22 to 2026-03-21).
- **Calibration bug discovered**: All 6 model save/load methods only persisted `_residual_lower`/`_residual_upper` but NOT the `_residuals` array. This meant `predict_probability()` (which uses the full residual distribution) failed after model reload. Fixed by adding `"residuals": getattr(self, "_residuals", None)` to all save dicts and `self._residuals = data.get("residuals")` to all load methods.
- **Per-stat calibration**: `STAT_CALIBRATION_PERCENTILES` dict in config.py maps stat names to (lower_pct, upper_pct) tuples. `calibrate_intervals()` in base.py checks this dict when `stat_name` is provided.
- **Walk-forward performance**: Ridge is fast enough for walk-forward (4 folds × 9 stats in ~2min). GBM was too heavy and died. The expanding_window_split produces folds from 2017-18 through 2025-26.
- **Production model detection in evaluator**: The evaluator's production model flag only matches models that existed in registry before the current API startup. Newly retrained models show `is_production=false` in eval output even though they're registered. This is cosmetic — the holdout metrics are still valid.
- **Prop bet improvement**: Excluding PTS/AST improved hit rate from 53.1% → 57.0% and ROI from -8.6% → -5.0%. BLK (68.6%) and STL (66.7%) are the strongest alpha generators.
- **STL calibration**: Widening from q10/q90 to q7/q93 improved coverage from 76.8% → 80.3%. STL's discrete nature (0-3 values) means standard percentiles underestimate variance.
- **nvm installation**: No sudo needed. Installed at `~/.nvm`, Node.js v20.20.1, npm v10.8.2. Must source nvm before use: `export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"`
- **Server**: beelink-gti13, Ubuntu 22.04, user jbl. Docker containers: nba-ml-db, nba-ml-mlflow, nba-ml-api, nba-ml-dashboard, nba-ml-scheduler
- **Model training time**: ~1-2hrs per stat (6 models + walk-forward CV each)
- **Feature groups disabled (no signal)**: b2b_fatigue (3 features), injury_return (2 features), target_encoding (6 features) = 11 total
- **Feature groups enabled (marginal signal)**: minutes_trend (3), season_phase (2), matchup (4) Key evaluation findings (Sprint 12):
- Strong: pts (R²=0.506), ast (R²=0.504), reb (R²=0.447)
- Moderate: fg3m (R²=0.322), tov (R²=0.288)
- Weak: blk (R²=0.215), stl (R²=0.107), fg_pct (R²=0.099), ft_pct (R²=0.061)
- R² stable vs Sprint 11 (removing dead features had negligible impact)
- AST showing declining trend in walk-forward (0.547→0.499) — possible regime change

## Important Files

- `/home/jbl/projects/nba-ml-engine/config.py`
- Central configuration hub for all flags
- Sprint 12: Removed USE_LSTM, added 5 feature group flags, STAT_CALIBRATION_PERCENTILES, updated EXCLUDED_PROP_STATS
- Feature flags around lines 112-123, calibration percentiles around lines 128-134, prop config around lines 147-156

- `/home/jbl/projects/nba-ml-engine/src/features/builder.py`
- Feature matrix assembly (~950 lines)
- Sprint 12: Lines 96-107 gated all 6 feature groups behind config flags
- `build_features()` is the main entry point, calls `_add_*` functions conditionally

- `/home/jbl/projects/nba-ml-engine/src/models/base.py`
- Base class for all models, defines calibrate_intervals() and predict_with_uncertainty()
- Sprint 12: `calibrate_intervals()` now accepts `stat_name` param for per-stat overrides (lines ~74-95)

- `/home/jbl/projects/nba-ml-engine/src/models/{catboost,xgboost,lightgbm,random_forest,ridge}_model.py` and `ensemble.py`
- All 6 model implementations
- Sprint 12: Each now persists `_residuals` array in save()/load() methods

- `/home/jbl/projects/nba-ml-engine/src/training/trainer.py`
- Training orchestrator (~400 lines)
- Sprint 12: Removed LSTM conditional (was lines 77-80), passes stat_name to calibrate_intervals (lines ~207-214)
- MODEL_CLASSES list at lines 68-75 (5 models + ensemble, no LSTM)

- `/home/jbl/projects/nba-ml-engine/src/evaluation/holdout_evaluator.py`
- 700+ line evaluation module from Sprint 11 (not modified in Sprint 12)
- 3 modes: evaluate_holdout, evaluate_calibration, evaluate_feature_groups
- FEATURE_GROUPS dict at lines 36-46

- `/home/jbl/projects/nba-ml-engine/docs/reports/sprint12-cleanup-tuning.md`
- 344-line Sprint 12 report with all findings and 6 next-step priorities

- `/home/jbl/projects/nba-ml-engine/README.md`
- Sprint 12: Updated to remove LSTM, add CatBoost, 52 tests, feature group config flags

- `/home/jbl/projects/homelab/compose/compose.nba-ml.yml`
- Docker compose for NBA ML stack (not modified but used for all deploys)

## Next Steps

Sprint 12 is fully complete. The npx skills installation has an open prompt asking about installing `find-skills` skill (shell still active with shellId 5).

**If the user wants Sprint 13, the report identifies 6 priorities:**
1. Minutes prediction model (biggest potential lever for PTS/REB/AST)
2. Player usage rate features (USG%, AST%, TOV%)
3. Opponent defensive features (DRtg, pace, pts allowed by position)
4. Edge threshold optimization (Kelly criterion, per-stat threshold tuning)
5. Model ensemble improvements (weighted by recent fold performance)
6. Binary classification for STL/BLK (P(steals≥1) instead of regression)

Immediate: Handle the find-skills prompt in shell 5 if user wants it.

## Related Wiki Pages

- [[Sprint 12 NBA ML Engine Code Cleanup and Feature Tuning]]
- [[Per-Stat Calibration Fixes and Residual Persistence in Model Save/Load]]
- [[Walk-Forward Stability Analysis and Backtesting in NBA ML Engine]]
- [[Node.js Installation via nvm and Global Taste-Skill Package Installation]]
- [[NBA ML Engine]]
- [[Node Version Manager (nvm)]]
- [[Taste-Skill Package]]
- [[Homelab]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-12-complete-and-skills-installed-48a02b58.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-22 |
| URL | N/A |
