---
title: "Concurrent Refresh of PostgreSQL Materialized Views"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "775f812f7b3878f9c18195d90e9cda4785608659d21041c4a0edfdd122da8024"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-dashboard-matviews-implementation-in-progress-afa2957e.md
quality_score: 0
concepts:
  - concurrent-refresh-postgresql-materialized-views
related:
  - "[[PostgreSQL Materialized Views for Dashboard Optimization]]"
  - "[[Copilot Session Checkpoint: Dashboard Matviews Implementation In Progress]]"
tier: hot
tags: [postgresql, materialized-views, concurrent-refresh, database-availability]
---

# Concurrent Refresh of PostgreSQL Materialized Views

## Overview

Concurrent refresh allows a PostgreSQL materialized view to be refreshed without locking out reads, enabling continuous availability of data during refresh operations. This is crucial for production systems requiring high uptime and minimal query disruption.

## How It Works

By default, refreshing a materialized view in PostgreSQL locks the view for reads and writes, blocking queries until the refresh completes. The `REFRESH MATERIALIZED VIEW CONCURRENTLY` command mitigates this by creating a new copy of the view data in the background and then swapping it atomically with the old data. This process requires the materialized view to have a unique index to identify rows for the swap.

The refresh process proceeds as follows:

1. A new temporary table is populated with the fresh query results.
2. The unique index ensures rows can be matched between the old and new data.
3. Once the new data is ready, PostgreSQL atomically replaces the old materialized view data with the new data.
4. Queries continue to read from the old data until the swap completes, avoiding downtime.

However, concurrent refresh cannot be used on an empty materialized view because the unique index cannot be enforced without data. In such cases, a blocking refresh is required to initially populate the view.

In the implementation, the refresh function attempts the concurrent refresh first and falls back to a blocking refresh if an error occurs (e.g., on first populate). This approach balances availability with correctness.

Trade-offs include slightly higher resource usage during concurrent refresh due to maintaining two copies of the data temporarily and the complexity of managing unique indexes. Also, concurrent refresh is not available for matviews without unique indexes or those with certain types of queries.

## Key Properties

- **Requirement:** Materialized view must have a unique index to support concurrent refresh.
- **Fallback:** Fallback to blocking refresh if concurrent refresh fails (e.g., empty matview).
- **Availability:** Allows reads to continue during refresh, minimizing downtime.

## Limitations

Cannot be used on empty materialized views or those lacking unique indexes. Initial population requires blocking refresh, causing temporary read locks. Concurrent refresh may consume more disk and CPU resources during operation.

## Example

Pseudocode for refresh logic:

```python
def refresh_materialized_views():
  for mv in MATERIALIZED_VIEWS:
    try:
      execute_sql(f"REFRESH MATERIALIZED VIEW CONCURRENTLY {mv}")
    except ConcurrentRefreshError:
      execute_sql(f"REFRESH MATERIALIZED VIEW {mv}")
```

## Relationship to Other Concepts

- **[[PostgreSQL Materialized Views for Dashboard Optimization]]** — Concurrent refresh is a key technique enabling efficient matview updates without downtime.

## Practical Applications

Essential for production database environments where dashboards or reports must remain available during data refreshes. Enables continuous data availability and reduces impact on user queries during maintenance windows.

## Sources

- [[Copilot Session Checkpoint: Dashboard Matviews Implementation In Progress]] — primary source for this concept
