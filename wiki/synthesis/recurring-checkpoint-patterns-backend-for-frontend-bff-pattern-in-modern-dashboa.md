---
title: "Recurring checkpoint patterns: Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture, Handling PostgreSQL NUMERIC Type in Node.js with pg Library, Dashboard Chart Strategy and Data-Driven Refinement"
type: synthesis
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "synthesis-generated"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-props-db-query-and-chart-refinement-402d70da.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-rankings-page-and-performance-optimization-8063e05f.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-react-dashboard-scaffold-and-pages-built-2fe5dac8.md
concepts:
  - handling-postgresql-numeric-type-in-nodejs-with-pg-library
  - backend-for-frontend-bff-pattern-in-modern-dashboard-architecture
  - dashboard-chart-strategy-and-data-driven-refinement
  - replacing-fastapi-proxy-with-direct-postgresql-query-for-historical-props-data
related:
  - "[[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]]"
  - "[[Replacing FastAPI Proxy with Direct PostgreSQL Query for Historical Props Data]]"
  - "[[Handling PostgreSQL NUMERIC Type in Node.js with pg Library]]"
  - "[[Copilot Session Checkpoint: Rankings Page and Performance Optimization]]"
  - "[[Copilot Session Checkpoint: React Dashboard Scaffold and Pages Built]]"
  - "[[Copilot Session Checkpoint: Props DB Query and Chart Refinement]]"
  - "[[Dashboard Chart Strategy and Data-Driven Refinement]]"
tier: hot
checkpoint_cluster_community: 11
checkpoint_cluster_checkpoint_count: 3
checkpoint_cluster_signature: 8fdfc351df90067b
tags: [agents, checkpoint, checkpoint-synthesis, copilot-session, dashboard, durable-knowledge, fileback, homelab, nba-ml-engine]
quality_score: 75
---

# Recurring checkpoint patterns: Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture, Handling PostgreSQL NUMERIC Type in Node.js with pg Library, Dashboard Chart Strategy and Data-Driven Refinement

## Question

What recurring decisions, fixes, and durable patterns appear across the 3 session checkpoints in this cluster, especially around Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture, Handling PostgreSQL NUMERIC Type in Node.js with pg Library, Dashboard Chart Strategy and Data-Driven Refinement?

## Summary

Across 3 dashboard-rebuild checkpoints the recurring decision is to **collapse the FastAPI proxy into an Express BFF that talks directly to PostgreSQL**, with a `numericRow()` post-processor for NUMERIC→Number coercion and an iterative chart-pruning loop guided by backtest data. The thread: every bug here was caused by a layer doing too little (FastAPI proxy with a today-only filter) or too much (driver returning NUMERICs as strings); the BFF is where those failures get owned and resolved.

## Comparison

| Dimension | [[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]] | [[Handling PostgreSQL NUMERIC Type in Node.js with pg Library]] | [[Dashboard Chart Strategy and Data-Driven Refinement]] | [[Replacing FastAPI Proxy with Direct PostgreSQL Query for Historical Props Data]] |
|-----------|---------------------||---------------------||---------------------||---------------------|
| Layer it changes | Whole API surface: Express BFF in front of FastAPI + Postgres; direct DB for hot paths. | Server post-processor: numericRow() walks rows and parseFloat()s known numeric fields. | UI: drop 6 low-value charts, add 4 high-value ones (Edge Histogram, Hit Rate by Edge Size, etc.). | Specific endpoint: /api/props moves off FastAPI's today-only proxy onto a date-filtered SQL query in the BFF. |
| Bug it fixes | Frontend tightly coupled to FastAPI's data shapes and lifecycle; latency from chained backend calls. | `.toFixed()` on strings → frontend crash. | User attention scattered across redundant or low-signal charts. | Props page empty on days without games; no historical access. |
| Coupling implication | BFF now owns the schema-shape contract; needs versioning discipline. | Helper must be applied at every BFF endpoint that returns NUMERIC—missed call = silent regression. | Chart roster is a product decision; backtest data is the source of truth for inclusion. | Date picker added to PropsPage; API now returns both data and available_dates. |
| Where the logic lives now | Express server with mixed proxy + direct-query handlers. | BFF utility module reused across endpoints. | React components informed by backtest insights (larger predicted edges → higher hit rates). | Direct SQL with `WHERE game_date = $1` and a `SELECT DISTINCT game_date` for the date list. |

## Analysis

The dashboard rebuild collapses a multi-layer stack (React → FastAPI → Postgres) into a leaner one (React → Express BFF → Postgres) for hot paths, while preserving FastAPI proxy for endpoints that don't yet justify direct-query treatment. Every bug in this cluster is what happens when one of those layers either doesn't know about a precondition (FastAPI's today-only filter) or surfaces an implementation detail (pg's NUMERIC-as-string).

The BFF pattern is the unifying decision. By owning data normalization in one place (Express), the team can fix the NUMERIC bug once, change a query for date filtering once, and shape the response to match the React TypeScript interfaces without round-tripping through FastAPI's Pydantic models. The cost is real: the BFF now has duplicated query logic that has to track schema changes, and the team has to be disciplined about what stays proxied vs. what becomes direct-query.

The NUMERIC fix is a textbook leaky-abstraction story. The pg library returns PostgreSQL NUMERIC as strings to preserve precision (a defensible default), but the frontend calls `.toFixed()` and crashes. The `numericRow()` helper coerces at the BFF boundary, but the dependency on every endpoint remembering to call it is the new failure mode—a missed call ships a string to the frontend and the bug looks identical to the original. The Express BFF needed a convention here, and the checkpoints document it being applied 'to all DB query results involving ROUND() or NUMERIC columns'.

The Props endpoint replacement is the cleanest argument for the BFF over the proxy. The original FastAPI `/prop-edges` returned today only—on no-game days the page was empty, with no path to history. The BFF endpoint adds a date parameter, returns the available-dates list alongside the data, and lets the React PropsPage ship a date picker. None of those changes were possible inside the proxy because the proxy didn't know about the underlying query.

Chart refinement is the product layer's version of the same discipline. Backtest data identified that larger predicted edges have higher hit rates—an insight worth a dedicated Hit-Rate-by-Edge-Size chart—while Prop Volume and Injury Status Breakdown were dropped for low signal. The pattern is data-driven pruning, and the chart roster is a maintained artifact, not a one-time scaffold.

## Key Insights

1. **The BFF pattern wins here specifically because it gives the team a single place to own response shape, type coercion, and data sourcing—decisions that would otherwise drift across FastAPI handlers and React components.** — supported by [[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]], [[Replacing FastAPI Proxy with Direct PostgreSQL Query for Historical Props Data]]
2. **numericRow() is a per-endpoint convention not a global middleware—because the pg library returns NUMERIC as strings for good reasons (precision), and only the BFF knows which columns the frontend will treat as numbers.** — supported by [[Handling PostgreSQL NUMERIC Type in Node.js with pg Library]]
3. **Chart strategy is treated as a product artifact: backtest insights gate inclusion, low-signal charts are removed, and the roster is maintained—dashboards that don't do this drift toward chart-clutter.** — supported by [[Dashboard Chart Strategy and Data-Driven Refinement]]

## Open Questions

- Should NUMERIC coercion move from a per-endpoint helper to a typed query layer (e.g. a small ORM or a `pg-types` global override) to eliminate the missed-call regression risk?
- What's the cutoff for promoting a FastAPI-proxied endpoint to a direct BFF query—latency? frontend pain? both?
- Is the chart-pruning loop ever in tension with cross-page consistency (e.g. removing a chart from PropsPage that operators expect to see on RankingsPage)?

## Sources

- [[Copilot Session Checkpoint: Props DB Query and Chart Refinement]]
- [[Copilot Session Checkpoint: Rankings Page and Performance Optimization]]
- [[Copilot Session Checkpoint: React Dashboard Scaffold and Pages Built]]
