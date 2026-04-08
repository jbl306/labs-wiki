---
title: "Maximum Likelihood Estimation in Logistic Regression"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "cc9f0a06fdc1e5b2ca1a3d132d3204277ea1fcf5c85d34f4c17c99e0570d79e5"
sources:
  - raw/2026-04-08-logistic-regression-in-machine-learning-geeksforgeeks.md
quality_score: 0
concepts:
  - maximum-likelihood-estimation-in-logistic-regression
related:
  - "[[Gradient Descent in Linear Regression]]"
  - "[[Logistic Regression in Machine Learning - GeeksforGeeks]]"
tier: hot
tags: [optimization, statistical-inference, logistic-regression, maximum-likelihood]
---

# Maximum Likelihood Estimation in Logistic Regression

## Overview

Maximum likelihood estimation (MLE) is the method used to fit the parameters of logistic regression. It seeks to find the weights and bias that maximize the probability of observing the given data, ensuring the model's predictions align closely with the actual outcomes.

## How It Works

MLE in logistic regression involves constructing a likelihood function based on the predicted probabilities for each data point. For binary classification, the likelihood for a single observation is:

- If $y_i = 1$, the likelihood is $p(x_i)$.
- If $y_i = 0$, the likelihood is $1 - p(x_i)$.

For a dataset of $n$ observations, the overall likelihood is:

$$ L(b, w) = \prod_{i=1}^{n} p(x_i)^{y_i} (1 - p(x_i))^{1 - y_i} $$

Taking the logarithm yields the log-likelihood:

$$ \log(L(b, w)) = \sum_{i=1}^{n} y_i \log p(x_i) + (1 - y_i) \log(1 - p(x_i)) $$

The log-likelihood is maximized with respect to the weights and bias using gradient ascent. The gradient with respect to each weight $w_j$ is:

$$ \frac{\partial J(l(b, w))}{\partial w_j} = \sum_{i=1}^{n} (y_i - p(x_i; b, w)) x_{ij} $$

This formula expresses how the difference between the actual label and predicted probability, multiplied by the feature value, accumulates over all samples. The optimization iteratively updates the weights in the direction that increases the log-likelihood, converging to the best-fit parameters.

MLE is preferred over least squares in logistic regression because the target variable is categorical, and the likelihood function is specifically designed to handle probabilities. The approach is robust and provides interpretable coefficients, but requires careful handling of numerical stability and convergence, especially with large datasets or many features.

MLE also forms the basis for statistical inference in logistic regression, enabling confidence intervals and hypothesis testing for model parameters.

## Key Properties

- **Objective:** Maximize the likelihood of observed data given model parameters.
- **Optimization:** Uses gradient ascent on the log-likelihood function.
- **Interpretability:** Coefficients represent the log-odds change per unit change in predictor.

## Limitations

MLE can be sensitive to outliers and may not converge if the data is perfectly separable. It requires a sufficiently large sample size for stable estimates and can be computationally intensive for large datasets. Numerical instability may occur with extreme probabilities.

## Example

Given a dataset:
- For each sample, compute $p(x_i)$ using the sigmoid function.
- Calculate log-likelihood:
  $$ \log(L(b, w)) = \sum_{i=1}^{n} y_i \log p(x_i) + (1 - y_i) \log(1 - p(x_i)) $$
- Update weights using gradient ascent:
  $$ w_j \leftarrow w_j + \alpha \sum_{i=1}^{n} (y_i - p(x_i)) x_{ij} $$
where $\alpha$ is the learning rate.

## Relationship to Other Concepts

- **[[Gradient Descent in Linear Regression]]** — Both use gradient-based optimization, but logistic regression uses gradient ascent on log-likelihood.

## Practical Applications

MLE is used to fit logistic regression models in medical research, social sciences, and business analytics, providing interpretable coefficients and robust predictions for classification tasks.

## Sources

- [[Logistic Regression in Machine Learning - GeeksforGeeks]] — primary source for this concept
