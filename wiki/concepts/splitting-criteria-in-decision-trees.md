---
title: "Splitting Criteria in Decision Trees"
type: concept
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "64bae2ab67e559be6bdf893fb29bac5a1194853f67a015e0a9239e88019b5bdd"
sources:
  - raw/2026-04-08-decision-tree-geeksforgeeks.md
quality_score: 100
concepts:
  - splitting-criteria-in-decision-trees
related:
  - "[[Decision Tree Algorithm]]"
  - "[[Decision Tree - GeeksforGeeks]]"
tier: hot
tags: [splitting-criteria, gini-impurity, entropy, decision-tree]
---

# Splitting Criteria in Decision Trees

## Overview

Splitting criteria are mathematical measures used to determine the best feature and threshold for partitioning data at each node in a Decision Tree. The most common criteria are Gini impurity and entropy, which help maximize the information gain and improve the tree's predictive power.

## How It Works

At each internal node of a Decision Tree, the algorithm must decide which feature and value to split the data on. This decision is made using splitting criteria that quantify the quality of a split. The two most widely used criteria are:

- **Gini Impurity**: For classification tasks, Gini impurity measures the probability of misclassifying a randomly chosen sample from the node. It is calculated as:
  \[
  Gini = 1 - \sum_{i=1}^{n} p_i^2
  \]
  where \(p_i\) is the proportion of samples belonging to class \(i\) in the node. A lower Gini impurity indicates a more homogeneous node.

- **Entropy**: Entropy measures the disorder or uncertainty in the node. It is defined as:
  \[
  Entropy = -\sum_{i=1}^{n} p_i \log_2 p_i
  \]
  The algorithm seeks to reduce entropy by splitting on features that provide the most information about the target variable (information gain).

For regression tasks, splitting criteria may involve minimizing variance or mean squared error within the resulting subsets.

The algorithm evaluates all possible splits for each feature and selects the one that results in the greatest reduction in impurity or entropy. This process is repeated at each node, recursively partitioning the data until a stopping condition is met (e.g., minimum samples per node, maximum depth, or pure nodes).

Splitting criteria are fundamental to the performance of Decision Trees, as they directly influence the structure and predictive accuracy of the tree. Choosing the right criterion and tuning associated parameters can help balance tree complexity and generalization.

## Key Properties

- **Gini Impurity:** Measures node impurity; lower values indicate better splits for classification.
- **Entropy:** Measures uncertainty; used to maximize information gain at each split.
- **Variance Reduction:** For regression trees, splits aim to minimize variance within subsets.

## Limitations

Splitting criteria can bias the tree towards features with many categories, potentially overlooking simpler, more predictive features. For large datasets, evaluating all possible splits can be computationally intensive. The choice of criterion may affect the interpretability and accuracy of the tree.

## Example

Suppose a node contains samples from two classes, A and B. If 80% are A and 20% are B:

- Gini impurity: \(1 - (0.8^2 + 0.2^2) = 1 - (0.64 + 0.04) = 0.32\)
- Entropy: \(-[0.8 \log_2 0.8 + 0.2 \log_2 0.2] \approx 0.72\)

The algorithm would prefer splits that reduce these values.

## Visual

No specific diagram for splitting criteria, but the tree diagrams illustrate how splits occur at internal nodes based on feature values.

## Relationship to Other Concepts

- **[[Decision Tree Algorithm]]** — Splitting criteria are core to the construction of Decision Trees.

## Practical Applications

Splitting criteria are used in all Decision Tree implementations for tasks such as loan approval, medical diagnosis, and fraud detection, ensuring the tree partitions data effectively for accurate predictions.

## Sources

- [[Decision Tree - GeeksforGeeks]] — primary source for this concept
