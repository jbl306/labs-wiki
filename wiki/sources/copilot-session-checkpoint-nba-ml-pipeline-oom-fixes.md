---
title: "Copilot Session Checkpoint: NBA ML Pipeline OOM Fixes"
type: source
created: '2026-04-23'
last_verified: '2026-04-23'
source_hash: "16035a6f5cdc2578c200345a8209b1b969443251f4126a9af138fbf055e69779"
sources:
  - raw/2026-04-23-copilot-session-nba-ml-pipeline-oom-fixes-2781c1dc.md
concepts:
  - daily-weekly-validation-split-nba-ml-pipelines
related:
  - "[[Daily/Weekly Validation Split for NBA ML Pipelines]]"
  - "[[Walk-Forward Cross-Validation for Model Selection]]"
  - "[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]"
  - "[[NBA ML Engine]]"
  - "[[Ofelia Scheduler]]"
  - "[[NBA-ML Model Registry]]"
  - "[[MemPalace]]"
tags: [copilot-session, checkpoint, nba-ml-engine, ml-pipeline, oom, homelab, model-registry, ofelia]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 85
checkpoint_class: durable-debugging
retention_mode: retain
---

# Copilot Session Checkpoint: NBA ML Pipeline OOM Fixes

## Summary

This checkpoint captures a production debugging session on the [[Homelab]]-hosted [[NBA ML Engine]] after the daily training pipeline first failed silently because of a pasted patch block in `main.py`, then later died during a host-level OOM event. The durable lesson is not just how the run was recovered, but why the daily path was restructured: nightly training now favors immediate model registration over full [[Walk-Forward Cross-Validation for Model Selection]], while the heavier validation path remains on the weekly retrain cadence.

## Key Points

- A stray patch-format dump inserted into `main.py` created a `SyntaxError` that silently broke all [[Ofelia Scheduler]] jobs for roughly two days until the bad block was removed and the container image was rebuilt.
- The later pipeline failure was **not** a cgroup kill inside `nba-ml-api`; `dmesg` showed `CONSTRAINT_NONE`, meaning the host hit a global OOM condition across containers and host services.
- Before dying, the daily run completed Steps 1-4b and trained all 7 target stats (`pts`, `reb`, `ast`, `stl`, `blk`, `tov`, `fg3m`), then failed during walk-forward CV for `pts`.
- Recovery avoided retraining from scratch: the session resumed from post-training work by running `python main.py predict --store`, storing 4,168 predictions, then refreshing all 9 materialized views.
- The session found that today's predictions were generated from stale production models because the latest [[NBA-ML Model Registry]] entry was still `2026-04-19`; fresh models had trained to disk but were never promoted.
- The root cause of the stale registry was a registration gate in `trainer.py`: when both CV-based selection and walk-forward CV are enabled, registration waits until the full CV routine completes, so an OOM mid-CV strands newly trained models.
- Memory pressure was amplified by 24 leaked [[MemPalace]] MCP processes; 21 old processes were terminated, freeing about 5 GB and materially reducing host pressure alongside MLflow and Plex load.
- The `nba-ml-api` container limit was lowered from 18 GB to 12 GB so the training container becomes the preferred OOM victim before the entire host is destabilized.
- The durable code change was to make the daily `pipeline()` temporarily disable walk-forward CV and CV-based selection, while the weekly Sunday `train` job still performs the full evaluation workflow.

## Key Concepts

- [[Daily/Weekly Validation Split for NBA ML Pipelines]]
- [[Walk-Forward Cross-Validation for Model Selection]]
- [[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]

## Related Entities

- **[[NBA ML Engine]]** — The primary training system whose daily pipeline, registration behavior, and failure handling were adjusted.
- **[[Ofelia Scheduler]]** — The Docker cron scheduler whose jobs first failed because `main.py` was syntactically invalid.
- **[[NBA-ML Model Registry]]** — The production registry that exposed the deferred-registration failure mode when it remained stuck on 2026-04-19.
- **[[nba-ml-api]]** — The container that trained the models, stored the resumed predictions, and had its memory limit reduced from 18 GB to 12 GB.
- **[[MemPalace]]** — Its leaked MCP helper processes consumed gigabytes of RAM and contributed to the host-wide memory squeeze.
- **[[Homelab]]** — The production host where container limits, background services, and scheduler behavior all interacted during the outage.
