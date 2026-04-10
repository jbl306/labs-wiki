---
title: "Pruning In Decision Trees"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "8068cff7cb6d79c87388b9b9408f59c8234c6cee6ef3847d205df8a8b7b53210"
sources:
  - raw/2026-04-08-decision-tree-geeksforgeeks.md
quality_score: 100
concepts:
  - pruning-in-decision-trees
related:
  - "[[Decision Tree - GeeksforGeeks]]"
tier: hot
tags: [pruning, overfitting, model-simplification, tree-based-models]
---

# Pruning In Decision Trees

## Overview

Pruning is a technique used to reduce the complexity of Decision Trees and prevent overfitting. By removing branches that have little predictive power, pruning helps the model generalize better to unseen data and improves performance.

## How It Works

As Decision Trees grow deeper, they can start to memorize the training data, capturing noise and irrelevant patterns. This phenomenon, known as overfitting, leads to poor performance on new, unseen data. Pruning addresses this by systematically removing branches that do not contribute significantly to the model's predictive accuracy.

There are two main types of pruning:

- **Pre-pruning (Early Stopping):** The tree growth is halted before it becomes too complex. Criteria such as maximum depth, minimum samples per leaf, or minimum impurity decrease are used to stop splitting early.

- **Post-pruning (Reduced Error Pruning):** The tree is first grown to its full depth, then branches are removed based on their impact on validation error or predictive power. This can involve replacing subtrees with leaf nodes if the subtree does not improve performance.

Pruning can be implemented using algorithms like cost-complexity pruning, which balances tree complexity against predictive accuracy. The process involves evaluating each branch's contribution to the overall model and removing those that do not meet a threshold.

Pruning not only improves generalization but also simplifies the model, making it faster to deploy and easier to interpret. It is especially useful when the tree is deep and starts to capture noise in the data. However, excessive pruning can lead to underfitting, where the model becomes too simple and fails to capture important patterns.

The trade-off between overfitting and underfitting is managed by tuning pruning parameters, often validated using cross-validation techniques.

## Key Properties

- **Reduces Overfitting:** Removes branches that memorize training data, improving generalization.
- **Simplifies Model:** Results in a smaller, faster, and more interpretable tree.
- **Improves Performance:** Enhances predictive accuracy on unseen data.

## Limitations

If pruning is too aggressive, the model may underfit, missing important patterns in the data. Determining optimal pruning parameters can be challenging and may require cross-validation. Pruning may not fully address instability or bias toward features with many categories.

## Example

Suppose a Decision Tree for loan approval has deep branches based on rare applicant features. Pruning removes these branches, leaving only those that contribute to accurate predictions for most applicants. This results in a simpler tree that generalizes better.

## Visual

No specific pruning diagram in the source, but the generic tree diagram illustrates how branches can be removed to simplify the structure.

## Relationship to Other Concepts

- **Underfitting and Overfitting in ML** — Pruning is a technique to manage the balance between overfitting and underfitting.
- **Cross Validation in Machine Learning** — Cross-validation is used to validate pruning effectiveness and tune parameters.

## Practical Applications

Pruning is essential in deploying Decision Trees for real-world applications such as loan approval, medical diagnosis, and fraud detection, where model simplicity and generalization are critical for reliable decision-making.

## Sources

- [[Decision Tree - GeeksforGeeks]] — primary source for this concept
