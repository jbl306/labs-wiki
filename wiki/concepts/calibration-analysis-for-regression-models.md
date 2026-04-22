---
title: "Calibration Analysis for Regression Models"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "7947d08e9a063fe0b24b8984da65f96b90179927fffc01c1f05927569f503763"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-11-evaluation-and-report-5b560f0f.md
quality_score: 64
concepts:
  - calibration-analysis-for-regression-models
related:
  - "[[Holdout Evaluator Module]]"
  - "[[Copilot Session Checkpoint: Sprint 11 Evaluation and Report]]"
tier: hot
tags: [model calibration, uncertainty quantification, regression evaluation]
---

# Calibration Analysis for Regression Models

## Overview

Calibration analysis assesses how well the predicted confidence intervals or quantiles of regression models correspond to the actual distribution of errors. Proper calibration means the predicted uncertainty accurately reflects real-world variability, which is crucial for reliable decision-making based on model outputs.

## How It Works

In the Sprint 11 evaluation, calibration was performed using a residual-based percentile method implemented in `calibrate_intervals()`. The process involves:

1. Calculating residuals (differences between predicted and actual values) on the holdout test set.
2. Computing empirical coverage probabilities at multiple quantiles (q10 to q90), which correspond to the proportion of true values falling within predicted intervals.
3. Comparing these empirical coverages to a target coverage level of approximately 80%.

The calibration results showed that five out of six production models achieved coverage within ±1.2% of the 80% target, indicating well-calibrated predictions. One model, STL, was under-calibrated at 76.8%, suggesting its prediction intervals are too narrow and over-confident.

Calibration is critical for applications like prop betting where confidence in predictions affects risk management and bet sizing. The method used is non-parametric and relies on empirical residual distributions, making it robust to model assumptions.

This analysis was integrated into the holdout evaluator module and can be toggled via CLI options. Calibration results are reported alongside accuracy metrics to provide a holistic view of model performance.

## Key Properties

- **Empirical Coverage:** Measures the fraction of true outcomes falling within predicted quantile intervals.
- **Residual-Based Percentiles:** Uses residuals to estimate prediction interval coverage without parametric assumptions.
- **Target Coverage:** Aims for approximately 80% coverage as a benchmark for well-calibrated models.

## Limitations

Calibration analysis requires sufficient test data to estimate coverage accurately. It is limited to models registered in the production model registry; stats without production models (e.g., BLK, FG_PCT, FT_PCT) could not be fully calibrated. The method assumes residuals are representative and stationary over time, which may not hold in non-stationary environments.

## Example

Pseudocode for calibration coverage calculation:
```
residuals = y_true - y_pred
coverage = {}
for q in [0.10, 0.20, ..., 0.90]:
    lower = np.percentile(y_pred + residuals, q*100)
    upper = np.percentile(y_pred + residuals, (1-q)*100)
    coverage[q] = np.mean((y_true >= lower) & (y_true <= upper))
```

Report example:
```
Stat: AST
Coverage at 80% target: 81.1%
```


## Relationship to Other Concepts

- **[[Holdout Evaluator Module]]** — Calibration analysis is one of the three evaluation modes implemented.

## Practical Applications

Used to validate the reliability of regression model uncertainty estimates in sports analytics and betting applications. Helps identify over- or under-confident models and guides model recalibration or retraining decisions.

## Sources

- [[Copilot Session Checkpoint: Sprint 11 Evaluation and Report]] — primary source for this concept
