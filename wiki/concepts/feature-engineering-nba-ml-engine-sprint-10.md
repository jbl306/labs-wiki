---
title: "Feature Engineering for NBA ML Engine Sprint 10"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "016d553979837ab306dec9cdf9e2309752249db326f2d6c75448f89eba8e6a11"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-implementation-and-deployment-693c9264.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-complete-and-deployed-cb380016.md
quality_score: 100
concepts:
  - feature-engineering-nba-ml-engine-sprint-10
related:
  - "[[Copilot Session Checkpoint: Sprint 10 Complete and Deployed]]"
tier: hot
tags: [feature-engineering, nba-ml, data-preprocessing]
---

# Feature Engineering for NBA ML Engine Sprint 10

## Overview

Feature engineering is a critical step in improving model performance by creating informative input variables. In Sprint 10 of the NBA ML Engine project, six new feature groups were added, totaling approximately 20 new features, to enhance predictive accuracy across multiple basketball statistics.

## How It Works

The feature engineering process involved adding six distinct feature groups integrated into the existing pipeline in `src/features/builder.py`. These groups include:

1. **Back-to-Back (B2B) Fatigue Features:** Capture player fatigue effects by quantifying rest days and game frequency.
2. **Minutes Trend Features:** Track recent playing time trends to reflect player usage changes.
3. **Injury Return Features:** Indicate players returning from injury, which can affect performance.
4. **Season Phase Features:** Encode different phases of the NBA season (e.g., early, mid, late) to capture temporal effects.
5. **Matchup Features:** Represent specific opponent-related statistics and contextual matchup data.
6. **Target Encoding Features:** Use shifted expanding mean statistics per team/opponent for points, rebounds, and assists to provide leak-free encoding.

A key technical challenge was handling NaN values produced by `pd.cut()` in the rest category feature, which originally caused type conversion errors. This was resolved by converting to float, filling NaNs with a default category (3), then converting back to int.

The feature matrix after Sprint 10 contained 95,271 rows and 417 columns, with 383 feature columns. This extensive feature set supports robust model training and evaluation.

The feature engineering pipeline is modular and extensible, allowing seamless integration of new features and fixes. It is critical for capturing nuanced player and game dynamics that improve model predictive power.

## Key Properties

- **Feature Groups Added:** Six new groups: B2B fatigue, minutes trend, injury return, season phase, matchup, target encoding.
- **Feature Matrix Size:** 95,271 rows × 417 columns (383 feature columns).
- **NaN Handling:** Fixed NaN in categorical binning by converting to float, filling NaNs with 3, then converting to int.

## Limitations

The feature engineering relies on historical and contextual data that may have missing or noisy entries. Target encoding must be carefully implemented to avoid data leakage, which is handled here by shifted expanding means. Some features like injury return may have limited data availability or delayed updates. The large feature set can increase training time and risk overfitting if not properly regularized.

## Example

Example NaN fix in rest category feature:
```python
# Original failing code
bins = pd.cut(series, bins).astype(int)  # Fails on NaN

# Fixed code
bins = pd.cut(series, bins).astype(float).fillna(3).astype(int)
```

## Relationship to Other Concepts

- **Warmstarting Hyperparameter Tuning** — Feature engineering improvements complement warmstarting to accelerate model optimization.
- **Quantile Crossing Fix in Tree Models** — Feature quality impacts quantile regression predictions requiring crossing fixes.

## Practical Applications

Used to improve predictive accuracy of NBA player statistics models by capturing fatigue, injury, temporal, and matchup effects. Enables more nuanced and context-aware predictions for sports analytics platforms.

## Sources

- [[Copilot Session Checkpoint: Sprint 10 Complete and Deployed]] — primary source for this concept
- [[Copilot Session Checkpoint: Sprint 10 Implementation and Deployment]] — additional source
