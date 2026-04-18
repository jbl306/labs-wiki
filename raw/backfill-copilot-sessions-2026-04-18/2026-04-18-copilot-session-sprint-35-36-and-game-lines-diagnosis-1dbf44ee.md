---
title: "Copilot Session Checkpoint: Sprint 35-36 and game lines diagnosis"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, dashboard]
status: pending
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint 35-36 and game lines diagnosis
**Session ID:** `8d466128-8017-482d-b021-0fffe970d5eb`
**Checkpoint file:** `/home/jbl/.copilot/session-state/8d466128-8017-482d-b021-0fffe970d5eb/checkpoints/004-sprint-35-36-and-game-lines-di.md`
**Checkpoint timestamp:** 2026-03-29T12:21:39.358625Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user is iterating on the NBA ML Engine project through sprint-based development on a homelab server (beelink-gti13). This session covered Sprint 35 (Props page historical predictions, P&L tracking, Kelly Criterion), Sprint 36 (DriftReport AttributeError fix + ntfy notifications for prop ingestion), rerunning the daily pipeline, and diagnosing settlement and game lines issues. The approach follows the `execute-sprint-from-report` skill workflow with autonomous implementation, deployment, and verification.
</overview>

<history>
1. Sprint 35: Props page historical predictions, P&L & Kelly sizing (COMPLETED)
   - Context was compacted mid-sprint with audits done but no code written
   - Implemented BFF `/api/props/history` endpoint joining prop_line_snapshots + predictions + players, computing hit/miss, flat P&L (±1 unit), and half-Kelly P&L
   - Added `hit` (boolean|null) and `actual` (number|null) fields to existing `/api/props` response by joining with settlement data
   - Rewrote PropsPage.tsx with tabbed interface: "Today" tab (existing functionality + new Hit column) and "History & P&L" tab (signal strip, P&L curve chart, by-stat breakdown, full DataTable)
   - Added types to api.ts: HistoricalBet, PnlCurvePoint, StatBreakdown, PnlSummary, PropsHistoryData
   - TypeScript compiled clean, Vite build succeeded
   - Deployed nba-ml-dashboard container, verified endpoints (1,111 settled bets, 61.1% hit rate, +247u flat, +42.65u Kelly)
   - Wrote sprint report, committed to feature branch, merged to main, pushed to GitHub

2. Sprint 36: Fix DriftReport AttributeError + ntfy for prop ingestion (COMPLETED)
   - User reported daily pipeline failing with "DriftReport object has no attribute 'get'"
   - Found error in scheduler logs: `trainer.py:153` and `dispatcher.py:234-237` treating DriftReport dataclass as dict
   - Fixed both locations: `drift_report.get("drifted_features", [])` → `drift_report.drifted_features` and `drift.get("summary", {})` → `drift.summary`
   - Added ntfy push notification in `prop_lines.py` after successful prop upsert (line counts, settlement stats, API quota, sources)
   - Verified fixes in-container with simulated DriftReport
   - Rebuilt and deployed nba-ml-api, committed to main, pushed
   - Added lesson to tasks/lessons.md

3. User asked to rerun daily pipeline
   - Launched `docker exec -e PYTHONUNBUFFERED=1 nba-ml-api python main.py pipeline`
   - Pipeline completed successfully — DriftReport fix confirmed working (no AttributeError)
   - Odds API returned 401 Unauthorized (quota exhausted), SportsGameOdds provided 994 rows as fallback
   - 1,568 prop lines ingested, snapshots timestamped at 12:05 UTC
   - Predictions: 5,100 for 2026-03-28, 0 for today (no games)

4. User asked why no settled lines were ingested
   - Investigated: 6,695 total settled across 5 dates, settlement IS working
   - Unsettled remainders (~1,989 past-date) are orphan props from SGO — props for players whose teams didn't play on that game_date
   - The 12:05 re-run settled 0 new because the 07:17 run already settled everything with matching game logs
   - Explained: these can never be settled because no game log exists for those player+date combos

5. User asked about 0 game lines in the 3:18am pipeline + fix if not storing correctly (IN PROGRESS)
   - Found in scheduler logs: `game_lines.py` got 401 from Odds API (same quota exhaustion)
   - `fetch_game_lines()` has NO fallback — only uses The Odds API, unlike props which falls back to SportsGameOdds
   - Was investigating whether to add SportsGameOdds as a fallback source for game lines
   - Examined SGO API structure: `_extract_sportsgameodds_prop_rows` currently filters for player props only (statEntityID != "all"/"home"/"away" and betTypeID == "ou"), explicitly skipping game-level odds
   - Was about to implement a fallback that extracts spreads/totals/moneylines from SGO events
</history>

<work_done>
## Sprint 35 (COMPLETE)
Files modified:
- `dashboard-ui/server/src/index.ts` — Added settlement enrichment to `/api/props` (+35 lines), new `/api/props/history` endpoint (~200 lines) with Kelly computation, P&L curves, by-stat breakdown
- `dashboard-ui/src/lib/api.ts` — Added `hit`/`actual` to PropRecord, new types (HistoricalBet, PnlCurvePoint, etc.), `propsHistory` API method
- `dashboard-ui/src/pages/PropsPage.tsx` — Full rewrite: tabbed interface (Today/History), HitIndicator component, SignalBox cards, HistoryTab with filters/charts/table, Hit column on Today tab (237→470+ lines)
- `docs/reports/sprint35-props-historical-pnl.md` — Sprint report

## Sprint 36 (COMPLETE)
Files modified:
- `src/training/trainer.py:153` — `drift_report.get("drifted_features", [])` → `drift_report.drifted_features`
- `src/notifications/dispatcher.py:234-237` — Dict-style access → dataclass attribute access on DriftReport
- `src/data/prop_lines.py` — Added ntfy notification block after prop upsert (+19 lines)
- `docs/reports/sprint36-drift-fix-ntfy.md` — Sprint report
- `tasks/lessons.md` — Added Sprint 36 lesson on dataclass vs dict access

## Game Lines Investigation (IN PROGRESS)
- Root cause identified: `fetch_game_lines()` in `src/data/game_lines.py` has no fallback when Odds API returns 401
- SportsGameOdds data includes game-level odds but they're filtered out in `_extract_sportsgameodds_prop_rows` (line 347-349 skips statEntityID "all"/"home"/"away")
- Need to add SGO fallback to game_lines.py similar to how prop_lines.py uses both APIs
</work_done>

<technical_details>
### Environment
- Server: beelink-gti13 (local homelab, `server` mode)
- Deploy: `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache <service> && ... up -d`
- Containers: nba-ml-api (FastAPI:8000), nba-ml-dashboard (BFF+React:8501), nba-ml-db (TimescaleDB), nba-ml-scheduler (Ofelia cron), nba-ml-mlflow
- PYTHONUNBUFFERED=1 required for real-time docker exec log output
- Container has no `ps` command — use /proc to check processes

### Odds API Quota Issue
- The Odds API key (`eb4a4ca82b5709fde429d542cb9bfcc0`) has exhausted its monthly quota — all requests return 401 Unauthorized
- `fetch_prop_lines()` falls back to SportsGameOdds successfully (994 rows)
- `fetch_game_lines()` has NO fallback — returns 0 lines on 401
- SportsGameOdds API uses `x-api-key` header, base URL `https://api.sportsgameodds.com/v2/events`, leagueID=NBA

### SGO Event Structure (for game lines fallback)
- Events have `.odds` dict with odd entries
- Player props: `statEntityID` is a player identifier, `betTypeID` is "ou"
- Game lines: `statEntityID` is "all"/"home"/"away", stats like spreads/totals use different statIDs
- Current prop extraction at `prop_lines.py:347-349` explicitly `continue`s past game-level odds
- Bookmaker mapping: `_SPORTSGAMEODDS_BOOKMAKER_MAP` maps SGO IDs to source labels

### Settlement System
- `settle_prop_line_snapshots()` joins PropLineSnapshot with GameLog on (player_id, game_date)
- Works correctly — 6,695 settled across 5 dates
- ~1,989 unsettled past-date snapshots are orphans (props for players who didn't play)
- Settlement runs at top of `fetch_prop_lines()` (line 704)

### Kelly Criterion Implementation
- Half-Kelly: `f = max(0, min((p*(b+1)-1) / (2*b), 0.25))`
- p = model confidence score, b = decimal_odds - 1
- American→decimal: positive `(american/100) + 1`, negative `(100/|american|) + 1`
- Capped at 25% per bet

### DriftReport is a @dataclass (NOT a dict)
- Defined in `src/evaluation/feature_drift.py:30-37`
- Fields: `drifted_features` (list[dict]), `feature_psi` (dict), `summary` (dict), `threshold` (float)
- Must use attribute access, not `.get()` or bracket access

### Scheduler (Ofelia)
- pipeline-daily: 07:00 UTC (03:00 AM ET)
- props-refresh: 22:00 UTC (6:00 PM ET)
- predict-refresh: 22:15 UTC
- weekly-retrain: 16:00 Sundays
- health-check: 23:00 UTC
- db-backup: 05:00 UTC

### Notification Infrastructure
- Apprise-based: `src/notifications/ntfy.py` wraps Apprise
- Config: `APPRISE_URLS` env var (space-separated)
- Homelab: `NBA_ML_APPRISE_URLS="ntfy://ntfy.sh/nba-ml-pipeline"`
- `send(title, message)` function, `notify_edges(edges)` for prop alerts
- `PipelineResult` in dispatcher.py for structured pipeline notifications
</technical_details>

<important_files>
- `src/data/game_lines.py` (189 lines)
  - PRIMARY target for current fix — needs SportsGameOdds fallback
  - Only uses Odds API, returns 0 on 401 with no alternative
  - Key function: `fetch_game_lines()` line 72
  - Uses `_api_get()` helper, upserts to `GameLine` model via pg_insert

- `src/data/prop_lines.py` (~800 lines)
  - Template for SGO fallback pattern — already uses both Odds API and SportsGameOdds
  - SGO extraction at `_extract_sportsgameodds_prop_rows()` line 331 — filters OUT game-level odds at line 347-349
  - `_sportsgameodds_get()` line 580 — reusable HTTP client for SGO API
  - Sprint 36: Added ntfy notification after prop upsert

- `dashboard-ui/server/src/index.ts` (~1550 lines)
  - BFF server with all dashboard endpoints
  - Sprint 35: Added settlement enrichment to `/api/props` (around line 561-596), new `/api/props/history` endpoint (lines 627-810)
  - Key helpers: `PREDICTION_BLEND_CTE`, `PROP_CONFIDENCE_SQL`, `cached()`, `getCurrentNbaSeason()`

- `dashboard-ui/src/pages/PropsPage.tsx` (~470 lines)
  - Sprint 35: Complete rewrite with tabbed interface, Hit column, History tab with P&L
  - TodayTab and HistoryTab components, SignalBox, HitIndicator

- `dashboard-ui/src/lib/api.ts` (~465 lines)
  - All API types and fetch functions
  - Sprint 35: Added HistoricalBet, PnlCurvePoint, etc. types + propsHistory method

- `src/training/trainer.py`
  - Sprint 36 fix at line 153: DriftReport attribute access
  - `_exclude_drifted_features()` function

- `src/notifications/dispatcher.py` (~253 lines)
  - Sprint 36 fix at lines 234-237: DriftReport attribute access
  - `check_model_health()` for drift/calibration/hit-rate alerts

- `src/evaluation/feature_drift.py`
  - DriftReport dataclass definition at lines 30-37
  - `detect_training_inference_drift()` at line 156

- `src/db/models.py`
  - GameLine model — target for upsert in game_lines.py
  - PropLineSnapshot model — settlement columns (actual_value, result, settled_at)

- `config.py`
  - `SPORTSGAMEODDS_API_KEY`, `ODDS_API_KEY`, `SPORTSGAMEODDS_EVENT_LIMIT`
  - `ODDS_API_MAX_RETRIES`, `ODDS_API_BACKOFF_SECONDS`, `ODDS_API_REQUEST_TIMEOUT`
</important_files>

<next_steps>
## Immediate: Fix game lines ingestion (IN PROGRESS)
The user's request: "the props ingestion pipeline that errored at 3:18am had 0 game lines. are we storing game lines correctly? fix if not."

Root cause: `fetch_game_lines()` only uses Odds API which is returning 401 (quota exhausted). No fallback.

### Plan:
1. **Add SportsGameOdds fallback to `fetch_game_lines()`** — Extract game-level odds (spreads, totals, moneylines) from SGO events
   - SGO events already fetched in prop pipeline — the odds dict contains game-level entries where `statEntityID` is "all"/"home"/"away"
   - Need to understand SGO's statID mapping for spreads/totals/moneylines (different from player prop statIDs)
   - May need to add a new SGO-specific fetch or reuse `_sportsgameodds_get()` from prop_lines.py
   
2. **Key technical question**: What are SGO's betTypeID and statID values for spreads, totals, and moneylines?
   - Player props use `betTypeID == "ou"` — game lines likely use different betTypeIDs
   - May need to inspect a live SGO response or check their API docs
   
3. **Implementation approach**:
   - Add `_fetch_sportsgameodds_game_lines()` function to `game_lines.py`
   - Import `_sportsgameodds_get` from prop_lines or duplicate the HTTP helper
   - Parse SGO game-level odds into GameLine rows (spread_home, spread_away, total, moneyline_home, moneyline_away)
   - Call as fallback when Odds API fails or returns 0 rows
   
4. **Deploy and verify**: Rebuild nba-ml-api, run pipeline, confirm game lines stored

5. **Commit and report**: Update sprint 36 report or create new one
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
