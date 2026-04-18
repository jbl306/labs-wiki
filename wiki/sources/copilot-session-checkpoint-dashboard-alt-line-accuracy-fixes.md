---
title: "Copilot Session Checkpoint: Dashboard Alt-Line Accuracy Fixes"
type: source
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "d12567d0a0a05fa3d657bf2e2ec6bb6e9fa482a9676eee6bf73ec13f8bbf53c0"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-dashboard-alt-line-accuracy-fixes-466ff308.md
quality_score: 100
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
tier: archive
tags: [sports-betting, nba-ml-engine, fileback, dashboard, checkpoint, data-accuracy, copilot-session, machine-learning, kelly-criterion, homelab, durable-knowledge, data-cleaning]
checkpoint_class: project-progress
retention_mode: compress
---

# Copilot Session Checkpoint: Dashboard Alt-Line Accuracy Fixes

## Summary

This session checkpoint documents the iterative development and deployment of fixes for the NBA ML Engine dashboard, focusing on correcting data accuracy issues caused by SportsGameOdds DraftKings alternate/game-prop lines. The fixes include refining prediction line selection logic, filtering one-sided props, and improving bankroll simulation accuracy, all deployed and verified on a homelab server.

## Key Points

- Identified and fixed contamination of confidence scores and P&L calculations by alternate/game-prop lines from SportsGameOdds DraftKings data.
- Implemented a SQL-based selection of primary prop lines closest to model predictions to avoid alt-line distortions.
- Added ingestion-level filters to exclude one-sided prop lines missing either over or under odds.
- Adjusted Kelly bankroll simulator to use quarter-Kelly sizing with a daily exposure cap for realistic wager sizing.
- Deployed fixes on local homelab server with Docker, verified API health and dashboard data accuracy.

## Concepts Extracted

- **[[Primary Prop Line Selection to Avoid Alternate Line Contamination]]** — In sports betting data, alternate or game-prop lines can distort model confidence scores and profit-and-loss (P&L) calculations if not properly filtered. This concept addresses the problem of selecting the correct primary prop line from multiple lines per player and stat, especially when data sources provide alternate lines that differ significantly from primary market lines.
- **[[One-Sided Prop Line Filtering in Sports Betting Data]]** — One-sided prop lines in sports betting data are those where either the over or under odds are missing (NULL), often representing non-standard bets like 'will the player get 3+ blocks?'. These lines can distort analytics and must be filtered out during data ingestion to maintain data quality.
- **[[Kelly Bankroll Simulator with Quarter-Kelly Sizing and Daily Exposure Cap]]** — The Kelly criterion is a formula used to size bets optimally to maximize logarithmic growth of bankroll. However, applying full Kelly sizing across many daily bets can lead to unrealistic bankroll growth estimates. This concept describes a practical adjustment using quarter-Kelly sizing and a daily exposure cap to produce realistic bankroll simulations.

## Entities Mentioned

- **[[NBA ML Engine]]** — An ML-driven sports betting analytics system focused on NBA games, deployed on a homelab server. It includes prediction generation, model health snapshotting, and a dashboard for confidence and P&L tracking. The system integrates data ingestion from SportsGameOdds, prediction modeling, and dashboard visualization.
- **SportsGameOdds (SGO) DraftKings Data** — A sports betting data source providing player prop lines including primary and alternate lines for NBA games. The data includes over/under odds for various player statistics but contains alternate lines that can distort analytics if not filtered properly. It also includes one-sided prop lines with missing odds on one side.
- **[[Docker]]** — A containerization platform used to deploy and manage the NBA ML Engine services (nba-ml-api, nba-ml-dashboard, nba-ml-db) on a homelab server. Docker Compose is used to build and run containers with environment variables and service dependencies.

## Notable Quotes

> "The SGO extractor uses `setdefault()` with key `(player_id, date, source, stat_name)` — whichever line comes first wins, and DK alts come first." — Technical Details
> "Full Kelly across 30+ daily bets compounds to absurd numbers (quintillions). Correct approach: quarter-Kelly (0.25×) with 25% daily exposure cap." — Technical Details
> "Added filter rejecting prop lines where `over_odds IS NULL OR under_odds IS NULL` to remove one-sided game props." — Work Done

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-dashboard-alt-line-accuracy-fixes-466ff308.md` |
| Type | note |
| Author | Unknown |
| Date | 2026-04-18T03:23:51.483387Z |
| URL | N/A |
