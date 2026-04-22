---
title: "Copilot Session Checkpoint: Sprint 35-36 and game lines diagnosis"
type: source
created: 2026-03-29
last_verified: 2026-04-21
source_hash: "8d3bad50b4e5ce4338c31ee04997a2c1d6d8ea252241b5844aada1b951f76d4b"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-35-36-and-game-lines-diagnosis-1dbf44ee.md
quality_score: 61
concepts:
  []
related:
  - "[[Homelab]]"
  - "[[NBA ML Engine]]"
tier: archive
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, dashboard]
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: validated
---

# Copilot Session Checkpoint: Sprint 35-36 and game lines diagnosis

## Summary

The user is iterating on the NBA ML Engine project through sprint-based development on a homelab server (beelink-gti13). This session covered Sprint 35 (Props page historical predictions, P&L tracking, Kelly Criterion), Sprint 36 (DriftReport AttributeError fix + ntfy notifications for prop ingestion), rerunning the daily pipeline, and diagnosing settlement and game lines issues. The approach follows the `execute-sprint-from-report` skill workflow with autonomous implementation, deployment, and verification.

## Key Points

- Added `hit` (boolean|null) and `actual` (number|null) fields to existing `/api/props` response by joining with settlement data
- Added types to api.ts: HistoricalBet, PnlCurvePoint, StatBreakdown, PnlSummary, PropsHistoryData
- Deployed nba-ml-dashboard container, verified endpoints (1,111 settled bets, 61.1% hit rate, +247u flat, +42.65u Kelly)
- Wrote sprint report, committed to feature branch, merged to main, pushed to GitHub
- Sprint 36: Fix DriftReport AttributeError + ntfy for prop ingestion (COMPLETED)
- Fixed both locations: `drift_report.get("drifted_features", [])` → `drift_report.drifted_features` and `drift.get("summary", {})` → `drift.summary`

## Execution Snapshot

## Sprint 35 (COMPLETE)

**Files modified:**
- `dashboard-ui/server/src/index.ts` — Added settlement enrichment to `/api/props` (+35 lines), new `/api/props/history` endpoint (~200 lines) with Kelly computation, P&L curves, by-stat breakdown
- `dashboard-ui/src/lib/api.ts` — Added `hit`/`actual` to PropRecord, new types (HistoricalBet, PnlCurvePoint, etc.), `propsHistory` API method
- `dashboard-ui/src/pages/PropsPage.tsx` — Full rewrite: tabbed interface (Today/History), HitIndicator component, SignalBox cards, HistoryTab with filters/charts/table, Hit column on Today tab (237→470+ lines)
- `docs/reports/sprint35-props-historical-pnl.md` — Sprint report

## Sprint 36 (COMPLETE)

**Files modified:**
- `src/training/trainer.py:153` — `drift_report.get("drifted_features", [])` → `drift_report.drifted_features`
- `src/notifications/dispatcher.py:234-237` — Dict-style access → dataclass attribute access on DriftReport
- `src/data/prop_lines.py` — Added ntfy notification block after prop upsert (+19 lines)
- `docs/reports/sprint36-drift-fix-ntfy.md` — Sprint report
- `tasks/lessons.md` — Added Sprint 36 lesson on dataclass vs dict access

## Game Lines Investigation (IN PROGRESS)
- Root cause identified: `fetch_game_lines()` in `src/data/game_lines.py` has no fallback when Odds API returns 401
- SportsGameOdds data includes game-level odds but they're filtered out in `_extract_sportsgameodds_prop_rows` (line 347-349 skips statEntityID "all"/"home"/"away")
- Need to add SGO fallback to game_lines.py similar to how prop_lines.py uses both APIs

## Technical Details

- Server: beelink-gti13 (local homelab, `server` mode)
- Deploy: `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache <service> && ... up -d`
- Containers: nba-ml-api (FastAPI:8000), nba-ml-dashboard (BFF+React:8501), nba-ml-db (TimescaleDB), nba-ml-scheduler (Ofelia cron), nba-ml-mlflow
- PYTHONUNBUFFERED=1 required for real-time docker exec log output
- Container has no `ps` command — use /proc to check processes ### Odds API Quota Issue
- The Odds API key (`eb4a4ca82b5709fde429d542cb9bfcc0`) has exhausted its monthly quota — all requests return 401 Unauthorized
- `fetch_prop_lines()` falls back to SportsGameOdds successfully (994 rows)
- `fetch_game_lines()` has NO fallback — returns 0 lines on 401
- SportsGameOdds API uses `x-api-key` header, base URL `https://api.sportsgameodds.com/v2/events`, leagueID=NBA ### SGO Event Structure (for game lines fallback)
- Events have `.odds` dict with odd entries
- Player props: `statEntityID` is a player identifier, `betTypeID` is "ou"
- Game lines: `statEntityID` is "all"/"home"/"away", stats like spreads/totals use different statIDs
- Current prop extraction at `prop_lines.py:347-349` explicitly `continue`s past game-level odds
- Bookmaker mapping: `_SPORTSGAMEODDS_BOOKMAKER_MAP` maps SGO IDs to source labels ### Settlement System
- `settle_prop_line_snapshots()` joins PropLineSnapshot with GameLog on (player_id, game_date)
- Works correctly — 6,695 settled across 5 dates
- ~1,989 unsettled past-date snapshots are orphans (props for players who didn't play)
- Settlement runs at top of `fetch_prop_lines()` (line 704) ### Kelly Criterion Implementation
- Half-Kelly: `f = max(0, min((p*(b+1)-1) / (2*b), 0.25))`
- p = model confidence score, b = decimal_odds - 1
- American→decimal: positive `(american/100) + 1`, negative `(100/|american|) + 1`
- Capped at 25% per bet ### DriftReport is a @dataclass (NOT a dict)
- Defined in `src/evaluation/feature_drift.py:30-37`
- Fields: `drifted_features` (list[dict]), `feature_psi` (dict), `summary` (dict), `threshold` (float)
- Must use attribute access, not `.get()` or bracket access ### Scheduler (Ofelia)
- pipeline-daily: 07:00 UTC (03:00 AM ET)
- props-refresh: 22:00 UTC (6:00 PM ET)
- predict-refresh: 22:15 UTC
- weekly-retrain: 16:00 Sundays
- health-check: 23:00 UTC
- db-backup: 05:00 UTC ### Notification Infrastructure
- Apprise-based: `src/notifications/ntfy.py` wraps Apprise
- Config: `APPRISE_URLS` env var (space-separated)
- Homelab: `NBA_ML_APPRISE_URLS="ntfy://ntfy.sh/nba-ml-pipeline"`
- `send(title, message)` function, `notify_edges(edges)` for prop alerts
- `PipelineResult` in dispatcher.py for structured pipeline notifications

## Important Files

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

## Next Steps

## Immediate: Fix game lines ingestion (IN PROGRESS)
The user's request: "the props ingestion pipeline that errored at 3:18am had 0 game lines. are we storing game lines correctly? fix if not."

Root cause: `fetch_game_lines()` only uses Odds API which is returning 401 (quota exhausted). No fallback.

**### Plan:**
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

## Related Wiki Pages

- [[Homelab]]
- [[NBA ML Engine]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-35-36-and-game-lines-diagnosis-1dbf44ee.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-29 |
| URL | N/A |
