---
title: "Copilot Session Checkpoint: Dashboard Accuracy Finalization"
type: text
captured: 2026-04-25T10:53:58.394902Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, mempalace, agents, dashboard]
checkpoint_class: project-progress
checkpoint_class_rule: "body:deployed"
retention_mode: compress
status: success
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Dashboard Accuracy Finalization
**Session ID:** `39cb6a8f-14d7-43a7-bad1-98ec00e06033`
**Checkpoint file:** `/home/jbl/.copilot/session-state/39cb6a8f-14d7-43a7-bad1-98ec00e06033/checkpoints/002-dashboard-accuracy-finalizatio.md`
**Checkpoint timestamp:** 2026-04-25T10:52:56.209470Z
**Exported:** 2026-04-25T10:53:58.394902Z
**Checkpoint class:** `project-progress` (rule: `body:deployed`)
**Retention mode:** `compress`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user is iteratively improving the accuracy and trustworthiness of the NBA ML dashboard at `nba-dashboard.jbl-lab.com`, especially prop predictions, “most confident” picks, model R² display, calibration, stale data handling, and remaining model artifact issues. The approach has been to audit live dashboard/API behavior, implement fixes in isolated git worktrees with TDD and targeted validation, deploy the affected homelab containers, re-evaluate live endpoints, write reports under `nba-ml-engine/reports`, and push changes to GitHub.
</overview>

<history>
1. The user first asked to evaluate `nba-dashboard.jbl-lab.com`, improve accuracy for “Today's Most Confident Predictions,” Props, and “Production Models R² by Stat,” then check the rest of the dashboard and push a report.
   - Loaded NBA/homelab memory and skills; attempted stealth browser but Chrome was unavailable, so pivoted to direct HTTP/API inspection with `curl`.
   - Found `/api/dashboard` showed 354 “confident props” and 10 top predictions, while `/api/props` was empty for the same featured date.
   - Found `/api/models` returned nested `metrics.test_r2`/`metrics.val_r2`, while the React Models page expected top-level `test_r2`, `val_r2`, and `stat_name`.
   - Found confidence was badly calibrated: high-confidence prop tier hit ~48.86%, worse than medium/low; ECE ~0.3661; model health degraded; game logs stale at `2026-04-12`.
   - Created and pushed `reports/2026-04-24-dashboard-accuracy-audit.md` in commit `47a351b`.

2. The user asked to implement the plan, evaluate again, and push a new report.
   - Created an isolated worktree `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-fixes` on `feature/dashboard-accuracy-fixes`.
   - Added tests first in `dashboard-ui/server/src/dashboardContracts.test.ts`.
   - Implemented `dashboard-ui/server/src/dashboardContracts.ts` to normalize model records and FastAPI prop-edge records.
   - Updated the BFF and React UI:
     - `/api/models` normalizes nested metrics for the R² chart.
     - Overview/Props/Rankings use a shared canonical prop-pick source.
     - Props and dashboard expose `data_source`, `empty_reason`, and accuracy warnings.
     - UI wording changed from “Confidence” to “Model Signal.”
   - Deployed `nba-ml-dashboard` from the worktree.
   - Live re-evaluation showed:
     - Models chart fixed: 8 production models with chartable R².
     - Props/Overview/Rankings now consistently showed zero canonical prop picks instead of old uncalibrated SQL-only “confident” picks.
     - Accuracy warnings exposed stale logs, prop/prediction date mismatch, and degraded model health.
   - Wrote `reports/2026-04-25-dashboard-accuracy-implementation-reevaluation.md`.
   - Committed and pushed to `main` as `c0233fe fix: align dashboard accuracy contracts`.

3. The user then asked to complete fixes in the new report, validate/deploy, and create a new status report.
   - Created fresh worktree `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-followups` from `origin/main`.
   - Investigated remaining issues with subagents:
     - Canonical `/prop-edges` empty because all joined candidates were filtered by safety gates, especially low calibrated model signal.
     - Game logs were stale because only regular-season logs were fetched, while current slate was playoff-period.
     - Props history tier data was present under `by_confidence` but needed compatibility aliases.
   - Added TDD tests in `tests/test_dashboard_accuracy_followups.py` and extended dashboard contract tests.
   - Implemented:
     - FastAPI `/prop-edges/diagnostics`.
     - Filter diagnostics in `src/applications/prop_finder.py`.
     - BFF consumption of diagnostics endpoint for specific empty reasons.
     - `main.py ingest --gamelogs`.
     - Freshness gates before `pipeline` and `predict --store`.
     - Playoff game-log ingest in `src/data/nba_ingest.py`.
     - Props-history aliases `confidence_tiers` and `by_confidence_tier`.
   - Deployed rebuilt `nba-ml-api` and `nba-ml-dashboard`.
   - Ran:
     - `python main.py ingest --gamelogs` inside container; eventually ingested Regular Season + Playoffs, 26,427 rows.
     - `python main.py predict --store --date 2026-04-24`; stored 3,647 predictions after freshness gate passed.
     - `python main.py post-retrain`; refreshed CI Platt calibrator on 19,949 samples.
   - Live re-evaluation showed:
     - `game_logs` and `predictions` both current to `2026-04-24`.
     - Props/Overview/Rankings still zero, but now with precise reason: `357` joined candidates, `276` removed by low model signal, `81` by edge caps.
     - Props history now had 4,129 bets and 3 confidence tiers/aliases.
     - Remaining risks: model health degraded, ECE ~0.3663, missing artifacts for `MinutesModel_minutes`, `EnsembleModel_reb`, `EnsembleModel_tov`, and prop lines ahead of predictions.
   - Wrote `reports/2026-04-24-dashboard-accuracy-followup-status.md`.
   - Committed and pushed to `main` as `009d353 fix: harden dashboard prop accuracy signals`.

4. The latest user request was: “finish the remaining accuracy work from the report.”
   - Loaded skills and MemPalace context.
   - Created a fresh worktree `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final` on branch `feature/dashboard-accuracy-final` from `origin/main`, currently at `009d353`.
   - Loaded current plan and homelab references.
   - Main checkout `/home/jbl/projects/nba-ml-engine` is still dirty with unrelated `.github/skills/nba-ml-pipeline/SKILL.md` and behind; do not touch it.
   - Work was interrupted by compaction before investigating or modifying code in `dashboard-accuracy-final`.
</history>

<work_done>
Files created/pushed in earlier turns:
- `reports/2026-04-24-dashboard-accuracy-audit.md`
  - Initial dashboard accuracy audit and proposed fixes.
  - Pushed in commit `47a351b`.
- `dashboard-ui/server/src/dashboardContracts.ts`
  - Shared BFF/dashboard normalization helpers for model metrics, prop edges, props payloads, confidence tiers.
  - Pushed in commit `c0233fe`.
- `dashboard-ui/server/src/dashboardContracts.test.ts`
  - Contract tests for normalized models, prop edge normalization, zero-edge direction, props metadata, history aliases.
  - Pushed and later extended.
- `reports/2026-04-25-dashboard-accuracy-implementation-reevaluation.md`
  - Follow-up report after first implementation/deployment.
  - Pushed in commit `c0233fe`.
- `tests/test_dashboard_accuracy_followups.py`
  - TDD tests for `ingest --gamelogs`, freshness validation, prop-edge empty reasons, and playoff game-log ingestion.
  - Pushed in commit `009d353`.
- `reports/2026-04-24-dashboard-accuracy-followup-status.md`
  - Status report after follow-up fixes, deployment, live validation.
  - Pushed in commit `009d353`.

Files modified/pushed:
- `dashboard-ui/server/src/index.ts`
  - Canonical prop source switched to FastAPI prop-edge diagnostics.
  - Empty reasons and accuracy warnings surfaced.
  - Props history response now includes `confidence_tiers` and `by_confidence_tier`.
  - Stale game-log warning threshold tightened to 12 hours.
- `dashboard-ui/src/lib/api.ts`
  - Added normalized model metric fields, prop metadata, warnings, source/empty-reason types.
- `dashboard-ui/src/pages/DashboardPage.tsx`
  - Accuracy warnings panel and “Model Signal” wording.
- `dashboard-ui/src/pages/props/TodayTab.tsx`
  - Source/empty reason display and “Model Signal” wording.
- `dashboard-ui/src/pages/RankingsPage.tsx`
  - “Confident Props” relabeled to “Prop Signals”; source metadata.
- `dashboard-ui/src/pages/ModelsPage.tsx`
  - R² chart reads normalized top-level metrics and allows valid zero/negative metrics.
- `src/applications/prop_finder.py`
  - Added diagnostics helpers and per-filter counters.
  - Added user-facing empty reason generation.
  - Added diagnostics parameter to `find_edges()`.
- `src/api/server.py`
  - Added `/prop-edges/diagnostics`.
  - Preserved existing `/prop-edges` array contract.
- `main.py`
  - Added `validate_game_log_freshness`.
  - Added `ingest --gamelogs`.
  - Added freshness gates before `pipeline` and `predict --store`.
- `src/data/nba_ingest.py`
  - `ingest_game_logs()` now fetches both `Regular Season` and `Playoffs` by default.
- `config.py`
  - Added `PREDICTION_MAX_GAME_LOG_LAG_DAYS=1`.

Current state:
- `origin/main` has `009d353`.
- Fresh worktree exists:
  - Path: `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final`
  - Branch: `feature/dashboard-accuracy-final`
  - Base: `origin/main` at `009d353`
  - No code changes yet in that worktree as of compaction.
- Deployed services from previous work:
  - `nba-ml-api` and `nba-ml-dashboard` were rebuilt and running.
  - Live last known data:
    - `game_logs`: `2026-04-24`
    - `predictions`: `2026-04-24`
    - `prop_lines`: `2026-04-26`
    - `/api/props`: 0 canonical picks
    - Empty reason: `Canonical prop edge service filtered all 357 joined candidates; low model signal removed 276.`
    - `/api/props/history`: 4,129 bets and 3 tier aliases.
    - `/api/models`: 8 production models chartable.
  - Remaining issues from report:
    - Missing production artifacts for `MinutesModel_minutes`, `EnsembleModel_reb`, `EnsembleModel_tov`.
    - Public calibration ECE remains high around `0.3663`.
    - Model health degraded with calibration error `0.4055`.
    - Prop lines extend beyond predictions (`2026-04-26` vs `2026-04-24`).
</work_done>

<technical_details>
- Important constraints:
  - Do not work directly in the original `main` checkout. It is dirty with unrelated `.github/skills/nba-ml-pipeline/SKILL.md`.
  - Use worktrees under `.worktrees/`; `.worktrees` is gitignored.
  - Preserve rule from lessons: HTTP endpoints must not run live inference; they read stored predictions only.
  - Do not lower `MIN_CONFIDENCE_THRESHOLD` just to show picks. The low-signal gate is intentionally withholding poor-confidence picks.
- Deployment:
  - NBA ML stack is in `/home/jbl/projects/homelab/compose/compose.nba-ml.yml`.
  - API service: `nba-ml-api`, port 8000, built from `Dockerfile`.
  - Dashboard service: `nba-ml-dashboard`, port 8501, built from `Dockerfile.dashboard-react`.
  - Use `NBA_ML_ENGINE_PATH=/home/jbl/projects/nba-ml-engine/.worktrees/<branch>` when deploying from a worktree.
  - Source-built containers require `docker compose build --no-cache <service>` before `up -d`.
- Homelab deployment safety:
  - Existing service redeploy only; no new ports, secrets, or mounts needed unless the final work changes compose.
  - Existing ports: 5000 MLflow, 8000 API, 8501 dashboard.
  - Existing memory headroom is okay; no new stack expected.
- Validation commands used successfully:
  - Python:
    - `.venv/bin/python -m pytest tests/test_dashboard_accuracy_followups.py -q`
    - `.venv/bin/python -m compileall -q main.py config.py src/applications/prop_finder.py src/api/server.py src/data/nba_ingest.py`
  - Dashboard:
    - `cd dashboard-ui && npx eslint server/src/index.ts server/src/dashboardContracts.ts server/src/dashboardContracts.test.ts`
    - `npx tsc -p server/tsconfig.json`
    - `npx tsx --test server/src/dashboardContracts.test.ts`
    - `npm run build`
  - Live endpoint checks via `curl -fsSL -A 'Mozilla/5.0'`.
- Full dashboard lint still has unrelated baseline failures in untouched React files:
  - `FeatureDriftPanel.tsx`, `ModelHealthPanel.tsx`, `NavBar.tsx`, `theme.tsx`, `PlayerPage.tsx`, `SeasonsPage.tsx`.
  - Do not claim full lint passes unless those are fixed; prior work only validated changed files/server.
- Previous Docker build got stricter than local `npm run build` because `Dockerfile.dashboard-react` runs `npx tsc -p server/tsconfig.json`. Always run that before deployment.
- Key lessons from `tasks/lessons.md` relevant now:
  - Missing artifacts can poison production registry; registry must match disk artifacts.
  - Predictor has fallback loading, but fallback is not a true fix for registry drift.
  - Minutes model is first-class and should not be missing.
  - Atomic model saves and artifact verification matter.
  - Calibrator function names/signatures must be checked against source; prior wrong function imports silently skipped refits.
- Live unresolved accuracy issues likely require:
  - Repairing/demoting missing production artifacts (`MinutesModel_minutes`, `EnsembleModel_reb`, `EnsembleModel_tov`) or retraining them.
  - Improving calibration beyond CI Platt refresh; public `/evaluation/calibration` still reports high ECE.
  - Generating predictions for prop-line dates through `2026-04-26` after schedule/props availability, if safe and model artifacts repaired.
- Current direct final worktree baseline likely needs setup:
  - `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final`
  - It may not yet have `.venv` or `dashboard-ui/node_modules` installed.
</technical_details>

<important_files>
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final`
  - Fresh isolated worktree for the latest request.
  - Branch: `feature/dashboard-accuracy-final`.
  - Base: `origin/main` at `009d353`.
- `/home/jbl/.copilot/session-state/39cb6a8f-14d7-43a7-bad1-98ec00e06033/plan.md`
  - Current plan still describes previous follow-up work, not the newest “finish remaining accuracy work” request.
  - Needs updating to focus on final remaining risks: missing artifacts, degraded calibration, prop lines ahead of predictions.
- `reports/2026-04-24-dashboard-accuracy-followup-status.md`
  - Latest status report and source of remaining work.
  - Remaining risks section is the user’s requested target.
- `main.py`
  - Contains `ingest --gamelogs`, `predict --store`, `pipeline`, `post-retrain`, `health-check`, `registry-health`.
  - Likely central to final fixes around retraining/demotion, prediction refresh, calibrator refresh, and artifact repair.
- `src/inference/registry_health.py`
  - Registry/artifact validation utilities; important for missing artifact repair.
  - Needs inspection before final artifact fix.
- `src/inference/predictor.py`
  - Model loading/fallback logic; likely logs missing artifacts and uses fallbacks.
  - Need inspect to understand how missing `minutes`, `reb`, `tov` affect predictions and what safe repair means.
- `src/training/trainer.py`
  - Model registration and artifact save logic; lessons mention `_register_best_model`, `_register_minutes_model`, `assert_artifact_saved`, and atomic saves.
  - Important if implementing a durable fix rather than manual demotion.
- `src/evaluation/calibration.py`
  - Calibration fitting/loading/application; prior `post-retrain` only improved CI Platt, but public ECE remained high.
  - Need inspect for correct ways to fit global/per-stat calibrators and update model health.
- `src/applications/prop_finder.py`
  - Canonical prop-edge filtering and diagnostics.
  - Currently correctly withholds low-signal picks; do not bypass without calibration evidence.
- `dashboard-ui/server/src/index.ts`
  - BFF warnings/status display; may need updates if final work introduces new status fields.
- `/home/jbl/projects/homelab/compose/compose.nba-ml.yml`
  - Deployment stack and Ofelia schedules.
  - May need update if adding scheduled calibration/registry repair, but avoid unless necessary.
- `tasks/lessons.md`
  - Contains important historical gotchas, especially registry drift and calibration failures.
</important_files>

<next_steps>
Immediate next steps after compaction:
1. Update `/home/jbl/.copilot/session-state/39cb6a8f-14d7-43a7-bad1-98ec00e06033/plan.md` for the new request:
   - Problem: finish remaining risks from `2026-04-24-dashboard-accuracy-followup-status.md`.
   - Tasks:
     - Diagnose missing production artifacts and decide safe repair/demotion/retrain path.
     - Improve calibration/model-health status or run correct calibrator refresh workflow.
     - Address prop lines ahead of predictions by safe prediction refresh for latest prop dates if schedules/data are available.
     - Validate/deploy/re-evaluate.
     - Write final status report and push.
2. Create SQL todos for the new request, e.g.:
   - `diagnose-final-accuracy-risks`
   - `repair-production-artifacts`
   - `improve-calibration-health`
   - `sync-prop-prediction-dates`
   - `validate-deploy-final`
   - `write-final-status-report`
3. Set up baseline in the final worktree:
   - `cd /home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final`
   - likely create `.venv` and install requirements if Python tests needed.
   - `cd dashboard-ui && npm ci --quiet` if dashboard validation needed.
4. Launch focused research agents if helpful:
   - One to inspect registry/artifact mismatch and propose safe repair.
   - One to inspect calibration pipeline/public ECE and propose correct fixes.
   - One to inspect prop line/prediction date mismatch and safe prediction refresh path.
5. Before changing code, inspect:
   - `reports/2026-04-24-dashboard-accuracy-followup-status.md`
   - `src/inference/registry_health.py`
   - `src/inference/predictor.py`
   - `src/training/trainer.py`
   - `src/evaluation/calibration.py`
   - `main.py`
   - live DB state for `model_registry`, artifact paths, latest dates.
6. Use TDD for any code changes. Do not manually fix without tests.
7. If repairing live model artifacts, be cautious:
   - Do not demote/poke DB blindly.
   - Prefer existing CLI/retrain/registry-health mechanisms if available.
   - If a one-time DB repair is needed, document and include report evidence.
8. After code/ops:
   - Rebuild affected containers with `--no-cache`.
   - Redeploy only needed services.
   - Re-run live endpoint checks.
   - Write a new report under `reports/`.
   - Commit with required trailer and push to `main`.

Open questions/blockers:
- Need determine whether missing artifacts should be solved by retraining, registry demotion to fallback models, copying existing artifacts, or changing promotion logic.
- Need determine why public calibration ECE remains high even after `post-retrain`; may require fitting global/per-stat confidence calibrators, not only CI Platt.
- Need determine whether predictions can/should be generated for `2026-04-26` now, and whether schedule/game context exists.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
