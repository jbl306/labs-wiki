---
title: "Calibration Leakage Fix in Machine Learning Pipelines"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "1544a9390c8a215aeb38b788d3103fd5a18163dc8ce9182c4c6fc36fbb638e43"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-implementing-critical-ml-fixes-sprint-28-9cff218d.md
quality_score: 100
concepts:
  - calibration-leakage-fix-in-machine-learning-pipelines
related:
  - "[[Copilot Session Checkpoint: Implementing Critical ML Fixes Sprint 28]]"
tier: hot
tags: [machine learning, model calibration, data leakage, model evaluation]
---

# Calibration Leakage Fix in Machine Learning Pipelines

## Overview

Calibration leakage occurs when calibration methods use data from both training and validation sets improperly, causing overly optimistic performance estimates and biased predictions. Fixing calibration leakage is essential for reliable model evaluation and deployment.

## How It Works

Calibration adjusts predicted probabilities to better reflect true likelihoods, often using methods like `CalibratedClassifierCV` which applies cross-validation to fit calibration models. Leakage happens when the calibration step uses combined training and validation data, allowing information from validation to influence the calibration model, thus invalidating the separation between training and evaluation.

The fix involves restricting calibration to only the training data and enabling internal cross-validation within the calibration method itself. This means:

- Instead of concatenating `X_train` and `X_val` and their labels, only `X_train` and `y_train` are passed to `CalibratedClassifierCV`.
- The calibration method uses internal k-fold cross-validation (e.g., 3-fold) on the training data to fit calibration models without peeking at validation data.
- The previous guard checking if validation data is present is removed to ensure calibration always runs with internal CV.

This approach maintains the integrity of the validation set for unbiased evaluation and prevents data leakage.

Trade-offs include potentially increased computational cost due to internal cross-validation and the need for sufficient training data to support calibration folds.

Edge cases include scenarios with no separate validation data, where internal CV is the only option, and cases where calibration is skipped, leading to uncalibrated predictions.

## Key Properties

- **Calibration Method:** Uses `CalibratedClassifierCV` with internal 3-fold cross-validation on training data only.
- **Data Usage:** Calibration fit restricted to `X_train` and `y_train` only; validation data excluded.
- **Code Change:** Removed `X_val is not None` guard to always run calibration.

## Limitations

Requires sufficient training data to perform internal cross-validation effectively. If training data is small, calibration may be unstable. Also, calibration assumes the training data distribution matches deployment conditions.

## Example

```python
# Before (leakage):
X_combined = np.concatenate([X_train, X_val])
y_combined = np.concatenate([y_train, y_val])
calibrator = CalibratedClassifierCV(base_estimator, cv='prefit')
calibrator.fit(X_combined, y_combined)

# After (fixed):
calibrator = CalibratedClassifierCV(base_estimator, cv=3)
calibrator.fit(X_train, y_train)
```

## Relationship to Other Concepts

- **Model Calibration** — Calibration leakage is a failure mode in model calibration processes.

## Practical Applications

Ensures reliable probability estimates from classifiers in production ML pipelines, especially for risk-sensitive applications like betting or medical diagnosis. Prevents overly optimistic performance metrics that can mislead stakeholders.

## Sources

- [[Copilot Session Checkpoint: Implementing Critical ML Fixes Sprint 28]] — primary source for this concept
