---
title: "Decision Tree - GeeksforGeeks"
type: url
captured: 2026-04-08T01:11:37.037344+00:00
source: android-share
url: "https://www.geeksforgeeks.org/machine-learning/decision-tree/"
content_hash: "sha256:26bf6724d45bdc37fabc158684460302000978d00da950ef28a49b32f0d56d06"
tags: []
status: ingested
---

https://www.geeksforgeeks.org/machine-learning/decision-tree/

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T13:30:58+00:00
- source_url: https://www.geeksforgeeks.org/machine-learning/decision-tree/
- resolved_url: https://www.geeksforgeeks.org/machine-learning/decision-tree/
- content_type: text/html; charset=utf-8
- image_urls: ["https://media.geeksforgeeks.org/wp-content/uploads/20250626155729954380/Decision-tree-1.webp", "https://media.geeksforgeeks.org/wp-content/uploads/20250626155813124211/Decision-Tree-2.webp"]

## Fetched Content
A Decision Tree helps us to make decisions by mapping out different choices and their possible outcomes. It’s used in machine learning for tasks like classification and prediction. In this article, we’ll see more about Decision Trees, their types and other core concepts.
A Decision Tree helps us make decisions by showing different options and how they are related. It has a tree-like structure that starts with one main question called the root node which represents the entire dataset. From there, the tree branches out into different possibilities based on features in the data.
- Root Node: Starting point representing the whole dataset.
- Branches: Lines connecting nodes showing the flow from one decision to another.
- Internal Nodes: Points where decisions are made based on data features.
- Leaf Nodes: End points of the tree where the final decision or prediction is made.
Decision Tree
A Decision Tree also helps with decision-making by showing possible outcomes clearly. By looking at the "branches" we can quickly compare options and figure out the best choice.
There are mainly two types of Decision Trees based on the target variable:
- Classification Trees: Used for predicting categorical outcomes like spam or not spam. These trees split the data based on features to classify data into predefined categories.
- Regression Trees: Used for predicting continuous outcomes like predicting house prices. Instead of assigning categories, it provides numerical predictions based on the input features.
## How Decision Trees Work?
1. Start with the Root Node:
It begins with a main question at the root node which is derived from the dataset’s features.
2. Ask Yes/No Questions:
From the root, the tree asks a series of yes/no questions to split the data into subsets based on specific attributes.
3. Branching Based on Answers:
Each question leads to different branches:
- If the answer is yes, the tree follows one path.
- If the answer is no, the tree follows another path.
4. Continue Splitting:
This branching continues through further decisions helps in reducing the data down step-by-step.
5. Reach the Leaf Node:
The process ends when there are no more useful questions to ask leading to the leaf node where the final decision or prediction is made.
Let’s look at a simple example to understand how it works. Imagine we need to decide whether to drink coffee based on the time of day and how tired we feel. The tree first checks the time:
1. In the morning: It asks “Tired?”
- If yes, the tree suggests drinking coffee.
- If no, it says no coffee is needed.
2. In the afternoon: It asks again “Tired?”
- If yes, it suggests drinking coffee.
- If no, no coffee is needed.
Example
## Splitting Criteria in Decision Trees
In a Decision Tree, the process of splitting data at each node is important. The splitting criteria finds the best feature to split the data on. Common splitting criteria include
Gini Impurity and Entropy.
- Gini Impurity : This criterion measures how "impure" a node is. The lower the Gini Impurity the better the feature splits the data into distinct categories.
- Entropy : This measures the amount of uncertainty or disorder in the data. The tree tries to reduce the entropy by splitting the data on features that provide the most information about the target variable.
These criteria help decide which features are useful for making the best split at each decision point in the tree.
### Pruning in Decision Trees
- Pruning is an important technique used to prevent overfitting in Decision Trees. Overfitting occurs when a tree becomes too deep and starts to memorize the training data rather than learning general patterns. This leads to poor performance on new, unseen data.
- This technique reduces the complexity of the tree by removing branches that have little predictive power. It improves model performance by helping the tree generalize better to new data. It also makes the model simpler and faster to deploy.
- It is useful when a Decision Tree is too deep and starts to capture noise in the data.
## Advantages of Decision Trees
- Easy to Understand: Decision Trees are visual which makes it easy to follow the decision-making process.
- Versatility : Can be used for both classification and regression problems.
- No Need for Feature Scaling : Unlike many machine learning models, it don’t require us to scale or normalize our data.
- Handles Non-linear Relationships : It capture complex, non-linear relationships between features and outcomes effectively.
- Interpretability : The tree structure is easy to interpret helps in allowing users to understand the reasoning behind each decision.
- Handles Missing Data : It can handle missing values by using strategies like assigning the most common value or ignoring missing data during splits.
## Disadvantages of Decision Trees
- Overfitting: They can overfit the training data if they are too deep which means they memorize the data instead of learning general patterns. This leads to poor performance on unseen data.
- Instability: It can be unstable which means that small changes in the data may lead to significant differences in the tree structure and predictions.
- Bias towards Features with Many Categories: It can become biased toward features with many distinct values which focuses too much on them and potentially missing other important features which can reduce prediction accuracy.
- Difficulty in Capturing Complex Interactions: Decision Trees may struggle to capture complex interactions between features which helps in making them less effective for certain types of data.
- Computationally Expensive for Large Datasets: For large datasets, building and pruning a Decision Tree can be computationally intensive, especially as the tree depth increases.
## Applications of Decision Trees
Decision Trees are used across various fields due to their simplicity, interpretability and versatility lets see some key applications:
- Loan Approval in Banking: Banks use Decision Trees to assess whether a loan application should be approved. The decision is based on factors like credit score, income, employment status and loan history. This helps predict approval or rejection helps in enabling quick and reliable decisions.
- Medical Diagnosis: In healthcare they assist in diagnosing diseases. For example, they can predict whether a patient has diabetes based on clinical data like glucose levels, BMI and blood pressure. This helps classify patients into diabetic or non-diabetic categories, supporting early diagnosis and treatment.
- Predicting Exam Results in Education: Educational institutions use  to predict whether a student will pass or fail based on factors like attendance, study time and past grades. This helps teachers identify at-risk students and offer targeted support.
- Customer Churn Prediction: Companies use Decision Trees to predict whether a customer will leave or stay based on behavior patterns, purchase history, and interactions. This allows businesses to take proactive steps to retain customers.
- Fraud Detection: In finance, Decision Trees are used to detect fraudulent activities, such as credit card fraud. By analyzing past transaction data and patterns, Decision Trees can identify suspicious activities and flag them for further investigation.
A decision tree can also be used to help build automated predictive models which have applications in machine learning, data mining and statistics. By mastering Decision Trees, we can gain a deeper understanding of data and make more informed decisions across different fields.
If you want to learn that refer to related article:
- Python | Decision tree implementation
- How To Build Decision Tree in MATLAB?
<!-- fetched-content:end -->
