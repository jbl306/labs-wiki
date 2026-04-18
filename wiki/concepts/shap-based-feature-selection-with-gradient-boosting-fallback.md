---
title: "SHAP-Based Feature Selection with Gradient Boosting Fallback"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "09d0f25cf67625d2215d0a83135693fea032d2bab65425e15c21d99f6b87103a"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-implementing-sprint-29-ml-improvements-986267e7.md
quality_score: 0
concepts:
  - shap-based-feature-selection-with-gradient-boosting-fallback
related:
  - "[[Gradient Boosting Machine (GBM)]]"
  - "[[Copilot Session Checkpoint: Implementing Sprint 29 ML Improvements]]"
tier: hot
tags: [feature selection, explainability, shap, gradient boosting]
---

# SHAP-Based Feature Selection with Gradient Boosting Fallback

## Overview

SHAP (SHapley Additive exPlanations) is a method to explain model predictions by assigning each feature an importance value. Using SHAP for feature selection helps identify the most influential features for low-R² statistics, improving model interpretability and performance. A fallback to traditional gradient boosting feature importances ensures robustness.

## How It Works

The feature selection process uses `shap.TreeExplainer` applied to a GradientBoostingRegressor model trained on the dataset. To maintain efficiency, the implementation subsamples 500 rows for SHAP value computation, which reduces computational overhead while preserving explanation quality.

Steps involved:

1. Train a GradientBoostingRegressor on the target variable.
2. Use `shap.TreeExplainer` to compute SHAP values for the subsampled data.
3. Aggregate SHAP values to obtain feature importances.
4. If SHAP computation fails (due to exceptions or model incompatibility), fallback to using the model's built-in `feature_importances_` attribute.
5. Select features based on their SHAP importance scores, focusing on low-R² stats such as steals, blocks, field goal percentage, and free throw percentage.

This approach leverages SHAP's game-theoretic foundation to provide consistent and locally accurate feature attributions, which are more informative than simple gain or split counts. The fallback mechanism ensures the system remains operational even if SHAP fails, maintaining robustness in production.

Trade-offs include the additional dependency on the SHAP library and the need to manage subsampling to balance speed and accuracy.

## Key Properties

- **Subsampling:** Uses 500-row subsample for SHAP value computation to optimize speed.
- **Fallback Mechanism:** Falls back to GradientBoostingRegressor's feature_importances_ if SHAP fails.
- **Targeted Stats:** Applied specifically to low-R² statistics where feature selection can improve model quality.

## Limitations

SHAP computation can be resource-intensive on large datasets. Subsampling may reduce explanation fidelity. The fallback method provides less nuanced feature importance, potentially affecting selection quality.

## Example

Python snippet illustrating SHAP-based feature importance extraction with fallback:

```python
import shap
from sklearn.ensemble import GradientBoostingRegressor

def get_shap_importances(X, y):
    model = GradientBoostingRegressor().fit(X, y)
    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X.sample(500))
        importances = np.abs(shap_values).mean(axis=0)
    except Exception:
        importances = model.feature_importances_
    return importances
```

This function returns feature importance scores used for feature selection.

## Relationship to Other Concepts

- **[[Gradient Boosting Machine (GBM)]]** — SHAP explanations are computed on GBM models for feature importance.

## Practical Applications

Improves feature selection in machine learning pipelines for sports analytics and other domains with complex feature interactions and low signal-to-noise ratios in certain target variables.

## Sources

- [[Copilot Session Checkpoint: Implementing Sprint 29 ML Improvements]] — primary source for this concept
