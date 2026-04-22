---
title: "PRA Composite Prediction"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "e3e47d55fb1d0008f60d9a2e427faad4b28e2a2e353601179a533125dc59d19e"
sources:
  - raw/2026-04-18-copilot-session-sprint-56-no-retrain-fixes-planning-895454cb.md
quality_score: 69
concepts:
  - pra-composite-prediction
related:
  - "[[Stat Exclusion Policy In ML Prediction Pipelines]]"
  - "[[Copilot Session Checkpoint: Sprint 56 No-Retrain Fixes Planning]]"
  - "[[NBA-ML Model Registry]]"
tier: hot
tags: [pra, nba-ml, stat, prediction, deprecated]
---

# PRA Composite Prediction

## Overview

PRA composite prediction is a specific stat prediction target in the NBA-ML pipeline, aggregating points, rebounds, and assists into a single composite value. It is generated in inference routines and surfaced in dashboards, but was disabled in Sprint 56 due to quota exhaustion and reliability concerns.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Model |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Deprecated |

## Relevance

PRA was a key prediction target but became problematic due to API quota exhaustion and model drift. Its exclusion required code and UI updates, database cleanup, and policy revision, serving as a case study in stat exclusion management.

## Associated Concepts

- **[[Stat Exclusion Policy In ML Prediction Pipelines]]** — PRA was excluded via policy updates and code gating.

## Related Entities

- **[[NBA-ML Model Registry]]** — Registry entry for PRA was demoted.

## Sources

- [[Copilot Session Checkpoint: Sprint 56 No-Retrain Fixes Planning]] — where this entity was mentioned
