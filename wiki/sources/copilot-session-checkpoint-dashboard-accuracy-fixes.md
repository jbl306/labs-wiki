---
title: "Copilot Session Checkpoint: Dashboard Accuracy Fixes"
type: source
created: '2026-04-25'
last_verified: '2026-04-25'
source_hash: 664cba87ef6621c1f63044b989fa00f476930abd1aab2bee1fcf33d463fce646
sources:
  - raw/2026-04-25-copilot-session-dashboard-accuracy-fixes-3717a5b2.md
concepts:
  - shared-contract-normalization-dashboard-apis
  - honest-fallback-metadata-accuracy-warnings-ml-dashboards
related:
  - "[[NBA ML Engine]]"
  - "[[Copilot CLI]]"
  - "[[Durable Copilot Session Checkpoint]]"
  - "[[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]]"
  - "[[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]"
tags: [copilot-session, checkpoint, nba-ml-engine, dashboard, bff, api-contracts, data-quality, reliability]
tier: hot
checkpoint_class: durable-workflow
retention_mode: retain
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 78
---

# Copilot Session Checkpoint: Dashboard Accuracy Fixes

## Summary

This checkpoint captures a mid-implementation repair pass on the [[NBA ML Engine]] dashboard after a live audit found broken accuracy signals across overview predictions, props, and production-model R² charts. The durable lesson is not just that several bugs existed, but that the fix centered on unifying contracts across the Express BFF, the FastAPI service, and the React frontend while surfacing honest provenance and warning metadata instead of silently returning misleading empty states.

## Key Points

- A live audit found three distinct trust failures at once: `/api/dashboard` showed featured predictions and prop counts, `/api/props` returned empty arrays for the same slate, and `/api/models` returned nested `metrics.test_r2` values that the frontend expected at top level.
- The implementation introduced a shared helper module, `dashboard-ui/server/src/dashboardContracts.ts`, to normalize model records, normalize FastAPI prop-edge rows, build props payloads, and centralize confidence-tier behavior.
- `normalizeModelRecord(raw)` flattened nested metrics such as `metrics.test_r2`, `metrics.val_r2`, `metrics.val_mae`, and `metrics.test_mae`, while also deriving `stat_name` and `model_family` from names like `EnsembleModel_fg3m`.
- `normalizeFastApiPropEdge(raw, resolvedDate)` mapped backend fields like `stat`, `predicted`, `edge`, and `confidence` into frontend-oriented fields such as `stat_name`, `predicted_value`, `edge_pct`, `confidence_score`, `edge_abs`, `call`, and `direction`.
- The BFF stopped maintaining separate prop-pick logic per route and instead reused `getPropPicksForSlate()` for `/api/dashboard`, `/api/props`, and `/api/rankings`, reducing cross-endpoint drift.
- The new shared flow explicitly labeled provenance with `prop_data_source` / `data_source` and `empty_reason`, allowing the UI to distinguish canonical FastAPI results from `bff_sql_fallback` output.
- User-facing copy was adjusted from “Confidence” to “Model Signal,” acknowledging that the score is a model-derived ranking signal rather than a literal calibrated probability.
- The dashboard added `accuracy_warnings` so degraded calibration and stale or incomplete upstream data become visible to users instead of hiding behind polished UI surfaces.
- The checkpoint preserved concrete audit evidence: high-confidence props were only 48.86% accurate, below medium-confidence props at 52.95%; `/api/evaluation/calibration` returned ECE 0.3661; `/api/evaluation/model-health` showed ECE 0.4055 and 21 drifted features.
- Verification at this stage was intentionally scoped: focused contract tests passed and the dashboard build passed, but lint remained dirty because of baseline repo issues plus one touched-file escape-character fix and one touched-area `prefer-const` cleanup.

## Key Concepts

- [[Shared Contract Normalization for Dashboard APIs]]
- [[Honest Fallback Metadata and Accuracy Warnings in ML Dashboards]]
- [[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]]
- [[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]

## Related Entities

- **[[NBA ML Engine]]** — The ML system whose dashboard contracts, props feeds, and model-metric displays were being repaired.
- **[[Copilot CLI]]** — The agent runtime used to audit the live endpoints, create the worktree, implement fixes, and preserve the checkpoint as durable knowledge.
- **[[Durable Copilot Session Checkpoint]]** — The artifact class this export belongs to: a retained, ingestable snapshot of an in-progress Copilot repair workflow.
- **[[Express.js]]** — The BFF layer where shared contract helpers and route-level normalization were added.
- **[[FastAPI]]** — The upstream API whose prop-edge responses were normalized and reused through a common BFF contract path.
