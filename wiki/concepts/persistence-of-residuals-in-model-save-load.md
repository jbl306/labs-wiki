---
title: "Persistence of Residuals in Model Save/Load for Probability Prediction"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9abff5d56824e0f4fae96781e1391fb0dbad2aaf59efa4bd9dfe557ce4eed23d"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-12-complete-and-skills-installed-48a02b58.md
quality_score: 53
concepts:
  - persistence-of-residuals-in-model-save-load
related:
  - "[[Copilot Session Checkpoint: Sprint 12 Complete and Skills Installed]]"
tier: hot
tags: [model-serialization, probabilistic-prediction, residuals]
---

# Persistence of Residuals in Model Save/Load for Probability Prediction

## Overview

Persisting residual distributions in model serialization enables accurate probability predictions with uncertainty after model reload. Without saving residuals, prediction probability functions relying on residual distributions fail or degrade.

## How It Works

In the NBA ML Engine, models maintain arrays of residuals from training data, which are used in methods like `predict_probability()` to estimate the likelihood of outcomes within calibrated intervals.

Before Sprint 12, the model save/load methods only persisted residual interval bounds (`_residual_lower` and `_residual_upper`) but did not save the full residual arrays (`_residuals`). This omission caused the residual arrays to be lost on reload, breaking probability prediction functionality that depends on the full residual distribution.

Sprint 12 fixed this by modifying all six model implementations (catboost, xgboost, lightgbm, random_forest, ridge, ensemble) to include the `_residuals` array in their save dictionaries and load methods. Specifically, the save method adds:

```python
"residuals": getattr(self, "_residuals", None)
```

and the load method restores it:

```python
self._residuals = data.get("residuals")
```

This ensures that after model deserialization, the residual distribution is intact, allowing `predict_probability()` to function correctly and provide calibrated probability estimates.

This fix improves model reliability and trustworthiness in production, especially for applications requiring probabilistic forecasts rather than point predictions.

## Key Properties

- **Residual Array Persistence:** Full residual arrays are saved and loaded with the model state.
- **Compatibility:** Implemented consistently across all six model types in the codebase.
- **Enables Probability Prediction:** Restores functionality of methods relying on residual distributions.

## Limitations

Residual arrays can be large, increasing model save file size. Requires careful versioning to ensure backward compatibility. If residuals are corrupted or incomplete, probability predictions may be inaccurate.

## Example

In catboost_model.py save method:

```python
save_dict = {
    ...
    "residuals": getattr(self, "_residuals", None),
}
```

In load method:

```python
self._residuals = data.get("residuals")
```

This pattern is repeated in all model classes.

## Relationship to Other Concepts

- **Model Serialization** — Persistence of residuals is an enhancement to standard model serialization.
- **Prediction Interval Calibration** — Residuals are used to compute calibrated prediction intervals.

## Practical Applications

Critical for ML systems that provide probabilistic predictions or uncertainty estimates, such as sports betting models, risk assessment tools, or any regression model requiring calibrated confidence intervals.

## Sources

- [[Copilot Session Checkpoint: Sprint 12 Complete and Skills Installed]] — primary source for this concept
