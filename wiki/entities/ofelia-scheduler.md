---
title: "Ofelia Scheduler"
type: entity
created: 2026-04-20
last_verified: 2026-04-26
source_hash: "8d4ffe804f00fc1786f05b552df93998c7e6bf7f3b353158464961c4edb4f8a3"
sources:
  - raw/2026-04-20-copilot-session-scheduler-dns-agents-cleanup-2222559c.md
  - raw/2026-04-26-copilot-session-oom-mitigation-and-follow-up-93744ca8.md
quality_score: 79
concepts:
  - ofelia-scheduler
related:
  - "[[Stale Training Status Detection and Remediation in ML Pipelines]]"
  - "[[Copilot Session Checkpoint: Scheduler DNS Agents Cleanup]]"
  - "[[Homelab]]"
  - "[[NBA ML Engine]]"
  - "[[AdGuard]]"
tier: hot
tags: [scheduler, cron, job-orchestration, homelab]
---

# Ofelia Scheduler

## Overview

Ofelia Scheduler is a cron-based job orchestration tool used in the homelab stack to schedule and execute recurring tasks, such as NBA ML Engine pipeline refreshes and data ingest jobs. It supports 6-field cron syntax, integrates with Docker containers, and acts as the control plane for whether a "daily refresh" is really a bounded freshness job or an expensive retraining job.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

Ofelia Scheduler has become central to multiple NBA ML operational fixes because its labels are the durable source of truth for recurring command paths. In the 2026-04-26 checkpoint, the daily NBA ML command was changed from `python main.py pipeline` to `python main.py pipeline --skip-training`, turning the scheduler itself into the enforcement point for a memory-safety guardrail on the shared host.

## Associated Concepts

- **[[Stale Training Status Detection and Remediation in ML Pipelines]]** — Ofelia schedules training jobs whose status is tracked and remediated.
- **[[Skip-Training Daily Pipeline Guardrails in Shared ML Containers]]** — the scheduler label is where the daily inference-only guardrail is made executable.

## Related Entities

- **[[Homelab]]** — Ofelia Scheduler is deployed and managed within the homelab infrastructure.
- **[[NBA ML Engine]]** — Ofelia orchestrates NBA ML Engine pipeline jobs.
- **[[AdGuard]]** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Scheduler DNS Agents Cleanup]] — where this entity was mentioned
- [[Copilot Session Checkpoint: OOM Mitigation and Follow-Up]] — documents the scheduler label change and the need to verify runtime behavior beyond stored labels
