---
title: "Holdout Evaluator Module"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "7947d08e9a063fe0b24b8984da65f96b90179927fffc01c1f05927569f503763"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-11-evaluation-and-report-5b560f0f.md
quality_score: 100
concepts:
  - holdout-evaluator-module
related:
  - "[[Copilot Session Checkpoint: Sprint 11 Evaluation and Report]]"
tier: hot
tags: [evaluation, machine learning, model calibration, feature importance]
---

# Holdout Evaluator Module

## Overview

The holdout evaluator module is a comprehensive evaluation framework developed to assess model performance on holdout test data. It supports multiple evaluation modes including traditional regression metrics, calibration analysis, and feature group permutation importance, enabling a deep understanding of model accuracy, reliability, and feature contributions.

## How It Works

The holdout evaluator module is implemented primarily in the `holdout_evaluator.py` file, spanning over 700 lines of code. It provides three distinct evaluation modes:

1. **Holdout Metrics Evaluation:** Computes standard regression metrics such as Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), R-squared (R²), and Median Absolute Error (MedAE) on the holdout test set. This quantifies the predictive accuracy of models on unseen data.

2. **Calibration Analysis:** Uses residual-based percentiles to assess how well the prediction intervals correspond to actual outcomes. The method `calibrate_intervals()` calculates coverage probabilities at quantiles q10 to q90, aiming for an empirical coverage close to 80%. This analysis reveals if models are over- or under-confident in their predictions.

3. **Feature Group Permutation Importance:** Measures the importance of predefined feature groups by shuffling all features within a group simultaneously and observing the increase in Mean Squared Error (MSE). This process is repeated three times and averaged to reduce variance. The feature groups correspond to Sprint 10's six groups, including minutes_trend, matchup, target_encoding, injury_return, and b2b_fatigue.

The module includes a critical helper function `_align_features()` that ensures the test feature matrix is filtered to match the exact features expected by each model, addressing a key bug discovered during evaluation. Additionally, an optimization parameter `_prebuilt` allows the feature matrix to be built once and reused across evaluation modes, reducing redundant computation and speeding up evaluation.

The module supports CLI integration with options to specify statistics, toggle calibration and importance analyses, and save results in JSON format. It also includes formatting functions for generating human-readable reports.

This modular design allows flexible, repeatable, and thorough evaluation of multiple models across various stats, facilitating robust model validation and comparison.

## Key Properties

- **Evaluation Modes:** Supports holdout metrics, calibration analysis, and feature group permutation importance.
- **Feature Alignment:** Includes `_align_features()` to filter test features to match model expectations, critical for models trained with feature selection.
- **Performance Optimization:** Uses `_prebuilt` parameter to avoid rebuilding features multiple times, reducing evaluation runtime significantly.
- **Output Formats:** Generates both CLI formatted reports and JSON output for programmatic use.

## Limitations

Permutation importance results showed marginal impact (<0.3%) for all feature groups, indicating limited discriminative power of these groups in the current models. Calibration analysis is limited to production models registered in the model registry; some stats like BLK, FG_PCT, and FT_PCT lacked production models and thus had limited calibration data. The module assumes feature names are consistent and requires careful feature alignment to avoid errors.

## Example

Example CLI command to run full evaluation with JSON output:
```
python main.py evaluate --save-json /app/evaluation_results.json
```

Pseudocode for permutation importance:
```
for feature_group in FEATURE_GROUPS:
    mse_increases = []
    for repeat in range(3):
        shuffled_features = shuffle_features_in_group(X_test, feature_group)
        mse = evaluate_model_mse(model, shuffled_features, y_test)
        mse_increases.append(mse - baseline_mse)
    importance[feature_group] = average(mse_increases)
```

## Relationship to Other Concepts

- **Feature Group Permutation Importance** — One of the three evaluation modes implemented within the holdout evaluator module.
- **Calibration Analysis** — Another evaluation mode provided by the holdout evaluator to assess prediction interval reliability.

## Practical Applications

Used to rigorously evaluate machine learning models predicting NBA player statistics on holdout test data. Helps identify model strengths and weaknesses, calibrate prediction confidence, and understand feature group contributions. Supports model validation before production deployment and guides feature engineering and model selection decisions.

## Sources

- [[Copilot Session Checkpoint: Sprint 11 Evaluation and Report]] — primary source for this concept
