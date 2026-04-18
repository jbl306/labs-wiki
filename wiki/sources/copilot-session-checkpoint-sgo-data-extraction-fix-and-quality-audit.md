---
title: "Copilot Session Checkpoint: SGO Data Extraction Fix and Quality Audit"
type: source
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "f5369b2de503515b0170a7d6c7a6ed15870125c0336cf70152cfa7db68adcca2"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sgo-data-extraction-fix-and-quality-audit-76644cc8.md
quality_score: 100
concepts:
  - sportsgameodds-sgo-api-data-extraction-challenges-and-fixes
related:
  - "[[SportsGameOdds (SGO) API]]"
  - "[[Durable Copilot Session Checkpoint]]"
tier: hot
tags: [data-quality, checkpoint, copilot-session, dashboard, api-integration, homelab, sports-data, durable-knowledge, nba-ml, fileback]
---

# Copilot Session Checkpoint: SGO Data Extraction Fix and Quality Audit

## Summary

This session checkpoint documents a detailed investigation and iterative fixes applied to the SportsGameOdds (SGO) API data extraction process within an NBA ML prediction platform. The main issues addressed include sparse data due to filtering of valid lines marked unavailable, missing under-side odds data, and contamination by alternate betting lines with extreme odds values. The fixes involved refining extraction filters, adding fallback logic, and implementing data quality guards, followed by audits and redeployment.

## Key Points

- Initial sparse data issue caused by filtering out 'available=false' bookmaker odds which were actually valid.
- SGO API only provides per-bookmaker odds on the 'over' side; the 'under' side requires fallback to consensus odds.
- Extreme odds values and alternate line contamination required additional filtering and capping mechanisms.
- Cross-source data quality audits confirmed high accuracy but revealed edge cases needing correction.
- Final extraction logic prefers 'available=true' lines and uses 'available=false' only as fallback to improve data consistency.

## Concepts Extracted

- **SportsGameOdds (SGO) API Data Extraction Challenges and Fixes** — The SportsGameOdds (SGO) API provides sports betting odds data but presents unique challenges for data extraction due to its data structure and filtering flags. This concept covers the root causes of sparse data extraction, the nature of the 'available' flag, the asymmetry of odds data between 'over' and 'under' sides, and the iterative fixes applied to improve data quality and completeness in an NBA ML prediction platform.

## Entities Mentioned

- **[[SportsGameOdds (SGO) API]]** — The SportsGameOdds (SGO) API is a sports betting odds data provider used in the NBA ML prediction platform. It provides odds data with a unique structure including consensus odds and per-bookmaker odds, but has quirks such as the `available` flag and asymmetrical data availability between 'over' and 'under' sides. It is a critical data source especially when other APIs like OddsAPI hit quota limits.
- **[[Durable Copilot Session Checkpoint]]** — A durable checkpoint mechanism used in Copilot CLI sessions to save and promote session state snapshots for later ingestion into the labs-wiki knowledge base. This checkpoint represents a snapshot of a session focused on fixing SGO data extraction and auditing quality.

## Notable Quotes

> "92% of SGO odds marked `available=false` even though they have fresh, valid line data (updated same minute)." — Durable Session Summary
> "SGO `byBookmaker` typically only exists on the "over" side. The "under" side has consensus data only." — Technical Details
> "Consensus fallback now capped at ±999 (`_MAX_CONSENSUS_ODDS`)." — Durable Session Summary

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sgo-data-extraction-fix-and-quality-audit-76644cc8.md` |
| Type | note |
| Author | Unknown |
| Date | 2026-04-18T03:23:51.483387Z |
| URL | N/A |
