---
title: "Walk-Forward Cross-Validation for Model Selection"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "09d0f25cf67625d2215d0a83135693fea032d2bab65425e15c21d99f6b87103a"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-implementing-sprint-29-ml-improvements-986267e7.md
quality_score: 61
concepts:
  - walk-forward-cross-validation-for-model-selection
related:
  - "[[Copilot Session Checkpoint: Implementing Sprint 29 ML Improvements]]"
tier: hot
tags: [machine learning, cross-validation, time-series, model selection]
---

# Walk-Forward Cross-Validation for Model Selection

## Overview

Walk-forward cross-validation (CV) is a time-series aware validation technique used to evaluate and select machine learning models by simulating how models perform on sequential data splits. It is critical for time-dependent data to avoid lookahead bias and ensure robust model generalization.

## How It Works

Walk-forward CV partitions the dataset into multiple sequential training and validation folds, where each fold trains on data up to a certain time point and validates on the immediately following period. This simulates real-world forecasting where future data is unseen during training. The process involves:

1. Splitting the data into an expanding window of training sets and corresponding validation sets.
2. Training the model on each training fold and evaluating performance on the validation fold.
3. Collecting metrics such as mean squared error (MSE) for each fold.
4. Aggregating these metrics (e.g., average validation MSE) to assess model quality.

In this implementation, the function `_run_walk_forward_cv()` was refactored to return a nested dictionary of metrics instead of None, enabling programmatic model selection based on CV results. Model registration is deferred until CV completes, and the best model is chosen by a fallback chain prioritizing average validation MSE (`cv_avg_val_mse`), then validation, test, and training MSEs.

This approach prevents overfitting to any single fold and provides a realistic estimate of model performance on future data. It is especially suitable for the NBA ML Engine's time-series sports prediction tasks where temporal ordering is crucial.

Trade-offs include increased computational cost due to multiple training runs and complexity in fold construction. However, the benefits in reliable model selection outweigh these costs in production pipelines.

## Key Properties

- **Return Type:** Returns a nested dictionary of CV metrics: dict[str, dict[str, dict[str, float]]], enabling detailed performance tracking.
- **Model Selection Criteria:** Uses a fallback chain prioritizing cv_avg_val_mse → val_mse → test_mse → train_mse for robust best model selection.
- **Fold Construction:** Expanding window splits with smart imputation applied to training and validation sets.

## Limitations

Walk-forward CV can be computationally expensive due to repeated training. It assumes temporal stationarity within folds, which may not hold if data distribution shifts. Also, fold sizes and number must be carefully chosen to balance bias and variance in estimates.

## Example

Pseudocode for walk-forward CV fold construction and evaluation:

```python
for fold in range(num_folds):
    train_data = data[:fold_end_index]
    val_data = data[fold_end_index:fold_end_index+val_size]
    model.train(train_data)
    val_pred = model.predict(val_data.features)
    mse = mean_squared_error(val_data.labels, val_pred)
    metrics[fold] = mse
average_mse = sum(metrics.values()) / len(metrics)
```

Model registration occurs after all folds complete, selecting the model with the lowest average validation MSE.

## Relationship to Other Concepts

- **Optuna Hyperparameter Tuning** — Walk-forward CV folds are passed to Optuna tuner for robust hyperparameter optimization.

## Practical Applications

Used in time-series forecasting tasks such as sports analytics, financial modeling, and any domain where temporal order must be preserved during model validation to avoid lookahead bias.

## Sources

- [[Copilot Session Checkpoint: Implementing Sprint 29 ML Improvements]] — primary source for this concept
