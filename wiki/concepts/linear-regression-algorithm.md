---
title: "Linear Regression Algorithm"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "c892018b8120e90b1106c76253490edb44602548be1401649da66b3872a23c74"
sources:
  - raw/2026-04-08-top-15-machine-learning-algorithms-every-data-scientist-shou.md
quality_score: 100
concepts:
  - linear-regression-algorithm
related:
  - "[[Logistic Regression]]"
  - "[[Regularization Techniques in Linear Regression]]"
  - "[[Top 15 Machine Learning Algorithms Every Data Scientist Should Know in 2025]]"
tier: hot
tags: [supervised-learning, regression, prediction, interpretability]
---

# Linear Regression Algorithm

## Overview

Linear Regression is a foundational supervised learning algorithm used to model the relationship between an independent variable and a dependent variable by fitting a linear equation to observed data. It is widely applied for prediction and trend analysis in domains such as finance, real estate, and economics.

## How It Works

Linear Regression operates by finding the best-fitting straight line (y = mx + c) that minimizes the sum of squared differences between the predicted and actual values of the dependent variable. The algorithm uses a dataset containing pairs of input features and output values, and applies techniques such as Ordinary Least Squares (OLS) to estimate the coefficients (weights) for each feature.

The process begins with data collection and preprocessing, ensuring that relevant features are selected and normalized if necessary. The model is then trained by solving for the coefficients that minimize the mean squared error (MSE):

\[
MSE = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
\]

where \(y_i\) is the actual value and \(\hat{y}_i\) is the predicted value. The solution involves matrix operations, and for multiple features, the equation becomes:

\[
\hat{\beta} = (X^TX)^{-1}X^Ty
\]

where X is the matrix of input features and y is the vector of outputs.

Once trained, the model can predict new values by plugging new feature values into the learned equation. Linear Regression assumes linearity, independence, homoscedasticity, and normality of errors, which are critical for its validity. It is computationally efficient, with time complexity O(n × d^2) and auxiliary space O(d), making it suitable for large datasets with moderate feature counts.

Edge cases include handling multicollinearity (correlated features), outliers, and non-linear relationships, which may require feature engineering or switching to more complex models. Regularization techniques like Ridge or Lasso can mitigate overfitting and improve generalization.

Trade-offs involve interpretability versus flexibility; Linear Regression is highly interpretable but limited to linear relationships, making it less suitable for complex, non-linear patterns.

## Key Properties

- **Time Complexity:** O(n × d^2) for training, where n is the number of samples and d is the number of features.
- **Auxiliary Space:** O(d), efficient for moderate feature counts.
- **Interpretability:** Highly interpretable due to explicit coefficients for each feature.

## Limitations

Linear Regression is limited to modeling linear relationships and can be sensitive to outliers, multicollinearity, and violations of assumptions such as homoscedasticity and normality. It cannot capture complex, non-linear patterns without feature transformations.

## Example

Predicting house prices based on features such as size, number of bedrooms, and age:
```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```


## Visual

A scatter plot with a set of points and a straight line fitted through them, illustrating the linear relationship between X (feature) and Y (target).

## Relationship to Other Concepts

- **[[Logistic Regression]]** — Both are regression algorithms; Logistic Regression is used for classification, while Linear Regression is for continuous prediction.
- **[[Regularization Techniques in Linear Regression]]** — Regularization methods extend Linear Regression to handle overfitting and multicollinearity.

## Practical Applications

Used in real estate for price prediction, finance for forecasting trends, and economics for modeling relationships between variables. It is also applied in marketing for sales prediction and healthcare for risk assessment.

## Sources

- [[Top 15 Machine Learning Algorithms Every Data Scientist Should Know in 2025]] — primary source for this concept
