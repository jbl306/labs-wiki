---
title: "Per-Stat Calibration Fixes and Residual Persistence in Model Save/Load"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9abff5d56824e0f4fae96781e1391fb0dbad2aaf59efa4bd9dfe557ce4eed23d"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-12-complete-and-skills-installed-48a02b58.md
quality_score: 100
concepts:
  - per-stat-calibration-fixes-residual-persistence-model-save-load
related:
  - "[[Calibration Analysis for Regression Models]]"
  - "[[Post-Ingest Quality Fixes in Auto-Ingest Pipelines]]"
  - "[[Copilot Session Checkpoint: Sprint 12 Complete and Skills Installed]]"
tier: hot
tags: [model-calibration, uncertainty-estimation, machine-learning, nba-ml]
---

# Per-Stat Calibration Fixes and Residual Persistence in Model Save/Load

## Overview

Calibration fixes in Sprint 12 addressed a critical bug where residual distributions used for uncertainty estimation were not persisted during model save/load, causing prediction probability calculations to fail. Additionally, per-stat calibration percentiles were introduced to improve interval calibration accuracy for different statistics.

## How It Works

The calibration mechanism relies on residual distributions to estimate prediction uncertainty and confidence intervals. Previously, only the lower and upper residual bounds (`_residual_lower` and `_residual_upper`) were saved and loaded, but the full residual array (`_residuals`) was omitted. This omission caused the `predict_probability()` function, which uses the full residual distribution, to malfunction after model reload.

Sprint 12 fixed this by modifying all six model classes (catboost, xgboost, lightgbm, random_forest, ridge, and ensemble) to include the `_residuals` array in their save dictionaries and restore it on load. This ensures the residual distribution is fully available for calibration computations post-reload.

Furthermore, a new configuration dictionary `STAT_CALIBRATION_PERCENTILES` was added to map each statistic to custom lower and upper percentile thresholds. For example, steals (STL) uses q7/q93 percentiles instead of default q10/q90 to better capture its discrete and low-variance nature. The base model's `calibrate_intervals()` method was updated to accept a `stat_name` parameter and apply these per-stat overrides, allowing more precise calibration tailored to each statistic's distribution characteristics.

These improvements resulted in better calibration coverage, e.g., STL coverage improved from 76.8% to 80.3%, indicating more reliable uncertainty intervals.

## Key Properties

- **Residual Persistence:** All model save/load methods now persist the full residual distribution array, enabling accurate uncertainty predictions after reload.
- **Per-Stat Calibration Percentiles:** Custom percentile thresholds per statistic improve calibration interval accuracy, especially for discrete or skewed stats.
- **Calibration Function Update:** `calibrate_intervals()` accepts `stat_name` to apply per-stat overrides dynamically.

## Limitations

Calibration improvements depend on accurate residual distributions; if residuals are noisy or biased, calibration may still be suboptimal. Per-stat percentiles require manual tuning and domain knowledge, which may not generalize across datasets.

## Example

In `config.py`:
```python
STAT_CALIBRATION_PERCENTILES = {
    'STL': (7, 93),
    'BLK': (8, 92),
    # defaults for others
}
```
In `base.py`:
```python
def calibrate_intervals(self, stat_name=None):
    if stat_name and stat_name in STAT_CALIBRATION_PERCENTILES:
        lower, upper = STAT_CALIBRATION_PERCENTILES[stat_name]
    else:
        lower, upper = default_percentiles
    # compute intervals using these percentiles
```
In model save/load methods:
```python
data['residuals'] = getattr(self, '_residuals', None)
self._residuals = data.get('residuals')
```


## Relationship to Other Concepts

- **[[Calibration Analysis for Regression Models]]** — Calibration fixes improve regression model uncertainty estimation
- **[[Post-Ingest Quality Fixes in Auto-Ingest Pipelines]]** — Both involve quality improvements in ML pipelines

## Practical Applications

Accurate calibration is critical in risk-sensitive applications like sports betting, where confidence intervals guide decision thresholds. Persisting residuals ensures model reliability after deployment restarts. Per-stat calibration allows tailored uncertainty quantification for heterogeneous targets.

## Sources

- [[Copilot Session Checkpoint: Sprint 12 Complete and Skills Installed]] — primary source for this concept
