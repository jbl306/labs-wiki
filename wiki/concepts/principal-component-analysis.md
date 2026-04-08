---
title: "Principal Component Analysis"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "50ae0a25a9509f94ffb1846a82d1f7e75e047e8b67587ac7f4cf9ff980b5a63b"
sources:
  - raw/2026-04-08-principal-component-analysis-pca-geeksforgeeks.md
quality_score: 0
concepts:
  - principal-component-analysis
related:
  - "[[Linear Regression]]"
  - "[[Logistic Regression]]"
  - "[[Standardization]]"
  - "[[Principal Component Analysis (PCA) - GeeksforGeeks]]"
tier: hot
tags: [dimensionality-reduction, data-analysis, machine-learning, linear-algebra, feature-extraction]
---

# Principal Component Analysis

## Overview

Principal Component Analysis (PCA) is a statistical technique used to reduce the dimensionality of datasets while preserving as much variance as possible. It transforms correlated features into a smaller set of uncorrelated principal components, making data easier to analyze, visualize, and model. PCA is widely used in machine learning, data analysis, and pattern recognition for preprocessing and feature extraction.

## How It Works

PCA operates by leveraging linear algebra to identify new axes (principal components) along which the data exhibits the greatest variance. The process begins with standardizing the dataset, ensuring each feature has a mean of 0 and a standard deviation of 1. This is crucial because features often have different scales, and PCA is sensitive to these differences.

The next step is to compute the covariance matrix, which quantifies how pairs of features vary together. The covariance between two features x₁ and x₂ is calculated as:

$$
\text{cov}(x_1, x_2) = \frac{\sum_{i=1}^{n}(x_{1i} - \bar{x}_1)(x_{2i} - \bar{x}_2)}{n-1}
$$

where \( \bar{x}_1 \) and \( \bar{x}_2 \) are the means of features x₁ and x₂, and n is the number of data points. The resulting covariance matrix is square, with diagonal elements representing variances and off-diagonal elements representing covariances.

PCA then finds the eigenvectors and eigenvalues of this covariance matrix. Eigenvectors indicate the directions (principal components) along which the data varies most, while eigenvalues quantify the magnitude of this variance. The principal components are ranked by their eigenvalues, and the top k components are selected to capture the majority of the variance—often a threshold like 95% is used.

The original data is projected onto these top principal components, effectively reducing the number of features while retaining the most important information. For example, a 2D dataset with features 'Radius' and 'Area' can be transformed into a 1D dataset along the direction of maximum variance (PC₁), as illustrated in the source's diagram.

In practical terms, PCA can be implemented in Python using libraries like scikit-learn. The workflow involves standardizing the data, applying PCA to extract principal components, splitting the data for training/testing, and using the reduced dataset for modeling (e.g., logistic regression). Visualization before and after PCA shows improved class separation and structure in the reduced space.

PCA is particularly effective for handling multicollinearity, compressing data, reducing noise, and detecting outliers. However, it assumes linear relationships, can be computationally intensive for large datasets, and may lead to information loss if too few components are retained. The new components are linear combinations of original features, which can make interpretation challenging.

## Key Properties

- **Dimensionality Reduction:** Transforms high-dimensional data into a lower-dimensional space by selecting principal components with highest variance.
- **Uncorrelated Features:** Principal components are uncorrelated, addressing multicollinearity issues in the original dataset.
- **Variance Preservation:** Retains the directions of maximum variance, prioritizing components that capture the most information.
- **Linear Transformation:** Relies on linear algebra (eigenvectors/eigenvalues) and assumes linear relationships between features.
- **Computational Complexity:** Can be resource-intensive for large datasets due to matrix operations and eigen decomposition.

## Limitations

PCA's effectiveness depends on proper data scaling; unstandardized features can skew results. It assumes linear relationships and may not capture non-linear patterns. Interpretation of principal components can be difficult since they are combinations of original features. Reducing too many dimensions risks losing important information. PCA can be slow on large datasets and may overfit if too many components are used or the dataset is small.

## Example

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Sample dataset
data = {
    'Height': [170, 165, 180, 175, 160, 172, 168, 177, 162, 158],
    'Weight': [65, 59, 75, 68, 55, 70, 62, 74, 58, 54],
    'Age': [30, 25, 35, 28, 22, 32, 27, 33, 24, 21],
    'Gender': [1, 0, 1, 1, 0, 1, 0, 1, 0, 0]
}
df = pd.DataFrame(data)
X = df.drop('Gender', axis=1)
y = df['Gender']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.3, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Female', 'Male'], yticklabels=['Female', 'Male'])
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()
```

## Visual

Several images illustrate PCA: (1) A diagram showing how PCA reduces multiple colors to dominant colors, representing dimensionality reduction; (2) A 2D plot with axes 'Radius' and 'Area', showing how principal components (PC₁ and PC₂) are rotated axes capturing variance, and how projecting onto PC₁ transforms 2D data to 1D; (3) A confusion matrix heatmap visualizing classification results after PCA; (4) Side-by-side scatter plots showing data before and after PCA, with improved separation in the reduced space.

## Relationship to Other Concepts

- **[[Linear Regression]]** — Both rely on linear algebra and are sensitive to feature scaling.
- **[[Logistic Regression]]** — PCA is often used as a preprocessing step before logistic regression for dimensionality reduction.
- **[[Standardization]]** — Standardization is a prerequisite for PCA to ensure fair comparison of features.

## Practical Applications

PCA is used in exploratory data analysis to visualize high-dimensional data, in preprocessing pipelines for machine learning models to reduce feature space, in image compression to identify dominant patterns, in genomics for analyzing gene expression data, and in finance for risk management by identifying principal factors affecting asset prices. It is also valuable for noise reduction and outlier detection in various domains.

## Sources

- [[Principal Component Analysis (PCA) - GeeksforGeeks]] — primary source for this concept
