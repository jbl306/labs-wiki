---
title: "Copilot Session Checkpoint: Props DB query and chart refinement"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, graph, agents, dashboard]
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Props DB query and chart refinement
**Session ID:** `94eedf26-380e-451c-89d2-f703046de219`
**Checkpoint file:** `/home/jbl/.copilot/session-state/94eedf26-380e-451c-89d2-f703046de219/checkpoints/007-props-db-query-and-chart-refin.md`
**Checkpoint timestamp:** 2026-03-22T23:37:38.615919Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user is building a modern React + Node.js dashboard to replace a 3,272-line Streamlit monolith for the NBA ML Engine. The approach uses a Vite + React 19 + TypeScript SPA with an Express BFF (Backend-For-Frontend) that proxies to FastAPI and queries PostgreSQL directly. After the initial scaffold and deployment, the focus shifted to fixing data pipeline issues (empty tabs, type mismatches) and refining the chart strategy to maximize actionable insights. We're currently mid-fix on the Props page which was showing no data due to relying on a today-only FastAPI endpoint.
</overview>

<history>
1. Prior sprints (context from before this session): Built NBA ML Engine with FastAPI, PostgreSQL, model training pipeline. Completed sprints 9-12 covering model improvements, feature engineering, evaluation/calibration, and cleanup. Created feature/react-dashboard-redesign branch and scaffolded the entire React dashboard (Phases 1-5: foundation, components, BFF API, all 10 pages).

2. Session start: Resumed from compaction — React build had just been fixed (2 unused import errors). Built successfully.
   - Updated homelab compose to use `Dockerfile.dashboard-react` instead of `Dockerfile.dashboard`
   - Hit Express 5 wildcard route error (`'*'` → `'{*path}'`)
   - Hit `__dirname` path resolution bug (needed `../../dist` not `../dist`)
   - Hit `tsx` not available in production (switched to compiling server TS to JS at build time with `tsc`)
   - Fixed server/tsconfig.json: `"module": "NodeNext"` for proper ESM compilation
   - Successfully deployed, all pages returning HTTP 200

3. Created PR #11 and merged to main. Updated homepage config (icon: si-streamlit → si-react).

4. User reported "not getting data on many tabs"
   - Diagnosed: BFF only proxied to FastAPI (6 endpoints), but 5 tabs needed direct PostgreSQL queries
   - DB had plenty of data: 536 players, 153K game_logs, 431 injuries, 22K predictions, 3.5K prop_lines, 400 models
   - Agent added `pg` package and implemented 20+ SQL queries in BFF for: injuries, seasons, health/data, backtest, dashboard enhancements, player detail enrichment
   - Hit "Invalid URL" error — DATABASE_URL password contained `/+= ` chars that broke pg's URL parser
   - Fixed by parsing connection string manually into individual params (user/password/host/port/database)
   - All endpoints returned real data after fix

5. User reported still not getting data — found 16 field/structure mismatches between BFF responses and frontend TypeScript interfaces
   - Mapped all mismatches via explore agent: wrong field names, missing fields, nested vs flat structures
   - Agent fixed all 16 across 9 endpoints (injuries: add position, dashboard: stat→stat_name, seasons: avg_points→pts, backtest: add roi/pnl, player: flatten response, waiver: flatten projections, search: id→player_id, health: table_name→name)
   - Also added 8s timeout to waiver endpoint (upstream FastAPI hangs)

6. User asked for Top Edges card on overview + relevant graphs for each tab
   - Agent added 11 new charts across 7 pages + 3 new BFF SQL queries (trending_players, hit_rate_trend, prop_volume)
   - Featured 🎯 Top Edges card on Dashboard, full Seasons page implementation, pipeline calendar on Health page

7. User reported "page not loading"
   - Root cause: PostgreSQL `ROUND()` returns NUMERIC type → `pg` serializes as strings → frontend `.toFixed()` crashes on strings
   - Added `numericRow()` helper function, applied to all DB query results with ROUND() columns
   - Fixed trending_players, edge_summary, season stats, team_trends, player season_averages
   - Recorded lesson in tasks/lessons.md

8. User asked to evaluate charts — keep/drop/add recommendations
   - Evaluated all charts, recommended dropping 6 low-value (Prop Volume, Avg Edge by Stat, Injury Status Breakdown, Minutes vs Points, MAE/Bets by Stat backtest, MAE models)
   - Recommended adding 4 high-value (Model Accuracy Trend, Edge Distribution histogram, Hit Rate by Edge Size, Predicted vs Actual overlay)
   - User approved, agent implemented all drops and adds
   - Key finding: 10%+ edge bets hit at 53.5% vs 45.5% for tiny edges

9. User reported Props page not showing data
   - Diagnosed: BFF proxies to FastAPI `/prop-edges` which only returns TODAY's data. No games today = no props.
   - DB has plenty of historical data (341 edges for 3/21, 470 for 3/20, etc.)
   - **Currently implementing**: Replacing FastAPI proxy with direct DB query supporting date filtering
   - Wrote the new SQL query and BFF endpoint, was about to update the frontend page when compaction triggered
</history>

<work_done>
Files created/modified in nba-ml-engine repo (branch: `main`):

**BFF Server** (`dashboard-ui/server/src/index.ts`):
- Added PostgreSQL connection via `pg` Pool (imports from `./db.js`)
- `numericRow()` helper at top for coercing pg NUMERIC strings to numbers
- 11 API endpoints, most now query DB directly instead of proxying FastAPI
- `/api/props` endpoint was JUST rewritten (in progress) — replaced FastAPI proxy with direct DB query supporting `?date=` param, returns available dates for date picker
- `/api/dashboard` — aggregates FastAPI health + DB queries for edge_summary, trending_players, hit_rate_trend, model_accuracy_trend, games_today
- `/api/injuries`, `/api/seasons`, `/api/health/data`, `/api/backtest` — all direct DB queries
- `/api/players/:id` — enriched with game_log, injury_history, season_averages from DB
- `/api/waiver` — FastAPI proxy with 8s timeout, flattens projections
- `/api/players/search`, `/api/models`, `/api/health` — still proxy to FastAPI

**DB Module** (`dashboard-ui/server/src/db.ts`):
- pg Pool with manual URL parsing for passwords with special chars
- `query()` and `shutdown()` exports

**Frontend Pages** (all in `dashboard-ui/src/pages/`):
- DashboardPage.tsx: Signal cards, 🎯 Top Edges card, Trending Players bar, Edge Hit Rate line, Model Accuracy Trend line
- PropsPage.tsx: Filters (stat, source, min edge), DataTable, scatter, edge distribution, market depth — NEEDS date picker added
- InjuriesPage.tsx: Status filter, DataTable, team breakdown chart
- SeasonsPage.tsx: Season selector, DataTable, Top Scorers bar, Team Pace bar
- BacktestPage.tsx: Signal cards, P&L line, Hit Rate by Stat bar, Hit Rate by Edge Size bar
- PlayerPage.tsx: Signal cards, stat tabs, trend line, predicted vs actual overlay, game log table, injury history
- HealthPage.tsx: Table health grid, 31-day pipeline calendar with ✓/✗
- ModelsPage.tsx: R² by Stat bar, full model registry DataTable
- WaiverPage.tsx: DataTable with projections
- ReferencePage.tsx: Data dictionary + model guide

**Homelab** (`compose/compose.nba-ml.yml`):
- nba-ml-dashboard uses Dockerfile.dashboard-react
- Environment: NODE_ENV=production, PORT=8501, FASTAPI_URL=http://nba-ml-api:8000, DATABASE_URL
- Depends on nba-ml-db (healthy) and nba-ml-api (started)
- Memory limit: 256M, CPU: 0.5

**Currently running on homelab**: Container `nba-ml-dashboard` on port 8501, all 10 pages return HTTP 200.

Work in progress:
- [x] BFF `/api/props` endpoint rewritten with DB query (code written, NOT YET compiled/deployed)
- [ ] PropsPage.tsx needs date picker filter added to use the new `dates` field
- [ ] api.ts PropsData interface needs `dates: string[]` added
- [ ] Compile, build, deploy, verify
</work_done>

<technical_details>
**Architecture:**
- Two repos: `homelab` (/home/jbl/projects/homelab) manages Docker compose; `nba-ml-engine` (/home/jbl/projects/nba-ml-engine) is the ML + dashboard codebase
- BFF pattern: Express server at dashboard-ui/server/ proxies some calls to FastAPI (localhost:8000) and queries PostgreSQL directly for most data
- Docker: multi-stage build — Stage 1 builds React + compiles server TS, Stage 2 runs compiled JS with node:20-slim
- Port 8501 (drop-in for old Streamlit), Caddy reverse proxy at nba-dashboard.DOMAIN

**Key Bugs & Fixes:**
- Express 5: wildcard route must be `'{*path}'` not `'*'`
- ESM `__dirname`: must polyfill with `path.dirname(fileURLToPath(import.meta.url))`
- Server path: compiled to `server/dist/index.js`, so dist path is `../../dist` not `../dist`
- `tsx` not in production: compile server TS at build time, run compiled JS
- pg NUMERIC/ROUND: returns strings, not numbers. Always wrap with `numericRow()` helper
- DATABASE_URL with special chars: pg Pool's `connectionString` fails on `/+=` in passwords. Parse manually with regex: `/^postgresql:\/\/([^:]+):(.+)@([^:]+):(\d+)\/(.+)$/`
- FastAPI `/prop-edges`: only returns TODAY's data. Replaced with direct DB query.
- FastAPI `/waiver-wire`: hangs/times out. Added 8s AbortSignal timeout.

**Database:** PostgreSQL with 15 tables. Key tables: players (536 active), game_logs (153K), predictions (22K), prop_lines (3.5K), model_registry (400), injuries (431), team_stats (360), games (25). All accessed via pg Pool in BFF.

**Design System:** Tailwind CSS 4 with `@theme` directive. Warm bone (#F7F6F3) light / OLED black (#0A0A0A) dark. Emerald accent (#059669). Geist Sans/Mono fonts via Google Fonts CDN. Phosphor Icons v2 (bold weight).

**Node.js:** v20.20.1 via nvm. Must source: `export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"`

**TypeScript:** Strict mode with noUnusedLocals/noUnusedParameters. Server uses `"module": "NodeNext"`. Frontend uses Vite with `@tailwindcss/vite` plugin.

**Deployment lesson:** ALWAYS `--no-cache` on Docker builds after code changes. Verify rendered pages not just HTTP 200.

**Key insight from backtest data:** Bigger predicted edges (10%+) hit at 53.5% vs 45.5% for tiny (0-2%) edges — model edge sizing is meaningful.
</technical_details>

<important_files>
- `dashboard-ui/server/src/index.ts`
  - THE critical file — Express BFF server with all API endpoints
  - Just rewrote `/api/props` endpoint (lines ~144-200) to use direct DB query with date filter instead of FastAPI proxy
  - `numericRow()` helper at line ~16 for pg NUMERIC string coercion
  - All 11 API endpoints defined here

- `dashboard-ui/server/src/db.ts`
  - PostgreSQL connection pool with manual URL parsing for special char passwords
  - Exports `query()` and `shutdown()`

- `dashboard-ui/src/pages/PropsPage.tsx`
  - NEEDS UPDATE: add date picker using new `dates` field from API
  - Currently has: stat/source/minEdge filters, DataTable, scatter, edge distribution, market depth
  - ~150 lines

- `dashboard-ui/src/lib/api.ts`
  - All TypeScript interfaces and fetch functions
  - NEEDS UPDATE: add `dates: string[]` to `PropsData` interface
  - ~230 lines, interfaces defined throughout

- `dashboard-ui/src/pages/DashboardPage.tsx`
  - Overview page with Top Edges card, trending players, hit rate, model accuracy
  - ~165 lines

- `dashboard-ui/src/components/charts/Charts.tsx`
  - LineChartCard, BarChartCard, ScatterChartCard wrappers for Recharts
  - Props: data, xKey, yKeys (array with key/color/label), title, subtitle, height, stacked

- `Dockerfile.dashboard-react`
  - Multi-stage: node:20-slim builds React + compiles server TS, then runs compiled JS
  - Exposes 8501

- `homelab/compose/compose.nba-ml.yml`
  - nba-ml-dashboard service config (lines ~129-168)
  - Uses Dockerfile.dashboard-react, env: NODE_ENV, PORT, FASTAPI_URL, DATABASE_URL

- `dashboard-ui/src/components/shared/Filters.tsx`
  - Select, MultiSelect, Slider filter components
  - Will need to reference Select component for date picker

- `tasks/lessons.md`
  - Accumulated lessons from all sprints including pg NUMERIC string bug
</important_files>

<next_steps>
**Immediate (in progress when compacted):**
1. The `/api/props` BFF endpoint has been rewritten in `server/src/index.ts` but NOT yet compiled or tested
2. Need to update `api.ts` — add `dates: string[]` to `PropsData` interface, update `props()` function to accept optional `date` param
3. Need to update `PropsPage.tsx` — add date picker (Select component) that passes selected date to API, default to most recent date
4. Compile: `npx tsc -p server/tsconfig.json --noEmit && npx tsc -b && npm run build`
5. Deploy: `docker compose build --no-cache nba-ml-dashboard && docker compose up -d nba-ml-dashboard`
6. Verify: `curl http://localhost:8501/api/props` returns data, check page renders in browser

**Props page improvements planned:**
- Date picker filter (dates from API response)
- Game date column in table
- Opponent column
- Signal cards showing total edges, avg edge, best edge
- All data comes from the new DB query (not FastAPI)

**After Props fix:**
- Full end-to-end verification of all 10 pages with real data
- Consider adding more date range support to other pages
- Commit, push, verify production
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
