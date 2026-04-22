---
title: "K-Nearest Neighbor Algorithm"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "27cec2b0cffbc21273436407fb7f0d8419b0d567f35c1607c8074be77d4bcd74"
sources:
  - raw/2026-04-08-k-nearest-neighborknn-algorithm-geeksforgeeks.md
quality_score: 76
concepts:
  - k-nearest-neighbor-algorithm
related:
  - "[[Decision Tree Algorithm]]"
  - "[[K-Nearest Neighbor(KNN) Algorithm - GeeksforGeeks]]"
tier: hot
tags: [machine-learning, classification, regression, distance-metrics, non-parametric]
---

# K-Nearest Neighbor Algorithm

## Overview

The K-Nearest Neighbor (KNN) algorithm is a fundamental machine learning technique used for both classification and regression. It operates by identifying the 'k' closest data points to a given input and making predictions based on their labels or values. KNN is valued for its simplicity, versatility, and non-parametric nature, making it suitable for a wide range of tasks.

## How It Works

KNN is an instance-based learning algorithm, meaning it does not build an explicit model during training. Instead, it stores the entire dataset and makes predictions only when queried. The algorithm works by measuring the similarity between a new data point and all points in the training set, typically using a distance metric such as Euclidean, Manhattan, or Minkowski distance.

The process begins with selecting the optimal value of 'k', which determines how many neighbors are considered for prediction. A small 'k' can make the model sensitive to noise and outliers, while a large 'k' may oversimplify the decision boundary, leading to underfitting. Statistical methods like k-fold cross-validation and the elbow method are commonly used to select 'k'. Cross-validation involves partitioning the dataset into 'k' subsets, training on some and testing on others, and choosing the 'k' that yields the highest average accuracy. The elbow method plots error rates against different 'k' values, and the optimal 'k' is where the curve bends sharply.

Once 'k' is chosen, the algorithm computes the distance between the target (test) point and all training points. The most widely used metric is Euclidean distance, defined as:

$$
d(x, X_i) = \sqrt{\sum_{j=1}^{n} (x_j - X_{ij})^2}
$$

Other metrics include Manhattan distance:

$$
d(x, y) = \sum_{i=1}^{n} |x_i - y_i|
$$

and Minkowski distance:

$$
d(x, y) = \left( \sum_{i=1}^{n} |x_i - y_i|^p \right)^{1/p}
$$

where $p=1$ gives Manhattan and $p=2$ gives Euclidean distance.

After computing distances, the algorithm sorts the training points by proximity and selects the 'k' nearest neighbors. For classification, it uses majority voting—assigning the label that appears most frequently among the neighbors. For regression, it averages the values of the neighbors. This approach leverages local patterns and is robust to non-linear boundaries.

KNN is a lazy learner: it does not generalize from the data until prediction time, which can make it computationally expensive for large datasets. It is also non-parametric, meaning it makes no assumptions about the underlying data distribution, allowing it to adapt to complex patterns. However, it struggles with high-dimensional data due to the curse of dimensionality, where distance metrics become less meaningful.

The algorithm can be implemented from scratch in Python, as shown in the article:

```python
import numpy as np
from collections import Counter

def euclidean_distance(point1, point2):
    return np.sqrt(np.sum((np.array(point1) - np.array(point2)) ** 2))

def knn_predict(training_data, training_labels, test_point, k):
    distances = []
    for i in range(len(training_data)):
        dist = euclidean_distance(test_point, training_data[i])
        distances.append((dist, training_labels[i]))
    distances.sort(key=lambda x: x[0])
    k_nearest_labels = [label for _, label in distances[:k]]
    return Counter(k_nearest_labels).most_common(1)[0][0]
```

This code calculates distances, finds the nearest neighbors, and predicts the label using majority voting. The algorithm is easy to understand and implement, but its simplicity comes with trade-offs in scalability and performance.

## Key Properties

- **Non-Parametric:** KNN does not assume any specific form for the data distribution, allowing it to model complex relationships.
- **Instance-Based (Lazy Learning):** The algorithm stores the entire dataset and only performs computation at prediction time, leading to high prediction-time complexity.
- **Distance Metric Flexibility:** Supports multiple distance metrics (Euclidean, Manhattan, Minkowski), which can be chosen based on the problem context.
- **Time Complexity:** Prediction requires O(n) distance computations per query, where n is the number of training samples.

## Limitations

KNN is computationally expensive for large datasets, as it must compute distances to all training points for each prediction. It suffers from the curse of dimensionality, where accuracy drops as the number of features increases. The algorithm can overfit noisy data with small 'k' or underfit with large 'k'. It also requires careful feature scaling, as distance metrics are sensitive to feature magnitude. KNN does not handle missing data or categorical variables natively.

## Example

Suppose you have a dataset of fruits with features 'shape' and 'size', labeled as 'apple' or 'banana'. To classify a new fruit, KNN with k=3 computes the distance to all known fruits, selects the three closest, and assigns the label that appears most frequently among them. If two are apples and one is a banana, the new fruit is classified as an apple.

Python example:
```python
training_data = [[1, 2], [2, 3], [3, 4], [6, 7], [7, 8]]
training_labels = ['A', 'A', 'A', 'B', 'B']
test_point = [4, 5]
k = 3
prediction = knn_predict(training_data, training_labels, test_point, k)
print(prediction)  # Output: 'A'
```


## Visual

The article includes a diagram showing two categories (green and red points) and a new data point. The new point checks its closest neighbors (circled points); since the majority are red, it is classified as Category 2. This visually demonstrates majority voting in KNN.

## Relationship to Other Concepts

- **[[Decision Tree Algorithm]]** — Both are used for classification and regression, but KNN is instance-based while Decision Tree is model-based.
- **Cross Validation in Machine Learning** — Cross-validation is used to select the optimal value of 'k' in KNN.
- **Feature Engineering** — Feature scaling and selection are critical for KNN's performance due to its reliance on distance metrics.

## Practical Applications

KNN is used in recommendation systems to suggest items based on user similarity, spam detection by comparing emails to known examples, customer segmentation by grouping similar shopping behaviors, and speech recognition by matching spoken words to known patterns. It is also applied in medical diagnosis, image classification, and anomaly detection.

## Sources

- [[K-Nearest Neighbor(KNN) Algorithm - GeeksforGeeks]] — primary source for this concept
