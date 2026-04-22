---
title: "Calibration Leakage Mitigation in ML Model Training"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "f8d0a04a06d081eb78a648694aa8e0e839423db4ece7d887aafeef2087fa93fe"
sources:
  - raw/2026-04-18-copilot-session-sprint-55-planning-and-exploration-be98e3c5.md
  - raw/2026-04-18-copilot-session-sprint-55-implementation-and-deployment-2d04e4e0.md
quality_score: 64
concepts:
  - calibration-leakage-mitigation-ml-model-training
related:
  - "[[Ensemble Model Save-Round-Trip Validation Gate]]"
  - "[[Copilot Session Checkpoint: Sprint 55 Implementation and Deployment]]"
tier: hot
tags: [calibration, ml-training, data-leakage]
---

# Calibration Leakage Mitigation in ML Model Training

## Overview

Calibration leakage mitigation is a critical step in ML model training, ensuring that calibration data is not contaminated by training data. In Sprint 55, this was addressed by using a held-out calibration set and the CalibratedClassifierCV with cv="prefit", preventing overfitting and improving model reliability.

## How It Works

Calibration leakage occurs when calibration data overlaps with training data, leading to over-optimistic probability estimates and reduced generalizability. In the Sprint 55 implementation, the over/under classifier was modified to use an 80/20 train/calibration split. The base classifier is trained on the 80% training split, and calibration is performed on the held-out 20% using CalibratedClassifierCV with cv="prefit".

This approach ensures that the calibration process does not see any data used during model training, preserving the independence of calibration and preventing leakage. The CalibratedClassifierCV wrapper is initialized with the base classifier and cv="prefit", indicating that the base classifier has already been fitted and calibration should only use the provided calibration set.

The implementation required careful orchestration of train/test splits and explicit handling of calibration sets. Early stopping parameters for XGBoost were also confirmed to be correctly passed via set_params, avoiding TypeErrors from incorrect fit_kwargs usage. The calibration process is now robust, with clear separation between training and calibration phases.

Edge cases include ensuring that binary flags (e.g., feature presence indicators) default to 0, as they may not have meaningful medians. The three-tier approach saves feature medians as JSON during training, loads them during prediction, and applies imputation where necessary. This prevents zero-fill imputation, which can introduce bias.

Trade-offs involve increased complexity in data handling and the need for additional validation to confirm that calibration sets are truly independent. However, the benefits in model reliability and calibration accuracy are substantial, as calibration is identified as the primary bottleneck in model performance.

## Key Properties

- **Held-Out Calibration Set:** Uses an 80/20 split to ensure calibration data is independent from training data.
- **CalibratedClassifierCV with cv="prefit":** Applies calibration only to the held-out set, avoiding data leakage.
- **Improved Reliability:** Reduces overfitting and produces more trustworthy probability estimates.

## Limitations

Requires careful management of data splits and explicit handling of calibration sets. Increased complexity in orchestration and validation. If calibration set is too small, calibration may be unstable.

## Example

```python
from sklearn.model_selection import train_test_split
from sklearn.calibration import CalibratedClassifierCV

X_train, X_calib, y_train, y_calib = train_test_split(X, y, test_size=0.2, random_state=42)
base_clf.fit(X_train, y_train)
calib_clf = CalibratedClassifierCV(base_clf, cv="prefit")
calib_clf.fit(X_calib, y_calib)
```

## Relationship to Other Concepts

- **[[Ensemble Model Save-Round-Trip Validation Gate]]** — Both address reliability and validation in ML pipelines.

## Practical Applications

Essential in production ML pipelines where probability calibration impacts downstream decisions, such as sports betting, medical diagnosis, or risk assessment. Prevents overconfidence and improves model trustworthiness.

## Sources

- [[Copilot Session Checkpoint: Sprint 55 Implementation and Deployment]] — primary source for this concept
- [[Copilot Session Checkpoint: Sprint 55 Planning and Exploration]] — additional source
