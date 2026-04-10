---
title: "K-Means Clustering Algorithm"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "c892018b8120e90b1106c76253490edb44602548be1401649da66b3872a23c74"
sources:
  - raw/2026-04-08-top-15-machine-learning-algorithms-every-data-scientist-shou.md
quality_score: 100
concepts:
  - k-means-clustering-algorithm
related:
  - "[[Principal Component Analysis]]"
  - "[[Top 15 Machine Learning Algorithms Every Data Scientist Should Know in 2025]]"
tier: hot
tags: [unsupervised-learning, clustering, segmentation, pattern-discovery]
---

# K-Means Clustering Algorithm

## Overview

K-Means Clustering is a popular unsupervised learning algorithm used to partition data into k distinct clusters based on feature similarity. It is widely used for pattern discovery, segmentation, and anomaly detection in large datasets.

## How It Works

K-Means Clustering begins by selecting k initial centroids, either randomly or using heuristics. Each data point is assigned to the nearest centroid based on a distance metric (usually Euclidean distance). After assignment, the centroids are recalculated as the mean of all points in each cluster.

This process repeats iteratively: points are reassigned to the nearest centroid, and centroids are updated, until convergence (when assignments no longer change or centroids stabilize). The algorithm aims to minimize the within-cluster sum of squares (WCSS):

\[
WCSS = \sum_{i=1}^{k} \sum_{x \in C_i} ||x - \mu_i||^2
\]

where \(C_i\) is the set of points in cluster i and \(\mu_i\) is the centroid.

K-Means is efficient, with time complexity O(n × k × i), where n is the number of points, k is the number of clusters, and i is the number of iterations. Auxiliary space is O(k × d), suitable for large datasets with moderate feature counts.

Edge cases include choosing the optimal k (number of clusters), handling outliers, and dealing with non-spherical clusters. K-Means assumes clusters are roughly equal in size and density, which may not hold in real-world data.

Trade-offs involve speed versus accuracy; K-Means is fast but may converge to local minima, requiring multiple runs with different initializations. It is sensitive to scaling and feature normalization.

## Key Properties

- **Time Complexity:** O(n × k × i), efficient for large datasets.
- **Auxiliary Space:** O(k × d), scalable for moderate feature counts.
- **Pattern Discovery:** Effective for uncovering inherent groupings in data.

## Limitations

K-Means is sensitive to the initial choice of centroids and may converge to local minima. It assumes spherical, equally sized clusters and struggles with outliers and non-uniform cluster shapes. Choosing the optimal k is non-trivial and may require domain knowledge or methods like the elbow method.

## Example

Segmenting customers in a retail store based on spending behavior:
```python
from sklearn.cluster import KMeans
model = KMeans(n_clusters=3)
model.fit(X)
labels = model.predict(X_new)
```


## Visual

A diagram showing data points grouped into distinct clusters, each with a centroid, illustrating the partitioning process.

## Relationship to Other Concepts

- **[[Principal Component Analysis]]** — PCA can be used to reduce dimensionality before clustering.

## Practical Applications

Used in customer segmentation, image compression, anomaly detection, and social network analysis. It helps businesses identify distinct groups for targeted marketing and resource allocation.

## Sources

- [[Top 15 Machine Learning Algorithms Every Data Scientist Should Know in 2025]] — primary source for this concept
