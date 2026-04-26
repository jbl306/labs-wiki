---
title: "nba-ml-api"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "5696101c1ddba558560149a708018979e6d8425067b82872f36a6d08784426d9"
sources:
  - raw/2026-04-18-copilot-session-training-status-tracker-and-oom-fix-6c60a486.md
  - raw/2026-04-26-copilot-session-oom-mitigation-and-follow-up-93744ca8.md
quality_score: 62
concepts:
  - nba-ml-api
related:
  - "[[Training Pipeline Status Tracking in ML Systems]]"
  - "[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]"
  - "[[Copilot Session Checkpoint: Training Status Tracker and OOM Fix]]"
  - "[[NBA ML Engine]]"
  - "[[MinutesModel]]"
  - "[[Qdrant]]"
tier: hot
tags: [api, docker, ml-pipeline, nba]
---

# nba-ml-api

## Overview

nba-ml-api is a Dockerized API service for the [[NBA ML Engine]], exposing endpoints for training pipeline status while also serving as the execution environment for scheduled pipeline work. It is built from local source code, integrates with the homepage dashboard for operational visibility, and in practice has carried both API-serving and ML job duties on the homelab host.

That dual role makes it operationally significant: the same container can remain "up" for health checks while a scheduled Python process inside its Docker scope is OOM-killed. The 2026-04-26 checkpoint also records a stronger daily guardrail for this service, where the routine pipeline path was changed to `python main.py pipeline --skip-training` so daily refreshes can reuse production models instead of retraining inside the shared container.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

The nba-ml-api container is the execution environment for status tracking, prediction refreshes, and some historically overloaded training workflows, which is why it keeps reappearing in OOM investigations. The newer checkpoint clarifies that `.State.OOMKilled=true` can coexist with a still-running API container, so operators need host-kernel evidence and scheduler/process correlation instead of assuming the container itself fully crashed.

## Associated Concepts

- **[[Training Pipeline Status Tracking in ML Systems]]** — nba-ml-api exposes the status tracker API endpoint.
- **[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]** — nba-ml-api was OOM-killed and required remediation.
- **[[Skip-Training Daily Pipeline Guardrails in Shared ML Containers]]** — the daily scheduled path now prefers inference-only refresh work over full retraining inside this shared container.

## Related Entities

- **[[NBA ML Engine]]** — Parent ML pipeline orchestrated by nba-ml-api.
- **[[MinutesModel]]** — Model trained by nba-ml-api as first pipeline stage.
- **[[Qdrant]]** — Monitored via homepage dashboard, affected by network isolation.

## Sources

- [[Copilot Session Checkpoint: Training Status Tracker and OOM Fix]] — where this entity was mentioned
- [[Copilot Session Checkpoint: OOM Mitigation and Follow-Up]] — documents the `--skip-training` daily guardrail and the follow-up host-level OOM investigation
