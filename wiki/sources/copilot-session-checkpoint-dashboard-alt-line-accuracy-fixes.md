---
title: "Copilot Session Checkpoint: Dashboard Alt-Line Accuracy Fixes"
type: source
created: 2026-03-29
last_verified: 2026-04-21
source_hash: "d12567d0a0a05fa3d657bf2e2ec6bb6e9fa482a9676eee6bf73ec13f8bbf53c0"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-dashboard-alt-line-accuracy-fixes-466ff308.md
quality_score: 90
concepts:
  - primary-prop-line-selection-to-avoid-alternate-line-contamination
  - one-sided-prop-line-filtering-in-sports-betting-data
  - kelly-bankroll-simulator-quarter-kelly-sizing-daily-exposure-cap
related:
  - "[[Primary Prop Line Selection to Avoid Alternate Line Contamination]]"
  - "[[One-Sided Prop Line Filtering in Sports Betting Data]]"
  - "[[Kelly Bankroll Simulator with Quarter-Kelly Sizing and Daily Exposure Cap]]"
  - "[[NBA ML Engine]]"
  - "[[Docker]]"
  - "[[Homelab]]"
tier: hot
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, dashboard, sports-betting, data-accuracy, machine-learning, kelly-criterion, data-cleaning]
checkpoint_class: durable-debugging
retention_mode: retain
knowledge_state: validated
---

# Copilot Session Checkpoint: Dashboard Alt-Line Accuracy Fixes

## Summary

The user is iterating on the NBA ML Engine project through sprint-based development on a homelab server (beelink-gti13). This session segment focused on deploying Sprint 37 changes (PRA predictions, model health snapshots, dashboard analytics), then diagnosing and fixing critical dashboard data accuracy issues caused by SportsGameOdds (SGO) DraftKings alternate/game-prop lines contaminating confidence scores, hit rates, and P&L calculations. The approach followed autonomous investigation, fix, deploy, and verify cycles.

## Key Points

- Sprint 37 deployment was pending (build done, not yet deployed)
- Fixed with quarter-Kelly (0.25×) sizing and 25% daily exposure cap using start-of-day balance
- After fix: $1000 → $1531 (53.1% ROI over 5 days) — realistic
- Committed Sprint 37 to main, pushed to GitHub (9 files, +507/-19)
- First fix attempt: MAX line per player+stat — but this picked high alt lines on the other extreme (Clingan reb 14.5)
- Second fix: Pick line **closest to model prediction** via `DISTINCT ON ... ORDER BY ABS(predicted_value - line) ASC` — this naturally selects primary market lines

## Execution Snapshot

**## Files Modified:**

**### Sprint 37 deployment + Kelly fix:**
- `dashboard-ui/server/src/index.ts` — Kelly bankroll simulator: quarter-Kelly (0.25×) with 25% daily exposure cap, start-of-day balance for wager sizing
- `src/inference/predictor.py` — PRA prediction derivation (pts+reb+ast sum)
- `src/db/models.py` — ModelHealthSnapshot model
- `src/notifications/dispatcher.py` — check_model_health() stores snapshots in DB
- `src/api/server.py` — model-health endpoint reads from DB (instant vs 50s)
- `dashboard-ui/src/lib/api.ts` — Added ConfidenceTierBreakdown, PlayerBreakdown, BankrollSimulation types
- `dashboard-ui/src/pages/PropsPage.tsx` — HistoryTab: bankroll input, tier breakdown, bankroll sim chart, player P&L leaderboard

**### Alt-line fix (committed to main):**
- `dashboard-ui/server/src/index.ts` — Three query fixes:
1. Overview: `primary_props` CTE picks line closest to prediction per player+stat
2. History: `ranked_snaps` CTE with `ROW_NUMBER() PARTITION BY player_id, game_date, stat_name ORDER BY ABS(predicted_value - line) ASC` + `WHERE rn = 1`
3. Props page: Same `primary_props` pattern for confidence rankings
- `tasks/lessons.md` — Added SGO alt-line contamination lesson

**### One-sided prop filter (committed to main, deployed):**
- `src/data/prop_lines.py` (~line 757) — Added filter rejecting prop lines where `over_odds IS NULL OR under_odds IS NULL`
- DB cleanup: Deleted 814 prop_lines + 1,840 prop_line_snapshots with missing odds

**### Sprint report:**
- `docs/reports/sprint37-backfill-dashboard-enhancements.md` — Full sprint report

**## Current State:**
- All three services running (nba-ml-api, nba-ml-dashboard, nba-ml-db)
- API healthy, dashboard serving correct data
- Predictions generated for today (3/29): 5,621 predictions
- Tracking backfill needs restart (container was recreated by API deploy)
- All changes committed to main and pushed to GitHub

**## Git State:**
- Branch: `main` (all sprint-37 work merged)
- Latest commits: Sprint 37 commit, alt-line fix, lesson, one-sided prop filter
- Clean working tree (need to verify after last API rebuild)

## Technical Details

- SportsGameOdds DraftKings data includes alternate/game-prop lines alongside primary O/U lines
- DK alt lines: ast 2.5 (primary 7.5), reb 2.5 (primary 8.5), blk 2.5 (primary 0.5)
- The SGO extractor uses `setdefault()` with key `(player_id, date, source, stat_name)` — whichever line comes first wins, and DK alts come first
- One-sided game props: `over_odds` present but `under_odds IS NULL`, often with extreme over odds (+800)
- Fix: `primary_props` CTE picks line closest to model prediction; ingestion rejects lines missing either side's odds ### Kelly Bankroll Simulator
- Full Kelly across 30+ daily bets compounds to absurd numbers (quintillions)
- Correct approach: quarter-Kelly (0.25×) with 25% daily exposure cap
- All wagers sized from start-of-day balance, not running balance
- If total raw wagers exceed daily cap, all wagers scaled proportionally ### Prop Line Snapshot Duplicates
- Same snapshot created multiple times in one settlement run (unique constraint includes `fetched_at` timestamp)
- Pipeline runs 3x/day creates 3 snapshots per prop line per source
- BFF deduplication by `player_name|stat_name|game_date` handles this but was keeping wrong line (highest confidence = alt line)
- Fixed by SQL-level deduplication via `ROW_NUMBER()` before BFF processing ### Deployment Details
- Server: beelink-gti13, deploy locally
- `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache <service> && ... up -d`
- PYTHONUNBUFFERED=1 required for real-time docker exec output
- Container has no `ps` — use `/proc` or `docker top` for process checks
- Tracking backfill is resumable but killed by container recreation ### Edge Policy
- API returns `excluded_stats: ["fg_pct", "ft_pct"]` (NOT pts/ast)
- Fallback policy in BFF also excludes pts, ast — but API policy takes precedence when reachable
- Per-stat minimum edge thresholds: pts 10%, reb/ast/tov/fg3m 8%, stl/blk 5%, fg_pct/ft_pct 15% ### Data Accuracy After Fixes
- History: 1,401 bets, 53.5% hit rate, +99u flat (7.1% ROI) — verified manually
- High confidence: 42 bets, 71.4% hit rate
- Medium: 536 bets, 51.9%
- Low: 823 bets, 53.7%
- 3/1401 edge cases where pred==line exactly (0.2%) show as hit=False incorrectly — negligible

## Important Files

- `dashboard-ui/server/src/index.ts` (~1600+ lines)
- Central BFF serving all dashboard API endpoints
- Lines ~316-370: Overview best_predictions query with `primary_props` CTE
- Lines ~666-700: History query with `ranked_snaps` CTE for primary line selection
- Lines ~851-890: Kelly bankroll simulator (quarter-Kelly, 25% daily cap)
- Lines ~1534-1580: Props page confidence rankings with `primary_props` CTE
- Lines 28-43: FALLBACK_EDGE_POLICY with stat thresholds and excluded stats
- Lines 45-57: PREDICTION_BLEND_CTE (shared across queries)

- `src/data/prop_lines.py` (~800 lines)
- Lines 331-421: `_extract_sportsgameodds_prop_rows()` — SGO prop extraction with `rows_by_key` dedup
- Lines 633-691: `_fetch_sportsgameodds_prop_rows()` — SGO API pagination
- Lines ~748-765: Stat floor filter + one-sided prop filter (new)
- Lines 765-783: Snapshot creation (plain INSERT, creates duplicates across pipeline runs)

- `src/inference/predictor.py`
- PRA prediction derivation in `store_predictions()` — sums pts+reb+ast per player

- `src/db/models.py`
- `ModelHealthSnapshot` model at end of file

- `src/notifications/dispatcher.py`
- `check_model_health()` stores snapshots in DB after computation

- `src/api/server.py`
- `/evaluation/model-health` reads latest snapshot (instant), falls back to live computation

- `dashboard-ui/src/pages/PropsPage.tsx`
- HistoryTab: bankroll input, confidence tier grid, bankroll sim chart, player P&L leaderboard

- `tasks/lessons.md`
- Contains SGO alt-line contamination lesson (2025-03-29)

- `docs/reports/sprint37-backfill-dashboard-enhancements.md`
- Sprint 37 report (note: pre-dates the alt-line and one-sided prop fixes)

## Next Steps

**## Immediate:**
- Verify git working tree is clean after last API rebuild/deploy
- Commit the one-sided prop filter change if not yet committed
- Restart tracking backfill: `docker exec -d -e PYTHONUNBUFFERED=1 nba-ml-api python main.py backfill --tracking-browser` (was killed by API container recreation)
- Seed initial model health snapshot: `docker exec nba-ml-api python main.py health-check`

**## Should Do:**
- Fix SGO DK alt-line issue at ingestion level (the `setdefault` picks first line seen; should prefer line closest to historical average or highest line)
- Clean up prop_line_snapshots duplicate entries (same source+line appears multiple times from multiple pipeline runs)
- Add unique constraint or ON CONFLICT handling to prevent future snapshot duplicates
- Update Sprint 37 report to reflect the alt-line and one-sided prop fixes

**## Tracking:**
- SQL todos: `tracking-backfill` still in_progress (7,397 games, ~6 hours, resumable)
- All other Sprint 37 todos complete

## Related Wiki Pages

- [[Primary Prop Line Selection to Avoid Alternate Line Contamination]]
- [[One-Sided Prop Line Filtering in Sports Betting Data]]
- [[Kelly Bankroll Simulator with Quarter-Kelly Sizing and Daily Exposure Cap]]
- [[NBA ML Engine]]
- [[Docker]]
- [[Homelab]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-dashboard-alt-line-accuracy-fixes-466ff308.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-29 |
| URL | N/A |
