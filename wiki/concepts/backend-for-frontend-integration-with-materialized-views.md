---
title: "Backend-For-Frontend (BFF) Integration with Materialized Views"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "775f812f7b3878f9c18195d90e9cda4785608659d21041c4a0edfdd122da8024"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-dashboard-matviews-implementation-in-progress-afa2957e.md
quality_score: 100
concepts:
  - backend-for-frontend-integration-with-materialized-views
related:
  - "[[PostgreSQL Materialized Views for Dashboard Optimization]]"
  - "[[Copilot Session Checkpoint: Dashboard Matviews Implementation In Progress]]"
tier: hot
tags: [backend-for-frontend, bff, materialized-views, dashboard, caching]
---

# Backend-For-Frontend (BFF) Integration with Materialized Views

## Overview

The Backend-For-Frontend (BFF) pattern provides a tailored backend service for frontend applications, optimizing data delivery and aggregation. Integrating materialized views into the BFF layer reduces query complexity and latency by serving precomputed data, improving dashboard responsiveness.

## How It Works

In this architecture, the frontend React UI communicates with a BFF implemented in Express.js, which in turn queries a FastAPI service and PostgreSQL database. The BFF previously executed complex, heavy queries involving multiple joins and CTEs on-demand, causing latency and load issues.

By defining materialized views that precompute these heavy aggregations, the BFF can replace complex queries with simple `SELECT * FROM matview` statements. This reduces query execution time and server CPU usage.

The BFF maintains an LRU cache with a configurable TTL (2-30 minutes) to serve frequent requests efficiently while ensuring data freshness between pipeline runs that refresh the matviews.

Post-processing logic such as computing profit and loss curves, confidence scoring, and Kelly criterion calculations remains in the BFF JavaScript code because these are stateless transformations that do not require database persistence.

Endpoints are incrementally updated to use matviews, starting with `/api/backtest`, followed by `/api/rankings`, `/api/dashboard`, and `/api/prop-hit-rate`. Some queries that require dynamic parameters or real-time data may still use fallback queries or partial matview data.

This integration pattern improves maintainability by centralizing heavy computations in the database layer and simplifying the BFF codebase, while preserving flexibility for dynamic computations.

## Key Properties

- **Query Simplification:** Replaces complex CTE/join queries with simple SELECTs from matviews.
- **Caching:** LRU cache with TTL in BFF balances performance and data freshness.
- **Incremental Integration:** Endpoints updated progressively to use matviews.
- **Stateless Post-Processing:** Complex transforms remain in BFF code for flexibility.

## Limitations

Matviews may not support all dynamic query parameters, requiring fallback queries. Cache TTL introduces potential staleness. Integration requires careful coordination between database schema, BFF code, and pipeline refresh schedules.

## Example

Example BFF endpoint replacement:

Before:
```typescript
const backtestData = await db.query(`
  WITH heavy_cte AS (...) 
  SELECT * FROM heavy_cte WHERE ...
`);
```

After:
```typescript
const backtestData = await db.query(`SELECT * FROM mv_backtest_summary`);
```

Cache usage example:
```typescript
const cachedData = cache.get('backtest');
if (cachedData) return cachedData;
const freshData = await db.query(...);
cache.set('backtest', freshData, ttl);
return freshData;
```

## Relationship to Other Concepts

- **[[PostgreSQL Materialized Views for Dashboard Optimization]]** — Matviews provide the precomputed data that the BFF queries.
- **LRU Cache** — Caching layer in BFF to optimize repeated queries.

## Practical Applications

Improves dashboard responsiveness and scalability in web applications by offloading heavy computations to the database layer and caching results in the BFF. Enables maintainable, modular architecture separating data aggregation and presentation logic.

## Sources

- [[Copilot Session Checkpoint: Dashboard Matviews Implementation In Progress]] — primary source for this concept
