---
title: "Copilot Session Checkpoint: Sprint 35 props page audit"
type: source
created: 2026-03-29
last_verified: 2026-04-21
source_hash: "eaf81287307bc2630200ead492f9b804e648a3171ee694aed464bc2ffda519a6"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-35-props-page-audit-a5db365f.md
quality_score: 61
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

# Copilot Session Checkpoint: Sprint 35 props page audit

## Summary

The user is iterating on the NBA ML Engine project through sprint-based development on a homelab server (beelink-gti13). This session started with Sprint 34 (dashboard chart accuracy fixes), which was completed and deployed. Now Sprint 35 is being planned: adding a historical predictions table with P&L tracking, Kelly Criterion bet sizing, and prop hit status to the Props page of the React dashboard. The approach follows the `execute-sprint-from-report` skill workflow: audit → plan → implement → test → deploy → report → push.

## Key Points

- Built and deployed both Docker images (nba-ml-api and nba-ml-dashboard)
- Wrote Sprint 34 report, lessons learned, committed and pushed to GitHub
- Created branch `feature/sprint-35-props-historical-pnl`
- Deploy: `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache <service> && ... up -d`
- **PRA composite stat**: Has 0 rows in predictions table. Fixed by summing pts+reb+ast component predictions per player/game in `prop-hit-rate` endpoint
- **Prop hit column** — add hit/miss indicator to the existing props table ### Immediate Next Steps

## Execution Snapshot

## Sprint 34 (COMPLETE)

**Files modified:**
- `src/api/server.py` — PRA hit rate computation from component stats (pts+reb+ast), model-health 5-min TTL cache
- `dashboard-ui/server/src/index.ts` — fg_pct/ft_pct CASE branches in hit_rate_trend, `getCurrentNbaSeason()` replacing hardcoded '2025-26', ROI calc `pnl/total_bets*100`, avg_edge fix (MAE→actual edge%), edge buckets 0-5/5-15/15-30/30%+
- `dashboard-ui/src/pages/PropsPage.tsx` — Edge distribution bucket ranges aligned
- `docs/reports/sprint34-dashboard-accuracy.md` — Sprint report
- `tasks/lessons.md` — Two new lessons (composite stats, expensive endpoint computation)
- `tasks/PROGRESS-sprint34-dashboard-accuracy-0329.md` — Progress tracker

All committed on main, pushed to GitHub, deployed to homelab.

## Sprint 35 (IN PROGRESS — planning/audit phase only)
- Branch created: `feature/sprint-35-props-historical-pnl`
- No code changes yet
- Two comprehensive audits completed (see Technical Details)
- No progress tracker or todos created yet

## Technical Details

- Server mode: beelink-gti13 (local homelab)
- Deploy: `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache <service> && ... up -d`
- API key: `WbmM4ifSnNbXwl5fuaFLdthcoOYHfWH8/QMs4YFGEk8=` (from container env, the trailing `=` gets stripped by shell grep)
- API on port 8000, BFF on port 8501, dashboard serves on 8501 ### Sprint 34 Key Fixes
- **PRA composite stat**: Has 0 rows in predictions table. Fixed by summing pts+reb+ast component predictions per player/game in `prop-hit-rate` endpoint
- **Model-health cache**: `_model_health_cache` dict with `result` and `expires` keys, 300s TTL. First call ~50s, cached ~27ms
- **Dynamic season**: `getCurrentNbaSeason()` in BFF — month >= 10 means current year, else previous year. Format: `YYYY-YY` ### Sprint 35 Audit Findings (for implementation) **Dashboard UI Stack:**
- React 19.2.4, TypeScript 5.9.3, Vite 8.0.1
- Tailwind CSS 4.2 with custom CSS vars (light/dark theme via `.dark` class)
- @tanstack/react-table v8 for DataTable (sorting, filtering, pagination, CSV export)
- @tanstack/react-query v5 for data fetching (5min stale, 10min gc)
- Recharts 3.8 for charts (LineChartCard, BarChartCard, ScatterChartCard)
- Phosphor Icons, Framer Motion
- Geist font family **Database Settlement Data:**
- `prop_line_snapshots` table has: actual_value, result (OVER/UNDER), settled_at
- 5,329 settled props across 4 days (2026-03-24 to 2026-03-27)
- Key columns: player_id, game_date, source, stat_name, line, over_odds, under_odds, actual_value, result, settled_at
- No Kelly/bankroll/bet-size logic exists anywhere in codebase **BFF `/api/props` endpoint** (lines 508-588):
- Proxies FastAPI `/prop-edges` endpoint
- Returns: props[], stats[], sources[], dates[] (last 14 days), policy
- Props sorted by confidence DESC then edge DESC
- Each prop has: player_name, team, source, stat_name, line, predicted_value, confidence_score/low/high/tier, edge_pct, edge_value, direction, call, game_date, odds, opponent, is_home, game_time **BFF `/api/backtest` endpoint** (lines 826-915):
- 60-day rolling window, 5-min cache
- CTE joins predictions→prop_lines→game_logs
- Returns: summary, by_stat, pnl_curve, details[], by_edge_size
- PnL: ±1 unit flat bets (hit=+1, miss=-1)
- BacktestDetail type exists but `details` array is returned empty `[]` **BFF `/api/dashboard` best_predictions** (lines 312-361):
- 8-table join, confidence-ranked, edge-policy-filtered
- Deduped to 10 by player+stat (highest confidence kept)
- Confidence: logistic approximation using CI width vs line distance **BFF caching**: In-memory Map with TTL (dashboard=2min, backtest=5min, edge-policy=10min) **PropsPage current state** (237 lines):
- Filters: stat, source, edge preset (recommended/custom/all), min edge slider
- Charts: Scatter (line vs predicted), Bar (edge distribution), Bar (market depth)
- Table columns: Player, Matchup, Tipoff, Stat, Book, Confidence, Line, Predicted, Edge%, Call
- No historical data, no P&L, no hit column, no Kelly sizing **Routes** (App.tsx): /, /props, /rankings, /injuries, /seasons, /models, /health, /waiver, /backtest, /reference, /player/:id ### Known Issues
- Settlement data only covers 4 days (limited historical depth)
- `BacktestDetail[]` (individual bet records) is returned as empty array — the type exists but data isn't populated
- Odds data (over_odds/under_odds) is available in prop_line_snapshots for Kelly calculations

## Important Files

- `dashboard-ui/src/pages/PropsPage.tsx` (237 lines)
- PRIMARY target for Sprint 35 changes
- Currently: filters + scatter/bar charts + props table
- Needs: historical predictions tab/section, prop hit column, P&L tracking, Kelly bet sizing
- Table uses DataTable component with @tanstack/react-table

- `dashboard-ui/server/src/index.ts` (~1355 lines)
- BFF server — needs new endpoint(s) for historical settled predictions with P&L
- `/api/props` (lines 508-588) — current props endpoint
- `/api/backtest` (lines 826-915) — existing backtest logic (template for historical P&L)
- `/api/dashboard` (lines 262-505) — best_predictions query (template for confident predictions)
- Caching mechanism at lines 142-150
- `getCurrentNbaSeason()` at lines 107-113
- `buildEdgeFilterClause()` at lines 189-222

- `dashboard-ui/src/lib/api.ts` (405 lines)
- All API types and fetch functions
- Needs: new types for historical predictions, Kelly sizing, P&L data
- Key types: PropRecord, FeaturedPredictionRecord, BacktestData, BacktestDetail

- `dashboard-ui/src/components/charts/Charts.tsx` (186 lines)
- LineChartCard, BarChartCard, ScatterChartCard
- May need new chart for P&L curve on props page

- `dashboard-ui/src/components/shared/DataTable.tsx` (161 lines)
- Reusable table with sorting, filtering, pagination, CSV export
- Used by PropsPage for the props table
- Will be used for historical predictions table

- `dashboard-ui/src/pages/BacktestPage.tsx` (73 lines)
- Template for P&L display patterns (signal strip, PnL curve, by_stat breakdown)

- `src/api/server.py`
- Sprint 34: Added PRA hit rate computation, model-health cache
- May not need changes for Sprint 35 (BFF handles most dashboard queries directly)

- `tasks/lessons.md`
- Running lessons log — needs Sprint 35 entries after implementation

- `docs/reports/sprint34-dashboard-accuracy.md`
- Source report for Sprint 35 next steps context

## Next Steps

## Sprint 35 Implementation Plan

### Scope (from user request)
1. **Historical predictions table** on Props page — shows settled "most confident predictions" with drill-down by stat, date
2. **Running P&L** — cumulative profit/loss tracking
3. **Kelly Criterion bet sizing** — configurable bet sizes based on edge and confidence
4. **Prop hit column** — add hit/miss indicator to the existing props table

### Immediate Next Steps
1. Create progress tracker: `tasks/PROGRESS-sprint35-props-historical-pnl-0329.md`
2. Insert Sprint 35 todos into SQL
3. Implement BFF endpoint: `/api/props/history` — query settled prop_line_snapshots joined with predictions, compute hit/miss, P&L (flat + Kelly), aggregate by date/stat
4. Add Kelly Criterion utility function: `kellyFraction(edge, odds) = (p * (b+1) - 1) / b` where p = win probability, b = decimal odds
5. Add types to `api.ts`: HistoricalPrediction, KellyBet, PnLSummary
6. Update PropsPage: add tab/section for historical view with date range picker, stat filter, P&L summary cards, cumulative P&L chart, and detailed table
7. Add "Hit" column to existing props table (requires joining with prop_line_snapshots for settled games)
8. TypeScript build check, deploy both images, verify live
9. Write Sprint 35 report, commit, push

### Key Design Decisions Needed
- Kelly Criterion fractional Kelly (e.g., half-Kelly) vs full Kelly — half-Kelly is standard for risk management
- Bankroll assumption for P&L display (configurable? default $1000?)
- Whether to add a separate tab vs inline section on PropsPage
- How to handle the "hit" column for unsettled (today's) props — show "pending" indicator

## Related Wiki Pages

- [[Homelab]]
- [[NBA ML Engine]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-35-props-page-audit-a5db365f.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-29 |
| URL | N/A |
