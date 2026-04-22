---
title: "Copilot Session Checkpoint: Odds API Quota Optimization, SGO Investigation"
type: source
created: 2026-04-13
last_verified: 2026-04-21
source_hash: "c4cd8c8e81648711e1dbceea098279d1120878d54e1d8ae18c7015937060ae6d"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-odds-api-quota-optimization-sgo-investigation-f4c98efb.md
quality_score: 90
concepts:
  - odds-api-quota-optimization
  - cascading-pipeline-failure-diagnosis-and-resilience
  - sportsgameodds-sgo-api-data-extraction-challenges
related:
  - "[[Odds API Quota Optimization]]"
  - "[[Cascading Pipeline Failure Diagnosis and Resilience]]"
  - "[[SportsGameOdds (SGO) API Data Extraction Challenges]]"
  - "[[Odds API]]"
  - "[[SportsGameOdds (SGO) API]]"
  - "[[Homelab]]"
  - "[[NBA ML Engine]]"
tier: archive
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard, api, sports-betting, quota-optimization, pipeline-resilience, data-extraction]
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: validated
---

# Copilot Session Checkpoint: Odds API Quota Optimization, SGO Investigation

## Summary

The user reported three dashboard issues: stale props (April 7 instead of today), hit rate discrepancies between pages, and requested a full metrics audit. Investigation revealed cascading pipeline failures (missing ensemble models, MLflow DNS failure, Odds API 401). All code fixes were implemented, tested, deployed. Then the user asked about API quota waste — discovered the Odds API 500 calls/month quota was exhausted due to double-fetching and over-chunking. Implemented quota optimizations reducing usage from ~1,530 to ~300 calls/month. Currently investigating why SGO (SportsGameOdds) is returning very sparse data despite the API being functional.

## Key Points

- Diagnosed and fixed props fallback (missing ensemble models)
- Diagnosed and fixed MLflow DNS failure resilience
- Diagnosed hit rate discrepancy (different populations, not a bug)
- Fixed /prop-hit-rate mixed data sources
- Wrote tests and sprint report
- Identified Odds API quota exhaustion as root cause of 401

## Execution Snapshot

**Files modified and deployed:**
- `src/inference/predictor.py`: Added `_FALLBACK_ORDER` and `_try_fallback_model()` for resilient model loading
- `src/training/trainer.py`: Added `_mlflow_available` flag and `_ensure_mlflow()` with local tracking fallback
- `src/api/server.py`: Fixed `/prop-hit-rate` to use matview totals consistently (line 689: `total=model_total if model_total > 0 else total`)
- `config.py`: Changed `ODDS_API_MIN_REQUESTS_REMAINING` 5→50, `ODDS_API_MARKETS_PER_REQUEST` 3→8
- `main.py`: Removed prop fetch from pipeline() function (Step 4), kept game lines
- `src/data/prop_lines.py`: Added quota usage logging after Odds API fetch
- `tasks/lessons.md`: 4 new lessons added
- `tests/test_pipeline_resilience.py`: Created — 9 tests (fallback, MLflow, hit rate)
- `docs/reports/sprint54-pipeline-resilience.md`: Created — sprint results report

**Files deployed:**
- PR #38 merged (pipeline resilience fixes)
- PR #39 merged (quota optimization)
- Both containers rebuilt and deployed (nba-ml-api, nba-ml-dashboard)

**Work completed:**
- [x] Diagnosed and fixed props fallback (missing ensemble models)
- [x] Diagnosed and fixed MLflow DNS failure resilience
- [x] Diagnosed hit rate discrepancy (different populations, not a bug)
- [x] Fixed /prop-hit-rate mixed data sources
- [x] Wrote tests and sprint report
- [x] Identified Odds API quota exhaustion as root cause of 401
- [x] Implemented quota optimization (1530→300 calls/month)
- [x] Deployed all fixes to production containers
- [ ] SGO data investigation — API works but fetcher returns very sparse data (IN PROGRESS)
- [ ] Full weekly retrain to regenerate proper ensemble models

## Technical Details

- April 11 training interrupted mid-ensemble assembly — only pts and fg3m ensemble pkls saved, 7 stats had base models only
- April 12 weekly retrain failed because MLflow container was restarting (DNS resolution failure for nba-ml-mlflow)
- Odds API key valid but 500/500 quota exhausted — 401 on all prop/game line requests since ~April 4-5 **Odds API quota math:**
- Old: ~51 calls/day (pipeline 07:00 + props-refresh 22:00) × 30 = ~1,530/month on 500 budget
- New: ~10 calls/day (props-refresh 22:00 only, 8 markets/request) × 30 = ~300/month
- Quota resets: 1st of each month at 12:00 AM UTC **Hit rate — three different views, all correct:**
- History P&L: 3,360 bets, 51.46% (from prop_line_snapshots with settlement)
- Backtest: 9,483 bets, 52.52% (from mv_backtest_summary via predictions×game_logs)
- Prop Hit Rate: 9,941 bets, 51.98% (from mv_daily_hit_rates)
- 100% agreement when computed on same overlapping data (6,328 rows) **SGO API status (NEEDS INVESTIGATION):**
- API key works: `NBA_ML_SPORTSGAMEODDS_API_KEY=8efe463dcde774dcd75cf3f7df8a1a1d`
- API returns rich data: 618 odds entries per game, all player stats present
- "Response is missing 11797 bookmaker odds. Upgrade your API key to access all data"
- Despite API having data, SGO_DK stopped April 10, SGO_FD only 1 PRA line April 12
- SGO odds structure: `bookOdds` field contains bookmaker data, oddID format is `{statID}-{playerEntity}-{period}-{betType}-{side}`
- Need to check `_extract_sportsgameodds_prop_rows()` and `_selected_sportsgameodds_bookmakers()` to see why lines aren't being extracted
- The `bookOdds` field value might be a string not a dict (saw `AttributeError: 'str' object has no attribute 'keys'` during investigation) **Deployment gotchas:**
- Must use `--env-file .env` when running docker compose or all env vars are blank
- `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache <service> && up -d <service>`
- `NBA_ML_ENGINE_PATH` is relative (`../../nba-ml-engine`) — use absolute path override when needed **DB schema notes:**
- `prop_lines` columns: player_id, game_date, source, stat_name, line, over_odds, under_odds, fetched_at, opponent, is_home, game_time
- `players` columns: id (PK), nba_api_id, name, name_normalized, position, team, active, etc.
- Join: `prop_lines.player_id = players.id` (not players.player_id)
- No `game_schedule` table exists — use `game_lines` for game data **Container status (as of deployment):**
- nba-ml-api: Rebuilt with all fixes, running
- nba-ml-dashboard: Rebuilt, running on port 8501 (BFF + React)
- nba-ml-mlflow: Running, accessible (was transiently down during training)
- nba-ml-db: Healthy
- nba-ml-scheduler: Running (Ofelia cron jobs)

## Important Files

- `src/data/prop_lines.py`
- Core prop line fetching from both APIs (Odds API + SGO)
- MODIFIED: Added quota logging (line ~763)
- `_fetch_odds_api_prop_rows()` line 464-617: Odds API fetcher with market chunking
- `_fetch_sportsgameodds_prop_rows()` line 673-731: SGO fetcher with pagination
- `_extract_sportsgameodds_prop_rows()`: Extracts prop rows from SGO event — NEEDS INVESTIGATION for why it's returning sparse data
- `_selected_sportsgameodds_bookmakers()`: Determines which SGO bookmakers to extract — NEEDS INVESTIGATION
- `fetch_prop_lines()` line 734: Main entry point, calls both APIs

- `config.py`
- MODIFIED: `ODDS_API_MARKETS_PER_REQUEST` 3→8, `ODDS_API_MIN_REQUESTS_REMAINING` 5→50
- Lines 50-60: All Odds API and SGO configuration

- `main.py`
- MODIFIED: Removed prop fetch from `pipeline()` function (was Step 4, now skipped)
- `pipeline()` line 789-851: Daily pipeline
- `ingest()` line 54-128: CLI command for prop fetching

- `src/inference/predictor.py`
- MODIFIED: Added `_FALLBACK_ORDER` and `_try_fallback_model()` method
- `_load_production_models()` line 84-136 + fallback after

- `src/training/trainer.py`
- MODIFIED: Added `_ensure_mlflow()` function with local tracking fallback
- Lines ~44-67: MLflow resilience code

- `src/api/server.py`
- MODIFIED: Fixed `/prop-hit-rate` total to use matview data consistently (line 689)
- Line 618-716: `/prop-hit-rate` endpoint

- `~/projects/homelab/compose/compose.nba-ml.yml`
- Cron schedules: pipeline-daily (07:00 UTC), props-refresh (22:00 UTC), predict-refresh (22:15 UTC), weekly-retrain (Sunday 16:00 UTC)
- NOT MODIFIED — props-refresh cron still runs at 22:00 UTC (this is correct)

- `dashboard-ui/server/src/index.ts`
- BFF server — all dashboard API endpoints, reads from DB only, NO external API calls
- NOT MODIFIED

- `tests/test_pipeline_resilience.py`
- CREATED: 9 tests for fallback loading, MLflow resilience, hit rate consistency

## Next Steps

**Immediate — SGO data investigation (actively working):**
1. Debug why SGO fetcher returns sparse data despite API having rich odds:
- Check `_extract_sportsgameodds_prop_rows()` function logic
- Check `_selected_sportsgameodds_bookmakers()` — may be filtering too aggressively
- The `bookOdds` field structure may have changed — saw evidence it might be a string not dict
- SGO oddID format: `{statID}-{playerEntity}-{period}-{betType}-{side}`
- Raw API shows ~618 odds/game with all player stats, but only 1 line stored for April 12
- Key question: are DK/FD bookmaker odds still in the free tier, or gated behind upgrade?

2. Test a manual SGO fetch to see logs/warnings:
- `docker exec nba-ml-api python main.py ingest --props` and check logs
- Look for "skipping" or "unmatched" warnings in SGO extraction

**Remaining work:**
3. Trigger full weekly retrain to regenerate proper ensemble models (MLflow now resilient)
4. When Odds API quota resets (May 1), verify optimized fetch works correctly (~10 calls/day)
5. Consider adding population labels to dashboard hit rate displays
6. Consider model registry validation at startup (verify pkl files match DB entries)

## Related Wiki Pages

- [[Odds API Quota Optimization]]
- [[Cascading Pipeline Failure Diagnosis and Resilience]]
- [[SportsGameOdds (SGO) API Data Extraction Challenges]]
- [[Odds API]]
- [[SportsGameOdds (SGO) API]]
- [[Homelab]]
- [[NBA ML Engine]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-odds-api-quota-optimization-sgo-investigation-f4c98efb.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-04-13 |
| URL | N/A |
