---
title: "Copilot Session Checkpoint: Rankings Page and Performance Optimization"
type: source
created: 2026-03-23
last_verified: 2026-04-21
source_hash: "f073ae4fd7b3295570081cdf37f1d67fc5c9838cf1ce8f2aa7e1d9409b01f107"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-rankings-page-and-performance-optimization-8063e05f.md
quality_score: 100
concepts:
  - backend-for-frontend-pattern-in-dashboard-architecture
  - replacing-lateral-joins-with-regular-join-case-for-performance-optimization
  - server-side-in-memory-caching-with-ttl-for-api-performance
related:
  - "[[Replacing LATERAL Joins with Regular JOIN + CASE for Performance Optimization]]"
  - "[[Server-Side In-Memory Caching with TTL for API Performance]]"
  - "[[NBA ML Engine]]"
  - "[[Express.js]]"
  - "[[PostgreSQL]]"
  - "[[Homelab]]"
tier: archive
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard, nba, performance-optimization, sql, bff, caching]
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: validated
---

# Copilot Session Checkpoint: Rankings Page and Performance Optimization

## Summary

The user is building a modern React + Node.js dashboard to replace a Streamlit monolith for their NBA ML Engine. The approach uses Vite + React 19 + TypeScript SPA with an Express BFF (Backend-For-Frontend) that proxies to FastAPI and queries PostgreSQL directly. This session focused on fixing the Props page (empty due to today-only FastAPI endpoint), adding a new Rankings page with 7 betting-insight tabs, and now optimizing all slow API endpoints by replacing LATERAL joins with regular JOINs and adding server-side caching.

## Key Points

- Prior context (from compaction): Built NBA ML Engine across sprints 9-12. Created React dashboard replacing Streamlit monolith. Fixed numerous deployment issues (Express 5 wildcards, ESM __dirname, tsx in production, pg NUMERIC strings). Added 11 charts across 7 pages. Fixed data pipeline issues across all tabs. Props page was showing no data because BFF proxied to FastAPI which only returned today's data.
- Props page fix was in progress when session resumed
- Added `dates: string[]` to `PropsData` interface in api.ts
- Added date picker (Select component) to PropsPage.tsx with date state and query key
- Added Badge showing filtered edge count
- Compiled, built, deployed successfully

## Execution Snapshot

**Files created/modified in nba-ml-engine repo (branch: `main`):**

**Committed changes:**
- Props page fix: api.ts dates field, PropsPage.tsx date picker, server/src/index.ts props endpoint
- Rankings page: RankingsPage.tsx (new), api.ts types, App.tsx route, NavBar.tsx nav item, server/src/index.ts endpoint

**In-progress changes (NOT yet compiled/deployed):**

**`dashboard-ui/server/src/index.ts`:**
- Added `cached()` helper function with TTL-based in-memory cache (lines ~24-31)
- Replaced rankings model_accuracy LATERAL with regular JOIN + CASE (verified 200x faster)
- Replaced rankings over/under LATERAL with regular JOIN + CASE (verified 43x faster)
- **PARTIALLY REPLACED** backtest endpoint — the old 3-query LATERAL approach was replaced with a CTE + UNION ALL approach, BUT the closing part of the backtest handler that processes dailyRes/byStatRes/byEdgeRes still references the OLD variable names (dailyRes, byStatRes, byEdgeRes) which no longer exist. Need to update the rest of the handler to use the new `daily`, `byStat`, `byEdge` variables from the CTE result.
- The `cached()` wrapper was started on the backtest handler but the closing `})` for the cache callback hasn't been added yet

**Database changes (applied directly, not in code):**
- Created 4 new indexes on nba-ml-db:
- `ix_game_logs_player_id` ON game_logs(player_id)
- `ix_predictions_player_date` ON predictions(player_id, game_date)
- `ix_prop_lines_player_date` ON prop_lines(player_id, game_date)
- `ix_players_active` ON players(id) WHERE active = true

**What works:** All 11 pages return HTTP 200 with the pre-optimization code. Rankings has real data.
**What doesn't:** The server/src/index.ts is mid-edit and will NOT compile in current state.

## Technical Details

- Two repos: `homelab` (/home/jbl/projects/homelab) manages Docker compose; `nba-ml-engine` (/home/jbl/projects/nba-ml-engine) is the ML + dashboard codebase
- BFF pattern: Express server at dashboard-ui/server/ proxies some calls to FastAPI (localhost:8000) and queries PostgreSQL directly for most data
- Docker: multi-stage build — Stage 1 builds React + compiles server TS, Stage 2 runs compiled JS with node:20-slim
- Port 8501 (drop-in for old Streamlit), Caddy reverse proxy at nba-dashboard.DOMAIN **CRITICAL DB Schema Facts (learned the hard way):**
- `game_logs.player_id` joins to `players.id` (auto-increment PK), NOT `players.nba_api_id`
- Column is `players.active` (not `is_active`)
- `game_logs` has no `id` column — use `COUNT(*)` not `COUNT(gl.id)`
- `predictions` table has NO `actual_value` column — must JOIN game_logs with CASE expression to get actuals
- Query params from Express are strings — must cast: `$1::int / 5` not `$1 / 5`
- pg NUMERIC/ROUND returns strings — always wrap with `numericRow()` helper **Performance Optimization Knowledge:**
- LATERAL joins are catastrophically slow (16.8s for 22K predictions) — replace with regular JOIN + inline CASE
- Regular JOIN + CASE approach: 83ms for same query (200x speedup)
- CTE approach for backtest: compute the base join once, then UNION ALL different aggregations
- Indexes created: player_id on game_logs, (player_id, game_date) on predictions and prop_lines
- TimescaleDB (used for game_logs) does NOT support CONCURRENTLY in CREATE INDEX
- Server-side caching with TTL is essential for queries that don't change frequently **Key Bugs & Fixes from prior context:**
- Express 5: wildcard route must be `'{*path}'` not `'*'`
- ESM `__dirname`: must polyfill with `path.dirname(fileURLToPath(import.meta.url))`
- Server path: compiled to `server/dist/index.js`, so dist path is `../../dist` not `../dist`
- `tsx` not in production: compile server TS at build time, run compiled JS
- DATABASE_URL with special chars: pg Pool's `connectionString` fails on `/+=` in passwords. Parse manually with regex **DataTable Component:**
- Uses TanStack's `ColumnDef` with `accessorKey` and `cell` (NOT `key`/`render`)
- Must import `type ColumnDef` from `@tanstack/react-table`, not from DataTable component **Design System:** Tailwind CSS 4 with `@theme` directive. Warm bone (#F7F6F3) light / OLED black (#0A0A0A) dark. Emerald accent (#059669). Phosphor Icons v2 (bold weight). **Node.js:** v20.20.1 via nvm. Must source: `export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"` **Deployment:** ALWAYS `--no-cache` on Docker builds after code changes. Build command chain: ```bash cd dashboard-ui && npx tsc -p server/tsconfig.json --noEmit && npm run build cd /home/jbl/projects/homelab && docker compose -f compose/compose.nba-ml.yml --env-file .env build --no-cache nba-ml-dashboard && docker compose -f compose/compose.nba-ml.yml --env-file .env up -d nba-ml-dashboard ``` **Endpoint timing (pre-optimization):**
- rankings: 22.5s, backtest: 9s, waiver: 8s (timeout), dashboard: 3.1s
- props: 67ms, injuries: 7ms, seasons: 291ms, health: 6ms, models: 28ms

## Important Files

- `dashboard-ui/server/src/index.ts` (~730 lines, MID-EDIT)
- THE critical file — Express BFF server with all API endpoints
- Added `cached()` helper at top (~line 24-31)
- Rankings LATERAL joins replaced with regular JOINs (lines ~663-720)
- Backtest handler PARTIALLY rewritten (lines ~357-425) — old LATERAL code replaced with CTE but handler continuation still references old variables
- Need to: finish backtest handler, wrap rankings/dashboard/backtest in cached(), add cache to remaining slow endpoints

- `dashboard-ui/server/src/db.ts`
- PostgreSQL connection pool with manual URL parsing for special char passwords

- `dashboard-ui/src/pages/RankingsPage.tsx` (~454 lines, NEW)
- 7 tabs: rankings, streaks, consistency, splits, matchups, accuracy, overunder
- Each tab is a separate component with useMemo columns + charts
- Uses TanStack ColumnDef, BarChartCard, DataTable

- `dashboard-ui/src/lib/api.ts` (~310 lines)
- All TypeScript interfaces including new Rankings types
- `api.rankings()` function added

- `dashboard-ui/src/pages/PropsPage.tsx`
- Date picker added, queries with date param

- `dashboard-ui/src/App.tsx`
- Routes: added `/rankings` → RankingsPage

- `dashboard-ui/src/components/layout/NavBar.tsx`
- Added Trophy icon, Rankings nav item between Props and Injuries

- `compose/compose.nba-ml.yml` (homelab repo)
- nba-ml-dashboard service: Dockerfile.dashboard-react, port 8501, 256M memory, 0.5 CPU

- `Dockerfile.dashboard-react` (nba-ml-engine repo)
- Multi-stage build: node:20-slim, Vite build + tsc server compile

## Next Steps

**Immediate (in-progress when compacted):**
1. **FINISH the backtest handler rewrite** — the CTE + UNION ALL query is in place but the code that processes results still references old variables (`dailyRes`, `byStatRes`, `byEdgeRes`). Need to update to use `daily`, `byStat`, `byEdge` from the new code AND close the `cached()` callback properly.

2. **Wrap slow endpoints in `cached()` calls:**
- Rankings: 5-min TTL (data changes daily at most)
- Backtest: 5-min TTL
- Dashboard: 2-min TTL (has edge summary, trending)
- Seasons: 5-min TTL
- Props: 2-min TTL (per date key)

3. **Dashboard endpoint optimization** — check which sub-queries are slow (currently 3.1s) and optimize similarly (replace any LATERAL joins, add caching)

4. **Waiver endpoint** — currently 8s (FastAPI timeout). Already has 8s AbortSignal; consider caching or investigating FastAPI slowness.

5. **After all optimizations:** Compile (`npx tsc -p server/tsconfig.json --noEmit && npm run build`), deploy (`docker compose build --no-cache && up -d`), time all endpoints again to verify improvements.

6. **Commit** with descriptive message about performance optimizations.

**Remaining backtest handler code that needs updating (around line 425+):**
The old code references `dailyRes.rows`, `byStatRes.rows`, `byEdgeRes.rows` — these need to be replaced with the new `daily`, `byStat`, `byEdge` arrays computed from the CTE result. The PnL curve computation, summary stats, and response formatting all need to use these new variables.

## Related Wiki Pages

- [[Replacing LATERAL Joins with Regular JOIN + CASE for Performance Optimization]]
- [[Server-Side In-Memory Caching with TTL for API Performance]]
- [[NBA ML Engine]]
- [[Express.js]]
- [[PostgreSQL]]
- [[Homelab]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-rankings-page-and-performance-optimization-8063e05f.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-23 |
| URL | N/A |
