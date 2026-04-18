---
title: "Target Encoding with Shifted Expanding Mean for Time-Series Features"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "a9957a514ef115fac2994880e48b192287f8ae021bb0cc13f878e4b0cd04a43b"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-retrain-in-progress-742b0d94.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-implementation-and-deployment-693c9264.md
quality_score: 100
concepts:
  - target-encoding-shifted-expanding-mean-time-series
related:
  - "[[Copilot Session Checkpoint: Sprint 10 Implementation and Deployment]]"
tier: hot
tags: [target encoding, time-series, feature engineering, leakage prevention]
---

# Target Encoding with Shifted Expanding Mean for Time-Series Features

## Overview

Target encoding replaces categorical variables with a statistic of the target variable, such as the mean target value for each category. For time-series data, a shifted expanding mean is used to avoid data leakage by only using past data to encode current rows. This technique enhances model predictive power by incorporating historical performance trends per team or opponent.

## How It Works

Target encoding transforms categorical features into numerical features by aggregating the target variable conditioned on the category. However, in time-series or sequential data, naive target encoding can cause leakage if future target values are used to encode current rows.

To prevent leakage, a shifted expanding mean is computed:

- For each category (e.g., team or opponent), the target values are ordered by time.
- The expanding mean is calculated cumulatively up to the previous time step, excluding the current row.
- Formally, for a category c at time t, the encoded value is:
  \[ TE_{c,t} = \frac{1}{N_{c,t-1}} \sum_{i=1}^{t-1} y_{c,i} \]
  where \( y_{c,i} \) is the target at time i for category c, and \( N_{c,t-1} \) is the count of observations before time t.

- This is implemented as `x.shift(1).expanding(min_periods=10).mean()` in pandas, ensuring at least 10 prior observations before encoding.

This encoding is applied to features like team points, rebounds, and assists, both for the team and opponent, enriching the feature set with historical performance context.

Trade-offs include the need for sufficient historical data per category to produce stable estimates and the computational cost of maintaining these statistics.

## Key Properties

- **Leak-Free Encoding:** Shifted expanding mean prevents target leakage by excluding current and future targets.
- **Minimum Observations:** Requires a minimum number of prior data points (e.g., 10) for stable encoding.
- **Applicability:** Effective for categorical features with temporal order, such as teams or opponents in sports data.
- **Integration:** Controlled by `USE_TARGET_ENCODING` config variable.

## Limitations

Requires sufficient historical data per category; sparse categories may have unreliable encodings. Computationally more expensive than simple categorical encodings. Not suitable for non-temporal or cross-sectional data without modification.

## Example

Pandas implementation snippet:

```python
# x is a DataFrame with target variable y and categorical column 'team'
team_target_enc = x.groupby('team')['y'].apply(lambda s: s.shift(1).expanding(min_periods=10).mean())
# Add as new feature
x['te_team_pts'] = team_target_enc
```


## Relationship to Other Concepts

- **Feature Engineering in Time-Series Models** — Target encoding is a key feature engineering technique for time-series categorical variables

## Practical Applications

Used in sports analytics to encode team and opponent historical performance, improving predictive accuracy of player stats models. Also applicable in any time-series domain with categorical grouping variables.

## Sources

- [[Copilot Session Checkpoint: Sprint 10 Implementation and Deployment]] — primary source for this concept
- [[Copilot Session Checkpoint: Sprint 10 Retrain In Progress]] — additional source
