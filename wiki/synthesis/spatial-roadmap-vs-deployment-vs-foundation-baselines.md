---
title: "Roadmap Planning vs Deployment Hardening vs Foundation Baselines in Spatial Design Studio"
type: synthesis
created: '2026-05-14'
last_verified: '2026-05-14'
source_hash: "synthesis-generated"
sources:
  - raw/2026-05-14-copilot-session-spatial-studio-production-roadmap-9170f546.md
  - raw/2026-05-11-copilot-session-spatial-production-deployment-56f1f521.md
  - raw/2026-05-14-copilot-session-implementing-s6-sprint-foundation-sds-100-102-10-4831f34a.md
concepts:
  - cpu-bound-ai-stack-planning-homelab-spatial-apps
  - staged-toolchain-baseline-hardening-active-monorepos
  - phased-progress-tracking-validation-gates
related:
  - "[[Spatial Design Studio]]"
  - "[[Copilot Session Checkpoint: Spatial Studio Production Roadmap]]"
  - "[[Copilot Session Checkpoint: Spatial Production Deployment]]"
  - "[[Copilot Session Checkpoint: Implementing S6 sprint foundation (SDS-100/102/101)]]"
tier: hot
tags: [spatial-design-studio, roadmap, deployment, tooling, synthesis, homelab]
---

# Roadmap Planning vs Deployment Hardening vs Foundation Baselines in Spatial Design Studio

## Question

How should an actively evolving homelab product move from high-level production planning to real deployment and then to repository-level delivery/tooling discipline without stalling feature work?

## Summary

The three Spatial Design Studio checkpoints answer different layers of the same maturity problem. The roadmap checkpoint defines what is feasible and worth pursuing, the deployment checkpoint establishes the live runtime contract, and the S6 foundation checkpoint turns those decisions into repeatable repository mechanics through scoped branches, validation gates, and a staged toolchain baseline.

## Comparison

| Dimension | [[Copilot Session Checkpoint: Spatial Studio Production Roadmap]] | [[Copilot Session Checkpoint: Spatial Production Deployment]] | [[Copilot Session Checkpoint: Implementing S6 sprint foundation (SDS-100/102/101)]] |
|-----------|---------------|---------------|---------------|
| Primary question | What should the product become under real homelab constraints? | What already runs in production, and under which invariants? | How should the next tranche of work be executed safely inside the repo? |
| Main artifact | `plans/spatial-design-studio-production-grade-roadmap.md` and planning constraints | Live app/runtime surfaces, agent files, deployment path, health checks | S6 issue/branch/PR execution pattern plus API/web tooling configs |
| Constraint focus | CPU limits, cost, license boundaries, service inventory reality | Secrets, compose path truth, same-origin routing, health and deploy verification | Reviewable diffs, tool compatibility, domain-specific lint exceptions, CI readiness |
| Failure mode prevented | Building an unrealistic GPU-first or SaaS-heavy roadmap | Shipping an app that runs locally but not as a durable homelab service | Enforcing noisy or misleading checks that collide with planned refactors |
| Evidence style | Feasibility analysis, named tools, latency/cost expectations | Concrete runtime checks, config invariants, deployed endpoints | Exact file paths, pinned tool versions, failing rules, and next-step commands |
| Resulting leverage | Better prioritization | Safer operation | Faster future delivery with less review noise |

## Analysis

The key insight across these sources is that "production-grade" is not one decision. In the roadmap checkpoint, production-readiness means choosing ambitions the homelab can actually support. The source narrows the system toward CPU-feasible vision, free-first tooling, and explicit licensing/cost boundaries. That work matters because it prevents the team from optimizing for a fantasy stack that would never survive deployment on the real machine.

The deployment checkpoint moves one level down from strategy into operational truth. It answers questions the roadmap cannot: which compose file is authoritative, which routes are live, which secrets and security flags are mandatory, and which architectural seams already exist in the code. This is where [[Spatial Design Studio]] stops being just a plan and becomes a service with known ingress, health checks, and production assumptions. Without that checkpoint, later repository work would risk hardening the wrong execution path.

The S6 foundation checkpoint adds a third kind of maturity: delivery discipline inside the repository itself. Once a project has a plausible roadmap and a working deployment surface, the next bottleneck is no longer "what should we build?" or "can we run it?" but "can we land changes repeatedly without review chaos?" The checkpoint's answer is a workflow contract: scope large tasks down, respect dependencies, require registry row -> issue -> branch -> validation -> PR, and introduce tooling in a staged manner that preserves momentum. That is why the most durable details here are not just filenames; they are the reasons strict formatting, aggressive lint rules, and CI expansion were sequenced the way they were.

Together, the three pages describe a maturity ladder. First, constrain the roadmap by physical and operational reality. Second, prove the service boundary in deployment. Third, harden the repo's inner loop so future changes can accumulate without regressions or unreviewable churn. The order matters. Trying to add strict CI before the deployment contract is known or before the roadmap is scoped would create busywork. Conversely, planning and deployment alone are insufficient if every subsequent branch still has to rediscover how to open an issue, name a branch, or keep React Three Fiber code from fighting generic DOM lint rules.

## Key Insights

1. **Roadmap realism, runtime realism, and repo realism are separate problems.** — supported by [[Copilot Session Checkpoint: Spatial Studio Production Roadmap]], [[Copilot Session Checkpoint: Spatial Production Deployment]], [[Copilot Session Checkpoint: Implementing S6 sprint foundation (SDS-100/102/101)]]
2. **The highest-leverage "foundation" work is often workflow and tooling, not new product surface.** — supported by [[Staged Toolchain Baseline Hardening for Active Monorepos]], [[Copilot Session Checkpoint: Implementing S6 sprint foundation (SDS-100/102/101)]]
3. **Strictness should follow architecture, not fight it.** — supported by [[Copilot Session Checkpoint: Spatial Production Deployment]], [[Copilot Session Checkpoint: Implementing S6 sprint foundation (SDS-100/102/101)]]

## Open Questions

- When should the repo promote the deferred formatter and stricter mypy rules from "documented debt" into mandatory gates?
- Should SDS-101's `run-gates.sh` include `ruff format --check` immediately, or wait until the planned large-file decompositions land?
- Is the repo-specific `spatial-task-delivery` workflow general enough to become a reusable concept or template across other homelab projects?

## Sources

- [[Copilot Session Checkpoint: Spatial Studio Production Roadmap]]
- [[Copilot Session Checkpoint: Spatial Production Deployment]]
- [[Copilot Session Checkpoint: Implementing S6 sprint foundation (SDS-100/102/101)]]
