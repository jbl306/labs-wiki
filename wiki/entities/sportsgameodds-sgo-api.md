---
title: "SportsGameOdds (SGO) API"
type: entity
created: 2026-04-18
last_verified: 2026-04-25
source_hash: "c4cd8c8e81648711e1dbceea098279d1120878d54e1d8ae18c7015937060ae6d"
sources:
  - raw/2026-04-25-copilot-session-backtest-completion-props-investigation-ed8d6cc6.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sgo-data-extraction-fix-and-quality-audit-76644cc8.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-odds-api-quota-optimization-sgo-investigation-f4c98efb.md
quality_score: 73
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
| Type | Dataset |
| Created | Unknown |
| Creator | Unknown |
| URL | https://sportsdata.io |
| Status | Active |

## Relevance

Used alongside the Odds API to enrich player prop data in the ML pipeline. Later checkpoint evidence shows it remains a high-risk dependency for sportsbook truth: the provider can mix standard over/under props with alternate or game-prop markets, and mismatches between sportsbook UI, provider payload, and dashboard rows must be audited directly rather than assumed away.

## Associated Concepts

- **[[SportsGameOdds (SGO) API Data Extraction Challenges]]** — Primary API subject of extraction challenges
- **[[Primary Prop Line Selection to Avoid Alternate Line Contamination]]** — Describes one downstream heuristic used to cope with SGO alternate-line noise.
- **[[One-Sided Prop Line Filtering in Sports Betting Data]]** — Covers another defensive filter added because SGO can emit non-standard one-sided markets.

## Related Entities

- **[[Odds API]]** — co-mentioned in source (Tool)
- **MLflow** — co-mentioned in source (Tool)
- **[[NBA ML Engine]]** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Odds API Quota Optimization, SGO Investigation]] — where this entity was mentioned
- [[Copilot Session Checkpoint: SGO Data Extraction Fix and Quality Audit]] — additional source
- [[Copilot Session Checkpoint: Backtest Completion Props Investigation]] — preserves the later Josh Hart DK/FD mismatch investigation and validation plan
