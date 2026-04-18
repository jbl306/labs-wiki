---
title: "Copilot Session Checkpoint: Odds API Quota Optimization, SGO Investigation"
type: source
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "c4cd8c8e81648711e1dbceea098279d1120878d54e1d8ae18c7015937060ae6d"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-odds-api-quota-optimization-sgo-investigation-f4c98efb.md
quality_score: 100
concepts:
  - odds-api-quota-optimization
  - cascading-pipeline-failure-diagnosis-and-resilience
  - sportsgameodds-sgo-api-data-extraction-challenges
related:
  - "[[Odds API Quota Optimization]]"
  - "[[Cascading Pipeline Failure Diagnosis and Resilience]]"
  - "[[SportsGameOdds (SGO) API Data Extraction Challenges]]"
  - "[[Odds API]]"
  - "[[SportsGameOdds (SGO) API]]"
tier: hot
tags: [api, checkpoint, copilot-session, dashboard, homelab, sports-betting, durable-knowledge, agents, quota-optimization, pipeline-resilience, data-extraction, fileback, nba-ml-engine]
---

# Copilot Session Checkpoint: Odds API Quota Optimization, SGO Investigation

## Summary

This session checkpoint documents the diagnosis and remediation of multiple cascading failures in a sports betting ML pipeline, including stale data due to missing ensemble models, MLflow service DNS failure, and Odds API quota exhaustion causing 401 errors. It details the investigation and implementation of quota optimizations that reduced API calls from approximately 1,530 to 300 per month, and ongoing investigation into sparse data returned by the SportsGameOdds (SGO) API despite it being functional.

## Key Points

- Cascading pipeline failures caused stale dashboard props and hit rate discrepancies.
- Odds API quota was exhausted due to double-fetching and inefficient chunking, leading to 401 Unauthorized errors.
- Quota optimizations included removing redundant fetches and increasing markets per request, reducing calls from ~1,530 to ~300 per month.
- SGO API returns rich odds data but the fetcher extracts very sparse data; investigation ongoing.
- Resilience improvements were made for model loading fallback and MLflow connectivity.

## Concepts Extracted

- **[[Odds API Quota Optimization]]** — Odds API quota optimization is the process of reducing the number of external API calls made to a sports betting odds provider to stay within a limited monthly quota. This is critical to prevent service disruptions due to quota exhaustion, which causes unauthorized errors and stale data in dependent systems.
- **[[Cascading Pipeline Failure Diagnosis and Resilience]]** — Cascading pipeline failure diagnosis involves identifying multiple interrelated failures in a data processing or ML pipeline that cause downstream issues such as stale data or incorrect metrics. Resilience techniques are implemented to prevent or mitigate such failures, ensuring continuous operation and data integrity.
- **[[SportsGameOdds (SGO) API Data Extraction Challenges]]** — The SportsGameOdds (SGO) API provides rich bookmaker odds data for sports games, including player props. However, extracting complete and accurate data from the API can be challenging due to quota restrictions, data structure changes, and parsing issues. Understanding and debugging these challenges is crucial for reliable data ingestion.

## Entities Mentioned

- **[[Odds API]]** — The Odds API is a third-party sports betting odds provider API used to fetch player prop lines and game odds. It enforces a monthly quota limit of 500 calls per API key, with quota resetting monthly at midnight UTC. The API supports fetching multiple markets per request, configurable by the client. Quota exhaustion results in HTTP 401 Unauthorized errors, impacting dependent systems.
- **[[SportsGameOdds (SGO) API]]** — The SportsGameOdds (SGO) API is a sports odds data provider API that returns detailed bookmaker odds including player props for all stats. It provides a rich data set with hundreds of odds entries per game. However, free tier API keys limit access to full bookmaker data, and the API response structure may change, complicating data extraction. The API key used is valid but returns warnings about missing bookmaker odds, indicating a need for an upgraded key for full access.
- **MLflow** — MLflow is an open-source platform for managing the ML lifecycle, including experiment tracking, model packaging, and deployment. In this context, MLflow is used to track training runs and store ensemble model artifacts. A DNS resolution failure caused the MLflow container to restart, leading to retraining failures and missing ensemble models. Resilience improvements include connectivity checks and fallback to local file tracking to maintain pipeline continuity.

## Notable Quotes

> "Implemented quota optimizations reducing usage from ~1,530 to ~300 calls/month." — Copilot Session Checkpoint
> "SGO returns ~618 odds per game with player props for all stats but fetcher returns very sparse data." — Copilot Session Checkpoint

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-odds-api-quota-optimization-sgo-investigation-f4c98efb.md` |
| Type | note |
| Author | Unknown |
| Date | 2026-04-18T03:23:51.483387Z |
| URL | N/A |
