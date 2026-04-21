---
title: "Apriori Algorithm - GeeksforGeeks"
type: url
captured: 2026-04-08T01:13:33.907052+00:00
source: android-share
url: "https://www.geeksforgeeks.org/machine-learning/apriori-algorithm/"
content_hash: "sha256:d0bff13a11845d104b4329d38757e6f1ce77032d2b2f6ac75b3ec54f9794e769"
tags: []
status: ingested
---

https://www.geeksforgeeks.org/machine-learning/apriori-algorithm/

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T13:29:59+00:00
- source_url: https://www.geeksforgeeks.org/machine-learning/apriori-algorithm/
- resolved_url: https://www.geeksforgeeks.org/machine-learning/apriori-algorithm/
- content_type: text/html; charset=utf-8
- image_urls: ["https://media.geeksforgeeks.org/wp-content/uploads/20260220120811552453/transaction_id.webp", "https://media.geeksforgeeks.org/wp-content/uploads/20260220120818315592/item.webp", "https://media.geeksforgeeks.org/wp-content/uploads/20260220120811407443/item_pair.webp", "https://media.geeksforgeeks.org/wp-content/uploads/20260220120811478424/item_triplet.webp"]

## Fetched Content
Apriori Algorithm is a basic method used in data analysis to find groups of items that often appear together in large sets of data. It helps to discover useful patterns or rules about how items are related which is particularly valuable in market basket analysis.
Like in a grocery store if many customers buy bread and butter together, the store can use this information to place these items closer or create special offers. This helps the store sell more and make customers happy.
## How the Apriori Algorithm Works?
The Apriori Algorithm operates through a systematic process that involves several key steps:
### 1. Identifying Frequent Item-Sets
- The Apriori algorithm starts by looking through all the data to count how many times each single item appears. These single items are called 1-Item-Sets.
- Next it uses a rule called minimum support this is a number that tells us how often an item or group of items needs to appear to be important. If an item appears often enough meaning its count is above this minimum support it is called a frequent Item-Set.
### 2. Creating Possible Item Group
- After finding the single items that appear often enough (frequent 1-item groups) the algorithm combines them to create pairs of items (2-item groups). Then it checks which pairs are frequent by seeing if they appear enough times in the data.
- This process keeps going step by step making groups of 3 items, then 4 items and so on. The algorithm stops when it can’t find any bigger groups that happen often enough.
### 3. Removing Infrequent Item Groups
- The Apriori algorithm uses a helpful rule to save time. This rule says: if a group of items does not appear often enough then any larger group that incl2 udes these items will also not appear often.
- Because of this, the algorithm does not check those larger groups. This way it avoids wasting time looking at groups that won’t be important make the whole process faster.
### 4. Generating Association Rules
- The algorithm makes rules to show how items are related.
- It checks these rules using support, confidence and lift to find the strongest ones.
## Key Metrics of Apriori Algorithm
- Support : This metric measures how frequently an item appears in the dataset relative to the total number of transactions. A higher support indicates a more significant presence of the Item-Set in the dataset. Support tells us how often a particular item or combination of items appears in all the transactions like Bread is bought in 20% of all transactions.
- Confidence : Confidence assesses the likelihood that an item Y is purchased when item X is purchased. It provides insight into the strength of the association between two items. Confidence tells us how often items go together i.e If bread is bought, butter is bought 75% of the time.
- Lift : Lift evaluates how much more likely two items are to be purchased together compared to being purchased independently. A lift greater than 1 suggests a strong positive association. Lift shows how strong the connection is between items. Like Bread and butter are much more likely to be bought together than by chance.
## Example
Lets understand the concept of apriori Algorithm with the help of an example. Consider the following dataset and we will find frequent Item-Sets and generate association rules for them:
Transactions of a Grocery Shop
### Step 1 : Setting the parameters
- Minimum Support Threshold: 50% (item must appear in at least 3/5 transactions). This threshold is formulated from this formula:
\text{Support}(A) = \frac{\text{Number of transactions containing itemset } A}{\text{Total number of transactions}}
- Minimum Confidence Threshold: 70% ( You can change the value of parameters as per the use case and problem statement ). This threshold is formulated from this formula:
\text{Confidence}(X \rightarrow Y) = \frac{\text{Support}(X \cup Y)}{\text{Support}(X)}
### Step 2: Find Frequent 1-Item-Sets
Lets count how many transactions include each item in the dataset (calculating the frequency of each item).
Frequent 1-Itemsets
All items have support% ≥ 50%, so they qualify as frequent 1-Item-Sets. if any item has support% < 50%, It will be omitted out from the frequent 1- Item-Sets.
### Step 3: Generate Candidate 2-Item-Sets
Combine the frequent 1-Item-Sets into pairs and calculate their support.
For this use case we will get 3 item pairs ( bread,butter) , (bread,ilk) and (butter,milk) and will calculate the support similar to step 2
Candidate 2-Itemsets
Frequent 2-Item-Sets:
{Bread, Milk} meet the 50% threshold but {Butter, Milk} and {Bread ,Butter} doesn't meet the threshold, so will be committed out.
### Step 4: Generate Candidate 3-Item-Sets
Combine the frequent 2-Item-Sets into groups of 3 and calculate their support. For the triplet we have only got one case i.e {bread,butter,milk} and we will calculate the support.
Candidate 3-Itemsets
Since this does not meet the 50% threshold, there are no frequent 3-Item-Sets.
### Step 5: Generate Association Rules
Now we generate rules from the frequent Item-Sets and calculate confidence.
#### Rule 1: If Bread -> Butter (if customer buys bread, the customer will buy butter also)
- Support of {Bread, Butter} = 2.
- Support of {Bread} = 4.
- Confidence = 2/4 = 50% (Failed threshold).
#### Rule 2: If Butter -> Bread (if customer buys butter, the customer will buy bread also)
- Support of {Bread, Butter} = 2.
- Support of {Butter} = 3.
- Confidence = 2/3 = 66.67% (Fails threshold).
#### Rule 3: If Bread -> Milk (if customer buys bread, the customer will buy milk also)
- Support of {Bread, Milk} = 3.
- Support of {Bread} = 4.
- Confidence = 3/4 = 75% (Passes threshold).
The Apriori Algorithm, as demonstrated in the bread-butter example, is widely used in modern startups like Zomato, Swiggy and other food delivery platforms. These companies use it to perform
market basket analysis
which helps them identify customer behaviour patterns and optimise recommendations.
## Applications of Apriori Algorithm
Below are some applications of Apriori algorithm used in today's companies and startups
- E-commerce: Used to recommend products that are often bought together like laptop + laptop bag, increasing sales.
- Food Delivery Services: Identifies popular combos such as burger + fries to offer combo deals to customers.
- Streaming Services: Recommends related movies or shows based on what users often watch together like action + superhero movies.
- Financial Services: Analyzes spending habits to suggest personalised offers such as credit card deals based on frequent purchases.
- Travel & Hospitality: Creates travel packages like flight + hotel by finding commonly purchased services together.
- Health & Fitness: Suggests workout plans or supplements based on users past activities like protein shakes + workouts.
### Related Articles
- Apriori algorithm in Python
<!-- fetched-content:end -->
