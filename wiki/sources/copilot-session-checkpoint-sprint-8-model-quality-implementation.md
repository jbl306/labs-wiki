---
title: "Copilot Session Checkpoint: Sprint 8 model quality implementation"
type: source
created: 2026-03-21
last_verified: 2026-04-21
source_hash: "35047e02739f51a7cd9bb66835bd07acad22f52e996646d16ba02b647f1a5ac6"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-8-model-quality-implementation-b523f5d0.md
quality_score: 57
concepts:
  []
related:
  - "[[Homelab]]"
  - "[[NBA ML Engine]]"
tier: archive
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents]
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: executed
---

# Copilot Session Checkpoint: Sprint 8 model quality implementation

## Summary

The user is implementing Sprint 8 of their NBA ML Engine project, focused on fixing root causes of model performance plateau (~56% hit rate, 0.0-0.7% MSE gains per sprint). The approach involves 5 phases: (1) fix data integrity issues (leakage, imputation, scaling), (2) enable Optuna hyperparameter tuning, (3) add opponent-adjusted and game-line features, (4) improve validation with walk-forward CV and guardrails, (5) deploy, validate, and create a sprint report. I'm implementing all phases, committing, deploying to homelab, and writing a sprint 8 evaluation report.

## Key Points

- Deep research on ML model improvements
- Sprint 7 next steps updated with Sprint 8 plan
- Progress tracker created (SQL todos)
- Fix feature leakage in _add_opp_vs_position_features
- Fix feature leakage in _merge_advanced_stats (prior-season)
- Add opponent rolling defensive features

## Execution Snapshot

**Files modified:**
- `docs/reports/sprint7-evaluation-browser-backfill_0320.md`: Replaced Next Steps section with comprehensive Sprint 8 plan (5 phases, 18 items with detailed descriptions). Committed as `346807b`.
- `src/features/builder.py`: **IN PROGRESS** — Multiple edits applied but NOT yet committed:
1. Added `GameLine` to imports (line ~20)
2. Fixed `_add_opp_vs_position_features()` (~line 521): Changed from leaky `groupby().transform("mean")` to leak-free `shift(1).expanding(min_periods=3).mean()` with proper date sorting
3. Fixed `_merge_advanced_stats()` (~line 675): Changed from current-season merge to prior-season lookup with rookie fallback
4. Added `_add_opp_rolling_features()` at end of file: New function computing opponent rolling defensive stats allowed (pts/reb/ast over last 10 games, shifted to avoid leakage) + pace_factor
5. Added `_load_game_lines()` and `_add_game_line_features()`: New functions loading Vegas lines and computing line_spread, line_total, line_implied_team_total features
6. Wired both new functions into `build_features()` pipeline (after bbref, before targets)

**Files NOT yet modified (still pending):**
- `src/training/trainer.py`: Needs fillna(0) replacement with smart imputation
- `src/training/feature_selector.py`: Needs threshold adjustment (0.85 → 0.95 or disable)
- `config.py`: Needs USE_FEATURE_SELECTION default change, USE_WALK_FORWARD_CV enable
- `src/training/tuner.py`: Needs wider search ranges for Optuna
- Tests not yet run

**SQL Todos status:**
- `p1-leakage`: in_progress (builder.py edits done, not committed)
- All others: pending

**Work completed:**
- [x] Deep research on ML model improvements
- [x] Sprint 7 next steps updated with Sprint 8 plan
- [x] Progress tracker created (SQL todos)
- [x] Fix feature leakage in _add_opp_vs_position_features
- [x] Fix feature leakage in _merge_advanced_stats (prior-season)
- [x] Add opponent rolling defensive features
- [x] Add game-line features (Vegas lines)
- [ ] Replace fillna(0) with smart imputation (Phase 1b)
- [ ] Fix feature scaling inconsistency (Phase 1c)
- [ ] Enable/configure Optuna tuning (Phase 2)
- [ ] Fix feature selection threshold (Phase 3)
- [ ] Enable walk-forward CV (Phase 4)
- [ ] Add model degradation guardrails (Phase 4)
- [ ] Run tests to validate changes
- [ ] Commit all Phase 1-4 changes
- [ ] Deploy to homelab
- [ ] Create sprint 8 evaluation report

## Technical Details

- **9-stat prediction system**: pts, reb, ast, stl, blk, tov, fg_pct, ft_pct, fg3m
- **Models**: XGBoost, LightGBM, RandomForest, Ridge, EnsembleModel (stacking with 3-fold OOF meta-learner using Ridge). LSTM exists but 2-3x worse MSE, included only if PyTorch available.
- **Feature matrix**: ~353 features (lags, rolling means/stds, EWMA, trends, context, advanced, tracking, hustle, BBRef)
- **Training split**: Date-based — train <2023-10, val 2023-24, test 2024-25 (9:1:1 ratio)
- **MLflow tracking** at `http://localhost:5000`, experiments per stat ### Critical Issues Found
- **Feature leakage in `_add_opp_vs_position_features()`**: Used `groupby(["opponent","_pos","season"]).transform("mean")` which includes current game row. FIXED → `shift(1).expanding().mean()`
- **Feature leakage in `_merge_advanced_stats()`**: Merged current-season stats that include future games. FIXED → uses prior-season stats with rookie fallback
- **Team stats (opp_ortg, opp_drtg, opp_pace)**: Season-level from TeamStats table. These are full-season averages — potential mild leakage but lower severity since they're team-level aggregates, not player-game level
- **Universal `fillna(0)` in trainer.py** (lines 104, 106, 160, 234): Corrupts feature distributions. Rolling means of 0 mean "player scored 0" not "data missing"
- **Feature selection threshold 0.85**: Too aggressive for low-R² stats, removes 30-50% of features. Applied only to STL/BLK/FG_PCT/FT_PCT
- **Optuna disabled by default** (`USE_OPTUNA=false`): All models use conservative defaults
- **Walk-forward CV disabled** (`USE_WALK_FORWARD_CV=false`): Code exists in splitter.py and trainer.py but never runs
- **Ridge is only model with StandardScaler**: Inconsistent scaling in ensemble ### Environment
- Project runs in Docker container `nba-ml-api` on homelab (beelink-gti13)
- No local Python — must use `docker exec` for running commands
- Branch: `feature/sprint-7-browser-backfill`
- Deployment: `cd ~/projects/homelab/compose && docker compose --env-file ../.env -f docker-compose.yml -f compose.nba-ml.yml build --no-cache nba-ml-api && ... up -d nba-ml-api` ### GameLog has no `team` column
- `team` comes into the DataFrame via `_load_team_stats()` which loads from `TeamStats` table and merges by opponent/season
- The Player model has `team` field (String(3)), and `_load_game_logs` doesn't include it
- The test fixture `sample_game_logs` includes a `team` column manually
- The `_add_teammate_availability_features()` uses `df["team"]` — this column must come from somewhere before that function is called. Looking at `_add_context_features()`: it merges `own_stats` which has a `team` column that gets merged into df. So `team` exists in df after context features are added. ### GameLine schema
- `game_lines` table: game_id, game_date, bookmaker, home_team (String(50)), away_team (String(50)), spread_home, spread_away, total, moneyline_home, moneyline_away
- Note: home_team/away_team are String(50) in GameLine but String(3) in other models — may need mapping ### Key Metrics (Current Production) | Stat | Val MSE | Test MSE | R² | |------|---------|----------|-----| | pts | 43.54 | 41.56 | 0.51 | | reb | 7.17 | 6.84 | 0.46 | | ast | 4.07 | 3.81 | 0.52 | | stl | 0.916 | 0.978 | 0.10 | | blk | 0.722 | 0.616 | 0.21 | ### Backtest Results (Mar 16-19, 2026)
- Overall hit rate: 56.2% (777 bets)
- Best: BLK 68.2%, STL 65.5%
- Worst: PTS 49.2% (below break-even)

## Important Files

- `src/features/builder.py` (now ~1080 lines)
- Core feature engineering pipeline
- **ACTIVELY MODIFYING**: Fixed leakage in opp_vs_position and advanced_stats, added opponent rolling features and game-line features
- Key functions: `build_features()` (line 49), `_add_opp_vs_position_features()` (~521), `_merge_advanced_stats()` (~675), `_add_opp_rolling_features()` (new, ~980), `_add_game_line_features()` (new, ~1040)

- `src/training/trainer.py` (432 lines)
- Training orchestrator — trains all models, logs MLflow, registers best
- **NEEDS MODIFICATION**: Lines 104, 106, 160 — replace `fillna(0)` with smart imputation
- Key: `train_all()` (line 51), feature selection at line 110, walk-forward CV at line 218

- `src/training/feature_selector.py` (122 lines)
- Feature selection using tree importance with cumsum threshold
- **NEEDS MODIFICATION**: Raise threshold from 0.85 to 0.95 or change defaults
- Key: `select_features_for_stat()` (line 28), `LOW_R2_STATS` (line 22), `DEFAULT_IMPORTANCE_THRESHOLD` (line 25)

- `config.py` (160 lines)
- All config variables loaded from env
- **NEEDS MODIFICATION**: Change defaults for USE_FEATURE_SELECTION, USE_WALK_FORWARD_CV, FEATURE_IMPORTANCE_THRESHOLD
- Key settings: lines 93 (USE_WALK_FORWARD_CV), 97 (USE_OPTUNA), 102 (USE_FEATURE_SELECTION), 103 (FEATURE_IMPORTANCE_THRESHOLD)

- `src/training/tuner.py` (164 lines)
- Optuna hyperparameter search spaces per model type
- May need wider ranges for LightGBM (num_leaves up to 256, min_child_samples up to 200)
- Key: `tune_model()` (line 99), search spaces (lines 27-88)

- `src/training/splitter.py` (168 lines)
- Date and season-based splitting, expanding window CV
- Key: `date_split()` (line 91), `expanding_window_split()` (line 131)

- `docs/reports/sprint7-evaluation-browser-backfill_0320.md` (310 lines)
- Sprint 7 report — Next Steps section updated with Sprint 8 plan
- Already committed

- `tests/test_features.py`, `tests/test_models.py`, `tests/test_tuner.py`, `tests/test_backtester.py`
- Test suite — need to run after changes to validate
- test_features has a `sample_game_logs` fixture with 30 games for player_id=1

## Next Steps

**Remaining work (in order):**
1. **Phase 1b — Fix imputation in trainer.py**: Replace `fillna(0)` with column-mean for rolling/advanced features, forward-fill for lags
2. **Phase 1c — Fix scaling**: Add note or adjust Ridge scaling approach for ensemble consistency
3. **Phase 2 — Optuna config**: Update config.py defaults, widen tuner.py search ranges
4. **Phase 3 — Feature selection fix**: Raise threshold to 0.95 in config.py/feature_selector.py
5. **Phase 4 — Walk-forward CV**: Enable in config.py (USE_WALK_FORWARD_CV=true)
6. **Phase 4 — Degradation guardrails**: Add val_mse threshold checks in trainer.py _register_best_model()
7. **Run tests**: `docker exec nba-ml-api pytest` to validate all changes
8. **Commit all changes** on feature/sprint-7-browser-backfill branch
9. **Deploy to homelab**: Build Docker image and restart container
10. **Retrain models**: `docker exec nba-ml-api python main.py train` and capture metrics
11. **Create sprint 8 evaluation report**: `docs/reports/sprint8-evaluation-model-quality.md`
12. **Update SQL todos** as each phase completes

**Immediate next action:**
- Implement Phase 1b (smart imputation in trainer.py) — replace `fillna(0)` on lines 104, 106, 160, 234
- Then Phase 1c, then commit all Phase 1 changes together

**Blockers/concerns:**
- GameLine home_team/away_team are String(50) but team column in df may be String(3) — need to verify mapping works or game_lines may be empty (no data in table yet)
- Can't run Python locally — all validation must go through `docker exec nba-ml-api`
- builder.py changes are extensive — need thorough test run before deploy

## Related Wiki Pages

- [[Homelab]]
- [[NBA ML Engine]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-8-model-quality-implementation-b523f5d0.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-21 |
| URL | N/A |
