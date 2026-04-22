---
title: "Linear Regression"
type: concept
created: 2026-04-08
last_verified: 2026-04-17
source_hash: "64f3d7794fd5e8567333444aa2dcf2ae76e118f9bf78cb15eb014a7029e90e95"
sources:
  - raw/2026-04-08-linear-regression-in-machine-learning-geeksforgeeks.md
  - raw/2026-04-08-top-15-machine-learning-algorithms-every-data-scientist-shou.md
quality_score: 81
concepts:
  - linear-regression
related:
  - "[[Linear Regression in Machine Learning - GeeksforGeeks]]"
  - "[[Top 15 Machine Learning Algorithms Every Data Scientist Should Know in 2025]]"
  - "[[Logistic Regression]]"
  - "[[Regularization Techniques in Linear Regression]]"
  - "[[Gradient Descent in Linear Regression]]"
tier: established
tags: [machine-learning, regression, supervised-learning, statistics, python, prediction, interpretability]
---

# Linear Regression

## Overview

Linear regression is a supervised learning algorithm that models the relationship between a dependent variable and one or more independent variables by fitting a straight line to observed data. It is widely used for predicting continuous values, understanding variable relationships, and serves as a baseline for more complex models.

## How It Works

Linear regression operates under the assumption that there is a linear relationship between the input features (independent variables) and the target output (dependent variable). The model fits a straight line, called the best-fit line, to the data points such that the sum of squared differences (residuals) between the actual and predicted values is minimized. This is achieved using the least squares method.

The mathematical formulation for simple linear regression (one independent variable) is:

\[ y = mx + b \]
where:
- \( y \): predicted value (dependent variable)
- \( x \): input (independent variable)
- \( m \): slope (rate of change of y with respect to x)
- \( b \): intercept (value of y when x = 0)

For multiple linear regression (multiple independent variables), the equation generalizes to:

\[ \hat{y} = \theta_0 + \theta_1 x_1 + \theta_2 x_2 + \cdots + \theta_n x_n \]
where \( \theta_0 \) is the intercept and \( \theta_1, \theta_2, ..., \theta_n \) are coefficients for each predictor.

The least squares method minimizes the sum of squared residuals:
\[ \text{Residual} = y_i - \hat{y}_i \]
\[ \sum (y_i - \hat{y}_i)^2 \]
This ensures the line best represents the data, making predictions for new, unseen values possible.

The cost function most commonly used is Mean Squared Error (MSE):
\[ J = \frac{1}{n} \sum_{i=1}^{n} (\hat{y}_i - y_i)^2 \]
To minimize this cost, gradient descent is employed. It starts with random parameter values and iteratively updates them by moving in the direction of the negative gradient of the cost function, ultimately converging to the minimum error.

Linear regression relies on several key assumptions:
- Linearity: Relationship between inputs and output is linear.
- Independence of errors: Prediction errors are independent.
- Homoscedasticity: Errors have constant variance across input values.
- Normality of errors: Errors follow a normal distribution.
- No multicollinearity: Predictors are not highly correlated.
- No autocorrelation: Errors do not show repeating patterns.
- Additivity: Effects of predictors are additive.

The model is interpretable, with coefficients indicating the influence of each variable. It is computationally efficient and forms the basis for many advanced algorithms.

## Key Properties

- **Equation:** Simple: y = mx + b; Multiple: \hat{y} = \theta_0 + \theta_1 x_1 + ... + \theta_n x_n
- **Optimization:** Uses least squares method and gradient descent for parameter estimation.
- **Evaluation Metrics:** MSE, MAE, RMSE, R-squared, Adjusted R-squared.
- **Time Complexity:** Training: O(n) for simple regression, O(n × d^2) for multiple regression via the closed-form normal equation `β̂ = (XᵀX)⁻¹Xᵀy`.
- **Auxiliary Space:** O(d), efficient for moderate feature counts.
- **Interpretability:** Highly interpretable due to explicit coefficients for each feature.

## Limitations

Linear regression assumes a linear relationship between variables, making it unsuitable for modeling complex or non-linear data. It is sensitive to outliers, which can skew the best-fit line. Multicollinearity among predictors can degrade performance. The model can overfit or underfit depending on feature selection and data quality. It requires proper feature engineering and fails when assumptions (linearity, homoscedasticity, independence) are violated.

## Example

Predicting a student's exam score based on hours studied:
```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Generate random data
np.random.seed(42)
X = np.random.rand(50, 1) * 100
Y = 3.5 * X + np.random.randn(50, 1) * 20

# Train model
model = LinearRegression()
model.fit(X, Y)
Y_pred = model.predict(X)

# Visualize
plt.scatter(X, Y, color='blue', label='Data Points')
plt.plot(X, Y_pred, color='red', linewidth=2, label='Regression Line')
plt.title('Linear Regression on Random Dataset')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.show()

print("Slope (Coefficient):", model.coef_[0][0])
print("Intercept:", model.intercept_[0])
```


## Visual

The first diagram illustrates the linear regression line (y = θ₁ + θ₂x) fitted to data points, showing observed values, predicted values, random error (residual), and the slope/intercept. The second image compares linear and non-linear relationships, highlighting linear regression's limitation to linear data. The third image demonstrates homoscedasticity (constant error variance) versus heteroscedasticity (changing error variance), a key assumption for linear regression. The fourth diagram shows the gradient descent process on a cost curve, with steps from initial weight to minimum cost.

## Relationship to Other Concepts

- **Gradient Descent** — Used to optimize linear regression parameters by minimizing the cost function.
- **Lasso Regression** — Regularization technique to prevent overfitting in linear models.
- **Ridge Regression** — Regularization method for handling multicollinearity in linear regression.
- **Elastic Net Regression** — Combines L1 and L2 regularization for linear regression.

## Practical Applications

Linear regression is used in forecasting (e.g., sales, stock prices), trend analysis, predictive modeling in finance, healthcare, real estate, agriculture, and e-commerce. It helps quantify relationships between variables, predict continuous outcomes, and serves as a baseline for more complex models.

## Sources

- [[Linear Regression in Machine Learning - GeeksforGeeks]] — primary deep-dive (gradient descent, assumptions, code example)
- [[Top 15 Machine Learning Algorithms Every Data Scientist Should Know in 2025]] — survey context (closed-form solution, complexity, trade-offs)
