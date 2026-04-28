---
title: "Memory Tuning vs Workload Shaping in NBA ML OOM Response"
type: synthesis
created: '2026-04-26'
last_verified: '2026-04-26'
source_hash: "synthesis-generated"
sources:
  - raw/2026-04-26-copilot-session-oom-mitigation-and-follow-up-93744ca8.md
  - raw/2026-04-23-copilot-session-nba-ml-pipeline-oom-fixes-2781c1dc.md
  - raw/2026-04-18-copilot-session-training-status-tracker-and-oom-fix-6c60a486.md
concepts:
  - oom-failure-diagnosis-remediation-ml-containers
  - daily-weekly-validation-split-nba-ml-pipelines
  - skip-training-daily-pipeline-guardrails-ml-containers
related:
  - "[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]"
  - "[[Daily/Weekly Validation Split for NBA ML Pipelines]]"
  - "[[Skip-Training Daily Pipeline Guardrails in Shared ML Containers]]"
  - "[[nba-ml-api]]"
  - "[[Ofelia Scheduler]]"
tier: hot
tags: [ml-ops, oom, synthesis, nba-ml-engine, homelab]
quality_score: 75
---

# Memory Tuning vs Workload Shaping in NBA ML OOM Response

## Question

When a shared ML service keeps hitting OOM conditions, should operators raise memory limits, reshape the daily workload, or remove training from the daily path entirely?

## Summary

The three pages answer different layers of the same operational problem. [[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]] explains how to prove what actually failed, [[Daily/Weekly Validation Split for NBA ML Pipelines]] reduces daily peak cost while preserving daily retraining, and [[Skip-Training Daily Pipeline Guardrails in Shared ML Containers]] goes further by turning the daily path into an inference-first refresh job.

The right choice depends on where the pressure comes from. If the failure is a temporary local cgroup squeeze, resource tuning may be enough; if the host is globally exhausted or the daily job is doing work it does not strictly need, workload shaping is the safer and more durable lever.

## Comparison

| Dimension | [[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]] | [[Daily/Weekly Validation Split for NBA ML Pipelines]] | [[Skip-Training Daily Pipeline Guardrails in Shared ML Containers]] |
|-----------|-----------------------------------------------------------------------------|--------------------------------------------------------|---------------------------------------------------------------------|
| Primary lever | Diagnose failure mode, then tune limits/config | Keep daily retraining but move heavy evaluation to weekly cadence | Remove retraining from the daily path entirely |
| Daily workload after change | Still may train, but with different resource settings or lighter config | Daily job still trains models, but avoids walk-forward CV / heavy selection | Daily job ingests, predicts, QA-checks, and refreshes using existing models |
| Best fit | One-off local memory pressure or recoverable container sizing mismatch | Daily freshness still requires retraining, but full evaluation is too costly every day | Daily value comes from fresh inputs, not fresh model weights |
| Main risk | Raising limits can destabilize the host if the real failure domain is global | Daily path is still a training path and can remain expensive | Model artifacts may grow stale if weekly/manual retraining is neglected |
| Operational proof needed | Kernel/container evidence (`OOMKilled`, `CONSTRAINT_NONE`, swap state) | Control-flow proof that daily and weekly paths really diverge | Scheduler/runtime proof that `--skip-training` is the command that actually ran |
| Failure mode if misapplied | Bigger container budgets but same root cause | Less evaluation pressure yet still too much training pressure | Stable service but silent model staleness or alternate hidden training path |

## Analysis

The first page in this family is diagnostic, not prescriptive. [[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]] teaches that operators should not treat every OOM as a container-sizing problem. That matters because the remediation branch depends on whether the kernel killed a process inside a tight cgroup or whether the entire host ran out of memory across containers, daemons, and interactive tooling. In the NBA ML sessions, `CONSTRAINT_NONE` was the tell that host-wide pressure, not just one badly sized container, was driving the incident.

Once diagnosis shows the workload itself is oversized for the daily path, the next question is how much work must remain daily. [[Daily/Weekly Validation Split for NBA ML Pipelines]] is a middle-ground answer. It keeps daily retraining intact but removes the heaviest evaluation stage from the nightly critical path. That is ideal when tomorrow's predictions truly benefit from new weights every day, yet walk-forward CV and full model-selection rigor do not. It is a control-flow redesign that preserves daily learning while shrinking peak cost.

[[Skip-Training Daily Pipeline Guardrails in Shared ML Containers]] is a stronger move because it redefines the daily contract. In the follow-up checkpoint, the lesson was that even lighter daily retraining was still the wrong operational target for a shared homelab container. The daily job needed prediction freshness, not necessarily fresh model fitting. That made `pipeline --skip-training` the correct safeguard: it removed retraining, pruning, and calibrator refits from the daily path and left the weekly retrain as the intentional heavy workflow.

The follow-up OOM after deployment is why these approaches should be treated as complementary rather than mutually exclusive. The skip-training design was still correct, but the later evidence suggested either another training path was firing or the observed logs were being misread. That means the durable stack is: diagnose precisely, reshape the workload to fit the cadence, and then verify at runtime that the scheduler and process tree actually respect the new boundary. In practical terms, memory tuning buys time, validation splitting buys efficiency, and skip-training guardrails buy safety when daily retraining is no longer worth the host-level risk.

## Key Insights

1. **Diagnosis comes before mitigation choice** — supported by [[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]] and [[Copilot Session Checkpoint: OOM Mitigation and Follow-Up]].
2. **Workload shaping is usually more durable than repeated memory bumps on a shared host** — supported by [[Daily/Weekly Validation Split for NBA ML Pipelines]] and [[Skip-Training Daily Pipeline Guardrails in Shared ML Containers]].
3. **Scheduler labels are intent, not proof** — supported by [[Skip-Training Daily Pipeline Guardrails in Shared ML Containers]] and [[Copilot Session Checkpoint: OOM Mitigation and Follow-Up]].

## Open Questions

- Should the NBA ML stack eventually move all heavy training out of `nba-ml-api` and into a separate disposable worker container so the API process never shares fate with retraining jobs?
- What runtime evidence should be recorded automatically so future OOM investigations can distinguish stale log tails from genuinely post-deploy training activity?

## Sources

- [[Copilot Session Checkpoint: Training Status Tracker and OOM Fix]]
- [[Copilot Session Checkpoint: NBA ML Pipeline OOM Fixes]]
- [[Copilot Session Checkpoint: OOM Mitigation and Follow-Up]]
