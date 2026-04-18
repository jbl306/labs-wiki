---
title: "Quantile Crossing Fix in Uncertainty Prediction"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "1a8605793607a924fae33927ca1c4abc23aa36d89dbda589fb5634f468d8ae67"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-retrain-in-progress-742b0d94.md
quality_score: 100
concepts:
  - quantile-crossing-fix-uncertainty-prediction
related:
  - "[[Copilot Session Checkpoint: Sprint 10 Retrain In Progress]]"
tier: hot
tags: [quantile regression, uncertainty estimation, XGBoost, LightGBM]
---

# Quantile Crossing Fix in Uncertainty Prediction

## Overview

Quantile crossing occurs when independently trained quantile regression models predict inconsistent intervals (e.g., the 10th percentile prediction is higher than the 90th percentile), violating quantile ordering. This sprint fixed quantile crossing issues in XGBoost and LightGBM models for uncertainty estimation.

## How It Works

The problem arises because quantile models for different quantiles (e.g., 10th and 90th percentiles) are trained independently, so their predictions can cross.

The fix implemented involves stacking the predicted quantiles and enforcing monotonicity by taking element-wise minimum and maximum:

- For the lower quantile (e.g., q10), the prediction is replaced by the element-wise minimum of the q10 and q90 predictions.
- For the upper quantile (e.g., q90), the prediction is replaced by the element-wise maximum of the q10 and q90 predictions.

This ensures the lower quantile prediction never exceeds the upper quantile prediction.

The implementation uses NumPy's `np.min(np.stack([low, high]), axis=0)` and `np.max(np.stack([low, high]), axis=0)` to enforce this constraint after model prediction.

This fix was applied in the `predict_with_uncertainty()` methods of both `xgboost_model.py` and `lightgbm_model.py`.

By correcting quantile crossing, the models produce valid uncertainty intervals, improving reliability of uncertainty estimates used in downstream decision-making.

## Key Properties

- **Applicability:** Fix applies to quantile regression models trained independently for different quantiles.
- **Implementation:** Uses NumPy stacking and element-wise min/max to enforce monotonicity.
- **Models Affected:** XGBoost and LightGBM quantile regression models.

## Limitations

This fix is a post-processing step and does not guarantee optimal quantile estimates; it only enforces monotonicity. It may mask underlying model misspecification or training issues. More sophisticated joint quantile regression methods could provide better uncertainty modeling.

## Example

Code snippet:

```python
low_pred = model.predict_q10(X)
high_pred = model.predict_q90(X)
corrected_low = np.minimum(low_pred, high_pred)
corrected_high = np.maximum(low_pred, high_pred)
return corrected_low, corrected_high
```


## Relationship to Other Concepts

- **Quantile Regression** — Quantile crossing is a known issue in quantile regression models.

## Practical Applications

Ensures valid prediction intervals for NBA player stat models, improving confidence in uncertainty estimates used for risk-aware decision-making or downstream analytics.

## Sources

- [[Copilot Session Checkpoint: Sprint 10 Retrain In Progress]] — primary source for this concept
