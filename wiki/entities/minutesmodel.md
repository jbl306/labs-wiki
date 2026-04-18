---
title: "MinutesModel"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "665c60129067f8fba29792521cb202b0e0ab91fc22982f1f58081019b034c549"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-13-model-improvements-code-5db17c4d.md
  - raw/2026-04-18-copilot-session-training-status-tracker-and-oom-fix-6c60a486.md
  - raw/2026-04-18-copilot-session-sprint-57-ensemble-save-diagnosis-e2943da5.md
quality_score: 100
concepts:
  - minutesmodel
related:
  - "[[Copilot Session Checkpoint: Sprint 57 Ensemble Save Diagnosis]]"
  - "[[NBA ML Engine]]"
  - "[[EnsembleModel]]"
tier: hot
tags: [minutes-model, artifact-validation, ml-model]
---

# MinutesModel

## Overview

MinutesModel is a statistical model within the NBA ML Engine focused on predicting player minutes. It is retrained as part of Sprint 57, with artifact saving and registry promotion validated through hardened gates.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Model |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

MinutesModel's retraining and artifact validation are part of the Sprint 57 workflow, ensuring that its production artifact is reliably saved and promoted.

## Associated Concepts

- **Save-Round-Trip Gate for Model Artifact Validation** — MinutesModel artifacts are validated with round-trip gates.

## Related Entities

- **[[NBA ML Engine]]** — Component of the NBA ML Engine pipeline
- **[[EnsembleModel]]** — co-mentioned in source (Model)

## Sources

- [[Copilot Session Checkpoint: Sprint 57 Ensemble Save Diagnosis]] — where this entity was mentioned
- [[Copilot Session Checkpoint: Training Status Tracker and OOM Fix]] — additional source
- [[Copilot Session Checkpoint: Sprint 13 Model Improvements Code]] — additional source
