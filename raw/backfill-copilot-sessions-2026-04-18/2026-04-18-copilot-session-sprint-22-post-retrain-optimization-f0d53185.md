---
title: "Copilot Session Checkpoint: Sprint 22 post-retrain optimization"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, agents]
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint 22 post-retrain optimization
**Session ID:** `c1de5ddc-0296-4d1b-ab46-50fab29eb8f1`
**Checkpoint file:** `/home/jbl/.copilot/session-state/c1de5ddc-0296-4d1b-ab46-50fab29eb8f1/checkpoints/004-sprint-22-post-retrain-optimiz.md`
**Checkpoint timestamp:** 2026-03-26T13:41:20.227596Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user requested execution of all four next steps from the Sprint 21 report (post-retrain optimization) using the execute-sprint-from-report skill. The goals are: (1) document post-retrain metrics comparison, (2) evaluate VIF pruning for Ridge models, (3) reduce feature overlap by cutting rolling windows from [5,10,20,30] to [5,20], and (4) add analyze-features to the periodic scheduler. I'm implementing these as Sprint 22, running on the homelab server (beelink-gti13) in server mode with local containers.
</overview>

<history>
1. User invoked `/execute-sprint-from-report` skill to complete Sprint 21 next steps
   - Loaded the skill from `.github/skills/execute-sprint-from-report/SKILL.md`
   - Read AGENTS.md (doesn't exist), tasks/lessons.md (extensive), Sprint 21 report, and progress tracker
   - Detected server mode (hostname beelink-gti13, nba-ml-* containers running locally)
   - Confirmed git is on `main` branch at commit `888c27e`, clean working tree

2. Collected baseline metrics before making changes
   - Ran `docker exec nba-ml-api python main.py compare` — post-retrain metrics stable (±0.0-0.2% across all stats)
   - Ran `docker exec nba-ml-api python main.py evaluate` — full holdout evaluation across all models/stats
   - Discovered bug: EnsembleModel fails holdout evaluation for stl/blk/fg_pct/ft_pct with "feature_names mismatch" error
   - Key finding: Ridge is competitive/best for stl, blk, tov, ft_pct

3. Created Sprint 22 plan and got approval for autopilot mode
   - Created branch `feature/sprint-22-post-retrain-optimization`
   - Defined 8 todos with dependencies in SQL
   - Plan approved, entered autopilot mode

4. Fixed EnsembleModel feature mismatch bug
   - Root cause: EnsembleModel.predict() passes X directly to base models without feature alignment; base models (XGBoost/LightGBM) reject mismatched column names
   - Added `_align_for_base()` static method to align features per base model before prediction
   - Added `feature_names` attribute to EnsembleModel (init, train, save, load)
   - All 163 tests pass (excluding pre-existing apprise module issue)

5. Evaluated VIF pruning for Ridge
   - Ran VIF pruning dry run in container with USE_VIF_PRUNING=true
   - Result: iterative VIF pruning only removes 50/307 high-VIF features (capped at max_iterations=50)
   - Each iteration recomputes full VIF matrix — too slow for aggressive pruning
   - Recommendation: keep USE_VIF_PRUNING=false; rolling window reduction is the practical approach

6. Reduced rolling windows from [5,10,20,30] to [5,20]
   - Changed config.py to make ROLLING_WINDOWS configurable via env var, defaulting to "5,20"
   - Updated test_features.py to check for reb_roll_20_mean instead of reb_roll_10_mean
   - Eliminates ~148 redundant features (roll_10 and roll_30 for all 17 stats × 2 windows × 2 metrics)

7. Added post-retrain analysis scheduler job
   - Added new Ofelia job label `post-retrain-analysis` in homelab compose
   - Runs at 20:00 UTC Sundays (4 hours after weekly retrain at 16:00 UTC)
   - Command: `analyze-features --save-json /app/data/feature_analysis.json && compare`

8. Deployed and started retrain
   - Rebuilt container with `docker compose build --no-cache nba-ml-api` from homelab
   - Restarted nba-ml-api and nba-ml-scheduler containers
   - Verified API healthy, ROLLING_WINDOWS=[5,20] confirmed in container
   - Started full retrain: `docker exec -d nba-ml-api python main.py train`
   - Training in progress: MinutesModel + pts stat (all 6 models) complete as of last check
   - **Compaction occurred while waiting for training to complete**
</history>

<work_done>
Files modified:
- `src/models/ensemble.py`: Fixed feature mismatch bug — added `_align_for_base()` static method, `feature_names` attribute in __init__/train/save/load, alignment in predict loop
- `config.py`: Changed `ROLLING_WINDOWS` from hardcoded `[5, 10, 20, 30]` to env-var-configurable defaulting to `[5, 20]`
- `tests/test_features.py`: Updated `test_creates_rolling_columns` to check `reb_roll_20_mean` instead of `reb_roll_10_mean`
- `~/projects/homelab/compose/compose.nba-ml.yml`: Added `post-retrain-analysis` Ofelia job at 20:00 UTC Sundays

Files created:
- `tasks/PROGRESS-sprint22-post-retrain-optimization-0326.md`: Progress tracker with checklists and baseline metrics

Work completed:
- [x] Run post-retrain `compare` and `evaluate` for baseline metrics
- [x] Fix EnsembleModel feature_names mismatch bug
- [x] Evaluate VIF pruning for Ridge (conclusion: keep disabled, too slow)
- [x] Reduce rolling windows [5,10,20,30] → [5,20] in config
- [x] Add post-retrain-analysis scheduler job to homelab compose
- [x] Update test for rolling window change
- [x] All 163 tests pass
- [x] Rebuild and deploy container
- [x] Start full retrain with reduced features
- [ ] Wait for retrain to complete
- [ ] Run post-retrain compare and evaluate
- [ ] Write Sprint 22 report (docs/reports/sprint22-post-retrain-optimization.md)
- [ ] Commit, push, create PR, merge to main

Current state:
- On branch `feature/sprint-22-post-retrain-optimization`
- Retrain running in background (docker exec -d), PID visible via `docker top nba-ml-api`
- As of last MLflow check: MinutesModel + all 6 pts models + RidgeModel_pts complete
- Training progressing through remaining 8 stats (reb, ast, stl, blk, tov, fg_pct, ft_pct, fg3m) + CV + classifiers
- Shell 268 is pending (was waiting 600s to check progress)
</work_done>

<technical_details>
- **EnsembleModel bug root cause**: `_align_features()` in holdout_evaluator.py only checks the top-level model's `feature_names`. EnsembleModel had no `feature_names` attribute, so X passed through unmodified. Then `EnsembleModel.predict()` called each base model's predict with the full feature matrix, and XGBoost/LightGBM internally validated column names against their stored `feature_names`, causing "feature_names mismatch". Fix: added `_align_for_base()` in ensemble.py that aligns X per base model before calling predict.

- **VIF pruning evaluation findings**: With max_iterations=50 (default), iterative VIF pruning only removed 50 of 307 high-VIF features. The highest VIF removed was pts_lag_4 at 132,822. The approach recomputes the full VIF matrix each iteration, making it O(50 × p³) — impractical for aggressive pruning down to VIF<10. Rolling window reduction is more surgical and eliminates the structural collinearity at source.

- **Rolling window reduction math**: Removing windows 10 and 30 from [5,10,20,30] eliminates 2 windows × 17 stats (9 target + 8 supporting) × 2 metrics (mean + std) = ~68 features per removed window × 2 = ~136 features. Actual reduction depends on which stats have all windows populated. Feature matrix shrinks from ~376 to ~228 features.

- **ROLLING_WINDOWS now configurable**: `config.py` reads `ROLLING_WINDOWS` from env var as comma-separated ints, defaulting to "5,20". This allows A/B testing different window configs without code changes.

- **Training timeline estimate**: Based on Sprint 21 data, full retrain takes ~2 hours (9 stats × 6 models + Optuna tuning + CV + 4 classifiers). The reduced feature set should be faster due to fewer features. MinutesModel started at 13:02, pts models finished by 13:25.

- **Homelab deploy pattern**: Build from homelab root: `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache nba-ml-api`, then `up -d nba-ml-api nba-ml-scheduler`.

- **Pre-existing test failures**: 15 tests in test_notifications.py fail due to missing `apprise` module in dev .venv — unrelated to our changes. All other 163 tests pass.

- **Ofelia scheduler format**: 6-field cron with seconds: `sec min hour day month weekday`. Labels go on the nba-ml-scheduler service, with `.container: nba-ml-api` to exec in the API container.

- **Post-retrain baseline metrics (holdout, 376 features)**:
  - pts: XGBoost MAE=5.063, R²=0.506
  - reb: CatBoost MAE=2.043, R²=0.449
  - ast: Ridge MAE=1.503, R²=0.503
  - stl: Ridge MAE=0.767, R²=0.106
  - blk: Ridge MAE=0.568, R²=0.216
  - tov: Ridge MAE=0.997, R²=0.287
  - fg_pct: CatBoost MAE=0.146, R²=0.098
  - ft_pct: Ridge MAE=0.205, R²=0.063
  - fg3m: LightGBM MAE=0.964, R²=0.318

- **Model comparison (pre vs post Sprint 21 retrain)**: All stats within ±0.2% MSE — retrain on same features produced stable results as expected.
</technical_details>

<important_files>
- `src/models/ensemble.py`
  - Fixed feature_names mismatch bug
  - Added `_align_for_base()` static method (lines ~134-144)
  - Added `feature_names: list[str] = []` in __init__ (line ~49)
  - Set `self.feature_names = list(X_train.columns)` at end of train (line ~88)
  - Added `feature_names` to save pickle dict and load restoration
  - Predict now calls `self._align_for_base(X, model)` per base model

- `config.py`
  - Changed line ~66: `ROLLING_WINDOWS = [int(w) for w in os.getenv("ROLLING_WINDOWS", "5,20").split(",")]`
  - Also has VIF config: USE_VIF_PRUNING (false), VIF_THRESHOLD (10.0) — unchanged

- `tests/test_features.py`
  - Line ~94: Changed assertion from `reb_roll_10_mean` to `reb_roll_20_mean`

- `~/projects/homelab/compose/compose.nba-ml.yml`
  - Added 3 new lines after weekly-retrain job (~lines 137-139):
    - `ofelia.job-exec.post-retrain-analysis.schedule: "0 0 20 * * 0"`
    - `ofelia.job-exec.post-retrain-analysis.container: nba-ml-api`
    - `ofelia.job-exec.post-retrain-analysis.command: "python main.py analyze-features --save-json /app/data/feature_analysis.json && python main.py compare"`

- `tasks/PROGRESS-sprint22-post-retrain-optimization-0326.md`
  - Sprint progress tracker with implementation/validation/deployment checklists
  - Contains pre-retrain baseline holdout metrics table

- `src/evaluation/holdout_evaluator.py`
  - Has `_align_features()` function at ~line 161 — works for individual models
  - The ensemble bug was that this function passes through unchanged when model has no feature_names
  - No changes needed here — fix was in ensemble.py itself

- `src/training/trainer.py`
  - Core training orchestrator — training running in container now
  - Has `compare_model_versions()` at ~line 926 for post-retrain comparison
  - Has guardrails from Sprint 21 (timeouts, resume)
</important_files>

<next_steps>
Remaining work:
- Wait for retrain to complete (currently running in container, started ~13:02 UTC)
- Shell 268 may still be pending — use `read_bash` with shellId 268 or run a new check
- Run `docker exec nba-ml-api python main.py compare` after retrain finishes
- Run `docker exec nba-ml-api python main.py evaluate` for full holdout metrics with reduced features
- Compare new metrics against baseline (376 features) to validate no regression
- Write sprint report: `docs/reports/sprint22-post-retrain-optimization.md`
- Update progress tracker with final results
- Commit all changes, push branch
- Create PR via `gh pr create` and merge to main
- Ensure homelab compose changes are committed in homelab repo

Immediate next actions:
1. Check if retrain is still running: `docker top nba-ml-api | grep train`
2. Check latest MLflow runs for progress
3. When complete, run compare + evaluate
4. Write report with before/after metrics comparison
5. Git workflow: commit → push → PR → merge

SQL todos remaining:
- `retrain-reduced-windows` (in_progress)
- `write-sprint-report` (in_progress)
- `deploy-and-verify` (pending — needs post-retrain verification)
- `commit-pr-merge` (pending)

Blockers:
- Retrain must complete before compare/evaluate/report can be finalized
- Estimated ~1-1.5 hours remaining from last check (6 of 9 stats plus CV + classifiers still pending)
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
