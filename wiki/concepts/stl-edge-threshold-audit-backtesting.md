---
title: "STL Edge-Threshold Audit and Backtesting"
type: concept
created: 2026-04-19
last_verified: 2026-04-19
source_hash: "1802936d1c3943c4f998038fc1d70bd57065648d6c678c845a0d02f69f44107b"
sources:
  - raw/2026-04-19-copilot-session-sprint-61-planning-audit-6c5cb258.md
quality_score: 56
concepts:
  - stl-edge-threshold-audit-backtesting
related:
  - "[[Edge Gating and Stat-Specific Thresholds in ML Prediction Pipelines]]"
  - "[[Copilot Session Checkpoint: Sprint 61 Planning + Audit]]"
tier: hot
tags: [threshold-tuning, backtesting, sports-analytics, nba-ml-engine, config-optimization]
---

# STL Edge-Threshold Audit and Backtesting

## Overview

The STL edge-threshold audit is a targeted review and backtest of the stat edge thresholds used for predicting steals (STL) in the NBA ML Engine. The goal is to optimize prediction volume and hit rate by adjusting configuration parameters based on empirical results.

## How It Works

In sports betting and predictive modeling, edge thresholds determine which predictions are actionable based on their expected value. For steals (STL), the NBA ML Engine uses configuration parameters in `config.py` to filter predictions:

- `STAT_EDGE_ABSOLUTE['stl']`: Minimum absolute edge required for a prediction to be considered.
- `STAT_EDGE_THRESHOLDS['stl']`: Additional thresholds that may further filter predictions.

Sprint 61 identifies that the current threshold (0.3) may be too restrictive, reducing prediction volume without materially improving hit rate. The audit process involves:

1. **Historical Performance Review**: STL hit rate was 64.6% on 478 bets in the last 60 days, suggesting that filters may be overly tight.
2. **Backtesting**: Run a SQL backtest comparing prediction performance at threshold 0.2 (prior value) versus 0.3 (current value). The backtest evaluates:
   - Hit rate (percentage of correct predictions)
   - Prediction volume (number of actionable bets)
   - Trade-off between increased volume and potential decrease in accuracy
3. **Config Editing**: If backtest results show that lowering the threshold to 0.2 maintains hit rate above 55% while increasing volume, edit `config.py` to reflect the new threshold.
4. **Reporting**: Document findings in the sprint report, including SQL queries, summary statistics, and rationale for any config changes.
5. **Deployment**: Changes are code-only and take effect immediately for future predictions; no retrain is required.

The intuition is to maximize actionable predictions without sacrificing accuracy. Overly tight thresholds may leave profitable bets on the table, while loose thresholds can degrade hit rate. By empirically tuning thresholds, the engine adapts to real-world performance and market dynamics.

Edge cases include ensuring that config changes do not inadvertently crash hit rate or introduce bias. The audit is performed as a pure config + backtest operation, minimizing risk and enabling rapid iteration.

## Key Properties

- **Empirical Backtesting:** Thresholds are tuned based on historical hit rate and prediction volume, not arbitrary values.
- **Config-Driven Optimization:** Thresholds are edited in `config.py`, enabling immediate deployment without retraining.
- **Volume vs. Accuracy Trade-off:** Audit balances increased prediction volume against the risk of lower hit rates.

## Limitations

The audit relies on historical data, which may not predict future performance. Lowering thresholds can increase risk if market conditions change. Hit rate must be monitored post-deployment to ensure sustained accuracy. The approach assumes that config changes are properly documented and tested.

## Example

```python
# In config.py
STAT_EDGE_ABSOLUTE['stl'] = 0.2  # Lowered from 0.3 after backtest

# SQL backtest example:
SELECT COUNT(*) AS bet_count, AVG(hit) AS hit_rate
FROM predictions
WHERE stat = 'stl' AND abs(edge) >= 0.2;
```

## Relationship to Other Concepts

- **[[Edge Gating and Stat-Specific Thresholds in ML Prediction Pipelines]]** — Both concepts address stat-specific edge threshold optimization in ML pipelines.

## Practical Applications

This audit is relevant for any predictive system where thresholds control actionable outputs, such as sports betting, financial trading, or anomaly detection. It enables data-driven optimization of filters to maximize value.

## Sources

- [[Copilot Session Checkpoint: Sprint 61 Planning + Audit]] — primary source for this concept
