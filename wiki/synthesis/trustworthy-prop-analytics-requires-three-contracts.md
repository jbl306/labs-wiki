---
title: Trustworthy Prop Analytics Requires Three Contracts
type: synthesis
created: '2026-05-31'
last_verified: '2026-05-31'
source_hash: 760baa9db4981a345a5194dd8a838c416745218038590dc1747bbce393d7a34c
sources:
- raw/2026-05-31-copilot-session-sprint-accuracy-planning-8edf737a.md
- raw/2026-05-31-copilot-session-canonical-props-implementation-c9632506.md
- raw/2026-04-25-copilot-session-backtest-accuracy-contracts-a089eefe.md
- raw/2026-04-25-copilot-session-dashboard-accuracy-fixes-3717a5b2.md
concepts:
- point-in-time-prop-snapshot-identity
- shared-canonical-settled-prop-population-consistency
- shared-contract-normalization-dashboard-apis
related:
- '[[Point-in-Time Prop Snapshot Identity]]'
- '[[Shared Canonical Settled-Prop Population for Analytics Consistency]]'
- '[[Shared Contract Normalization for Dashboard APIs]]'
- '[[NBA ML Engine]]'
tier: hot
tags:
- synthesis
- nba-ml-engine
- prop-accuracy
- dashboard
- backtesting
- data-contracts
quality_score: 84
evidence_scope: within-source
evidence_source_count: 4
evidence_origin_family_count: 1
---

# Trustworthy Prop Analytics Requires Three Contracts

## Question

What has to align for an NBA prop analytics stack to make trustworthy user-facing claims instead of producing locally plausible but globally inconsistent numbers?

## Summary

The checkpoint series shows that one fix is never enough. Trustworthy prop analytics in the [[NBA ML Engine]] requires three aligned contracts: immutable storage identity, a shared canonical settled population, and a normalized API/dashboard contract that tells consumers exactly what they are seeing.

If any one of those layers drifts, the others inherit ambiguity. Clean UI payloads cannot rescue duplicated storage grain, and a perfect canonical SQL helper still loses meaning if the dashboard routes reshape or label its output inconsistently.

## Comparison

| Dimension | [[Point-in-Time Prop Snapshot Identity]] | [[Shared Canonical Settled-Prop Population for Analytics Consistency]] | [[Shared Contract Normalization for Dashboard APIs]] |
|-----------|------------------------------------------|------------------------------------------------------------------------|------------------------------------------------------|
| Primary concern | Preserve historical truth at storage time | Reuse one settled denominator across analytics surfaces | Emit one stable consumer-facing payload shape |
| Main artifact | `prop_line_snapshots` unique key including `fetched_at` | `canonical_props.py` helpers and settled-population CTEs | `dashboardContracts.ts` normalization helpers |
| Typical failure prevented | Lost line movement and fake history | Fan-out, denominator drift, and cross-endpoint disagreement | Empty widgets, silently divergent field meanings, route-specific contract drift |
| Canonical grain | One captured row per player/date/source/stat/time | One settled row per player/date/stat | One normalized record shape per route payload |
| Where it shows up | Ingest and migration logic | Backtests, calibration, model-health, matviews, notifications | BFF and frontend response handling |
| User-visible symptom when broken | Historical audit queries cannot explain what line was seen when | Hit rates, counts, and health summaries disagree | Dashboard renders misleading or inconsistent views even with "successful" responses |

## Analysis

The first contract lives at the bottom of the stack: storage must preserve observed events as events. The May 31 checkpoint makes this painfully concrete. A snapshot table that collapses all repeated captures into one coarse identity is not a history table in any meaningful sense. Once that happens, every later metric is forced to reason over rewritten evidence. [[Point-in-Time Prop Snapshot Identity]] fixes that by making the capture timestamp part of the key and by treating exact duplicates as idempotent replays rather than updates.

The second contract lives in the middle: once history is real, analytics consumers still need to agree on which slice of that history counts as "canonical settled performance." The earlier backtest work established that headline metrics must match settled Props History rather than a broader convenience join. The May 31 checkpoint generalizes that lesson across calibration, model-health, notifications, and materialized views. [[Shared Canonical Settled-Prop Population for Analytics Consistency]] is the rule that keeps those consumers from quietly inventing their own denominators.

The third contract lives at the system boundary. Even if storage grain and population grain are correct, users still experience the system through API payloads and dashboard routes. [[Shared Contract Normalization for Dashboard APIs]] explains why nearby routes cannot each reinterpret upstream shapes on their own. If the BFF and frontend let every endpoint improvise its own field names, derived semantics, or failure shapes, the system can display structurally inconsistent truths while all the underlying SQL is technically correct.

Taken together, the three contracts form a dependency chain. Storage identity answers "what evidence exists?" Shared canonical population answers "which evidence counts for this claim?" Contract normalization answers "how is that claim presented to consumers?" The May 31 checkpoint is valuable because it shows a mature system recognizing that prop accuracy failures were not isolated bugs. They were contract-boundary leaks across three layers.

This layered view also prevents the wrong repair reflex. When dashboard numbers disagree, the instinct is often to patch the route or relabel the card. But the right question is which contract failed first. Was the historical record collapsed? Did a query multiply rows through source-sensitive ranking or mutable joins? Or did the BFF present different populations under similar names? Thinking in contracts turns a vague trust problem into a structured debugging sequence.

## Key Insights


1. **Immutable history is a prerequisite, not an optimization** — supported by [[Copilot Session Checkpoint: Canonical Props Implementation]], [[Point-in-Time Prop Snapshot Identity]]
2. **Canonical denominator reuse is what converts a one-off backtest fix into a stable analytics architecture** — supported by [[Copilot Session Checkpoint: Backtest Accuracy Contracts]], [[Shared Canonical Settled-Prop Population for Analytics Consistency]]
3. **A truthful dashboard requires semantic normalization in addition to correct SQL** — supported by [[Copilot Session Checkpoint: Dashboard Accuracy Fixes]], [[Shared Contract Normalization for Dashboard APIs]]

## Evidence Map

| Insight | Supporting pages | Raw provenance | Confidence / limits |
|---|---|---|---|
| **Immutable history is a prerequisite, not an optimization** | [[Copilot Session Checkpoint: Canonical Props Implementation]], [[Point-in-Time Prop Snapshot Identity]] | `raw/2026-05-31-copilot-session-canonical-props-implementation-c9632506.md`, `raw/2026-05-31-copilot-session-sprint-accuracy-planning-8edf737a.md` | Legacy mapping reconstructed from existing wikilinks and declared provenance; verify semantics. |
| **Canonical denominator reuse is what converts a one-off backtest fix into a stable analytics architecture** | [[Copilot Session Checkpoint: Backtest Accuracy Contracts]], [[Shared Canonical Settled-Prop Population for Analytics Consistency]] | `raw/2026-04-25-copilot-session-backtest-accuracy-contracts-a089eefe.md`, `raw/2026-05-31-copilot-session-canonical-props-implementation-c9632506.md`, `raw/2026-05-31-copilot-session-sprint-accuracy-planning-8edf737a.md` | Legacy mapping reconstructed from existing wikilinks and declared provenance; verify semantics. |
| **A truthful dashboard requires semantic normalization in addition to correct SQL** | [[Copilot Session Checkpoint: Dashboard Accuracy Fixes]], [[Shared Contract Normalization for Dashboard APIs]] | `raw/2026-04-25-copilot-session-dashboard-accuracy-fixes-3717a5b2.md` | Legacy mapping reconstructed from existing wikilinks and declared provenance; verify semantics. |

## Open Questions

- Should canonical population metadata become a mandatory field on every dashboard payload so users can always see which denominator a card or table used?
- When direct-book lines are stale or quarantined, should the canonical population shrink loudly, or should the system preserve coverage with explicit lower-trust fallback labels?

## Sources

- [[Copilot Session Checkpoint: Canonical Props Implementation]]
- [[Copilot Session Checkpoint: Sprint Accuracy Planning]]
- [[Copilot Session Checkpoint: Backtest Accuracy Contracts]]
- [[Copilot Session Checkpoint: Dashboard Accuracy Fixes]]
