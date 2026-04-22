---
title: "Copilot Session Checkpoint: Sprint 7 browser-based NBA backfill"
type: source
created: 2026-03-20
last_verified: 2026-04-21
source_hash: "9f4a8dfdf1194cb257374f76181b6d2349a5df514f2b0126309d332953863586"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-7-browser-based-nba-backfill-9848a69e.md
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

# Copilot Session Checkpoint: Sprint 7 browser-based NBA backfill

## Summary

The user requested creating a new branch off main to implement Sprint 7 for their NBA ML prediction engine. Sprint 7 focuses on browser-based data backfill for hustle stats and tracking stats that were previously blocked by stats.nba.com's bot protection. The approach uses `curl_cffi` with Chrome TLS fingerprint impersonation to bypass Akamai/Cloudflare bot detection, enabling access to NBA API endpoints that Python's `requests` library cannot reach.

## Key Points

- Created branch `feature/sprint-7-browser-backfill` off main
- Created plan and SQL todos
- Implemented `src/data/nba_browser.py` with curl_cffi Chrome impersonation
- Validated curl_cffi works against all 3 previously-blocked endpoints
- Updated CLI with `--hustle-browser` and `--tracking-browser` flags
- Added curl_cffi to requirements and installed locally

## Execution Snapshot

**Files created:**
- `src/data/nba_browser.py`: New browser-based NBA stats fetcher (~320 lines) with `_browser_get()`, `_parse_result_set()`, `_parse_tracking_v3()`, `ingest_hustle_stats_browser()`, `ingest_tracking_stats_browser()`
- `docs/reports/sprint7-evaluation-browser-backfill_0320.md`: Sprint 7 evaluation report with problem analysis, implementation details, deployment steps, and next steps

**Files modified:**
- `requirements.txt`: Added `curl_cffi>=0.7.0` after `rapidfuzz`
- `main.py`: Added `--hustle-browser` and `--tracking-browser` flags to backfill command, refactored flag validation logic (~lines 420-520)
- `tasks/PROGRESS.md`: Added curl_cffi decision to decisions log

**Work completed:**
- [x] Created branch `feature/sprint-7-browser-backfill` off main
- [x] Created plan and SQL todos
- [x] Implemented `src/data/nba_browser.py` with curl_cffi Chrome impersonation
- [x] Validated curl_cffi works against all 3 previously-blocked endpoints
- [x] Updated CLI with `--hustle-browser` and `--tracking-browser` flags
- [x] Added curl_cffi to requirements and installed locally
- [x] All 30 tests pass (no regressions)
- [x] Created comprehensive sprint 7 evaluation report
- [x] Updated PROGRESS.md decisions log
- [ ] NOT YET: Committed changes to git
- [ ] NOT YET: Pushed to GitHub
- [ ] NOT YET: Updated lessons.md (was viewing the end of the file when compaction triggered)
- [ ] NOT YET: Deployed to homelab (no SSH access)
- [ ] NOT YET: Run actual backfills on homelab
- [ ] NOT YET: Retrained models with new data

## Technical Details

- stats.nba.com uses Akamai/Cloudflare bot detection that checks TLS fingerprint (JA3/JA4)
- Python's `requests`/`urllib3` have a distinct TLS fingerprint from Chrome → requests get dropped after TLS handshake
- `curl_cffi` with `impersonate="chrome"` reproduces Chrome's exact TLS ClientHello → requests succeed
- This is a 5MB solution vs 300MB for Playwright/Selenium ### API Response Formats
- Hustle stats (`leaguehustlestatsplayer`): Uses legacy `resultSets` format with flat headers/rowSet arrays
- Tracking stats V3 (`boxscoreplayertrackv3`): Uses nested JSON: `{boxScorePlayerTrack: {homeTeam/awayTeam: {players: [{personId, statistics: {speed, distance, ...}}]}}}`
- V3 tracking does NOT include `deflections` field (returns null) — may need V2 fallback later
- Tracking V3 uses `contestedFieldGoalsAttempted` (not `CONTESTED_SHOTS`) and `uncontestedFieldGoalsAttempted` ### Data Coverage
- Hustle stats available from 2016-17 onward (10 seasons), ~535-567 players per season
- Tracking stats per-game for all ~12,752 games × ~24 players = ~150,000+ rows expected
- Feature matrix expands from 356 → 377 columns (7 hustle + 14 tracking rolling features) ### Existing Code Patterns
- `ingest_hustle_stats()` in `nba_ingest.py` (lines 1863-1933) uses `nba_api.LeagueHustleStatsPlayer` — blocked
- `ingest_game_tracking_stats()` in `nba_ingest.py` (lines 1745-1860) uses `nba_api.BoxScorePlayerTrackV3` — blocked
- Both use `_call_nba_endpoint()` wrapper (lines 89-123) with `_NBA_HEADERS` (browser-like but wrong TLS)
- Feature builder wiring: `_load_hustle_stats()` (line 872), `_add_hustle_features()` (line 901), `_load_game_tracking_stats()` (line 796), `_add_tracking_rolling()` (line 839) ### Pre-existing Test Failures
- `tests/test_models.py::TestXGBoost::test_quantile_mode` — pre-existing failure, not related to our changes
- Sprint 4 report noted "2 pre-existing quantile mode failures" ### Environment
- Python 3.12.3, venv at `.venv/`
- Homelab at 192.168.1.238 — cannot SSH (publickey auth fails from this machine)
- Homelab Docker containers: nba-ml-db, nba-ml-mlflow, nba-ml-api, nba-ml-dashboard, nba-ml-scheduler
- Deployment requires: `docker compose build --no-cache nba-ml-api` then `docker compose up -d` ### Unresolved Questions
- User said "use the script from the last commit in main for clues" — interpreted as the game_lines.py pattern. Not 100% certain what specific script they meant.
- User said "we just solved populating hustle stats via browser" — could mean they already have data in the DB, or they confirmed the approach works. Implemented the automated backfill code regardless.

## Important Files

- `src/data/nba_browser.py`
- **NEW** — Core sprint 7 deliverable. Browser-based NBA stats fetcher using curl_cffi
- Key functions: `_browser_get()` (line ~60), `_parse_result_set()` (line ~95), `_parse_tracking_v3()` (line ~250), `ingest_hustle_stats_browser()` (line ~170), `ingest_tracking_stats_browser()` (line ~280)
- Imports: `curl_cffi`, config, models (HustleStats, GameTrackingStats, GameLog, Player)

- `main.py`
- CLI entry point. Modified backfill command (~lines 420-520) to add `--hustle-browser` and `--tracking-browser` flags
- Browser backfill flags don't need `player_map` from `sync_players()` — they build their own lookup internally

- `requirements.txt`
- Added `curl_cffi>=0.7.0` on line 8 (after rapidfuzz)

- `docs/reports/sprint7-evaluation-browser-backfill_0320.md`
- **NEW** — Comprehensive sprint 7 evaluation report with problem analysis, validation results, deployment steps, next steps

- `src/data/nba_ingest.py`
- Original blocked ingestion functions: `ingest_hustle_stats()` (line 1863), `ingest_game_tracking_stats()` (line 1745)
- `_call_nba_endpoint()` (line 89) — the wrapper that fails due to TLS fingerprinting
- Not modified in sprint 7 — browser alternatives live in nba_browser.py

- `src/features/builder.py`
- Feature engineering pipeline. Hustle features (line 872-909), tracking features (line 796-867)
- Not modified — existing wiring will automatically pick up data once tables are populated

- `src/db/models.py`
- `HustleStats` model (line 328), `GameTrackingStats` model (line 303)
- Not modified — schema already correct

- `tasks/PROGRESS.md`
- Updated decisions log with curl_cffi choice

- `config.py`
- `NBA_API_DELAY` = 0.6s (used by browser client for rate limiting)
- `NBA_HISTORICAL_START_SEASON` = "2014-15", `NBA_CURRENT_SEASON` = "2025-26"

## Next Steps

**Remaining work:**
- Update `tasks/lessons.md` with the TLS fingerprinting lesson
- Git commit all changes with descriptive message
- Git push to GitHub (origin)
- Deploy to homelab (user will need to do manually since no SSH access)
- Run `--hustle-browser` backfill on homelab
- Run `--tracking-browser` backfill on homelab
- Verify row counts in hustle_stats and game_tracking_stats tables
- Retrain models with `python main.py train`
- Run backtester comparison
- Update evaluation report with actual results

**Immediate next steps:**
1. Add lesson to `tasks/lessons.md` about TLS fingerprinting bypass
2. `git add` all changed/new files
3. `git commit` with Sprint 7 message
4. `git push origin feature/sprint-7-browser-backfill`
5. Mark SQL todos as done/pending-deploy
6. Call task_complete with summary of what was accomplished and what the user needs to do for deployment

## Related Wiki Pages

- [[Homelab]]
- [[NBA ML Engine]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-7-browser-based-nba-backfill-9848a69e.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-20 |
| URL | N/A |
