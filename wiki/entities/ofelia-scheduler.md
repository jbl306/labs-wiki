---
title: "Ofelia Scheduler"
type: entity
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "8d4ffe804f00fc1786f05b552df93998c7e6bf7f3b353158464961c4edb4f8a3"
sources:
  - raw/2026-04-20-copilot-session-scheduler-dns-agents-cleanup-2222559c.md
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

Ofelia Scheduler is a cron-based job orchestration tool used in the homelab stack to schedule and execute recurring tasks, such as NBA ML Engine pipeline refreshes and data ingest jobs. It supports 6-field cron syntax and integrates with Docker containers.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

Ofelia Scheduler was audited and updated in the session to move the NBA ML Engine props-refresh job to 4 PM EDT. Its health and job registration were verified, ensuring robust pipeline orchestration.

## Associated Concepts

- **[[Stale Training Status Detection and Remediation in ML Pipelines]]** — Ofelia schedules training jobs whose status is tracked and remediated.

## Related Entities

- **[[Homelab]]** — Ofelia Scheduler is deployed and managed within the homelab infrastructure.
- **[[NBA ML Engine]]** — Ofelia orchestrates NBA ML Engine pipeline jobs.
- **[[AdGuard]]** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Scheduler DNS Agents Cleanup]] — where this entity was mentioned
