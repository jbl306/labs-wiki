---
title: "Feature Engineering for NBA Player Performance Modeling"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "1a8605793607a924fae33927ca1c4abc23aa36d89dbda589fb5634f468d8ae67"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-retrain-in-progress-742b0d94.md
quality_score: 53
concepts:
  - feature-engineering-nba-player-performance-modeling
related:
  - "[[Copilot Session Checkpoint: Sprint 10 Retrain In Progress]]"
tier: hot
tags: [feature engineering, NBA, machine learning, sports analytics]
---

# Feature Engineering for NBA Player Performance Modeling

## Overview

Feature engineering is critical in improving the predictive accuracy of machine learning models for NBA player statistics. This sprint introduced several new feature groups capturing player fatigue, minutes trends, injury return status, season phase, matchup history, and target encoding to enhance model inputs.

## How It Works

The feature engineering process added six new feature functions integrated into the core build_features pipeline:

1. **Back-to-Back (B2B) Fatigue Features:** These include `b2b_second_game` (indicator if the game is the second in a back-to-back), `b2b_fatigue` (a rolling frequency count of back-to-back games), and `rest_category` (categorizing rest days before the game). This captures player fatigue effects on performance.

2. **Minutes Trend Features:** Features like `minutes_trend_10`, `minutes_trend_5`, and `minutes_share_change` capture recent trends in playing time, helping models understand workload changes.

3. **Injury Return Features:** `games_since_absence` and `is_ramping_up` track how recently a player returned from injury and whether their minutes are increasing, which can affect performance.

4. **Season Phase Features:** `season_phase` categorizes the season into early, mid, and late phases, while `is_post_allstar` flags games after the All-Star break, capturing temporal effects.

5. **Matchup Features:** Rolling averages of points, rebounds, and assists against specific opponents (`matchup_pts_avg`, etc.) and the number of games played against those opponents (`matchup_games`) provide opponent-specific context.

6. **Target Encoding:** Uses a leak-free shifted expanding mean for team and opponent statistics (points, rebounds, assists), which encodes categorical variables into continuous features reflecting historical performance.

A key fix involved handling NaN values in `rest_category` by converting the categorical cut to float, filling NaNs with a default category, then casting to int to avoid errors during model training.

These engineered features increase the feature set from approximately 397 to 417 columns, enriching the input space for the models to capture nuanced player performance factors.

## Key Properties

- **Feature Count:** Increased from ~397 to 417 columns, with 383 used as features after selection.
- **NaN Handling:** Fixed NaN bug in rest_category by chaining `.astype(float).fillna(3).astype(int)` to avoid errors.
- **Leak-Free Target Encoding:** Uses shifted expanding mean: `x.shift(1).expanding(min_periods=10).mean()` to prevent data leakage.

## Limitations

Feature engineering depends on accurate and complete historical data; noisy or missing data can degrade feature quality. The target encoding assumes stationarity in team/opponent stats, which may not hold in rapidly changing contexts. Also, the NaN fix is a heuristic that may misclassify some rest categories if data is sparse.

## Example

Example pseudocode for rest_category NaN fix:

```python
rest_category = pd.cut(rest_days, bins=[-1,0,1,2,3,10], labels=[0,1,2,3,4])
rest_category = rest_category.astype(float).fillna(3).astype(int)
```

This ensures no NaNs remain before model input.

## Relationship to Other Concepts

- **Target Encoding** — Target encoding is one of the new feature engineering techniques added.

## Practical Applications

Used to improve predictive accuracy of NBA player stat models by capturing fatigue, workload trends, injury recovery, seasonal effects, and opponent-specific performance patterns. These features help models generalize better and adapt to temporal and contextual changes in player performance.

## Sources

- [[Copilot Session Checkpoint: Sprint 10 Retrain In Progress]] — primary source for this concept
