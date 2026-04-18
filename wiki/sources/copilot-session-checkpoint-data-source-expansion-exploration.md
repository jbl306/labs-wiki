---
title: "Copilot Session Checkpoint: Data Source Expansion Exploration"
type: source
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9f90b86f2aab32a86e7ca650c6477398444e04958726c5b3ca2ccd9f465e7581"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-data-source-expansion-exploration-b12f747f.md
quality_score: 100
concepts:
  - data-source-expansion-nba-ml-prediction-platform
  - homelab-server-deployment-nba-ml-platform
  - feature-engineering-pipeline-nba-ml-platform
related:
  - "[[Data Source Expansion for NBA ML Prediction Platform]]"
  - "[[Homelab Server Deployment Architecture for NBA ML Platform]]"
  - "[[Feature Engineering Pipeline for NBA ML Platform]]"
  - "[[NBA ML Engine]]"
  - "[[EnsembleModel]]"
tier: hot
tags: [deployment, nba-ml-engine, fileback, dashboard, data ingestion, checkpoint, copilot-session, nba, homelab, feature engineering, durable-knowledge, machine learning, ensemble learning]
checkpoint_class: durable-debugging
retention_mode: retain
---

# Copilot Session Checkpoint: Data Source Expansion Exploration

## Summary

This document captures a multi-sprint development campaign focused on expanding data sources and improving an NBA ML prediction platform deployed on a homelab server. It details completed phases of data ingestion and feature engineering, ongoing work to implement additional data sources and features, deployment strategies, and plans for model retraining and evaluation.

## Key Points

- Completed initial phases of data source expansion including position backfill, starter data backfill, and CDN advanced stats ingestion with over 270K rows.
- Identified and planned implementation for additional data sources such as player tracking stats, hustle stats, and Basketball Reference advanced metrics.
- Outlined deployment on a homelab server using Docker containers, with scheduled cron jobs and a multi-component architecture including TimescaleDB, MLflow, FastAPI, Streamlit dashboard, and Ofelia scheduler.
- Planned model retraining with expanded feature sets and comprehensive validation and evaluation reports comparing model performance before and after data expansion.

## Concepts Extracted

- **[[Data Source Expansion for NBA ML Prediction Platform]]** — Data source expansion is a critical process in enhancing the predictive accuracy and robustness of machine learning models by integrating additional relevant datasets. In the context of an NBA ML prediction platform, expanding data sources involves ingesting new basketball statistics from APIs, CDNs, and web scrapers to enrich feature sets for model training and evaluation.
- **[[Homelab Server Deployment Architecture for NBA ML Platform]]** — The NBA ML prediction platform is deployed on a homelab server using Docker containers to encapsulate all components. This architecture supports local development, deployment, and scheduled execution of data pipelines and model training in an isolated environment.
- **[[Feature Engineering Pipeline for NBA ML Platform]]** — Feature engineering transforms raw basketball data into meaningful predictive features that improve model performance. The pipeline integrates newly ingested data sources to compute rolling statistics, starter indicators, and advanced metrics for each player and game.

## Entities Mentioned

- **[[NBA ML Engine]]** — The NBA ML Engine is a machine learning platform designed for predicting NBA player and game statistics. It integrates multiple data sources including NBA APIs, CDN data, and Basketball Reference metrics, and employs an ensemble model combining XGBoost, LightGBM, RandomForest, and Ridge regression. The platform is deployed on a homelab server using Docker containers and supports scheduled data ingestion, model training, and dashboard visualization.
- **Homelab Server (beelink-gti13)** — The homelab server named beelink-gti13 hosts the NBA ML Engine and its associated services in a local Docker containerized environment. It runs TimescaleDB for data storage, MLflow for model tracking, FastAPI for API services, Streamlit for dashboards, and Ofelia for cron scheduling. This server enables development, deployment, and scheduled execution of the entire NBA ML prediction stack without external cloud dependencies.
- **[[EnsembleModel]]** — EnsembleModel is a stacking meta-learner used in the NBA ML Engine that combines predictions from multiple base learners including XGBoost, LightGBM, RandomForest, and Ridge regression models. It achieved the best performance in 8 out of 9 statistical categories during model retraining and evaluation.

## Notable Quotes

> "CDN advanced stats accuracy: Exact for ts_pct/efg_pct/ast_tov/pie. ~95% for usg_pct/ast_pct/pace. Team proxy for off_rating/def_rating/net_rating (need stats.nba.com overlay for individual values)." — Technical Details Section
> "EnsembleModel: Stacking meta-learner over XGBoost+LightGBM+RandomForest+Ridge. Won 8/9 categories. RidgeModel won BLK." — Technical Details Section
> "NBA API rate limit: 0.6s delay between requests. No hard limit but aggressive scraping gets IP-blocked." — Technical Details Section

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-data-source-expansion-exploration-b12f747f.md` |
| Type | note |
| Author | Unknown |
| Date | 2026-04-18T03:23:51.483387Z |
| URL | N/A |
