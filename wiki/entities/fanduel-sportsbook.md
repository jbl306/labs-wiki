---
title: FanDuel Sportsbook
type: entity
created: 2026-04-25
last_verified: 2026-04-25
source_hash: 4d5a0e3b43a55119a052f549e5b4c61f5c03a47374bde5fa8b813cb7f181fa31
sources:
  - raw/2026-04-25-copilot-session-direct-sportsbook-sources-855a32a8.md
concepts:
  - browser-backed-sportsbook-truth-validation
  - standard-over-under-vs-milestone-prop-market-identity
related:
  - "[[DraftKings Sportsbook]]"
  - "[[NBA ML Engine]]"
  - "[[Odds API]]"
  - "[[SportsGameOdds (SGO) API]]"
  - "[[Browser-Backed Sportsbook Truth Validation]]"
tier: hot
tags: [fanduel, sportsbook, nba, prop-lines, sportsbook-data]
---

# FanDuel Sportsbook

## Overview

FanDuel Sportsbook was the cleaner of the two direct-book sources in this checkpoint. Unlike DraftKings, its state-specific sportsbook APIs responded directly from the local environment, which let the session confirm both event discovery and player-prop retrieval without relying on reverse-engineered browser state or anti-bot workarounds.

That ease of access also exposed a subtle but important modeling problem: FanDuel returns both standard over/under markets and milestone ladder markets in nearby surfaces. Because both can mention the same player and stat, ingest code must identify the market family explicitly instead of assuming the first matching prop is the canonical line.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Sportsbook Platform |
| Created | Unknown |
| Creator | FanDuel |
| URL | https://sbapi.nj.sportsbook.fanduel.com/api/event-page |
| Status | Active |

## Technical Interface

The checkpoint preserved two direct FanDuel API patterns:

```text
GET https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?page=CUSTOM&customPageId=nba&pbHorizontal=false&timezone=America/New_York&_ak=FhMFpcPWXMeyZxOx
GET https://sbapi.nj.sportsbook.fanduel.com/api/event-page?_ak=FhMFpcPWXMeyZxOx&eventId=35517728&tab=player-defense&timezone=America/New_York
```

The same host pattern worked for multiple states (`nj`, `ny`, `pa`), which makes FanDuel a comparatively straightforward direct validation source. The checkpoint also recorded the working tab slugs for standard player props: `player-points`, `player-rebounds`, `player-assists`, `player-threes`, and `player-defense`.

## Market Model and Evidence

The FanDuel evidence chain clearly separated standard O/U from milestone markets. The standard Josh Hart steals market had:

- `marketId=734.165832700`
- `marketName="Josh Hart - Steals"`
- `marketType=PLAYER_E_TOTAL_STEALS`
- `bettingType=MOVING_HANDICAP`
- `marketStatus=OPEN`
- `Over 1.5 +178`
- `Under 1.5 -245`

The same source family also contained milestone markets such as **To Record 2+ Steals**, which the session marked as invalid for standard over/under ingestion. That makes FanDuel a strong example of why market identity must be checked even when the source is directly accessible.

## Relevance

For the [[NBA ML Engine]], FanDuel Sportsbook is both a validation target and a design reference for direct adapters. It demonstrates the desirable case: direct JSON works, event discovery is systematic, and standard-market filters can be expressed from explicit fields like `bettingType`, runner labels, and shared handicap values.

## Related Concepts

- **[[Browser-Backed Sportsbook Truth Validation]]** — FanDuel validated both directly and through Chromium, showing the simplest form of the truth-check workflow.
- **[[Standard Over/Under vs Milestone Prop Market Identity]]** — The checkpoint's FanDuel payloads provide the cleanest concrete example of how to reject `N+` milestone markets when the goal is standard O/U truth.
- **[[SportsGameOdds (SGO) API Data Extraction Challenges]]** — Highlights why direct book surfaces matter when aggregator payloads can mix or mislabel prop families.

## Sources

- [[Copilot Session Checkpoint: Direct Sportsbook Sources]] — documents the working `sbapi` endpoints, tab structure, and Josh Hart market example

