---
title: "Odds API"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "c4cd8c8e81648711e1dbceea098279d1120878d54e1d8ae18c7015937060ae6d"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-pipeline-resilience-fixes-dashboard-metrics-inve-3ea0d6d8.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-odds-api-quota-optimization-sgo-investigation-f4c98efb.md
quality_score: 100
concepts:
  - odds-api
related:
  - "[[Odds API Quota Optimization]]"
  - "[[Copilot Session Checkpoint: Odds API Quota Optimization, SGO Investigation]]"
  - "[[SportsGameOdds (SGO) API]]"
tier: hot
tags: [api, sports-betting, quota]
---

# Odds API

## Overview

The Odds API is a third-party sports betting odds provider API used to fetch player prop lines and game odds. It enforces a monthly quota limit of 500 calls per API key, with quota resetting monthly at midnight UTC. The API supports fetching multiple markets per request, configurable by the client. Quota exhaustion results in HTTP 401 Unauthorized errors, impacting dependent systems.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

Central to the sports betting ML pipeline for providing real-time odds data. Quota management and efficient usage are critical to maintain data freshness and avoid service disruptions.

## Associated Concepts

- **[[Odds API Quota Optimization]]** — Primary API subject of quota optimization efforts

## Related Entities

- **[[SportsGameOdds (SGO) API]]** — co-mentioned in source (Tool)
- **MLflow** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Odds API Quota Optimization, SGO Investigation]] — where this entity was mentioned
- [[Copilot Session Checkpoint: Pipeline Resilience Fixes, Dashboard Metrics Investigation]] — additional source
