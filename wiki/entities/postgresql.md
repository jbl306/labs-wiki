---
title: "PostgreSQL"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "bda088556b526d765495b4eb44e9e07a7a9a83c274765d5b943d5a42aa248499"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-rankings-page-and-performance-optimization-8063e05f.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-props-db-query-and-chart-refinement-402d70da.md
quality_score: 76
concepts:
  - postgresql
related:
  - "[[Handling PostgreSQL NUMERIC Type in Node.js with pg Library]]"
  - "[[Replacing FastAPI Proxy with Direct PostgreSQL Query for Historical Props Data]]"
  - "[[Copilot Session Checkpoint: Props DB Query and Chart Refinement]]"
  - "[[NBA ML Engine]]"
  - "[[Express.js]]"
  - "[[FastAPI]]"
tier: hot
tags: [database, sql, data-storage]
---

# PostgreSQL

## Overview

PostgreSQL is a powerful, open-source object-relational database system. It stores all the NBA ML Engine's structured data including players, game logs, injuries, predictions, and prop lines. The BFF uses the `pg` Node.js library to query PostgreSQL directly for most data, replacing some FastAPI endpoints to improve performance and data availability.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

PostgreSQL is the primary data store for the NBA ML Engine, and direct querying from the BFF enables richer data access and filtering capabilities such as date filtering for props data.

## Associated Concepts

- **[[Handling PostgreSQL NUMERIC Type in Node.js with pg Library]]** — PostgreSQL NUMERIC type handling in BFF
- **[[Replacing FastAPI Proxy with Direct PostgreSQL Query for Historical Props Data]]** — Direct SQL queries against PostgreSQL

## Related Entities

- **[[NBA ML Engine]]** — co-mentioned in source (Tool)
- **[[Express.js]]** — co-mentioned in source (Tool)
- **[[FastAPI]]** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Props DB Query and Chart Refinement]] — where this entity was mentioned
- [[Copilot Session Checkpoint: Rankings Page and Performance Optimization]] — additional source
