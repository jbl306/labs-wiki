---
title: "Gradient Descent in Linear Regression"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "64f3d7794fd5e8567333444aa2dcf2ae76e118f9bf78cb15eb014a7029e90e95"
sources:
  - raw/2026-04-08-linear-regression-in-machine-learning-geeksforgeeks.md
quality_score: 0
concepts:
  - gradient-descent-in-linear-regression
related:
  - "[[Linear Regression]]"
  - "[[Linear Regression in Machine Learning - GeeksforGeeks]]"
tier: hot
tags: [optimization, machine-learning, regression, gradient-descent]
---

# Gradient Descent in Linear Regression

## Overview

Gradient descent is an iterative optimization algorithm used to minimize the cost function in linear regression, enabling the model to find the best-fit line for the data. It systematically adjusts model parameters to reduce prediction error.

## How It Works

Gradient descent begins with random initial values for the model parameters (slope and intercept in simple linear regression). The algorithm computes the gradient, which is the partial derivative of the cost function (typically MSE) with respect to each parameter. This gradient indicates the direction and magnitude of change needed to reduce the error.

At each iteration, the parameters are updated by moving in the direction opposite to the gradient, scaled by a learning rate (α):
\[ \theta_j := \theta_j - \alpha \frac{\partial J}{\partial \theta_j} \]
where \( J \) is the cost function, \( \theta_j \) is the parameter, and \( \alpha \) is the learning rate.

The process repeats until convergence, i.e., when the change in cost function between iterations falls below a threshold or a maximum number of iterations is reached. Gradient descent can be applied in batch (using all data), stochastic (using one data point at a time), or mini-batch (using subsets) modes.

The algorithm is robust and computationally efficient, especially for large datasets and high-dimensional spaces. However, the choice of learning rate is critical: too high can cause divergence, too low can slow convergence. Gradient descent finds the global minimum for convex cost functions (like MSE in linear regression), but may get stuck in local minima for non-convex problems.

In linear regression, gradient descent ensures the model parameters are optimized to minimize prediction error, resulting in the best-fit line for the data.

## Key Properties

- **Optimization Method:** Iteratively updates parameters to minimize cost function (MSE).
- **Learning Rate:** Controls step size in parameter updates; critical for convergence.
- **Convergence:** Guaranteed for convex cost functions; may require tuning for speed and stability.

## Limitations

Sensitive to learning rate selection; improper choice can cause slow convergence or divergence. May get stuck in local minima for non-convex functions (not an issue for linear regression). Requires careful initialization and stopping criteria. Computational cost increases with dataset size and number of features.

## Example

Gradient descent for linear regression:
```python
# Cost function: J = (1/n) * sum((y_pred - y_actual)**2)
# Parameter update:
for epoch in range(num_epochs):
    y_pred = theta_0 + theta_1 * X
    error = y_pred - Y
    theta_0 -= alpha * error.mean()
    theta_1 -= alpha * (error * X).mean()
```


## Visual

The gradient descent diagram shows a cost curve (J(θ)) with steps from initial weight toward minimum cost, illustrating how the algorithm moves parameters to minimize error.

## Relationship to Other Concepts

- **[[Linear Regression]]** — Gradient descent is used to optimize linear regression parameters.

## Practical Applications

Used in training linear regression models for large datasets, real-time applications, and high-dimensional data. Forms the basis for optimization in many machine learning algorithms.

## Sources

- [[Linear Regression in Machine Learning - GeeksforGeeks]] — primary source for this concept
