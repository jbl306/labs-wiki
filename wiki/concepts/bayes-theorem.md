---
title: "Bayes' Theorem"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "7f88957808ce58eefae33d9edfda055fb6c6a809b340111b3d89f3c73a7e3b49"
sources:
  - raw/2026-04-08-naive-bayes-classifiers-geeksforgeeks.md
quality_score: 0
concepts:
  - bayes-theorem
related:
  - "[[Naive Bayes Classifier]]"
  - "[[Naive Bayes Classifiers - GeeksforGeeks]]"
tier: hot
tags: [probability, bayesian, machine-learning]
---

# Bayes' Theorem

## Overview

Bayes' Theorem is a foundational principle in probability theory that allows the computation of the probability of a hypothesis given observed evidence. It is central to the Naive Bayes classifier and many other probabilistic models.

## How It Works

Bayes' Theorem provides a way to reverse conditional probabilities, enabling the calculation of the probability of a class given observed features. The theorem is stated as:

$$
P(y|X) = \frac{P(X|y) \cdot P(y)}{P(X)}
$$
where:
- $P(y|X)$ is the posterior probability (probability of class $y$ given features $X$).
- $P(X|y)$ is the likelihood (probability of features $X$ given class $y$).
- $P(y)$ is the prior (probability of class $y$ before seeing the features).
- $P(X)$ is the marginal likelihood (probability of observing features $X$ under all classes).

Bayes' Theorem is used in classification by computing the posterior for each class and selecting the class with the highest probability. In practice, the denominator $P(X)$ is constant for a given input and can be ignored when comparing classes.

**Intuition:**
Bayes' Theorem allows updating beliefs about the likelihood of a hypothesis as new evidence is observed. This is particularly useful in machine learning, where the goal is to infer the most probable class label given observed features.

**Edge Cases:**
If the prior or likelihood is zero, the posterior will be zero. This can be problematic in sparse datasets and is often addressed with smoothing techniques.

## Key Properties

- **Probabilistic Reasoning:** Enables principled reasoning about uncertainty and evidence.
- **Foundation for Bayesian Models:** Forms the basis for many Bayesian inference techniques, including Naive Bayes.

## Limitations

Requires accurate estimation of priors and likelihoods. Sensitive to zero probabilities, which can lead to poor generalization if not handled properly.

## Example

Suppose you want to predict whether it will rain given that the sky is cloudy. If:
- $P(	ext{Rain}) = 0.3$
- $P(	ext{Cloudy}|	ext{Rain}) = 0.8$
- $P(	ext{Cloudy}) = 0.5$

Then:
$$
P(	ext{Rain}|	ext{Cloudy}) = \frac{0.8 \times 0.3}{0.5} = 0.48
$$

## Relationship to Other Concepts

- **[[Naive Bayes Classifier]]** — Uses Bayes' Theorem as its mathematical foundation.

## Practical Applications

Used in probabilistic classification, Bayesian inference, medical diagnosis, spam filtering, and any domain requiring reasoning under uncertainty.

## Sources

- [[Naive Bayes Classifiers - GeeksforGeeks]] — primary source for this concept
