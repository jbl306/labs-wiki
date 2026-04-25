---
title: "Standard Over/Under vs Milestone Prop Market Identity"
type: concept
created: 2026-04-25
last_verified: 2026-04-25
source_hash: "4d5a0e3b43a55119a052f549e5b4c61f5c03a47374bde5fa8b813cb7f181fa31"
sources:
  - raw/2026-04-25-copilot-session-direct-sportsbook-sources-855a32a8.md
related:
  - "[[Browser-Backed Sportsbook Truth Validation]]"
  - "[[Primary Prop Line Selection to Avoid Alternate Line Contamination]]"
  - "[[One-Sided Prop Line Filtering in Sports Betting Data]]"
  - "[[Heuristic Prop-Line Selection vs Direct Sportsbook Validation]]"
tier: hot
tags: [sports-betting, market-taxonomy, prop-lines, sportsbook-data, data-validation]
---

# Standard Over/Under vs Milestone Prop Market Identity

## Overview

Standard over/under and milestone prop markets often describe the same player and stat while representing different betting questions. The durable lesson from this checkpoint is that a sportsbook line like **0.5 steals O/U** and a UI label like **2+ steals** are not competing answers to the same prompt; they are different market families that must be identified before any ingest pipeline can claim it has captured the "true" line.

This concept matters because many sports-data failures are not parsing failures at all. They are taxonomy failures: the system successfully extracted a real market, but it extracted the wrong class of market for the dashboard contract.

## How It Works

The concept begins with a simple sportsbook reality: books publish several prop families for the same athlete-stat combination. A player can simultaneously have a standard line such as **Steals O/U 0.5**, an alternate ladder like **1+ steals**, **2+ steals**, **3+ steals**, and sometimes special bet-builder or quick-bet variants. These are all legitimate sportsbook products, but they are not interchangeable. A dashboard or model that intends to show the canonical current over/under line must explicitly choose the standard market family and reject the rest.

The Josh Hart example in the checkpoint makes the ambiguity concrete. The user saw **2+** on DraftKings and understandably interpreted that as the relevant steals line. Meanwhile, the dashboard carried `SGO_DK 0.5`. If one assumes there can only be one "real" DraftKings steals market, the mismatch looks like proof of a bad ingestion row. But the browser-backed audit showed something subtler: DraftKings' standard market for Josh Hart was indeed **Steals O/U 0.5**, while the observed **2+** belonged to a milestone ladder family. The conflict was semantic, not merely numeric.

From an implementation perspective, market identity is best defined through structure rather than through fuzzy name matching. The checkpoint provides a strong FanDuel rule set for standard O/U selection:

- `bettingType=MOVING_HANDICAP`
- `marketStatus=OPEN`
- exactly two active runners
- runner names ending with `Over` / `Under`
- both sides share the same handicap

Those conditions are valuable because they describe the market's shape, not just its marketing copy. A line called "Josh Hart - Steals" becomes trustworthy only when it also behaves like a two-sided moving-handicap market.

DraftKings expresses the same concept through a different taxonomy. The session discovered that `Player Defense` -> `Steals O/U` corresponded to `subcategoryId=13508`, with `marketType.name="Steals O/U"`. The captured Josh Hart market then had two selections, `Over` and `Under`, each on the same `points=0.5`. In addition, the selections included tags such as `MainPointLine`, which is a strong signal that the market is the primary book line rather than a novelty or derivative market.

This structural approach is why milestone markets must be rejected even when they mention the same player and stat. A phrase like **To Record 2+ Steals** is not just an alternate number on the same curve. It changes the contract:

- it often behaves like a one-sided threshold market rather than a symmetric two-way handicap
- it may not provide a paired under side in the same surface
- it is designed as a ladder product, not as the canonical line around which prediction error and edge are usually measured

That difference matters downstream. A model edge, a hit-rate computation, or a dashboard "best line" view assumes the line represents a primary market close to the bookmaker's central estimate. Milestone ladders are deliberately farther from that center and can dramatically change implied probabilities. Treating them as standard lines would corrupt confidence, P&L interpretation, and comparisons across sportsbooks.

In practice, the identity problem should be solved as early as possible in the ingestion chain. A useful pattern is:

1. enumerate all candidate markets for a player/stat
2. classify each market by structure and explicit sportsbook fields
3. keep only standard O/U candidates for canonical dashboard use
4. apply secondary heuristics, such as closest-to-prediction ranking, only *after* taxonomy filtering

This sequencing is crucial. Existing cleanup logic like [[Primary Prop Line Selection to Avoid Alternate Line Contamination]] is still valuable, but it operates best after the candidate set has already been restricted to the correct market family. Otherwise, the heuristic may rank a milestone or alternate market highly simply because its number happens to sit near the model prediction.

The checkpoint also shows that the required markers can vary by sportsbook, so the identity layer must be source-aware. FanDuel offers useful fields like `bettingType` and runner structure. DraftKings exposed `marketType.name`, `subcategoryId`, explicit over/under labels, and `MainPointLine` tagging. A robust system therefore should not look for one universal field across all books; it should express a shared semantic contract through sportsbook-specific predicates.

## Key Properties

- **Two-sided symmetry:** Standard markets expose paired `Over` and `Under` outcomes on the same handicap or points value.
- **Source-aware taxonomy:** The identifying fields differ by sportsbook, such as FanDuel `MOVING_HANDICAP` versus DraftKings `Steals O/U` plus `MainPointLine`.
- **Canonical-line suitability:** Standard O/U markets are appropriate for dashboards, edge calculations, and cross-book comparison; milestone ladders are usually not.
- **Ordering rule:** Market-family classification should happen before closest-line or dedup heuristics.

## Limitations

Market taxonomy can shift as sportsbooks rename tabs, add new tags, or change response schemas, so filters need periodic re-validation. Some books may also expose specialized markets that look superficially two-sided but still do not represent the canonical line a dashboard intends to show. Finally, direct-book truth at one timestamp does not guarantee the same IDs or categories remain stable later in the season.

## Examples

```python
def is_standard_fanduel_ou(market):
    runners = [r for r in market["runners"] if r["runnerStatus"] == "ACTIVE"]
    return (
        market["bettingType"] == "MOVING_HANDICAP"
        and market["marketStatus"] == "OPEN"
        and len(runners) == 2
        and runners[0]["handicap"] == runners[1]["handicap"]
        and runners[0]["runnerName"].endswith("Over")
        and runners[1]["runnerName"].endswith("Under")
    )
```

## Practical Applications

This concept is central to sportsbook-ingestion pipelines, current-props dashboards, and audit tooling for projects like the [[NBA ML Engine]]. It is the difference between saying "we extracted a real sportsbook market" and saying "we extracted the correct canonical market for user-facing over/under analysis."

## Related Concepts

- **[[Browser-Backed Sportsbook Truth Validation]]**: Supplies the direct-book evidence needed to prove which market family the sportsbook is actually showing.
- **[[Primary Prop Line Selection to Avoid Alternate Line Contamination]]**: Works best after taxonomy filters have removed milestone and other non-canonical markets.
- **[[One-Sided Prop Line Filtering in Sports Betting Data]]**: Covers one structural symptom often associated with non-standard prop families.

## Sources

- [[Copilot Session Checkpoint: Direct Sportsbook Sources]] — provides the FanDuel and DraftKings examples that distinguish standard O/U from milestone `N+` markets

