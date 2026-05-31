---
title: "Copilot Session Checkpoint: Sprint Accuracy Planning"
type: source
created: '2026-05-31'
last_verified: '2026-05-31'
source_hash: f58d03d9198f9d44771d6097a9392ee851f201bb2af67af7fcf6677a0961769b
sources:
  - raw/2026-05-31-copilot-session-sprint-accuracy-planning-8edf737a.md
concepts:
  - point-in-time-prop-snapshot-identity
  - shared-canonical-settled-prop-population-consistency
  - shared-contract-normalization-dashboard-apis
related:
  - "[[NBA ML Engine]]"
  - "[[Durable Copilot Session Checkpoint]]"
  - "[[Copilot CLI]]"
  - "[[MemPalace]]"
  - "[[Copilot Session Checkpoint: Audit Recommendations Sprint]]"
  - "[[Copilot Session Checkpoint: Canonical Props Implementation]]"
  - "[[Trustworthy Prop Analytics Requires Three Contracts]]"
tags: [copilot-session, checkpoint, nba-ml-engine, sprint-planning, prop-accuracy, dashboard, data-contracts]
tier: hot
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 74
---

# Copilot Session Checkpoint: Sprint Accuracy Planning

## Summary

This checkpoint captures the planning handoff that turned a broad accuracy audit of the [[NBA ML Engine]] into Sprint 62 implementation work. Its durable value is the way it preserves both the live database evidence behind the trust concerns and the explicit implementation order that later became the canonical-props hardening effort.

It also shows that the problem was not a single broken query. DB freshness, prop matching, calibration fan-out, and dashboard semantics were all drifting at once, which is why the session converged on immutable snapshots, a shared canonical settled-prop helper, and stricter downstream contract discipline.

## Key Points

- The session began as a three-surface audit: DB accuracy, props accuracy, and dashboard accuracy were reviewed together and then converted into **Sprint 62 - Accuracy Trust Hardening** in `nba-ml-engine/tasks/todo.md`.
- Investigation used three parallel researcher agents plus live read-only Postgres checks through `docker exec -i nba-ml-db ... psql` because the default local `nba_ml` connection was failing password authentication.
- The live audit exposed freshness drift across layers: `game_logs` were current through **2026-05-30**, `predictions` through **2026-05-31**, and `prop_lines` / `prop_line_snapshots` through **2026-06-03**, but the latest joined prop-plus-prediction slate only reached **2026-05-26**.
- `prop_line_snapshots` showed **24,421** rows and **24,421** coarse identities, strong evidence that repeated captures were collapsing instead of preserving real line-movement history.
- The 30-day comparison preserved the denominator problem that later drove the canonical helper design: **6,080** settled snapshots, **2,238** canonical joined bets, **4,360** broad materialized-view calls, and a calibration join fan-out of **3.80x**.
- Model-health evidence already showed downstream trust risk: the latest status was **degraded**, expected calibration error was **0.026**, hit rate was **60.2%**, and the PTS alert sat at **42.4%** over **92** seven-day predictions.
- Concrete line mismatches made the quality problem legible, including Victor Wembanyama rebounds **3.5 vs 12.5**, Josh Hart rebounds **2.5 vs 7.5**, Jalen Brunson assists **2.5 vs 6.5**, and Josh Hart steals **0.5 vs 1.5**.
- The planned architecture centered on one shared settled-prop population: canonical identity should come from immutable snapshot data rather than mutable `prop_lines`, with grain defined by player, date, stat, source/bookmaker, line, and capture time.
- The implementation plan was decomposed into seven workstreams: `canonical-helper`, `snapshot-identity`, `prop-edge-gates`, `calibration-health`, `canonical-matviews`, `dashboard-contracts`, and `validation-tests`.
- The checkpoint set durable operating rules that later implementation followed: heavy aggregation belongs in materialized views, dashboard fallbacks should not hide data problems, and missing canonical values should prefer `NULL` over invented defaults.

## Key Concepts

- **[[Point-in-Time Prop Snapshot Identity]]** — the storage-layer fix required to stop `prop_line_snapshots` from behaving like a mutable latest-state table.
- **[[Shared Canonical Settled-Prop Population for Analytics Consistency]]** — the rule that every realized-performance surface should reuse one settled denominator.
- **[[Shared Contract Normalization for Dashboard APIs]]** — the downstream contract discipline needed so dashboard payloads do not hide or relabel population drift.

## Related Entities

- **[[NBA ML Engine]]** — the system whose prop-history, calibration, and dashboard layers were being rewritten around one trust boundary.
- **[[Durable Copilot Session Checkpoint]]** — the artifact pattern that preserved this pre-implementation planning state as reusable knowledge.
- **[[Copilot CLI]]** — the execution environment used to coordinate parallel review, live DB inspection, sprint planning, and checkpoint capture.
- **[[MemPalace]]** — the memory system used to recover earlier repo context and preserve findings from the audit phase.
