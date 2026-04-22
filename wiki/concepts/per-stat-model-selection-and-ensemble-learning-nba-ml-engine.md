---
title: "Per-Stat Model Selection and Ensemble Learning in NBA ML Engine"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "1a8605793607a924fae33927ca1c4abc23aa36d89dbda589fb5634f468d8ae67"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-retrain-in-progress-742b0d94.md
quality_score: 59
concepts:
  - per-stat-model-selection-and-ensemble-learning-nba-ml-engine
related:
  - "[[EnsembleModel Stacking Meta-Learner]]"
  - "[[Feature Engineering Pipeline for NBA ML Platform]]"
  - "[[Copilot Session Checkpoint: Sprint 10 Retrain In Progress]]"
tier: hot
tags: [ensemble-learning, model-selection, sports-analytics, gradient-boosting, ridge-regression]
---

# Per-Stat Model Selection and Ensemble Learning in NBA ML Engine

## Overview

Per-stat model selection involves choosing the best predictive model independently for each target statistic, recognizing that different stats may have different underlying data distributions and predictive patterns. Ensemble learning combines multiple models to improve prediction accuracy and reduce variance, particularly effective for low-variance statistics.

## How It Works

The NBA ML Engine sprint 10 implemented a per-stat model selection architecture where models are trained and evaluated separately for each of nine basketball statistics (e.g., points, rebounds, assists).

For each stat, multiple model families are trained: XGBoost, LightGBM, CatBoost, Ridge regression, Random Forest, and an ensemble model using 3-fold cross-validation stacking.

Model performance is measured by validation mean squared error (val_mse). The best-performing model per stat is selected based on lowest val_mse.

Key observations from the retrain results:

- High-variance stats like points (pts) are best predicted by LightGBM.
- Rebounds (reb) are best predicted by CatBoost.
- Assists (ast) and blocks (blk), which have lower variance, benefit from ensemble models combining multiple base learners.
- Ridge regression is competitive for assists, indicating linear relationships.
- Feature selection is applied selectively, with fewer features used for rare-event stats like steals (stl) and blocks (blk).

Ensemble stacking involves training base models on folds of data and then training a meta-learner on their predictions to reduce variance and improve robustness.

This approach balances bias and variance trade-offs and leverages strengths of different model types per statistic.

Edge cases include stats with very sparse events or noisy measurements where model selection and feature selection become critical.

## Key Properties

- **Model Diversity:** Uses multiple model families to capture different data patterns.
- **Ensemble Stacking:** 3-fold cross-validation stacking reduces variance for low-variance stats.
- **Feature Selection:** Selective feature usage improves performance on rare-event stats.
- **Validation Metric:** Validation MSE guides model selection per statistic.

## Limitations

Requires more computational resources to train multiple models per stat. Ensemble models add complexity and inference latency. Model selection depends on validation data representativeness.

## Example

For the 'ast' stat, the ensemble model achieved val_mse=4.18, narrowly beating Ridge regression at 4.19 and tree-based models, validating the ensemble approach.

## Visual

A table summarizing val_mse by stat and model family shows different best models per stat, highlighting the effectiveness of per-stat selection and ensembles.

## Relationship to Other Concepts

- **[[EnsembleModel Stacking Meta-Learner]]** — Technique used for ensemble predictions
- **[[Feature Engineering Pipeline for NBA ML Platform]]** — Provides features used by models

## Practical Applications

Applied in sports analytics to optimize predictive accuracy for multiple related targets, allowing tailored modeling approaches per statistic and leveraging ensembles for stability.

## Sources

- [[Copilot Session Checkpoint: Sprint 10 Retrain In Progress]] — primary source for this concept
