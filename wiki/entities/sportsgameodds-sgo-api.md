---
title: "SportsGameOdds (SGO) API"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "c4cd8c8e81648711e1dbceea098279d1120878d54e1d8ae18c7015937060ae6d"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sgo-data-extraction-fix-and-quality-audit-76644cc8.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-odds-api-quota-optimization-sgo-investigation-f4c98efb.md
quality_score: 100
concepts:
  - sportsgameodds-sgo-api
related:
  - "[[SportsGameOdds (SGO) API Data Extraction Challenges]]"
  - "[[Copilot Session Checkpoint: Odds API Quota Optimization, SGO Investigation]]"
  - "[[Odds API]]"
tier: hot
tags: [api, sports-betting, data-extraction]
---

# SportsGameOdds (SGO) API

## Overview

The SportsGameOdds (SGO) API is a sports odds data provider API that returns detailed bookmaker odds including player props for all stats. It provides a rich data set with hundreds of odds entries per game. However, free tier API keys limit access to full bookmaker data, and the API response structure may change, complicating data extraction. The API key used is valid but returns warnings about missing bookmaker odds, indicating a need for an upgraded key for full access.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

Used alongside the Odds API to enrich player prop data in the ML pipeline. Current investigation focuses on why the fetcher extracts sparse data despite the API returning rich responses.

## Associated Concepts

- **[[SportsGameOdds (SGO) API Data Extraction Challenges]]** — Primary API subject of extraction challenges

## Related Entities

- **[[Odds API]]** — co-mentioned in source (Tool)
- **MLflow** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Odds API Quota Optimization, SGO Investigation]] — where this entity was mentioned
- [[Copilot Session Checkpoint: SGO Data Extraction Fix and Quality Audit]] — additional source
