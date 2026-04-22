---
title: "Multinomial Naive Bayes"
type: concept
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "738facc8613e17bebe1ccc6110aded89b719c025ec238ad0ddf175a33ca3d5be"
sources:
  - raw/2026-04-08-naive-bayes-classifiers-geeksforgeeks.md
quality_score: 56
concepts:
  - multinomial-naive-bayes
related:
  - "[[Naive Bayes Classifier]]"
  - "[[Naive Bayes Classifiers - GeeksforGeeks]]"
tier: hot
tags: [classification, probabilistic-model, text-classification, discrete-features]
---

# Multinomial Naive Bayes

## Overview

Multinomial Naive Bayes is a variant of Naive Bayes tailored for discrete features representing counts or frequencies, such as word counts in text documents.

## How It Works

Multinomial Naive Bayes models the likelihood of discrete features using the multinomial distribution. It is especially suitable for text classification tasks, where features are word frequencies or term counts.

**Algorithm Steps:**
1. For each class, estimate the probability of each feature (e.g., word) occurring, based on frequency counts in the training data.
2. For a new document, compute the likelihood of its feature vector under each class's multinomial distribution.
3. Multiply these likelihoods (with the class prior) to obtain the posterior probability for each class.
4. Predict the class with the highest posterior.

**Intuition:**
The multinomial model captures the distribution of term frequencies in documents, making it highly effective for text classification, spam filtering, and sentiment analysis. It assumes that the occurrence of each term is independent given the class.

**Edge Cases:**
- Zero probability for unseen words can be problematic; Laplace smoothing is commonly applied to mitigate this.
- Works best when term frequencies are informative for classification.

**Trade-offs:**
- Multinomial Naive Bayes is robust for text data but less effective for binary or continuous features.

**Complexity:**
- Training: $O(n)$ for frequency counts.
- Prediction: $O(m)$ for likelihood computation.


## Key Properties

- **Multinomial Distribution Assumption:** Discrete features are modeled as counts/frequencies under the multinomial distribution.
- **Text Classification Suitability:** Highly effective for document categorization and spam filtering.
- **Smoothing Techniques:** Laplace smoothing prevents zero probability for unseen features.

## Limitations

Not suitable for continuous or strictly binary features. Sensitive to irrelevant terms and zero probability issues without smoothing.

## Example

In spam filtering, Multinomial Naive Bayes counts the frequency of each word in spam and non-spam emails, then uses these counts to classify new emails based on their word frequencies.

## Relationship to Other Concepts

- **[[Naive Bayes Classifier]]** — Multinomial Naive Bayes is a variant for count-based discrete features.

## Practical Applications

Used in document categorization, sentiment analysis, spam filtering, and topic classification where term frequencies are key.

## Sources

- [[Naive Bayes Classifiers - GeeksforGeeks]] — primary source for this concept
