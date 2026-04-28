---
title: DraftKings Sportsbook
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
  - "[[FanDuel Sportsbook]]"
  - "[[NBA ML Engine]]"
  - "[[Odds API]]"
  - "[[SportsGameOdds (SGO) API]]"
  - "[[Browser-Backed Sportsbook Truth Validation]]"
tier: hot
tags: [draftkings, sportsbook, nba, prop-lines, sportsbook-data]
quality_score: 85
---

# DraftKings Sportsbook

## Overview

DraftKings Sportsbook is the bookmaker surface the checkpoint used to settle the Josh Hart steals dispute. It mattered because the production dashboard showed a DraftKings line of `0.5`, while the user reported seeing `2+` on the DraftKings UI; only the book's own rendered page and underlying network calls could determine whether the dashboard was wrong or whether multiple DraftKings market families were being conflated.

The session shows that DraftKings cannot be treated as a single stable public JSON source. The older `/api/v5/eventgroups/42648?format=json` endpoints were fully blocked by Akamai, even with browser-like headers, `curl_cffi` impersonation, and FlareSolverr. But the modern sportsbook web shell still exposed usable JSON once Chromium loaded the real page and revealed the newer `sportscontent/controldata` request family.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Sportsbook Platform |
| Created | Unknown |
| Creator | DraftKings |
| URL | https://sportsbook.draftkings.com/page/nba-player-props |
| Status | Active |

## Technical Interface

The decisive working endpoint family discovered in-browser was:

```text
https://sportsbook-nash.draftkings.com/sites/US-NJ-SB/api/sportscontent/controldata/standalone/leagueSubcategory/v1/markets
```

For the NBA player-props investigation, the relevant query filtered on `leagueId='42648'`, `subCategoryId='13508'`, `include=Events`, and `entity=events`. Within the UI, this corresponded to `Player Defense` -> `Steals O/U`.

The checkpoint also preserved the failed legacy path:

```text
/sites/{SITE}/api/v5/eventgroups/42648?format=json
```

That path consistently returned `403 text/html` with `server: AkamaiGHost`, making it a useful historical warning but not a reliable production adapter.

## Market Model and Evidence

The captured DraftKings market clarified the source of the user-visible mismatch. The sportsbook returned a standard two-sided market with:

- `eventId=34041275`
- `market id=328789167`
- `market name="Josh Hart Steals O/U"`
- `marketType.name="Steals O/U"`
- `subcategoryId=13508`
- `Over 0.5 -226`
- `Under 0.5 +168`

Those values matched the dashboard's DraftKings `0.5` line rather than the user's observed **2+** ladder market. The durable lesson is that DraftKings can publish multiple prop families for the same player/stat pair, and a UI observation is only meaningful once the exact market type has been identified.

## Relevance

For the [[NBA ML Engine]], DraftKings Sportsbook is the authoritative truth surface when a provider or heuristic result is disputed. The session's direct-book evidence did not merely validate one line; it established that browser-backed endpoint discovery is sometimes necessary because the sportsbook's accessible JSON surface has changed even when the rendered site still works.

## Related Concepts

- **[[Browser-Backed Sportsbook Truth Validation]]** — The process that exposed the usable DraftKings `sportscontent` endpoint after legacy public JSON failed.
- **[[Standard Over/Under vs Milestone Prop Market Identity]]** — Explains why `0.5 O/U` and `2+` can both appear on DraftKings without representing the same market.
- **[[Primary Prop Line Selection to Avoid Alternate Line Contamination]]** — Still useful for provider cleanup, but not enough to certify direct DraftKings truth by itself.

## Sources

- [[Copilot Session Checkpoint: Direct Sportsbook Sources]] — documents the working endpoint, failed legacy endpoint, and Josh Hart market evidence

