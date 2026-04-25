---
title: "Source-Priority Canonical Prop Ingestion"
type: concept
created: 2026-04-25
last_verified: 2026-04-25
source_hash: "bb9e0e187a674b361745d7868096604ab473d7668e4150d2c9f287781caa7f56"
sources:
  - raw/2026-04-25-copilot-session-direct-sportsbook-ingestion-a78d087a.md
related:
  - "[[Primary Prop Line Selection to Avoid Alternate Line Contamination]]"
  - "[[Standard Over/Under vs Milestone Prop Market Identity]]"
  - "[[Generic Sportsbook Market Storage for Non-Canonical Props]]"
  - "[[Heuristic Cleanup vs Market-Aware Prop Ingestion]]"
tier: hot
tags: [sports-betting, data-ingestion, prop-lines, sportsbook-data, nba-ml-engine]
---

# Source-Priority Canonical Prop Ingestion

## Overview

Source-priority canonical prop ingestion is a market-serving rule that decides which current prop row should represent a bookmaker when multiple providers claim to have the same player/stat line. Instead of treating all sources as peers or relying only on "closest to prediction," the pipeline assigns explicit trust order to each source and resolves conflicts inside the same bookmaker family before rows reach user-facing queries.

This matters because once direct sportsbook adapters exist, a pipeline no longer has to guess equally among aggregator rows. It can prefer direct-book truth (`DK_WEB`, `FD_WEB`) over indirect or noisier feeds while still preserving cross-book diversity between DraftKings and FanDuel.

## How It Works

The concept starts by separating two different questions that older pipelines often blur together. The first question is **which bookmaker** a row belongs to: DraftKings, FanDuel, or something else. The second is **which source within that bookmaker family** should win when several rows describe the same `player_id`, `game_date`, and `stat_name`. The checkpoint codifies both pieces instead of allowing source strings to float around as opaque labels. `DK_WEB`, `DK`, and `SGO_DK` all map to the bookmaker key `draftkings`; `FD_WEB`, `FD`, and `SGO_FD` all map to `fanduel`. Unknown sources are intentionally isolated under synthetic keys like `source:<source>` so they do not accidentally shadow trusted rows from known books.

Once rows are grouped by bookmaker, the pipeline applies an explicit priority ladder. The highest-trust sources are the direct sportsbook adapters, `DK_WEB` and `FD_WEB`, both ranked at priority `0`. The next tier is bookmaker-specific aggregator rows from `DK` and `FD`, ranked at `10`. SportsGameOdds-derived rows (`SGO_DK`, `SGO_FD`) are ranked at `20`, reflecting the already-documented risk that mixed market families or stale extractions can survive in that feed. Lower is better, so a direct DraftKings row always beats a DraftKings aggregator row for the same player/date/stat combination, but it does **not** erase FanDuel's row because cross-book comparison remains useful.

This ranking is powerful because it changes the ingestion contract from a best-effort heuristic to an explicit trust model. Earlier cleanup logic, captured in [[Primary Prop Line Selection to Avoid Alternate Line Contamination]], picked the line closest to the model prediction. That is still a reasonable heuristic when the system has only noisy provider rows. But once the system has direct-book data, the canonical current-line question becomes lexicographic rather than purely numeric:

$$
\text{rank}(r) = \left(p_{\text{source}}(r), \left|\hat{y} - \text{line}(r)\right|\right)
$$

where $p_{\text{source}}(r)$ is the explicit source-priority score and $\hat{y}$ is the model prediction. In the new architecture, source priority decides first; "closest to prediction" only becomes relevant after the right market class and source tier have already been selected.

The implementation uses this rule twice. During ingestion, `_filter_current_prop_rows_by_source_priority()` removes lower-priority duplicates among current rows, and `_delete_shadowed_current_prop_lines()` clears already-stored rows that would otherwise coexist incorrectly with a higher-trust replacement. That means the live `prop_lines` table stops carrying several mutually competing "current DraftKings steals" rows for the same player/stat. During read-time serving, the materialized view `mv_prop_lines_primary` and FastAPI prop-edge query logic both rank by bookmaker-aware source priority before choosing the best surviving row. The unique index on the view also changes to `(player_id, game_date, stat_name, bookmaker)`, which makes the contract explicit: one canonical current row per bookmaker, not one global winner across all books.

The concept also depends on prior taxonomy work. Source priority only works safely after the candidate rows have already been limited to the right market family. That is why the same checkpoint adds `market_scope` and `market_class` metadata and filters serving queries to `market_scope='player'` and `market_class='standard_ou'`. Without that constraint, a high-trust direct source could still provide the wrong kind of market, such as a milestone ladder or game prop, and win for the wrong reason. In other words, source priority is not a substitute for market classification; it is the decision rule that becomes reliable **after** market classification.

Another important design feature is failure tolerance. Direct sportsbooks are preferred, but not required for ingestion to continue. The pipeline fetches direct sportsbook rows first, then falls back to [[Odds API]], then to [[SportsGameOdds (SGO) API]], logging provider failures as warnings instead of aborting the whole run. That turns source priority into a graceful degradation system rather than a brittle dependency graph. If `DK_WEB` fails today, a valid `DK` row can still serve; if only `SGO_DK` exists, it can still participate, but at an explicitly lower trust level.

The result is a cleaner separation of roles. Bookmaker identity answers "whose line is this?" Source priority answers "which observation of that bookmaker should we trust most right now?" Prediction proximity answers "which surviving line is most representative when more than one still qualifies?" Each layer has a clear job, and the later layers no longer have to compensate for missing truth signals that the earlier layers could have encoded directly.

## Key Properties

- **Bookmaker-aware deduplication:** Conflict resolution happens inside a bookmaker family rather than globally across all books.
- **Explicit trust ladder:** `DK_WEB`/`FD_WEB` outrank `DK`/`FD`, which outrank `SGO_DK`/`SGO_FD`, making source preference auditable and repeatable.
- **Graceful fallback:** Direct-source failure does not stop ingestion; lower-trust sources remain available with their reduced priority.
- **Serving alignment:** The same source-priority rule is enforced both at write time and in read-time query paths.

## Limitations

Source priority assumes the source-to-bookmaker map is correct and maintained as new providers or labels appear. It also cannot rescue rows that were misclassified into the wrong market family; that problem must be solved upstream by taxonomy filters such as [[Standard Over/Under vs Milestone Prop Market Identity]]. Finally, if a direct-book endpoint becomes stale or structurally wrong, the system will still trust it until validation rules or audits detect the drift.

## Examples

```python
def rank_prop_row(row, predicted_value):
    source_priority = {
        "DK_WEB": 0,
        "FD_WEB": 0,
        "DK": 10,
        "FD": 10,
        "SGO_DK": 20,
        "SGO_FD": 20,
    }.get(row["source"], 100)
    return (source_priority, abs(predicted_value - row["line"]))
```

## Practical Applications

This concept is useful anywhere a sportsbook pipeline combines direct bookmaker adapters with aggregator fallbacks. In the [[NBA ML Engine]], it protects current prop views, API edge generation, and materialized views from reverting to weaker feeds when stronger book-specific truth is available.

## Related Concepts

- **[[Primary Prop Line Selection to Avoid Alternate Line Contamination]]** — An earlier heuristic cleanup layer that now operates after explicit source trust and market filtering.
- **[[Standard Over/Under vs Milestone Prop Market Identity]]** — Defines the market-family filter that must run before source priority can safely pick a winner.
- **[[Generic Sportsbook Market Storage for Non-Canonical Props]]** — Supplies the storage split that keeps non-canonical markets out of the canonical prop candidate set.

## Sources

- [[Copilot Session Checkpoint: Direct Sportsbook Ingestion]] — the implementation checkpoint that adds the source ladder, shadowed-row deletion, and serving-path alignment

