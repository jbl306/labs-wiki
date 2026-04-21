---
title: "Copilot Session Checkpoint: Sprint 37 backfill and dashboard enhancements"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, dashboard]
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint 37 backfill and dashboard enhancements
**Session ID:** `8d466128-8017-482d-b021-0fffe970d5eb`
**Checkpoint file:** `/home/jbl/.copilot/session-state/8d466128-8017-482d-b021-0fffe970d5eb/checkpoints/005-sprint-37-backfill-and-dashboa.md`
**Checkpoint timestamp:** 2026-03-29T13:41:10.356796Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user is iterating on the NBA ML Engine project through sprint-based development on a homelab server (beelink-gti13). This session covered Sprints 35-37: fixing DriftReport errors, adding SGO fallback for game lines, running historical tracking stats backfill, and implementing dashboard enhancements (confidence tiers, player P&L, Kelly bankroll simulator, PRA predictions, model-health background job). The approach follows the `execute-sprint-from-report` skill workflow with autonomous implementation, deployment, and verification.
</overview>

<history>
1. User asked to check stuck training pipeline, validate, fix, and deploy Sprint 31 (earlier in session, completed)

2. User invoked execute-sprint-from-report for Sprints 31-33 (earlier, completed)

3. User asked to fix dashboard chart accuracy issues and move Sprint 33 items forward (Sprint 34, completed)

4. User asked to update props page with historical predictions, P&L, Kelly Criterion (Sprint 35, completed)

5. User reported daily pipeline DriftReport error + requested ntfy notifications (Sprint 36, completed)
   - Fixed `drift_report.get()` → `drift_report.drifted_features` attribute access
   - Added ntfy notification for prop ingestion

6. User asked to rerun daily pipeline → completed successfully, DriftReport fix confirmed

7. User asked about 0 settled lines → explained orphan props from SGO (players who didn't play)

8. User asked about 0 game lines in 3:18am pipeline
   - Root cause: `fetch_game_lines()` only used Odds API which returned 401 (quota exhausted)
   - Implemented SportsGameOdds fallback in `game_lines.py`
   - First attempt had bugs: used wrong betTypeID ("spread" instead of "sp"), missed periodID filter (quarter/half totals leaked in at 54.5), used `overUnder` instead of `spread` for spread values
   - Fixed: filter by `periodID='game'`, use `bk_data['spread']` for spread values, `betTypeID='sp'`
   - Verified: 18 game lines fetched with correct spreads (e.g., MIL +14.0), totals (215-245), and moneylines
   - Committed and pushed to main

9. User asked to run historical backfill from Sprint 34 using browser method + move Sprint 34/35 next steps forward (Sprint 37, IN PROGRESS)
   - Created branch `feature/sprint-37-backfill-and-next-steps`
   - Created progress tracker at `tasks/PROGRESS-sprint37-backfill-next-steps-0329.md`
   - Launched tracking stats backfill: `docker exec -d nba-ml-api python main.py backfill --tracking-browser` — 7,397 games missing, running in background (~6 hours)
   - Verified backfill process is running (PID 3215139)
   - Implemented PRA prediction generation in `predictor.py` — derives PRA by summing pts+reb+ast after storing individual predictions
   - Implemented model-health background job:
     - Added `ModelHealthSnapshot` model to `src/db/models.py`
     - Created `model_health_snapshots` table directly in DB
     - Updated `check_model_health()` in dispatcher.py to store results in DB
     - Updated API endpoint to read latest snapshot from DB (instant response)
   - Implemented BFF enhancements in `index.ts`:
     - Added `bankroll` query parameter for Kelly bankroll simulation
     - Added `by_confidence` tier breakdown (High/Medium/Low hit rates)
     - Added `by_player` leaderboard (top/bottom performers, min 3 bets)
     - Added `bankroll_sim` with starting/ending/peak/trough/roi/curve
   - Updated frontend types in `api.ts`: added ConfidenceTierBreakdown, PlayerBreakdown, BankrollSimulation interfaces
   - Updated `PropsPage.tsx` HistoryTab:
     - Added bankroll input field to filters
     - Added confidence tier breakdown section (3-column grid with hit rates)
     - Added bankroll simulator section with balance curve chart
     - Added player P&L leaderboard (top 5 / bottom 5)
   - TypeScript clean (both frontend and BFF)
   - Vite build succeeded
   - **Docker build completed for both nba-ml-api and nba-ml-dashboard**
   - **PENDING: `docker compose up -d` to deploy, then verify endpoints**
</history>

<work_done>
## Sprint 36 (COMPLETE, committed to main)
- `src/data/game_lines.py` — Added SportsGameOdds fallback with correct field mappings (betTypeID='sp' for spreads, periodID='game' filter, `spread` field for spread values)
- `docs/reports/sprint36-drift-fix-ntfy.md` — Sprint report (done earlier)

## Sprint 37 (IN PROGRESS — build done, deploy pending)

### Files Modified:
- `src/inference/predictor.py` — Added PRA prediction derivation in `store_predictions()`: after storing individual stats, sums pts+reb+ast per player and inserts as stat_name='pra', model_name='composite_pra'
- `src/db/models.py` — Added `ModelHealthSnapshot` model (id, checked_at, status, ece, hit_rate, hit_rate_samples, drift_count, alerts JSONB, alert_count, details JSONB)
- `src/notifications/dispatcher.py` — Updated `check_model_health()` to track ece_val/hitrate_val/drift_count during computation and INSERT into model_health_snapshots at the end. Added `import json`.
- `src/api/server.py` — Updated `/evaluation/model-health` endpoint to read latest row from model_health_snapshots table (instant), falls back to live computation if no snapshot exists
- `dashboard-ui/server/src/index.ts` — Extended `/api/props/history`: added `bankroll` param, `by_confidence` tier aggregation, `by_player` aggregation (min 3 bets), `bankroll_sim` with balance curve. Updated cache key and error response.
- `dashboard-ui/src/lib/api.ts` — Added interfaces: ConfidenceTierBreakdown, PlayerBreakdown, BankrollSimulation. Extended PropsHistoryData with by_confidence, by_player, bankroll_sim.
- `dashboard-ui/src/pages/PropsPage.tsx` — HistoryTab: added bankroll input, confidence tier breakdown grid, bankroll simulator section with SignalBoxes and LineChart, player P&L leaderboard (top/bottom 5).
- `tasks/PROGRESS-sprint37-backfill-next-steps-0329.md` — Progress tracker created

### Current State:
- Docker images for nba-ml-api and nba-ml-dashboard are BUILT (compose build --no-cache completed)
- **NOT YET DEPLOYED** — need to run `docker compose up -d` for both services
- Tracking stats backfill is running inside the current nba-ml-api container (will be interrupted by deploy)
- model_health_snapshots table created in DB (persists across deploys)
- All TypeScript and Python syntax checks pass
- Branch: `feature/sprint-37-backfill-and-next-steps` (not yet committed)

### SQL Todo Status:
- tracking-backfill: in_progress (running in background, ~7,397 games)
- pra-predictions: done
- model-health-bg: done
- confidence-tiers: done
- player-pnl: done
- kelly-bankroll: done
- deploy-verify: in_progress
- report-commit: pending (depends on deploy-verify + tracking-backfill)
</work_done>

<technical_details>
### SportsGameOdds API Game Lines Structure
- **oddID format**: `{statID}-{entity}-{period}-{betType}-{side}` (e.g., `points-home-game-sp-home`)
- **betTypeID mapping**: `sp` = spreads, `ou` = totals, `ml` = moneylines, `ml3way` = 3-way moneyline, `eo` = even/odd
- **periodID**: `game` for full game, `1h`/`2h` for halves, `1q`/`2q`/`3q`/`4q` for quarters, `reg` for regulation
- **Spread values**: stored in `bk_data['spread']` (NOT `overUnder`)
- **Total values**: stored in `bk_data['overUnder']`
- **Moneyline values**: stored in `bk_data['odds']`
- **CRITICAL**: Must filter by `periodID == 'game'` to avoid quarter/half lines contaminating data (e.g., 1Q total of 54.5 vs game total of 222.5)
- **statEntityID**: `all` for totals, `home`/`away` for spreads and moneylines

### Tracking Stats Backfill Coverage
- 6,866/14,263 games tracked (48%), 7,397 missing
- Full: 2014-15 through 2017-18 (100%), 2024-25 (100%)
- Partial: 2018-19 (60%), 2025-26 (3%)
- Empty: 2019-20 through 2023-24 (5 full seasons)
- Uses curl_cffi with Chrome TLS impersonation (NOT Playwright/Selenium)
- Rate: ~20 games/minute, estimated ~6 hours total
- CLI: `python main.py backfill --tracking-browser`

### PRA Prediction Generation
- PRA is a composite stat (pts + reb + ast) with NO dedicated model
- Previously derived on-the-fly in BFF `/api/props/history` endpoint
- Now also stored in predictions table: model_name='composite_pra', stat_name='pra'
- Derived in `store_predictions()` after individual stat predictions are stored

### Model Health Background Job
- `model_health_snapshots` table stores periodic health check results
- `check_model_health()` in dispatcher.py now INSERTs after computing ECE/hit-rate/drift
- API endpoint reads latest snapshot (instant) instead of computing inline (was 50+ seconds)
- Falls back to live computation if no snapshot exists (first-time scenario)
- Health check runs daily at 23:00 UTC via Ofelia scheduler (`python main.py health-check`)

### Kelly Bankroll Simulator
- Uses sequential bet processing by date
- Each bet wagered as `balance * kelly_fraction`
- Win: `balance += wager * (decimalOdds - 1)`
- Loss: `balance -= wager`
- Returns starting/ending/peak/trough/roi + daily balance curve

### Deployment
- Server mode (beelink-gti13), deploy locally
- `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache <service> && ... up -d`
- PYTHONUNBUFFERED=1 required for real-time docker exec log output
- Container has no `ps` — use `/proc` or `docker top` to check processes
- Odds API key exhausted (401) — all requests fail, SGO fallback handles it

### Important Gotcha: Backfill + Deploy Conflict
- Tracking backfill is running inside the current nba-ml-api container
- Deploying (docker compose up -d) will recreate the container, killing the backfill
- After deploy, backfill must be restarted: `docker exec -d -e PYTHONUNBUFFERED=1 nba-ml-api python main.py backfill --tracking-browser`
- The backfill is resumable — it finds games missing from game_tracking_stats and only fetches those
</technical_details>

<important_files>
- `src/data/game_lines.py` (~280 lines)
  - Added SportsGameOdds fallback for game lines
  - `_fetch_sgo_game_lines()` function (~120 lines) with pagination, Chrome TLS-like headers
  - `fetch_game_lines()` updated to call SGO fallback when Odds API fails
  - Key: periodID='game' filter, spread in `bk_data['spread']`, betTypeID='sp'

- `src/inference/predictor.py`
  - Added PRA derivation in `store_predictions()` after line ~313
  - Groups by player_id, sums pts+reb+ast predicted/low/high, inserts as 'pra'

- `src/db/models.py`
  - Added `ModelHealthSnapshot` class after BBRefAdvancedStats (end of file)
  - Fields: id, checked_at, status, ece, hit_rate, hit_rate_samples, drift_count, alerts (JSONB), alert_count, details (JSONB)

- `src/notifications/dispatcher.py`
  - Updated `check_model_health()` (lines ~137-270): now tracks ece_val/hitrate_val/drift_count and INSERTs into model_health_snapshots
  - Added `import json` at top

- `src/api/server.py`
  - Updated `/evaluation/model-health` endpoint (lines ~1292-1340): reads from model_health_snapshots table, falls back to live computation

- `dashboard-ui/server/src/index.ts` (~1600 lines)
  - `/api/props/history` endpoint (~lines 628-870): added bankroll param, by_confidence, by_player, bankroll_sim
  - Cache key updated to include bankroll

- `dashboard-ui/src/lib/api.ts`
  - Added types: ConfidenceTierBreakdown, PlayerBreakdown, BankrollSimulation
  - Extended PropsHistoryData interface

- `dashboard-ui/src/pages/PropsPage.tsx` (~550+ lines)
  - HistoryTab: added bankroll input, confidence tier grid, bankroll simulator section, player P&L leaderboard
  - Destructured new fields: by_confidence, by_player, bankroll_sim

- `src/data/nba_browser.py` (413 lines)
  - Contains `ingest_tracking_stats_browser()` — the backfill function currently running
  - Uses curl_cffi with Chrome TLS impersonation for BoxScorePlayerTrackV3

- `tasks/PROGRESS-sprint37-backfill-next-steps-0329.md`
  - Sprint 37 progress tracker
</important_files>

<next_steps>
## Immediate: Deploy and Verify (deploy-verify task)
1. **Deploy both services**: `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml up -d nba-ml-api nba-ml-dashboard`
2. **Verify API health**: `curl http://localhost:8000/health`
3. **Verify model-health endpoint**: `curl http://localhost:8000/evaluation/model-health` — should return from DB or compute first snapshot
4. **Verify props history endpoint**: `curl 'http://localhost:8501/api/props/history?days=30&bankroll=1000'` — should include by_confidence, by_player, bankroll_sim
5. **Restart tracking backfill**: `docker exec -d -e PYTHONUNBUFFERED=1 nba-ml-api python main.py backfill --tracking-browser` (container recreation kills the old one)
6. **Run predictions to generate PRA**: `docker exec -e PYTHONUNBUFFERED=1 nba-ml-api python main.py predict --store` then verify PRA predictions exist
7. **Seed initial model health snapshot**: `docker exec nba-ml-api python main.py health-check`

## After Verification: Report and Commit (report-commit task)
1. Write sprint 37 report at `docs/reports/sprint37-backfill-next-steps.md`
2. Commit all changes on `feature/sprint-37-backfill-and-next-steps` branch
3. Merge to main and push to GitHub
4. Update lessons.md if any new patterns discovered

## Long-running: Tracking Backfill
- Backfill will run for ~6 hours in background
- Resumable — finds missing games automatically
- Monitor with `docker logs nba-ml-api --tail 20` or check DB: `SELECT COUNT(DISTINCT game_id) FROM game_tracking_stats`
- Once complete, mark tracking-backfill todo as done
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
