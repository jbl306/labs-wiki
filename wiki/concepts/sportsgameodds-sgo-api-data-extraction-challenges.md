---
title: "SportsGameOdds (SGO) API Data Extraction Challenges"
type: concept
created: 2026-04-18
last_verified: 2026-04-25
source_hash: "c4cd8c8e81648711e1dbceea098279d1120878d54e1d8ae18c7015937060ae6d"
sources:
  - raw/2026-04-25-copilot-session-backtest-completion-props-investigation-ed8d6cc6.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sgo-data-extraction-fix-and-quality-audit-76644cc8.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-odds-api-quota-optimization-sgo-investigation-f4c98efb.md
quality_score: 92
concepts:
  - sportsgameodds-sgo-api-data-extraction-challenges
related:
  - "[[Odds API Quota Optimization]]"
  - "[[Copilot Session Checkpoint: Odds API Quota Optimization, SGO Investigation]]"
tier: hot
tags: [sports-data, api, data-extraction, parsing, sportsbetting]
---

# SportsGameOdds (SGO) API Data Extraction Challenges

## Overview

The SportsGameOdds (SGO) API provides rich bookmaker odds data for sports games, including player props. However, extracting complete and accurate data from the API can be challenging due to quota restrictions, data structure changes, parsing issues, and market-identity ambiguity between standard over/under props and alternate or game-prop variants. Understanding and debugging these challenges is crucial for reliable data ingestion.

## How It Works

The SGO API returns a large number of odds entries per game (~618), covering all player stats. The data structure includes a `bookOdds` field that contains bookmaker-specific odds, with an `oddID` formatted as `{statID}-{playerEntity}-{period}-{betType}-{side}`.

Challenges encountered include:

- **Quota Limitations:** The free API tier returns a notice that 11,797 bookmaker odds are missing and suggests upgrading the API key to access all data.
- **Sparse Data Extraction:** Despite the API returning rich data, the fetcher extracts very sparse data (e.g., only 1 PRA line for April 12).
- **Data Structure Changes:** The `bookOdds` field may have changed from a dictionary to a string, causing attribute errors during parsing.
- **Bookmaker Filtering:** The function `_selected_sportsgameodds_bookmakers()` may be filtering bookmakers too aggressively, excluding valid data.
- **Market-Type Ambiguity:** DraftKings and FanDuel payloads can contain both normal O/U props and alternate or game-prop markets, so a row that looks syntactically valid may still be the wrong market for dashboard use.
- **Truth-Validation Gap:** A later checkpoint showed that API/dashboard rows for Josh Hart steals (`SGO_DK line=0.5`, `SGO_FD line=1.5`) could not be trusted without comparing sportsbook UI, raw provider payload, `prop_lines`, `prop_line_snapshots`, and `/api/props` together.

The extraction process involves:

1. Fetching paginated data from the SGO API.
2. Parsing the `bookOdds` field to extract odds per bookmaker.
3. Mapping odds to player stats and game periods.
4. Filtering bookmakers based on configured preferences.
5. Selecting or deduplicating rows for downstream use, often with heuristics such as "closest line to prediction."

Debugging requires inspecting raw API responses, adjusting parsing logic to handle data type changes, and verifying filtering criteria. The later checkpoint adds another requirement: preserve or inspect enough market identity to distinguish primary O/U markets from alternate or one-sided bets, because downstream heuristics can accidentally bless the wrong row. Manual testing with direct API calls, sportsbook UI inspection, DB comparison, and log inspection helps identify skipped, stale, or mismatched lines.

## Key Properties

- **API Key:** Valid key with limited quota; free tier restricts full bookmaker odds access.
- **Odds Entries Per Game:** ~618 odds entries including player props.
- **Data Structure:** `bookOdds` field contains bookmaker odds; may be dict or string.
- **OddID Format:** `{statID}-{playerEntity}-{period}-{betType}-{side}`
- **Validation chain:** Reliable audits often require four-way comparison across sportsbook UI, raw SGO payload, production DB tables, and dashboard/API outputs.

## Limitations

Free tier API keys limit access to full bookmaker odds, causing incomplete data extraction. Changes in API response structure (e.g., `bookOdds` field type) can break parsing logic. Aggressive filtering of bookmakers may exclude valid data. Even when extraction succeeds, missing market-type markers or stale provider rows can make the "best" parsed line diverge from the actual sportsbook UI, which impacts downstream analytics, dashboards, and trust.

## Example

Example oddID: `1234-5678-1-OVER-Home` representing statID 1234, player 5678, period 1, bet type OVER, home side.

Pseudocode for parsing `bookOdds`:

```python
book_odds = event['bookOdds']
if isinstance(book_odds, str):
    book_odds = json.loads(book_odds)
for bookmaker, odds_data in book_odds.items():
    if bookmaker in selected_bookmakers:
        process_odds(odds_data)
```

Manual test command:

```bash
docker exec nba-ml-api python main.py ingest --props
# Check logs for warnings about skipping or unmatched lines
```

## Relationship to Other Concepts

- **[[Odds API Quota Optimization]]** — Both concepts relate to external sports odds API usage and limitations.

## Practical Applications

This concept is critical for sports analytics platforms relying on third-party odds data. Correct extraction ensures accurate player prop lines for betting models. Understanding API limitations and data structure changes enables robust ingestion pipelines and informs decisions about API key upgrades or alternative data sources.

## Sources

- [[Copilot Session Checkpoint: Odds API Quota Optimization, SGO Investigation]] — primary source for this concept
- [[Copilot Session Checkpoint: SGO Data Extraction Fix and Quality Audit]] — additional source
- [[Copilot Session Checkpoint: Backtest Completion Props Investigation]] — adds the later DK/FD validation workflow and market-truth caveat
