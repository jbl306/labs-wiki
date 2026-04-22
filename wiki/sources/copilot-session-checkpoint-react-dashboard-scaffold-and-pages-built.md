---
title: "Copilot Session Checkpoint: React Dashboard Scaffold and Pages Built"
type: source
created: 2026-03-22
last_verified: 2026-04-21
source_hash: "8fde9c682fa2180a86ed53a5cd3c3e4eb8b2053c8c9f3aa44cb67b6ca8eba25c"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-react-dashboard-scaffold-and-pages-built-2fe5dac8.md
quality_score: 90
concepts:
  - backend-for-frontend-pattern-in-dashboard-architecture
  - react-dashboard-redesign-typescript-tailwindcss
  - taste-skill-design-system-ui-consistency
related:
  - "[[React Dashboard Redesign with TypeScript and Tailwind CSS]]"
  - "[[Taste-Skill Design System for UI Consistency]]"
  - "[[NBA ML Engine]]"
  - "[[Express 5]]"
  - "[[FastAPI]]"
  - "[[Tailwind CSS 4]]"
  - "[[Vite]]"
  - "[[Homelab]]"
tier: hot
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard, frontend-redesign, tailwindcss, typescript, react, bff]
checkpoint_class: durable-architecture
retention_mode: retain
knowledge_state: validated
---

# Copilot Session Checkpoint: React Dashboard Scaffold and Pages Built

## Summary

The user requested a complete frontend redesign of the NBA ML Engine dashboard, replacing the existing 3,272-line monolithic Streamlit Python app with a modern React + Node.js stack. The taste-skill design system (7 skills installed globally at ~/.agents/skills/) guides the visual language: Minimalist-UI base with warm monochrome palette, Geist fonts, single emerald accent, and industrial data density for analytics. The approach is a 7-phase plan with validation gates: scaffold React SPA + Express BFF, build design system components, wire BFF API endpoints, implement 10 pages with feature parity, polish/deploy, and cleanup.

## Key Points

- Phase 1: Foundation (Vite, React, TypeScript, Tailwind, routing, BFF scaffold)
- Phase 2: Design system + all shared components
- Phase 3: BFF API endpoints (partially — proxy routes work, some endpoints return placeholder data)
- Phase 4+5: All 10 pages written with data fetching
- Created branch `feature/react-dashboard-redesign` from main in nba-ml-engine repo
- Created SQL todos (41 items) with dependency chain (65 deps)

## Execution Snapshot

**Files created in nba-ml-engine repo (on branch `feature/react-dashboard-redesign`):**
- `dashboard-ui/` — Full Vite + React + TypeScript project
- `package.json` — All deps configured, scripts: dev, dev:server, dev:all, build, start
- `vite.config.ts` — Tailwind plugin, path aliases, proxy to BFF :3080
- `tsconfig.app.json` — Added baseUrl + paths for @/ alias
- `index.html` — Geist font preconnect + Google Fonts link
- `src/index.css` — Tailwind CSS 4 with full design token system (light/dark)
- `src/main.tsx` — React 19 entry point
- `src/App.tsx` — QueryClient + ThemeProvider + BrowserRouter with all 10 routes
- `src/lib/theme.tsx` — Dark mode context with localStorage persistence
- `src/lib/api.ts` — API client + all TypeScript interfaces (20+ types)
- `src/components/layout/AppLayout.tsx` — Main layout shell
- `src/components/layout/NavBar.tsx` — Navigation with search + dark mode
- `src/components/shared/SignalCard.tsx` — Metric display cards
- `src/components/shared/DataTable.tsx` — TanStack Table wrapper
- `src/components/shared/Badge.tsx` — Badge/InjuryBadge/EdgeBadge
- `src/components/shared/Skeleton.tsx` — Loading skeletons
- `src/components/shared/States.tsx` — EmptyState + ErrorState
- `src/components/shared/Filters.tsx` — Select, MultiSelect, Slider
- `src/components/charts/Charts.tsx` — LineChartCard, BarChartCard, ScatterChartCard
- `src/pages/DashboardPage.tsx` — Overview with signals + edges
- `src/pages/PropsPage.tsx` — Full prop table with filters + scatter
- `src/pages/InjuriesPage.tsx` — Injury reports with team breakdown
- `src/pages/PlayerPage.tsx` — Player drill-down with stat tabs
- `src/pages/ModelsPage.tsx` — Model registry + R² chart
- `src/pages/SeasonsPage.tsx` — Placeholder (needs DB aggregation)
- `src/pages/BacktestPage.tsx` — P&L cards + charts
- `src/pages/HealthPage.tsx` — Pipeline status table
- `src/pages/WaiverPage.tsx` — Waiver recommendations table
- `src/pages/ReferencePage.tsx` — Data dictionary + model guide
- `server/src/index.ts` — Express BFF with 11 endpoints
- `server/tsconfig.json` — BFF TypeScript config
- `Dockerfile.dashboard-react` — Multi-stage Node build + serve
- `tasks/PROGRESS-react-dashboard.md` — Progress tracker

**Work completed:**
- [x] Phase 1: Foundation (Vite, React, TypeScript, Tailwind, routing, BFF scaffold)
- [x] Phase 2: Design system + all shared components
- [x] Phase 3: BFF API endpoints (partially — proxy routes work, some endpoints return placeholder data)
- [x] Phase 4+5: All 10 pages written with data fetching
- [ ] Final build verification (was fixing 2 unused import errors, about to rebuild)
- [ ] Phase 6: Docker deploy + production verification
- [ ] Phase 7: Docs + cleanup + PR

SQL todo status: 16 done, 6 in_progress (p3-bff-endpoints, p3-gate, p4-overview, p4-props, p4-injuries, p4-player), 19 pending

## Technical Details

- **Two repos**: homelab (`/home/jbl/projects/homelab`) manages Docker compose; nba-ml-engine (`/home/jbl/projects/nba-ml-engine`) is the ML codebase
- **Docker compose**: `docker compose -f compose/compose.nba-ml.yml --env-file .env` from homelab dir
- **Node.js**: Installed via nvm at `~/.nvm`, v20.20.1. Must source nvm: `export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"`
- **Port conflicts**: Ports 3000-3003 occupied on homelab (by existing services). BFF uses port 3080. Vite dev on 5173. Dashboard Docker will use 8501 (drop-in for Streamlit).
- **Express 5**: Using express@5.2.1. Works with ESM (`"type": "module"`). Server uses `node --import tsx` for TypeScript execution.
- **Tailwind CSS 4**: Uses `@tailwindcss/vite` plugin and `@theme` directive (not tailwind.config.js). Design tokens defined as CSS custom properties in `@theme` block.
- **Path aliases**: `@/` → `./src/*` configured in both tsconfig.app.json (paths) and vite.config.ts (resolve.alias).
- **Geist font**: Loaded via Google Fonts CDN in index.html. Font family: 'Geist' for sans, 'Geist Mono' for monospace.
- **Phosphor Icons v2**: Icon names differ from v1. `HeartPulse` doesn't exist → use `Heartbeat`. Always check exports.
- **BFF architecture**: Express server at dashboard-ui/server/src/index.ts proxies to FastAPI at localhost:8000. Aggregates multiple API calls for dashboard page. Serves static React build in production.
- **FastAPI endpoints available**: /health, /projections, /projections/{id}, /prop-edges, /models, /waiver-wire, /players/search
- **Placeholder BFF endpoints**: /api/injuries, /api/seasons, /api/health/data, /api/backtest return empty data (FastAPI doesn't have these). Dashboard currently reads these from PostgreSQL directly in Streamlit.
- **Dockerfile.dashboard-react**: Multi-stage — Stage 1 builds React with `npm run build`, Stage 2 runs Node.js with tsx for the BFF server. Exposes port 8501.
- **Strict TypeScript**: noUnusedLocals=true, noUnusedParameters=true. Must clean up imports.
- **Lessons from prior sprints**: Always rebuild Docker images with --no-cache; verify rendered page not just HTTP 200; use PYTHONPATH=/app for docker exec; check port availability before binding.
- **Server**: beelink-gti13, Ubuntu 22.04, user jbl. Docker containers for NBA ML stack.
- **Current Streamlit dashboard**: Runs on port 8501 via Dockerfile.dashboard. Will keep running in parallel until React dashboard verified.
- **Design tokens**: Light mode uses warm bone (#F7F6F3) canvas, dark mode uses OLED black (#0A0A0A). Single emerald accent (#059669/#34D399). All in CSS custom properties. Key architecture decision: BFF (Backend-For-Frontend) pattern chosen over direct FastAPI consumption because:
- FastAPI only has 6 endpoints but dashboard needs 20+ views
- BFF aggregates multiple API calls into single response
- Serves static React build in production (single container)
- Keeps ML API focused on ML, presentation in Node.js

## Important Files

- `dashboard-ui/package.json`
- Central dependency manifest for the React frontend + BFF
- Scripts: dev (vite), dev:server (tsx watch), build (tsc + vite build), start (production)
- Key deps: react@19, react-router-dom@7, @tanstack/react-query@5, @tanstack/react-table@8, recharts@3, express@5, tailwindcss@4

- `dashboard-ui/src/index.css`
- Design token system — ALL theme colors, fonts, shadows defined here
- Uses Tailwind CSS 4 `@theme` directive for custom properties
- Dark mode via `.dark` class overrides
- Scrollbar styling, font smoothing, tabular nums

- `dashboard-ui/src/App.tsx`
- Root component: QueryClient (5-min stale) + ThemeProvider + BrowserRouter
- All 10 routes defined under AppLayout wrapper

- `dashboard-ui/server/src/index.ts`
- Express BFF server — 11 API endpoints
- Proxies to FastAPI at FASTAPI_URL (default localhost:8000)
- PORT defaults to 3080 (dev) or 8501 (production via env)
- Serves static React build in production mode
- Has EADDRINUSE error handling

- `dashboard-ui/src/lib/api.ts`
- API client with typed fetch functions for all endpoints
- 20+ TypeScript interfaces (DashboardData, PropRecord, ModelRecord, PlayerData, etc.)
- All types used by pages and components

- `dashboard-ui/src/components/shared/DataTable.tsx`
- Generic TanStack Table wrapper — sorting, filtering, pagination, CSV export
- Used by Props, Injuries, Models, Waiver pages

- `dashboard-ui/src/components/charts/Charts.tsx`
- Recharts wrappers: LineChartCard, BarChartCard, ScatterChartCard
- Themed with CSS custom properties (--color-border, --color-surface, --font-mono)
- SERIES_COLORS palette for multi-series

- `dashboard-ui/src/components/layout/NavBar.tsx`
- Main navigation: 9 pill links, player search with debounced API, dark mode toggle
- Uses Phosphor icons (bold weight)
- Sticky header with backdrop-blur

- `Dockerfile.dashboard-react`
- Multi-stage Docker build for production
- Stage 1: node:20-slim builds React app
- Stage 2: node:20-slim runs BFF server serving built static files
- Exposes 8501 for drop-in Streamlit replacement

- `tasks/PROGRESS-react-dashboard.md`
- Progress tracker with phase/task/status tables

- `dashboard/app.py` (existing, 3,272 lines)
- The Streamlit app being replaced — reference for feature parity
- 9 tabs: Overview, Props, Injuries, Seasons, Models, Health, Waiver, Backtest, Reference
- Directly queries PostgreSQL via SQLAlchemy (not through FastAPI)

## Next Steps

**Immediate (was in progress when compacted):**
1. Run `npm run build` — just fixed 2 unused import errors (BarChartCard in PlayerPage, Badge in WaiverPage), need to verify clean build
2. Mark Phase 3-5 SQL todos as done after build succeeds

Phase 6: Deploy to Docker
3. Update homelab compose to use Dockerfile.dashboard-react instead of Dockerfile.dashboard
4. Set FASTAPI_URL=http://nba-ml-api:8000 in compose env (Docker internal network)
5. `docker compose build --no-cache nba-ml-dashboard` (lesson: always rebuild after code changes)
6. `docker compose up -d nba-ml-dashboard`
7. Verify rendered pages (lesson: check actual pages, not just HTTP 200)
8. Test all 10 pages with real production data
9. Smoke test: player search, dark mode toggle, props filtering, CSV export

Phase 7: Cleanup
10. Update nba-ml-engine README with new dashboard architecture
11. Remove old Streamlit files (dashboard/app.py, Dockerfile.dashboard, requirements.dashboard.txt)
12. Update homelab homepage config for new dashboard
13. Commit all changes, push, create PR
14. Update tasks/PROGRESS-react-dashboard.md

**Open questions:**
- Several BFF endpoints return placeholder data (injuries, seasons, health, backtest) because FastAPI doesn't expose these. Need to either add FastAPI endpoints or have BFF query DB directly.
- The FASTAPI_URL in Docker needs to use the Docker network hostname (nba-ml-api), not localhost.

## Related Wiki Pages

- [[React Dashboard Redesign with TypeScript and Tailwind CSS]]
- [[Taste-Skill Design System for UI Consistency]]
- [[NBA ML Engine]]
- [[Express 5]]
- [[FastAPI]]
- [[Tailwind CSS 4]]
- [[Vite]]
- [[Homelab]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-react-dashboard-scaffold-and-pages-built-2fe5dac8.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-22 |
| URL | N/A |
