---
title: "Weekly Retrain Survivability vs Observability on Shared ML Hosts"
type: synthesis
created: 2026-04-27
last_verified: 2026-04-27
source_hash: "synthesis-generated"
sources:
  - raw/2026-04-27-copilot-session-weekly-retrain-oom-debugging-c722e705.md
  - raw/2026-04-18-copilot-session-training-status-tracker-and-oom-fix-6c60a486.md
  - raw/2026-04-26-copilot-session-oom-mitigation-and-follow-up-93744ca8.md
concepts:
  - per-model-subprocess-isolation-memory-safe-weekly-retrains
  - persistent-log-manifest-observability-detached-ml-runs
  - training-pipeline-status-tracking-ml-systems
related:
  - "[[Per-Model Subprocess Isolation for Memory-Safe Weekly Retrains]]"
  - "[[Persistent Log and Manifest Observability for Detached ML Runs]]"
  - "[[Training Pipeline Status Tracking in ML Systems]]"
  - "[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]"
  - "[[NBA ML Engine]]"
  - "[[nba-ml-api]]"
tier: hot
tags: [ml-ops, synthesis, nba-ml-engine, observability, oom, retraining]
---

# Weekly Retrain Survivability vs Observability on Shared ML Hosts

## Question

When a weekly retrain still fails on a shared host after the obvious scheduler and memory guardrails are already in place, should the next move be to reshape the workload, add better observability, or deepen status tracking?

## Summary

The checkpoint family says these are complementary, but not interchangeable, levers. [[Per-Model Subprocess Isolation for Memory-Safe Weekly Retrains]] reduces the memory footprint of the work itself, [[Persistent Log and Manifest Observability for Detached ML Runs]] makes detached failures reconstructable, and [[Training Pipeline Status Tracking in ML Systems]] provides the lightweight runtime surface operators need while the job is in flight.

If the host is still OOM-killing weekly runs, workload reshaping has to come first because no amount of telemetry will make an oversized stage finish. But once the execution unit is small enough, observability and status tracking determine whether the next failure is diagnosable in minutes instead of after another full rerun.

## Comparison

| Dimension | [[Per-Model Subprocess Isolation for Memory-Safe Weekly Retrains]] | [[Persistent Log and Manifest Observability for Detached ML Runs]] | [[Training Pipeline Status Tracking in ML Systems]] |
|-----------|--------------------------------------------------------------------|--------------------------------------------------------------------|-----------------------------------------------------|
| Primary problem solved | Peak memory remains too high even after coarse isolation | Detached jobs leave too little evidence after failure | Operators cannot see live stage progress from dashboards/APIs |
| Unit of control | `stat × model` child stage | Run log plus structured manifest | Pipeline stage state file |
| Main output | Smaller execution envelope and parent-side registration | Durable forensic trace and machine-readable run plan | Pollable status such as running/idle/failed and current stage |
| Best time horizon | Before or during execution design | During failure investigation and resume planning | During execution and quick health checks |
| Key strength | Changes the workload so the host can survive it | Tells humans what happened after a background run | Gives lightweight live visibility without reading full logs |
| Main blind spot | Still needs good evidence when a child fails | Does not itself prevent OOM or stale states | Can be stale or too shallow if lifecycle hooks are missing |

## Analysis

The three concepts line up as layers of operational control. [[Training Pipeline Status Tracking in ML Systems]] is the lightest layer: it tells a dashboard whether something is running and roughly where it is. That matters because without a pollable public surface, every retrain becomes a shell-level debugging exercise. But the weekly retrain checkpoint also shows the limit of status tracking alone: if the orchestration path forgets to call `start_pipeline()` or `finish_pipeline()`, the API can remain `Idle` while real work is running.

[[Persistent Log and Manifest Observability for Detached ML Runs]] addresses a different failure mode. Once a run is detached from the terminal, the operator needs durable evidence that survives beyond the launch moment. Persistent logs and manifests answer questions like "Which stage died?" and "Where is the trace?" much better than a single status file can. They also combine well with artifact timestamps and registry inspection, which became essential in the checkpoint when the registry under-reported how far the run had actually progressed.

But neither of those observability layers solves the root physical constraint when a host is still getting OOM-killed. That is why [[Per-Model Subprocess Isolation for Memory-Safe Weekly Retrains]] is the decisive redesign in this checkpoint family. The first memory-safe attempt already had a better scheduler boundary and a manual process check, yet the `reb` child still likely died in a walk-forward-CV tail. The lesson is that control-flow structure itself is part of memory management. If the work unit is too large, richer telemetry just gives a more detailed obituary.

The most durable operating model therefore stacks the three layers in order. First, reshape the workload so a single bounded child can finish safely on the host. Second, make every detached run leave a manifest and log trail so failures are reconstructable. Third, expose stage progression through a status tracker so humans and dashboards can monitor the run without opening the full trace. On a shared homelab node, survivability comes from bounded stages; trust comes from observability.

## Key Insights

1. **Status tracking is necessary but insufficient** — supported by [[Training Pipeline Status Tracking in ML Systems]] and [[Copilot Session Checkpoint: Weekly Retrain OOM Debugging]].
2. **For background jobs, logs and manifests are part of correctness, not just convenience** — supported by [[Persistent Log and Manifest Observability for Detached ML Runs]] and [[Copilot Session Checkpoint: Weekly Retrain OOM Debugging]].
3. **When coarse isolation still OOMs, the next durable lever is smaller execution units, not bigger memory limits** — supported by [[Per-Model Subprocess Isolation for Memory-Safe Weekly Retrains]] and [[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]].

## Open Questions

- If one model family remains too large even inside the per-model design, should the weekly retrain move to a separate disposable worker service rather than keep sharing fate with [[nba-ml-api]]?
- What manifest schema should become canonical so future retrain runs can be resumed or audited automatically rather than only debugged manually?

## Sources

- [[Copilot Session Checkpoint: Weekly Retrain OOM Debugging]]
- [[Copilot Session Checkpoint: Training Status Tracker and OOM Fix]]
- [[Copilot Session Checkpoint: OOM Mitigation and Follow-Up]]
