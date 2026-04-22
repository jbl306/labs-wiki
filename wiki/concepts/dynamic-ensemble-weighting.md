---
title: "Dynamic Ensemble Weighting"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9583aca364f19d189456564e8242665d819c8e046298a36e6032014ff646bea6"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-13-model-improvements-code-5db17c4d.md
quality_score: 72
concepts:
  - dynamic-ensemble-weighting
related:
  - "[[Minutes Prediction Sub-Model]]"
  - "[[Copilot Session Checkpoint: Sprint 13 Model Improvements Code]]"
tier: hot
tags: [ensemble learning, model weighting, recency bias, sports analytics]
---

# Dynamic Ensemble Weighting

## Overview

Dynamic Ensemble Weighting is a technique to combine multiple model predictions into a single ensemble prediction by weighting models inversely proportional to their recent mean absolute error (MAE). This approach emphasizes models that have performed better on the most recent data, introducing a recency bias to adapt to changing conditions.

## How It Works

The ensemble model is modified to support two weight modes: a ridge regression meta-learner and a recent performance weighting mode. In the recent performance mode, the ensemble computes inverse-MAE weights based on the last fold of training data only, reflecting the most recent model performance.

The process involves:

1. Calculating the MAE of each base model on the most recent validation fold.
2. Computing weights as the inverse of these MAEs, so models with lower error receive higher weight.
3. Normalizing the weights to sum to one to maintain a proper convex combination.
4. During prediction, the ensemble outputs a weighted average of base model predictions using these dynamic weights.

This method allows the ensemble to adapt quickly to changes in model accuracy over time, which is important in non-stationary environments like sports analytics where player performance and team dynamics evolve.

The ensemble's save and load methods are updated to persist the new weighting mode and performance weights, ensuring consistency across sessions.

## Key Properties

- **Weight Modes:** Supports 'ridge' meta-learner and 'recent_performance' inverse-MAE weighting
- **Recency Bias:** Weights computed from last fold only to emphasize recent model accuracy
- **Prediction:** Dual-mode predict() method supports both weighted average and ridge meta-learner

## Limitations

Inverse-MAE weighting assumes that recent performance is a reliable indicator of future accuracy, which may not hold if recent data is noisy or unrepresentative. The approach may overweight models that performed well due to chance. Ridge meta-learner mode requires additional training and may be more complex to maintain.

## Example

```python
# Compute inverse-MAE weights
mae_scores = [0.1, 0.2, 0.15]
inverse_mae = [1/m for m in mae_scores]
weights = [w / sum(inverse_mae) for w in inverse_mae]

# Weighted ensemble prediction
ensemble_prediction = sum(w * pred for w, pred in zip(weights, base_model_preds))
```

## Relationship to Other Concepts

- **[[Minutes Prediction Sub-Model]]** — Uses minutes predictions as input features for ensemble models

## Practical Applications

Improves prediction accuracy in NBA ML systems by dynamically adapting model weights based on recent performance, useful in environments with evolving data distributions such as sports analytics and betting.

## Sources

- [[Copilot Session Checkpoint: Sprint 13 Model Improvements Code]] — primary source for this concept
