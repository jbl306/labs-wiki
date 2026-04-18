---
title: "Copilot Session Checkpoint: Sprint 38 and documentation audit"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard]
status: pending
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint 38 and documentation audit
**Session ID:** `8d466128-8017-482d-b021-0fffe970d5eb`
**Checkpoint file:** `/home/jbl/.copilot/session-state/8d466128-8017-482d-b021-0fffe970d5eb/checkpoints/007-sprint-38-and-documentation-au.md`
**Checkpoint timestamp:** 2026-03-30T11:12:44.432575Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user is iterating on the NBA ML Engine project through sprint-based development on a homelab server (beelink-gti13). This session segment focused on implementing Sprint 38 (Sprint 34 remaining next steps): PSI drift snapshot storage, model health time series dashboard, GitHub Actions CI/CD pipeline, and feature importance drift analysis. The approach followed the execute-sprint-from-report skill workflow: audit existing state, plan, implement, deploy, verify, report, and commit.
</overview>

<history>
1. Prior context: Sprints 31-37 were already completed in earlier conversation segments
   - Sprint 37 deployed PRA predictions, model health snapshots, dashboard analytics
   - Alt-line contamination fix: `primary_props` CTE in BFF queries to filter SGO DraftKings alternate lines
   - One-sided prop filter: Reject prop lines with NULL over_odds or under_odds (814 lines + 1840 snapshots cleaned)
   - Kelly bankroll simulator fixed: quarter-Kelly (0.25×) with 25% daily exposure cap
   - History corrected: 1,070 bets, 53.3% hit rate, +70u flat (6.5% ROI)

2. User requested: "implement all of sprint 34 next steps except full retrain"
   - Invoked execute-sprint-from-report skill
   - Read Sprint 34 report (`docs/reports/sprint34-dashboard-accuracy.md`) to identify next steps
   - Audited codebase to determine which items were already done from prior sprints:
     - ✅ Model-health to background job (Sprint 37 - ModelHealthSnapshot)
     - ✅ PRA prediction generation (Sprint 37 - predictor.py sums pts+reb+ast)
     - ✅ Historical backfill via browser method (Sprint 37)
     - ✅ Z-score confidence calibration (existing)
     - ✅ Feature importance drift CLI (`feature-importance-drift` command already existed)
   - Identified remaining items to implement:
     - PSI drift snapshot DB storage + trend endpoint
     - Model health time series dashboard panel
     - GitHub Actions CI/CD pipeline
   - Created branch `feature/sprint-38-s34-next-steps`

3. Implementation phase (parallelized via sub-agents):
   - **Backend agent**: Added DriftSnapshot model, updated dispatcher to batch-insert PSI values, added `/evaluation/model-health/history` and `/evaluation/drift-trends` API endpoints, created Alembic migration `011_add_drift_snapshots.py`
   - **CI/CD agent**: Created `.github/workflows/ci.yml` with python-tests and dashboard-build jobs
   - **Dashboard work** (done directly): Added ModelHealthPanel component, BFF proxy endpoints for model-health/history/drift-trends, API types in api.ts, integrated panel into HealthPage

4. Deployment and verification:
   - Created `drift_snapshots` table via psql
   - Built and deployed both nba-ml-api and nba-ml-dashboard containers
   - Initial health check failed: SQLAlchemy `::jsonb` cast syntax broke parameter binding
   - Fixed by changing `::jsonb` to `CAST(:param AS jsonb)` in dispatcher.py
   - Rebuilt and redeployed API
   - Seeded health check: 308 drift snapshots stored, model health snapshot persisted (degraded, 1 alert - 6 drifted features)
   - Verified all endpoints: model-health (ECE=0.362, HR=53.2%, drift=6), health history (1 snapshot), drift trends (top 5 features)
   - Dashboard HTTP 200, BFF proxies all working
   - Restarted tracking backfill (killed by container recreation)

5. Committed Sprint 38: 11 files, +694 lines, merged to main, pushed to GitHub

6. User requested: "update all documentation based on sprint changes"
   - Launched explore agent to audit ALL documentation files
   - Comprehensive audit completed identifying gaps across README.md, docs/02-data-layer.md, docs/06-applications.md, docs/07-deployment.md
   - Key gaps found:
     - README missing 9+ DB tables, 7+ API endpoints, CI/CD mention
     - 02-data-layer.md missing drift_snapshots and model_health_snapshots tables
     - 06-applications.md missing prop history/P&L, PRA composite, one-sided prop filtering, model health monitoring
     - 07-deployment.md has placeholder CI/CD section (wrong workflow content), missing actual ci.yml details
   - Read all 4 files that need updating (README.md, 02-data-layer.md, 06-applications.md, 07-deployment.md)
   - **Work was interrupted at this point** — files have been read but edits not yet applied
</history>

<work_done>
## Files Created (Sprint 38):
- `.github/workflows/ci.yml` — GitHub Actions CI: pytest + TypeScript build on push/PR to main
- `alembic/versions/011_add_drift_snapshots.py` — Migration for drift_snapshots table
- `dashboard-ui/src/components/charts/ModelHealthPanel.tsx` — Model health status card + ECE/hit rate trend charts
- `docs/reports/sprint38-s34-next-steps.md` — Sprint 38 report
- `tasks/PROGRESS-sprint38-s34-next-steps-0330.md` — Progress tracker

## Files Modified (Sprint 38):
- `src/db/models.py` — Added DriftSnapshot model (feature_name, psi_value, drift_status, window params)
- `src/notifications/dispatcher.py` — PSI snapshot batch-insert after drift analysis + JSONB cast fix (`::jsonb` → `CAST AS jsonb`)
- `src/api/server.py` — Added `/evaluation/model-health/history` and `/evaluation/drift-trends` endpoints
- `dashboard-ui/server/src/index.ts` — Added 3 BFF proxy endpoints (model-health, history, drift-trends)
- `dashboard-ui/src/lib/api.ts` — Added ModelHealthData, ModelHealthHistoryData, DriftTrendsData types + API functions
- `dashboard-ui/src/pages/HealthPage.tsx` — Added ModelHealthPanel import and placement

## Sprint 38 Status: ✅ COMPLETE - Committed and deployed
- All 6 todos done (feat-importance-drift, psi-snapshot-storage, model-health-dashboard, ci-cd-pipeline, deploy-verify, sprint-report)
- Branch merged to main, pushed to GitHub (commit f36bd4e)

## Documentation Update Status: 🔄 IN PROGRESS
- Audit complete — identified all gaps
- Files read and ready for editing
- Edits NOT yet applied to: README.md, docs/02-data-layer.md, docs/06-applications.md, docs/07-deployment.md

## Current State:
- All services running on beelink-gti13 (nba-ml-api, nba-ml-dashboard, nba-ml-db, nba-ml-scheduler, nba-ml-mlflow)
- Tracking backfill restarted (background)
- Git: on main branch, clean working tree (pre-docs update)
</work_done>

<technical_details>
### SQLAlchemy JSONB Parameter Binding
- `::jsonb` PostgreSQL cast syntax conflicts with SQLAlchemy's `text()` parameter parser — `text()` interprets `:jsonb` as a second bind parameter
- Fix: Use `CAST(:param AS jsonb)` instead of `:param::jsonb`
- Affected: `src/notifications/dispatcher.py` health snapshot INSERT

### Drift Analysis Results
- 6/308 features show significant drift (PSI > 0.2)
- Top drifted: `month` (8.51), `season_phase` (1.56), `season_game_number` (1.17), `game_hour` (1.17) — all temporal features that naturally drift as season progresses
- Only non-temporal: `opp_vs_pos_reb_avg` (0.26)
- Hit rate remains solid at 53.2% over 7,930 samples despite drift — model is robust

### SGO Alt-Line Problem (from prior segments)
- SportsGameOdds DraftKings returns alternate/game-prop lines alongside primary O/U lines
- Fix: `primary_props` CTE picks line closest to model prediction via `DISTINCT ON ... ORDER BY ABS(predicted_value - line) ASC`
- One-sided game props (NULL under_odds) filtered at ingestion in prop_lines.py

### Deployment Details
- Server: beelink-gti13 (local/server mode)
- Deploy: `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache <service> && ... up -d`
- PYTHONUNBUFFERED=1 required for real-time docker exec output
- Container recreation kills running backfill — must restart with `docker exec -d`
- DB table creation done via `docker exec nba-ml-db psql` (not alembic upgrade, since alembic runs on container start)

### Dashboard Architecture
- React SPA + Express BFF pattern
- BFF queries Postgres directly for data-heavy endpoints (overview, history, props)
- BFF proxies to FastAPI for evaluation endpoints (model-health, feature-drift, calibration)
- `apiFetch()` automatically includes `X-API-Key` header
- BFF caching via `cached()` helper with configurable TTL

### Documentation Gaps Identified (for pending work)
- **README.md**: Missing tables: drift_snapshots, model_health_snapshots, prop_line_snapshots, game_advanced_stats, game_tracking_stats, hustle_stats, bbref_advanced_stats, game_lines, daily_lineups. Missing API endpoints: /evaluation/model-health, /evaluation/model-health/history, /evaluation/drift-trends, /evaluation/clv, /evaluation/calibration, /evaluation/feature-drift, /evaluation/rolling-window-analysis. Missing: CI/CD section, data sources update (SGO), prop filtering notes.
- **docs/02-data-layer.md**: Already has most tables but missing drift_snapshots and model_health_snapshots
- **docs/06-applications.md**: Missing prop history/P&L tracking, PRA composite predictions, one-sided prop filtering, model health monitoring application, Kelly criterion details
- **docs/07-deployment.md**: Has placeholder CI/CD with wrong workflow content; needs actual `.github/workflows/ci.yml` details
</technical_details>

<important_files>
- `README.md`
   - Project README — needs update with missing tables, endpoints, CI/CD, data sources
   - Full file read (326 lines), edits pending
   - Key sections: API Endpoints (line 189), Database Schema (line 202), Tech Stack (line 86), Configuration (line 299)

- `docs/02-data-layer.md`
   - Database schema documentation — needs drift_snapshots + model_health_snapshots tables
   - Full file read (393 lines), edits pending
   - Has all tables through Sprint 15 but missing Sprint 37-38 tables

- `docs/06-applications.md`
   - Applications documentation — needs new applications and endpoint updates
   - Full file read (284 lines), edits pending
   - Missing: prop history/P&L, PRA composite, model health monitoring, one-sided prop filter

- `docs/07-deployment.md`
   - Deployment documentation — needs CI/CD update
   - Full file read (144 lines), edits pending
   - Lines 47-71: Has wrong placeholder CI/CD workflow, needs replacement with actual ci.yml

- `src/db/models.py`
   - ORM models — DriftSnapshot added at end (after ModelHealthSnapshot at line 469-489)
   - New DriftSnapshot: id, checked_at, feature_name, psi_value, drift_status, reference/inference window days

- `src/notifications/dispatcher.py`
   - Health check orchestrator — PSI snapshot batch-insert added after drift check (lines 258-282)
   - JSONB cast fix at line 292

- `src/api/server.py`
   - FastAPI endpoints — model-health/history (line 1346) and drift-trends (line 1380) added after existing model-health endpoint

- `dashboard-ui/server/src/index.ts`
   - BFF server — 3 new proxy endpoints added before feature-drift endpoint
   - ~1800+ lines total

- `dashboard-ui/src/components/charts/ModelHealthPanel.tsx`
   - New component: status card with ECE/HR/drift/alerts + ECE and hit rate trend line charts
   - Uses Recharts, TanStack Query

- `dashboard-ui/src/lib/api.ts`
   - API types + fetch functions — added ModelHealthData, ModelHealthHistoryData, DriftTrendsData types
   - Added modelHealth, modelHealthHistory, driftTrends API functions

- `.github/workflows/ci.yml`
   - GitHub Actions CI pipeline: python-tests (pytest) + dashboard-build (tsc + npm build)

- `docs/reports/sprint38-s34-next-steps.md`
   - Sprint 38 report documenting all changes
</important_files>

<next_steps>
## Active Work: Documentation Update
The user requested updating all documentation based on sprint changes. Audit is complete and all target files have been read. Need to apply edits to:

1. **README.md** — Add missing database tables (drift_snapshots, model_health_snapshots + 7 others already in 02-data-layer.md but not README), add missing API endpoints (7+ evaluation endpoints), update Tech Stack (add SportsGameOdds data source), add CI/CD mention, update test count, update data sources reference

2. **docs/02-data-layer.md** — Add `drift_snapshots` table schema and `model_health_snapshots` table schema sections at end

3. **docs/06-applications.md** — Add: Application for Model Health Monitoring (background checks, PSI snapshots, trend tracking), update Prop Edge Finder with one-sided prop filtering and alt-line contamination fix details, add PRA composite prediction details, update API endpoints table with all evaluation endpoints, add prop history/P&L tracking details

4. **docs/07-deployment.md** — Replace placeholder CI/CD section (lines 47-71) with actual `.github/workflows/ci.yml` content (pytest + dashboard-build), add notable migration for 011_add_drift_snapshots, update monitoring section

5. **Commit and push** documentation changes

## Approach:
- Use general-purpose sub-agents to parallelize the 4 file updates
- TypeScript/Python validation not needed (docs-only changes)
- Commit on current branch (main), push to GitHub
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
