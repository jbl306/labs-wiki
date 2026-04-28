---
title: "Persistent Log and Manifest Observability for Detached ML Runs"
type: concept
created: 2026-04-27
last_verified: 2026-04-27
source_hash: "165e5628d8ddd993272d93401f75c9d8f491e65e7efcf3a0deaddced6ef2cf38"
sources:
  - raw/2026-04-27-copilot-session-weekly-retrain-oom-debugging-c722e705.md
related:
  - "[[Training Pipeline Status Tracking in ML Systems]]"
  - "[[Artifact Registry Validation In ML Pipelines]]"
  - "[[The Observability Imperative]]"
  - "[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]"
tier: hot
tags: [observability, ml-ops, detached-runs, manifests, logging, nba-ml-engine]
quality_score: 65
---

# Persistent Log and Manifest Observability for Detached ML Runs

## Overview

Persistent log-and-manifest observability is a durability pattern for asynchronous or detached ML jobs where normal process output is not sufficient to reconstruct what happened after failure. In the weekly retrain checkpoint behind this concept, a background `docker exec -d` run appeared alive at the process level, but neither `/training/status` nor ordinary container logs provided enough evidence to explain progress, late-stage failure, or which exact stage had died.

The pattern matters when a long-running job is executed outside an interactive shell and therefore loses the rich operator feedback loop that exists during foreground development. Instead of relying on transient stdout, it writes durable stage logs and machine-readable manifests into a persistent training directory that survives long enough for postmortem analysis and resume logic.

## How It Works

The core problem begins with detached execution. A foreground training command gives the operator a tight loop: terminal output, stack traces, and the ability to infer which stage is currently active. But once the job is launched via `docker exec -d`, cron, or a background subprocess tree, that loop breaks. Child processes may inherit stdout/stderr in ways that do not end up in `docker logs`, shell history may only preserve the parent command, and API-level status endpoints may lag or remain idle if the orchestration path does not update them. In the checkpoint source, this is exactly what happened: the weekly retrain was running, but `/training/status` still reported `Idle`, and later the failed run left too little direct logging to explain why it stopped.

Persistent log-and-manifest observability fixes that by separating human-readable traces from machine-readable state. The first component is an append-only run log, typically stored under a directory such as `MEMORY_SAFE_TRAINING_DIR`. Every child stage gets a `log_path`, and the subprocess wrapper redirects stdout/stderr there. This means that even if the command was launched in the background, the full stage stream still exists on disk. The crucial detail is that the log path is passed through orchestration deliberately rather than left to incidental shell inheritance.

The second component is the manifest. A log tells humans what happened; a manifest tells the system what it intended to do and how far it got. In the checkpoint, the design direction included helpers such as `_write_memory_safe_manifest()` and `_memory_safe_target_stats()`, indicating that the parent weekly retrain should record the run plan in structured form. A manifest can include the source command, selected stats, ordered stages, start timestamp, current stage, output log path, and perhaps the metrics or artifact files expected from each child. That gives operators a durable control-plane snapshot even if the job dies before final cleanup.

The value of the manifest becomes obvious during partial failure. Suppose the run completes `minutes`, all `pts` children, all `reb` children, and then dies before `ast`. A status tracker alone may tell you the last visible stage, but it does not necessarily tell you the plan, the child boundaries, or the persistent log location. A registry query may tell you only which models were promoted. Artifact mtimes may tell you that files exist. The manifest complements all three by answering: what stages were supposed to run, which stage name was active, and where should the detailed trace be read? In that sense, observability becomes multi-layered:

$$
\text{Operational Truth} \approx \text{status tracker} + \text{run manifest} + \text{persistent logs} + \text{artifact evidence}
$$

No one layer is sufficient on its own. The checkpoint explicitly showed why: [[ModelRegistry]] under-reported progress, artifact mtimes revealed more progress than the DB, and the status tracker stayed idle because the first-generation path never called its lifecycle hooks.

A well-designed subprocess wrapper makes this pattern practical. In the session, `_run_self_cli_subprocess()` was being extended with `log_path` and `stage_name`. That is a strong design choice because it forces every child invocation to declare not just the command but also the operator-facing context for that command. If the child exits non-zero, the parent can raise an error that includes the stage name and log path. This turns a vague "weekly retrain failed" incident into a concrete report such as "stage `reb/lightgbm` failed; inspect `/app/training/memory-safe/2026-04-27/run.log`."

This pattern also complements, rather than replaces, [[Training Pipeline Status Tracking in ML Systems]]. Status tracking is ideal for lightweight polling surfaces such as dashboards or `/training/status` APIs. A manifest is better for structured run-state recovery. Persistent logs are best for detailed forensic reconstruction. Together they let detached jobs be both machine-observable and human-debuggable. That is especially important on shared hosts, where operators may only learn about a failure after the fact from a downstream symptom or a kernel OOM line.

There are trade-offs. Persistent logs need rotation or retention policy, manifests need schema discipline, and error propagation has to preserve context without swallowing exceptions. But those costs are justified when the alternative is losing the only useful evidence from a six-hour training job. In practice, the pattern turns background execution from "fire and hope" into "fire, record, and recover."

## Key Properties

- **Durable run trace:** Child stdout/stderr is redirected into a persistent file instead of disappearing with the launching shell.
- **Machine-readable run plan:** A manifest captures intended stages, selected stats, file paths, and current progress independently of log text.
- **Stage-aware failures:** Parent exceptions can name both the failed stage and the log file operators should inspect.
- **Cross-layer observability:** Logs, manifests, status files, and artifact evidence each contribute a different slice of operational truth.
- **Postmortem-friendly detached execution:** Background jobs become diagnosable even when no operator watched them live.

## Limitations

This pattern does not itself prevent failures; it makes them intelligible. If the log directory lives on ephemeral storage, evidence can still vanish after restart. A noisy log without consistent stage boundaries may remain hard to use, and a manifest that is not updated atomically can drift from reality. The pattern also adds operational data that must be cleaned up or archived to avoid filling disk on systems with frequent scheduled jobs.

## Examples

```python
manifest = {
    "run_id": "2026-04-27-weekly-retrain",
    "stats": ["pts", "reb", "ast"],
    "stages": ["minutes", "pts/xgb", "pts/lgb", "reb/xgb"],
    "log_path": "/app/training/memory-safe/2026-04-27/run.log",
}
write_manifest(manifest)

run_self_cli_subprocess(
    ["train", "--stat", "reb", "--model", "lightgbm", "--skip-cv"],
    stage_name="reb/lightgbm",
    log_path=manifest["log_path"],
)
```

Even if the child is OOM-killed later, operators can still read the manifest, inspect the log, compare artifact mtimes, and tell exactly which stage needs attention or retry.

## Practical Applications

Persistent log-and-manifest observability is useful for cron-triggered retrains, background fine-tuning jobs, GPU evaluations launched from schedulers, ETL pipelines kicked off through detached shells, and any long-running workflow where the human who launched it is not guaranteed to stay attached. It is especially valuable in homelab and small-team environments where there may be no full-featured workflow orchestrator, but postmortem accuracy still matters.

## Related Concepts

- **[[Training Pipeline Status Tracking in ML Systems]]**: Covers the lightweight public status surface that this pattern augments with durable forensic evidence.
- **[[Artifact Registry Validation In ML Pipelines]]**: Shows how on-disk artifacts can reveal reality when the registry view is incomplete or stale.
- **[[The Observability Imperative]]**: Provides the broader engineering principle behind recording enough evidence to debug real production behavior.
- **[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]**: Supplies the failure context that makes persistent evidence especially important on shared, memory-constrained hosts.

## Sources

- [[Copilot Session Checkpoint: Weekly Retrain OOM Debugging]] — documents the detached weekly run, the missing live visibility, and the redesign toward persistent logs plus run manifests.
