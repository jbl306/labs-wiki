---
title: "Heuristic Cleanup vs Market-Aware Prop Ingestion"
type: synthesis
created: 2026-04-25
last_verified: 2026-04-25
source_hash: "synthesis-generated"
sources:
  - raw/2026-04-25-copilot-session-direct-sportsbook-ingestion-a78d087a.md
  - raw/2026-04-25-copilot-session-direct-sportsbook-sources-855a32a8.md
  - raw/2026-04-25-copilot-session-backtest-completion-props-investigation-ed8d6cc6.md
concepts:
  - primary-prop-line-selection-to-avoid-alternate-line-contamination
  - source-priority-canonical-prop-ingestion
  - generic-sportsbook-market-storage-non-canonical-props
  - local-db-only-prop-market-metadata-backfill
related:
  - "[[Primary Prop Line Selection to Avoid Alternate Line Contamination]]"
  - "[[Source-Priority Canonical Prop Ingestion]]"
  - "[[Generic Sportsbook Market Storage for Non-Canonical Props]]"
  - "[[Local DB-Only Prop Market Metadata Backfill]]"
  - "[[Heuristic Prop-Line Selection vs Direct Sportsbook Validation]]"
tier: hot
tags: [sports-betting, synthesis, data-ingestion, prop-lines, nba-ml-engine]
---

# Heuristic Cleanup vs Market-Aware Prop Ingestion

## Question

How should a sportsbook ingestion stack evolve once "closest to prediction" heuristics are no longer enough to guarantee canonical user-facing lines?

## Summary

Heuristic cleanup remains useful as a defensive filter for noisy provider data, but it is no longer sufficient once the system can observe richer market taxonomy and direct-book truth. The stronger architecture is market-aware ingestion: classify the market first, store non-canonical markets separately, prefer explicit source trust inside each bookmaker, and use backfill only to make older rows compatible with that contract.

## Comparison

| Dimension | [[Primary Prop Line Selection to Avoid Alternate Line Contamination]] | [[Source-Priority Canonical Prop Ingestion]] |
|-----------|---------------|---------------|
| Core decision rule | Pick the row closest to the model prediction | Prefer the highest-trust source within each bookmaker, then rank surviving rows |
| Best input environment | Noisy provider feeds with many alternate lines | Mixed direct-book plus aggregator ecosystem with explicit source tiers |
| Market taxonomy dependency | Implicit; can still mis-rank mixed market families | Explicit; expects `market_scope` and `market_class` filtering first |
| Storage model | Assumes candidate rows already live in one canonical table | Works with [[Generic Sportsbook Market Storage for Non-Canonical Props]] so only canonical markets compete |
| Historical migration story | Limited; mostly helps current selection | Uses [[Local DB-Only Prop Market Metadata Backfill]] to retrofit old rows into the new contract |
| Main failure mode | Closest line can still be the wrong market family | Wrong source map or misclassified market can still promote the wrong row |

## Analysis

The older heuristic approach solved a real and important problem: when a provider feed contains many rows for the same player/stat pair, allowing "first row wins" is clearly wrong. Ranking by distance to the model prediction is a strong corrective because canonical sportsbook lines often cluster near the model's central expectation, while alternates and ladders tend to drift farther away. For a system that only has noisy feed data, this is a pragmatic and scalable solution.

But the direct sportsbook work changes the architecture in a deeper way. Once the pipeline can parse direct DraftKings and FanDuel rows, the core question is no longer just "which row looks most plausible?" The system can ask "which row comes from the most trustworthy observation of this bookmaker?" That moves the design from inference to explicit policy. A direct DraftKings row beating an SGO-derived DraftKings row is not merely a statistical preference; it is a declared truth hierarchy.

The new design is stronger because it combines several changes rather than swapping one ranking function for another. [[Generic Sportsbook Market Storage for Non-Canonical Props]] removes milestones, ladders, spreads, and other non-canonical markets from the main competition set. [[Source-Priority Canonical Prop Ingestion]] then resolves conflicts among the remaining canonical candidates inside each bookmaker. [[Local DB-Only Prop Market Metadata Backfill]] makes historical rows legible to the new filters without forcing a costly external re-ingest. Together, these layers turn canonical current-line selection into an architecture problem instead of a single SQL trick.

This does not make the older heuristic obsolete. It still matters when direct-book rows are unavailable, when the system must degrade gracefully to aggregator feeds, or when several same-tier candidates remain after market filtering. In fact, the best reading is that the heuristic has been demoted from "truth proxy" to "secondary tiebreaker." That is a healthier role because it matches what the heuristic actually knows.

For a production system like the [[NBA ML Engine]], the practical choice is therefore staged. Use heuristic cleanup as the baseline defense for ambiguous provider payloads. Add direct-book validation when truth is in dispute. Then, once direct adapters become part of ingestion, encode that truth hierarchy directly into storage and serving. The checkpoint is valuable because it captures that exact transition from reactive auditing to durable system design.

## Key Insights

1. **Heuristics are most reliable after market taxonomy has already narrowed the candidate set** — supported by [[Primary Prop Line Selection to Avoid Alternate Line Contamination]] and [[Generic Sportsbook Market Storage for Non-Canonical Props]].
2. **Direct-book truth becomes operationally valuable only when source trust is encoded in the ingestion contract** — supported by [[Source-Priority Canonical Prop Ingestion]] and [[Copilot Session Checkpoint: Direct Sportsbook Sources]].
3. **Schema upgrades need rate-limit-safe migration paths, not just better live ingests** — supported by [[Local DB-Only Prop Market Metadata Backfill]].

## Open Questions

- Should unknown or newly added providers automatically land in isolated bookmaker buckets, or should some be mapped into trusted bookmaker families only after explicit review?
- When direct-book data is temporarily missing, what is the safest fallback policy for serving user-facing current props: stale direct rows, fresh aggregator rows, or a surfaced "truth uncertain" state?

## Sources

- [[Copilot Session Checkpoint: Direct Sportsbook Ingestion]]
- [[Copilot Session Checkpoint: Direct Sportsbook Sources]]
- [[Copilot Session Checkpoint: Backtest Completion Props Investigation]]

