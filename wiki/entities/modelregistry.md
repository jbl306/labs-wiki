---
title: "ModelRegistry"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "924e132f95d9fa94650d78f540b91683d2ddb7c4f20d9fb9d776cf74f1885c5a"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-retrain-in-progress-742b0d94.md
  - raw/2026-04-18-copilot-session-sprint-58-shap-bug-planning-dfccfb5c.md
quality_score: 100
concepts:
  - modelregistry
related:
  - "[[SHAP Analysis Bug Resolution In NBA ML Engine]]"
  - "[[Copilot Session Checkpoint: Sprint 58 SHAP Bug Planning]]"
  - "[[NBA ML Engine]]"
  - "[[EnsembleModel]]"
tier: hot
tags: [database, artifact tracking, ML registry]
---

# ModelRegistry

## Overview

ModelRegistry is a database schema used in NBA ML Engine to track production models, their artifact paths, metrics, and configuration snapshots. It is queried for model selection and artifact loading during explainability and prediction workflows.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Dataset |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

ModelRegistry's schema drift was a root cause of the SHAP analysis bug, requiring robust query and artifact resolution logic. It is essential for reliable model deployment and explainability.

## Associated Concepts

- **[[SHAP Analysis Bug Resolution In NBA ML Engine]]** — Source of bug and fix target

## Related Entities

- **[[NBA ML Engine]]** — Parent ML pipeline
- **[[EnsembleModel]]** — co-mentioned in source (Model)

## Sources

- [[Copilot Session Checkpoint: Sprint 58 SHAP Bug Planning]] — where this entity was mentioned
- [[Copilot Session Checkpoint: Sprint 10 Retrain In Progress]] — additional source
