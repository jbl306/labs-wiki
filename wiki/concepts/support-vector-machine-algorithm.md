---
title: "Support Vector Machine Algorithm"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "5380388bec62eebb61d0e40915eb60f05cf82459ab6250e8951020d927eefc0d"
sources:
  - raw/2026-04-08-support-vector-machine-svm-algorithm-geeksforgeeks.md
quality_score: 100
concepts:
  - support-vector-machine-algorithm
related:
  - "[[Support Vector Machine (SVM) Algorithm - GeeksforGeeks]]"
tier: hot
tags: [machine-learning, classification, regression, kernel-methods, optimization]
---

# Support Vector Machine Algorithm

## Overview

Support Vector Machine (SVM) is a supervised learning algorithm used for classification and regression tasks. It seeks to find the optimal hyperplane that separates classes in the feature space, maximizing the margin between them. SVM is renowned for its robustness to outliers and its ability to handle both linear and non-linear classification problems using kernel functions.

## How It Works

The core principle of SVM is to identify a hyperplane in the feature space that best separates data points belonging to different classes. For binary classification, the hyperplane is defined by the equation \( w^T x + b = 0 \), where \( w \) is the normal vector and \( b \) is the bias. The margin is the distance between the hyperplane and the nearest data points from each class, known as support vectors. SVM maximizes this margin, which empirically leads to better generalization on unseen data.

For linearly separable data, SVM solves the following optimization problem:

\[
\underset{w,b}{\text{minimize}} \frac{1}{2} \| w \|^2
\]
subject to:
\[
y_i (w^T x_i + b) \geq 1 \quad \forall i
\]
where \( y_i \) is the class label (+1 or -1), and \( x_i \) is the feature vector.

When data is not perfectly separable, SVM introduces slack variables \( \zeta_i \) to allow some misclassification (soft margin), modifying the optimization problem:

\[
\underset{w, b}{\text{minimize }} \frac{1}{2} \|w\|^2 + C \sum_{i=1}^{m} \zeta_i
\]
subject to:
\[
y_i (w^T x_i + b) \geq 1 - \zeta_i \quad \text{and} \quad \zeta_i \geq 0
\]
\( C \) is a regularization parameter controlling the trade-off between margin maximization and penalty for misclassification.

The loss function used is hinge loss, which penalizes misclassified points and margin violations:
- If a point is correctly classified and outside the margin: loss = 0
- If a point is misclassified or within the margin: loss increases proportionally to the violation

For non-linearly separable data, SVM employs kernel functions to map data into higher-dimensional spaces where a linear separation is possible. Common kernels include linear, polynomial, and radial basis function (RBF). The kernel trick allows SVM to compute the similarity between data points in this transformed space without explicitly calculating their coordinates.

The dual problem formulation leverages Lagrange multipliers \( \alpha_i \) and kernel functions \( K(x_i, x_j) \) to efficiently solve the SVM optimization, especially for large datasets and non-linear classification:

\[
\max_{\alpha} \; \frac{1}{2} \sum_{i=1}^{m} \sum_{j=1}^{m} \alpha_i \alpha_j t_i t_j K(x_i, x_j)- \sum_{i=1}^{m} \alpha_i
\]

The decision boundary is then determined by:
\[
w = \sum_{i=1}^{m} \alpha_i t_i K(x_i, x) + b
\]

Support vectors are those data points where \( \alpha_i > 0 \), and the bias \( b \) is computed using these vectors.

SVM can be used for both linear and non-linear classification, as well as regression tasks. Its mathematical rigor, margin maximization, and kernel trick make it a versatile and powerful algorithm in machine learning.

## Key Properties

- **Margin Maximization:** SVM maximizes the margin between classes, improving generalization.
- **Kernel Trick:** Efficiently handles non-linear data by mapping it to higher-dimensional spaces.
- **Support Vectors:** Only the closest data points to the hyperplane (support vectors) influence the decision boundary.
- **Dual Problem Formulation:** Enables efficient computation and kernel application, especially for large and complex datasets.
- **Time Complexity:** Training can be slow for large datasets; complexity depends on the number of support vectors and kernel used.

## Limitations

SVMs can be slow to train on large datasets due to quadratic optimization. They require careful parameter tuning (kernel selection, C value) and are sensitive to feature scaling. SVMs may struggle with noisy data and overlapping classes, and their decision boundaries in high-dimensional spaces are less interpretable than simpler models. Additionally, multiclass classification requires extensions like one-vs-rest or one-vs-one strategies.

## Example

```python
from sklearn.datasets import load_breast_cancer
from sklearn.svm import SVC
cancer = load_breast_cancer()
X = cancer.data[:, :2]
y = cancer.target
svm = SVC(kernel="linear", C=1)
svm.fit(X, y)
```
This code trains a linear SVM to classify breast cancer as benign or malignant based on two features.

## Visual

Several diagrams illustrate SVM concepts:
- One chart shows three candidate hyperplanes (L1, L2, L3) separating blue and red points, with L2 maximizing the margin.
- Another chart shows linearly separable data with a single optimal hyperplane.
- A 1D diagram demonstrates mapping data to higher dimensions for kernel-based separation.

## Relationship to Other Concepts

- **Kernel** — Kernel functions are used in SVM to enable non-linear classification.
- **Hinge Loss** — Hinge loss is the penalty function used in SVM optimization.
- **Dual Problem** — The dual formulation is central to SVM's efficient computation and kernel trick.

## Practical Applications

SVM is widely used in image classification, gene expression analysis, text categorization, spam detection, and medical diagnosis. Its robustness to outliers and ability to handle high-dimensional data make it suitable for domains where feature spaces are large and complex. SVM is also applied in financial modeling, handwriting recognition, and bioinformatics.

## Sources

- [[Support Vector Machine (SVM) Algorithm - GeeksforGeeks]] — primary source for this concept
