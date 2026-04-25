---
title: "Copilot Session Checkpoint: Direct Sportsbook Sources"
type: source
created: '2026-04-25'
last_verified: '2026-04-25'
source_hash: 4d5a0e3b43a55119a052f549e5b4c61f5c03a47374bde5fa8b813cb7f181fa31
sources:
  - raw/2026-04-25-copilot-session-direct-sportsbook-sources-855a32a8.md
concepts:
  - browser-backed-sportsbook-truth-validation
  - standard-over-under-vs-milestone-prop-market-identity
  - primary-prop-line-selection-to-avoid-alternate-line-contamination
  - sportsgameodds-sgo-api-data-extraction-challenges
  - odds-api-quota-optimization
related:
  - "[[NBA ML Engine]]"
  - "[[FanDuel Sportsbook]]"
  - "[[DraftKings Sportsbook]]"
  - "[[Odds API]]"
  - "[[SportsGameOdds (SGO) API]]"
  - "[[Heuristic Prop-Line Selection vs Direct Sportsbook Validation]]"
tags: [copilot-session, checkpoint, nba-ml-engine, sportsbook-data, prop-lines, fanduel, draftkings, browser-validation]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 78
---

# Copilot Session Checkpoint: Direct Sportsbook Sources

## Summary

This checkpoint closes the open Josh Hart sportsbook-truth investigation by moving from suspicion about provider contamination to direct evidence from the books themselves. It documents which direct FanDuel and DraftKings surfaces actually work, why the old DraftKings public JSON path is no longer sufficient, and how browser-backed capture resolved the apparent contradiction between a DraftKings **2+** UI observation and a dashboard line of **0.5**.

It also upgrades the durable operating model for the [[NBA ML Engine]]: use direct sportsbook surfaces as validation-first adapters when live prop truth is in doubt, keep [[Odds API]] as the safest production baseline when quota is available, and continue treating [[SportsGameOdds (SGO) API]] as a potentially contaminated feed until market-identity filters are stronger.

## Key Points

- The investigation began because the user saw **Josh Hart steals 2+** on DraftKings while the live dashboard/API showed `SGO_DK stl=0.5` and `SGO_FD stl=1.5`, making sportsbook truth the central question rather than a simple parsing bug.
- [[Odds API]] was already known to return bookmaker-specific DraftKings/FanDuel props and remains the cleanest production-safe source, but the account quota was exhausted during this session.
- FanDuel direct JSON worked from the local environment on multiple state hosts (`nj`, `ny`, `pa`) using state-specific `sbapi.{state}.sportsbook.fanduel.com` APIs.
- The FanDuel discovery flow used `api/content-managed-page?page=CUSTOM&customPageId=nba` to enumerate NBA events, then `api/event-page?...&eventId=35517728&tab=player-defense` to inspect prop markets.
- The FanDuel standard steals market for Josh Hart was clearly identified as `marketId=734.165832700`, `marketType=PLAYER_E_TOTAL_STEALS`, `bettingType=MOVING_HANDICAP`, with **Over 1.5 +178 / Under 1.5 -245**.
- FanDuel also exposed milestone ladder markets such as **To Record 2+ Steals**, which the checkpoint explicitly marks as invalid for standard over/under ingestion.
- DraftKings' older `/sites/{SITE}/api/v5/eventgroups/42648?format=json` endpoints were blocked by Akamai `403 Access Denied` across plain HTTP, browser-like headers, `curl_cffi` Chrome impersonation, and FlareSolverr, showing that the issue was not a simple Cloudflare challenge.
- Browser-backed Chromium loading `https://sportsbook.draftkings.com/page/nba-player-props` revealed a newer working JSON family: `/sites/US-NJ-SB/api/sportscontent/controldata/standalone/leagueSubcategory/v1/markets`.
- Within DraftKings, `Player Defense` -> `Steals O/U` mapped to `subcategoryId=13508`; the Josh Hart market was `market id 328789167`, `marketType.name="Steals O/U"`, with **Over 0.5 -226 / Under 0.5 +168**.
- The durable conclusion is that the dashboard's DraftKings `0.5` line matched the book's standard O/U market at capture time, while the user's observed **2+** line belonged to a different milestone/ladder family rather than disproving the dashboard outright.
- Operationally, the source recommends direct `FD_WEB` and discovered `DK_WEB` adapters for truth validation, continued use of [[Odds API]] when credits exist, and continued quarantine/demotion of [[SportsGameOdds (SGO) API]] until validation and market-type filters are hardened.

## Key Concepts

- [[Browser-Backed Sportsbook Truth Validation]]
- [[Standard Over/Under vs Milestone Prop Market Identity]]
- [[Primary Prop Line Selection to Avoid Alternate Line Contamination]]
- [[SportsGameOdds (SGO) API Data Extraction Challenges]]
- [[Odds API Quota Optimization]]

## Related Entities

- **[[NBA ML Engine]]** — The production system whose current-slate prop accuracy depends on knowing when sportsbook truth has diverged from provider heuristics.
- **[[FanDuel Sportsbook]]** — The direct sportsbook source whose public JSON APIs worked immediately and exposed both valid O/U and misleading milestone markets.
- **[[DraftKings Sportsbook]]** — The sportsbook whose legacy public JSON path failed, but whose browser-discovered `sportscontent` endpoint yielded the decisive Josh Hart evidence.
- **[[Odds API]]** — The safest third-party aggregator baseline when quota is available, even though it could not settle this session's question because credits were exhausted.
- **[[SportsGameOdds (SGO) API]]** — The provider whose mixed market identities made direct sportsbook verification necessary in the first place.

