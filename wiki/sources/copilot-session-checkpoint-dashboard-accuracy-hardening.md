---
title: "Copilot Session Checkpoint: Dashboard Accuracy Hardening"
type: source
created: '2026-04-25'
last_verified: '2026-04-25'
source_hash: 6caf80ac3afa85f4adf295e7c39d6eeba187acacd73f68dd65fc123c58576db1
sources:
  - raw/2026-04-25-copilot-session-dashboard-accuracy-hardening-404bc17e.md
concepts:
  - serving-signal-aligned-calibration-reporting
  - reference-safe-artifact-pruning-shared-model-registries
  - freshness-gate-alignment-between-ml-apis-and-dashboards
  - shared-contract-normalization-dashboard-apis
  - honest-fallback-metadata-accuracy-warnings-ml-dashboards
related:
  - "[[Copilot Session Checkpoint: Dashboard Accuracy Fixes]]"
  - "[[Copilot Session Checkpoint: Dashboard Accuracy Finalization]]"
  - "[[NBA ML Engine]]"
  - "[[NBA-ML Model Registry]]"
  - "[[Durable Copilot Session Checkpoint]]"
  - "[[Copilot CLI]]"
  - "[[Homelab]]"
  - "[[MemPalace]]"
tags: [copilot-session, checkpoint, nba-ml-engine, dashboard, model-calibration, artifact-registry, freshness, homelab]
tier: hot
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 79
---

# Copilot Session Checkpoint: Dashboard Accuracy Hardening

## Summary

This checkpoint captures the final hardening pass that turned the earlier dashboard-accuracy repair campaign into a mostly trustworthy production state for the [[NBA ML Engine]]. The durable lessons are that dashboard trust required three deeper alignments after the earlier contract/provenance work: calibration endpoints had to measure the same score actually used for prop serving, registry pruning had to stop deleting shared artifacts still referenced by kept rows, and dashboard freshness warnings had to match the backend's one-day lag policy.

## Key Points

- The checkpoint closes a multi-pass campaign that started with broken dashboard trust signals, moved through contract normalization and provenance fixes, and ended by focusing on the remaining live blockers: calibration mismatch, registry artifact drift, and freshness-warning drift.
- The final work stayed isolated in `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final` on branch `feature/dashboard-accuracy-final`, explicitly avoiding a dirty main checkout.
- Public calibration had been misleading because `/evaluation/calibration` measured a raw edge ratio while prop filtering used a served confidence signal built from CI width, CI Platt calibration, and optional post-hoc calibration.
- The hardening pass added `compute_ci_z_scores()` and `compute_serving_confidence_scores()`, updated `/evaluation/calibration` and `/evaluation/calibration-by-stat` to use the served signal, and exposed raw-edge ECE separately so operators could still see the old discrepancy.
- A sparse-bin bug in `compute_calibration()` was fixed: `sklearn.calibration_curve()` only returns populated bins, so pairing those values with the first `N` bin edges could incorrectly report zero counts and zero ECE for middle-only probability mass.
- Model-health alerting was aligned with serving semantics too: `src/notifications/dispatcher.py` now evaluates ECE and OOS ECE on the same served score source and records `ece_score_source` metadata.
- Registry health uncovered a subtler lifecycle bug: `model_registry` rows could share unversioned artifact paths, so pruning an older row could delete a file still referenced by a kept or production row.
- `prune_old_models()` was hardened with `_delete_artifact_if_unreferenced()`, and missing production artifacts were rebuilt through normal training flows rather than manual copying or DB edits.
- The final live state was materially better: `registry-health` reported `missing_count=0`, public served-score calibration dropped to `expected_calibration_error=0.0215`, raw-edge ECE remained visible at `0.3653`, and dashboard warnings no longer falsely flagged a one-day game-log lag as stale.
- Live dashboard checks showed `featured_date=2026-04-25`, `best_predictions=10`, `/api/props=340` from `fastapi_prop_edges`, 8 chartable production models, and only one remaining warning: legitimate degraded model health driven by hit-rate, feature-importance instability, and drift alerts.
- Validation was substantial rather than cosmetic: targeted Python suites passed (`39 passed`), dashboard contract tests passed (`8 passed`), and the final local commit `92cdb88 fix: finish dashboard accuracy hardening` was created but not yet pushed at compaction time.

## Key Concepts

- [[Serving-Signal-Aligned Calibration Reporting]]
- [[Reference-Safe Artifact Pruning in Shared Model Registries]]
- [[Freshness-Gate Alignment Between ML APIs and Dashboards]]
- [[Shared Contract Normalization for Dashboard APIs]]
- [[Honest Fallback Metadata and Accuracy Warnings in ML Dashboards]]
- [[Artifact Registry Validation In ML Pipelines]]

## Related Entities

- **[[NBA ML Engine]]** — The production ML system whose calibration, registry integrity, and dashboard trust signals were hardened.
- **[[NBA-ML Model Registry]]** — The registry whose shared artifact paths created the hidden prune/delete failure mode.
- **[[Copilot CLI]]** — The agent runtime used to audit live endpoints, manage worktrees, apply fixes, and preserve the session as durable knowledge.
- **[[Durable Copilot Session Checkpoint]]** — The artifact class that turned a long, interruptible engineering thread into an ingestible memory object.
- **[[Homelab]]** — The deployment environment hosting the `nba-ml-api` and `nba-ml-dashboard` containers and the compose workflow that needed correct `.env` loading.
- **[[MemPalace]]** — The memory system used to recover prior context and maintain continuity across the repair passes.
