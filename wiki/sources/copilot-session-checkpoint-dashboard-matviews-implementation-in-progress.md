---
title: "Copilot Session Checkpoint: Dashboard Matviews Implementation In Progress"
type: source
created: 2026-04-12
last_verified: 2026-04-21
source_hash: "775f812f7b3878f9c18195d90e9cda4785608659d21041c4a0edfdd122da8024"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-dashboard-matviews-implementation-in-progress-afa2957e.md
quality_score: 100
concepts:
  - postgresql-materialized-views-for-dashboard-optimization
  - concurrent-refresh-postgresql-materialized-views
  - backend-for-frontend-integration-with-materialized-views
related:
  - "[[PostgreSQL Materialized Views for Dashboard Optimization]]"
  - "[[Concurrent Refresh of PostgreSQL Materialized Views]]"
  - "[[Backend-For-Frontend (BFF) Integration with Materialized Views]]"
  - "[[NBA ML Engine]]"
  - "[[Homelab]]"
  - "[[MemPalace]]"
  - "[[PostgreSQL]]"
tier: archive
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, mempalace, agents, dashboard, postgresql, bff, database-optimization, materialized-views]
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: executed
---

# Copilot Session Checkpoint: Dashboard Matviews Implementation In Progress

## Summary

The user is executing Sprint 51 for the NBA ML Engine project: creating a new Dashboard agent and adding 5 PostgreSQL materialized views to precompute heavy dashboard aggregations. The approach is to define matviews in the existing `scripts/optimize_db.py` infrastructure, create an alembic migration, then rewire BFF (Express) and FastAPI endpoints to read from matviews instead of computing on-demand. The pipeline already calls `refresh_materialized_views()` after every run, so no new cron is needed.

## Key Points

- create-agent
- update-agents-md
- mv-definitions
- mv-refresh-concurrent
- alembic-migration
- Earlier in session: Sprint 50 was executed (PTS threshold fix, SGO timezone bug, BFF hit rate dedup fix), merged as PR #32.

## Execution Snapshot

**Files created:**
- `agents/dashboard.md`: New dashboard agent (owns BFF, React UI, matviews)
- `alembic/versions/a1b2c3d4e5f6_add_dashboard_matviews.py`: Migration creating 5 matviews + unique/secondary indexes

**Files modified:**
- `AGENTS.md`: Added dashboard agent to roster, routing guide, file-by-target table, file ownership, quality gates
- `scripts/optimize_db.py`: Added 5 new matview definitions (mv_daily_hit_rates, mv_backtest_summary, mv_player_rankings, mv_clv_daily, mv_dashboard_metrics), MV_UNIQUE_INDEXES list, updated create/refresh functions for CONCURRENTLY
- `dashboard-ui/server/src/index.ts`: Replaced `/api/backtest` heavy CTE query with `SELECT FROM mv_backtest_summary`

**From earlier in session (already merged to main):**
- `config.py`: PTS edge threshold 0.01→0.005
- `src/data/game_lines.py`: SGO timezone fix
- `dashboard-ui/server/src/index.ts`: BFF hit rate dedup fix
- `.github/copilot-instructions.md`: MemPalace, optimized
- `.github/skills/execute-sprint-from-report/SKILL.md`: 65% reduction
- `agents/sprint-orchestrator.md`: Deduplicated
- `tests/test_sprint50.py`: 7 tests
- `docs/reports/sprint50-results.md`: Sprint report

**Current git state:**
- On branch `feature/sprint-51-dashboard-matviews`
- Working tree has uncommitted changes
- PRs #32, #33, #34 already merged to main

**Todo tracking (SQL todos table):**
- [x] create-agent
- [x] update-agents-md
- [x] mv-definitions
- [x] mv-refresh-concurrent
- [x] alembic-migration
- [ ] bff-integration (IN PROGRESS — backtest done, rankings/dashboard/hit-rates remaining)
- [ ] api-integration (pending — FastAPI /prop-hit-rate and /evaluation/clv)
- [ ] tests (pending)
- [ ] deploy-verify (pending)

## Technical Details

- All 5 new matviews defined in `scripts/optimize_db.py` MATERIALIZED_VIEWS dict
- Each has a unique index (MV_UNIQUE_INDEXES) required for `REFRESH MATERIALIZED VIEW CONCURRENTLY`
- `refresh_materialized_views()` tries CONCURRENTLY first, falls back to blocking on first populate (empty matview can't use CONCURRENTLY)
- Pipeline already calls `refresh_materialized_views()` in `main.py` Step 7 after QA — no new cron needed **Matview Definitions:**
- `mv_daily_hit_rates` — DISTINCT ON dedup (closest line to prediction, SGO deprioritized), CROSS JOIN LATERAL for stat extraction, grouped by (game_date, stat_name)
- `mv_backtest_summary` — UNION ALL of daily/by_stat/by_edge aggregations, exact match of BFF `/api/backtest` query logic. Unique key: (qtype, grp)
- `mv_player_rankings` — 30-day window, composite score (pts×1.0 + reb×1.2 + ast×1.5 + stl×2.0 + blk×2.0 - tov×1.0), home/away splits. Unique key: (player_id)
- `mv_clv_daily` — Joins prop_line_snapshots with predictions for daily CLV/PnL per stat. Unique key: (game_date, stat_name)
- `mv_dashboard_metrics` — JSONB metric_value column, stores trending players and model accuracy. Unique key: (metric_type, metric_key) **BFF Integration Pattern:**
- Replace heavy CTE/JOIN queries with simple `SELECT FROM mv_*`
- Keep BFF LRU cache (2-30min TTL) as fallback for freshness between pipeline runs
- Post-processing (PnL curves, confidence scoring, Kelly) stays in BFF JS code since it's stateless transforms **Key Gotchas:**
- DISTINCT ON for prop line dedup: ORDER BY `ABS(predicted_value - line) ASC` then `CASE WHEN source LIKE 'SGO%' THEN 1 ELSE 0 END ASC` — SGO returns alt lines
- mv_backtest_summary has no date filter (includes all history) — BFF can filter in JS or we could add date range to the matview
- Rankings matview uses hardcoded 30-day window — the BFF endpoint accepts `?days=` param (30-90). May need to keep fallback query for non-30-day requests or accept 30-day-only from matview
- mv_dashboard_metrics uses JSONB for flexible metric storage — trending players and model accuracy in one view **Environment:**
- Server mode: hostname `beelink-gti13`, local containers
- Deploy: `cd ~/projects/homelab && docker compose build --no-cache <service> && up -d`
- Tests: `.venv/bin/python -m pytest` (256 tests passing before this sprint)
- Alembic migrations must be docker cp'd into nba-ml-api container (not volume-mounted) **Existing 3 matviews (pre-sprint):** mv_season_summary, mv_player_leaderboard, mv_injury_latest — these also got unique indexes added for CONCURRENTLY support.

## Important Files

- `scripts/optimize_db.py`
- Central matview definitions, indexes, create/refresh functions
- Added 5 new matview DDLs, MV_UNIQUE_INDEXES list, updated create_materialized_views() and refresh_materialized_views() for CONCURRENTLY
- MATERIALIZED_VIEWS dict starts around line 32, functions around line 155+

- `dashboard-ui/server/src/index.ts`
- BFF layer (2064+ lines), 26 endpoints, LRU cache + circuit breaker
- `/api/backtest` (line ~1366) — DONE, replaced with matview query
- `/api/rankings` (line ~1537) — NEXT, needs matview replacement for power rankings query (3 heavy queries: rankings, streaks, model accuracy by player)
- `/api/dashboard` (line ~343) — needs trending players and hit rate trend queries replaced
- `/api/prop-hit-rate` (line ~1192) — currently proxies to FastAPI, could read from mv_daily_hit_rates

- `alembic/versions/a1b2c3d4e5f6_add_dashboard_matviews.py`
- Migration creating 5 matviews + indexes, idempotent with _view_exists/_index_exists guards
- Revision chain: d7e4f2a1b835 → a1b2c3d4e5f6

- `agents/dashboard.md`
- New dashboard agent definition, 4.5KB
- Owns: dashboard-ui/, scripts/optimize_db.py (mv_*), Dockerfile.dashboard-react

- `AGENTS.md`
- Updated with dashboard agent in: roster (line 12), routing guide (line 24), file-by-target (line 34), file ownership (line 60), quality gates (line 69)

- `src/api/server.py`
- FastAPI endpoints — `/prop-hit-rate` (line 591-742) and `/evaluation/clv` (line 798-825) need matview integration
- `/prop-hit-rate` currently settles snapshots on every call + computes PRA from components — matview replaces the aggregation but settling may still need a trigger

- `main.py`
- Pipeline function (line 745+) — already calls `refresh_materialized_views()` at line ~955 after QA step
- No changes needed here

- `src/evaluation/clv_tracker.py`
- `compute_clv()` function — the matview `mv_clv_daily` precomputes its core aggregation
- FastAPI endpoint can read from matview instead of running full query

## Next Steps

**Currently in progress: BFF Integration (`bff-integration` todo)**

**Remaining BFF endpoints to update:**
1. `/api/rankings` (line ~1537) — Replace power rankings query with `SELECT FROM mv_player_rankings ORDER BY composite_score DESC LIMIT $1`. The streaks and model-accuracy-by-player sub-queries may need to stay as-is (not in matview) or be added to mv_player_rankings. Note: rankings endpoint takes `?days=` param (30-90) but matview is hardcoded to 30 days — decide whether to keep fallback for non-default days or accept matview-only.
2. `/api/dashboard` (line ~343) — Replace trending players query with `SELECT FROM mv_dashboard_metrics WHERE metric_type = 'trending'` and model accuracy trend with `WHERE metric_type = 'model_accuracy'`. Hit rate trend query can use mv_daily_hit_rates. The edge count, best predictions, games today, and edge summary queries are date-specific (today's slate) and can't be matviewed.
3. `/api/prop-hit-rate` (line ~1192) — Currently proxies to FastAPI; could read from mv_daily_hit_rates for aggregated data

**API Integration (`api-integration` todo):**
- Update FastAPI `/prop-hit-rate` (src/api/server.py:591) to read from mv_daily_hit_rates instead of settling + computing on every call. Note: settlement still needs to happen somewhere (maybe keep it in pipeline).
- Update FastAPI `/evaluation/clv` (src/api/server.py:798) to read from mv_clv_daily instead of calling compute_clv()

**Tests (`tests` todo):**
- Write tests for matview creation and refresh in optimize_db.py
- Verify BFF endpoints return equivalent data from matviews

**Deploy (`deploy-verify` todo):**
- Run alembic migration in container (docker cp + alembic upgrade head)
- Rebuild nba-ml-api and nba-ml-dashboard containers
- Verify dashboard loads correctly with matview data
- Manual refresh to populate matviews initially

**Documentation:**
- Write sprint report (docs/reports/sprint51-results.md)
- Update tasks/lessons.md with any lessons
- Commit, push, create PR, merge

## Related Wiki Pages

- [[PostgreSQL Materialized Views for Dashboard Optimization]]
- [[Concurrent Refresh of PostgreSQL Materialized Views]]
- [[Backend-For-Frontend (BFF) Integration with Materialized Views]]
- [[NBA ML Engine]]
- [[Homelab]]
- [[MemPalace]]
- [[PostgreSQL]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-dashboard-matviews-implementation-in-progress-afa2957e.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-04-12 |
| URL | N/A |
