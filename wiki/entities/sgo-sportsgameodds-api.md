---
title: "SGO (SportsGameOdds) API"
type: entity
created: 2026-04-19
last_verified: 2026-04-22
source_hash: "d9cea72e0198e7d3d24aa2f2351ac17ebe1246338b49cf42f47130ad7dc14949"
sources:
  - raw/2026-04-19-copilot-session-sprint-60-pts-feature-planning-abd21993.md
quality_score: 60
concepts:
  - sgo-sportsgameodds-api
related:
  - "[[PTS Feature Engineering With Opponent Defensive Rating Rolling Window]]"
  - "[[Copilot Session Checkpoint: Sprint 60 PTS Feature Planning]]"
  - "[[NBA ML Engine]]"
tier: hot
tags: [nba-ml, api, prop-line, data-quality]
---

# SGO (SportsGameOdds) API

## Overview

The SGO API provides prop-line and odds data for NBA games, used in the NBA ML Engine for feature engineering and market expansion. Data quality gates and API quota constraints are critical operational considerations.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Dataset |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

SGO API is referenced as a data source for prop-line backfill and quality gating. Its quota exhaustion blocks some Sprint 60 items, highlighting the importance of API budgeting and data freshness in ML workflows.

## Associated Concepts

- **[[PTS Feature Engineering With Opponent Defensive Rating Rolling Window]]** — SGO data is used for prop-line features and quality gating.

## Related Entities

- **[[NBA ML Engine]]** — co-mentioned in source (Model)

## Sources

- [[Copilot Session Checkpoint: Sprint 60 PTS Feature Planning]] — where this entity was mentioned
