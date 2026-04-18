---
title: "Copilot Session Checkpoint: Sprint 13 Model Improvements Code"
type: source
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9583aca364f19d189456564e8242665d819c8e046298a36e6032014ff646bea6"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-13-model-improvements-code-5db17c4d.md
quality_score: 100
concepts:
  - minutes-prediction-sub-model
  - edge-threshold-optimizer-with-kelly-criterion
  - dynamic-ensemble-weighting
  - binary-over-under-classifier
related:
  - "[[Minutes Prediction Sub-Model]]"
  - "[[Dynamic Ensemble Weighting]]"
  - "[[MinutesModel]]"
  - "[[OverUnderClassifier]]"
  - "[[Edge Optimizer]]"
  - "[[EnsembleModel]]"
tier: hot
tags: [nba, model improvements, checkpoint, copilot-session, dashboard, sports betting, homelab, machine learning, xgboost, ensemble learning, durable-knowledge, agents, fileback, nba-ml-engine]
---

# Copilot Session Checkpoint: Sprint 13 Model Improvements Code

## Summary

This document details the development progress and technical implementation of Sprint 13 for an NBA ML prediction engine project. Key improvements include a minutes prediction sub-model, an edge threshold optimizer using the Kelly criterion, dynamic ensemble weighting, and a binary over/under classifier, with code fully implemented and import-validated but pending retraining and deployment.

## Key Points

- Implemented four major model improvements: MinutesModel, Edge Threshold Optimizer, Dynamic Ensemble Weighting, and OverUnderClassifier.
- MinutesModel uses XGBoost with feature selection for predicting player minutes, feeding into other stat models.
- Edge threshold optimization applies walk-forward cross-validation and fractional Kelly betting for threshold tuning.
- Dynamic ensemble weighting uses inverse-MAE from recent data for weighting model predictions.
- OverUnderClassifier is a calibrated binary classifier supplementing regression models for over/under prop bets.
- Training optimization planned to reduce long training times via parallelism, lighter Optuna tuning, and early stopping.

## Concepts Extracted

- **[[Minutes Prediction Sub-Model]]** — The Minutes Prediction Sub-Model is a specialized machine learning model designed to predict the number of minutes a player will play in a game. This prediction is crucial as it serves as an input feature for other statistical models within the NBA ML prediction engine, improving overall accuracy by providing a refined estimate of player participation.
- **Edge Threshold Optimizer with Kelly Criterion** — The Edge Threshold Optimizer is a system designed to optimize betting thresholds for statistical predictions by applying walk-forward cross-validation and fractional Kelly betting. It aims to find thresholds that maximize expected returns while avoiding overfitting and excessive risk.
- **[[Dynamic Ensemble Weighting]]** — Dynamic Ensemble Weighting is a technique to improve predictive performance by combining multiple models' outputs using weights that adapt based on recent model performance. This approach introduces recency bias to emphasize models that perform better on the most recent data, enhancing responsiveness to changing conditions.
- **Binary Over/Under Classifier** — The Binary Over/Under Classifier is a supplemental machine learning model designed to predict whether a player's statistical performance will be over or under a given prop line. It complements regression models by providing calibrated binary probability estimates, improving decision-making in betting contexts.

## Entities Mentioned

- **[[MinutesModel]]** — MinutesModel is an XGBoost-based regression model designed to predict player minutes in NBA games. It uses a filtered subset of features relevant to minutes played and integrates its predictions as features for other statistical models in the NBA ML prediction engine.
- **[[OverUnderClassifier]]** — OverUnderClassifier is an XGBoost-based binary classifier with isotonic calibration designed to predict whether a player's performance will be over or under a specified prop line. It supplements regression models by providing calibrated probability estimates for over/under betting decisions.
- **[[Edge Optimizer]]** — Edge Optimizer is a module that implements threshold optimization for statistical predictions using walk-forward cross-validation and fractional Kelly betting. It calculates optimized thresholds and bet sizes to maximize expected returns while managing risk.
- **[[EnsembleModel]]** — EnsembleModel is the combined predictive model that integrates multiple base models' outputs using either a Ridge regression meta-learner or dynamic weighting based on recent performance (inverse MAE). It supports dual prediction modes and persists weighting configurations.

## Notable Quotes

No notable quotes.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-13-model-improvements-code-5db17c4d.md` |
| Type | note |
| Author | Unknown |
| Date | 2026-04-18T03:23:51.483387Z |
| URL | N/A |
