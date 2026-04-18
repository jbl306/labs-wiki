---
title: "Feature Engineering Pipeline for NBA ML Platform"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9f90b86f2aab32a86e7ca650c6477398444e04958726c5b3ca2ccd9f465e7581"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-data-source-expansion-exploration-b12f747f.md
quality_score: 0
concepts:
  - feature-engineering-pipeline-nba-ml-platform
related:
  - "[[Data Source Expansion for NBA ML Prediction Platform]]"
  - "[[Model Retraining and Evaluation]]"
  - "[[Copilot Session Checkpoint: Data Source Expansion Exploration]]"
tier: hot
tags: [feature engineering, rolling statistics, sports analytics, nba, machine learning]
---

# Feature Engineering Pipeline for NBA ML Platform

## Overview

Feature engineering transforms raw basketball data into meaningful predictive features that improve model performance. The pipeline integrates newly ingested data sources to compute rolling statistics, starter indicators, and advanced metrics for each player and game.

## How It Works

The feature engineering pipeline is implemented primarily in `src/features/builder.py` with a main entry function `build_features()`. It processes multiple data sources to produce a feature matrix for model training:

1. **Starter Features:**
   - Binary indicator if a player started the game (`is_starter`).
   - Rolling averages of minutes played as starter or bench over recent games (`starter_roll_5`, `minutes_starter_avg_10`, `minutes_bench_avg_10`).

2. **Game-Advanced Rolling Features:**
   - 14 features derived from 7 key stats computed over two rolling windows.
   - These capture recent performance trends and variability.

3. **Pending Additions:**
   - Rolling features from player tracking stats (speed, distance, touches).
   - Hustle stats features (deflections, contested shots, loose balls).
   - Basketball Reference advanced metrics (WS, BPM, VORP).

4. **Integration:**
   - Features are merged into a unified feature matrix keyed by player and game.
   - Null and missing value handling ensures data quality.
   - Feature windows and thresholds are configurable via `config.py`.

5. **Output:**
   - The final feature matrix has grown from 95K rows × 341 columns to over 325 features with new expansions.
   - This matrix is used for model training, validation, and prediction.

The pipeline is designed for extensibility to incorporate new data sources as they become available, supporting continuous improvement of model inputs.

## Key Properties

- **Modular Feature Addition:** New feature groups are added via dedicated functions (_add_starter_features, _add_game_advanced_rolling) for maintainability.
- **Rolling Window Computations:** Features use rolling averages over configurable windows to capture temporal trends.
- **Configurable Thresholds:** Stat-specific edge thresholds and excluded stats are defined in a central config for easy tuning.
- **Scalability:** Pipeline handles large feature matrices efficiently, supporting over 300 features and 95K+ rows.

## Limitations

The pipeline depends on complete and validated input data; missing or null values in key columns can degrade feature quality. Rolling window computations may be sensitive to sparse data or irregular game schedules. Adding new features requires careful validation to avoid data leakage or multicollinearity. The current pipeline has some cosmetic warnings (e.g., pandas FutureWarning) that do not break functionality but should be addressed.

## Example

Example snippet from feature builder:

```python
def _add_starter_features(df):
    df['is_starter'] = df['starter_flag'].astype(int)
    df['starter_roll_5'] = df.groupby('player_id')['is_starter'].rolling(5).mean().reset_index(level=0, drop=True)
    df['minutes_starter_avg_10'] = df.groupby('player_id')['minutes_played'].rolling(10).mean().reset_index(level=0, drop=True)
    return df
```

This function computes starter-related features using rolling averages grouped by player.

## Relationship to Other Concepts

- **[[Data Source Expansion for NBA ML Prediction Platform]]** — Feature engineering depends on newly ingested data sources to create predictive features.
- **[[Model Retraining and Evaluation]]** — Engineered features are inputs for retraining models and evaluating performance gains.

## Practical Applications

Feature engineering pipelines like this are essential in sports analytics and other time-series prediction domains to capture player form, game context, and advanced metrics that improve model accuracy and robustness.

## Sources

- [[Copilot Session Checkpoint: Data Source Expansion Exploration]] — primary source for this concept
