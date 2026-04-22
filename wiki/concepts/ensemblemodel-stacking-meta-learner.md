---
title: "EnsembleModel Stacking Meta-Learner"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "2dd27a20077564eb88e056625dfe5cd1c2c8abd76362bdf39f21f0b3da93e67f"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-retrained-models-deploying-improvements-59ba9a6c.md
quality_score: 75
concepts:
  - ensemblemodel-stacking-meta-learner
related:
  - "[[Ensemble Model Save-Round-Trip Validation Gate]]"
  - "[[LightGBM]]"
  - "[[Copilot Session Checkpoint: Retrained Models, Deploying Improvements]]"
tier: hot
tags: [ensemble learning, stacking, nba analytics, machine learning]
---

# EnsembleModel Stacking Meta-Learner

## Overview

EnsembleModel is a stacking meta-learner that combines predictions from multiple base models—XGBoost, LightGBM, RandomForest, and Ridge regression—using 3-fold cross-validation to improve predictive performance. It was the best performing model for eight out of nine NBA stat prediction categories in this sprint.

## How It Works

Stacking is an ensemble learning technique that trains a meta-model to combine the predictions of several base learners, aiming to leverage their complementary strengths and reduce individual model biases. The EnsembleModel uses four base models: XGBoost, LightGBM, RandomForest, and Ridge regression.

The training process involves the following steps:

1. **Base Model Training:** Each base model is trained on the training dataset using features and target variables.

2. **Cross-Validation Predictions:** Using 3-fold cross-validation, each base model generates out-of-fold predictions on the training data. These predictions serve as new features for the meta-learner.

3. **Meta-Learner Training:** A meta-model (often a simple model like Ridge regression or logistic regression) is trained on the out-of-fold predictions to learn how to best combine the base models' outputs.

4. **Final Model:** For inference, base models generate predictions on new data, which are then combined by the meta-learner to produce the final prediction.

This approach reduces overfitting by using cross-validation and improves accuracy by combining diverse model types. The EnsembleModel outperformed individual models in most stat categories, demonstrating the benefit of stacking.

The exception was the block stat (blk), where RidgeModel alone performed best, indicating that simpler linear models may suffice for some prediction targets.

The LSTM model underperformed, showing 2-3 times higher validation MSE and early stopping at 10-12 epochs, suggesting that sequence modeling was less effective for these tabular features.

## Key Properties

- **Base Models:** XGBoost, LightGBM, RandomForest, Ridge regression.
- **Cross-Validation:** 3-fold CV used to generate meta-features for stacking.
- **Performance:** Best validation and test MSE for 8 of 9 stat categories.
- **Training Data:** 95,004 rows × 341 columns feature matrix with time-based splits.

## Limitations

Stacking increases training complexity and computational cost due to multiple model trainings and cross-validation. It requires careful management of data leakage to prevent overfitting. The meta-learner's performance depends on the quality of base models and diversity among them. In some cases, simpler models like Ridge regression may outperform the ensemble, as seen with the block stat.

## Example

Pseudocode for stacking training:

```python
# Split training data into 3 folds
folds = KFold(n_splits=3)
meta_features = np.zeros((n_samples, n_base_models))

for i, base_model in enumerate(base_models):
    for train_idx, val_idx in folds.split(X_train):
        base_model.fit(X_train[train_idx], y_train[train_idx])
        preds = base_model.predict(X_train[val_idx])
        meta_features[val_idx, i] = preds

# Train meta-learner on out-of-fold predictions
meta_learner.fit(meta_features, y_train)

# For inference:
base_preds = np.column_stack([model.predict(X_test) for model in base_models])
final_preds = meta_learner.predict(base_preds)
```

Example training result snippet:

| Stat | Best Model    | Val MSE | Test MSE |
|-------|--------------|---------|----------|
| pts   | EnsembleModel| 43.7283 | 41.6886  |
| blk   | RidgeModel   | 0.7250  | 0.6214   |


## Relationship to Other Concepts

- **[[Ensemble Model Save-Round-Trip Validation Gate]]** — Related to validation and deployment of ensemble models.
- **XGBoost** — One of the base models used in the ensemble.
- **[[LightGBM]]** — One of the base models used in the ensemble.
- **RandomForest** — One of the base models used in the ensemble.
- **Ridge Regression** — One of the base models and also the meta-learner candidate.

## Practical Applications

Stacking ensembles like EnsembleModel are widely used in production ML systems to improve prediction accuracy by combining diverse model strengths. This approach is particularly useful in tabular data domains such as sports analytics, finance, and healthcare, where multiple models capture different aspects of the data. It supports robust predictions and can be integrated into automated retraining pipelines for continuous improvement.

## Sources

- [[Copilot Session Checkpoint: Retrained Models, Deploying Improvements]] — primary source for this concept
