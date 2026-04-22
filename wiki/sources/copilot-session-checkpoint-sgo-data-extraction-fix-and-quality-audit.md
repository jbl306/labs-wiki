---
title: "Copilot Session Checkpoint: SGO Data Extraction Fix and Quality Audit"
type: source
created: 2026-04-13
last_verified: 2026-04-21
source_hash: "f5369b2de503515b0170a7d6c7a6ed15870125c0336cf70152cfa7db68adcca2"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sgo-data-extraction-fix-and-quality-audit-76644cc8.md
quality_score: 84
concepts:
  - sportsgameodds-sgo-api-data-extraction-challenges-and-fixes
related:
  - "[[SportsGameOdds (SGO) API]]"
  - "[[Durable Copilot Session Checkpoint]]"
  - "[[Homelab]]"
tier: hot
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, dashboard, data-quality, api-integration, sports-data, nba-ml]
checkpoint_class: durable-debugging
retention_mode: retain
knowledge_state: validated
---

# Copilot Session Checkpoint: SGO Data Extraction Fix and Quality Audit

## Summary

The user reported SGO (SportsGameOdds) API returning very sparse data despite the API being functional — only 1 line stored on April 12 despite the API having ~618 odds entries per game. Investigation revealed two root causes: (1) the `available=false` filter was discarding 92% of valid lines, and (2) SGO only provides per-bookmaker odds on the "over" side, leaving "under" side lines rejected as one-sided. After fixing both issues, a data quality audit revealed alt-line contamination and extreme consensus odds, requiring additional guards. All fixes were deployed iteratively with live verification.

## Key Points

- Diagnosed SGO sparse data (available=false filter + missing under-side)
- Fixed available filter to accept unavailable lines with data
- Added consensus odds fallback for under-side
- Added extreme-odds guard on consensus fallback (±999)
- Added alt-line filter (|odds| >= 1000) at ingestion
- Cleaned 21 bad rows from prod DB

## Execution Snapshot

**Files modified:**
- `src/data/prop_lines.py`: Major refactor of `_extract_sportsgameodds_prop_rows()` function (lines ~416-505)
- Removed `available=false` filter, replaced with data-presence check
- Added consensus odds fallback for under-side (with ±999 guard)
- Added `_available` tracking to prefer available lines over unavailable
- Added alt-line filter (`_ALT_LINE_ODDS_THRESHOLD = 1000`) in `fetch_prop_lines()`
- Cleaned up `_available` internal field before returning rows

**DB changes:**
- Deleted 21 extreme-odds rows from `prop_lines` and `prop_line_snapshots` (April 12 only)
- Deleted all 368 April 12 prop_lines + snapshots for clean re-fetch with improved logic

**Git state:**
- All 4 commits on `main`, pushed to origin
- Branch `fix/sgo-accept-unavailable-lines` exists but main has moved past it
- All 332 tests passing (1 pre-existing failure in test_api_auth skipped)

**Work completed:**
- [x] Diagnosed SGO sparse data (available=false filter + missing under-side)
- [x] Fixed available filter to accept unavailable lines with data
- [x] Added consensus odds fallback for under-side
- [x] Added extreme-odds guard on consensus fallback (±999)
- [x] Added alt-line filter (|odds| >= 1000) at ingestion
- [x] Cleaned 21 bad rows from prod DB
- [x] Added available-line preference logic to reduce alt-line contamination
- [x] Pushed all commits to main
- [ ] Re-fetch April 12 data with improved logic (container deployed but fetch not run)
- [ ] Verify April 12 data quality after re-fetch
- [ ] Compare new April 12 DK/FD agreement (target: ~80% exact, matching historical)

## Technical Details

- Each oddID format: `{statID}-{playerEntity}-{period}-{betType}-{side}` (e.g., `assists-DESMOND_BANE_1_NBA-game-ou-over`)
- Top-level fields: `bookOdds` (string, consensus price), `bookOverUnder` (consensus line), `sideID` (over/under)
- `byBookmaker` dict contains per-bookmaker data: `{bookmaker: {odds, overUnder, available, lastUpdatedAt, ...}}`
- **CRITICAL**: `byBookmaker` typically only exists on the "over" side. The "under" side has consensus data only.
- `available: false` lines still have fresh data (updated same minute) — just means not currently offered for live betting
- Free tier shows "Response is missing 11797 bookmaker odds. Upgrade your API key" — limits bookmaker coverage **Alt-line contamination:**
- SGO returns alt lines alongside primary lines for same player/stat
- Alt lines identifiable by: extreme odds (|odds| >= 1000), large deviations from consensus
- FD fg3m particularly affected: alt lines at 7.5-9.5 with +5000/+10000 odds vs primary at 1.5-3.5
- BFF already handles this via `primary_props` CTE with `DISTINCT ON + ORDER BY ABS(predicted - line) ASC`
- But raw DB data and snapshot P&L calculations are affected if alt lines stored **Consensus odds quality:**
- Consensus `bookOdds` can be extreme (9897, -50000) — not usable as real odds
- Guarded at ±999 threshold before applying as fallback
- After guard, odds diversity is healthy (20-40 distinct values per source/stat) **Cross-source accuracy (verified on overlapping dates):**
- SGO_FD vs OddsAPI FD: 98% exact match, avg diff 0.03 (1,206 pairs)
- SGO_DK vs OddsAPI DK: 96% exact match, avg diff 0.12 (572 pairs)
- SGO is accurate enough to be sole data source during Odds API quota exhaustion **Data volume:**
- OddsAPI: 2,418 DK + 3,117 FD lines across 12-13 days (stopped Apr 4-5, quota)
- SGO: 4,187 SGO_DK + 5,159 SGO_FD lines across 18-19 days (active since Mar 24)
- April 12 post-fix: 321 clean lines from single fetch (SGO only, OddsAPI quota exhausted) **Deployment notes:**
- Container rebuilt 4 times during this session
- Build command: `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache nba-ml-api`
- Up command: `docker compose --env-file .env -f compose/compose.nba-ml.yml up -d nba-ml-api`
- Test fetch: `docker exec nba-ml-api python main.py ingest --props`
- SGO API key: `8efe463dcde774dcd75cf3f7df8a1a1d` (working)
- Odds API key: `eb4a4ca82b5709fde429d542cb9bfcc0` (valid but 500/500 quota until May 1) **Unmapped SGO stat IDs (logged as warning, not extracted):** blocks_steals, fantasyscore, fieldgoalsattempted, fieldgoalsmade, freethrowsattempted, freethrowsmade, points_assists, points_rebounds, rebounds_assists, threepointersattempted, twopointersattempted, twopointersmade

## Important Files

- `src/data/prop_lines.py`
- Core prop line fetching from both APIs (Odds API + SGO)
- **Heavily modified** in this session — 4 commits touching extraction logic
- `_extract_sportsgameodds_prop_rows()` (lines ~380-505): Main SGO extraction with available-preference, consensus fallback, data-presence checks
- `fetch_prop_lines()` (lines ~750-870): Main entry point with floor filter, alt-line filter (|odds|>=1000), one-sided filter
- `_selected_sportsgameodds_bookmakers()` (line 185): Returns ['draftkings', 'fanduel'] based on config
- `_SPORTSGAMEODDS_BOOKMAKER_MAP` (around line 170): Maps SGO bookmaker IDs to source names

- `config.py`
- Modified in prior session: `ODDS_API_MARKETS_PER_REQUEST` 3→8, `ODDS_API_MIN_REQUESTS_REMAINING` 5→50
- Lines 50-60: All Odds API and SGO configuration

- `main.py`
- Modified in prior session: Removed prop fetch from `pipeline()` function
- `pipeline()` line 789-851: Daily pipeline
- `ingest()` line 54-128: CLI command for prop fetching

- `dashboard-ui/server/src/index.ts`
- BFF server — all dashboard API endpoints, reads from DB only
- Has `primary_props` CTE with DISTINCT ON + ORDER BY ABS(predicted - line) to handle alt lines
- NOT modified in this session but critical for understanding how alt lines are handled downstream

## Next Steps

**Immediate (in progress):**
1. **Re-fetch April 12 data** — container is deployed with latest code, April 12 data was deleted from DB. Need to run `docker exec nba-ml-api python main.py ingest --props` and verify:
- DK/FD agreement should be ~80% exact (matching historical, not the 42% from before)
- No extreme odds (|odds| >= 1000) in stored data
- Line values should be reasonable for all stats

2. **Verify data quality** — Run the same audit queries from this session:
- Cross-source agreement (SGO_DK vs SGO_FD)
- Odds diversity per source/stat
- No extreme/null values
- Compare against historical baseline

**Remaining work:**
3. Full weekly retrain to regenerate proper ensemble models (MLflow now resilient from PR #38)
4. When Odds API quota resets (May 1), verify optimized fetch works correctly (~10 calls/day)
5. Consider mapping additional SGO stats (points_assists, points_rebounds, rebounds_assists, blocks_steals could be useful)
6. Add lesson to tasks/lessons.md about SGO data structure quirks
7. Consider adding population labels to dashboard hit rate displays

## Related Wiki Pages

- [[SportsGameOdds (SGO) API]]
- [[Durable Copilot Session Checkpoint]]
- [[Homelab]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sgo-data-extraction-fix-and-quality-audit-76644cc8.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-04-13 |
| URL | N/A |
