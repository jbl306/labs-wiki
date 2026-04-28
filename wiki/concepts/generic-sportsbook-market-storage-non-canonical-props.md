---
title: "Generic Sportsbook Market Storage for Non-Canonical Props"
type: concept
created: 2026-04-25
last_verified: 2026-04-25
source_hash: "bb9e0e187a674b361745d7868096604ab473d7668e4150d2c9f287781caa7f56"
sources:
  - raw/2026-04-25-copilot-session-direct-sportsbook-ingestion-a78d087a.md
related:
  - "[[Standard Over/Under vs Milestone Prop Market Identity]]"
  - "[[Source-Priority Canonical Prop Ingestion]]"
  - "[[Local DB-Only Prop Market Metadata Backfill]]"
  - "[[Heuristic Cleanup vs Market-Aware Prop Ingestion]]"
tier: hot
tags: [sports-betting, data-modeling, prop-lines, sportsbook-data, nba-ml-engine]
quality_score: 65
---

# Generic Sportsbook Market Storage for Non-Canonical Props

## Overview

Generic sportsbook market storage is a schema pattern that keeps canonical player over/under props separate from the larger universe of sportsbook markets. Instead of forcing milestones, ladders, game spreads, moneylines, and other non-model-ready selections into the same table as standard player O/U rows, the pipeline gives them their own durable storage while preserving just enough metadata on canonical rows to make the boundary explicit.

This matters because many sportsbook ingestion failures come from treating "all extracted betting markets" as if they served the same downstream purpose. Canonical model inputs, historical evaluation rows, and exploratory sportsbook intelligence all have different storage needs.

## How It Works

The checkpoint begins from an architectural diagnosis: `prop_lines` had become too semantically overloaded. The table was useful because it already powered model serving, dashboard props views, and snapshot history, but that same convenience made it a magnet for data that did not belong there. Once direct sportsbook parsing became richer, the system could easily see milestone ladders like `2+ steals`, game spreads, totals, and other bookmaker markets that are interesting in their own right but unsafe to present as the canonical player line used for model comparison. The solution was not to discard those markets; it was to stop pretending they had the same contract as standard player O/U rows.

The new design therefore defines `prop_lines` much more narrowly: it remains the home for **model-ready standard player over/under markets only**. To support that narrowing, both `PropLine` and `PropLineSnapshot` gain explicit metadata fields: `bookmaker`, `market_scope`, `market_class`, and `provider_market_id`. Those columns encode the semantic assumptions that were previously implicit. A row can now say, in the schema itself, that it belongs to the `draftkings` bookmaker, has `market_scope='player'`, has `market_class='standard_ou'`, and came from a specific provider market identifier. Once those fields exist, downstream queries no longer have to infer intent from a source string alone.

Everything else moves into new generic tables: `sportsbook_markets` and `sportsbook_market_snapshots`. The idea is simple but powerful. A sportsbook can expose many real and useful markets that should be kept for auditability, future product work, or later modeling, even if the current production dashboard must not treat them as the "main line." By creating dedicated generic market tables, the pipeline can retain milestone ladders, game props, spreads, totals, moneylines, and similar rows without contaminating the canonical prop surface. This is especially important for DraftKings, where the checkpoint explicitly routes standard `Steals O/U` rows into `prop_lines` while sending steals milestones and game-scope markets into generic sportsbook storage.

The ingestion flow makes the separation concrete. Direct adapters emit either canonical prop rows or generic sportsbook market rows based on sportsbook-specific parsing rules. FanDuel's adapter accepts standard `MOVING_HANDICAP` player O/U markets as canonical rows. DraftKings' adapter recognizes standard categories such as `Steals O/U`, but captures milestone and game markets separately. `fetch_prop_lines()` then persists generic market rows and snapshots before normalizing canonical prop rows, applying validation filters, and enforcing source priority. This ordering matters because it prevents the system from needing an all-or-nothing decision. A market can be preserved for knowledge and audit while still being rejected from the canonical path.

The new schema also improves query safety. Materialized views and API paths can now filter explicitly on `(market_scope = 'player' OR NULL)` and `(market_class = 'standard_ou' OR NULL)` as a transitional contract, then progressively rely more on the populated metadata fields over time. The checkpoint updates `mv_prop_lines_primary` and `src/applications/prop_finder.py` to do exactly that. This is a major upgrade from earlier heuristics that had to infer "primary-ness" from predicted-value proximity alone. The storage model teaches the serving layer what kind of row it is allowed to consider before any ranking happens.

One of the most subtle benefits appears in snapshot semantics. The checkpoint notes that `prop_line_snapshots` still conflict on `(player_id, game_date, stat_name, source)`, which means they do not yet preserve every fetch timestamp as immutable line-movement history for props. By contrast, generic sportsbook snapshots use a richer identity based on `provider_source`, `external_market_id`, `selection_label`, and `fetched_at`. That difference reveals why generic market storage is not merely a side table; it is also a better fit for high-cardinality sportsbook surfaces where multiple related selections can coexist and where retaining each fetch matters more than collapsing to a single current row.

The design therefore turns one overloaded table into a layered market model. Canonical tables serve the narrow needs of prediction comparison and user-facing current props. Generic tables preserve the broader sportsbook world without forcing the dashboard contract to widen. This makes the system both more honest and more extensible: future features can mine generic markets without reopening the contamination problems that the canonical serving path just solved.

## Key Properties

- **Contract narrowing:** `prop_lines` is explicitly reserved for standard player O/U markets.
- **Schema-level taxonomy:** `bookmaker`, `market_scope`, `market_class`, and `provider_market_id` make row meaning explicit.
- **Lossless retention:** Non-canonical sportsbook markets are preserved in dedicated generic tables instead of being discarded.
- **Better snapshot identity:** Generic market snapshots preserve richer market-level provenance than the older canonical snapshot contract.

## Limitations

The storage split depends on accurate parser classification, so schema clarity does not remove the need for sportsbook-specific market rules. Historical canonical snapshots still have the older conflict key and therefore do not yet capture every line movement immutably. The generic tables also preserve more data than the current dashboard uses, which is valuable but can increase storage and interpretation complexity if not paired with clear downstream contracts.

## Examples

```sql
-- Canonical model-ready row
INSERT INTO prop_lines (
  player_id, game_date, stat_name, source, bookmaker, market_scope, market_class, provider_market_id
) VALUES (
  123, '2026-04-25', 'stl', 'DK_WEB', 'draftkings', 'player', 'standard_ou', '328789167'
);

-- Non-canonical sportsbook market kept for audit and future use
INSERT INTO sportsbook_markets (
  provider_source, bookmaker, market_scope, market_class, external_market_id, selection_label
) VALUES (
  'DK_WEB', 'draftkings', 'player', 'milestone', '328789999', 'Josh Hart 2+ Steals'
);
```

## Practical Applications

This concept is useful for sports-betting systems that need both a narrow model-serving contract and a broader sportsbook intelligence layer. In the [[NBA ML Engine]], it lets the current props dashboard stay clean while still retaining milestone and game-market data for future products, audits, or exploratory modeling.

## Related Concepts

- **[[Standard Over/Under vs Milestone Prop Market Identity]]** — Supplies the taxonomy that determines whether a market belongs in the canonical or generic path.
- **[[Source-Priority Canonical Prop Ingestion]]** — Uses the canonical subset after the storage model has already removed non-canonical market classes.
- **[[Local DB-Only Prop Market Metadata Backfill]]** — Retrofits older canonical rows with the metadata needed to participate in this new storage contract.

## Sources

- [[Copilot Session Checkpoint: Direct Sportsbook Ingestion]] — primary source for the schema expansion, adapter routing, and snapshot-contract distinction

