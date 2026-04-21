---
title: "Copilot Session Checkpoint: Sprint 53 merged, dashboard metrics investigation started"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, dashboard]
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint 53 merged, dashboard metrics investigation started
**Session ID:** `31d93251-dac7-4543-89a4-bd567847c867`
**Checkpoint file:** `/home/jbl/.copilot/session-state/31d93251-dac7-4543-89a4-bd567847c867/checkpoints/008-sprint-53-merged-dashboard-met.md`
**Checkpoint timestamp:** 2026-04-12T22:51:25.215444Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user is running Sprint 53 for the NBA ML Engine project, which was completed and merged as PR #37. After that, the user reported three dashboard issues: (1) props showing in fallback state with stale data from April 7 instead of today April 12, (2) hit rate discrepancy between props history P&L and backtesting page, and (3) requesting a deep dive on accuracy of metrics across the dashboard. Investigation is underway to diagnose root causes.
</overview>

<history>
1. Sprint 53 was implemented, tested, deployed, and merged (PR #37)
   - 5 tasks completed: edge_abs dashboard display, SHAP post-training hook, scale-aware edge monitoring (by_edge_abs buckets), Grafana matview latency dashboard with Prometheus metrics, CI lint
   - 16 new tests, 75 total sprint tests pass
   - Deployed to homelab: nba-ml-api and nba-ml-dashboard containers rebuilt
   - Fixed /metrics endpoint blocked by API key middleware (added to _PUBLIC_PATHS)
   - Fixed Prometheus cross-network scraping (connected prometheus to nba-ml Docker network)
   - Fixed matview not updating (had to DROP + CREATE mv_backtest_summary for new by_edge_abs UNION ALL)
   - Fixed prometheus_client duplicate collector registration in tests (_get_or_create helper)
   - Sprint report written to docs/reports/sprint53-results.md, lessons added to tasks/lessons.md
   - Branch merged to main, homelab synced

2. User reported dashboard issues: props in fallback state, hit rate discrepancy, wants deep dive on metrics accuracy
   - Investigated data freshness: only pts and stl predictions exist for today (April 12), prop lines stopped after April 10 for most stats, only 1 PRA prop from SGO_FD for today
   - 14 games scheduled today but pipeline hasn't generated full predictions or fetched props
   - `getFeaturedPropSlate()` falls back to latest date where prop_lines JOIN predictions exists — that's April 7
   - Today tab shows 154 props all from game_date 2026-04-07 (stale by 5 days)
   - History endpoint (`/api/props/history`) uses `prop_line_snapshots` table with `settled_at IS NOT NULL` and computes hits via `result === modelDir` (OVER/UNDER string match)
   - Backtest endpoint (`/api/backtest`) uses `mv_backtest_summary` materialized view which computes hits by comparing `predicted_value > line AND gl_stat > line` from game_logs
   - These are fundamentally different data sources and computations — discrepancy is expected but needs investigation to quantify and potentially reconcile
   - Was in the middle of reading the history endpoint code (lines 726-960 of index.ts) when compaction triggered
</history>

<work_done>
Sprint 53 completed and merged (PR #37):
- `dashboard-ui/src/pages/props/TodayTab.tsx`: Added edge_abs column after edge_pct with ±color coding
- `dashboard-ui/src/pages/props/HistoryTab.tsx`: Added edge_abs column after edge_pct, text-xs variant
- `main.py`: Added `shap-report` CLI command (~line 636-670), added non-blocking SHAP analysis after full pipeline training (~line 162-173)
- `scripts/optimize_db.py`: Added `by_edge_abs` UNION ALL to mv_backtest_summary (buckets: 0-0.5, 0.5-1, 1-2, 2-3, 3+), added Prometheus Histogram/Gauge metrics with _get_or_create helper, added timing to refresh_materialized_views
- `src/api/server.py`: Added /metrics endpoint (excluded from API key middleware via _PUBLIC_PATHS), imports prometheus_client generate_latest
- `dashboard-ui/server/src/index.ts`: Added by_edge_abs parsing in backtest endpoint, returns avg_edge_pts
- `.github/workflows/ci.yml`: Added lint step (continue-on-error), BFF tsc type-check
- `requirements.txt`: Added prometheus_client>=0.20.0
- `tests/test_sprint53.py`: 16 new tests covering all 5 tasks
- `docs/reports/sprint53-results.md`: Sprint results report
- `tasks/lessons.md`: 3 new lessons (prometheus re-import, docker networking, matview DROP+CREATE)

Homelab changes (outside nba-ml-engine repo):
- `~/projects/homelab/config/prometheus/prometheus.yml`: Added nba-ml-api scrape target
- `~/projects/homelab/config/grafana/dashboards/nba-ml-matviews.json`: Created Grafana dashboard
- `~/projects/homelab/compose/compose.monitoring.yml`: Added nba-ml as external network, attached prometheus to it

Dashboard investigation in progress (NOT yet fixed):
- Identified props fallback root cause: pipeline not generating predictions for most stats
- Identified hit rate discrepancy root cause: different data sources and computation methods
- Was reading /api/props/history endpoint code when compaction occurred
</work_done>

<technical_details>
**Props Fallback Root Cause:**
- `getFeaturedPropSlate()` (index.ts:308-332) queries for dates where prop_lines JOIN predictions exist
- Only pts and stl have predictions for today (April 12), but no matching prop_lines for those stats today
- Prop lines stopped being fetched after April 10 for most stats (pts, reb, ast, fg3m, blk, stl)
- Only 1 PRA prop line exists for today from SGO_FD
- Result: featuredDate falls back to April 7, the last date with both props AND predictions joined
- Dashboard shows 154 stale props from April 7

**Hit Rate Discrepancy — Two Different Systems:**
1. **History P&L** (`/api/props/history`, index.ts:726+): Uses `prop_line_snapshots` table (settled_at IS NOT NULL), computes hit via `result === modelDir` where modelDir is 'OVER'/'UNDER'. Uses `prediction_blend` CTE to join predictions.
2. **Backtest** (`/api/backtest`, index.ts:1336+): Uses `mv_backtest_summary` materialized view. Computes hits via `predicted_value > line AND gl_stat > line` from game_logs. All-time data.
3. Key differences: different time windows, different inclusion criteria (prop_line_snapshots settlement vs game_logs actuals), different dedup logic

**Data State (as of April 12, 2026):**
- Predictions table: 516 pts + 516 stl for today, 1032 total
- Prop lines today: 1 PRA from SGO_FD only
- Prop lines last 3 days: data exists up to April 10 for all 7 stats
- 14 games scheduled today
- Backtest matview: 9,483 total bets, 52.5% hit rate overall

**Edge Analysis by Absolute Points (from mv_backtest_summary):**
- 0-0.5: 51.5% (4,173 bets) — baseline
- 0.5-1: 54.5% (2,121 bets) — strongest mid-range
- 1-2: 50.7% (1,676 bets)
- 2-3: 47.8% (573 bets) — underperforming
- 3+: 58.6% (940 bets) — highest but suspicious avg_edge of 11.44 pts

**Key Technical Gotchas (from this session):**
- prometheus_client module-level metrics cause ValueError on re-import across test files → use _get_or_create helper
- CREATE MATERIALIZED VIEW IF NOT EXISTS preserves old SQL definition → must DROP CASCADE + CREATE when changing query
- Docker containers on different compose networks can't resolve each other → add external network + attach
- /metrics endpoint needs to be in _PUBLIC_PATHS to bypass API key middleware for Prometheus scraping
- BFF has 5-min TTL cache on backtest endpoint → restart dashboard container to clear

**Unresolved Questions:**
- Why did the pipeline stop generating predictions for reb, ast, blk, tov, fg3m? Only pts and stl work.
- Why did prop line fetching stop after April 10? Is the SGO/FD scraper failing?
- What exactly should the hit rate show on each page? Should they be reconciled or are they intentionally different views?
- Is prop_line_snapshots a separate table from prop_lines? How does settlement work?
</technical_details>

<important_files>
- `dashboard-ui/server/src/index.ts` (~2000+ lines)
  - BFF server with all API endpoints
  - `getFeaturedPropSlate()` at line 308-332: determines which date to show, this is the fallback logic
  - `/api/props` at line 598-723: today's props endpoint, calls FastAPI `/prop-edges`, enriches with settlement from prop_line_snapshots
  - `/api/props/history` at line 726-1070+: history P&L endpoint, uses prop_line_snapshots with settled_at, computes hit via result string match
  - `/api/backtest` at line 1336-1393: backtest endpoint using mv_backtest_summary matview, now returns by_edge_abs
  - Settlement enrichment at line 656-673: queries prop_line_snapshots for settled results
  - PREDICTION_BLEND_CTE and PROP_CONFIDENCE_SQL referenced throughout

- `scripts/optimize_db.py`
  - mv_backtest_summary definition with by_edge_abs UNION ALL (Sprint 53 addition)
  - Prometheus metrics: MV_REFRESH_SECONDS Histogram, MV_REFRESH_LAST Gauge
  - refresh_materialized_views() with timing at line ~384+

- `src/api/server.py`
  - FastAPI app with /metrics endpoint (Sprint 53)
  - _PUBLIC_PATHS at line 67 includes /metrics
  - /prop-edges endpoint called by BFF for today's props

- `main.py`
  - Pipeline orchestrator: train, predict, post-retrain, shap-report commands
  - Train command now runs SHAP post-training (~line 162-173)
  - Key for understanding why only pts/stl predictions exist

- `dashboard-ui/src/pages/props/TodayTab.tsx` and `HistoryTab.tsx`
  - React components showing props data
  - Both now have edge_abs column (Sprint 53)
  - Need to understand how they consume the BFF data and display hit rates

- `config.py`
  - STAT_COLUMNS defines which stats are trained/predicted
  - STAT_EDGE_ABSOLUTE defines per-stat absolute edge thresholds

- `~/projects/homelab/compose/compose.monitoring.yml`
  - Prometheus now on both monitoring and nba-ml networks
  - Grafana dashboard provisioned at config/grafana/dashboards/

- `docs/reports/sprint53-results.md` - Sprint 53 results report
- `tasks/lessons.md` - Lessons learned, 3 new entries from Sprint 53
- `tests/test_sprint53.py` - 16 tests for Sprint 53 features
</important_files>

<next_steps>
**Active Investigation — Dashboard Metrics Deep Dive:**

The user asked: "Why are props in fallback state? Why is hit rate different on props history P&L vs backtesting page? Do a deep dive on accuracy of metrics across the dashboard and fix."

Three problems to solve:

1. **Props Fallback (stale data from April 7)**
   - Root cause identified: pipeline not generating predictions for most stats, prop fetching stalled after April 10
   - Need to check: scheduler logs, SGO/FD scraper status, why only pts+stl predictions exist
   - Check `docker logs nba-ml-api` and scheduler job history
   - May need to manually trigger pipeline: `python main.py predict --store`

2. **Hit Rate Discrepancy Between History P&L and Backtest**
   - Already identified the two different computation methods
   - Need to quantify the gap: run both computations on the same date range and compare
   - Determine if discrepancy is a bug or expected (different data sources)
   - Check if prop_line_snapshots settlement is working correctly
   - Consider: should both use the same source of truth? (game_logs actuals vs settlement)

3. **Full Dashboard Metrics Accuracy Audit**
   - Cross-check all dashboard pages that show hit rates, P&L, or accuracy metrics
   - Pages to audit: Today tab, History tab, Backtest page, Dashboard overview
   - Verify: are confidence scores consistent? Are edge calculations the same everywhere?
   - Check if PRA composite stat handling is correct in all places
   - Look at the dashboard overview endpoint at `/api/dashboard` for its hit rate computation

**Immediate next actions:**
- Check pipeline/scheduler logs to understand why predictions stopped for most stats
- Query prop_line_snapshots vs game_logs to compare settlement results
- Run `/api/props/history` with the same date range as backtest and compare hit rates numerically
- Map all hit rate computations across the codebase and identify inconsistencies
- Fix the pipeline data freshness issue (likely scheduler or SGO scraper problem)
- Reconcile or document the expected differences between history and backtest hit rates

**Git state:** On main branch, clean (Sprint 53 merged). No uncommitted changes.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
