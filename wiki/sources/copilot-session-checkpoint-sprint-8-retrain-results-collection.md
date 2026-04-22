---
title: "Copilot Session Checkpoint: Sprint 8 retrain results collection"
type: source
created: 2026-03-21
last_verified: 2026-04-21
source_hash: "e5841a90e88d9462db5c3d88ad2104b899f374efbd7fcd370a7fd80299c98c4c"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-8-retrain-results-collection-8d2c8d55.md
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

# Copilot Session Checkpoint: Sprint 8 retrain results collection

## Summary

The user is implementing Sprint 8 of their NBA ML Engine project, focused on fixing root causes of model performance plateau (~56% hit rate). The approach involved fixing data integrity issues (feature leakage, imputation, scaling), enabling Optuna hyperparameter tuning, improving feature engineering, adding validation guardrails, deploying to homelab, and running a full retrain to validate. A critical Optuna parameter-naming bug was discovered and fixed during validation. The full retrain completed for 8/9 stats, with fg3m currently retraining separately.

## Key Points

- User asked to fix and run a broken Python diagnostic command
- Fixed indentation/line-break issues in docker exec command
- Committed: `346807b`
- User asked to create progress tracker, implement all plans, commit, deploy, validate, update docs
- Created SQL todos (12 items with 15 dependencies)
- Fixed feature leakage in `_add_opp_vs_position_features` and `_merge_advanced_stats`

## Execution Snapshot

### Files Modified and Committed (Sprint 8)
- `src/features/builder.py` (+189/-8): Fixed 2 leakages, added opponent rolling features, added game-line features
- `src/training/trainer.py` (+61/-6): Smart imputation (`_smart_impute()`), degradation guardrails in `_register_best_model()`
- `src/training/tuner.py` (+23/-23 then +23/-23): Wider search spaces, stat-specific tuning, then **critical fix** removing `xgb_`/`lgb_`/`rf_`/`ridge_` prefixes from trial param names
- `src/training/feature_selector.py` (+3/-3): Threshold 0.85→0.95, min features 20→50
- `src/models/ridge_model.py` (+4/-4): Removed redundant `fillna(0)`
- `config.py` (+5/-5): Enabled Optuna, walk-forward CV, raised threshold
- `pytest.ini` (+1): Added `pythonpath = .`
- `docs/reports/sprint8-evaluation-model-quality.md` (new): Full sprint report — NEEDS UPDATE with actual retrain results
- `docs/reports/sprint7-evaluation-browser-backfill_0320.md`: Updated Next Steps with Sprint 8 plan

### Commits on `feature/sprint-7-browser-backfill`
- `346807b`: Sprint 7 next steps update
- `4a30119`: Sprint 8 Phase 1-4 changes
- `e64e63a`: pytest.ini fix
- `b6fba28`: Sprint 8 evaluation report
- `8a57aa6`: Critical Optuna param name fix

### Retrain Results (Sprint 8 — Post Optuna Fix)

**Best model per stat (val_mse):**

| Stat | Best Model | Val MSE | Test MSE | Val R² | Test R² |
|------|-----------|---------|----------|--------|---------|
| pts | LightGBM | 44.1838 | 42.2437 | 0.5089 | 0.5069 |
| reb | LightGBM | 7.3248 | 7.0101 | 0.4648 | 0.4483 |
| ast | Ensemble | 4.1792 | 3.9304 | 0.5198 | 0.5069 |
| stl | XGBoost | 0.9086 | 0.9681 | 0.1008 | 0.1075 |
| blk | LightGBM | 0.7217 | 0.6191 | 0.2367 | 0.2098 |
| tov | LightGBM | 1.7107 | 1.6807 | 0.2742 | 0.2909 |
| fg_pct | XGBoost | 0.0354 | 0.0376 | 0.1144 | 0.1002 |
| ft_pct | XGBoost | 0.0650 | 0.0675 | 0.0618 | 0.0627 |
| fg3m | **RETRAINING NOW** | — | — | — | — |

**Previous baseline (leaky + Optuna bug):**

| Stat | Previous Best | Prev Val MSE | S8 Val MSE | Δ% |
|------|-------------|-------------|-----------|-----|
| pts | Ensemble | 43.54 | 44.18 | +1.5% |
| reb | Ensemble | 7.17 | 7.32 | +2.1% |
| ast | Ensemble | 4.07 | 4.18 | +2.7% |
| stl | LightGBM | 0.916 | 0.909 | **-0.8%** ✓ |
| blk | Ridge | 0.721 | 0.722 | +0.1% |
| tov | Ensemble | 1.671 | 1.711 | +2.3% |
| fg_pct | Ensemble | 0.0349 | 0.0354 | +1.4% |
| ft_pct | Ensemble | 0.0644 | 0.0650 | +0.9% |

**All models per stat (Sprint 8 retrain):**
- **PTS**: XGB=44.23, LGB=44.18★, RF=44.82, Ridge=44.96, Ensemble=44.80, LSTM=61.51
- **REB**: XGB=7.33, LGB=7.32★, RF=7.42, Ridge=7.94, Ensemble=7.53, LSTM=10.92
- **AST**: XGB=4.21, LGB=4.20, RF=4.26, Ridge=4.18, Ensemble=4.18★, LSTM=6.00
- **STL**: XGB=0.909★, LGB=0.909, RF=0.910, Ridge=0.941, Ensemble=0.913, LSTM=1.201
- **BLK**: XGB=0.724, LGB=0.722★, RF=0.728, Ridge=0.783, Ensemble=0.756, LSTM=1.202
- **TOV**: XGB=1.711, LGB=1.711★, RF=1.722, Ridge=1.904, Ensemble=1.789, LSTM=2.181
- **FG_PCT**: XGB=0.0354★, LGB=0.0354, RF=0.0357, Ridge=0.0384, Ensemble=0.0365, LSTM=0.0426
- **FT_PCT**: XGB=0.0650★, LGB=0.0651, RF=0.0655, Ridge=0.0651, Ensemble=0.0651, LSTM=0.0782

### Current State
- fg3m retrain is running in Docker container (container PID 233577, shell `fg3m-train`)
- All stale processes have been cleaned up
- Sprint 8 report needs updating with actual results
- Backtest has not been run yet
- No commit/push of updated report yet

## Technical Details

- **9-stat prediction system**: pts, reb, ast, stl, blk, tov, fg_pct, ft_pct, fg3m
- **Models per stat**: XGBoost, LightGBM, RandomForest, Ridge, EnsembleModel (3-fold OOF Ridge meta-learner), LSTM
- **Feature matrix**: 95,202 rows × 397 columns (363 feature columns)
- **Training split**: Date-based — train <2023-10-24 (56,924), val 2023-24 (12,463), test 2024-25 (25,815)
- **MLflow tracking** at `http://localhost:5000`
- **Feature selection per stat**: stl=233/363, blk=196/363, fg_pct=233/363, ft_pct=241/363 ### Critical Bug Found & Fixed: Optuna Parameter Names
- `study.best_params` returns trial parameter names, NOT the dict keys from the space function
- Space functions had: `"n_estimators": trial.suggest_int("xgb_n_estimators", ...)`
- `best_params` returned: `{"xgb_n_estimators": 800}` instead of `{"n_estimators": 800}`
- Model constructors received prefixed params, XGBoost/LightGBM silently ignored them → used defaults
- **This means Optuna tuning NEVER actually worked before Sprint 8 fix**
- Fix: Removed all prefixes from `trial.suggest_*` names (safe since each study is per-model) ### Val MSE Appearing Higher After Leakage Fix
- Previous baselines were inflated by: (a) feature leakage giving models future data, (b) Optuna bug meaning models used defaults (which happened to pair well with Ensemble stacking)
- Post-fix val_mse is higher by 0.1-2.7% — this is the HONEST, leak-free performance
- The real measure of improvement will be backtest hit rate (out-of-sample predictions)
- Critically: previous Ensemble dominated because leaky features + default params created useful diversity; with tuned params, LightGBM/XGBoost now win most stats individually ### Feature Leakage Details (Fixed)
- `_add_opp_vs_position_features()`: Used `groupby().transform("mean")` including current game → changed to `shift(1).expanding(min_periods=3).mean()`
- `_merge_advanced_stats()`: Merged current-season stats that include future games → changed to prior-season lookup with rookie fallback ### Smart Imputation Strategy
- Rolling/EWMA/trend/advanced/tracking/game-line features → column median
- Lag features, binary flags, counts → 0
- Prevents `fillna(0)` from meaning "player scored 0" when data is actually missing ### Training Patterns Observed
- LightGBM consistently wins for high-variance stats (pts, reb, blk, tov)
- Ensemble won for AST (stacking helps for moderate-variance stats)
- XGBoost won for STL, FG_PCT, FT_PCT
- RandomForest consistently gets only 3-9 Optuna trials in 300s timeout (too slow)
- LSTM consistently worst performer across all stats
- Ridge competitive for low-complexity stats (AST: 4.1838, very close to best) ### Container Process Management
- Container doesn't have `kill` or `ps` commands
- Use `docker top` for host PIDs, then find container PIDs via `/proc/[pid]/cmdline`
- Kill processes inside container via: `docker exec ... python -c "import os, signal; os.kill(pid, signal.SIGTERM)"`
- The PIDs shown by `docker top` are HOST PIDs, not container PIDs — can't use them with `os.kill()` inside container ### Daily Pipeline Conflict
- Ofelia cron runs daily pipeline at 3:00 AM ET (07:00 UTC), which includes a train step
- This started PID 179308 (`python main.py pipeline`) during our retrain
- The concurrent pipeline process was cleaned up
- **For Sprint 9**: Need to handle Optuna timeout for daily pipeline (5-6 hour retrain too long for daily runs) ### Environment
- Project runs in Docker container `nba-ml-api` on homelab (beelink-gti13)
- No local Python — all validation via `docker exec`
- Branch: `feature/sprint-7-browser-backfill`
- Deploy: `cd ~/projects/homelab/compose && docker compose --env-file ../.env -f docker-compose.yml -f compose.nba-ml.yml build --no-cache nba-ml-api && ... up -d nba-ml-api`
- Ofelia scheduler: daily pipeline 3 AM ET, weekly retrain Sundays 4 AM ET
- Model results stored in `model_registry` table (columns: id, model_name, version, trained_at, metrics, artifact_path, is_production, config_snapshot)
- MLflow registered_models table is EMPTY — models only in model_registry table ### model_registry Table Schema ```sql model_registry: id, model_name, version, trained_at, metrics (JSON), artifact_path, is_production, config_snapshot ```
- `model_name` format: `{ModelType}_{stat}` e.g., `LightGBMModel_pts`
- `metrics` is JSON containing: val_r2, test_r2, val_mae, val_mse, test_mae, test_mse, train_r2, train_mae, train_mse
- For Ensemble models, also includes `meta_weight_{base_model}` entries ### Sprint 9 Priority Evaluation (from explore agent)
- **Recency weighting**: NOT implemented — all training samples weighted equally regardless of age. HIGH impact.
- **Pace × Usage interaction**: Partial — pace and usage features exist separately but no explicit interaction term. LOW effort.
- **Back-to-back/fatigue**: Already implemented (rest_days, is_b2b, games_last_7). No travel distance.
- **CatBoost**: NOT in requirements.txt. Would add diversity to ensemble.
- **Calibration**: Basic empirical residual percentiles exist. No Platt/isotonic scaling.
- **Team name mapping**: Exists in `src/data/game_lines.py` (lines 26-56). Duplicated in `prop_lines.py`. Risk: silent merge failures.
- **Ensemble meta-learner**: Ridge with 3-fold OOF. No recency decay in fold construction.

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

- `docs/reports/sprint8-evaluation-model-quality.md` (152 lines)
- Sprint 8 report with baseline metrics, changes, expected impact, Sprint 9 next steps
- **NEEDS UPDATING** with actual retrain results (has placeholder "retrain pending")

- `src/models/ensemble.py`
- Stacking ensemble: XGB+LGB+RF+Ridge base → Ridge meta-learner, 3-fold OOF
- Not modified in Sprint 8 but relevant for Sprint 9 (upgrade meta-learner)

- `src/data/game_lines.py`
- Contains `_ODDS_NAME_TO_ABBR` team name mapping (lines 26-56)
- Duplicated in `src/data/prop_lines.py` — needs centralization in Sprint 9

## Next Steps

### Immediate: fg3m Retrain (In Progress)
- fg3m retrain is running in Docker container (container PID 233577)
- The shell `fg3m-train` is tracking it but output is buffered by `tail`
- Monitor via: `docker top nba-ml-api` to check if still running
- When complete, check results: query `model_registry` for latest fg3m entry
- Expected ~1 hour from start (~05:34 UTC)

### After fg3m Completes
1. Collect fg3m results from model_registry
2. Update SQL `train_results` table with fg3m data
3. **Update `docs/reports/sprint8-evaluation-model-quality.md`** with all actual retrain results:
- Replace "retrain pending" status
- Add actual val_mse/test_mse/R² comparison table
- Document the Optuna param name bug discovery
- Note that val_mse appears slightly higher due to leakage removal (expected)
- Update Sprint 9 priorities based on findings
4. Run backtest: `docker exec nba-ml-api python main.py backtest --start 2026-03-16 --end 2026-03-19` for hit-rate comparison against pre-Sprint 8 baseline (56.2%)
5. Commit updated report + push to GitHub
6. Evaluate whether to merge to main based on backtest results

### Sprint 9 Priorities (evaluated, ready to plan)
**High impact:**
1. Recency decay sample weighting — exponential time-decay weights
2. Reduce Optuna timeout for daily pipeline (or disable for daily, keep for weekly)
3. Centralize team name mapping (deduplicate `_ODDS_NAME_TO_ABBR`)

**Medium impact:**
4. Pace × usage interaction features
5. Add CatBoost model for ensemble diversity
6. Verify game_lines data is populated

**Lower impact:**
7. Platt/isotonic calibration
8. Upgrade ensemble meta-learner to LightGBM
9. Minutes load fatigue features
10. Consider dropping LSTM (consistently worst, adds ~5min/stat)

## Related Wiki Pages

- [[Homelab]]
- [[NBA ML Engine]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-8-retrain-results-collection-8d2c8d55.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-21 |
| URL | N/A |
