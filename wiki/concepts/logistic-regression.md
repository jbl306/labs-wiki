---
title: "Logistic Regression"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "cc9f0a06fdc1e5b2ca1a3d132d3204277ea1fcf5c85d34f4c17c99e0570d79e5"
sources:
  - raw/2026-04-08-logistic-regression-in-machine-learning-geeksforgeeks.md
quality_score: 0
concepts:
  - logistic-regression
related:
  - "[[Linear Regression]]"
  - "[[Activation Functions in Neural Networks]]"
  - "[[Logistic Regression in Machine Learning - GeeksforGeeks]]"
tier: hot
tags: [classification, machine-learning, supervised-learning, python, scikit-learn]
---

# Logistic Regression

## Overview

Logistic regression is a supervised learning algorithm designed for classification tasks, particularly binary classification. It models the probability that a given input belongs to a specific class by applying a sigmoid function to a linear combination of input features. Unlike linear regression, which predicts continuous values, logistic regression outputs probabilities, making it suitable for problems where the target variable is categorical.

## How It Works

Logistic regression operates by first computing a weighted sum of the input features, often called the linear predictor. This is expressed mathematically as:

$$ z = w \cdot X + b $$

where $w$ represents the vector of weights (coefficients), $X$ is the feature vector, and $b$ is the bias (intercept). The result $z$ is a real-valued number, similar to the output of linear regression.

To transform this linear output into a probability, logistic regression applies the sigmoid function:

$$ \sigma(z) = \frac{1}{1 + e^{-z}} $$

The sigmoid function maps any real number into the range (0, 1), forming an S-shaped curve. This output can be interpreted as the probability that the input belongs to the positive class (e.g., '1' or 'Yes'). A threshold (commonly 0.5) is used to assign a class label: if $\sigma(z) \geq 0.5$, the input is classified as the positive class; otherwise, it is classified as the negative class.

The model is trained using maximum likelihood estimation (MLE), which seeks to find the weights and bias that maximize the likelihood of observing the given data. The likelihood function for logistic regression is:

$$ L(b, w) = \prod_{i=1}^{n} p(x_i)^{y_i} (1 - p(x_i))^{1 - y_i} $$

Taking the natural logarithm yields the log-likelihood:

$$ \log(L(b, w)) = \sum_{i=1}^{n} y_i \log p(x_i) + (1 - y_i) \log(1 - p(x_i)) $$

Optimization is typically performed using gradient ascent, where the gradient of the log-likelihood with respect to each weight $w_j$ is:

$$ \frac{\partial J(l(b, w))}{\partial w_j} = \sum_{i=1}^{n} (y_i - p(x_i; b, w)) x_{ij} $$

This iterative process adjusts the weights to improve the fit of the model.

Logistic regression can be extended to handle multiclass classification via multinomial logistic regression, which uses the softmax function instead of the sigmoid. For ordinal classification, ordinal logistic regression incorporates the order of categories.

Intuitively, logistic regression is favored for its simplicity, interpretability, and effectiveness in situations where the relationship between predictors and the log-odds of the outcome is linear. It is robust to moderate violations of its assumptions but can be sensitive to outliers and collinearity among predictors.

## Key Properties

- **Type:** Supervised classification algorithm; primarily binary but extendable to multiclass and ordinal problems.
- **Output:** Probability value between 0 and 1, thresholded to assign class labels.
- **Estimation Method:** Maximum likelihood estimation (MLE) using gradient ascent.
- **Time Complexity:** Training: O(n*m*iterations), where n is the number of samples, m is the number of features. Prediction: O(m).

## Limitations

Logistic regression assumes independent observations and a linear relationship between predictors and log-odds. It is sensitive to extreme outliers, requires a sufficiently large sample size, and can be affected by multicollinearity among features. It may struggle with complex, non-linear decision boundaries and is not suitable for regression tasks involving continuous target variables.

## Example

```python
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=23)
clf = LogisticRegression(max_iter=10000, random_state=0)
clf.fit(X_train, y_train)
acc = accuracy_score(y_test, clf.predict(X_test)) * 100
print(f"Logistic Regression model accuracy: {acc:.2f}%")
# Output: Logistic Regression model accuracy (in %): 96.49%
```

## Visual

A chart depicting the sigmoid function: the curve rises steeply between -2 and 2, mapping values from near 0 (for large negative inputs) to near 1 (for large positive inputs). The formula sig(t) = 1/(1+e^{-z}) is shown, illustrating how the function transforms linear outputs into probabilities.

## Relationship to Other Concepts

- **[[Linear Regression]]** — Linear regression predicts continuous values, while logistic regression predicts probabilities for categorical outcomes.
- **[[Activation Functions in Neural Networks]]** — The sigmoid function used in logistic regression is a common activation function in neural networks.

## Practical Applications

Logistic regression is widely used in medical diagnosis (e.g., predicting disease presence), credit scoring (e.g., loan approval), marketing (e.g., predicting customer churn), and any scenario where the outcome is categorical. It is favored for its interpretability and ease of implementation in situations with linear relationships and moderate feature sizes.

## Sources

- [[Logistic Regression in Machine Learning - GeeksforGeeks]] — primary source for this concept
