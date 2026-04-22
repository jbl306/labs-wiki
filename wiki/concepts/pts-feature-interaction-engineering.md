---
title: "PTS Feature Interaction Engineering"
type: concept
created: 2026-04-19
last_verified: 2026-04-19
source_hash: "1802936d1c3943c4f998038fc1d70bd57065648d6c678c845a0d02f69f44107b"
sources:
  - raw/2026-04-19-copilot-session-sprint-61-planning-audit-6c5cb258.md
quality_score: 67
concepts:
  - pts-feature-interaction-engineering
related:
  - "[[Feature Engineering Pipeline for NBA ML Platform]]"
  - "[[Sprint 12 NBA ML Engine Code Cleanup and Feature Tuning]]"
  - "[[Copilot Session Checkpoint: Sprint 61 Planning + Audit]]"
tier: hot
tags: [feature-engineering, nba-ml-engine, sports-analytics, interaction-terms, prediction]
---

# PTS Feature Interaction Engineering

## Overview

PTS feature interaction engineering involves the systematic addition of new interaction terms to the NBA ML Engine's feature builder. These interactions capture nuanced relationships between player usage and contextual factors, improving prediction accuracy for points scored (PTS) and related stats.

## How It Works

Feature engineering is a cornerstone of predictive modeling, especially in sports analytics where player performance is influenced by a complex interplay of contextual variables. In Sprint 61, the NBA ML Engine targets new interaction terms for points prediction, specifically:

- `usage × pace_factor`: Captures how a player's usage rate interacts with the game's pace, reflecting opportunities for scoring.
- `home × usage`: Models the effect of home-court advantage on player usage.
- `rest × usage`: Quantifies how rest days impact a player's involvement.
- `usage × opportunity_boost`: (Optional) Measures how external boosts (e.g., teammate injuries) amplify usage effects.

The engineering process unfolds as follows:

1. **Contextual Availability**: The feature builder (`src/features/builder.py`) is structured so that certain variables (e.g., `gadv_usg_pct`) become available only after specific functions run. Sprint 60 revealed an ordering trap: new features dependent on `gadv_usg_pct` must be added after `_add_game_advanced_rolling` (line 90 in `build_features`).
2. **Function Addition**: A new function, `_add_usage_interactions(df)`, is introduced. It is called after `_add_game_advanced_rolling` and `_add_teammate_out_usage_share`, ensuring all necessary context is present.
3. **Feature Construction**: Within `_add_usage_interactions`, interaction terms are computed as arithmetic products of relevant columns. For example:
   ```python
   df['usage_x_pace_factor'] = df['gadv_usg_pct'] * df['pace_factor']
   df['home_x_usage'] = df['home'] * df['gadv_usg_pct']
   df['rest_x_usage'] = df['rest_days'] * df['gadv_usg_pct']
   # Optional
   df['usage_x_opportunity_boost'] = df['gadv_usg_pct'] * df['opportunity_boost']
   ```
4. **Testing**: Tests verify the presence, finiteness, and arithmetic correctness of each new column. Edge cases include missing values, non-finite numbers, or ordering errors.
5. **Avoiding Ordering Traps**: The session emphasizes not repeating Sprint 60's mistake, where features were added before their dependencies were available. Careful sequencing ensures robust feature construction.

The intuition behind these interactions is to capture multiplicative effects that are not evident in raw features. For example, a player's high usage rate may only translate to high scoring if the game's pace is fast, or if the player is well-rested. By explicitly modeling these relationships, the engine can make more granular and accurate predictions.

Trade-offs include increased feature dimensionality, which can lead to overfitting if not managed properly. However, the targeted nature of these interactions (focused on PTS and related stats) mitigates this risk. The engineering is code-only and takes effect at the next model retrain, aligning with the sprint's constraint of no immediate retrain.

## Key Properties

- **Context-Aware Feature Sequencing:** Features are added only after all dependencies are available, preventing ordering errors.
- **Multiplicative Interaction Terms:** New features capture nuanced relationships between usage and contextual factors.
- **Test Coverage:** Tests ensure column presence, arithmetic correctness, and finiteness.

## Limitations

The new features are only effective after the next model retrain. Overfitting risk increases with feature dimensionality. Ordering traps can cause silent failures if dependencies are not properly sequenced. The approach assumes all contextual variables are reliably available and finite.

## Example

```python
# In src/features/builder.py

def _add_usage_interactions(df):
    df['usage_x_pace_factor'] = df['gadv_usg_pct'] * df['pace_factor']
    df['home_x_usage'] = df['home'] * df['gadv_usg_pct']
    df['rest_x_usage'] = df['rest_days'] * df['gadv_usg_pct']
    # Optional
    df['usage_x_opportunity_boost'] = df['gadv_usg_pct'] * df['opportunity_boost']

# Called after _add_game_advanced_rolling and _add_teammate_out_usage_share
```

## Relationship to Other Concepts

- **[[Feature Engineering Pipeline for NBA ML Platform]]** — PTS feature interaction engineering extends the platform's feature engineering pipeline.
- **[[Sprint 12 NBA ML Engine Code Cleanup and Feature Tuning]]** — Both involve systematic feature improvements and sequencing in the NBA ML Engine.

## Practical Applications

This engineering is crucial for sports analytics platforms seeking to improve prediction accuracy for player points and related stats. It is also relevant for any ML system where contextual interactions drive outcomes, such as healthcare, finance, or operations research.

## Sources

- [[Copilot Session Checkpoint: Sprint 61 Planning + Audit]] — primary source for this concept
