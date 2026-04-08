---
title: "Decision Tree Algorithm"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "8068cff7cb6d79c87388b9b9408f59c8234c6cee6ef3847d205df8a8b7b53210"
sources:
  - raw/2026-04-08-top-15-machine-learning-algorithms-every-data-scientist-shou.md
  - raw/2026-04-08-decision-tree-geeksforgeeks.md
quality_score: 0
concepts:
  - decision-tree-algorithm
related:
  - "[[Random Forest Algorithm]]"
  - "[[Support Vector Machine (SVM) Algorithm]]"
  - "[[Apriori Algorithm]]"
  - "[[Decision Tree - GeeksforGeeks]]"
tier: hot
tags: [machine-learning, classification, regression, interpretability, tree-based-models]
---

# Decision Tree Algorithm

## Overview

A Decision Tree is a supervised learning algorithm used for both classification and regression tasks. It models decisions and their possible consequences in a tree-like structure, making it easy to interpret and visualize. Decision Trees are widely used in machine learning due to their versatility and ability to handle both categorical and numerical data.

## How It Works

The Decision Tree algorithm starts with a root node representing the entire dataset. At each node, the algorithm selects a feature and asks a question (often binary, such as yes/no), splitting the data into subsets based on the answer. This process continues recursively, creating branches for each possible outcome. Internal nodes represent decision points based on feature values, while leaf nodes represent final outcomes or predictions.

Splitting criteria are crucial for determining the best feature to split on at each node. Common criteria include Gini impurity and entropy:

- **Gini Impurity** measures the likelihood of incorrect classification of a randomly chosen element if it was randomly labeled according to the distribution of labels in the node. The formula is:
  
  $$ Gini = 1 - \sum_{i=1}^{n} p_i^2 $$
  where $p_i$ is the probability of class $i$ in the node.

- **Entropy** measures the amount of disorder or uncertainty in the node. The formula is:
  
  $$ Entropy = -\sum_{i=1}^{n} p_i \log_2 p_i $$

The algorithm selects the feature and split that maximizes information gain (reduces impurity or entropy the most).

The tree grows until stopping criteria are met, such as reaching a maximum depth, minimum samples per leaf, or no further improvement in impurity reduction. However, deep trees can overfit the training data, capturing noise rather than general patterns. To address this, pruning techniques are applied. Pruning removes branches that have little predictive power, simplifying the tree and improving generalization.

Decision Trees can handle missing values by assigning the most common value or ignoring missing data during splits. They are robust to non-linear relationships and do not require feature scaling or normalization.

The tree structure is highly interpretable, allowing users to trace the decision-making process step by step. However, Decision Trees can be unstable—small changes in the data may lead to significantly different tree structures. They also tend to favor features with many categories, which can bias the model.

For large datasets, building and pruning Decision Trees can be computationally expensive, especially as the tree depth increases. Despite these limitations, Decision Trees remain a foundational technique in machine learning, often serving as the basis for ensemble methods like Random Forests.

## Key Properties

- **Tree Structure:** Composed of root, internal, and leaf nodes; visually maps decision paths.
- **Splitting Criteria:** Uses Gini impurity or entropy to determine optimal feature splits.
- **Interpretability:** Highly interpretable; users can trace decisions from root to leaf.
- **Versatility:** Applicable to both classification and regression tasks.
- **No Feature Scaling Required:** Handles raw data without normalization or scaling.

## Limitations

Decision Trees are prone to overfitting, especially when deep, leading to poor generalization on unseen data. They can be unstable, with small data changes causing large structural shifts. The algorithm may become biased toward features with many categories, potentially ignoring other important features. Decision Trees may struggle to capture complex feature interactions and are computationally intensive for large datasets.

## Example

Consider a Decision Tree for deciding whether to drink coffee:

- Root node: Time of Day (Morning/Afternoon)
- Internal node: Tired? (Yes/No)
- Leaf node: Drink Coffee or No Coffee

```plaintext
Time of Day
├── Morning
│   ├── Tired? Yes → Drink Coffee
│   └── Tired? No → No Coffee
└── Afternoon
    ├── Tired? Yes → Drink Coffee
    └── Tired? No → No Coffee
```

## Visual

Two diagrams illustrate the concept. The first shows a generic tree structure: a root node branching into internal nodes, which further branch into leaf nodes. The second diagram visualizes the coffee decision example, starting with 'Time of Day' and branching into 'Morning' and 'Afternoon', each followed by a 'Tired?' decision, leading to 'Drink Coffee' or 'No'.

## Relationship to Other Concepts

- **[[Random Forest Algorithm]]** — Random Forests are ensembles of Decision Trees, reducing overfitting and instability.
- **[[Support Vector Machine (SVM) Algorithm]]** — Both are used for classification, but SVMs use hyperplanes while Decision Trees use hierarchical splits.
- **[[Apriori Algorithm]]** — Both are used in data mining, but Apriori focuses on association rules while Decision Trees focus on prediction.

## Practical Applications

Decision Trees are used in loan approval (banking), medical diagnosis (healthcare), predicting exam results (education), customer churn prediction (business), and fraud detection (finance). Their interpretability and ability to handle diverse data types make them suitable for automated predictive models in machine learning, data mining, and statistics.

## Sources

- [[Decision Tree - GeeksforGeeks]] — primary source for this concept
- [[Top 15 Machine Learning Algorithms Every Data Scientist Should Know in 2025]] — additional source
