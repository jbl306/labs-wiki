---
title: "NBA ML Prediction Pipeline"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "e46b28ceb3142b4379144f0651127cee40410b71fb087908b377ab58ca92a883"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-pipeline-resilience-fixes-dashboard-metrics-inve-3ea0d6d8.md
quality_score: 67
concepts:
  - nba-ml-prediction-pipeline
related:
  - "[[Pipeline Resilience in Machine Learning Systems]]"
  - "[[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]"
  - "[[MLflow Resilience and Fallback Mechanisms in Model Training]]"
  - "[[Copilot Session Checkpoint: Pipeline Resilience Fixes, Dashboard Metrics Investigation]]"
  - "[[Odds API]]"
  - "[[SportsGameOdds (SGO) API]]"
tier: hot
tags: [nba, machine-learning, sports-betting, ml-pipeline]
---

# NBA ML Prediction Pipeline

## Overview

An NBA machine learning prediction system that generates player stat predictions and prop lines for sports betting. It includes components for model training, inference, dashboard visualization, and data ingestion from external APIs such as the-odds-api.com and SportsGameOdds (SGO).

## Key Facts

| Field | Value |
|-------|-------|
| Type | Framework |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

The pipeline is the context for the resilience fixes and dashboard metrics investigation. It uses ensemble and base models for predictions, MLflow for experiment tracking, and external APIs for prop line data. Failures in this pipeline caused stale dashboard data and metric discrepancies.

## Associated Concepts

- **[[Pipeline Resilience in Machine Learning Systems]]** — Pipeline architecture and resilience
- **[[Dashboard Metrics Consistency and Hit Rate Discrepancy Analysis]]** — Dashboard metrics reporting
- **[[MLflow Resilience and Fallback Mechanisms in Model Training]]** — Training orchestration

## Related Entities

- **[[Odds API]]** — External data source for prop lines
- **[[SportsGameOdds (SGO) API]]** — Alternative external data source
- **MLflow** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Pipeline Resilience Fixes, Dashboard Metrics Investigation]] — where this entity was mentioned
