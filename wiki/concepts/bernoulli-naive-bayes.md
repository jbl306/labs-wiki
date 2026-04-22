---
title: "Bernoulli Naive Bayes"
type: concept
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "738facc8613e17bebe1ccc6110aded89b719c025ec238ad0ddf175a33ca3d5be"
sources:
  - raw/2026-04-08-naive-bayes-classifiers-geeksforgeeks.md
quality_score: 56
concepts:
  - bernoulli-naive-bayes
related:
  - "[[Naive Bayes Classifier]]"
  - "[[Naive Bayes Classifiers - GeeksforGeeks]]"
tier: hot
tags: [classification, probabilistic-model, binary-features, text-classification]
---

# Bernoulli Naive Bayes

## Overview

Bernoulli Naive Bayes is a variant of Naive Bayes designed for binary features, where each feature represents the presence or absence of a term or attribute.

## How It Works

Bernoulli Naive Bayes models the likelihood of binary features using the Bernoulli distribution. Each feature is treated as a binary indicator (0 or 1), and the model estimates the probability of each feature being present or absent for each class.

**Algorithm Steps:**
1. For each class, estimate the probability of each feature being present (value 1) or absent (value 0) from the training data.
2. For a new sample, compute the likelihood of its binary feature vector under each class's Bernoulli distribution.
3. Multiply these likelihoods (with the class prior) to obtain the posterior probability for each class.
4. Predict the class with the highest posterior.

**Intuition:**
Bernoulli Naive Bayes is effective when the presence or absence of features (e.g., words in a document) is more informative than their frequency. It is commonly used in document classification tasks where binary indicators are relevant.

**Edge Cases:**
- Not suitable for count-based or continuous features.
- Sensitive to irrelevant features and zero probability issues.

**Trade-offs:**
- Works best when binary features are truly informative for classification.

**Complexity:**
- Training: $O(n)$ for probability estimation.
- Prediction: $O(m)$ for likelihood computation.


## Key Properties

- **Binary Feature Modeling:** Features are modeled as binary indicators under the Bernoulli distribution.
- **Presence/Absence Relevance:** Effective when the presence or absence of features is more important than their frequency.

## Limitations

Not suitable for count-based or continuous features. Sensitive to irrelevant features and zero probability issues.

## Example

In document classification, Bernoulli Naive Bayes checks whether each word is present or absent in a document and uses these binary indicators to classify the document.

## Relationship to Other Concepts

- **[[Naive Bayes Classifier]]** — Bernoulli Naive Bayes is a variant for binary features.

## Practical Applications

Used in document classification and sentiment analysis where binary feature presence is key.

## Sources

- [[Naive Bayes Classifiers - GeeksforGeeks]] — primary source for this concept
