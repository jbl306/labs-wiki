---
title: "Implementing the AdaBoost Algorithm From Scratch - GeeksforGeeks"
type: url
captured: 2026-04-08T01:17:58.747043+00:00
source: android-share
url: "https://www.geeksforgeeks.org/machine-learning/implementing-the-adaboost-algorithm-from-scratch/"
content_hash: "sha256:55e4ecb7d6f63b79a1e3f293697ca403ab33b1d1705201f6fa1817f47abbf2f0"
tags: []
status: ingested
---

https://www.geeksforgeeks.org/machine-learning/implementing-the-adaboost-algorithm-from-scratch/

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T13:32:07+00:00
- source_url: https://www.geeksforgeeks.org/machine-learning/implementing-the-adaboost-algorithm-from-scratch/
- resolved_url: https://www.geeksforgeeks.org/machine-learning/implementing-the-adaboost-algorithm-from-scratch/
- content_type: text/html; charset=utf-8
- image_urls: ["https://media.geeksforgeeks.org/wp-content/uploads/20250512093455986788/Evaluation_metrics.png"]

## Fetched Content
AdaBoost
means Adaptive Boosting which is a
ensemble learning technique
that combines multiple weak classifiers to create a strong classifier. It works by sequentially adding classifiers to correct the errors made by previous models giving more weight to the misclassified data points. Lets implement AdaBoost algorithm from scratch.
## 1. Import Libraries
Let's begin with importing important libraries like
numpy
and
scikit learn
which will be required to do classification task.
Python
````
import
numpy
as
np
from
sklearn.tree
import
DecisionTreeClassifier
from
sklearn.datasets
import
load_iris
from
sklearn.datasets
import
make_classification
from
sklearn.model_selection
import
train_test_split
from
sklearn.metrics
import
accuracy_score
,
confusion_matrix
,
precision_score
,
recall_score
,
f1_score
,
roc_auc_score
````
## 2. Defining the AdaBoost Class
In this step we define a custom class called AdaBoost that will implement the AdaBoost algorithm from scratch. This class will handle the entire training process and predictions.
The AdaBoost class is where we define the entire AdaBoost algorithm which consists of:
- Initializing model parameters like number of estimators, weights and models.
- Fitting the model to the training data.
- Making predictions using the trained model.
Python
````
class
AdaBoost
:
def
__init__
(
self
,
n_estimators
=
50
):
self
.
n_estimators
=
n_estimators
self
.
alphas
=
[]
self
.
models
=
[]
````
The constructor
(__init__)
initializes the number of weak models
(n_estimators)
to a list to store the alphas
(self.alphas)
and a list to store the weak classifiers
(self.models)
## 3. Training the AdaBoost Model
In the fit() method we:
- Sample Weights Initialization : w= np.ones(n_samples) / n_samples initializes all sample weights equally.
- Training the Weak Classifier : A DecisionTreeClassifier with max_depth =1 is trained using the current sample weights.
- Error Calculation : err = np.sum (w* ( predictions != y)) / np.sum(w) computes the weighted error of the classifier.
- Alpha Calculation : alpha = 0.5*np.log ((1-err) / (err+1e-10) ) calculates the classifier's weight (alpha).
- Updating Weights : Misclassified samples weights are increased using w *= np.exp(-alpha *y *predictions) and normalized with w /= np.sum(w).
Python
````
def
fit
(
self
,
X
,
y
):
n_samples
,
n_features
=
X
.
shape
w
=
np
.
ones
(
n_samples
)
/
n_samples
for
_
in
range
(
self
.
n_estimators
):
model
=
DecisionTreeClassifier
(
max_depth
=
1
)
model
.
fit
(
X
,
y
,
sample_weight
=
w
)
predictions
=
model
.
predict
(
X
)
err
=
np
.
sum
(
w
*
(
predictions
!=
y
))
/
np
.
sum
(
w
)
alpha
=
0.5
*
np
.
log
((
1
-
err
)
/
(
err
+
1e-10
))
self
.
models
.
append
(
model
)
self
.
alphas
.
append
(
alpha
)
w
*=
np
.
exp
(
-
alpha
*
y
*
predictions
)
w
/=
np
.
sum
(
w
)
````
## 4. Defining Predict Method
In the predict() method  we combine the predictions of all weak classifiers using their respective alpha values to make the final prediction.
- strong_preds = np.zeroes(X.shape[0]) initializes an array of zeros to store the weighted sum of predictions from all weak classifiers.
- for model, alpha in zip(self.models, self.alphas) loops through each trained model and its corresponding alpha value.
- strong_preds += alpha * predictions adds the weighted prediction of each weak model to strong_preds
- np.sign(strong_preds) takes the sign of the sum to classify samples as 1 (positive class) or -1 (negative class).
Python
````
def
predict
(
self
,
X
):
strong_preds
=
np
.
zeros
(
X
.
shape
[
0
])
for
model
,
alpha
in
zip
(
self
.
models
,
self
.
alphas
):
predictions
=
model
.
predict
(
X
)
strong_preds
+=
alpha
*
predictions
return
np
.
sign
(
strong_preds
)
.
astype
(
int
)
````
## 5. Example Usage
- We are generating a synthetic dataset with 1000 samples and 20 features.
- Then, we split the data into training and testing sets.
- We initialize and train an AdaBoost classifier with 50 estimators.
- After training, we predict on the test set and evaluate the model.
Python
````
if
__name__
==
"__main__"
:
X
,
y
=
make_classification
(
n_samples
=
1000
,
n_features
=
20
,
n_classes
=
2
,
random_state
=
42
)
X_train
,
X_test
,
y_train
,
y_test
=
train_test_split
(
X
,
y
,
test_size
=
0.3
,
random_state
=
42
)
adaboost
=
AdaBoost
(
n_estimators
=
50
)
adaboost
.
fit
(
X_train
,
y_train
)
predictions
=
adaboost
.
predict
(
X_test
)
accuracy
=
accuracy_score
(
y_test
,
predictions
)
precision
=
precision_score
(
y_test
,
predictions
)
recall
=
recall_score
(
y_test
,
predictions
)
f1
=
f1_score
(
y_test
,
predictions
)
try
:
roc_auc
=
roc_auc_score
(
y_test
,
predictions
)
except
ValueError
:
roc_auc
=
'Undefined (requires probability scores)'
print
(
f
"Accuracy:
{
accuracy
*
100
}
%"
)
print
(
f
"Precision:
{
precision
}
"
)
print
(
f
"Recall:
{
recall
}
"
)
print
(
f
"F1 Score:
{
f1
}
"
)
print
(
f
"ROC-AUC:
{
roc_auc
}
"
)
````
Output:
Model performance
The model performs well with:
- Accuracy of 84% meaning it makes correct predictions most of the time.
- It has good balance between precision (0.836) which makes accurate positive predictions.
- Recall (0.858) which means it catch most of the actual positive cases.
- The F1 score (0.847) combines these two measures
- ROC-AUC (0.839) show the model does a good job of telling the difference between the two classes.
Overall these metrics indicate good performance.
<!-- fetched-content:end -->
