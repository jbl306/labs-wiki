---
title: "Copilot Session Checkpoint: Canonical Props Implementation"
type: source
created: '2026-05-31'
last_verified: '2026-05-31'
source_hash: 4789cd410f350d2cdd568e54d1046ea32d670d8e84f60dd954754b706b61ec98
sources:
  - raw/2026-05-31-copilot-session-canonical-props-implementation-c9632506.md
concepts:
  - point-in-time-prop-snapshot-identity
  - shared-canonical-settled-prop-population-consistency
  - canonical-settled-prop-backtesting-trustworthy-ml-dashboards
related:
  - "[[NBA ML Engine]]"
  - "[[Durable Copilot Session Checkpoint]]"
  - "[[Copilot CLI]]"
  - "[[MemPalace]]"
tags: [copilot-session, checkpoint, nba-ml-engine, prop-accuracy, backtesting, calibration, dashboard, data-contracts]
tier: hot
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 78
---

# Copilot Session Checkpoint: Canonical Props Implementation

## Summary

This checkpoint captures Sprint 62's shift from loosely related prop analytics surfaces to a single trust contract inside the [[NBA ML Engine]]. Its main lesson is that prop accuracy work does not stabilize until storage grain, canonical settled-population selection, and downstream dashboard/evaluation consumers all reuse the same immutable evidence boundary.

The checkpoint is also a mid-implementation handoff rather than a victory lap. It records the architectural decisions, live audit evidence, partial rewires, and open verification risks that remained before the hardening work could be called complete.

## Key Points

- Sprint 62 reframed the accuracy problem as a shared-contract problem: `prop_line_snapshots` plus a canonical settled-prop helper should become the source of truth for prop edges, backtests, calibration, model health, materialized views, notifications, and dashboard contracts.
- The live audit showed why the old setup was untrustworthy: `prop_lines` and `prop_line_snapshots` were current through **2026-06-03**, but the latest joined prop-plus-prediction slate only reached **2026-05-26**, indicating serious downstream drift.
- Snapshot history was not actually historical under the old uniqueness rule: `prop_line_snapshots` contained **24,421** rows and **24,421** coarse identities, meaning repeated captures were collapsing instead of preserving multi-point line movement.
- The new helper module `src/evaluation/canonical_props.py` defines `CANONICAL_SETTLED_PROPS_CTE`, `canonical_settled_props_query`, `fetch_canonical_settled_props`, `fetch_canonical_population_count`, and `fetch_canonical_calibration_rows` so multiple consumers can share the same settled population.
- Canonical identity is explicitly source-agnostic at the analytics grain: one settled snapshot per `player_id / game_date / stat_name`, chosen from immutable `prop_line_snapshots` with source priority and without falling back to mutable `prop_lines`.
- Snapshot identity was hardened at write time and schema level: `src/data/prop_lines.py` switched snapshot inserts to point-in-time `on_conflict_do_nothing`, while an Alembic migration replaced the coarse unique constraint with `player_id / game_date / source / stat_name / fetched_at`.
- The ingestion path now quarantines suspicious current-line rows earlier by rejecting unsupported stats, nonpositive lines, missing side odds, non-player or non-standard markets, missing game context, and paired DraftKings/FanDuel line gaps.
- Prop-edge scoring now carries explicit odds semantics instead of pseudo-edge shortcuts: the checkpoint adds American-odds helpers, implied probability, decimal odds, expected value, vig-aware gating, absolute edge thresholds, and diagnostic metadata fields such as `model_probability`, `implied_probability`, and `vig_gate_passed`.
- The checkpoint preserves hard evidence of denominator drift: over the previous 30 days the system had **6,080** settled snapshots, **2,238** canonical joined bets, **4,360** broad materialized-view calls, and a calibration join fan-out of **3.80x**.
- Several rewires were still incomplete at compaction time: `src/api/server.py`, `src/notifications/dispatcher.py`, and especially `scripts/optimize_db.py` needed syntax and correctness review before tests; no lint, build, or pytest pass had run yet.
- The broader durable lesson is architectural, not cosmetic: prefer explicit metadata over invented defaults, quarantine suspicious inputs before scoring, and push heavy aggregation into shared SQL helpers or materialized views instead of request-time ad hoc joins.

## Key Concepts

- **[[Point-in-Time Prop Snapshot Identity]]** — why immutable `fetched_at`-scoped snapshot keys are required if prop history is supposed to preserve line movement instead of overwriting it.
- **[[Shared Canonical Settled-Prop Population for Analytics Consistency]]** — why backtesting, calibration, model-health, notifications, and dashboard metrics need one shared settled-population boundary.
- **[[Canonical Settled-Prop Backtesting for Trustworthy ML Dashboards]]** — the earlier trust contract for headline backtesting that this checkpoint now generalizes into a wider analytics architecture.
- **[[Source-Priority Canonical Prop Ingestion]]** — the upstream bookmaker/source-ranking rule that remains important once the canonical population is built from immutable snapshots.

## Related Entities

- **[[NBA ML Engine]]** — the production system whose prop history, evaluation, and dashboard surfaces were being rewired around one canonical population.
- **[[Durable Copilot Session Checkpoint]]** — the artifact pattern that turned an interrupted implementation into reusable architectural memory.
- **[[Copilot CLI]]** — the agent runtime used to audit live DB state, track sprint work, edit code, and preserve the partial implementation.
- **[[MemPalace]]** — the memory system used earlier in the session to recover prior repo context and parallel review findings.

