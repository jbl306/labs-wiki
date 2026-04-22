---
title: "RidgeModel"
type: entity
created: 2026-04-18
last_verified: 2026-04-22
source_hash: "8e3ec5b24e92a02a9a1b03fb00f1bdd35fbc8dbe8d7723b1a284751ce576ff29"
sources:
  - raw/2026-04-18-copilot-session-sprint-59-shap-coverage-implementation-9a231f70.md
quality_score: 63
concepts:
  - ridgemodel
related:
  - "[[SHAP Coverage Extension for Ridge and Ensemble Models]]"
  - "[[Copilot Session Checkpoint: Sprint 59 SHAP Coverage Implementation]]"
  - "[[SHAP (SHapley Additive exPlanations)]]"
  - "[[EnsembleModel]]"
tier: hot
tags: [ridge, nba-ml-engine, explainability]
---

# RidgeModel

## Overview

RidgeModel is a wrapper for Ridge regression models in NBA ML Engine, incorporating a StandardScaler for feature normalization. SHAP LinearExplainer is used for explainability, ensuring SHAP values are computed on scaled features.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Model |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

RidgeModel supports robust linear regression predictions and transparent feature attribution via SHAP, critical for sports analytics and model debugging.

## Associated Concepts

- **[[SHAP Coverage Extension for Ridge and Ensemble Models]]** — RidgeModel is a key target for SHAP explainability extension.

## Related Entities

- **[[SHAP (SHapley Additive exPlanations)]]** — Used for explainability of RidgeModel predictions.
- **[[EnsembleModel]]** — co-mentioned in source (Model)

## Sources

- [[Copilot Session Checkpoint: Sprint 59 SHAP Coverage Implementation]] — where this entity was mentioned
