---
title: "Copilot Session Checkpoint: Dashboard Accuracy Hardening"
type: text
captured: 2026-04-25T11:59:59.498342Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, mempalace, agents, dashboard]
checkpoint_class: project-progress
checkpoint_class_rule: "body:status"
retention_mode: compress
status: success
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Dashboard Accuracy Hardening
**Session ID:** `39cb6a8f-14d7-43a7-bad1-98ec00e06033`
**Checkpoint file:** `/home/jbl/.copilot/session-state/39cb6a8f-14d7-43a7-bad1-98ec00e06033/checkpoints/003-dashboard-accuracy-hardening.md`
**Checkpoint timestamp:** 2026-04-25T11:58:57.527757Z
**Exported:** 2026-04-25T11:59:59.498342Z
**Checkpoint class:** `project-progress` (rule: `body:status`)
**Retention mode:** `compress`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user is iteratively improving the NBA ML dashboard at `nba-dashboard.jbl-lab.com`, with a focus on dashboard accuracy/trustworthiness: prop signals, “most confident” predictions, model R² charts, calibration, model-health status, artifact integrity, stale data, and final status reporting. Work has been done in isolated `nba-ml-engine` git worktrees, using TDD where code changed, validating locally and live, deploying through the homelab Docker Compose stack, writing reports under `nba-ml-engine/reports`, and pushing to GitHub.
</overview>

<history>
1. The user first asked to evaluate `nba-dashboard.jbl-lab.com`, identify accuracy problems in “Today’s Most Confident Predictions,” Props, and “Production Models R² by Stat,” then write a report and push it.
   - Investigated live dashboard/API via HTTP because stealth browser/Chrome was unavailable.
   - Found prop-source inconsistency: `/api/dashboard` showed hundreds of “confident” props while `/api/props` was empty.
   - Found model R² chart blank because `/api/models` returned nested `metrics.test_r2`/`metrics.val_r2` while the UI expected top-level fields.
   - Found severe calibration problems: high-confidence tier underperformed, public ECE ~0.366, stale game logs, and degraded model health.
   - Wrote and pushed `reports/2026-04-24-dashboard-accuracy-audit.md` in commit `47a351b`.

2. The user asked to implement the plan, evaluate again, and push a new report.
   - Created worktree `.worktrees/dashboard-accuracy-fixes`.
   - Added dashboard contract tests first.
   - Implemented `dashboard-ui/server/src/dashboardContracts.ts`.
   - Normalized `/api/models` output for the R² chart.
   - Switched Overview/Props/Rankings to a canonical FastAPI prop-edge source.
   - Added prop metadata, empty reasons, and accuracy warnings.
   - Relabeled UI “Confidence” to “Model Signal.”
   - Deployed `nba-ml-dashboard`.
   - Live re-evaluation showed the R² chart fixed, props consistently withheld when canonical source was empty, and warnings surfaced.
   - Wrote `reports/2026-04-25-dashboard-accuracy-implementation-reevaluation.md`.
   - Pushed commit `c0233fe fix: align dashboard accuracy contracts`.

3. The user asked to complete fixes in the new report, validate/deploy, and create a status report.
   - Created worktree `.worktrees/dashboard-accuracy-followups`.
   - Diagnosed why canonical `/prop-edges` returned zero picks: joined candidates existed but were filtered out by low model signal and edge caps.
   - Added FastAPI `/prop-edges/diagnostics` and filter diagnostics in `src/applications/prop_finder.py`.
   - Added `main.py ingest --gamelogs`.
   - Extended game-log ingestion to include playoffs.
   - Added freshness gates before `pipeline` and `predict --store`.
   - Added props-history aliases `confidence_tiers` and `by_confidence_tier`.
   - Deployed `nba-ml-api` and `nba-ml-dashboard`.
   - Ran game-log refresh, prediction refresh for `2026-04-24`, and `post-retrain`.
   - Live checks showed game logs/predictions current to `2026-04-24`, canonical picks still withheld with clear diagnostics, and prop history fixed.
   - Wrote `reports/2026-04-24-dashboard-accuracy-followup-status.md`.
   - Pushed commit `009d353 fix: harden dashboard prop accuracy signals`.

4. The user asked to “finish the remaining accuracy work from the report.”
   - Continued in fresh worktree `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final` on branch `feature/dashboard-accuracy-final`, base `origin/main` at `009d353`.
   - Updated the session plan to focus on final live risks: missing artifacts, degraded calibration/model health, and prop-line/prediction date coverage.
   - Live state had changed since the prior report:
     - `/api/props` returned 340 canonical records.
     - `/api/dashboard` had 10 best predictions.
     - Predictions reached `2026-04-25`.
     - Public calibration still reported ECE ~0.365.
     - Model health was degraded.
     - Registry checks later showed missing production artifacts despite apparent production rows.
   - Found the calibration endpoint was measuring raw edge ratio, while prop filtering used CI Platt + optional post-hoc calibration.
   - Added/updated tests first for:
     - Sparse middle-bin ECE counting.
     - CI z-score computation matching prop-finder interval widths.
     - Serving confidence score source selection.
     - Model-health alerting with the new row shape.
     - Registry pruning preserving shared artifacts.
     - Dashboard freshness warnings allowing a one-day game-log lag.
   - Fixed `compute_calibration()` binning.
   - Added `compute_ci_z_scores()` and `compute_serving_confidence_scores()`.
   - Updated `/evaluation/calibration` and `/evaluation/calibration-by-stat` to evaluate the served CI/post-hoc signal and expose raw-edge ECE separately.
   - Updated `src/notifications/dispatcher.py` model-health ECE checks to use the same served signal and store `ece_score_source`.
   - Discovered registry artifact drift:
     - Latest `registry-health` initially reported missing artifacts for `MinutesModel_minutes`, `EnsembleModel_reb`, `RidgeModel_ast`, `EnsembleModel_tov`, and `RidgeModel_fg3m`.
     - Root cause identified: registry rows share unversioned artifact paths, and `prune_old_models()` could delete an artifact referenced by a kept/production row.
   - Fixed `prune_old_models()` via `_delete_artifact_if_unreferenced()`.
   - Rebuilt missing artifacts via existing training paths:
     - `train_minutes_model(session)`
     - `python main.py train --stat ast --model RidgeModel`
     - `python main.py train --stat fg3m --model RidgeModel`
     - `python main.py train --stat reb --model EnsembleModel`
     - `python main.py train --stat tov --model EnsembleModel`
   - Deployed patched `nba-ml-api` and `nba-ml-dashboard` from final worktree.
   - Ran `python main.py registry-health`: latest snapshot `ok`, `missing_count=0`.
   - Ran `python main.py health-check`: latest ECE `0.0283` on `ci_platt+posthoc_isotonic`, OOS ECE `0.0390`, still degraded due to hit-rate/drift alerts.
   - Live dashboard final check:
     - Dashboard featured date `2026-04-25`.
     - Best predictions `10`.
     - Props `340`, source `fastapi_prop_edges`.
     - Models `8` production, all chartable R².
     - Calibration endpoint: score source `ci_platt+posthoc_isotonic`, ECE `0.0215`, raw-edge ECE `0.3653`.
     - Dashboard warning list only says model health degraded; stale game-log warning removed for allowed one-day lag.
   - Wrote `reports/2026-04-25-dashboard-accuracy-final-status.md`.
   - Ran final code review agent; approved.
   - Committed final changes as `92cdb88 fix: finish dashboard accuracy hardening`.
   - **Important:** Commit is created locally but had not yet been pushed before compaction.
</history>

<work_done>
Files created:
- `reports/2026-04-25-dashboard-accuracy-final-status.md`
  - Final live status report documenting artifact repair, calibration fix, registry health, dashboard warning fix, deployment actions, validation, and remaining true model-health risks.

Files modified in final worktree:
- `src/evaluation/calibration.py`
  - Fixed sparse-bin ECE calculation.
  - Added `compute_ci_z_scores()`.
  - Added `compute_serving_confidence_scores()`.
- `src/api/server.py`
  - `/evaluation/calibration` now uses served CI/post-hoc score source and reports raw-edge ECE separately.
  - `/evaluation/calibration-by-stat` now uses the served score source.
- `src/notifications/dispatcher.py`
  - Model-health ECE/OOS ECE checks now use served CI/post-hoc score source and store score source details.
- `src/training/trainer.py`
  - Added `_delete_artifact_if_unreferenced()`.
  - Updated `prune_old_models()` so pruning old registry rows does not delete artifacts still referenced by kept rows.
- `tests/test_calibration_extended.py`
  - Added tests for sparse middle-bin ECE, CI z-score computation, and serving confidence scoring.
- `tests/test_alerting.py`
  - Updated model-health ECE test rows for the new scoring inputs.
- `tests/test_sprint56.py`
  - Added regression test that pruning preserves a shared artifact referenced by a kept entry.
- `dashboard-ui/server/src/dashboardContracts.ts`
  - Added `FreshnessDates`, `buildFreshnessWarnings()`, and date-lag helper.
  - Dashboard freshness warning logic allows one-day game-log lag by default.
- `dashboard-ui/server/src/dashboardContracts.test.ts`
  - Added freshness warning tests.
- `dashboard-ui/server/src/index.ts`
  - Uses `buildFreshnessWarnings()` instead of hardcoded 12-hour stale-log rule.

Deployment/ops completed:
- Recovered NBA ML stack after an initial compose command accidentally ran without homelab env loaded and partially recreated services with missing env.
- Correct deployment pattern used thereafter:
  - `cd /home/jbl/projects/homelab`
  - `set -a && . ./.env && set +a`
  - `NBA_ML_ENGINE_PATH=/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final docker compose --env-file .env -f compose/compose.nba-ml.yml ...`
- Rebuilt/restarted `nba-ml-api`.
- Rebuilt/restarted `nba-ml-dashboard`.
- Rebuilt missing model artifacts using training commands.
- Refreshed registry health and model health.

Validation completed:
- Python targeted suite:
  - `tests/test_calibration_extended.py`
  - `tests/test_alerting.py`
  - `tests/test_dashboard_accuracy_followups.py`
  - `tests/test_sprint56.py`
  - Result: `39 passed`
- Python compile check passed for changed Python modules.
- Dashboard contract tests: `8 passed`.
- Dashboard server TypeScript compile passed.
- ESLint passed for changed dashboard/server files.
- Dashboard production build passed.
- Live endpoint checks passed.
- Code review agent approved final changes.

Current state:
- Worktree path: `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final`
- Branch: `feature/dashboard-accuracy-final`
- Latest local commit: `92cdb88 fix: finish dashboard accuracy hardening`
- Commit includes required trailer.
- The commit has not yet been pushed/merged to `main`.
- SQL todo `validate-deploy-report` was still `in_progress`; other final todos were marked `done`.
</work_done>

<technical_details>
- Original checkout `/home/jbl/projects/nba-ml-engine` is dirty with unrelated `.github/skills/nba-ml-pipeline/SKILL.md`; do not work there.
- Use `.worktrees/dashboard-accuracy-final` for the current final work.
- Homelab NBA stack:
  - Compose file: `/home/jbl/projects/homelab/compose/compose.nba-ml.yml`
  - API container: `nba-ml-api`, port `8000`, built from `Dockerfile`
  - Dashboard container: `nba-ml-dashboard`, port `8501`, built from `Dockerfile.dashboard-react`
  - DB: `nba-ml-db`
  - MLflow: `nba-ml-mlflow`
- Critical deployment gotcha:
  - Running compose directly without loading `/home/jbl/projects/homelab/.env` caused missing env vars and temporarily recreated `nba-ml-db` unhealthy.
  - Correct pattern must load `.env` and use `--env-file .env`; do not run compose without it.
- Calibration discovery:
  - Old public `/evaluation/calibration` used raw `ABS(pred.predicted_value - pl.line) / pl.line`, producing ECE ~0.365.
  - Prop filtering uses a CI-based signal:
    - z-score from prediction interval width.
    - CI Platt calibrator if available.
    - optional global/post-hoc calibrator.
  - After change, public endpoint reports served-score ECE and raw-edge ECE separately.
  - Live final:
    - `/api/evaluation/calibration.score_source`: `ci_platt+posthoc_isotonic`
    - `expected_calibration_error`: `0.0215`
    - `raw_edge_expected_calibration_error`: `0.3653`
- ECE binning bug:
  - `sklearn.calibration_curve()` returns only populated bins; previous code paired those populated bins with the first N bin edges, so sparse middle-only probabilities could have count zero and ECE zero incorrectly.
  - Fixed by iterating actual bin edges and keeping only populated bins with correct counts.
- Registry/artifact discovery:
  - `model_registry` rows use unversioned artifact paths like `/app/models/reb/ensemblemodel.pkl`.
  - Older non-production rows can share the same artifact path as production rows.
  - `prune_old_models()` previously deleted artifact files for pruned rows without checking if kept rows still referenced the same path.
  - This likely caused production artifact drift.
  - Fixed by checking kept entries before unlinking artifacts.
- Artifact repair:
  - Missing artifacts were repaired through training commands, not manual DB updates or copying:
    - minutes via `train_minutes_model(session)` run inside container with `docker exec -i`.
    - stat models via `python main.py train --stat ... --model ...`.
  - First minutes command failed to execute because `docker exec` lacked `-i`; reran with `docker exec -i`.
  - Ensemble `tov` training took a long time due walk-forward CV but completed successfully.
- Live final model health:
  - `registry-health`: latest snapshot `ok`, `missing_count=0`.
  - `model-health`: still `degraded`.
  - ECE no longer the problem:
    - `ece`: `0.0283`
    - OOS ECE in details: `0.0390`
  - Remaining alerts are legitimate:
    - points hit-rate below threshold.
    - feature importance instability.
    - feature drift.
- Live final dashboard data:
  - `featured_date`: `2026-04-25`
  - `best_predictions`: `10`
  - `/api/props`: `340`, source `fastapi_prop_edges`
  - `/api/models`: 8 production, all have test R²
  - `game_logs`: `2026-04-24`
  - `predictions`: `2026-04-25`
  - `prop_lines`: `2026-04-26`
  - `/api/dashboard.accuracy_warnings`: only model-health degraded warning.
- Date/freshness decision:
  - API freshness gate allows one-day lag: `PREDICTION_MAX_GAME_LOG_LAG_DAYS=1`.
  - Dashboard warning now matches this: one-day lag is OK; two or more days stale.
  - `2026-04-26` predictions are blocked with `2026-04-24` game logs because lag is 2 days.
- Important constraints:
  - Do not lower `MIN_CONFIDENCE_THRESHOLD` just to show more picks.
  - HTTP endpoints must not run live inference; they should read stored predictions.
  - Full dashboard lint has unrelated baseline failures in untouched React files; only changed-file lint/build should be claimed.
- Commit state:
  - Final local commit exists: `92cdb88`.
  - Need push to GitHub and probably merge/update `main`.
</technical_details>

<important_files>
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/reports/2026-04-25-dashboard-accuracy-final-status.md`
  - Final status report requested by user.
  - Documents fixes, deployment, validation, live evidence, and remaining true model-health risks.

- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/src/evaluation/calibration.py`
  - Central calibration logic.
  - Modified `compute_calibration()` to fix sparse-bin ECE.
  - Added `compute_ci_z_scores()` and `compute_serving_confidence_scores()`.

- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/src/api/server.py`
  - FastAPI server.
  - Modified `/evaluation/calibration` and `/evaluation/calibration-by-stat` to use served model-signal calibration.
  - Exposes raw-edge ECE separately.

- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/src/notifications/dispatcher.py`
  - `check_model_health()` computes/stores model-health snapshots.
  - Modified ECE/OOS ECE to use served score source and include details keys `ece_score_source` and `oos_ece_score_source`.

- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/src/training/trainer.py`
  - Training and pruning logic.
  - Added `_delete_artifact_if_unreferenced()`.
  - Updated `prune_old_models()` to prevent deleting shared artifacts still referenced by kept entries.

- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/dashboard-ui/server/src/dashboardContracts.ts`
  - Dashboard BFF contract helpers.
  - Added `buildFreshnessWarnings()` and `FreshnessDates`.
  - Aligns dashboard warnings with API one-day freshness gate.

- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/dashboard-ui/server/src/index.ts`
  - Dashboard BFF server.
  - Now uses `buildFreshnessWarnings()` instead of hardcoded 12-hour stale threshold.

- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/tests/test_calibration_extended.py`
  - Tests for CI Platt and new calibration helpers.
  - Added regression tests for sparse-bin ECE and served confidence scoring.

- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/tests/test_alerting.py`
  - Alerting/model-health tests updated for new scoring row shape.

- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/tests/test_sprint56.py`
  - Registry/artifact integrity tests.
  - Added pruning regression test for shared artifacts.

- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/dashboard-ui/server/src/dashboardContracts.test.ts`
  - Dashboard contract tests.
  - Added freshness warning tests.

- `/home/jbl/projects/homelab/compose/compose.nba-ml.yml`
  - NBA ML deployment stack.
  - Relevant services: `nba-ml-api`, `nba-ml-dashboard`, `nba-ml-db`, `nba-ml-mlflow`, `nba-ml-scheduler`.

- `/home/jbl/projects/homelab/scripts/ops/deploy.sh`
  - Existing homelab deploy script.
  - Shows correct `.env` loading and compose pattern.
</important_files>

<next_steps>
Immediate pending work:
1. Push the final commit to GitHub.
   - Current branch: `feature/dashboard-accuracy-final`
   - Local commit: `92cdb88 fix: finish dashboard accuracy hardening`
   - Likely need to push/merge to `main` depending on repo workflow.
2. Mark SQL todo `validate-deploy-report` as `done`.
3. Optionally write MemPalace diary/add drawer for final findings:
   - Final dashboard accuracy hardening completed.
   - Registry prune bug root cause.
   - Served-score calibration endpoint fix.
4. Confirm remote state after push with `git status`/`git log` as needed.

No additional code changes are planned unless push/merge reveals conflicts.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
