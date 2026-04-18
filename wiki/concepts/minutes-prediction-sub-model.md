---
title: "Minutes Prediction Sub-Model"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9583aca364f19d189456564e8242665d819c8e046298a36e6032014ff646bea6"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-13-model-improvements-code-5db17c4d.md
quality_score: 100
concepts:
  - minutes-prediction-sub-model
related:
  - "[[Dynamic Ensemble Weighting]]"
  - "[[Copilot Session Checkpoint: Sprint 13 Model Improvements Code]]"
tier: hot
tags: [machine learning, regression, feature engineering, sports analytics]
---

# Minutes Prediction Sub-Model

## Overview

The Minutes Prediction Sub-Model is a specialized machine learning model designed to predict the number of minutes a basketball player will play in a game. This prediction is critical as it serves as an input feature for other statistical models in the NBA ML engine, improving overall prediction accuracy.

## How It Works

The Minutes Prediction Sub-Model is implemented as a dedicated class called MinutesModel using the XGBoost algorithm. It focuses on predicting a continuous target — the player's minutes — which is a more predictable and stable metric compared to other statistics. To enhance model performance and reduce overfitting, the feature set is filtered from approximately 400 raw features down to about 40 minutes-relevant features. These features include player starter status, rest days, pace, usage rate, and game lines, which are known to influence playing time.

The model uses shallower trees (max_depth=5) and a lower learning rate (0.03) to avoid overfitting and to capture the relatively stable patterns in minutes played. The training process integrates this model early in the pipeline because its predictions are used as features for subsequent stat prediction models.

In the feature building pipeline, a helper function _add_predicted_minutes() is called before conditional feature groups to insert the predicted minutes into the feature set. This function gracefully falls back to zero if the minutes model is not yet available in production, ensuring robustness.

The model is integrated into the trainer and predictor modules, allowing it to be trained, saved, loaded, and used for inference seamlessly within the overall system. This modular approach supports maintainability and extensibility.

By isolating minutes prediction, the system can better capture the variance in player availability and usage, which is a key driver of other statistical outcomes. This design choice reflects an understanding that minutes played is a foundational variable influencing many basketball statistics.

## Key Properties

- **Algorithm:** XGBoost regression with max_depth=5 and learning_rate=0.03
- **Feature Selection:** Filters ~400 features down to ~40 minutes-relevant features based on domain knowledge
- **Integration:** Minutes predictions are added as features for other stat models
- **Fallback Behavior:** If no production minutes model exists, predicted minutes default to 0.0

## Limitations

The model assumes that the selected ~40 features sufficiently capture the factors influencing minutes played; unexpected events like injuries or coach decisions may not be well predicted. The reliance on XGBoost parameters tuned for stability may limit capturing rare but impactful minute fluctuations. Also, the model requires retraining to adapt to changing player roles or team strategies.

## Example

```python
# Example usage snippet
from src.models.minutes_model import MinutesModel, get_minutes_feature_columns

# Instantiate model
minutes_model = MinutesModel()

# Get features relevant for minutes prediction
features = get_minutes_feature_columns(all_features)

# Train model (simplified)
minutes_model.train(X_train[features], y_train_minutes)

# Predict minutes
predicted_minutes = minutes_model.predict(X_test[features])

# Add predicted minutes to feature builder
features_with_minutes = _add_predicted_minutes(features, predicted_minutes)
```

## Relationship to Other Concepts

- **[[Dynamic Ensemble Weighting]]** — Minutes predictions feed into ensemble models as features

## Practical Applications

Used in NBA player performance prediction pipelines to improve accuracy by incorporating expected playing time. This is critical for fantasy sports, betting models, and team strategy analytics where minutes played strongly influence other statistics.

## Sources

- [[Copilot Session Checkpoint: Sprint 13 Model Improvements Code]] — primary source for this concept
