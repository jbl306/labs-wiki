---
title: "Copilot Session Checkpoint: Backtest Accuracy Contracts"
type: source
created: '2026-04-25'
last_verified: '2026-04-25'
source_hash: 6925ce7a48d728479bbb091c23eb9fd2775349c5187f58544249a5dc6cbc546f
sources:
  - raw/2026-04-25-copilot-session-backtest-accuracy-contracts-a089eefe.md
concepts:
  - canonical-settled-prop-backtesting-trustworthy-ml-dashboards
  - broad-diagnostic-backtesting-secondary-model-evidence
related:
  - "[[NBA ML Engine]]"
  - "[[Durable Copilot Session Checkpoint]]"
  - "[[Copilot CLI]]"
  - "[[Shared Contract Normalization for Dashboard APIs]]"
  - "[[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]"
tags: [copilot-session, checkpoint, nba-ml-engine, backtesting, dashboard, api-contracts, canonical-data]
tier: hot
checkpoint_class: durable-architecture
retention_mode: retain
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 79
---

# Copilot Session Checkpoint: Backtest Accuracy Contracts

## Summary

This checkpoint captures the approved architecture for making the [[NBA ML Engine]] Backtesting page accuracy-first instead of convenience-first. Its durable lesson is that user-facing backtest claims should be anchored to settled canonical props that match the Props History population, while the broader `predictions × game_logs × prop_lines` population remains useful only as a clearly labeled diagnostic.

The source goes beyond a product note and records the actual contract: the canonical endpoint shape, confidence and edge bucket thresholds, SQL matching logic, failure semantics, and the next implementation steps that were still open at compaction time. For the design tradeoff itself, see [[Canonical Settled Backtests vs Broad Diagnostic Backtests]].

## Key Points

- The session explicitly chose **accuracy and trust first**: headline Backtesting metrics should use settled canonical props rather than the older broad materialized-view population.
- The motivating mismatch was concrete: live `/api/backtest` showed **11,400** broad calls with **53.45%** hit rate and **+786** pseudo-units, while `/api/props/history` showed **4,197** settled canonical bets with **52.82%** hit rate, **+237** flat units, and **-5.9%** Kelly ROI.
- The source treats that discrepancy as a **population problem, not a math bug**: History requires settled snapshots, while the old Backtest page summarized a much wider prediction/game-log population.
- The canonical contract fixes semantics, not just presentation: flat P&L is **+1 unit per hit, -1 per miss**, odds are ignored for that metric, and composite stats such as `pra` are flagged in warnings rather than silently dropped.
- The canonical FastAPI endpoint is `**/evaluation/backtest/canonical**` with `days` constrained to **1-365**, and it reads stored data only rather than triggering inference.
- The matching query uses a `prediction_blend` CTE plus a `ranked_snaps` CTE, with the crucial partition `snap.player_id, snap.game_date, snap.stat_name, snap.source` so sportsbook/source splits are preserved.
- Confidence-score behavior is specified precisely: missing prediction or zero-width uncertainty defaults to **0.5**; otherwise the SQL uses a logistic approximation `1 / (1 + EXP(-1.7 * ABS(predicted - line) / sigma))`.
- Confidence tiers were standardized for downstream consumers: **High >= 0.8**, **Medium >= 0.6**, **Low otherwise**.
- Edge buckets were standardized too: `0-5%`, `5-15%`, `15-30%`, and `30%+`; the BFF still needed a final semantic sort fix because lexicographic sorting produced the wrong order.
- Failure handling is part of the trust contract: canonical fetch failure must surface as **HTTP 502** with an unavailable payload, while broad diagnostic failure is allowed to degrade to `null` because it is secondary evidence, not the headline claim.
- The checkpoint paused with Task 5 still open, but Tasks 1-4 were accepted: canonical contract tests, aggregation service, FastAPI endpoint, and BFF contract helpers were already in place.

## Key Concepts

- [[Canonical Settled-Prop Backtesting for Trustworthy ML Dashboards]]
- [[Broad Diagnostic Backtesting as Secondary Model Evidence]]
- [[Shared Contract Normalization for Dashboard APIs]]
- [[Honest Fallback Metadata and Accuracy Warnings in ML Dashboards]]
- [[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]

## Related Entities

- **[[NBA ML Engine]]** — The production ML system whose Backtesting page, canonical endpoint, and BFF contracts were being redesigned.
- **[[Durable Copilot Session Checkpoint]]** — The artifact class that preserved this partially completed engineering thread as reusable knowledge.
- **[[Copilot CLI]]** — The agent runtime used to design, review, and checkpoint the work.
- **[[FastAPI]]** — The service layer exposing `/evaluation/backtest/canonical`.
- **[[Express.js]]** — The BFF layer responsible for proxying canonical results and attaching broad diagnostics safely.

