---
title: "Regularization Techniques in Linear Regression"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "64f3d7794fd5e8567333444aa2dcf2ae76e118f9bf78cb15eb014a7029e90e95"
sources:
  - raw/2026-04-08-linear-regression-in-machine-learning-geeksforgeeks.md
quality_score: 68
concepts:
  - regularization-techniques-in-linear-regression
related:
  - "[[Linear Regression]]"
  - "[[Linear Regression in Machine Learning - GeeksforGeeks]]"
tier: hot
tags: [regularization, machine-learning, regression, lasso, ridge, elastic-net]
---

# Regularization Techniques in Linear Regression

## Overview

Regularization techniques like Lasso, Ridge, and Elastic Net are used in linear regression to prevent overfitting by penalizing large coefficients. They improve model generalization, especially when dealing with multicollinearity or irrelevant features.

## How It Works

Regularization modifies the linear regression objective function by adding a penalty term that discourages large coefficient values. This helps prevent overfitting, where the model fits noise in the training data rather than the underlying pattern.

**Lasso Regression (L1 Regularization):**
Adds the sum of absolute values of coefficients to the cost function:
\[ J = \text{MSE} + \lambda \sum_{j=1}^n |\theta_j| \]
Lasso can shrink some coefficients to zero, effectively performing feature selection.

**Ridge Regression (L2 Regularization):**
Adds the sum of squared coefficients to the cost function:
\[ J = \text{MSE} + \lambda \sum_{j=1}^n \theta_j^2 \]
Ridge regression is useful when predictors are highly correlated (multicollinearity).

**Elastic Net Regression:**
Combines L1 and L2 penalties:
\[ J = \text{MSE} + \lambda_1 \sum_{j=1}^n |\theta_j| + \lambda_2 \sum_{j=1}^n \theta_j^2 \]
Elastic Net balances feature selection and coefficient shrinkage.

The regularization parameter (λ) controls the strength of the penalty. Higher values increase regularization, reducing overfitting but potentially underfitting if too strong. Regularization is especially important in high-dimensional datasets or when predictors are highly correlated.

## Key Properties

- **Penalty Term:** Lasso: L1; Ridge: L2; Elastic Net: L1 + L2
- **Feature Selection:** Lasso can eliminate irrelevant features by shrinking coefficients to zero.
- **Handling Multicollinearity:** Ridge and Elastic Net are effective when predictors are highly correlated.

## Limitations

Choosing the regularization parameter (λ) is critical; too high can underfit, too low can overfit. Lasso may struggle when predictors are highly correlated. Ridge cannot perform feature selection. Elastic Net requires tuning two parameters.

## Example

Applying Ridge regression in Python:
```python
from sklearn.linear_model import Ridge
model = Ridge(alpha=1.0)
model.fit(X, Y)
```


## Relationship to Other Concepts

- **[[Linear Regression]]** — Regularization extends linear regression to improve generalization.

## Practical Applications

Used in finance, healthcare, and e-commerce for predictive modeling with many features. Essential for high-dimensional datasets, preventing overfitting, and improving model robustness.

## Sources

- [[Linear Regression in Machine Learning - GeeksforGeeks]] — primary source for this concept
