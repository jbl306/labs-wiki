---
title: "Audit Remediation Patterns for NBA ML Integrity"
type: synthesis
created: 2026-04-30
last_verified: 2026-04-30
source_hash: "synthesis-generated"
sources:
  - raw/2026-04-25-copilot-session-audit-recommendations-implementation-4d25144f.md
  - raw/2026-04-25-copilot-session-dashboard-accuracy-fixes-3717a5b2.md
  - raw/2026-04-25-copilot-session-dashboard-accuracy-hardening-404bc17e.md
  - raw/2026-04-22-copilot-session-implementing-full-review-r1-r19-recommendations-884f7926.md
  - raw/2026-04-20-copilot-session-integrating-agent-skill-routing-3f817cb6.md
concepts:
  - source-tagged-confidence-contracts-ml-dashboards
  - training-mode-aware-rolling-window-metadata
  - prior-season-feature-mapping-temporal-leakage-prevention
related:
  - "[[Source-Tagged Confidence Contracts for ML Dashboards]]"
  - "[[Training-Mode-Aware Rolling Window Metadata]]"
  - "[[Prior-Season Feature Mapping for Temporal Leakage Prevention]]"
  - "[[Worktree-Based Subagent-Driven Development]]"
  - "[[Phased Progress Tracking With Validation Gates]]"
tier: hot
tags: [synthesis, nba-ml-engine, audit-remediation, ml-reliability, temporal-integrity, dashboard, workflow]
quality_score: 83
---

# Audit Remediation Patterns for NBA ML Integrity

## Question

How do worktree isolation, validation-gated execution, and temporal-integrity fixes combine to turn an ML audit report into durable production improvements?

## Summary

The checkpoint shows that the highest-value audit fixes were not random bug patches; they were contract upgrades that made hidden assumptions visible and enforceable. [[Worktree-Based Subagent-Driven Development]] and [[Phased Progress Tracking With Validation Gates]] supplied the delivery discipline, while [[Source-Tagged Confidence Contracts for ML Dashboards]], [[Training-Mode-Aware Rolling Window Metadata]], and [[Prior-Season Feature Mapping for Temporal Leakage Prevention]] repaired three different integrity layers: serving semantics, evaluation windows, and feature time alignment.

## Comparison

| Dimension | [[Source-Tagged Confidence Contracts for ML Dashboards]] | [[Training-Mode-Aware Rolling Window Metadata]] | [[Prior-Season Feature Mapping for Temporal Leakage Prevention]] | [[Worktree-Based Subagent-Driven Development]] |
|-----------|---------------|---------------|---------------|---------------|
| Integrity layer | Serving and UI semantics | Train/validation/test semantics | Feature-construction semantics | Delivery and change-isolation semantics |
| Hidden assumption surfaced | “Confidence” means one thing everywhere | One split policy fits both research and production | Season aggregates are safe to join onto same-season rows | Complex fixes can be shipped safely from a shared main checkout |
| Core mechanism | Propagate `confidence_source` and make tiering source-aware | Add `TRAINING_MODE`, chronological rolling windows, and window metadata | Attach season $S$ stats only to season $S+1$ rows; remove same-season fallback | Use isolated worktree branch, slice tasks, and run review/fix loops |
| Failure mode prevented | Heuristic or fallback scores being mislabeled as calibrated | Stale or invalid validation windows, including empty training splits | Future information leaking into historical feature rows | Cross-slice contamination, unsafe hotfixing, and hard-to-review large changes |
| Observable artifact | API contracts, frontend types, and source-aware UI copy | Registry snapshot fields and `/models` window display | Feature builder joins and leakage regression tests | Dedicated branch/worktree plus per-slice commits and reviews |

## Analysis

These concepts fit together because they all convert implicit assumptions into inspectable contracts. The dashboard-confidence fix says: do not call all scores the same thing. The training-window fix says: do not pretend a production retrain and a research experiment share the same evaluation semantics. The prior-season mapping fix says: do not join aggregates unless they were actually knowable at prediction time. In every case, the remedy is to expose and enforce metadata that had previously been hidden inside code paths.

The process concepts matter because integrity fixes are awkward to ship. They touch backend types, UI copy, registry metadata, tests, and sometimes historical assumptions embedded in multiple modules. [[Worktree-Based Subagent-Driven Development]] provides the blast-radius control: the audit campaign could progress slice by slice inside `feature/audit-recommendations` without contaminating main. [[Phased Progress Tracking With Validation Gates]] provides the progression rule: each slice earns completion only after focused tests and review loops close.

There is also a useful contrast with the earlier dashboard-repair checkpoints such as [[Copilot Session Checkpoint: Dashboard Accuracy Fixes]] and [[Copilot Session Checkpoint: Dashboard Accuracy Hardening]]. Those earlier pages concentrated on making live surfaces trustworthy again by unifying contracts, fixing calibration reporting, and surfacing honest warnings. The audit-recommendations implementation extends that same trust agenda deeper into training and feature engineering. In other words, the campaign moved from “make the dashboard stop lying” to “make the underlying training and feature pipeline deserve the dashboard's honesty.”

A second pattern is that the best fixes are deliberately incomplete in the honest sense. The checkpoint does not claim to have solved the entire minutes/ensemble problem; it leaves that slice open with a concrete scope. It also records the unresolved historical-team limitation in `Player.team`. This is good engineering practice: the durable artifact captures exactly which guarantees have been tightened and which remain deferred, so later work can resume without re-discovering the same boundaries.

The combined lesson is that ML integrity is layered. A model can have good code and still fail because its confidence semantics are misleading, its split policy is temporally dishonest, or its feature joins leak future information. The audit campaign became durable knowledge because it encoded fixes at each of those layers and tied them to an execution pattern strong enough to ship them safely.

## Key Insights

1. **The most durable audit fixes are metadata upgrades, not just logic patches.** — supported by [[Source-Tagged Confidence Contracts for ML Dashboards]], [[Training-Mode-Aware Rolling Window Metadata]]
2. **Temporal honesty has to be enforced twice: once in the split policy and once in the feature joins.** — supported by [[Training-Mode-Aware Rolling Window Metadata]], [[Prior-Season Feature Mapping for Temporal Leakage Prevention]]
3. **Process rigor is part of model integrity, not separate from it.** — supported by [[Worktree-Based Subagent-Driven Development]], [[Phased Progress Tracking With Validation Gates]]
4. **Explicitly preserving deferred risk is higher-value than claiming a broad fix is finished.** — supported by [[Copilot Session Checkpoint: Audit Recommendations Implementation]], [[Copilot Session Checkpoint: Dashboard Accuracy Hardening]]

## Open Questions

- What is the right leakage-safe replacement for production minutes predictions during historical stat-model training: rolling priors, cached OOF minutes, or a dedicated feature store?
- Should the model registry expose confidence-source composition metrics the same way it now exposes training-window metadata?
- When the historical-team limitation becomes material, should the next step be a game-level roster snapshot table or a true as-of feature store?

## Sources

- [[Copilot Session Checkpoint: Audit Recommendations Implementation]]
- [[Copilot Session Checkpoint: Dashboard Accuracy Fixes]]
- [[Copilot Session Checkpoint: Dashboard Accuracy Hardening]]
- [[Copilot Session Checkpoint: Integrating Agent Skill Routing]]
- [[Copilot Session Checkpoint: Implementing Full-Review R1-R19 Recommendations]]
