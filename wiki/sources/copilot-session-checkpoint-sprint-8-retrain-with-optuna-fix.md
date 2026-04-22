---
title: "Copilot Session Checkpoint: Sprint 8 retrain with Optuna fix"
type: source
created: 2026-03-21
last_verified: 2026-04-21
source_hash: "427a1145e8e5db01facd53a9da2ebde876a2c02445db3e73361f29ea2c4241e1"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-8-retrain-with-optuna-fix-af6747c6.md
quality_score: 61
concepts:
  []
related:
  - "[[Homelab]]"
  - "[[NBA ML Engine]]"
tier: archive
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents]
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: validated
---

# Copilot Session Checkpoint: Sprint 8 retrain with Optuna fix

## Summary

The user is implementing Sprint 8 of their NBA ML Engine project, focused on fixing root causes of model performance plateau (~56% hit rate). The approach involves fixing data integrity issues (leakage, imputation, scaling), enabling Optuna hyperparameter tuning, improving feature engineering, adding validation guardrails, deploying to homelab, and running a full retrain to validate. A critical Optuna parameter-naming bug was discovered and fixed during the retrain validation phase. The full retrain is currently running (3/9 stats complete) and I'm simultaneously evaluating Sprint 9 priorities.

## Key Points

- User asked to fix and run a broken Python diagnostic command
- Fixed indentation/line-break issues in docker exec command
- Committed: `346807b`
- User asked to create progress tracker, implement all plans, commit, deploy, validate, update docs
- Created SQL todos (12 items with 15 dependencies)
- Fixed feature leakage in `_add_opp_vs_position_features` and `_merge_advanced_stats`

## Execution Snapshot

**Files modified and committed:**
- `src/features/builder.py` (+189/-8): Fixed 2 leakages, added opponent rolling features, added game-line features
- `src/training/trainer.py` (+61/-6): Smart imputation (`_smart_impute()`), degradation guardrails in `_register_best_model()`
- `src/training/tuner.py` (+23/-23 then +23/-23): Wider search spaces, stat-specific tuning, then **critical fix** removing `xgb_`/`lgb_`/`rf_`/`ridge_` prefixes from trial param names
- `src/training/feature_selector.py` (+3/-3): Threshold 0.85→0.95, min features 20→50
- `src/models/ridge_model.py` (+4/-4): Removed redundant `fillna(0)`
- `config.py` (+5/-5): Enabled Optuna, walk-forward CV, raised threshold
- `pytest.ini` (+1): Added `pythonpath = .`
- `docs/reports/sprint8-evaluation-model-quality.md` (new): Full sprint report with baseline metrics, changes, expected impact, Sprint 9 next steps
- `docs/reports/sprint7-evaluation-browser-backfill_0320.md`: Updated Next Steps with Sprint 8 plan

**Commits on `feature/sprint-7-browser-backfill`:**
- `346807b`: Sprint 7 next steps update
- `4a30119`: Sprint 8 Phase 1-4 changes
- `e64e63a`: pytest.ini fix
- `b6fba28`: Sprint 8 evaluation report
- `8a57aa6`: Critical Optuna param name fix

**Current retrain in progress (shellId: `retrain`, async):**
- **PTS complete**: Best LightGBM val_mse=44.18 (baseline 43.54 — inflated by leakage)
- **REB complete**: Best LightGBM val_mse=7.32 (baseline 7.17)
- **AST in progress**: XGBoost val_mse=4.21 (baseline 4.07), LightGBM tuning started
- 6 more stats pending: stl, blk, tov, fg_pct, ft_pct, fg3m
- Estimated completion: ~3-4 more hours from current point

**SQL tracking tables:**
- `todos`: 12 items, all status='done'
- `train_results`: Tracking val_mse per stat/model as training progresses

## Technical Details

- **9-stat prediction system**: pts, reb, ast, stl, blk, tov, fg_pct, ft_pct, fg3m
- **Models**: XGBoost, LightGBM, RandomForest, Ridge, EnsembleModel (3-fold OOF Ridge meta-learner), LSTM
- **Feature matrix**: 95,202 rows × 397 columns (363 feature columns) — up from ~353 pre-Sprint 8
- **Training split**: Date-based — train <2023-10-24 (56,924), val 2023-24 (12,463), test 2024-25 (25,815)
- **MLflow tracking** at `http://localhost:5000` ### Critical Bug Found & Fixed: Optuna Parameter Names
- `study.best_params` returns trial parameter names, NOT the dict keys from the space function
- Space functions had: `"n_estimators": trial.suggest_int("xgb_n_estimators", ...)`
- `best_params` returned: `{"xgb_n_estimators": 800}` instead of `{"n_estimators": 800}`
- Model constructors received prefixed params, XGBoost/LightGBM silently ignored them → used defaults
- **This means Optuna tuning NEVER actually worked before Sprint 8 fix**
- Fix: Removed all prefixes from `trial.suggest_*` names (safe since each study is per-model) ### Val MSE Appearing Higher After Leakage Fix
- Baseline PTS val_mse=43.54 was inflated by leakage (current-game data in features)
- Post-fix PTS val_mse=44.18 is the honest, leak-free performance
- The real measure of improvement will be test_mse and backtest hit rate (out-of-sample) ### Feature Leakage Details (Fixed)
- `_add_opp_vs_position_features()`: Used `groupby().transform("mean")` including current game → changed to `shift(1).expanding(min_periods=3).mean()`
- `_merge_advanced_stats()`: Merged current-season stats that include future games → changed to prior-season lookup with rookie fallback ### Smart Imputation Strategy
- Rolling/EWMA/trend/advanced/tracking/game-line features → column median
- Lag features, binary flags, counts → 0
- Prevents `fillna(0)` from meaning "player scored 0" when data is actually missing ### Environment
- Project runs in Docker container `nba-ml-api` on homelab (beelink-gti13)
- No local Python — all validation via `docker exec`
- Branch: `feature/sprint-7-browser-backfill`
- Deploy: `cd ~/projects/homelab/compose && docker compose --env-file ../.env -f docker-compose.yml -f compose.nba-ml.yml build --no-cache nba-ml-api && ... up -d nba-ml-api`
- Ofelia scheduler: daily pipeline 3 AM ET, weekly retrain Sundays 4 AM ET ### Sprint 9 Priority Evaluation (from explore agent)
- **Recency weighting**: NOT implemented — all training samples weighted equally regardless of age. HIGH impact.
- **Pace × Usage interaction**: Partial — pace and usage features exist separately but no explicit interaction term. LOW effort.
- **Back-to-back/fatigue**: Already implemented (rest_days, is_b2b, games_last_7). No travel distance.
- **CatBoost**: NOT in requirements.txt. Would add diversity to ensemble.
- **Calibration**: Basic empirical residual percentiles exist. No Platt/isotonic scaling.
- **Team name mapping**: Exists in `src/data/game_lines.py` (lines 26-56) — full names converted to abbreviations during fetch. Duplicated in `prop_lines.py`. Risk: silent merge failures if mapping breaks.
- **Ensemble meta-learner**: Ridge with 3-fold OOF. No recency decay in fold construction. ### GameLine Schema Issue
- `home_team`/`away_team` are String(50) but abbreviations are String(3)
- Mapping exists in `src/data/game_lines.py` via `_ODDS_NAME_TO_ABBR` dict (applied during ingestion)
- Need to verify game_lines table actually has data: `SELECT COUNT(*) FROM game_lines` ### Optuna Training Time
- ~35-40 min per stat (4 models × 300s timeout each + ensemble + LSTM)
- 9 stats total = ~5-6 hours for full retrain with Optuna enabled
- May need to reduce for daily pipeline (conflict with 3:15 AM props refresh)

## Important Files

- `src/features/builder.py` (~1080 lines)
- Core feature engineering pipeline — all feature construction
- Sprint 8: Fixed leakage in `_add_opp_vs_position_features()` (~521), `_merge_advanced_stats()` (~675)
- Sprint 8: Added `_add_opp_rolling_features()` (~980), `_load_game_lines()` (~1044), `_add_game_line_features()` (~1071)
- `build_features()` at line 49 orchestrates the full pipeline

- `src/training/trainer.py` (~470 lines)
- Training orchestrator — trains all models, logs MLflow, registers best
- Sprint 8: Added `_smart_impute()` function (~35-58), replaced 4x `fillna(0)` calls
- Sprint 8: Added degradation guardrail in `_register_best_model()` (~297-335)
- Key: `train_all()` (line 51), Optuna integration (lines 157-163)

- `src/training/tuner.py` (164 lines)
- Optuna hyperparameter search spaces per model type
- Sprint 8: Widened ranges, added stat-specific tuning, **fixed critical param name prefix bug**
- Key: `_get_xgboost_space()` (28), `_get_lightgbm_space()` (47), `tune_model()` (97)

- `src/training/feature_selector.py` (122 lines)
- Feature selection using tree importance with cumsum threshold
- Sprint 8: Raised threshold 0.85→0.95, min features 20→50

- `src/models/ridge_model.py` (100 lines)
- Ridge regression with internal StandardScaler
- Sprint 8: Removed redundant `fillna(0)` — data arrives pre-imputed

- `config.py` (160 lines)
- All config loaded from env vars
- Sprint 8: Changed defaults — USE_OPTUNA=true, USE_WALK_FORWARD_CV=true, FEATURE_IMPORTANCE_THRESHOLD=0.95, OPTUNA_N_TRIALS=50, OPTUNA_TIMEOUT=300

- `docs/reports/sprint8-evaluation-model-quality.md` (151 lines)
- Sprint 8 report with baseline metrics, changes, expected impact, Sprint 9 next steps
- Will need updating with actual retrain results once complete

- `src/models/ensemble.py`
- Stacking ensemble: XGB+LGB+RF+Ridge base → Ridge meta-learner, 3-fold OOF
- Not modified in Sprint 8 but relevant for Sprint 9 (upgrade meta-learner)

- `src/data/game_lines.py`
- Contains `_ODDS_NAME_TO_ABBR` team name mapping (lines 26-56)
- Duplicated in `src/data/prop_lines.py` — needs centralization in Sprint 9

## Next Steps

### Immediate: Complete Retrain Monitoring
- Training is running asynchronously (shellId: `retrain`)
- 3/9 stats complete (pts, reb, ast in progress), ~3-4 hours remaining
- Need to collect all val_mse results when complete
- Results so far tracked in SQL `train_results` table

### After Retrain Completes
1. Collect all 9 stat val_mse results and compare against baseline
2. Run backtest: `docker exec nba-ml-api python main.py backtest --start 2026-03-16 --end 2026-03-19` for apples-to-apples comparison
3. Update `docs/reports/sprint8-evaluation-model-quality.md` with actual results
4. If hit rate improves, consider merging to main

### Sprint 9 Priorities (evaluated, not yet implemented)

**High impact:**
1. **Recency decay sample weighting** — Add exponential time-decay weights to training (currently all samples weighted equally)
2. **Centralize team name mapping** — Deduplicate `_ODDS_NAME_TO_ABBR` from game_lines.py and prop_lines.py into shared constants
3. **Verify game_lines data** — Check if game_lines table is populated; if empty, line features are all NaN

**Medium impact:**
4. **Pace × usage interaction features** — Create `usage_proxy * pace_factor` composite feature (low effort)
5. **Add CatBoost model** — Would add ensemble diversity (requires `pip install catboost`)
6. **Reduce Optuna timeout for daily pipeline** — Current 300s × 50 trials × 36 studies may conflict with daily cron schedule

**Lower impact:**
7. **Platt/isotonic calibration** — Replace empirical residual percentiles with proper probability calibration
8. **Upgrade ensemble meta-learner** — Replace Ridge with LightGBM for non-linear blending
9. **Minutes load fatigue features** — Already have rest_days/b2b, could add trailing 5-game minutes accumulation

### Concern: Daily Pipeline Duration
- With Optuna enabled at 50 trials/300s, full retrain takes ~5-6 hours
- Daily pipeline starts at 3:00 AM ET, props refresh at 3:15 AM
- May need to disable Optuna for daily runs (keep for weekly) or reduce trials significantly

## Related Wiki Pages

- [[Homelab]]
- [[NBA ML Engine]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-8-retrain-with-optuna-fix-af6747c6.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-21 |
| URL | N/A |
