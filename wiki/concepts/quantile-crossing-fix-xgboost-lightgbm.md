---
title: "Quantile Crossing Fix in XGBoost and LightGBM Models"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "016d553979837ab306dec9cdf9e2309752249db326f2d6c75448f89eba8e6a11"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-complete-and-deployed-cb380016.md
quality_score: 100
concepts:
  - quantile-crossing-fix-xgboost-lightgbm
related:
  - "[[Feature Engineering for NBA ML Engine Sprint 10]]"
  - "[[Copilot Session Checkpoint: Sprint 10 Complete and Deployed]]"
tier: hot
tags: [quantile-regression, xgboost, lightgbm, prediction-intervals]
---

# Quantile Crossing Fix in XGBoost and LightGBM Models

## Overview

Quantile regression models predict conditional quantiles (e.g., 10th and 90th percentiles) independently, which can lead to crossing intervals violating quantile order. Sprint 10 fixed this issue in XGBoost and LightGBM models by post-processing predictions to enforce monotonicity.

## How It Works

XGBoost and LightGBM train separate models for lower and upper quantiles (e.g., q10 and q90). Because these models are independent, the predicted lower quantile can sometimes exceed the upper quantile, causing an invalid interval.

The fix implemented involves:

1. **Stacking Predictions:** Collect the predicted lower and upper quantiles into a stacked numpy array.

2. **Applying Min/Max Operations:** For each prediction point, compute the element-wise minimum for the lower bound and maximum for the upper bound across the stacked predictions.

3. **Replacing Original Predictions:** Use these corrected bounds to ensure the lower quantile is never greater than the upper quantile.

The core code snippet is:
```python
corrected_lower = np.min(np.stack([lower_pred, upper_pred]), axis=0)
corrected_upper = np.max(np.stack([lower_pred, upper_pred]), axis=0)
```

This approach is a simple post-hoc correction that preserves the predictive uncertainty interval's validity without retraining.

It is implemented in the `predict_with_uncertainty` methods of both `xgboost_model.py` and `lightgbm_model.py`.

## Key Properties

- **Independent Quantile Models:** XGBoost/LightGBM train q10 and q90 models separately, causing potential crossing.
- **Post-Processing Correction:** Uses numpy min/max on stacked predictions to enforce monotonic quantile ordering.
- **Implementation Location:** Fixed in predict_with_uncertainty() methods of model classes.

## Limitations

This fix is a heuristic that corrects predictions after inference; it does not address underlying model training issues. It assumes that crossing is rare and can be resolved by simple min/max operations. In cases of frequent crossing, more sophisticated joint quantile regression methods may be needed.

## Example

Pseudocode for quantile crossing fix:
```python
low_pred = model.predict_q10(X)
high_pred = model.predict_q90(X)
corrected_low = np.minimum(low_pred, high_pred)
corrected_high = np.maximum(low_pred, high_pred)
return corrected_low, corrected_high
```

## Relationship to Other Concepts

- **[[Feature Engineering for NBA ML Engine Sprint 10]]** — Improved features support more accurate quantile predictions requiring crossing fixes.

## Practical Applications

Ensures valid prediction intervals in quantile regression models for sports statistics, finance, and other domains requiring uncertainty quantification.

## Sources

- [[Copilot Session Checkpoint: Sprint 10 Complete and Deployed]] — primary source for this concept
