---
title: "Configuration Scope vs Workload Shaping in Homelab Repairs"
type: synthesis
created: '2026-05-18'
last_verified: '2026-05-18'
source_hash: "synthesis-generated"
sources:
  - raw/2026-05-18-copilot-session-homelab-nba-repairs-e405020e.md
  - raw/2026-04-18-copilot-session-training-status-tracker-and-oom-fix-6c60a486.md
  - raw/2026-04-27-copilot-session-weekly-retrain-oom-debugging-c722e705.md
concepts:
  - trusted-domain-scope-reverse-proxied-nextcloud-checks
  - task-specific-feature-profiles-memory-bounded-ml-training
  - oom-failure-diagnosis-remediation-ml-containers
related:
  - "[[Trusted-Domain Scope for Reverse-Proxied Nextcloud Checks]]"
  - "[[Task-Specific Feature Profiles for Memory-Bounded ML Training]]"
  - "[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]"
  - "[[Nextcloud]]"
  - "[[NBA ML Engine]]"
  - "[[Homelab]]"
tier: hot
tags: [synthesis, homelab, nextcloud, nba-ml-engine, reliability, ml-ops]
quality_score: 79
---

# Configuration Scope vs Workload Shaping in Homelab Repairs

## Question

When a self-hosted system fails because its effective operating surface has grown broader than intended, should the fix narrow configuration scope, reshape the workload, or first prove a deeper resource failure?

## Summary

These approaches solve different layers of the same problem. [[Trusted-Domain Scope for Reverse-Proxied Nextcloud Checks]] narrows the declared ingress surface so diagnostics match the real deployment boundary, [[Task-Specific Feature Profiles for Memory-Bounded ML Training]] narrows the computational surface so a model stops paying for irrelevant work, and [[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]] establishes the evidence needed to know whether workload changes are even the right lever.

In practice, configuration-scope fixes are best when the system is "failing correctly" against an over-broad declaration, while workload shaping is best when the task itself is too large for the available runtime envelope. OOM diagnosis remains the guardrail that prevents operators from treating every broken run as either a proxy bug or a memory-budget problem by instinct alone.

## Comparison

| Dimension | [[Trusted-Domain Scope for Reverse-Proxied Nextcloud Checks]] | [[Task-Specific Feature Profiles for Memory-Bounded ML Training]] | [[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]] |
|-----------|---------------------------------------------------------------|-------------------------------------------------------------------|-----------------------------------------------------------------------------|
| Primary failure shape | App health/security checks report misleading exposure | Training stage is killed because the task loads unnecessary feature families | Operators know a job died, but not yet whether the cause is cgroup, host, or workload |
| Scope being reduced | Trusted hosts and proxy-visible ingress surface | Feature graph and loader set for one model task | None directly; this concept proves which remediation path is justified |
| Main evidence | Probes against trusted domains hit an unintended wildcard-routed host | `OOMKilled=true`, `exit -9`, and successful rerun after lighter profile | Container state, kernel/cgroup evidence, stale status signals, runtime logs |
| Best lever | Tighten `trusted_domains`, overwrite host, and proxy alignment | Add explicit per-task feature profiles such as `full` vs `minutes` | Inspect the failure mode before tuning memory or redesigning control flow |
| Risk if ignored | Persistent false positives and insecurely broad ingress assumptions | Repeated OOMs, longer runtimes, and hidden coupling between small and large models | Misapplied fixes such as random memory bumps or incorrect root-cause stories |
| Durable lesson | Declared host scope is executable behavior, not just metadata | Shared builders need honest workload boundaries | Diagnosis is the gate that separates symptoms from real remediation |

## Analysis

The new checkpoint adds a useful cross-domain pattern to the wiki: many "mysterious" operational failures are really scope-definition failures. In the Nextcloud case, storage placement and proxying were mostly correct by the end, yet the application still complained because its trusted-domain set told it to validate a larger ingress surface than the operators wanted to preserve. The app was not malfunctioning; it was faithfully evaluating the environment it had been told to trust.

The NBA minutes-model repair expresses the same pattern on the computational side. The shared feature builder was doing what it was designed to do—assemble a rich feature matrix—but the minutes stage no longer deserved that full workload. Once the system exposed `feature_profile="minutes"` as an explicit boundary, the smaller model stopped inheriting costs that belonged to broader stat-model training. This is the compute analogue of shrinking `trusted_domains` to the canonical hostname.

[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]] remains necessary because scope-reduction only makes sense after the failure mode is known. The checkpoint's `OOMKilled=true`, `oom_kill 4`, and exit `-9` evidence justified workload reshaping for the minutes model. Without that proof, an operator could have spent time on logging tweaks, container restarts, or proxy speculation instead of changing the feature pipeline. Diagnosis is the step that tells you whether the problem is over-broad compute, over-broad config, or something else entirely.

The durable operating rule is therefore layered. First, prove what failed. Second, ask whether the system is failing because it was told to treat too much surface as active—hosts, routes, loaders, stages, or side channels. Third, narrow only the surface that should never have been active for that task in the first place. On shared homelab infrastructure, this is often more reliable than broadening allowances or repeatedly raising resource limits.

## Key Insights

1. **Over-broad declarations create real failures even when the underlying subsystem is mostly healthy** — supported by [[Trusted-Domain Scope for Reverse-Proxied Nextcloud Checks]] and [[Copilot Session Checkpoint: Homelab NBA repairs]].
2. **Workload shaping is strongest when it reflects semantic task boundaries rather than generic "lighter mode" switches** — supported by [[Task-Specific Feature Profiles for Memory-Bounded ML Training]] and [[Copilot Session Checkpoint: Homelab NBA repairs]].
3. **Evidence should decide whether you narrow config scope or compute scope** — supported by [[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]] and [[Copilot Session Checkpoint: Training Status Tracker and OOM Fix]].

## Open Questions

- Should the homelab standardize a "canonical ingress only" rule across other reverse-proxied services so apps never accumulate convenience LAN aliases in production trusted-host settings?
- Should the [[NBA ML Engine]] expose more explicit feature-profile choices for other submodels before their workloads silently grow into the same failure pattern?

## Sources

- [[Copilot Session Checkpoint: Homelab NBA repairs]]
- [[Copilot Session Checkpoint: Training Status Tracker and OOM Fix]]
- [[Copilot Session Checkpoint: Weekly Retrain OOM Debugging]]

