---
title: "NBA ML Prediction Platform Sprint Workflow"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "2dd27a20077564eb88e056625dfe5cd1c2c8abd76362bdf39f21f0b3da93e67f"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-retrained-models-deploying-improvements-59ba9a6c.md
quality_score: 67
concepts:
  - nba-ml-prediction-platform-sprint-workflow
related:
  - "[[Ensemble Model Save-Round-Trip Validation Gate]]"
  - "[[Pipeline Resilience in Machine Learning Systems]]"
  - "[[Copilot Session Checkpoint: Retrained Models, Deploying Improvements]]"
tier: hot
tags: [machine learning, deployment, model retraining, docker, nba analytics]
---

# NBA ML Prediction Platform Sprint Workflow

## Overview

This concept covers the end-to-end workflow of conducting a sprint to improve an NBA machine learning prediction platform, including branching, implementation, deployment, retraining, evaluation, and documentation. It is critical for maintaining and enhancing predictive accuracy and system robustness in a production ML environment.

## How It Works

The sprint workflow begins with creating a new GitHub branch from an existing development branch to isolate changes. The team reviews existing planning documents to identify remaining impactful tasks, including model improvements, dashboard redesign, and bug fixes. Code changes are committed incrementally, such as adding stat-specific edge thresholds and enhancing UI responsiveness for mobile devices.

Deployment involves rebuilding Docker containers for the API and dashboard services using a Docker Compose setup on a homelab server. This server hosts all components including TimescaleDB for time-series data storage, MLflow for experiment tracking, FastAPI for serving APIs, Streamlit for dashboards, and Ofelia as a cron scheduler.

Retraining is performed across nine statistical categories (e.g., points, rebounds, assists) using six model types: XGBoost, LightGBM, RandomForest, Ridge regression, an Ensemble stacking meta-learner, and LSTM. The feature matrix used has 95,004 rows and 341 columns, split into train, validation, and test sets based on dates. Training logs and metrics are recorded in MLflow.

Post-training, predictions are generated and stored, followed by backtesting to evaluate hit rate, profit and loss, and return on investment. A progress tracker markdown document is created to consolidate training and evaluation results. Documentation updates and final git pushes complete the sprint.

This workflow emphasizes automation, reproducibility, and continuous integration/deployment practices to maintain a high-quality ML system. It also includes monitoring and handling of edge cases such as feature mismatch errors and test suite failures due to environment dependencies.

## Key Properties

- **Branching Strategy:** Feature branches created from a redesign branch to isolate improvements and facilitate code review.
- **Model Retraining:** Retraining all nine stat categories with six model types, using a large feature matrix and time-based data splits.
- **Deployment Architecture:** Docker Compose setup running TimescaleDB, MLflow, FastAPI API, Streamlit dashboard, and Ofelia scheduler on a homelab server.
- **Evaluation Metrics:** Validation and test mean squared error (MSE) tracked per model and stat category.
- **Edge Thresholds:** Stat-specific edge thresholds for filtering predictions, improving evaluation precision.

## Limitations

Evaluation is limited by the short historical data available for backtesting (only about 3 days of prop_lines data), which may not reflect long-term model performance. LSTM models underperform significantly and early stop, indicating possible model architecture or training issues. Test suite failures due to missing native libraries on the host environment highlight dependency management challenges.

## Example

Example Git commit message for feature branch:

```
feat(dashboard): timezone-aware queries using ET for game dates
feat: stat-specific edge thresholds, mobile CSS, per-stat hit rate
```

Example command to generate predictions:

```
docker exec nba-ml-api python main.py predict --store
```

Example Docker Compose snippet:

```yaml
services:
  nba-ml-api:
    build: .
    environment:
      - NBA_ML_ENGINE_PATH=/home/jbl/projects/nba-ml-engine
  nba-ml-dashboard:
    build: .
```

Example training results table snippet:

| Stat | Best Model | Val MSE | Test MSE |
|------|------------|---------|----------|
| pts  | EnsembleModel | 43.7283 | 41.6886 |
| blk  | RidgeModel   | 0.7250  | 0.6214  |


## Relationship to Other Concepts

- **[[Ensemble Model Save-Round-Trip Validation Gate]]** — Related to validation and deployment of ensemble models in ML pipelines.
- **[[Pipeline Resilience in Machine Learning Systems]]** — Related to deployment and operational robustness of ML pipelines.

## Practical Applications

This workflow is applicable for teams maintaining production ML systems for sports analytics or similar domains requiring frequent retraining and deployment. It ensures continuous improvement, reproducibility, and operational monitoring, enabling rapid iteration on models and dashboards while maintaining system stability.

## Sources

- [[Copilot Session Checkpoint: Retrained Models, Deploying Improvements]] — primary source for this concept
