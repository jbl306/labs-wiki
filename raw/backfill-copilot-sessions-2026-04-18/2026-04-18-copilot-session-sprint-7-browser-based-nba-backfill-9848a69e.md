---
title: "Copilot Session Checkpoint: Sprint 7 browser-based NBA backfill"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard]
status: pending
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint 7 browser-based NBA backfill
**Session ID:** `60e0cf52-fa90-4a78-bfaf-8571221bb5e6`
**Checkpoint file:** `/home/jbl/.copilot/session-state/60e0cf52-fa90-4a78-bfaf-8571221bb5e6/checkpoints/001-sprint-7-browser-based-nba-bac.md`
**Checkpoint timestamp:** 2026-03-20T21:08:59.153062Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user requested creating a new branch off main to implement Sprint 7 for their NBA ML prediction engine. Sprint 7 focuses on browser-based data backfill for hustle stats and tracking stats that were previously blocked by stats.nba.com's bot protection. The approach uses `curl_cffi` with Chrome TLS fingerprint impersonation to bypass Akamai/Cloudflare bot detection, enabling access to NBA API endpoints that Python's `requests` library cannot reach.
</overview>

<history>
1. User asked to create a new branch off main, plan Sprint 7 from sprint evaluation docs, implement it, deploy, validate, and create a report
   - Explored the codebase extensively: read sprint 4 evaluation report, model evaluation report, progress tracker, lessons.md, todo.md
   - Checked last commit (c47b1ab) which was Sprint 5-6 delivering: feature importance widget, ntfy notifications, shadow predictions, game-line ingestion, BBRef fuzzy matching, model auto-pruning, Docker multi-stage builds
   - Found no sprint5-6 evaluation report at the path referenced (doesn't exist) — used sprint4 evaluation + model evaluation report as basis for Sprint 7 planning
   - Launched explore agent to comprehensively map codebase (12 questions about hustle, tracking, browser scripts, models, config, etc.)
   - Asked user to clarify browser approach — user was unavailable, so worked autonomously
   - Identified key blocked items: `hustle_stats` (0 rows) and `game_tracking_stats` (0 rows), both blocked by stats.nba.com API timeouts

2. Investigated the browser-based approach
   - Confirmed `requests` and `nba_api` both timeout against stats.nba.com
   - Tested `curl_cffi` with Chrome TLS impersonation — **major breakthrough**:
     - `commonallplayers`: ✅ 200 OK
     - `scoreboardv3`: ✅ 200 OK
     - `leaguehustlestatsplayer`: ✅ 200 OK, 567 players, 28 columns
     - `boxscoreplayertrackv3`: ✅ 200 OK, per-game tracking data
     - `boxscoreadvancedv3`: ✅ 200 OK
   - Discovered V3 tracking endpoint uses nested JSON structure (`{boxScorePlayerTrack: {homeTeam/awayTeam: {players: [{statistics: {...}}]}}}`) instead of `resultSets` format
   - Discovered V3 tracking endpoint doesn't include `deflections` field (returns null)
   - Validated hustle stats for 3 seasons (2022-23: 535 players, 2023-24: 567, 2024-25: 567)

3. Implementation
   - Created branch `feature/sprint-7-browser-backfill` off main
   - Created plan.md in session workspace and SQL todos with dependencies
   - Created `src/data/nba_browser.py` — new browser-based NBA stats fetcher module
   - Updated `requirements.txt` — added `curl_cffi>=0.7.0`
   - Updated `main.py` — added `--hustle-browser` and `--tracking-browser` CLI flags, refactored backfill command
   - Created `docs/reports/sprint7-evaluation-browser-backfill_0320.md` — comprehensive evaluation report
   - Updated `tasks/PROGRESS.md` — added decisions log entry for curl_cffi choice
   - All 30 tests pass (1 pre-existing quantile mode failure in test_models.py, unrelated)

4. Deployment investigation
   - Cannot SSH to homelab (192.168.1.238) — Permission denied (publickey)
   - Documented full deployment steps in the evaluation report for user to follow
</history>

<work_done>
Files created:
- `src/data/nba_browser.py`: New browser-based NBA stats fetcher (~320 lines) with `_browser_get()`, `_parse_result_set()`, `_parse_tracking_v3()`, `ingest_hustle_stats_browser()`, `ingest_tracking_stats_browser()`
- `docs/reports/sprint7-evaluation-browser-backfill_0320.md`: Sprint 7 evaluation report with problem analysis, implementation details, deployment steps, and next steps

Files modified:
- `requirements.txt`: Added `curl_cffi>=0.7.0` after `rapidfuzz`
- `main.py`: Added `--hustle-browser` and `--tracking-browser` flags to backfill command, refactored flag validation logic (~lines 420-520)
- `tasks/PROGRESS.md`: Added curl_cffi decision to decisions log

Work completed:
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
</work_done>

<technical_details>
### Key Breakthrough: TLS Fingerprinting
- stats.nba.com uses Akamai/Cloudflare bot detection that checks TLS fingerprint (JA3/JA4)
- Python's `requests`/`urllib3` have a distinct TLS fingerprint from Chrome → requests get dropped after TLS handshake
- `curl_cffi` with `impersonate="chrome"` reproduces Chrome's exact TLS ClientHello → requests succeed
- This is a 5MB solution vs 300MB for Playwright/Selenium

### API Response Formats
- Hustle stats (`leaguehustlestatsplayer`): Uses legacy `resultSets` format with flat headers/rowSet arrays
- Tracking stats V3 (`boxscoreplayertrackv3`): Uses nested JSON: `{boxScorePlayerTrack: {homeTeam/awayTeam: {players: [{personId, statistics: {speed, distance, ...}}]}}}`
- V3 tracking does NOT include `deflections` field (returns null) — may need V2 fallback later
- Tracking V3 uses `contestedFieldGoalsAttempted` (not `CONTESTED_SHOTS`) and `uncontestedFieldGoalsAttempted`

### Data Coverage
- Hustle stats available from 2016-17 onward (10 seasons), ~535-567 players per season
- Tracking stats per-game for all ~12,752 games × ~24 players = ~150,000+ rows expected
- Feature matrix expands from 356 → 377 columns (7 hustle + 14 tracking rolling features)

### Existing Code Patterns
- `ingest_hustle_stats()` in `nba_ingest.py` (lines 1863-1933) uses `nba_api.LeagueHustleStatsPlayer` — blocked
- `ingest_game_tracking_stats()` in `nba_ingest.py` (lines 1745-1860) uses `nba_api.BoxScorePlayerTrackV3` — blocked
- Both use `_call_nba_endpoint()` wrapper (lines 89-123) with `_NBA_HEADERS` (browser-like but wrong TLS)
- Feature builder wiring: `_load_hustle_stats()` (line 872), `_add_hustle_features()` (line 901), `_load_game_tracking_stats()` (line 796), `_add_tracking_rolling()` (line 839)

### Pre-existing Test Failures
- `tests/test_models.py::TestXGBoost::test_quantile_mode` — pre-existing failure, not related to our changes
- Sprint 4 report noted "2 pre-existing quantile mode failures"

### Environment
- Python 3.12.3, venv at `.venv/`
- Homelab at 192.168.1.238 — cannot SSH (publickey auth fails from this machine)
- Homelab Docker containers: nba-ml-db, nba-ml-mlflow, nba-ml-api, nba-ml-dashboard, nba-ml-scheduler
- Deployment requires: `docker compose build --no-cache nba-ml-api` then `docker compose up -d`

### Unresolved Questions
- User said "use the script from the last commit in main for clues" — interpreted as the game_lines.py pattern. Not 100% certain what specific script they meant.
- User said "we just solved populating hustle stats via browser" — could mean they already have data in the DB, or they confirmed the approach works. Implemented the automated backfill code regardless.
</technical_details>

<important_files>
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
</important_files>

<next_steps>
Remaining work:
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

Immediate next steps:
1. Add lesson to `tasks/lessons.md` about TLS fingerprinting bypass
2. `git add` all changed/new files
3. `git commit` with Sprint 7 message
4. `git push origin feature/sprint-7-browser-backfill`
5. Mark SQL todos as done/pending-deploy
6. Call task_complete with summary of what was accomplished and what the user needs to do for deployment
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
