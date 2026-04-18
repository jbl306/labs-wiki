---
title: "Copilot Session Checkpoint: Props DB Query and Chart Refinement"
type: source
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "bda088556b526d765495b4eb44e9e07a7a9a83c274765d5b943d5a42aa248499"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-props-db-query-and-chart-refinement-402d70da.md
quality_score: 100
concepts:
  - backend-for-frontend-pattern-in-modern-dashboard-architecture
  - handling-postgresql-numeric-type-in-nodejs-pg-library
  - dashboard-chart-strategy-and-data-driven-refinement
  - replacing-fastapi-proxy-with-direct-postgresql-query-for-historical-props-data
related:
  - "[[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]]"
  - "[[Handling PostgreSQL NUMERIC Type in Node.js with pg Library]]"
  - "[[Dashboard Chart Strategy and Data-Driven Refinement]]"
  - "[[Replacing FastAPI Proxy with Direct PostgreSQL Query for Historical Props Data]]"
  - "[[NBA ML Engine]]"
  - "[[Express.js]]"
  - "[[FastAPI]]"
  - "[[PostgreSQL]]"
tier: hot
tags: [graph, checkpoint, copilot-session, dashboard, postgresql, express, homelab, backend-for-frontend, durable-knowledge, agents, data-visualization, fastapi, fileback, nba-ml-engine]
checkpoint_class: durable-architecture
retention_mode: retain
---

# Copilot Session Checkpoint: Props DB Query and Chart Refinement

## Summary

This document details a development checkpoint in rebuilding the NBA ML Engine dashboard from a monolithic Streamlit app to a modern React + Node.js SPA with an Express BFF querying PostgreSQL directly. It covers the architectural changes, bug fixes, API endpoint rewrites, and chart refinements focused on the Props page, including replacing a limited FastAPI proxy with a direct DB query supporting date filtering.

## Key Points

- Replaced Streamlit monolith with React 19 + TypeScript SPA and Express BFF proxying to FastAPI and PostgreSQL.
- Fixed multiple bugs including Express wildcard routing, ESM path resolution, pg NUMERIC string handling, and database URL parsing.
- Rewrote 11 API endpoints in BFF to query PostgreSQL directly, improving data availability and type consistency.
- Refined dashboard charts by dropping low-value and adding high-value visualizations based on backtest data insights.
- Props page data issue resolved by replacing FastAPI proxy endpoint with direct DB query supporting date filtering.

## Concepts Extracted

- **[[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]]** — The Backend-For-Frontend (BFF) pattern is a design approach where a dedicated backend service acts as an intermediary between frontend clients and multiple backend services or databases. This pattern is particularly useful in complex applications to tailor APIs specifically for frontend needs, improve performance, and encapsulate backend complexity.
- **[[Handling PostgreSQL NUMERIC Type in Node.js with pg Library]]** — PostgreSQL's NUMERIC type is used for exact numeric values but is returned by the `pg` Node.js library as strings by default. This can cause runtime errors in JavaScript when numeric operations are expected. Proper handling and conversion are necessary to maintain type safety and avoid frontend crashes.
- **[[Dashboard Chart Strategy and Data-Driven Refinement]]** — Effective dashboard design requires selecting and refining charts to maximize actionable insights while minimizing noise. This involves evaluating existing visualizations, dropping low-value charts, and adding high-value ones based on data analysis and user feedback.
- **[[Replacing FastAPI Proxy with Direct PostgreSQL Query for Historical Props Data]]** — The original FastAPI endpoint `/prop-edges` only returned data for the current day, causing the Props page to show no data on days without games. To provide comprehensive historical data and support date filtering, the endpoint was replaced with a direct PostgreSQL query within the BFF.

## Entities Mentioned

- **[[NBA ML Engine]]** — The NBA ML Engine is a machine learning platform focused on basketball analytics. It includes model training pipelines, data ingestion, and a dashboard for visualizing predictions, player statistics, injuries, and betting edges. The engine uses FastAPI for backend services, PostgreSQL for data storage, and is undergoing a dashboard redesign to a React + Node.js architecture.
- **[[Express.js]]** — Express.js is a minimal and flexible Node.js web application framework that provides a robust set of features for building web and mobile applications. In this project, Express is used to implement the Backend-For-Frontend (BFF) server that proxies some requests to FastAPI and directly queries PostgreSQL for others.
- **[[FastAPI]]** — FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. It serves as the backend for the NBA ML Engine, providing REST endpoints for model predictions, health data, and some props data. The BFF proxies some requests to FastAPI but is moving towards direct DB queries for better control.
- **[[PostgreSQL]]** — PostgreSQL is a powerful, open-source object-relational database system. It stores all the NBA ML Engine's structured data including players, game logs, injuries, predictions, and prop lines. The BFF uses the `pg` Node.js library to query PostgreSQL directly for most data, replacing some FastAPI endpoints to improve performance and data availability.

## Notable Quotes

> "Bigger predicted edges (10%+) hit at 53.5% vs 45.5% for tiny (0-2%) edges — model edge sizing is meaningful." — Durable Session Summary
> "FastAPI `/prop-edges` only returns TODAY's data. No games today = no props. Replaced with direct DB query." — Durable Session Summary

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-props-db-query-and-chart-refinement-402d70da.md` |
| Type | note |
| Author | Unknown |
| Date | 2026-04-18T03:23:51.483387Z |
| URL | N/A |
