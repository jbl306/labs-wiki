---
title: "Teammate-Injured-Usage Delta Feature"
type: concept
created: 2026-04-19
last_verified: 2026-04-19
source_hash: "d9cea72e0198e7d3d24aa2f2351ac17ebe1246338b49cf42f47130ad7dc14949"
sources:
  - raw/2026-04-19-copilot-session-sprint-60-pts-feature-planning-abd21993.md
quality_score: 100
concepts:
  - teammate-injured-usage-delta-feature
related:
  - "[[Feature Engineering Pipeline for NBA ML Platform]]"
  - "[[Copilot Session Checkpoint: Sprint 60 PTS Feature Planning]]"
tier: hot
tags: [feature-engineering, nba-ml, injury-impact, usage-delta, team-dynamics]
---

# Teammate-Injured-Usage Delta Feature

## Overview

The teammate-injured-usage delta feature quantifies the impact of injured teammates on a player's opportunity, weighting each injured teammate by their recent usage percentage. This provides a more nuanced signal than simple counts, capturing shifts in team dynamics that affect individual player performance.

## How It Works

In the NBA ML Engine, the teammate-injured-usage delta is designed to improve prediction accuracy by modeling how the absence of high-usage teammates increases a player's opportunity. The existing feature builder produces only a count of injured teammates and a basic opportunity boost, but does not account for the varying influence of each teammate.

To compute the delta, the system identifies teammates who are out or doubtful for a given game. For each, it retrieves their recent usage percentage (e.g., via a rolling window over their last N games, such as 'gadv_usg_pct_roll_10'). The usage percentages are summed across all injured teammates, yielding a total 'injured_usage_sum'.

This sum is then compared against a team baseline — the typical usage sum for all teammates when healthy. The difference ('usage_delta') represents the additional opportunity available to the remaining players. This value is assigned as a feature for the target player, indicating how much extra usage is likely to be redistributed.

Edge cases include teams with no injured teammates (delta is zero), or missing usage data (impute or exclude). The feature can be normalized by team total usage to avoid scaling issues. For teams with multiple injuries, the effect is additive, but care must be taken to avoid double-counting if players overlap in positions or roles.

This approach is motivated by the intuition that losing a high-usage teammate (e.g., a star player) has a greater impact than losing a bench player. By quantifying this effect, the model can better predict spikes in scoring, assists, or other stats when key teammates are absent.

Trade-offs include increased data requirements (must track teammate usage histories) and potential for noise if injury reports are unreliable or usage fluctuates rapidly. Validation via backtesting and calibration audit is essential to ensure the feature improves predictive power.

## Key Properties

- **Usage-Weighted Injury Impact:** Weights each injured teammate by their recent usage percentage, capturing their influence on team dynamics.
- **Rolling Window For Usage:** Uses a rolling window (e.g., last 10 games) to compute teammate usage, ensuring recency and stability.
- **Delta Against Team Baseline:** Computes the difference between injured usage sum and team baseline, quantifying extra opportunity.
- **Edge Case Handling:** Handles cases with no injured teammates or missing usage data gracefully.

## Limitations

Relies on accurate injury reports and teammate usage histories. May introduce noise if usage fluctuates or injury status changes late. Potential for scaling issues if not normalized. Complex to implement for teams with frequent lineup changes.

## Example

```python
injured_teammates = get_injured_teammates(game['team'], game['date'])
injured_usage_sum = sum([get_usage_pct(teammate, window=10) for teammate in injured_teammates])
team_baseline_usage = get_team_baseline_usage(game['team'])
usage_delta = injured_usage_sum - team_baseline_usage
game['features']['teammate_injured_usage_delta'] = usage_delta
```

## Relationship to Other Concepts

- **[[Feature Engineering Pipeline for NBA ML Platform]]** — This feature is an extension to the pipeline, improving modeling of teammate effects.

## Practical Applications

Enhances NBA ML Engine predictions for points, assists, rebounds, etc., by modeling shifts in opportunity due to teammate injuries. Useful in fantasy sports, betting, and team analytics where lineup changes affect individual performance.

## Sources

- [[Copilot Session Checkpoint: Sprint 60 PTS Feature Planning]] — primary source for this concept
