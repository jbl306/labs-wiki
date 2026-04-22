---
title: "Edge Threshold Optimizer Using Kelly Criterion"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9583aca364f19d189456564e8242665d819c8e046298a36e6032014ff646bea6"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-13-model-improvements-code-5db17c4d.md
quality_score: 53
concepts:
  - edge-threshold-optimizer-kelly-criterion
related:
  - "[[Copilot Session Checkpoint: Sprint 13 Model Improvements Code]]"
tier: hot
tags: [betting, optimization, cross-validation, Kelly criterion]
---

# Edge Threshold Optimizer Using Kelly Criterion

## Overview

The Edge Threshold Optimizer is a component designed to optimize betting thresholds for statistical predictions by applying walk-forward cross-validation and the Kelly criterion for bet sizing. This approach aims to maximize expected returns while controlling risk in prop betting scenarios.

## How It Works

The optimizer works by sweeping through possible edge thresholds for each statistical prediction to identify the threshold that yields the best performance in backtesting. Instead of using in-sample data, it employs walk-forward cross-validation (CV) with an expanding window and a small number of folds (n_folds=3) to prevent overfitting and simulate real-world sequential data conditions.

The key function optimize_thresholds() performs this threshold sweep per stat, evaluating performance metrics such as profit or accuracy at each candidate threshold. The results are then formatted into a configuration dictionary for use in production.

For bet sizing, the optimizer uses the Kelly criterion, a formula that calculates the optimal fraction of capital to wager based on the edge and odds. To reduce risk, a fractional Kelly approach is applied, using only 25% of the Kelly fraction. The formula used is:

$$ f^* = 0.25 \times \frac{bp - q}{b} $$

where:
- $b$ is the net odds received on the wager (e.g., decimal odds minus 1),
- $p$ is the probability of winning,
- $q = 1 - p$ is the probability of losing.

This conservative sizing helps avoid large drawdowns while still capitalizing on positive expected value bets.

The optimizer integrates with the predictor module to provide optimized edge thresholds dynamically during inference, improving decision-making for betting strategies.

## Key Properties

- **Cross-Validation:** Walk-forward CV with expanding window and 3 folds to avoid overfitting
- **Bet Sizing:** Fractional Kelly criterion at 25% fraction for conservative bet sizes
- **Output:** Optimized thresholds formatted into config dict for runtime use

## Limitations

The walk-forward CV with only 3 folds may provide limited statistical power, potentially leading to suboptimal thresholds in volatile environments. The fractional Kelly sizing reduces risk but may underutilize capital in some cases. The approach assumes stable odds and probabilities, which may not hold in rapidly changing markets.

## Example

```python
from src.evaluation.edge_optimizer import optimize_thresholds, kelly_bet_size

# Optimize thresholds on historical data
optimized_thresholds = optimize_thresholds(stat_predictions, actuals, n_folds=3)

# Calculate bet size for a given edge
fractional_kelly = kelly_bet_size(prob_win=0.6, odds=1.9, fraction=0.25)

print(f"Optimal bet fraction: {fractional_kelly:.2f}")
```

## Relationship to Other Concepts

- **Binary Over/Under Classifier** — Uses optimized thresholds for binary classification of prop bets

## Practical Applications

Applied in sports betting engines to determine when to place bets and how much to wager, balancing expected returns and risk. Useful for prop bet backtesting and live betting strategies in NBA ML systems.

## Sources

- [[Copilot Session Checkpoint: Sprint 13 Model Improvements Code]] — primary source for this concept
