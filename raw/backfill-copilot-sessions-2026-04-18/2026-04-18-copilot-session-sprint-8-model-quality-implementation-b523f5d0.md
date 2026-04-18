---
title: "Copilot Session Checkpoint: Sprint 8 model quality implementation"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents]
status: pending
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint 8 model quality implementation
**Session ID:** `8ddcc5a0-c1f3-4397-8f42-320e5da91f6e`
**Checkpoint file:** `/home/jbl/.copilot/session-state/8ddcc5a0-c1f3-4397-8f42-320e5da91f6e/checkpoints/001-sprint-8-model-quality-impleme.md`
**Checkpoint timestamp:** 2026-03-21T02:27:41.176519Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user is implementing Sprint 8 of their NBA ML Engine project, focused on fixing root causes of model performance plateau (~56% hit rate, 0.0-0.7% MSE gains per sprint). The approach involves 5 phases: (1) fix data integrity issues (leakage, imputation, scaling), (2) enable Optuna hyperparameter tuning, (3) add opponent-adjusted and game-line features, (4) improve validation with walk-forward CV and guardrails, (5) deploy, validate, and create a sprint report. I'm implementing all phases, committing, deploying to homelab, and writing a sprint 8 evaluation report.
</overview>

<history>
1. User asked to check on the tracking stats backfill and provide the correct command
   - Explored codebase via explore agent to find all backfill-related scripts
   - Found `python main.py backfill --tracking-browser` as the recommended command (uses curl_cffi with Chrome TLS impersonation)
   - Also `python main.py backfill --tracking` as the standard alternative

2. User provided a broken Python diagnostic command and asked to fix and run it
   - Fixed indentation and line-break issues in the multi-line docker exec command
   - Ran: `docker exec nba-ml-api python -c "..."` successfully
   - Result: **124,598 rows** in `game_tracking_stats` table

3. User asked to evaluate sprint 7 next steps, do deep research on ML model improvements, and update the doc
   - Read sprint 7 and sprint 4 evaluation reports in full
   - Launched two background explore agents to analyze: (a) ML model architecture, (b) prediction/backtesting pipeline
   - Conducted web searches on: NBA prop prediction best practices, LightGBM Optuna tuning, XGBoost vs LightGBM vs CatBoost, opponent-adjusted features, time-series cross-validation
   - Received comprehensive findings from both agents identifying critical issues
   - Updated `docs/reports/sprint7-evaluation-browser-backfill_0320.md` Next Steps section with detailed Sprint 8 plan (5 phases, 18 items)
   - Committed: `346807b` on `feature/sprint-7-browser-backfill`

4. User asked to create a progress tracker, implement all plans, commit, deploy, fix, validate, update docs, and create a new sprint report
   - Created SQL todos (12 items with 15 dependencies) for tracking
   - Created plan.md in session workspace
   - Read all critical source files in full: builder.py (950 lines), trainer.py (432 lines), feature_selector.py (122 lines), tuner.py (164 lines), splitter.py (168 lines), config.py (160 lines)
   - Examined DB models for GameLog (no team column directly, but player has team), GameLine schema, TeamStats
   - **Started Phase 1 implementation (in progress)**:
     - Fixed `_add_opp_vs_position_features()` leakage — changed from `groupby().transform("mean")` to `shift(1).expanding().mean()`
     - Fixed `_merge_advanced_stats()` leakage — now uses prior-season stats with fallback to current-season for rookies
     - Added `_add_opp_rolling_features()` — new function computing opponent rolling defensive averages (leak-free)
     - Added `_load_game_lines()` and `_add_game_line_features()` — new functions merging Vegas lines as features
     - Added `GameLine` to imports in builder.py
     - Wired new functions into `build_features()` pipeline
</history>

<work_done>
Files modified:
- `docs/reports/sprint7-evaluation-browser-backfill_0320.md`: Replaced Next Steps section with comprehensive Sprint 8 plan (5 phases, 18 items with detailed descriptions). Committed as `346807b`.
- `src/features/builder.py`: **IN PROGRESS** — Multiple edits applied but NOT yet committed:
  1. Added `GameLine` to imports (line ~20)
  2. Fixed `_add_opp_vs_position_features()` (~line 521): Changed from leaky `groupby().transform("mean")` to leak-free `shift(1).expanding(min_periods=3).mean()` with proper date sorting
  3. Fixed `_merge_advanced_stats()` (~line 675): Changed from current-season merge to prior-season lookup with rookie fallback
  4. Added `_add_opp_rolling_features()` at end of file: New function computing opponent rolling defensive stats allowed (pts/reb/ast over last 10 games, shifted to avoid leakage) + pace_factor
  5. Added `_load_game_lines()` and `_add_game_line_features()`: New functions loading Vegas lines and computing line_spread, line_total, line_implied_team_total features
  6. Wired both new functions into `build_features()` pipeline (after bbref, before targets)

Files NOT yet modified (still pending):
- `src/training/trainer.py`: Needs fillna(0) replacement with smart imputation
- `src/training/feature_selector.py`: Needs threshold adjustment (0.85 → 0.95 or disable)
- `config.py`: Needs USE_FEATURE_SELECTION default change, USE_WALK_FORWARD_CV enable
- `src/training/tuner.py`: Needs wider search ranges for Optuna
- Tests not yet run

SQL Todos status:
- `p1-leakage`: in_progress (builder.py edits done, not committed)
- All others: pending

Work completed:
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
</work_done>

<technical_details>
### Architecture
- **9-stat prediction system**: pts, reb, ast, stl, blk, tov, fg_pct, ft_pct, fg3m
- **Models**: XGBoost, LightGBM, RandomForest, Ridge, EnsembleModel (stacking with 3-fold OOF meta-learner using Ridge). LSTM exists but 2-3x worse MSE, included only if PyTorch available.
- **Feature matrix**: ~353 features (lags, rolling means/stds, EWMA, trends, context, advanced, tracking, hustle, BBRef)
- **Training split**: Date-based — train <2023-10, val 2023-24, test 2024-25 (9:1:1 ratio)
- **MLflow tracking** at `http://localhost:5000`, experiments per stat

### Critical Issues Found
1. **Feature leakage in `_add_opp_vs_position_features()`**: Used `groupby(["opponent","_pos","season"]).transform("mean")` which includes current game row. FIXED → `shift(1).expanding().mean()`
2. **Feature leakage in `_merge_advanced_stats()`**: Merged current-season stats that include future games. FIXED → uses prior-season stats with rookie fallback
3. **Team stats (opp_ortg, opp_drtg, opp_pace)**: Season-level from TeamStats table. These are full-season averages — potential mild leakage but lower severity since they're team-level aggregates, not player-game level
4. **Universal `fillna(0)` in trainer.py** (lines 104, 106, 160, 234): Corrupts feature distributions. Rolling means of 0 mean "player scored 0" not "data missing"
5. **Feature selection threshold 0.85**: Too aggressive for low-R² stats, removes 30-50% of features. Applied only to STL/BLK/FG_PCT/FT_PCT
6. **Optuna disabled by default** (`USE_OPTUNA=false`): All models use conservative defaults
7. **Walk-forward CV disabled** (`USE_WALK_FORWARD_CV=false`): Code exists in splitter.py and trainer.py but never runs
8. **Ridge is only model with StandardScaler**: Inconsistent scaling in ensemble

### Environment
- Project runs in Docker container `nba-ml-api` on homelab (beelink-gti13)
- No local Python — must use `docker exec` for running commands
- Branch: `feature/sprint-7-browser-backfill`
- Deployment: `cd ~/projects/homelab/compose && docker compose --env-file ../.env -f docker-compose.yml -f compose.nba-ml.yml build --no-cache nba-ml-api && ... up -d nba-ml-api`

### GameLog has no `team` column
- `team` comes into the DataFrame via `_load_team_stats()` which loads from `TeamStats` table and merges by opponent/season
- The Player model has `team` field (String(3)), and `_load_game_logs` doesn't include it
- The test fixture `sample_game_logs` includes a `team` column manually
- The `_add_teammate_availability_features()` uses `df["team"]` — this column must come from somewhere before that function is called. Looking at `_add_context_features()`: it merges `own_stats` which has a `team` column that gets merged into df. So `team` exists in df after context features are added.

### GameLine schema
- `game_lines` table: game_id, game_date, bookmaker, home_team (String(50)), away_team (String(50)), spread_home, spread_away, total, moneyline_home, moneyline_away
- Note: home_team/away_team are String(50) in GameLine but String(3) in other models — may need mapping

### Key Metrics (Current Production)
| Stat | Val MSE | Test MSE | R² |
|------|---------|----------|-----|
| pts | 43.54 | 41.56 | 0.51 |
| reb | 7.17 | 6.84 | 0.46 |
| ast | 4.07 | 3.81 | 0.52 |
| stl | 0.916 | 0.978 | 0.10 |
| blk | 0.722 | 0.616 | 0.21 |

### Backtest Results (Mar 16-19, 2026)
- Overall hit rate: 56.2% (777 bets)
- Best: BLK 68.2%, STL 65.5%
- Worst: PTS 49.2% (below break-even)
</technical_details>

<important_files>
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
</important_files>

<next_steps>
Remaining work (in order):
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

Immediate next action:
- Implement Phase 1b (smart imputation in trainer.py) — replace `fillna(0)` on lines 104, 106, 160, 234
- Then Phase 1c, then commit all Phase 1 changes together

Blockers/concerns:
- GameLine home_team/away_team are String(50) but team column in df may be String(3) — need to verify mapping works or game_lines may be empty (no data in table yet)
- Can't run Python locally — all validation must go through `docker exec nba-ml-api`
- builder.py changes are extensive — need thorough test run before deploy
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
