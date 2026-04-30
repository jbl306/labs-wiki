---
title: "Source-Tagged Confidence Contracts for ML Dashboards"
type: concept
created: 2026-04-30
last_verified: 2026-04-30
source_hash: "02ef1738c2df2fa90f694299ca6aad3b0a2119bff4c33aee54a4c6b0da5a52b5"
sources:
  - raw/2026-04-25-copilot-session-audit-recommendations-implementation-4d25144f.md
quality_score: 86
concepts:
  - source-tagged-confidence-contracts-ml-dashboards
related:
  - "[[Shared Contract Normalization for Dashboard APIs]]"
  - "[[Honest Fallback Metadata and Accuracy Warnings in ML Dashboards]]"
  - "[[Confidence Calibration Analysis in Machine Learning Models]]"
  - "[[Training-Mode-Aware Rolling Window Metadata]]"
tier: hot
tags: [confidence, api-contracts, dashboard, ml-reliability, provenance, calibration, nba-ml-engine]
---

# Source-Tagged Confidence Contracts for ML Dashboards

## Overview

Source-tagged confidence contracts are an API and UI design pattern for exposing model-confidence signals together with their provenance instead of presenting every score as if it were equally calibrated. In the checkpoint that introduced this pattern, the key correction was to propagate `confidence_source` end-to-end so heuristic confidence, CI-derived confidence, SQL fallback confidence, and truly calibrated confidence remain distinguishable all the way from backend model output to dashboard copy.

## How It Works

The core problem is that a single numeric field named `confidence` often hides multiple computation paths. In the NBA ML checkpoint, the same UI surfaces could receive scores derived from CI width, Platt-style calibration, SQL fallback heuristics, or other fallback paths. If those scores are all rendered with the same label, the dashboard communicates more certainty than the system actually has. A user sees one number; the system knows that number may have come from very different evidence pipelines.

The fix is a contract change rather than a model-only change. The backend response model is extended to carry both the score and its lineage, e.g. `confidence` plus `confidence_source`. That contract is then propagated through every layer that might otherwise collapse distinctions: FastAPI response types, prop finder payloads, canonical backtest detail endpoints, BFF normalization code, frontend API types, and UI components. The important design choice is that provenance is not reconstructed later from guesswork; it is emitted as first-class metadata at the point where the score is produced.

Once provenance is explicit, downstream consumers can apply source-aware policy. The checkpoint documents a particularly important rule: heuristic sources such as `ci_heuristic` and `ci_heuristic_sql` must never be labeled `High`. The tiering function therefore becomes conditional on both the numeric score and the source family. In effect, the tier label becomes:

$$
\text{tier} = f(\text{confidence\_score}, \text{confidence\_source})
$$

instead of the simpler but misleading `tier = f(score)` rule. This prevents a fallback heuristic from receiving the same semantic treatment as a fully calibrated signal merely because the raw number happened to be large.

The UI then aligns language with the new contract. Rather than globally calling the signal “calibrated,” the copy switches to phrasing such as “source-tagged” or “calibrated when available.” That wording matters because it encodes an honest promise to the user: the score is still useful for ranking and triage, but its meaning depends on how it was generated. This is especially important in dashboards where the same page can combine canonical API results with SQL fallbacks or historical records generated under older contracts.

Operationally, source-tagged contracts improve both debugging and trust. When a backtest discrepancy or ranking surprise appears, operators can inspect whether the issue was driven by a calibration path, a heuristic path, or a fallback path. The audit-remediation checkpoint preserved this distinction across current props, history, and canonical backtests, which means downstream analyses can ask a more precise question: “Did the model fail?” versus “Did a heuristic fallback stand in for the model?” Without explicit source tags, those failure modes collapse into one another and become much harder to reason about.

This pattern does not remove uncertainty; it makes uncertainty legible. That is the deeper point. A dashboard becomes more trustworthy not when every score is high quality, but when each score carries enough metadata that operators and users can interpret it correctly.

## Key Properties

- **End-to-end provenance:** `confidence_source` is carried through backend schemas, BFF normalization, frontend types, and user-facing components.
- **Source-aware tiering:** Tier labels depend on both the numeric value and the source family, preventing heuristics from impersonating calibrated confidence.
- **Backward-compatible ranking:** Existing consumers can still sort by a numeric signal, while newer consumers gain interpretability from the source tag.
- **Auditability:** Historical investigations can separate calibration regressions from fallback-path behavior.
- **UX honesty:** Copy such as “calibrated when available” avoids claiming a statistical guarantee the system cannot always provide.

## Limitations

The pattern depends on every producer emitting correct provenance. If one path forgets to set `confidence_source`, the UI can fall back into ambiguity. It also does not solve calibration quality by itself; it only stops poor or heuristic estimates from being mislabeled. Finally, mixed-source dashboards remain cognitively heavier for users, because the system is exposing real heterogeneity instead of smoothing it away.

## Examples

```ts
type PropEdge = {
  confidence: number
  confidence_source:
    | "ci_platt"
    | "ci_heuristic"
    | "ci_heuristic_sql"
    | "classifier_posthoc"
}

function getConfidenceTier(score: number, source: string) {
  if (source.startsWith("ci_heuristic")) return score >= 0.5 ? "Medium" : "Low"
  if (score >= 0.75) return "High"
  if (score >= 0.5) return "Medium"
  return "Low"
}
```

In practice, that means two props with the same numeric score can render differently if one came from a heuristic SQL fallback and the other from a calibrated CI-based path.

## Practical Applications

This pattern is useful anywhere ML products mix multiple score-generation paths: sports-betting dashboards, risk-ranking UIs, fallback-heavy recommendation systems, and analytics products with both online and offline model outputs. It is especially valuable when teams need to preserve degraded-but-useful behavior during incidents without pretending that degraded behavior is equivalent to the primary calibrated path.

## Related Concepts

- **[[Shared Contract Normalization for Dashboard APIs]]** — Provides the BFF and schema-normalization layer that makes confidence provenance survivable across multiple services.
- **[[Honest Fallback Metadata and Accuracy Warnings in ML Dashboards]]** — Generalizes the same idea from confidence scores to other degraded or fallback dashboard states.
- **[[Confidence Calibration Analysis in Machine Learning Models]]** — Explains the statistical side of confidence reliability that this contract exposes rather than obscures.
- **[[Training-Mode-Aware Rolling Window Metadata]]** — Another example of making hidden modeling assumptions explicit in service contracts.

## Sources

- [[Copilot Session Checkpoint: Audit Recommendations Implementation]] — primary source for the end-to-end `confidence_source` contract, heuristic-aware tiering, and UI wording changes.
