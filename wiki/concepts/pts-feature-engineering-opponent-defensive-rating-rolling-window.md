---
title: "PTS Feature Engineering With Opponent Defensive Rating Rolling Window"
type: concept
created: 2026-04-19
last_verified: 2026-04-19
source_hash: "d9cea72e0198e7d3d24aa2f2351ac17ebe1246338b49cf42f47130ad7dc14949"
sources:
  - raw/2026-04-19-copilot-session-sprint-60-pts-feature-planning-abd21993.md
quality_score: 100
concepts:
  - pts-feature-engineering-opponent-defensive-rating-rolling-window
related:
  - "[[Feature Engineering Pipeline for NBA ML Platform]]"
  - "[[SHAP Analysis Bug Resolution In NBA ML Engine]]"
  - "[[Copilot Session Checkpoint: Sprint 60 PTS Feature Planning]]"
tier: hot
tags: [feature-engineering, nba-ml, rolling-window, defensive-rating, usage-interaction]
---

# PTS Feature Engineering With Opponent Defensive Rating Rolling Window

## Overview

PTS feature engineering in Sprint 60 centers on introducing new features that capture opponent team defensive strength as a rolling window, and interactions with player usage. This approach aims to address gaps identified in prior SHAP analyses, where defensive matchup signals were underrepresented in points prediction models.

## How It Works

The core idea is to augment the NBA ML Engine's feature set for points (PTS) prediction by incorporating opponent team defensive rating as a rolling statistic, specifically over the last 10 games ('opp_team_def_rating_roll_10'). This rolling window captures recent trends in opponent defensive performance, offering a more dynamic and context-aware signal than static season averages.

To construct this feature, the system must aggregate opponent defensive ratings from the past 10 games, aligning them with the current matchup. This requires careful handling of game logs, ensuring leakage-safe computation (i.e., only using data available before the current game). The rolling calculation can be implemented via SQL or pandas, using window functions or rolling aggregations, and should be integrated into the feature builder pipeline near existing context features (e.g., 'opp_drtg', 'opp_pace').

A key enhancement is the interaction term: multiplying the rolling opponent defensive rating by the player's usage percentage ('gadv_usg_pct'). This interaction models the intuition that high-usage players are more affected by opponent defensive strength, and vice versa. The feature builder must create 'opp_team_def_rating_roll_10_x_gadv_usg_pct' alongside the raw rolling rating.

Edge cases include teams with fewer than 10 games played (early season), where the rolling window should gracefully degrade to available data or use expanding means. For teams with missing defensive rating data, imputation or exclusion must be handled to avoid introducing bias or errors.

This feature engineering is motivated by Sprint 59's SHAP analysis, which showed that usage/minutes dominated PTS prediction, while defensive matchup signals were weak. By explicitly modeling recent opponent defense, the model is expected to improve accuracy, especially for high-variance scoring outcomes. The approach is extensible: similar rolling windows can be applied to other stats (rebounds, assists) and other opponent attributes (pace, points allowed by position).

Trade-offs include increased feature complexity and potential for overfitting if rolling windows are too short or too noisy. Careful validation (e.g., via calibration audit and backtesting) is required to ensure the new features genuinely improve model performance.

## Key Properties

- **Rolling Window Length:** Uses a 10-game rolling window for opponent defensive rating, balancing recency and sample size.
- **Leakage-Safe Computation:** Ensures only past games are used in rolling calculations, preventing information leakage.
- **Interaction With Player Usage:** Creates a feature by multiplying rolling opponent defensive rating with player's usage percentage.
- **Edge Case Handling:** Handles early-season teams with fewer than 10 games and missing data gracefully.

## Limitations

Potential limitations include increased feature complexity, risk of overfitting with short or noisy rolling windows, and dependency on accurate opponent defensive rating data. Early season or teams with incomplete logs may degrade feature quality. Interaction terms can introduce multicollinearity if not properly regularized.

## Example

```python
# Example pseudocode for rolling opponent defensive rating feature
for game in games:
    opp_team = game['opponent']
    past_games = get_past_games(opp_team, before=game['date'], n=10)
    opp_def_rating_roll_10 = np.mean([g['def_rating'] for g in past_games])
    player_usage = game['player']['usage_pct']
    opp_def_roll_x_usage = opp_def_rating_roll_10 * player_usage
    game['features']['opp_def_roll_10'] = opp_def_rating_roll_10
    game['features']['opp_def_roll_x_usage'] = opp_def_roll_x_usage
```

## Relationship to Other Concepts

- **[[Feature Engineering Pipeline for NBA ML Platform]]** — This concept extends the existing feature engineering pipeline with new rolling window features.
- **[[SHAP Analysis Bug Resolution In NBA ML Engine]]** — Sprint 59 SHAP findings motivated the addition of rolling opponent defensive rating features.

## Practical Applications

Used in NBA ML Engine to improve points prediction accuracy by capturing dynamic opponent defensive strength. Applicable to other sports analytics contexts where recent opponent performance is a key predictor. Can be generalized to rolling windows for other stats or attributes.

## Sources

- [[Copilot Session Checkpoint: Sprint 60 PTS Feature Planning]] — primary source for this concept
