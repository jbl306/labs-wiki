---
title: "Copilot Session Checkpoint: OOM Mitigation and Follow-Up"
type: source
created: '2026-04-26'
last_verified: '2026-04-26'
source_hash: b3f0273fc681461d85cdd21c2845050babf29178ea5b90d9763ec60cc54409e3
sources:
  - raw/2026-04-26-copilot-session-oom-mitigation-and-follow-up-93744ca8.md
concepts:
  - skip-training-daily-pipeline-guardrails-ml-containers
  - daily-weekly-validation-split-nba-ml-pipelines
  - oom-failure-diagnosis-remediation-ml-containers
related:
  - "[[Skip-Training Daily Pipeline Guardrails in Shared ML Containers]]"
  - "[[Daily/Weekly Validation Split for NBA ML Pipelines]]"
  - "[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]"
  - "[[nba-ml-api]]"
  - "[[Ofelia Scheduler]]"
  - "[[Galloping-Bot]]"
  - "[[MemPalace]]"
tags: [copilot-session, checkpoint, durable-debugging, nba-ml-engine, homelab, oom, ofelia, galloping-bot]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 79
checkpoint_class: durable-debugging
retention_mode: retain
---

# Copilot Session Checkpoint: OOM Mitigation and Follow-Up

## Summary

This checkpoint captures a two-stage operational lesson for the [[NBA ML Engine]] on a shared homelab host: the first OOM was correctly diagnosed as a host-wide memory exhaustion event, not a simple container-limit breach, and the durable fix was to stop asking the daily [[Ofelia Scheduler]] path to perform full retraining inside [[nba-ml-api]]. It also preserves the follow-up uncertainty that matters just as much as the fix: a later OOM still appeared after deployment, implying that runtime labels, scheduler logs, and actual process paths can diverge and must be correlated carefully before declaring the incident closed.

The same session also records a smaller but durable homelab lesson around [[Galloping-Bot]]: cron wrappers that rely on `docker compose run` can silently execute stale images unless they rebuild first, so the reviewed and pushed wrapper now performs a cached image build before each run.

## Key Points

- The first incident was a **global host OOM**, not a clean cgroup breach inside `nba-ml-api`; kernel logs showed `constraint=CONSTRAINT_NONE`, swap was effectively exhausted, and the killed Python process had roughly **10.8 GB RSS**.
- Root-cause tracing showed the offender was the daily `pipeline-daily` job inside [[Ofelia Scheduler]], which was still running `python main.py pipeline` and therefore performing full training, pruning, and calibrator refits on a shared **32 GB** host.
- The durable remediation was a workload-shaping guardrail, not a memory-bump reflex: `nba-ml-engine/main.py` gained `pipeline --skip-training`, allowing the daily path to ingest, predict, QA, refresh materialized views, and notify **without** retraining models.
- The homelab scheduler definition was updated so the daily command became `python main.py pipeline --skip-training`, while the separate weekly retrain remained the heavy training path.
- The fix was implemented with TDD: new tests required the CLI flag, verified that training/calibration are skipped on the daily path, and added a homelab guardrail assertion so scheduler drift is caught if the label regresses.
- Deployment validation confirmed the live stack still exposed a healthy API, the CLI showed `--skip-training`, and the deployed Ofelia label reflected the new command.
- The session also reviewed an unpushed [[Galloping-Bot]] commit and decided it should be pushed because `docker compose run` does not rebuild an existing image; adding a cached `compose build galloping-bot` before execution closes a stale-image cron drift path.
- A **second OOM** then occurred at **2026-04-26 15:05 EDT** even after the skip-training mitigation was deployed; the killed Python process was again inside the `nba-ml-api` Docker scope with about **11.4 GB RSS**, while scheduler labels still claimed the daily path was using `--skip-training`.
- The unresolved clue is that scheduler logs still showed model-training output around **13:59**, suggesting either a different scheduler/manual path was still training, or the observed logs were being misread as post-fix activity when they were actually older output.

## Key Concepts

- [[Skip-Training Daily Pipeline Guardrails in Shared ML Containers]]
- [[Daily/Weekly Validation Split for NBA ML Pipelines]]
- [[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]

## Related Entities

- **[[nba-ml-api]]** — The shared API container that hosted both inference-serving duties and the scheduled Python workload killed during both host-level OOM events.
- **[[Ofelia Scheduler]]** — The cron orchestrator whose daily job label was changed to `python main.py pipeline --skip-training`, making it central to both the mitigation and the follow-up investigation.
- **[[Galloping-Bot]]** — The separate automation reviewed in the same session; its wrapper now rebuilds before execution so cron does not run stale images.
- **[[MemPalace]]** — The memory system queried for prior OOM and homelab context, letting the debugging session resume from durable lessons instead of starting cold.
- **[[NBA ML Engine]]** — The broader training and prediction system whose daily/weekly workload boundaries were tightened to reduce blast radius on the homelab host.
