---
title: "Walk-Forward Stability Analysis and Backtesting in NBA ML Engine"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9abff5d56824e0f4fae96781e1391fb0dbad2aaf59efa4bd9dfe557ce4eed23d"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-12-complete-and-skills-installed-48a02b58.md
quality_score: 100
concepts:
  - walk-forward-stability-analysis-backtesting-nba-ml-engine
related:
  - "[[NBA ML Prediction Pipeline]]"
  - "[[Feature Engineering Pipeline for NBA ML Platform]]"
  - "[[Copilot Session Checkpoint: Sprint 12 Complete and Skills Installed]]"
tier: hot
tags: [model-evaluation, time-series, backtesting, nba-ml]
---

# Walk-Forward Stability Analysis and Backtesting in NBA ML Engine

## Overview

Sprint 12 included extensive evaluation of model stability and predictive performance via walk-forward cross-validation and backtesting. These analyses assess how models perform over time and under realistic betting scenarios, guiding model improvements and feature selection.

## How It Works

Walk-forward cross-validation splits the dataset into sequential folds simulating real-time prediction scenarios. The expanding_window_split method generates folds from the 2017-18 season through 2025-26, training on past data and testing on future data iteratively. This approach reveals temporal stability and potential concept drift.

Initially, attempts to run GBM models for walk-forward failed due to computational intensity and memory constraints. Switching to Ridge regression enabled faster execution (4 folds × 9 stats in ~2 minutes), producing stable results. For example, points (PTS) R² remained stable (0.505-0.516), rebounds (REB) improved (0.412→0.462), while assists (AST) declined (0.547→0.499), suggesting possible regime changes.

Backtesting simulated prop bet outcomes using the model predictions, excluding PTS and AST stats to improve signal quality. The backtest covered 856 bets with a 57.0% hit rate and -5.0% ROI, improved from previous 53.1% hit rate and -8.6% ROI. BLK and STL stats showed the strongest alpha generation with hit rates of 68.6% and 66.7%, respectively.

These analyses provide actionable insights into model robustness over time and betting strategy effectiveness, informing next sprint priorities such as minutes prediction and opponent defensive features.

## Key Properties

- **Walk-Forward CV:** Sequential folds simulate real-time prediction, revealing temporal stability and drift.
- **Backtest Metrics:** Hit rate and ROI quantify betting strategy performance using model predictions.
- **Computational Constraints:** GBM models too heavy for walk-forward; Ridge regression used for speed and stability.

## Limitations

Walk-forward CV with complex models may be computationally prohibitive. Backtest results depend on accurate exclusion of noisy stats and realistic betting assumptions. Declining metrics may indicate model limitations or changing data regimes requiring retraining or feature updates.

## Example

Walk-forward evaluation command:
```bash
python main.py evaluate --save-json
```
Backtest summary:
- Bets: 856
- Hit Rate: 57.0%
- ROI: -5.0%
- Improvements from prior sprint hit rate 53.1%, ROI -8.6%


## Relationship to Other Concepts

- **[[NBA ML Prediction Pipeline]]** — Walk-forward and backtesting are integral evaluation components
- **[[Feature Engineering Pipeline for NBA ML Platform]]** — Feature quality impacts evaluation outcomes

## Practical Applications

Walk-forward CV is essential for assessing model generalization over time in time-series contexts. Backtesting validates model utility for betting strategies, guiding risk management and feature development.

## Sources

- [[Copilot Session Checkpoint: Sprint 12 Complete and Skills Installed]] — primary source for this concept
