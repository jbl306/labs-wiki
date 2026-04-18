---
title: "OverUnderClassifier"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9583aca364f19d189456564e8242665d819c8e046298a36e6032014ff646bea6"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-13-model-improvements-code-5db17c4d.md
quality_score: 100
concepts:
  - overunderclassifier
related:
  - "[[Binary Over/Under Classifier with Isotonic Calibration]]"
  - "[[Copilot Session Checkpoint: Sprint 13 Model Improvements Code]]"
  - "[[MinutesModel]]"
  - "[[Edge Optimizer]]"
  - "[[EnsembleModel]]"
tier: hot
tags: [XGBoost, binary classification, calibration]
---

# OverUnderClassifier

## Overview

OverUnderClassifier is an XGBoost-based binary classifier used in the NBA ML engine to predict whether a player's statistic will be over or under a betting line. It applies isotonic calibration for improved probability estimates and operates as a supplemental model alongside regression models.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Model |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

This classifier provides direct binary predictions for prop bets, enhancing the system's ability to support betting decisions with calibrated probabilities.

## Associated Concepts

- **[[Binary Over/Under Classifier with Isotonic Calibration]]** — Implementation of this concept

## Related Entities

- **[[MinutesModel]]** — co-mentioned in source (Model)
- **[[Edge Optimizer]]** — co-mentioned in source (Tool)
- **[[EnsembleModel]]** — co-mentioned in source (Model)

## Sources

- [[Copilot Session Checkpoint: Sprint 13 Model Improvements Code]] — where this entity was mentioned
