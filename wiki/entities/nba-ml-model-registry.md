---
title: "NBA-ML Model Registry"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "e3e47d55fb1d0008f60d9a2e427faad4b28e2a2e353601179a533125dc59d19e"
sources:
  - raw/2026-04-18-copilot-session-sprint-55-planning-and-exploration-be98e3c5.md
  - raw/2026-04-18-copilot-session-nba-ml-oom-fix-and-docs-cleanup-52d24b9f.md
  - raw/2026-04-18-copilot-session-sprint-56-no-retrain-fixes-planning-895454cb.md
quality_score: 91
concepts:
  - nba-ml-model-registry
related:
  - "[[Artifact Registry Validation In ML Pipelines]]"
  - "[[Stat Exclusion Policy In ML Prediction Pipelines]]"
  - "[[Copilot Session Checkpoint: Sprint 56 No-Retrain Fixes Planning]]"
  - "[[PRA Composite Prediction]]"
tier: hot
tags: [model-registry, nba-ml, production, artifact, database]
---

# NBA-ML Model Registry

## Overview

The NBA-ML Model Registry is a production database table that tracks all deployed machine learning models for NBA stats prediction, including their artifact paths, production status, and configuration snapshots. It is central to model promotion, artifact validation, and operational reliability, ensuring only valid models are served in the pipeline.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Dataset |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

The registry is critical for artifact validation, stat exclusion, and model lifecycle management. It enables demotion of missing or deprecated models, supports startup validation routines, and is referenced throughout code audits and sprint planning.

## Associated Concepts

- **[[Artifact Registry Validation In ML Pipelines]]** — Registry entries are the subject of artifact validation routines.
- **[[Stat Exclusion Policy In ML Prediction Pipelines]]** — Registry entries for excluded stats are demoted or removed.

## Related Entities

- **[[PRA Composite Prediction]]** — co-mentioned in source (Model)

## Sources

- [[Copilot Session Checkpoint: Sprint 56 No-Retrain Fixes Planning]] — where this entity was mentioned
- [[Copilot Session Checkpoint: NBA ML OOM Fix And Docs Cleanup]] — additional source
- [[Copilot Session Checkpoint: Sprint 55 Planning and Exploration]] — additional source
