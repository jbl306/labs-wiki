---
title: "Canonical Settled Backtests vs Broad Diagnostic Backtests"
type: synthesis
created: 2026-04-25
last_verified: 2026-04-25
source_hash: "synthesis-generated"
sources:
  - raw/2026-04-25-copilot-session-backtest-completion-props-investigation-ed8d6cc6.md
  - raw/2026-04-25-copilot-session-backtest-accuracy-contracts-a089eefe.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-pipeline-resilience-fixes-dashboard-metrics-inve-3ea0d6d8.md
concepts:
  - canonical-settled-prop-backtesting-trustworthy-ml-dashboards
  - broad-diagnostic-backtesting-secondary-model-evidence
  - dashboard-metrics-consistency-and-hit-rate-discrepancy-analysis
related:
  - "[[Canonical Settled-Prop Backtesting for Trustworthy ML Dashboards]]"
  - "[[Broad Diagnostic Backtesting as Secondary Model Evidence]]"
  - "[[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]"
tier: hot
tags: [backtesting, dashboard, trust, canonical-data, diagnostics, ml-ops]
quality_score: 91
---

# Canonical Settled Backtests vs Broad Diagnostic Backtests

## Question

When an ML dashboard has both a settlement-aligned backtest population and a broader diagnostic population, which one should carry the headline trust claim and how should the other be presented?

## Summary

Use canonical settled backtests for the headline claim whenever the page is supposed to represent realized user-facing performance. Keep the broader backtest only as a secondary diagnostic, clearly labeled as non-comparable contextual evidence; otherwise the dashboard turns a legitimate population difference into a recurring trust failure.

## Comparison

| Dimension | [[Canonical Settled-Prop Backtesting for Trustworthy ML Dashboards]] | [[Broad Diagnostic Backtesting as Secondary Model Evidence]] |
|-----------|-----------------------------------------------------------------------|---------------------------------------------------------------|
| Primary question answered | What happened on the settled bets users should treat as realized evidence? | What does the larger prediction universe say about model behavior and coverage? |
| Population basis | Settlement-aligned, history-comparable prop snapshots | Wider `predictions × game_logs × prop_lines` style population |
| Sample size tendency | Smaller, slower-moving, stricter | Larger, faster, operationally convenient |
| Trust role on dashboard | Headline cards and primary narrative | Secondary section with caveats and labels |
| Failure semantics | Should fail loudly if unavailable | Can degrade to `null` without invalidating the whole page |
| Main risk | Underpowered sample or delayed signals | Misleading users if presented as realized performance |

## Analysis

The core trade-off is not "accurate versus inaccurate." Both populations can be computed correctly. The real distinction is whether the number supports the interpretation the dashboard invites. A headline Backtesting card is usually read as a realized-performance statement, so it should be attached to the settled canonical population. If it is attached to a broader convenience population instead, the dashboard asks users to make a semantic leap they have no reason to notice.

The later completion checkpoint strengthens that conclusion with a practical implementation lesson: even after the product contract is correct, the canonical layer can still be wrong if its SQL grain is wrong. In that session, the first canonical implementation accidentally counted one row per sportsbook source and doubled the headline population to 8,394. Only after the ranking partition was changed to one row per `player/date/stat` did the canonical totals reconcile to Props History at 4,197. That result reinforces the synthesis: the canonical layer deserves headline status precisely because teams are willing to do the extra work to make its semantics exact.

Broad diagnostics still matter because the canonical population is not optimized for engineering visibility. A materialized diagnostic view can surface many more calls, coverage changes, and shape changes in the model's opportunity distribution. That is useful for operators and for feature work. The mistake is not keeping the broad layer; the mistake is letting it speak in the same voice as the canonical layer. Once both are visible but hierarchically labeled, the product retains operational richness without sacrificing interpretive honesty.

[[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]] provides the bridge between these two modes. It explains why teams often discover a disagreement before they discover the architectural lesson: one endpoint uses settled props and another uses a larger population, so the numbers diverge even when both are valid. The synthesis here turns that investigative finding into a design rule. Instead of repeatedly explaining the mismatch after the fact, the dashboard can prevent misreading up front.

Another reason to separate the layers is failure handling. If canonical data is missing, the page should tell the truth and treat the result as unavailable. If the broad diagnostic is missing, the primary trust surface can still stand. That asymmetry encodes product intent directly in the route behavior. A system that hides canonical failure behind broad fallback data might preserve continuity, but it destroys the meaning of the headline metric.

The practical design choice is therefore hierarchical duality: canonical settled evidence first, broad diagnostic evidence second. This is a better pattern than forcing a false unification and better than deleting the broad layer entirely. It preserves both truth and useful context.

## Key Insights

1. **Population correctness is not enough; interpretation correctness matters too.** — supported by [[Canonical Settled-Prop Backtesting for Trustworthy ML Dashboards]], [[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]
2. **Broad diagnostics are valuable when they are demoted from headline truth to contextual evidence.** — supported by [[Broad Diagnostic Backtesting as Secondary Model Evidence]]
3. **A recurring discrepancy investigation can usually be converted into a durable product contract.** — supported by [[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]], [[Canonical Settled-Prop Backtesting for Trustworthy ML Dashboards]]
4. **Failure policy is part of trust design: primary evidence must fail honestly, while secondary evidence may degrade gracefully.** — supported by [[Canonical Settled-Prop Backtesting for Trustworthy ML Dashboards]], [[Broad Diagnostic Backtesting as Secondary Model Evidence]]

## Open Questions

- When should a canonical population intentionally exclude noisy composite stats such as `pra`, and how should that policy change be disclosed?
- How much of the population explanation can be encoded directly in route metadata so future dashboards do not require ad hoc forensic analysis?
- What is the best user-facing visualization for showing that canonical and broad populations are related but not directly comparable?

## Sources

- [[Copilot Session Checkpoint: Backtest Accuracy Contracts]]
- [[Copilot Session Checkpoint: Pipeline Resilience Fixes, Dashboard Metrics Investigation]]
- [[Copilot Session Checkpoint: Backtest Completion Props Investigation]]
