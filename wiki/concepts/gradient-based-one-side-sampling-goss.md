---
title: "Gradient-Based One-Side Sampling (GOSS)"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "4283d5051205b4b685c0610b6b50ef642f6ff15e703f606bbbbbed91a7f5b021"
sources:
  - raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md
quality_score: 72
concepts:
  - gradient-based-one-side-sampling-goss
related:
  - "[[AdaBoost Algorithm]]"
  - "[[LightGBM (Light Gradient Boosting Machine) - GeeksforGeeks]]"
tier: hot
tags: [lightgbm, gradient-boosting, sampling, goss]
---

# Gradient-Based One-Side Sampling (GOSS)

## Overview

GOSS is an innovative sampling technique in LightGBM that prioritizes instances with large gradients during training. This method accelerates learning and improves efficiency without sacrificing accuracy.

## How It Works

In gradient boosting, each iteration focuses on correcting errors made by previous models. The gradient of the loss function with respect to each instance indicates how much the model needs to adjust its prediction for that instance. GOSS leverages this by sampling more heavily from instances with large gradients, which are typically harder to predict and contribute more to the overall loss.

The algorithm works by first sorting all training instances based on their gradient values. It then selects a fixed proportion of instances with the largest gradients (say, top 20%) and randomly samples from the remaining instances with small gradients (say, 20% of the rest). This ensures that the model pays more attention to difficult cases while still maintaining some coverage of easier cases.

To correct for the imbalance introduced by sampling, GOSS applies a scaling factor to the gradients of the randomly sampled instances, ensuring that the overall gradient statistics remain unbiased. This allows LightGBM to train faster, as fewer instances are used in each iteration, but the most informative samples are prioritized.

The trade-off is between speed and accuracy: GOSS can significantly reduce training time, especially for large datasets, but if the sampling proportions are not chosen carefully, model performance may suffer. Proper tuning of GOSS parameters is crucial for maintaining accuracy.

## Key Properties

- **Sampling Strategy:** Prioritizes instances with large gradients, randomly samples from those with small gradients.
- **Efficiency:** Reduces the number of training instances per iteration, accelerating training.
- **Bias Correction:** Applies scaling to maintain unbiased gradient statistics.

## Limitations

If the sampling proportions are set incorrectly, GOSS may overlook important patterns in the data, leading to reduced accuracy. It is less effective for small datasets where all instances are informative.

## Example

In a dataset with 100,000 samples, GOSS might select the top 20,000 samples with highest gradients and randomly sample 20,000 from the remaining 80,000. The gradients of the randomly sampled instances are scaled to ensure unbiased updates.

## Visual

No explicit diagram in source, but a GOSS illustration would show a histogram of gradient values, with high-gradient samples fully selected and low-gradient samples partially sampled.

## Relationship to Other Concepts

- **Gradient Boosting** — GOSS is a sampling innovation within gradient boosting.
- **[[AdaBoost Algorithm]]** — Both focus on difficult-to-predict instances, but GOSS uses gradient information.

## Practical Applications

GOSS is used in LightGBM to speed up training on large datasets, especially in scenarios where computational resources are limited and rapid model iteration is needed.

## Sources

- [[LightGBM (Light Gradient Boosting Machine) - GeeksforGeeks]] — primary source for this concept
