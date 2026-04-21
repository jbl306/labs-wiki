---
title: "Copilot Session Checkpoint: Sprint 33 drift-aware training deployment"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard]
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint 33 drift-aware training deployment
**Session ID:** `8d466128-8017-482d-b021-0fffe970d5eb`
**Checkpoint file:** `/home/jbl/.copilot/session-state/8d466128-8017-482d-b021-0fffe970d5eb/checkpoints/002-sprint-33-drift-aware-training.md`
**Checkpoint timestamp:** 2026-03-29T00:16:33.281544Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user asked to diagnose/fix a stuck training pipeline on the nba-ml-api homelab deployment, deploy Sprint 31 (committed but not deployed), then implement all Sprint 31 next steps as Sprint 32, and finally implement all Sprint 32 next steps as Sprint 33. The environment is `server` mode on `beelink-gti13` with local Docker containers. The approach was: fix pipeline → deploy Sprint 31 → implement Sprint 32 (monitoring, backups, calibration, UI) → implement Sprint 33 (drift-aware training, browser fallback, dashboard drift panel) using parallel sub-agents for independent work streams.
</overview>

<history>
1. User asked to check stuck training pipeline, fix it, and deploy Sprint 31
   - Discovered NBA BoxScorePlayerTrackV3 API timing out, causing pipeline hangs
   - Fixed: Added consecutive failure bail-out (3 failures → skip) in `nba_ingest.py`
   - Fixed: Added SIGALRM-based pipeline timeout enforcement in `main.py`
   - Merged Sprint 31 branch to main, rebuilt Docker images, deployed
   - Pipeline ran but failed at Step 5 (Training) with DB connection drop — known issue for long runs

2. User invoked `execute-sprint-from-report` to implement Sprint 31 next steps as Sprint 32
   - Created branch `feature/sprint-32-monitoring-backups-calibration`
   - Implemented all 11 items (H2, H3, M4-M7, L8-L10):
     - Feature drift monitoring via PSI (`src/evaluation/feature_drift.py`)
     - CI Platt calibrator replacing hardcoded logistic
     - Model health alerting (ECE, hit rate, drift checks)
     - Health check CLI command + pipeline Step 8/9
     - DB backup script with retention + Ofelia cron
     - BFF caching for 4 more endpoints
     - Dark mode toggle
     - 32 new tests (feature drift, calibration, alerting)
   - Fixed bugs: `config.CURRENT_SEASON` → `config.NBA_CURRENT_SEASON`, `ci_upper/lower` → `confidence_high/low`, missing pandas import
   - Deployed, verified all endpoints, wrote Sprint 32 report
   - Committed and pushed to GitHub + homelab repo

3. User invoked `execute-sprint-from-report` to implement Sprint 32 next steps as Sprint 33
   - Created branch `feature/sprint-33-drift-aware-training`
   - Ran comprehensive audit via explore agent
   - Implemented high priority items:
     - H1: Browser tracking fallback in daily pipeline (curl_cffi when NBA API fails after 3 consecutive failures)
     - H2: Drift-aware feature exclusion in trainer (PSI > 5.0 → auto-exclude, safety floor of 10 features)
     - H3: Auto-refit calibrators after weekly retrain (pipeline Step 5c with both isotonic and CI Platt)
   - Implemented medium priority items via parallel agents:
     - M4: Backup verification script (`scripts/verify_backup.sh`) + monthly Ofelia cron
     - M5: Feature importance comparison CLI (`feature-importance-drift` command)
     - M6: Dashboard feature drift visualization (Recharts horizontal bar chart on HealthPage)
     - M7: Integration test framework with pytest marker
   - Fixed TS build error in FeatureDriftPanel.tsx (Recharts Tooltip formatter type incompatibility — used `as any` cast)
   - Merged to main, pushed, rebuilt both Docker images, deployed
   - All endpoints verified: health OK, model health healthy, feature drift returning 12 drifted features, dashboard 302
   - Attempted to run integration tests but they're not in the Docker container (tests dir not copied in Dockerfile)
</history>

<work_done>
## Sprint 32 Files (already committed and deployed)
- `src/evaluation/feature_drift.py` — NEW: PSI-based drift monitoring (281 lines)
- `src/evaluation/calibration.py` — Added CI Platt calibrator functions
- `src/notifications/dispatcher.py` — Added `send_alert()`, `check_model_health()`
- `src/api/server.py` — 3 new endpoints, 3 bug fixes
- `src/applications/prop_finder.py` — CI Platt calibrator integration
- `config.py` — Alert threshold config vars
- `main.py` — `health-check` CLI, pipeline Step 8/9, SIGALRM timeout
- `src/data/nba_ingest.py` — Tracking stats bail-out
- `scripts/backup_db.sh` — pg_dump backup with retention
- `dashboard-ui/` — BFF caching, ThemeToggle, theme lib
- `tests/test_feature_drift.py`, `tests/test_calibration_extended.py`, `tests/test_alerting.py` — 32 tests
- `docs/reports/sprint32-monitoring-backups-calibration.md` — Sprint 32 report

## Sprint 33 Files (committed, deployed, verified)
- `config.py` — Added `TRACKING_BROWSER_FALLBACK`, `DRIFT_AWARE_TRAINING`, `DRIFT_PSI_EXCLUSION_THRESHOLD`
- `src/data/nba_ingest.py` — Added `_tracking_browser_fallback()` function + wiring after bail-out
- `src/training/trainer.py` — Added `_exclude_drifted_features()` function + integration into `train_all()`
- `main.py` — Added `health-check` enhancements, `feature-importance-drift` CLI command, calibrator refit in pipeline Step 5c, `--exclude-tracking` flag for `analyze-features`
- `scripts/verify_backup.sh` — NEW: Backup verification with temp DB restore
- `dashboard-ui/src/components/charts/FeatureDriftPanel.tsx` — NEW: Drift visualization
- `dashboard-ui/src/lib/api.ts` — Added `FeatureDriftData` types + `api.featureDrift()`
- `dashboard-ui/src/pages/HealthPage.tsx` — Integrated FeatureDriftPanel
- `dashboard-ui/server/src/index.ts` — BFF proxy for feature-drift with cache
- `tests/test_drift_training.py` — NEW: Tests for drift exclusion + browser fallback
- `tests/integration/` — NEW: Integration test framework (test_api_live.py)
- `pytest.ini` — Added integration marker, default excludes integration tests
- `tasks/PROGRESS-sprint33-drift-aware-training-0328.md` — Progress tracker

## Homelab Compose Changes (committed to ~/projects/homelab)
- `compose/compose.nba-ml.yml` — Added backup volumes, backup cron, health check cron, backup-verify cron + volume mount

## Current State
- Branch: `main` (Sprint 33 merged, pushed to GitHub)
- Homelab: All containers running with Sprint 33 code
- API: Healthy, all endpoints verified
- Dashboard: Running (302 → login)
- Integration tests: Created but can't run from host (no pytest) or container (tests dir not in Docker image)
- Low priority items L8/L9/L10 not implemented (tracking backfill, Grafana, prop sources)

## SQL Todo Status
- All H1-H3, M4-M7: done
- deploy-verify: pending (endpoints verified but integration tests didn't run)
- L8/L9/L10: pending (deferred)
- report-write: pending
</work_done>

<technical_details>
### Pipeline Architecture
- Daily pipeline runs steps: ingest → schedule → injuries → props → game lines → train → predict → QA → health check
- Step 5c (new): Auto-refit both isotonic and CI Platt calibrators after training
- Scheduler: Ofelia (mcuadros/ofelia:latest) with Docker labels for cron (6-field with seconds)
- `docker exec -d` detaches — output must be redirected to `/tmp/pipeline.log`

### Browser Tracking Fallback (H1)
- `_tracking_browser_fallback()` in `nba_ingest.py` retries failed games via `nba_browser._browser_get()`
- Uses curl_cffi with Chrome TLS impersonation to bypass stats.nba.com bot protection
- Triggered automatically after 3 consecutive NBA API failures when `config.TRACKING_BROWSER_FALLBACK=True`
- Browser fallback bails after 5 consecutive failures itself

### Drift-Aware Training (H2)
- `_exclude_drifted_features()` in `trainer.py` compares oldest 50% (reference) vs newest 30% (current) of training data
- Uses PSI from `feature_drift.compute_feature_drift()` with threshold `config.DRIFT_PSI_EXCLUSION_THRESHOLD` (default 5.0)
- Safety: never drops below 10 features even with massive drift
- Runs after VIF pruning, before final feature selection in `train_all()`

### Calibrator Auto-Refit (H3)
- Pipeline Step 5c calls `fit_calibrator()` (isotonic) and `fit_ci_platt_calibrator()` (logistic)
- CI Platt query uses `confidence_high`/`confidence_low` columns (NOT `ci_upper`/`ci_lower`)
- Fitted result from Sprint 32: A=0.8846, B=-0.1532 (vs hardcoded 1.7)

### Key Bugs Fixed
1. `config.CURRENT_SEASON` doesn't exist → use `config.NBA_CURRENT_SEASON`
2. Predictions table columns: `confidence_high`/`confidence_low`, NOT `ci_upper`/`ci_lower`
3. Missing `import pandas as pd` in lazy-loaded endpoint functions
4. Recharts Tooltip `formatter` type incompatibility — cast with `as any`

### Deploy Pattern
- Compose: `docker compose --env-file .env -f compose/compose.nba-ml.yml up -d`
- Build: `docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache <service>`
- Source path: `NBA_ML_ENGINE_PATH=../../nba-ml-engine` (relative to compose dir)
- Models volume: `${HOMELAB_BASE}/data/nba-ml/models:/app/models`
- HOMELAB_BASE=/opt/homelab

### Feature Drift in Production
- 12 drifted features out of 308 total (all `trk_*` tracking features)
- PSI >10 for tracking features — expected since NBA BoxScorePlayerTrackV3 API has been down
- Non-tracking features stable (PSI <0.2)

### Ofelia Cron Jobs (current)
- pipeline-daily: 07:00 UTC
- props-refresh: 22:00 UTC
- predict-refresh: 22:15 UTC
- weekly-retrain: 16:00 UTC Sundays
- post-retrain-analysis: 20:00 UTC Sundays
- db-backup: 05:00 UTC daily
- health-check: 23:00 UTC daily
- backup-verify: 06:00 UTC 1st of month

### Integration Tests Issue
- `tests/integration/` directory created but Dockerfile doesn't copy test files into container
- Can't run from host because pytest/requests not installed on beelink-gti13
- Tests require `NBA_ML_API_KEY` env var
</technical_details>

<important_files>
- `main.py`
  - CLI entry point for all commands
  - Sprint 33: Added `feature-importance-drift` CLI (~lines 575-640), calibrator refit Step 5c (~lines 680-730), `timedelta` import fix
  - Pipeline function has SIGALRM timeout, 9 steps total

- `src/data/nba_ingest.py`
  - Data ingestion from NBA API
  - Sprint 33: Added `_tracking_browser_fallback()` (~lines 1758-1855), wired into bail-out block (~lines 1920-1930)

- `src/training/trainer.py`
  - Model training with feature selection, VIF pruning
  - Sprint 33: Added `_exclude_drifted_features()` (~lines 115-170), called after VIF pruning in `train_all()` (~line 430)

- `config.py`
  - Sprint 33: Added `TRACKING_BROWSER_FALLBACK`, `DRIFT_AWARE_TRAINING`, `DRIFT_PSI_EXCLUSION_THRESHOLD` (~lines 106-110)
  - Sprint 32: Added `ALERT_ECE_THRESHOLD`, `ALERT_HITRATE_FLOOR`, etc.

- `src/evaluation/feature_drift.py`
  - PSI-based drift monitoring (281 lines, created Sprint 32)
  - Used by trainer's drift exclusion and API endpoint

- `dashboard-ui/src/components/charts/FeatureDriftPanel.tsx`
  - NEW: Drift visualization with Recharts horizontal bar chart
  - Fixed Tooltip formatter type issue (line 121: `as any` cast)

- `dashboard-ui/server/src/index.ts`
  - BFF server — queries Postgres directly + proxies to FastAPI
  - Sprint 33: Added `/api/evaluation/feature-drift` proxy with 10min cache

- `scripts/verify_backup.sh`
  - NEW: Backup verification script (restore test to temp DB)
  - Runs monthly via Ofelia cron

- `~/projects/homelab/compose/compose.nba-ml.yml`
  - Docker compose for all nba-ml services
  - Sprint 33: Added verify_backup volume mount, backup-verify cron label

- `tests/test_drift_training.py`
  - NEW: Tests for drift exclusion + browser fallback
  - TestExcludeDriftedFeatures (4 tests), TestTrackingBrowserFallback (2 tests)

- `tests/integration/test_api_live.py`
  - NEW: Integration tests against live Docker containers
  - Requires NBA_ML_API_KEY, run with `pytest -m integration`
  - Cannot currently run (not in Docker image, no pytest on host)

- `docs/reports/sprint32-monitoring-backups-calibration.md`
  - Sprint 32 report (source of Sprint 33 next steps)

- `tasks/lessons.md`
  - Sprint 32 lessons: column name mismatch, missing imports in lazy endpoints
</important_files>

<next_steps>
## Remaining Work

### Immediate (Sprint 33 completion)
1. **Write Sprint 33 report** — `docs/reports/sprint33-drift-aware-training.md` with all findings, validation results, and next steps
2. **Update progress tracker** — Mark all items complete in `tasks/PROGRESS-sprint33-drift-aware-training-0328.md`
3. **Add lessons to `tasks/lessons.md`** — Recharts Tooltip type cast, integration test Docker issue
4. **Commit report and push** — Final commit on main

### Low Priority (deferred from Sprint 33)
- L8: Backfill 1,104 games tracking stats via browser method
- L9: Grafana dashboards for model health metrics
- L10: Explore alternative prop line sources (Odds API key expired)

### Known Issues
- Integration tests can't run from host (no pytest) or container (tests/ not in Docker image) — need to either install pytest on host or add test files to Dockerfile
- Odds API returning 401 (key expired) — SportsGameOdds fallback covers ~570 prop lines
- NBA BoxScorePlayerTrackV3 API consistently down — browser fallback now handles this

### SQL Todo Status
All H1-H3, M4-M7: done | deploy-verify, L8-L10, report-write: pending
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
