---
title: "Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "e46b28ceb3142b4379144f0651127cee40410b71fb087908b377ab58ca92a883"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-pipeline-resilience-fixes-dashboard-metrics-inve-3ea0d6d8.md
quality_score: 75
concepts:
  - dashboard-metrics-consistency-and-hit-rate-discrepancy-analysis
related:
  - "[[Registry Health Snapshot Tracking and Dashboard Integration]]"
  - "[[PostgreSQL Materialized Views for Dashboard Optimization]]"
  - "[[Copilot Session Checkpoint: Pipeline Resilience Fixes, Dashboard Metrics Investigation]]"
tier: hot
tags: [dashboard, metrics, hit-rate, data-consistency]
---

# Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis

## Overview

Dashboard metrics consistency ensures that different views or endpoints reporting related statistics (such as hit rates) produce aligned and trustworthy results. Discrepancies can arise from differences in data sources, filtering criteria, or computation methods, which must be diagnosed and resolved to maintain user confidence.

## How It Works

In the NBA ML dashboard, two endpoints report hit rates:

1. **History P&L Endpoint (`/api/props/history`):** Uses `prop_line_snapshots` table filtered for settled bets (`settled_at IS NOT NULL`) joined with a `prediction_blend` Common Table Expression (CTE). It counts 3,360 bets with a hit rate of 51.46%.

2. **Backtest Endpoint (`/api/backtest`):** Uses a materialized view `mv_backtest_summary` derived from `prop_lines`, `predictions`, and `game_logs`. It counts 9,483 bets with a hit rate of 52.52%.

A critical investigation compared the two methods on the same overlapping 6,328 rows and found 100% agreement in settlement results and hit counts (3,372 hits, 53.3%). The approximately 1% difference in overall hit rate is due entirely to different bet populations, not computation logic.

Key technical details include:
- The `prediction_blend` CTE may transform raw predictions differently than the raw `predictions` table used in backtest.
- Deduplication strategies differ: history uses `ROW_NUMBER()` with JavaScript deduplication by player and stat; backtest uses `DISTINCT ON` SQL clause.
- Cache TTLs differ between endpoints (2 minutes vs 5 minutes).

This analysis highlights the importance of:
- Using consistent data sources or clearly labeling metrics to reflect differences.
- Understanding underlying SQL and application logic for metric computation.
- Auditing and testing metrics regularly to detect and explain discrepancies.

Trade-offs include balancing freshness (shorter cache TTL) against performance, and complexity of deduplication logic against accuracy.

## Key Properties

- **Data Source Differences:** History endpoint uses settled props only; backtest includes all predictions with actual game logs.
- **Deduplication Methods:** History uses window functions and JS deduplication; backtest uses SQL DISTINCT ON with ordering.
- **Cache TTL:** History endpoint cache TTL is 2 minutes; backtest cache TTL is 5 minutes, affecting data freshness.

## Limitations

Differences in data populations and deduplication methods can cause confusion if not clearly documented. Metrics computed on incomplete or stale data can mislead users. Cache settings may cause temporary inconsistencies. Without harmonization or clear labeling, users may misinterpret hit rate differences.

## Example

The session tested hit rate agreement by querying the intersection of bets present in both endpoints (6,328 rows). Both methods yielded exactly the same settlement results and hit counts, confirming that the computation logic is consistent. The difference in overall hit rate arises because the history endpoint excludes unsettled bets, while backtest includes all predictions with available game logs.

## Relationship to Other Concepts

- **[[Registry Health Snapshot Tracking and Dashboard Integration]]** — Related to monitoring and verifying data pipeline health and dashboard metrics
- **[[PostgreSQL Materialized Views for Dashboard Optimization]]** — Backtest endpoint uses materialized views for efficient metric computation

## Practical Applications

This analysis is crucial for ML-driven dashboards where multiple endpoints report related metrics. Understanding and documenting data sources, filtering criteria, and deduplication logic prevents user confusion and supports trust in reported statistics. It guides decisions on cache TTLs and data harmonization efforts to improve dashboard consistency.

## Sources

- [[Copilot Session Checkpoint: Pipeline Resilience Fixes, Dashboard Metrics Investigation]] — primary source for this concept
