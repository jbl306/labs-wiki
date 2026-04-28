---
title: "Broad Diagnostic Backtesting as Secondary Model Evidence"
type: concept
created: 2026-04-25
last_verified: 2026-04-25
source_hash: "6925ce7a48d728479bbb091c23eb9fd2775349c5187f58544249a5dc6cbc546f"
sources:
  - raw/2026-04-25-copilot-session-backtest-accuracy-contracts-a089eefe.md
quality_score: 65
related:
  - "[[Canonical Settled-Prop Backtesting for Trustworthy ML Dashboards]]"
  - "[[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]"
  - "[[Walk-Forward Stability Analysis and Backtesting in NBA ML Engine]]"
  - "[[Canonical Settled Backtests vs Broad Diagnostic Backtests]]"
tier: hot
tags: [backtesting, diagnostics, dashboard, model-evaluation, ml-ops, data-provenance, trust]
---

# Broad Diagnostic Backtesting as Secondary Model Evidence

## Overview

Broad diagnostic backtesting is the practice of evaluating a model on a wider population than the one used for user-facing realized performance claims, then presenting that wider result as diagnostic context instead of headline truth. It matters because engineering teams still need high-coverage model evidence, but dashboards become misleading when they present that broader evidence as though it were directly comparable to settled historical betting outcomes.

In the checkpoint, the old Backtesting page summarized a broad `predictions × game_logs × prop_lines` population. The architecture change did not declare that broad view useless; it reclassified it as a secondary diagnostic that should remain visible, but only with explicit labeling and caveats.

## How It Works

The starting point is to acknowledge that broad diagnostic populations answer a different question from settled canonical populations. A broad backtest asks something like, "Across a large universe of predictions for which we can assemble lines and outcomes, how did the model tend to behave?" That is valuable for coverage analysis, strategy exploration, and rapid monitoring because the population is large and the computation path is often pre-aggregated in a materialized view. In the source, this broader view produced **11,400** calls, far more than the **4,197** settled canonical bets available in the history-aligned population.

Mathematically, you can think of the relationship as a set inclusion problem. Let $C$ be the canonical settled population and $B$ be the broad diagnostic population. In many production systems,

$$
C \subset B
$$

or at least $C$ is a strict, more policy-constrained subset of the data universe that the diagnostic system can summarize. The danger appears when a dashboard reports a statistic over $B$ as though it described $C$. The metrics may be numerically close, but the interpretation changes because the denominator, matching rules, and settlement assumptions changed.

The broad diagnostic route in the checkpoint remained useful precisely because it was broad. It could summarize the larger model universe quickly through `mv_backtest_summary`, keep counts such as `SUM(total_calls)` available for quick diagnostics, and provide a wider-angle view of behavior by day, stat, or edge bucket. That breadth makes it good for answering operational questions such as whether a model family is drifting, whether edge distributions are skewing, or whether a route is still producing a healthy volume of opportunities. These are important engineering questions even if they are not the right substrate for the main trust claim shown to users.

Because the broad population is not authoritative for realized performance, the interface contract has to downgrade its epistemic status. The source's rule is clear: broad diagnostics stay on the page, but they live below the canonical summary and are labeled as a wider model diagnostic not directly comparable to Props History. This is a strong pattern because it preserves useful evidence instead of throwing it away while still protecting the headline interpretation. The dashboard teaches the user how to read the numbers instead of assuming they will infer the caveat on their own.

Another important part of the concept is graceful degradation. In the BFF, broad diagnostic failure is explicitly allowed to return `null` while canonical failure is not. That asymmetry tells you the intended role of the broad layer. If a secondary diagnostic disappears temporarily, the dashboard can remain truthful with canonical evidence intact. If the broad diagnostic were the main trust surface, such degradation would be much harder to justify. The failure policy therefore encodes product hierarchy: secondary evidence may be absent; primary evidence may not be silently faked.

The source also surfaces a subtler implementation lesson: even secondary diagnostics still deserve careful semantics. The broad layer needed a fix for semantic ordering of `by_edge_size` buckets because lexicographic sorting produced `0-5%`, `15-30%`, `30%+`, `5-15%`. That bug would not necessarily destroy the main trust claim, but it would still mislead users reading the diagnostic section. Secondary does not mean sloppy; it means the evidence is contextual rather than authoritative.

Finally, broad diagnostics help teams retain model-development visibility that a strict canonical view can hide. A smaller settled population may understate coverage changes or delay the appearance of shifts in model behavior. The broad layer can reveal those patterns sooner, especially when it is backed by a materialized summary. The right design move is therefore not to choose one population and delete the other, but to preserve both while making their roles unmistakable.

## Key Properties

- **High coverage**: Broad diagnostics summarize a larger prediction/outcome universe than settled canonical views.
- **Secondary status**: The results are presented as contextual model evidence, not as the main realized-performance claim.
- **Operational usefulness**: Materialized views and aggregate counts make the layer effective for quick health and coverage checks.
- **Interpretive caveats**: The UI must label the population clearly because the numbers are not directly comparable to settlement-aligned history.
- **Graceful optionality**: Broad diagnostic failure can degrade to `null` without invalidating the whole page.

## Limitations

Broad diagnostic backtesting is easy to overread. Its larger sample can look more stable or more flattering than the canonical population, tempting teams to treat it as the "real" answer because it is numerically richer. It also depends heavily on how the materialized view or aggregation logic is defined; if the population logic drifts, the diagnostic can become semantically stale even while still computing successfully. Finally, once a diagnostic layer exists, product teams may feel pressure to simplify the UI by merging it into the headline view, which recreates the original trust problem.

## Examples

```typescript
type BacktestPayload = {
  canonical: CanonicalBacktestPayload | null
  broadDiagnostic: {
    total_calls: number
    hit_rate: number
    units: number
    label: "Broad model diagnostic"
  } | null
}

const isComparableToHistory = false
```

This pattern keeps the diagnostic data available while refusing to imply that it is the same thing as settled historical performance.

## Practical Applications

This concept is useful in ML systems that need both user-facing trust surfaces and higher-coverage engineering diagnostics. In the [[NBA ML Engine]], it preserves the old broad backtest as a monitoring aid even after canonical settled props take over the main dashboard story. More generally, any analytics product that mixes settled outcomes, inferred coverage, and pre-aggregated monitoring data can use this design to avoid deleting useful evidence while still protecting interpretation.

## Related Concepts

- **[[Canonical Settled-Prop Backtesting for Trustworthy ML Dashboards]]**: Canonical settled props should be the headline layer; broad diagnostics belong underneath as contextual evidence.
- **[[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]**: That concept explains why broad and canonical views diverge in the first place.
- **[[Walk-Forward Stability Analysis and Backtesting in NBA ML Engine]]**: Walk-forward analysis studies temporal robustness, whereas broad diagnostics summarize a larger operational population for monitoring and comparison.
- **[[Honest Fallback Metadata and Accuracy Warnings in ML Dashboards]]**: Clear labels and optional secondary degradation keep the diagnostic layer honest.

## Sources

- [[Copilot Session Checkpoint: Backtest Accuracy Contracts]] — reclassifies the broad backtest from misleading headline metric to labeled secondary diagnostic.

