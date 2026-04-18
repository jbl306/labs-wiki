---
title: "PostgreSQL Materialized Views for Dashboard Optimization"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "775f812f7b3878f9c18195d90e9cda4785608659d21041c4a0edfdd122da8024"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-dashboard-matviews-implementation-in-progress-afa2957e.md
quality_score: 100
concepts:
  - postgresql-materialized-views-for-dashboard-optimization
related:
  - "[[Database Indexing For Performance Optimization]]"
  - "[[Copilot Session Checkpoint: Dashboard Matviews Implementation In Progress]]"
tier: hot
tags: [postgresql, materialized-views, database-optimization, dashboard]
---

# PostgreSQL Materialized Views for Dashboard Optimization

## Overview

Materialized views in PostgreSQL are database objects that store the results of a query physically, allowing expensive computations to be precomputed and queried efficiently. This concept is critical for optimizing dashboard performance by reducing on-demand computation overhead, especially for complex aggregations and joins.

## How It Works

PostgreSQL materialized views store the output of a query as a physical table that can be refreshed periodically or on demand. Unlike regular views, which execute the underlying query each time they are accessed, materialized views cache the data, providing faster read access at the cost of needing explicit refreshes to keep data current.

The implementation described defines multiple materialized views to precompute heavy aggregations such as hit rates, backtest summaries, player rankings, customer lifetime value (CLV), and dashboard metrics. Each matview is defined with a unique index to support the `REFRESH MATERIALIZED VIEW CONCURRENTLY` command, which allows refreshing the view without locking out reads, thus maintaining availability.

The refresh function attempts a concurrent refresh first; if the matview is empty (which disallows concurrent refresh), it falls back to a blocking refresh. This strategy ensures minimal disruption in production environments.

In the dashboard architecture, the Backend-For-Frontend (BFF) server replaces complex Common Table Expressions (CTEs) and joins with simple `SELECT FROM matview` queries. This reduces query execution time significantly. The BFF also maintains an LRU cache with a configurable TTL to balance freshness and performance.

The matviews are integrated into the existing pipeline, which already calls the refresh function after quality assurance steps, eliminating the need for additional cron jobs. This ensures that the dashboard data remains up to date with minimal manual intervention.

Trade-offs include the need to manage matview refreshes carefully to avoid stale data and the complexity of maintaining unique indexes for concurrency. Some queries that require dynamic parameters (e.g., variable date ranges) may not fully benefit from matviews and might require fallback queries or additional matview variants.

## Key Properties

- **Refresh Strategy:** Uses `REFRESH MATERIALIZED VIEW CONCURRENTLY` with fallback to blocking refresh if the matview is empty.
- **Unique Indexes:** Each matview has a unique index to enable concurrent refresh.
- **Integration:** Matviews are integrated into the BFF layer to replace heavy on-demand queries.
- **Caching:** BFF uses LRU caching with TTL to balance freshness and performance.

## Limitations

Concurrent refresh cannot be used on empty matviews, requiring fallback to blocking refresh which can lock reads temporarily. Matviews with hardcoded parameters (e.g., fixed 30-day window for rankings) limit flexibility and may require fallback queries for other parameter values. JSONB columns in matviews provide flexibility but may complicate querying and indexing.

## Example

Example matview definition snippet in `scripts/optimize_db.py`:

```python
MATERIALIZED_VIEWS = {
  'mv_player_rankings': '''
    CREATE MATERIALIZED VIEW mv_player_rankings AS
    SELECT player_id, SUM(pts*1.0 + reb*1.2 + ast*1.5 + stl*2.0 + blk*2.0 - tov*1.0) AS composite_score
    FROM player_stats
    WHERE game_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY player_id
  '''
}

# Unique index for concurrent refresh
MV_UNIQUE_INDEXES = {
  'mv_player_rankings': 'CREATE UNIQUE INDEX idx_mv_player_rankings_player_id ON mv_player_rankings(player_id)'
}

# Refresh function tries concurrent refresh first
try:
  REFRESH MATERIALIZED VIEW CONCURRENTLY mv_player_rankings
except ConcurrentRefreshError:
  REFRESH MATERIALIZED VIEW mv_player_rankings
```

## Relationship to Other Concepts

- **[[Database Indexing For Performance Optimization]]** — Materialized views rely on unique indexes to enable concurrent refresh and fast querying.
- **Backend-For-Frontend (BFF) Pattern** — Matviews are integrated into the BFF layer to optimize API endpoint performance.

## Practical Applications

Used to optimize dashboards with heavy aggregation queries by precomputing results, reducing latency and server load. Applicable in any system where complex analytics or reporting queries degrade performance when computed on-demand. Enables smoother user experience and scalability in data-intensive applications.

## Sources

- [[Copilot Session Checkpoint: Dashboard Matviews Implementation In Progress]] — primary source for this concept
