---
title: "Naive Bayes Classifier"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "7f88957808ce58eefae33d9edfda055fb6c6a809b340111b3d89f3c73a7e3b49"
sources:
  - raw/2026-04-08-naive-bayes-classifiers-geeksforgeeks.md
quality_score: 0
concepts:
  - naive-bayes-classifier
related:
  - "[[Bayes' Theorem]]"
  - "[[Gaussian Naive Bayes]]"
  - "[[Multinomial Naive Bayes]]"
  - "[[Bernoulli Naive Bayes]]"
  - "[[Naive Bayes Classifiers - GeeksforGeeks]]"
tier: hot
tags: [machine-learning, classification, probabilistic-model, bayesian]
---

# Naive Bayes Classifier

## Overview

The Naive Bayes classifier is a simple yet powerful probabilistic algorithm used for classification tasks in machine learning. It operates by applying Bayes' Theorem with the 'naive' assumption that all features in the dataset are independent given the class label. Despite its simplicity, Naive Bayes is widely used in real-world applications such as spam filtering, document categorization, and sentiment analysis.

## How It Works

Naive Bayes classifiers are grounded in Bayes' Theorem, which provides a principled way to reverse conditional probabilities. For classification, the algorithm computes the posterior probability of each class given the observed features and selects the class with the highest probability. The formula for Bayes' Theorem is:

$$
P(y|X) = \frac{P(X|y) \cdot P(y)}{P(X)}
$$
where:
- $P(y|X)$ is the posterior probability of class $y$ given features $X$.
- $P(X|y)$ is the likelihood of features $X$ given class $y$.
- $P(y)$ is the prior probability of class $y$.
- $P(X)$ is the marginal likelihood of features $X$.

The 'naive' assumption simplifies the likelihood calculation by assuming that each feature is independent given the class. Thus:

$$
P(x_1, x_2, ..., x_n | y) = \prod_{i=1}^{n} P(x_i | y)
$$

This allows the classifier to compute:

$$
P(y|x_1, ..., x_n) \propto P(y) \cdot \prod_{i=1}^{n} P(x_i | y)
$$

For each class, the algorithm calculates this product and selects the class with the highest value as the prediction.

**Algorithm Steps:**
1. Calculate prior probabilities for each class from the training data.
2. For each feature, calculate conditional probabilities for each class (using frequency tables for categorical features or Gaussian distributions for continuous features).
3. For a new input, compute the product of prior and conditional probabilities for each class.
4. Normalize the probabilities (optional, for interpretability).
5. Predict the class with the highest posterior probability.

**Example:**
Given a weather dataset with features like Outlook, Temperature, Humidity, and Wind, and a class variable 'Play Golf' (Yes/No), the classifier computes probabilities for each class based on the observed feature values. For instance, for input (Sunny, Hot, Normal, False), the algorithm calculates:

- $P(\text{Yes}|\text{Sunny, Hot, Normal, False})$
- $P(\text{No}|\text{Sunny, Hot, Normal, False})$

using the frequency of each feature value in the dataset for each class. The class with the higher probability is predicted.

**Variants:**
- *Gaussian Naive Bayes*: Assumes continuous features are normally distributed within each class. The likelihood is computed using the Gaussian formula:
  $$
  P(x_i | y) = \frac{1}{\sqrt{2\pi\sigma^2_y}} \exp\left( -\frac{(x_i - \mu_y)^2}{2\sigma^2_y} \right)
  $$
- *Multinomial Naive Bayes*: Used for discrete features, especially term frequencies in text classification.
- *Bernoulli Naive Bayes*: Used for binary features, such as the presence or absence of a word in a document.

**Intuition:**
Naive Bayes works well when features are truly independent, but even when this assumption is violated, it often performs surprisingly well, especially in high-dimensional spaces like text data. Its simplicity, speed, and effectiveness with limited data make it a popular baseline classifier.

**Edge Cases & Trade-offs:**
- The independence assumption can lead to poor performance when features are strongly correlated.
- Zero probability for unseen feature values (can be mitigated with smoothing techniques).
- Works best with categorical or normally distributed numerical features.

## Key Properties

- **Time Complexity:** Training: O(n) where n is the number of samples; Prediction: O(m) where m is the number of features.
- **Parameter Efficiency:** Requires very few parameters; only the probabilities for each feature-class combination.
- **Probabilistic Output:** Provides interpretable probability estimates for each class.

## Limitations

The primary limitation is the assumption of feature independence, which rarely holds in real-world data. This can lead to suboptimal predictions when features are correlated. Naive Bayes can also assign zero probability to unseen events, making it sensitive to rare feature values (addressed by Laplace smoothing). It may be influenced by irrelevant features and does not handle missing data natively.

## Example

Suppose we have a dataset for weather conditions and whether golf is played:

```python
# Example feature values
X = ('Sunny', 'Hot', 'Normal', False)

# Prior probabilities
P_yes = 9/14
P_no = 5/14

# Conditional probabilities (from frequency tables)
P_sunny_yes = 2/9
P_hot_yes = 2/9
P_normal_yes = 6/9
P_false_yes = 6/9

P_sunny_no = 3/5
P_hot_no = 2/5
P_normal_no = 1/5
P_false_no = 2/5

# Compute posteriors
P_yes_today = P_sunny_yes * P_hot_yes * P_normal_yes * P_false_yes * P_yes
P_no_today = P_sunny_no * P_hot_no * P_normal_no * P_false_no * P_no

# Normalize
P_yes_today_norm = P_yes_today / (P_yes_today + P_no_today)
P_no_today_norm = P_no_today / (P_yes_today + P_no_today)

# Prediction
prediction = 'Yes' if P_yes_today_norm > P_no_today_norm else 'No'
```


## Visual

A table showing conditional probabilities for each feature value given class labels (Yes/No):
| Feature     | Value   | P(Value|Yes) | P(Value|No) |
|------------|---------|-------------|-------------|
| Outlook    | Sunny   | 2/9         | 3/5         |
| Temperature| Hot     | 2/9         | 2/5         |
| Humidity   | Normal  | 6/9         | 1/5         |
| Wind       | False   | 6/9         | 2/5         |
This table is used to compute the likelihoods for each class.

## Relationship to Other Concepts

- **[[Bayes' Theorem]]** — Naive Bayes is built directly on Bayes' Theorem for probabilistic classification.
- **[[Gaussian Naive Bayes]]** — A variant for continuous features using Gaussian distributions.
- **[[Multinomial Naive Bayes]]** — A variant for discrete features, especially term frequencies.
- **[[Bernoulli Naive Bayes]]** — A variant for binary features.

## Practical Applications

Naive Bayes is widely used in:
- Spam email filtering: Classifies emails as spam or not based on feature probabilities.
- Text classification: Sentiment analysis, document categorization, topic classification.
- Medical diagnosis: Predicts disease likelihood based on symptoms.
- Credit scoring: Evaluates creditworthiness for loan approval.
- Weather prediction: Classifies weather conditions based on observed features.

## Sources

- [[Naive Bayes Classifiers - GeeksforGeeks]] — primary source for this concept
