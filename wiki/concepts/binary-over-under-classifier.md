---
title: "Binary Over/Under Classifier with Isotonic Calibration"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9583aca364f19d189456564e8242665d819c8e046298a36e6032014ff646bea6"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-13-model-improvements-code-5db17c4d.md
quality_score: 100
concepts:
  - binary-over-under-classifier
related:
  - "[[Edge Threshold Optimizer Using Kelly Criterion]]"
  - "[[Copilot Session Checkpoint: Sprint 13 Model Improvements Code]]"
tier: hot
tags: [binary classification, calibration, sports betting, XGBoost]
---

# Binary Over/Under Classifier with Isotonic Calibration

## Overview

The Binary Over/Under Classifier is a supplemental binary classification model designed to predict whether a player's statistic will be over or under a given betting line. It uses XGBoost as the base classifier and applies isotonic calibration to improve probability estimates, enhancing decision-making for prop bets.

## How It Works

Unlike other models in the system, the OverUnderClassifier is not a subclass of the BaseModel but operates as a standalone classifier. It takes as input the regression model's predictions combined with the betting line as additional features, enabling it to learn the binary classification task of over/under outcomes.

The training pipeline prepares data by joining features, predictions, prop lines, and actual outcomes to create a labeled dataset for classification. The model is trained using XGBoost's binary classification objective.

To improve the reliability of predicted probabilities, isotonic calibration is applied via scikit-learn's CalibratedClassifierCV. This non-parametric calibration method fits a piecewise constant non-decreasing function to map raw classifier scores to calibrated probabilities, which is particularly useful when the classifier's probability outputs are not well calibrated.

The classifier is integrated into the training pipeline and controlled via new configuration flags. It complements the regression models by providing direct binary predictions, which are valuable for betting decisions that require a yes/no outcome rather than a continuous estimate.

## Key Properties

- **Model Type:** XGBoost binary classifier
- **Calibration:** Isotonic calibration via CalibratedClassifierCV for better probability estimates
- **Input Features:** Regression predictions plus betting line values

## Limitations

Being a supplemental model, it depends on the quality of regression predictions and betting line data. Calibration requires sufficient data to avoid overfitting. The model does not directly model the continuous outcome, so it may lose some granularity compared to regression approaches.

## Example

```python
from src.models.over_under_model import OverUnderClassifier, prepare_classifier_data

# Prepare training data
X_train, y_train = prepare_classifier_data(features, predictions, prop_lines, actuals)

# Train classifier
classifier = OverUnderClassifier()
classifier.train(X_train, y_train)

# Predict probabilities
prob_over = classifier.predict_proba(X_test)[:, 1]
```

## Relationship to Other Concepts

- **[[Edge Threshold Optimizer Using Kelly Criterion]]** — Uses optimized thresholds to improve binary classification decisions

## Practical Applications

Used in sports betting ML pipelines to provide calibrated binary predictions for over/under prop bets, aiding bettors and analysts in making informed wagering decisions.

## Sources

- [[Copilot Session Checkpoint: Sprint 13 Model Improvements Code]] — primary source for this concept
