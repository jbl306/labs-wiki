---
title: "Per-Statistic Calibration Percentiles in Model Prediction"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9abff5d56824e0f4fae96781e1391fb0dbad2aaf59efa4bd9dfe557ce4eed23d"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-12-complete-and-skills-installed-48a02b58.md
quality_score: 100
concepts:
  - per-statistic-calibration-percentiles
related:
  - "[[Copilot Session Checkpoint: Sprint 12 Complete and Skills Installed]]"
tier: hot
tags: [model-calibration, uncertainty-estimation, regression]
---

# Per-Statistic Calibration Percentiles in Model Prediction

## Overview

Per-statistic calibration percentiles adjust the prediction interval calibration for each target statistic individually, improving the accuracy of uncertainty estimates in regression models. This technique accounts for differing residual distributions across statistics.

## How It Works

In the NBA ML Engine, calibration intervals are used to quantify prediction uncertainty by computing percentile bounds on residuals from training data. Previously, a uniform percentile range (e.g., 10th to 90th percentile) was applied to all statistics.

Sprint 12 introduced a configuration dictionary `STAT_CALIBRATION_PERCENTILES` mapping each statistic name to a tuple of lower and upper percentile values. For example, STL uses (7, 93) while BLK uses (8, 92). These percentiles define the quantiles of residuals used to calibrate prediction intervals.

The base model's `calibrate_intervals()` method was updated to accept a `stat_name` parameter. When provided, it looks up the corresponding percentile tuple and calculates calibration intervals accordingly. This allows each statistic to have tailored calibration reflecting its residual distribution characteristics.

The motivation is that different statistics have different variance and distribution shapes. For instance, STL (steals) is discrete with values mostly between 0 and 3, causing standard percentile intervals to underestimate variance. Adjusting percentiles widens or narrows intervals to better capture true uncertainty.

This per-stat calibration improves coverage accuracy, as demonstrated by STL calibration coverage increasing from 76.8% to 80.3% after widening percentiles. It enhances the reliability of prediction uncertainty estimates used downstream in decision-making or risk assessment.

## Key Properties

- **Configurable Percentiles:** Percentile bounds are specified per statistic in a dictionary, e.g., {'STL': (7, 93)}.
- **Integration in Model:** Calibration method accepts stat_name and applies corresponding percentiles during interval computation.
- **Improved Coverage:** Tailored intervals better capture residual variance, increasing calibration coverage metrics.

## Limitations

Requires sufficient residual data per statistic to estimate percentiles reliably. May not generalize well if residual distributions shift over time. Adds complexity to configuration and model code. Incorrect percentile choices can lead to over- or under-confidence in intervals.

## Example

In base.py:

```python
def calibrate_intervals(self, stat_name=None):
    lower_pct, upper_pct = self.config.STAT_CALIBRATION_PERCENTILES.get(stat_name, (10, 90))
    # Compute residual quantiles at lower_pct and upper_pct
    ...
```

For STL, the method uses (7, 93) instead of default (10, 90).

## Relationship to Other Concepts

- **Prediction Interval Calibration** — Per-stat calibration is an extension of general prediction interval calibration techniques.

## Practical Applications

Useful in multi-target regression problems where each target has distinct residual characteristics. Enhances uncertainty quantification for better risk management and decision-making in predictive systems.

## Sources

- [[Copilot Session Checkpoint: Sprint 12 Complete and Skills Installed]] — primary source for this concept
