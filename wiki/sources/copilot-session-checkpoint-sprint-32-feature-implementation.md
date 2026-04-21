---
title: "Copilot Session Checkpoint: Sprint 32 feature implementation"
type: source
created: 2026-03-28
last_verified: 2026-04-21
source_hash: "040b44d153750c1dc753a2e74e3c649fe6ac28ede67f756d2afff361b9f3abc2"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-32-feature-implementation-648fcb7c.md
quality_score: 100
concepts:
  []
related:
  - "[[Homelab]]"
tier: archive
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, agents, dashboard]
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: validated
---

# Copilot Session Checkpoint: Sprint 32 feature implementation

## Summary

The user asked to diagnose and fix a stuck training pipeline on the nba-ml-api homelab deployment, deploy Sprint 31 (committed but not deployed), and then implement all Sprint 31 next steps (high, medium, low priority) as Sprint 32. The environment is `server` mode on `beelink-gti13`. The approach was: diagnose pipeline → fix root cause → deploy Sprint 31 → implement Sprint 32 features using parallel sub-agents for independent work streams.

## Key Points

- H2: Fit calibrator on production data (ECE 0.36 → 0.0)
- H3: Rolling window analysis endpoint fix (config attr bug)
- M4: Feature drift monitoring module + API endpoint
- M5: Backup script created (compose changes NOT yet applied)
- M6: Model degradation alerting (ECE, hit rate, drift checks)
- L8: Phase 2 Platt scaling for ci_confidence

## Execution Snapshot

## Files Created
- `src/evaluation/feature_drift.py` — Feature drift monitoring via PSI (281 lines)
- `scripts/backup_db.sh` — Automated pg_dump backup script with retention policy
- `dashboard-ui/src/components/shared/ThemeToggle.tsx` — Dark mode toggle component
- `tasks/PROGRESS-sprint32-monitoring-backups-calibration-0328.md` — Sprint 32 progress tracker
- `docs/reports/sprint31-auth-calibration-ui.md` — Already existed (Sprint 31 report)

## Files Modified
- `main.py` — Added SIGALRM pipeline timeout enforcement + PipelineTimeout exception handling
- `src/data/nba_ingest.py` — Added consecutive failure bail-out in tracking stats loop
- `src/api/server.py` — Fixed `config.CURRENT_SEASON` → `config.NBA_CURRENT_SEASON`; added `/calibration/fit-ci-platt` and `/evaluation/feature-drift` endpoints
- `src/evaluation/calibration.py` — Added CI Platt calibrator: `fit_ci_platt_calibrator()`, `load_ci_platt_calibrator()`, `apply_ci_platt()`
- `src/applications/prop_finder.py` — Load CI Platt calibrator; use `apply_ci_platt()` instead of hardcoded `1/(1+exp(-1.7*z))`
- `src/notifications/dispatcher.py` — Added `send_alert()`, `check_model_health()` for model degradation alerting
- `dashboard-ui/server/src/index.ts` — Extended `cached()` to models (10min), injuries (5min), CLV (5min), calibration (10min) endpoints
- `dashboard-ui/src/components/shared/ThemeToggle.tsx` — Created (dark mode toggle)
- Dashboard NavBar/App — Updated to include ThemeToggle

## Work Completed
- [x] H2: Fit calibrator on production data (ECE 0.36 → 0.0)
- [x] H3: Rolling window analysis endpoint fix (config attr bug)
- [x] M4: Feature drift monitoring module + API endpoint
- [x] M5: Backup script created (compose changes NOT yet applied)
- [x] M6: Model degradation alerting (ECE, hit rate, drift checks)
- [x] L8: Phase 2 Platt scaling for ci_confidence
- [x] L9: BFF caching extended to 4 more endpoints
- [x] L10: Dark mode toggle created
- [ ] M7: Test coverage for new modules (NOT YET DONE)
- [ ] Deploy Sprint 32 to homelab (NOT YET DONE)
- [ ] Write Sprint 32 report (NOT YET DONE)
- [ ] Compose file backup changes (NOT applied — agent failed to modify)
- [ ] Backup directory creation (sudo needed)
- [ ] H3: Actually call rolling-window-analysis after the fix and document results

## Current State
- Branch: `feature/sprint-32-monitoring-backups-calibration` (NOT committed yet — all changes are unstaged)
- Sprint 31 is deployed and running on homelab
- Sprint 32 code exists locally but is NOT deployed
- API is healthy, serving Sprint 31 code
- Calibrator is fitted on production data
- Odds API returning 401 (key expired) — SportsGameOdds fallback handles it

## Technical Details

- Daily pipeline runs 8 steps: ingest → schedule → injuries → props → game lines → train → predict → QA
- Scheduler is Ofelia (mcuadros/ofelia:latest) using Docker labels for cron jobs (6-field with seconds)
- `docker exec -d` detaches from container logs — output must be redirected to `/tmp/pipeline.log` for monitoring
- Training process is spawned via `docker exec` into `nba-ml-api` container (not PID 1), so container stays healthy even if training dies ### Pipeline Timeout Fix
- `signal.SIGALRM` used for pipeline timeout on Linux — sets alarm for `config.PIPELINE_TOTAL_TIMEOUT` (8 hours)
- `PipelineTimeout` exception caught separately from general exceptions to send notification without re-raising
- Old signal handler saved and restored in `finally` block ### Tracking Stats Bail-out
- Each failed game takes ~330s (60s timeout × 3 attempts + 30+120s backoff)
- Consecutive failure counter resets to 0 on success, triggers bail-out at 3
- Without fix: 20 games × 330s = 110 min; with fix: 3 games × 330s = ~17 min ### Calibrator Details
- Isotonic calibration on 7583 samples gave ECE=0.0 (in-sample perfect — expected for isotonic)
- CI Platt calibrator replaces heuristic `1/(1+exp(-1.7*z))` with LogisticRegression fitted on (z_score, hit) pairs
- Calibrator saved to `models/calibrators/confidence_calibrator.pkl` and `ci_platt_calibrator.pkl`
- Confidence blend: `0.4 * ci_confidence + 0.6 * clf_directional`, then post-hoc calibration ### Feature Drift
- Uses PSI (Population Stability Index) with 10 quantile-based bins from reference distribution
- PSI < 0.1 = no drift, 0.1-0.2 = moderate, >0.2 = significant
- `detect_training_inference_drift()` builds features via `build_features()` and splits by date ### Homelab Deploy Pattern
- Compose: `docker compose --env-file .env -f compose/compose.nba-ml.yml up -d`
- Build: `docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache <service>`
- Source code path: `NBA_ML_ENGINE_PATH` in `.env`
- Models volume: `${HOMELAB_BASE}/data/nba-ml/models:/app/models`
- HOMELAB_BASE=/opt/homelab ### Known Issues
- Odds API key returning 401 — SportsGameOdds provides fallback (972 → 570 prop lines)
- NBA stats.nba.com BoxScorePlayerTrackV3 endpoint frequently times out
- 1104 games missing tracking stats (historical backfill gap)
- Compose file backup job NOT yet added (agent failed to modify the file)
- `sudo` commands for backup directory creation need interactive password ### Config Naming
- Use `config.NBA_CURRENT_SEASON` NOT `config.CURRENT_SEASON` (the latter doesn't exist)
- `config.MODELS_DIR` (Path) NOT `config.MODEL_DIR`
- `config.PIPELINE_TRACKING_MAX_GAMES` controls tracking stats limit (default 20) ### Alert Thresholds (in dispatcher.py)
- `ALERT_ECE_THRESHOLD`: 0.40 (configurable via config attrs)
- `ALERT_HITRATE_FLOOR`: 0.50
- `ALERT_HITRATE_DAYS`: 7

## Important Files

- `main.py`
- CLI entry point for all commands (pipeline, train, predict, ingest, etc.)
- Added SIGALRM timeout enforcement in `pipeline()` function (~lines 551-695)
- `PipelineTimeout` class and handler defined inside `pipeline()`

- `src/data/nba_ingest.py`
- Data ingestion from NBA API, ESPN, etc.
- Added consecutive failure bail-out in `ingest_game_tracking_stats()` (~lines 1808-1830)
- `_call_nba_endpoint()` at lines 89-123 handles retries with backoff

- `src/api/server.py`
- FastAPI server with all REST endpoints
- Fixed bug at line 1009: `config.CURRENT_SEASON` → `config.NBA_CURRENT_SEASON`
- Added `POST /calibration/fit-ci-platt` endpoint (~line 1153+)
- Added `GET /evaluation/feature-drift` endpoint (~line 1220+)

- `src/evaluation/calibration.py`
- Calibration analysis and post-hoc calibrators
- Added `fit_ci_platt_calibrator()`, `load_ci_platt_calibrator()`, `apply_ci_platt()` at end of file
- `CI_CALIBRATOR_PATH = CALIBRATOR_DIR / "ci_platt_calibrator.pkl"`

- `src/evaluation/feature_drift.py`
- NEW: Feature drift monitoring via PSI (281 lines)
- `compute_feature_drift()`, `detect_training_inference_drift()`, `format_drift_alert()`

- `src/applications/prop_finder.py`
- Prop line edge finder — computes confidence scores
- Updated to load CI Platt calibrator (~lines 113-135)
- Updated ci_confidence computation to use fitted Platt sigmoid (~lines 154-167)

- `src/notifications/dispatcher.py`
- Notification system using apprise
- Added `send_alert()` and `check_model_health()` for model degradation alerting

- `scripts/backup_db.sh`
- NEW: pg_dump backup script with 7-daily/4-weekly retention

- `dashboard-ui/server/src/index.ts`
- BFF (Express/Hono) server — queries Postgres directly
- Extended `cached()` usage to models, injuries, CLV, calibration endpoints

- `dashboard-ui/src/components/shared/ThemeToggle.tsx`
- NEW: Dark mode toggle with localStorage persistence

- `~/projects/homelab/compose/compose.nba-ml.yml`
- Docker compose for all nba-ml services
- NEEDS: backup volume mount for nba-ml-db, backup script mount, Ofelia cron job label

- `config.py`
- Central config: `PIPELINE_TOTAL_TIMEOUT=28800`, `PIPELINE_TRACKING_MAX_GAMES=20`, `NBA_CURRENT_SEASON`, `MODELS_DIR`, `APPRISE_URLS`

- `tasks/PROGRESS-sprint32-monitoring-backups-calibration-0328.md`
- Sprint 32 progress tracker

## Next Steps

## Remaining Work

### Must Do Before Deploy
1. **Compose file changes for backups** — Agent didn't actually modify `~/projects/homelab/compose/compose.nba-ml.yml`. Need to:
- Add `${HOMELAB_BASE}/data/nba-ml/backups:/backups` volume to nba-ml-db
- Add `${NBA_ML_ENGINE_PATH}/scripts/backup_db.sh:/usr/local/bin/backup_db.sh:ro` volume to nba-ml-db
- Add Ofelia cron label: `ofelia.job-exec.db-backup.schedule: "0 0 5 * * *"` / container: nba-ml-db / command: `/bin/bash /usr/local/bin/backup_db.sh`

2. **Create backup directory** — `sudo mkdir -p /opt/homelab/data/nba-ml/backups && sudo chown 999:999 /opt/homelab/data/nba-ml/backups` (needs sudo password)

3. **M7: Write tests** — Need tests for:
- Feature drift module (`test_feature_drift.py`)
- CI Platt calibrator functions
- New API endpoints (feature-drift, ci-platt-fit)
- Model health check alerting

4. **H3: Re-run rolling window analysis** — The config bug is fixed locally but not deployed. After deploy, call the endpoint and document results.

5. **Commit Sprint 32 changes** — All changes are unstaged on `feature/sprint-32-monitoring-backups-calibration`

6. **Verify BFF/dashboard changes** — ThemeToggle and caching changes need TypeScript build verification

### Deploy Sequence
1. Commit all Sprint 32 changes to branch
2. Merge to main, push
3. Apply compose changes to homelab repo
4. `docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache nba-ml-api nba-ml-dashboard`
5. `docker compose --env-file .env -f compose/compose.nba-ml.yml up -d`
6. Verify: API health, new endpoints, dashboard loads, dark mode toggle, backup cron
7. Call `POST /calibration/fit-ci-platt?days=60` to fit CI Platt calibrator
8. Call `GET /evaluation/rolling-window-analysis` to verify fix
9. Call `GET /evaluation/feature-drift` to verify drift monitoring

### Post-Deploy
- Write Sprint 32 report (`docs/reports/sprint32-monitoring-backups-calibration.md`)
- Update progress tracker
- Add health check to daily pipeline (call `check_model_health()` as Step 8)
- Update lessons.md if any new patterns discovered

### SQL Todo Status
- `h2-fit-calibrator`: done
- `h3-rolling-analysis`: in_progress (bug fixed, needs re-test after deploy)
- `m4-feature-drift`: in_progress (code done, needs tests)
- `m5-db-backups`: in_progress (script done, compose changes needed)
- `m6-alerting`: in_progress (code done, needs integration into pipeline)
- `m7-test-coverage`: pending (not started)
- `l8-platt-ci`: in_progress (code done, needs deploy + fit)
- `l9-bff-cache`: in_progress (code done by agent, needs verify)
- `l10-dark-mode`: in_progress (code done by agent, needs verify)
- `deploy-verify`: pending (blocked on above)
- `report-write`: pending (blocked on deploy)

## Related Wiki Pages

- [[Homelab]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-32-feature-implementation-648fcb7c.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-28 |
| URL | N/A |
