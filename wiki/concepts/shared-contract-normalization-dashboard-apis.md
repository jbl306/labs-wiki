---
title: "Shared Contract Normalization for Dashboard APIs"
type: concept
created: 2026-04-25
last_verified: 2026-04-25
source_hash: "664cba87ef6621c1f63044b989fa00f476930abd1aab2bee1fcf33d463fce646"
sources:
  - raw/2026-04-25-copilot-session-dashboard-accuracy-fixes-3717a5b2.md
quality_score: 65
related:
  - "[[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]]"
  - "[[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]"
  - "[[Honest Fallback Metadata and Accuracy Warnings in ML Dashboards]]"
tier: hot
tags: [dashboard, api-contracts, bff, normalization, typescript, fastapi, express, data-quality]
---

# Shared Contract Normalization for Dashboard APIs

## Overview

Shared contract normalization is the practice of defining one canonical transformation layer between heterogeneous backend responses and the frontend data model that actually drives the UI. It matters because dashboards frequently fail not when the data is absent, but when structurally valid data arrives in a shape that nearby components interpret differently, creating empty widgets, blank charts, or silently inconsistent metrics.

## How It Works

The checkpoint shows a classic multi-service dashboard failure mode: several endpoints were returning “good enough” data for their own layer, but not for the system as a whole. The React frontend expected production model metrics such as `test_r2`, `val_r2`, and `stat_name` to be top-level fields. The BFF and upstream API, however, were handing back records where some of those values lived under nested `metrics` objects or under backend-oriented names like `stat`, `predicted`, and `confidence`. Each endpoint had slowly accumulated its own assumptions, so the dashboard could simultaneously display featured predictions, return empty props, and render broken model-comparison charts.

The normalization fix was to stop letting each route improvise its own shape conversions. Instead, the BFF introduced a shared helper module, `dashboard-ui/server/src/dashboardContracts.ts`, and moved data shaping into named, reusable functions. That module became the contract boundary between upstream sources and the frontend. Rather than treating normalization as an afterthought near `res.json(...)`, the code treated it as the main unit of correctness.

One part of that layer handled model metrics. `normalizeModelRecord(raw)` took records whose important values were buried under `metrics.val_r2`, `metrics.test_r2`, `metrics.val_mae`, and similar nested keys, then flattened them into the top-level fields the UI already used. It also derived semantic identifiers like `stat_name` and `model_family` from strings such as `EnsembleModel_fg3m`. This is a crucial detail: contract normalization is not only about renaming keys; it is also about recovering implicit structure that the UI needs in explicit, typed form.

Another part handled prop-edge payloads. The upstream FastAPI response used domain-specific fields like `stat`, `predicted`, `edge`, and `confidence`. The frontend, however, rendered tables and badges using keys such as `stat_name`, `predicted_value`, `edge_pct`, `confidence_score`, `edge_abs`, `call`, and `direction`. `normalizeFastApiPropEdge(raw, resolvedDate)` created a canonical record shape so the rest of the BFF and frontend no longer had to know whether the row came from FastAPI or a fallback SQL query.

This pattern reduces semantic drift across routes. Before the fix, `/api/dashboard`, `/api/props`, and `/api/rankings` each had partially overlapping prop-pick logic. When those branches diverged, one view could show a non-empty slate while another returned an empty success response for the same date. The fix centralized retrieval through `getPropPicksForSlate()`, then passed results through shared normalization and shared payload-building logic. That means the system now has one place to decide what a prop record is, one place to decide how route responses are shaped, and one place to decide what metadata accompanies those payloads.

The deeper lesson is that contract normalization should sit close to the system boundary, not inside individual React components. If every page compensates for backend variability on its own, the result is a hidden mesh of local adapters. Those adapters are hard to test because the “real” contract is scattered across components, and they are hard to evolve because each page now depends on quirks of upstream responses. A dedicated contract module converts that accidental complexity into an explicit API surface.

This also improves testing strategy. The checkpoint did not merely add helpers; it added focused contract tests first in `dashboardContracts.test.ts`. That test suite covered metric flattening, prop-edge normalization, payload metadata, and confidence-tier boundaries. Testing the transformations directly is much more robust than waiting for a build or manual dashboard inspection to reveal that a nested field moved or a nullable value broke a chart.

There is a useful systems design intuition here: normalization trades local convenience for global consistency. A route author loses the ability to tweak one endpoint ad hoc, but the system gains a stable internal schema. In practice, this lowers the cost of adding new views because future pages consume the normalized shape instead of reverse-engineering upstream payloads from scratch.

Mathematically, you can think of the pattern as a composition of total functions over partially structured inputs. If an upstream record is $r$ and the canonical frontend record is $c$, the goal is to make each route compute

$$
c = N(r)
$$

instead of many route-specific variants $N_1(r), N_2(r), N_3(r)$ that are only approximately equivalent. When those route-specific functions diverge, consistency errors emerge even if each route is “mostly correct.”

The trade-off is obvious: the BFF becomes more responsible for type discipline and domain mapping. But for a multi-endpoint dashboard, that is a feature rather than a bug. The contract layer becomes the place where structural truth is asserted, tested, and documented.

## Key Properties

- **Canonical record shape**: One helper layer defines the frontend-oriented fields for models and props so routes no longer invent slightly different payloads.
- **Semantic derivation**: Normalization can recover missing structure, such as deriving `stat_name` or `model_family` from model identifiers.
- **Route convergence**: Shared retrieval plus shared shaping prevents `/api/dashboard`, `/api/props`, and `/api/rankings` from disagreeing about the same slate.
- **Testable transformations**: Small contract helpers are easy to unit test directly with targeted fixtures and boundary cases.
- **Boundary ownership**: The BFF becomes the explicit place where upstream API and SQL outputs are translated into UI contracts.

## Limitations

Shared normalization does not solve underlying data-quality problems by itself. If upstream services emit stale, wrong, or semantically misleading values, the contract layer can standardize their shape without fixing their meaning. It also creates a maintenance burden: once a contract module exists, every schema change should update the helpers and tests together. Finally, a canonical shape can become too frontend-specific if not designed carefully, making it harder to support multiple consumers with different needs.

## Examples

A simplified version of the checkpoint’s pattern looks like this:

```typescript
type RawModel = {
  model_name: string
  metrics?: {
    test_r2?: number | null
    val_r2?: number | null
  }
}

type NormalizedModel = {
  model_name: string
  model_family: string
  stat_name: string
  test_r2: number | null
  val_r2: number | null
}

function normalizeModelRecord(raw: RawModel): NormalizedModel {
  const [modelFamily, statName] = raw.model_name.split("_", 2)
  return {
    model_name: raw.model_name,
    model_family: modelFamily,
    stat_name: statName,
    test_r2: raw.metrics?.test_r2 ?? null,
    val_r2: raw.metrics?.val_r2 ?? null,
  }
}
```

The important part is not the syntax; it is the discipline that every route now emits `NormalizedModel`, not whichever subset happens to be convenient.

## Practical Applications

This concept is valuable anywhere a dashboard consumes data from multiple backends, especially when one layer proxies an API while another queries a database directly. It is particularly useful for ML dashboards, observability tools, and internal admin panels where field names, nesting, and nullability drift over time. In the labs-wiki workspace, it is a durable pattern for future `[[NBA ML Engine]]` dashboard work: repair the contract once at the BFF boundary, test it there, and let frontend pages stay simple.

## Related Concepts

- **[[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]]**: Shared normalization is a concrete implementation discipline within a BFF.
- **[[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]**: Both focus on trust, but this concept addresses structural contract drift while that one addresses metric-population drift.
- **[[Honest Fallback Metadata and Accuracy Warnings in ML Dashboards]]**: Normalized payloads become more valuable when they also carry truthful provenance and warning fields.

## Sources

- [[Copilot Session Checkpoint: Dashboard Accuracy Fixes]] — documents the creation of `dashboardContracts.ts`, shared normalization helpers, and contract tests.
