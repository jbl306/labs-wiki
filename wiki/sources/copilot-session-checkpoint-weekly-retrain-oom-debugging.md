---
title: "Copilot Session Checkpoint: Weekly Retrain OOM Debugging"
type: source
created: '2026-04-27'
last_verified: '2026-04-27'
source_hash: "165e5628d8ddd993272d93401f75c9d8f491e65e7efcf3a0deaddced6ef2cf38"
sources:
  - raw/2026-04-27-copilot-session-weekly-retrain-oom-debugging-c722e705.md
concepts:
  - per-model-subprocess-isolation-memory-safe-weekly-retrains
  - persistent-log-manifest-observability-detached-ml-runs
related:
  - "[[Per-Model Subprocess Isolation for Memory-Safe Weekly Retrains]]"
  - "[[Persistent Log and Manifest Observability for Detached ML Runs]]"
  - "[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]"
  - "[[Training Pipeline Status Tracking in ML Systems]]"
  - "[[Artifact Registry Validation In ML Pipelines]]"
  - "[[NBA ML Engine]]"
  - "[[Ofelia Scheduler]]"
  - "[[nba-ml-api]]"
  - "[[ModelRegistry]]"
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 85
tags: [copilot-session, checkpoint, durable-debugging, nba-ml-engine, homelab, oom, observability, ofelia]
checkpoint_class: durable-debugging
retention_mode: retain
---

# Copilot Session Checkpoint: Weekly Retrain OOM Debugging

## Summary

This checkpoint captures the second phase of the NBA ML Engine weekly-retrain incident after the first OOM mitigations were already deployed. The durable lesson is that scheduler guardrails and per-stat subprocess isolation were still not enough: the real fix needed finer-grained per-model isolation, parent-side registration, and much better observability for detached training runs.

## Key Points

- The live homelab state was re-verified before new code changes: the daily [[Ofelia Scheduler]] job still ran `python main.py pipeline --skip-training`, while the weekly job ran `python main.py train --memory-safe`.
- A manual weekly retrain was launched with `docker exec -d -w /app nba-ml-api python main.py train --memory-safe`, and the parent plus `train-minutes` child process were confirmed active even though `/training/status` still showed `Idle`.
- The decisive failure evidence came from the host kernel log: at **2026-04-26 18:15:19 EDT**, a `python` process inside [[nba-ml-api]] was OOM-killed at about **10.3 GB RSS**, indicating another host-level memory exhaustion event rather than a harmless partial failure.
- [[ModelRegistry]] alone under-reported progress. On-disk artifact mtimes showed the run had completed `minutes`, then full `pts`, then full `reb`, and only died before `ast`, which changed the diagnosis from "barely started" to "failed late in the weekly path."
- The first-generation memory-safe design isolated work per stat, but `train --stat <stat>` still called `train_all()` for that stat and therefore still paid the expensive walk-forward CV tail; the likely killer was the `reb` child process after model artifacts were already written.
- The redesign direction shifted from per-stat isolation to **per-model subprocess isolation**, with hidden child flags such as `--skip-cv`, `--skip-register`, and `--metrics-json` so each child performs only one bounded unit of work.
- Parent-side orchestration became part of the fix, not just a wrapper: the parent weekly command now needs to aggregate child metrics, call the best-model registration logic itself, and preserve timeout behavior and skip-stat filtering.
- Observability gaps were treated as first-class bugs. The session added a persistent training directory, append-only retrain logs, a manifest writer, and stage-aware error propagation because detached `docker exec -d` runs were not producing actionable traces in ordinary container logs.
- The existing [[Training Pipeline Status Tracking in ML Systems]] layer was explicitly pulled into the weekly retrain path so `/training/status` can reflect start, stage advancement, completion, and failure instead of staying misleadingly idle during background work.
- The code edits were mid-flight at checkpoint time: tests had been rewritten to drive the second-generation design, but the newest `main.py` and `trainer.py` patches still needed the full red/green validation cycle and redeploy.

## Key Concepts

- [[Per-Model Subprocess Isolation for Memory-Safe Weekly Retrains]]
- [[Persistent Log and Manifest Observability for Detached ML Runs]]
- [[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]
- [[Training Pipeline Status Tracking in ML Systems]]
- [[Artifact Registry Validation In ML Pipelines]]

## Related Entities

- **[[NBA ML Engine]]** — The training system being refactored so weekly retrains can finish safely on a shared homelab host.
- **[[Ofelia Scheduler]]** — The scheduler whose daily and weekly labels had to be rechecked to distinguish intended control flow from the manual debug run.
- **[[nba-ml-api]]** — The shared API container that hosted the retrain process killed by the host OOM event.
- **[[ModelRegistry]]** — The database view of training progress that proved incomplete without cross-checking artifact timestamps on disk.
- **[[Homelab]]** — The constrained shared environment whose host-wide memory pressure shaped both the diagnosis and the redesign.
