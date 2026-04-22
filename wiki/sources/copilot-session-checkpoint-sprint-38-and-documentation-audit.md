---
title: "Copilot Session Checkpoint: Sprint 38 and documentation audit"
type: source
created: 2026-03-30
last_verified: 2026-04-21
source_hash: "691e14ba6f91ebbafc99a05dc15c66d2b403a4b8fb1d0e8f7e2490e7fe52e926"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-38-and-documentation-audit-e1161529.md
quality_score: 69
concepts:
  []
related:
  - "[[Homelab]]"
  - "[[NBA ML Engine]]"
tier: archive
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard]
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: validated
---

# Copilot Session Checkpoint: Sprint 38 and documentation audit

## Summary

The user is iterating on the NBA ML Engine project through sprint-based development on a homelab server (beelink-gti13). This session segment focused on implementing Sprint 38 (Sprint 34 remaining next steps): PSI drift snapshot storage, model health time series dashboard, GitHub Actions CI/CD pipeline, and feature importance drift analysis. The approach followed the execute-sprint-from-report skill workflow: audit existing state, plan, implement, deploy, verify, report, and commit.

## Key Points

- Sprint 37 deployed PRA predictions, model health snapshots, dashboard analytics
- Alt-line contamination fix: `primary_props` CTE in BFF queries to filter SGO DraftKings alternate lines
- Kelly bankroll simulator fixed: quarter-Kelly (0.25×) with 25% daily exposure cap
- User requested: "implement all of sprint 34 next steps except full retrain"
- Identified remaining items to implement:
- Created branch `feature/sprint-38-s34-next-steps`

## Execution Snapshot

**## Files Created (Sprint 38):**
- `.github/workflows/ci.yml` — GitHub Actions CI: pytest + TypeScript build on push/PR to main
- `alembic/versions/011_add_drift_snapshots.py` — Migration for drift_snapshots table
- `dashboard-ui/src/components/charts/ModelHealthPanel.tsx` — Model health status card + ECE/hit rate trend charts
- `docs/reports/sprint38-s34-next-steps.md` — Sprint 38 report
- `tasks/PROGRESS-sprint38-s34-next-steps-0330.md` — Progress tracker

**## Files Modified (Sprint 38):**
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

**## Current State:**
- All services running on beelink-gti13 (nba-ml-api, nba-ml-dashboard, nba-ml-db, nba-ml-scheduler, nba-ml-mlflow)
- Tracking backfill restarted (background)
- Git: on main branch, clean working tree (pre-docs update)

## Technical Details

- `::jsonb` PostgreSQL cast syntax conflicts with SQLAlchemy's `text()` parameter parser — `text()` interprets `:jsonb` as a second bind parameter
- Fix: Use `CAST(:param AS jsonb)` instead of `:param::jsonb`
- Affected: `src/notifications/dispatcher.py` health snapshot INSERT ### Drift Analysis Results
- 6/308 features show significant drift (PSI > 0.2)
- Top drifted: `month` (8.51), `season_phase` (1.56), `season_game_number` (1.17), `game_hour` (1.17) — all temporal features that naturally drift as season progresses
- Only non-temporal: `opp_vs_pos_reb_avg` (0.26)
- Hit rate remains solid at 53.2% over 7,930 samples despite drift — model is robust ### SGO Alt-Line Problem (from prior segments)
- SportsGameOdds DraftKings returns alternate/game-prop lines alongside primary O/U lines
- Fix: `primary_props` CTE picks line closest to model prediction via `DISTINCT ON ... ORDER BY ABS(predicted_value - line) ASC`
- One-sided game props (NULL under_odds) filtered at ingestion in prop_lines.py ### Deployment Details
- Server: beelink-gti13 (local/server mode)
- Deploy: `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache <service> && ... up -d`
- PYTHONUNBUFFERED=1 required for real-time docker exec output
- Container recreation kills running backfill — must restart with `docker exec -d`
- DB table creation done via `docker exec nba-ml-db psql` (not alembic upgrade, since alembic runs on container start) ### Dashboard Architecture
- React SPA + Express BFF pattern
- BFF queries Postgres directly for data-heavy endpoints (overview, history, props)
- BFF proxies to FastAPI for evaluation endpoints (model-health, feature-drift, calibration)
- `apiFetch()` automatically includes `X-API-Key` header
- BFF caching via `cached()` helper with configurable TTL ### Documentation Gaps Identified (for pending work)
- **README.md**: Missing tables: drift_snapshots, model_health_snapshots, prop_line_snapshots, game_advanced_stats, game_tracking_stats, hustle_stats, bbref_advanced_stats, game_lines, daily_lineups. Missing API endpoints: /evaluation/model-health, /evaluation/model-health/history, /evaluation/drift-trends, /evaluation/clv, /evaluation/calibration, /evaluation/feature-drift, /evaluation/rolling-window-analysis. Missing: CI/CD section, data sources update (SGO), prop filtering notes.
- **docs/02-data-layer.md**: Already has most tables but missing drift_snapshots and model_health_snapshots
- **docs/06-applications.md**: Missing prop history/P&L tracking, PRA composite predictions, one-sided prop filtering, model health monitoring application, Kelly criterion details
- **docs/07-deployment.md**: Has placeholder CI/CD with wrong workflow content; needs actual `.github/workflows/ci.yml` details

## Important Files

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

## Next Steps

## Active Work: Documentation Update

**The user requested updating all documentation based on sprint changes. Audit is complete and all target files have been read. Need to apply edits to:**

1. **README.md** — Add missing database tables (drift_snapshots, model_health_snapshots + 7 others already in 02-data-layer.md but not README), add missing API endpoints (7+ evaluation endpoints), update Tech Stack (add SportsGameOdds data source), add CI/CD mention, update test count, update data sources reference

2. **docs/02-data-layer.md** — Add `drift_snapshots` table schema and `model_health_snapshots` table schema sections at end

3. **docs/06-applications.md** — Add: Application for Model Health Monitoring (background checks, PSI snapshots, trend tracking), update Prop Edge Finder with one-sided prop filtering and alt-line contamination fix details, add PRA composite prediction details, update API endpoints table with all evaluation endpoints, add prop history/P&L tracking details

4. **docs/07-deployment.md** — Replace placeholder CI/CD section (lines 47-71) with actual `.github/workflows/ci.yml` content (pytest + dashboard-build), add notable migration for 011_add_drift_snapshots, update monitoring section

5. **Commit and push** documentation changes

**## Approach:**
- Use general-purpose sub-agents to parallelize the 4 file updates
- TypeScript/Python validation not needed (docs-only changes)
- Commit on current branch (main), push to GitHub

## Related Wiki Pages

- [[Homelab]]
- [[NBA ML Engine]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-38-and-documentation-audit-e1161529.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-30 |
| URL | N/A |
