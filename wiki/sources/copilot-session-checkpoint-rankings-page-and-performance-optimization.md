---
title: "Copilot Session Checkpoint: Rankings Page and Performance Optimization"
type: source
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "f073ae4fd7b3295570081cdf37f1d67fc5c9838cf1ce8f2aa7e1d9409b01f107"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-rankings-page-and-performance-optimization-8063e05f.md
quality_score: 100
concepts:
  - backend-for-frontend-pattern-in-dashboard-architecture
  - replacing-lateral-joins-with-regular-join-case-for-performance-optimization
  - server-side-in-memory-caching-with-ttl-for-api-performance
related:
  - "[[Replacing LATERAL Joins with Regular JOIN + CASE for Performance Optimization]]"
  - "[[Server-Side In-Memory Caching with TTL for API Performance]]"
  - "[[NBA ML Engine]]"
  - "[[Express.js]]"
  - "[[PostgreSQL]]"
tier: hot
tags: [nba, checkpoint, copilot-session, dashboard, performance-optimization, sql, homelab, durable-knowledge, agents, bff, caching, fileback, nba-ml-engine]
checkpoint_class: durable-architecture
retention_mode: retain
---

# Copilot Session Checkpoint: Rankings Page and Performance Optimization

## Summary

This session documents the development and optimization of a modern React + Node.js dashboard for an NBA ML Engine, replacing a previous Streamlit monolith. Key work included fixing the Props page, building a new Rankings page with seven betting-insight tabs, and significantly optimizing slow API endpoints by replacing costly LATERAL joins with regular JOINs and adding server-side caching.

## Key Points

- Built a React 19 + TypeScript SPA with Express BFF proxying to FastAPI and PostgreSQL for NBA ML Engine dashboard.
- Created a new Rankings page with seven tabs featuring various player and betting insights, resolving multiple database schema issues.
- Diagnosed severe performance bottlenecks caused by LATERAL joins and replaced them with regular JOIN + CASE queries, achieving up to 200x speedup.
- Implemented server-side in-memory caching with TTL to further improve API responsiveness.
- Partially rewritten backtest endpoint using CTE + UNION ALL approach, with remaining code updates pending.

## Concepts Extracted

- **Backend-For-Frontend (BFF) Pattern in Dashboard Architecture** — The Backend-For-Frontend (BFF) pattern is an architectural approach where a dedicated backend service acts as an intermediary between the frontend UI and multiple backend services or databases. This pattern simplifies frontend development by providing a tailored API that aggregates, transforms, and optimizes data for the UI's specific needs.
- **[[Replacing LATERAL Joins with Regular JOIN + CASE for Performance Optimization]]** — LATERAL joins in SQL allow a subquery to reference columns from preceding tables in the FROM clause, enabling correlated subqueries. However, they can be extremely slow on large datasets. Replacing LATERAL joins with regular JOINs combined with CASE expressions can drastically improve query performance by enabling better query planning and index usage.
- **[[Server-Side In-Memory Caching with TTL for API Performance]]** — Server-side in-memory caching stores the results of expensive API calls temporarily in memory with a time-to-live (TTL) expiration. This reduces repeated database queries for frequently requested data that changes infrequently, improving API responsiveness and reducing backend load.

## Entities Mentioned

- **[[NBA ML Engine]]** — An NBA machine learning engine that powers predictive analytics and betting insights. It includes a React + Node.js dashboard frontend, an Express BFF backend, a FastAPI service, and a PostgreSQL database. The engine processes player statistics, game logs, and betting data to generate rankings, streaks, model accuracy metrics, and other advanced analytics for NBA players.
- **[[Express.js]]** — Express.js is a minimal and flexible Node.js web application framework providing a robust set of features for building web and mobile applications. In this context, Express serves as the Backend-For-Frontend (BFF) server that proxies API requests, performs database queries, and implements caching and query optimizations for the NBA ML Engine dashboard.
- **[[PostgreSQL]]** — PostgreSQL is a powerful, open-source object-relational database system with a strong reputation for reliability, feature robustness, and performance. It stores the NBA ML Engine's core data including player stats, game logs, predictions, and prop lines. Complex SQL queries with joins and aggregations are used to generate analytics for the dashboard.

## Notable Quotes

> "LATERAL joins are catastrophically slow (16.8s for 22K predictions) — replace with regular JOIN + inline CASE for 200x speedup." — Durable Session Summary
> "Created indexes on player_id and player_date columns to support query performance." — Durable Session Summary
> "Server-side caching with TTL is essential for queries that don't change frequently." — Durable Session Summary

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-rankings-page-and-performance-optimization-8063e05f.md` |
| Type | note |
| Author | Unknown |
| Date | 2026-04-18T03:23:51.483387Z |
| URL | N/A |
