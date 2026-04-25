---
title: "Canonical Settled-Prop Backtesting for Trustworthy ML Dashboards"
type: concept
created: 2026-04-25
last_verified: 2026-04-25
source_hash: "6925ce7a48d728479bbb091c23eb9fd2775349c5187f58544249a5dc6cbc546f"
sources:
  - raw/2026-04-25-copilot-session-backtest-accuracy-contracts-a089eefe.md
quality_score: 87
related:
  - "[[Broad Diagnostic Backtesting as Secondary Model Evidence]]"
  - "[[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]"
  - "[[Shared Contract Normalization for Dashboard APIs]]"
  - "[[Honest Fallback Metadata and Accuracy Warnings in ML Dashboards]]"
  - "[[Canonical Settled Backtests vs Broad Diagnostic Backtests]]"
tier: hot
tags: [backtesting, dashboard, canonical-data, settled-props, ml-ops, trust, api-contracts]
---

# Canonical Settled-Prop Backtesting for Trustworthy ML Dashboards

## Overview

Canonical settled-prop backtesting is a dashboard design pattern in which headline performance claims are computed from the exact population of bets that has actually settled, rather than from a broader convenience population that merely happens to be easy to aggregate. It matters because users interpret a Backtesting page as evidence of realized model quality, so the page should align with the same settlement rules and population boundaries used by the system's historical P&L view.

In the checkpoint, this concept became the governing contract for the Backtesting page: the dashboard would promote settled canonical props to the main view, keep broader model evidence as secondary context, and make the population difference explicit rather than letting two superficially similar hit-rate numbers fight for authority.

## How It Works

The first step is to define the canonical population. In this checkpoint, the canonical set is not "all predictions with enough downstream data to compute an outcome." It is the narrower set of settled prop snapshots that match the same logic users see in Props History. That distinction sounds small, but it changes the semantics of every headline card. If a dashboard says a model hit 53% and made money, the reader reasonably assumes those numbers come from bets that were actually settled under the platform's real matching rules. Canonical settled-prop backtesting enforces exactly that assumption.

Once the population is fixed, the system has to match predictions to the right settled snapshots. The source describes a `prediction_blend` CTE that averages predictions by `player_id`, `game_date`, and `stat_name`, then joins that blended prediction surface to prop-line snapshots in a `ranked_snaps` CTE. The key implementation detail is that the ranking partition includes `snap.source` in addition to player, date, and stat. Without source in the partition, the query silently collapses sportsbook/source splits and corrupts breakdowns such as `by_source`. This is a good example of why a canonical contract is not just a UX choice; it depends on precise relational semantics.

After the matching step, the canonical service computes outcome metrics that are simple enough to be auditable. The flat P&L rule is intentionally plain:

$$
\text{flat\_pnl} = \text{wins} - \text{losses}
$$

with each hit contributing `+1` unit and each miss contributing `-1` unit. Odds are ignored for this particular metric so the dashboard can show a settlement-aligned directional score without mixing in staking assumptions. Hit rate is the equally direct

$$
\text{hit\_rate} = \frac{\text{wins}}{\text{settled\_bets}}
$$

which makes the population denominator explicit.

The checkpoint also turns confidence from an ad hoc UI label into a stable contract surface. Missing predictions or degenerate uncertainty intervals default to `0.5`, while ordinary rows use a logistic approximation based on distance from the line and uncertainty width:

$$
\text{confidence} = \frac{1}{1 + e^{-1.7 \cdot \lvert \text{predicted} - \text{line} \rvert / \sigma}}
$$

This matters because the canonical endpoint does not merely return summary cards; it supports grouped reliability views such as `by_stat`, `by_confidence_tier`, `by_direction`, `by_source`, and `by_edge_size`. Thresholds become part of the durable interface: High means `>= 0.8`, Medium means `>= 0.6`, and Low means everything below that.

The design also encodes what not to over-clean. Composite stats such as `pra` were recognized as noisier and therefore flagged in warnings and `population.excluded_stats`, but the contract deliberately did **not** remove them from headline metrics or details in this pass. That is a subtle but important design discipline. Canonical settled-prop backtesting is about aligning the displayed population to a truthful operational definition; it is not a license to curate away inconvenient rows until the metric looks cleaner. If product policy later decides to exclude composites, that should be an explicit policy change, not an invisible contract mutation.

Another major part of the concept is failure semantics. In the BFF, canonical data is not optional. If the canonical FastAPI request fails, the route should return HTTP `502` with an unavailable payload rather than a fake success shell. Broad diagnostics may degrade to `null`, but headline evidence should fail loudly because a trust-oriented contract values epistemic honesty over cosmetic continuity. This connects canonical backtesting to [[Honest Fallback Metadata and Accuracy Warnings in ML Dashboards]]: reliability claims are only meaningful if degraded states are surfaced truthfully.

Finally, the concept changes how a team interprets discrepancies. Before this architecture, the natural instinct was to ask why `/api/backtest` and `/api/props/history` disagreed. After the architecture, the more useful question becomes whether the headline dashboard is attached to the correct population in the first place. That shift turns a recurrent debugging problem into a product contract. The Backtesting page stops competing with the History page and instead becomes its aligned analytical companion.

## Key Properties

- **Population fidelity**: Headline metrics are computed from settled snapshots that match realized historical outcomes, not from a broader proxy population.
- **Contracted thresholds**: Confidence tiers (`>= 0.8`, `>= 0.6`, else low) and edge buckets (`0-5%`, `5-15%`, `15-30%`, `30%+`) are fixed parts of the interface.
- **Source-preserving matching**: Snapshot ranking partitions by `snap.source` so sportsbook/source splits remain truthful in grouped views.
- **Auditable metrics**: Flat P&L and hit rate use simple, inspectable formulas rather than opaque blended outcome scores.
- **Honest failure mode**: Canonical fetch failure is treated as a route failure, not as empty success data.

## Limitations

Canonical settled-prop backtesting reduces ambiguity, but it does not remove every judgment call. Matching settled snapshots to prediction surfaces still depends on SQL ranking logic, and small partition mistakes can distort breakdowns without obviously breaking totals. The approach also narrows the available population, so headline samples may be smaller and move more slowly than broader diagnostics. Finally, settlement-aligned metrics say more about realized user-facing evidence than about model capacity in the abstract; teams still need separate diagnostic views for broader model analysis.

## Examples

A simplified payload contract looks like this:

```json
{
  "status": "ok",
  "summary": {
    "total_bets": 4197,
    "hit_rate": 0.5282,
    "flat_pnl": 237
  },
  "population": {
    "source_label": "settled canonical props",
    "excluded_stats": ["pra"]
  },
  "breakdowns": {
    "by_confidence_tier": [
      {"tier": "High", "total_bets": 812, "hit_rate": 0.5517}
    ]
  }
}
```

The key idea is not the exact field names. It is that every headline number is explicitly tied to a settled, named population rather than a vague "backtest" bucket.

## Practical Applications

This concept is valuable for decision-support dashboards where users could mistake broad evaluation data for realized performance evidence. In the [[NBA ML Engine]], it makes the Backtesting page trustworthy by aligning it with Props History instead of letting a looser materialized-view summary dominate the narrative. More generally, any ML product that mixes historical settlement, model diagnostics, and user-facing performance claims can use this pattern to separate "what actually settled" from "what the model did more broadly."

## Related Concepts

- **[[Broad Diagnostic Backtesting as Secondary Model Evidence]]**: Broad diagnostics remain useful, but only after the canonical settled population has taken over the headline trust surface.
- **[[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]**: That concept explains why metric populations drift; this concept turns the resolution into a durable contract.
- **[[Shared Contract Normalization for Dashboard APIs]]**: Canonical backtesting only works cleanly when the BFF and frontend share one stable response shape.
- **[[Honest Fallback Metadata and Accuracy Warnings in ML Dashboards]]**: Canonical evidence must fail honestly when unavailable rather than degrading into misleading success payloads.
- **[[Walk-Forward Stability Analysis and Backtesting in NBA ML Engine]]**: Walk-forward evaluation studies temporal robustness, while canonical settled-prop backtesting studies realized, user-facing settlement outcomes.

## Sources

- [[Copilot Session Checkpoint: Backtest Accuracy Contracts]] — defines the canonical endpoint, thresholds, matching logic, and trust-first presentation rule.

