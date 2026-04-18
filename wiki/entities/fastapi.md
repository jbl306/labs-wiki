---
title: "FastAPI"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "bda088556b526d765495b4eb44e9e07a7a9a83c274765d5b943d5a42aa248499"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-react-dashboard-scaffold-and-pages-built-2fe5dac8.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-props-db-query-and-chart-refinement-402d70da.md
quality_score: 100
concepts:
  - fastapi
related:
  - "[[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]]"
  - "[[Replacing FastAPI Proxy with Direct PostgreSQL Query for Historical Props Data]]"
  - "[[Copilot Session Checkpoint: Props DB Query and Chart Refinement]]"
  - "[[NBA ML Engine]]"
  - "[[Express.js]]"
  - "[[PostgreSQL]]"
tier: hot
tags: [python, web-framework, api]
---

# FastAPI

## Overview

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. It serves as the backend for the NBA ML Engine, providing REST endpoints for model predictions, health data, and some props data. The BFF proxies some requests to FastAPI but is moving towards direct DB queries for better control.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

FastAPI provides backend services for the NBA ML Engine, but some endpoints like `/prop-edges` are being replaced by direct DB queries in the BFF for improved functionality.

## Associated Concepts

- **[[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]]** — BFF proxies some endpoints to FastAPI
- **[[Replacing FastAPI Proxy with Direct PostgreSQL Query for Historical Props Data]]** — FastAPI `/prop-edges` endpoint replaced

## Related Entities

- **[[NBA ML Engine]]** — co-mentioned in source (Tool)
- **[[Express.js]]** — co-mentioned in source (Tool)
- **[[PostgreSQL]]** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Props DB Query and Chart Refinement]] — where this entity was mentioned
- [[Copilot Session Checkpoint: React Dashboard Scaffold and Pages Built]] — additional source
