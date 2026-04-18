---
title: "nba-ml-api"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "5696101c1ddba558560149a708018979e6d8425067b82872f36a6d08784426d9"
sources:
  - raw/2026-04-18-copilot-session-training-status-tracker-and-oom-fix-6c60a486.md
quality_score: 100
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

nba-ml-api is a Dockerized API service for the NBA ML Engine, exposing endpoints for training pipeline status and orchestrating model training jobs. It is built from local source code and integrates with the homepage dashboard for real-time analytics.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

The nba-ml-api container is the execution environment for model training and status tracking, and was the site of the OOM failure. It is critical for operational visibility and recovery workflows.

## Associated Concepts

- **[[Training Pipeline Status Tracking in ML Systems]]** — nba-ml-api exposes the status tracker API endpoint.
- **[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]** — nba-ml-api was OOM-killed and required remediation.

## Related Entities

- **[[NBA ML Engine]]** — Parent ML pipeline orchestrated by nba-ml-api.
- **[[MinutesModel]]** — Model trained by nba-ml-api as first pipeline stage.
- **[[Qdrant]]** — Monitored via homepage dashboard, affected by network isolation.

## Sources

- [[Copilot Session Checkpoint: Training Status Tracker and OOM Fix]] — where this entity was mentioned
