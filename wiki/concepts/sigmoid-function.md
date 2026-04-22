---
title: "Sigmoid Function"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "cc9f0a06fdc1e5b2ca1a3d132d3204277ea1fcf5c85d34f4c17c99e0570d79e5"
sources:
  - raw/2026-04-08-logistic-regression-in-machine-learning-geeksforgeeks.md
quality_score: 64
concepts:
  - sigmoid-function
related:
  - "[[Activation Functions in Neural Networks]]"
  - "[[Logistic Regression in Machine Learning - GeeksforGeeks]]"
tier: hot
tags: [activation-function, probability, machine-learning, logistic-regression]
---

# Sigmoid Function

## Overview

The sigmoid function is a mathematical function that maps any real-valued input into the range (0, 1). It is central to logistic regression, where it converts the linear predictor into a probability, enabling binary classification.

## How It Works

The sigmoid function is defined as:

$$ \sigma(z) = \frac{1}{1 + e^{-z}} $$

This function takes a real number $z$ and outputs a value between 0 and 1. As $z$ approaches positive infinity, $\sigma(z)$ approaches 1; as $z$ approaches negative infinity, $\sigma(z)$ approaches 0. The function forms an S-shaped curve, which is visually depicted in the source as a steep rise between -2 and 2, flattening out at the extremes.

In logistic regression, the sigmoid function is applied to the linear combination of features and weights to produce a probability. This probability is then thresholded (commonly at 0.5) to assign a class label. The sigmoid function is differentiable, which is essential for gradient-based optimization methods such as gradient ascent used in logistic regression.

The function's properties make it ideal for modeling probabilities, as it ensures outputs are bounded between 0 and 1. It also provides a smooth transition between classes, which helps in modeling uncertainty and probabilistic outcomes.

The derivative of the sigmoid function is:

$$ \sigma'(z) = \sigma(z) \cdot (1 - \sigma(z)) $$

This property is useful in backpropagation and optimization, as it simplifies the computation of gradients.

The sigmoid function is also used in neural networks as an activation function, although it can suffer from vanishing gradients for extreme input values. In logistic regression, its bounded output and monotonicity are crucial for interpreting model predictions as probabilities.

## Key Properties

- **Range:** Outputs values strictly between 0 and 1.
- **Shape:** S-shaped (logistic curve), steepest at z=0.
- **Derivative:** Derivative is σ(z) * (1 - σ(z)), facilitating gradient-based optimization.

## Limitations

The sigmoid function can suffer from vanishing gradients for large positive or negative inputs, making optimization slow in deep learning contexts. In logistic regression, this is less problematic due to the shallow nature of the model. The function is also not suitable for multiclass classification, where the softmax function is preferred.

## Example

For z = 0:
$$ \sigma(0) = \frac{1}{1 + e^{0}} = 0.5 $$

For z = 2:
$$ \sigma(2) = \frac{1}{1 + e^{-2}} \approx 0.88 $$

For z = -2:
$$ \sigma(-2) = \frac{1}{1 + e^{2}} \approx 0.12 $$

## Visual

A chart showing the sigmoid curve: the function starts near 0 for t=-8, rises sharply around t=0, and approaches 1 for t=8. The formula sig(t) = 1/(1+e^{-z}) is displayed alongside the curve.

## Relationship to Other Concepts

- **[[Activation Functions in Neural Networks]]** — Sigmoid is a classic activation function used in neural networks for binary outputs.
- **Softmax Function** — Softmax generalizes sigmoid for multiclass classification.

## Practical Applications

Used in logistic regression for binary classification, in neural networks for output layers, and in probabilistic modeling where outputs must be bounded between 0 and 1.

## Sources

- [[Logistic Regression in Machine Learning - GeeksforGeeks]] — primary source for this concept
