---
title: "Shared Canonical Settled-Prop Population for Analytics Consistency"
type: concept
created: 2026-05-31
last_verified: 2026-05-31
source_hash: "4789cd410f350d2cdd568e54d1046ea32d670d8e84f60dd954754b706b61ec98"
sources:
  - raw/2026-05-31-copilot-session-canonical-props-implementation-c9632506.md
quality_score: 88
related:
  - "[[Canonical Settled-Prop Backtesting for Trustworthy ML Dashboards]]"
  - "[[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]"
  - "[[Shared Contract Normalization for Dashboard APIs]]"
  - "[[Source-Priority Canonical Prop Ingestion]]"
tier: hot
tags: [backtesting, calibration, dashboard, canonical-data, sql, data-contracts, nba-ml-engine]
---

# Shared Canonical Settled-Prop Population for Analytics Consistency

## Overview

Shared canonical settled-prop population is the practice of making one explicitly defined settled population the reusable source of truth for every analytics surface that claims to describe realized prop performance. In the [[NBA ML Engine]], this means backtests, calibration, model-health, notifications, materialized views, and dashboard contracts should all reuse the same settled snapshot logic instead of each constructing their own slightly different join.

This matters because analytics drift rarely announces itself as a crash. More often, each query remains locally reasonable while silently counting a different denominator, duplicating rows through join fan-out, or blending mutable current-line state back into what should be settled historical evidence. The checkpoint turns that recurring pain into a durable rule: define the canonical settled population once, then reuse it everywhere.

## How It Works

The raw checkpoint gives a concrete diagnosis of why this pattern became necessary. In the prior 30-day window, the system had **6,080** settled snapshots, **2,238** canonical joined bets, and **4,360** broad materialized-view calls. Those counts are not small rounding differences; they are three different populations telling three different stories about "how many bets do we have?" The same audit also found a calibration join fan-out of **3.80x**, which means one prediction row was being multiplied into several evaluation rows somewhere downstream. That kind of error does not merely add noise. It changes hit rates, calibration curves, confidence buckets, and model-health alarms.

The checkpoint's corrective move is to formalize the canonical grain first. The shared helper in `src/evaluation/canonical_props.py` defines a reusable settled-prop boundary built from immutable `prop_line_snapshots`, not from mutable `prop_lines`. The grain is

$$
g = (\text{player\_id}, \text{game\_date}, \text{stat\_name})
$$

with one settled snapshot selected per grain, carrying its chosen source as metadata rather than letting source multiply the canonical population. The implementation detail matters: source priority still influences which snapshot wins, but `source` is not part of the population identity. That is how the system avoids denominator inflation while preserving descriptive source breakdowns.

Operationally, the helper module creates a shared SQL vocabulary. `CANONICAL_SETTLED_PROPS_CTE` expresses the settled snapshot set. `canonical_settled_props_query(...)` exposes the main query surface. `fetch_canonical_settled_props()` materializes headline backtest evidence. `fetch_canonical_population_count()` provides the count boundary directly. `fetch_canonical_calibration_rows()` gives calibration and model-health consumers the same canonical matching logic instead of forcing each caller to hand-roll a new join. This is a software-design improvement as much as a query fix: shared truth becomes a module, not a convention engineers are expected to remember.

The flow then extends that module across all relevant consumers. In the checkpoint, the backtest endpoint is rewired to `fetch_canonical_settled_props`. Calibration and model-health paths are partially rewired to `fetch_canonical_calibration_rows`. Notification queries begin using the same canonical CTE. `scripts/optimize_db.py` starts migrating materialized views like `mv_daily_hit_rates`, `mv_backtest_summary`, and `mv_clv_daily` away from `predictions × game_logs × prop_lines` joins and toward the settled snapshot boundary. The implementation was not complete at compaction, but the architectural intent is unmistakable: no more independent "almost canonical" populations.

Why is reuse so important? Because the alternative allows each layer to accidentally redefine truth. One query may join through mutable current lines. Another may partition by source and multiply headline rows. Another may average predictions at one grain, then join to settled rows at a finer grain and create fan-out. Another may drop certain stats silently for convenience. Each query can pass local spot checks while still making the dashboard ecosystem incoherent. Shared canonical population turns those differences into explicit design choices that must be encoded once and reused.

The checkpoint also clarifies what this concept is *not*. It is not a claim that every analytics view should have the same coverage. Broader diagnostic populations can still exist. Earlier checkpoints already preserved the value of broad backtests as secondary evidence. The new rule is narrower: when a surface claims to report canonical settled performance, it must use the same settled population as every other canonical surface. Secondary diagnostic populations may differ, but they must be labeled as such rather than masquerading as the headline truth.

There is an important performance and operability dimension too. The checkpoint explicitly says heavy aggregation belongs in shared SQL helpers or materialized views, not in dashboard request-time ad hoc joins. That statement follows naturally from the population contract. Once the canonical grain is known, compute-intensive rollups can be materialized safely because they are anchored to the same underlying population definition. Without that anchor, each precomputed view risks hard-coding a different denominator and making drift harder to detect.

Finally, the concept connects storage truth to API truth. A shared settled population only helps the dashboard if downstream contracts surface it clearly. That is why the checkpoint pairs canonical SQL reuse with explicit metadata and a preference for `NULL` over invented defaults. If a route cannot compute a canonical value, it should say so plainly. Consistent population boundaries and honest contract semantics reinforce each other.

## Key Properties

- **One canonical grain**: one settled row per `player_id / game_date / stat_name`, with source preserved as an attribute rather than treated as a separate identity.
- **Reusable helper surface**: canonical population logic lives in shared functions and CTEs instead of being recopied into each endpoint or materialized view.
- **Fan-out resistance**: consumers avoid accidental duplication by joining through the same pre-defined settled population.
- **Cross-surface consistency**: backtests, calibration, model-health, notifications, and dashboard summaries can report different projections of the same underlying evidence.
- **Explicit diagnostic separation**: broader or more convenient evaluation populations can still exist, but only as clearly labeled secondary evidence.

## Limitations

Shared canonical population narrows coverage relative to broader diagnostic joins, so headline sample sizes can be smaller and may update more slowly. It also depends on correct snapshot identity, settlement logic, and source-priority ranking; if those upstream assumptions are wrong, a perfectly shared population will still be consistently wrong. Finally, a shared helper can become a bottleneck if engineers bypass it during urgent fixes or if its SQL contract changes without updating dependent materialized views and tests together.

## Examples

```sql
WITH ranked_snaps AS (
  SELECT
    snap.*,
    ROW_NUMBER() OVER (
      PARTITION BY snap.player_id, snap.game_date, snap.stat_name
      ORDER BY source_priority, ABS(predicted_value - snap.line)
    ) AS rn
  FROM prop_line_snapshots snap
  JOIN prediction_blend pb
    ON pb.player_id = snap.player_id
   AND pb.game_date = snap.game_date
   AND pb.stat_name = snap.stat_name
  WHERE snap.settled_at IS NOT NULL
)
SELECT *
FROM ranked_snaps
WHERE rn = 1;
```

```python
summary_rows = fetch_canonical_settled_props(days=30)
calibration_rows = fetch_canonical_calibration_rows(days=30)
population_total = fetch_canonical_population_count(days=30)
```

## Practical Applications

This concept is useful in any analytics stack where multiple consumers summarize the same real-world events at different levels. In the [[NBA ML Engine]], it keeps backtesting cards, calibration charts, model-health alerts, notification triggers, and dashboard rollups from quietly disagreeing about the prop universe they are measuring. More generally, any system with both operational dashboards and diagnostic analytics can use a shared canonical population to separate "headline truth" from "broader evidence" without collapsing them into one misleading number.

## Related Concepts

- **[[Canonical Settled-Prop Backtesting for Trustworthy ML Dashboards]]**: that concept defines the trust-first headline backtest contract; this concept generalizes the same population discipline across all analytics consumers.
- **[[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]**: both deal with denominator drift, but this concept turns diagnosis into a reusable prevention pattern.
- **[[Shared Contract Normalization for Dashboard APIs]]**: shared SQL population boundaries become much more trustworthy when the BFF also emits a stable, explicit contract about what population was used.
- **[[Source-Priority Canonical Prop Ingestion]]**: source priority helps choose the best candidate row inside the canonical population, but the population itself must still be shared consistently across downstream surfaces.

## Sources

- [[Copilot Session Checkpoint: Canonical Props Implementation]] — records the settled-population helper, the 3.80x fan-out evidence, and the cross-surface rewiring plan.

