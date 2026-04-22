---
title: "Dashboard Expansion with Player Profile, Waiver Wire, and Data Health Tabs"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "f5ab464da78849dfc56ba65763a75665270132841e455836342a982aa3b2217d"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-phases-1-4-implementation-and-deployment-16041f82.md
quality_score: 56
concepts:
  - dashboard-expansion-player-profile-waiver-wire-data-health
related:
  - "[[Streamlit Dashboard]]"
  - "[[Copilot Session Checkpoint: Phases 1-4 Implementation and Deployment]]"
tier: hot
tags: [dashboard, data-visualization, sports-analytics, streamlit]
---

# Dashboard Expansion with Player Profile, Waiver Wire, and Data Health Tabs

## Overview

The dashboard expansion introduces new interactive tabs to enhance user experience and data visibility for the NBA ML Engine. These include a detailed player profile drill-down, a waiver wire analytics tab with advanced statistical computations, and a data health overview panel monitoring database freshness and completeness.

## How It Works

The player profile tab is accessible via query parameters (`?player_id=X`) and hides main tabs to focus on detailed player data. It integrates multiple data loaders fetching player lists, game logs, predictions, injuries, and season stats. The waiver wire tab computes z-scores for players' last 10 games against season baselines using SQL window functions and CTEs, enabling leaderboard and radar chart visualizations with category and position filters. The data health tab aggregates per-table row counts, freshness ages, and completeness metrics, displaying them with freshness badges (fresh, stale, critical) and completeness scores. These tabs are implemented in Streamlit within `dashboard/app.py` with modular data loaders and render functions. The dashboard also underwent typography and UX improvements for better readability and interaction.

## Key Properties

- **Player Profile:** Drill-down page with game log charts, rolling averages, injury history, and prediction overlays.
- **Waiver Wire:** Z-score leaderboard using SQL window functions and standard deviation population (STDDEV_POP).
- **Data Health:** Comprehensive metrics on data freshness, completeness, and row counts with semantic badges.

## Limitations

Some UX improvements like chart styling overhaul and signal card upgrades are pending. Data freshness depends on ETL pipeline reliability.

## Example

Waiver wire SQL snippet:
```sql
WITH last_10_games AS (
  SELECT player_id, stat, game_date,
         ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY game_date DESC) AS rn
  FROM game_logs
  WHERE rn <= 10
), z_scores AS (
  SELECT player_id, stat, AVG(stat) AS avg_stat, STDDEV_POP(stat) AS stddev_stat
  FROM last_10_games
  GROUP BY player_id, stat
)
SELECT player_id, stat, (avg_stat - season_baseline) / stddev_stat AS z_score
FROM z_scores
```

## Relationship to Other Concepts

- **[[Streamlit Dashboard]]** — Dashboard expansion implemented using Streamlit framework.
- **SQL Window Functions** — Used for computing z-scores and ranking in waiver wire tab.

## Practical Applications

Provides NBA analysts and users with rich interactive tools for player evaluation, waiver wire decisions, and monitoring data quality in ML-powered sports analytics platforms.

## Sources

- [[Copilot Session Checkpoint: Phases 1-4 Implementation and Deployment]] — primary source for this concept
