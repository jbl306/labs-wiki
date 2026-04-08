---
title: "Gaussian Naive Bayes"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "7f88957808ce58eefae33d9edfda055fb6c6a809b340111b3d89f3c73a7e3b49"
sources:
  - raw/2026-04-08-naive-bayes-classifiers-geeksforgeeks.md
quality_score: 0
concepts:
  - gaussian-naive-bayes
related:
  - "[[Naive Bayes Classifier]]"
  - "[[Naive Bayes Classifiers - GeeksforGeeks]]"
tier: hot
tags: [machine-learning, classification, gaussian, probabilistic-model]
---

# Gaussian Naive Bayes

## Overview

Gaussian Naive Bayes is a variant of the Naive Bayes classifier designed for continuous features, assuming each feature is normally distributed within each class. It is commonly used in scenarios where numerical data is prevalent.

## How It Works

In Gaussian Naive Bayes, the likelihood of each continuous feature given the class is modeled using a Gaussian (normal) distribution. For a feature $x_i$ and class $y$, the likelihood is:

$$
P(x_i | y) = \frac{1}{\sqrt{2\pi\sigma^2_y}} \exp\left( -\frac{(x_i - \mu_y)^2}{2\sigma^2_y} \right)
$$
where:
- $\mu_y$ is the mean of feature $x_i$ for class $y$.
- $\sigma^2_y$ is the variance of feature $x_i$ for class $y$.

During training, the algorithm estimates the mean and variance for each feature-class combination. For prediction, it computes the likelihood for each feature using the Gaussian formula, multiplies these likelihoods across features (assuming independence), and combines with the prior to get the posterior probability for each class.

**Intuition:**
The Gaussian assumption allows the classifier to handle continuous data efficiently. The bell-shaped curve of the normal distribution captures the spread and central tendency of feature values within each class.

**Edge Cases:**
If the actual feature distribution is not normal, performance may suffer. Outliers can skew the mean and variance estimates, affecting predictions.

## Key Properties

- **Handles Continuous Data:** Assumes features are normally distributed within each class.
- **Parameter Estimation:** Estimates mean and variance for each feature-class combination.

## Limitations

Assumes normality of feature distributions, which may not hold in practice. Sensitive to outliers and non-Gaussian distributions.

## Example

Suppose feature 'Temperature' for class 'Yes' has mean 24°C and variance 4. For a new sample with Temperature = 26°C:

$$
P(26 | 	ext{Yes}) = \frac{1}{\sqrt{2\pi \times 4}} \exp\left( -\frac{(26 - 24)^2}{2 \times 4} \right)
$$

## Visual

A bell-shaped curve representing the normal distribution of a feature within a class, symmetric about the mean.

## Relationship to Other Concepts

- **[[Naive Bayes Classifier]]** — Gaussian Naive Bayes is a variant for continuous features.

## Practical Applications

Used in medical diagnosis, credit scoring, and any domain with continuous numerical features.

## Sources

- [[Naive Bayes Classifiers - GeeksforGeeks]] — primary source for this concept
