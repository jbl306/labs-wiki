---
title: "Feature Alignment for Models with Feature Selection"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "7947d08e9a063fe0b24b8984da65f96b90179927fffc01c1f05927569f503763"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-11-evaluation-and-report-5b560f0f.md
quality_score: 56
concepts:
  - feature-alignment-for-feature-selection-models
related:
  - "[[Holdout Evaluator Module]]"
  - "[[Copilot Session Checkpoint: Sprint 11 Evaluation and Report]]"
tier: hot
tags: [feature engineering, model evaluation, data preprocessing]
---

# Feature Alignment for Models with Feature Selection

## Overview

Feature alignment is a critical process ensuring that the feature matrix used during model evaluation matches the exact subset of features each model was trained on. This is especially important for models trained with feature selection, where only a subset of all available features is used. Misalignment can cause errors or degraded performance during evaluation.

## How It Works

During Sprint 11 evaluation, a bug was discovered where models trained with feature selection (e.g., STL, BLK, FG_PCT, FT_PCT) failed during evaluation because the evaluator passed the full feature matrix containing all 383 features, while these models expected only their selected subset (ranging from 200 to 248 features).

The fix involved implementing a helper function `_align_features()` that takes the full test feature matrix `X_test` and filters it to include only the features present in the model's `feature_names` attribute. This ensures that the input to the model's prediction function matches the training feature space exactly.

The `_align_features()` function is applied consistently across all evaluation modes: holdout metrics, calibration, and feature group permutation importance. This uniform application prevents feature mismatch errors and ensures fair and accurate evaluation.

Additionally, this fix revealed that CatBoost models internally handle extra features gracefully, but other models like XGBoost, LightGBM, Ridge, and Random Forest raise errors if feature counts do not match.

This alignment step is essential for robust evaluation pipelines where multiple models with different feature subsets coexist. It also facilitates modularity, allowing models to be swapped or updated independently without breaking evaluation scripts.

## Key Properties

- **Selective Feature Filtering:** Filters test features to exactly those used by each model, preventing dimension mismatch errors.
- **Universal Application:** Applied across all evaluation functions to maintain consistency.
- **Compatibility:** Ensures compatibility with models that do not internally handle extra features.

## Limitations

Requires that each model exposes an accurate and complete `feature_names` attribute. If this metadata is missing or incorrect, alignment will fail or produce incorrect inputs. This approach assumes static feature sets per model and does not dynamically handle feature evolution or missing features at runtime.

## Example

Pseudocode for `_align_features()`:
```
def _align_features(X_test, model):
    selected_features = model.feature_names
    return X_test[selected_features]
```

Usage in evaluation:
```
X_aligned = _align_features(X_test, model)
predictions = model.predict(X_aligned)
```

## Relationship to Other Concepts

- **[[Holdout Evaluator Module]]** — Feature alignment is a critical internal step within the holdout evaluator to ensure correct evaluation.

## Practical Applications

Essential for evaluating machine learning models trained with feature selection in production or research settings. Prevents runtime errors and ensures fair comparison of models with varying feature subsets. Supports complex ML pipelines with heterogeneous models.

## Sources

- [[Copilot Session Checkpoint: Sprint 11 Evaluation and Report]] — primary source for this concept
