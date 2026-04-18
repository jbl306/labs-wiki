---
title: "Data Source Expansion for NBA ML Prediction Platform"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9f90b86f2aab32a86e7ca650c6477398444e04958726c5b3ca2ccd9f465e7581"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-data-source-expansion-exploration-b12f747f.md
quality_score: 100
concepts:
  - data-source-expansion-nba-ml-prediction-platform
related:
  - "[[Copilot Session Checkpoint: Data Source Expansion Exploration]]"
tier: hot
tags: [data ingestion, feature engineering, sports analytics, NBA, machine learning]
---

# Data Source Expansion for NBA ML Prediction Platform

## Overview

Data source expansion is a critical process in enhancing the predictive accuracy and robustness of machine learning models by integrating additional relevant datasets. In the context of an NBA ML prediction platform, expanding data sources involves ingesting new basketball statistics from APIs, CDNs, and web scrapers to enrich feature sets for model training and evaluation.

## How It Works

The data source expansion process for the NBA ML platform is organized into multiple phases, each targeting specific datasets and ingestion methods:

1. **Phase 1A-1C (Completed):**
   - Position backfill for all active players to fill previously null position data.
   - Starter data backfill using CDN sources to achieve near-complete coverage.
   - Partial ingestion of advanced game statistics from NBA CDN, handling over 270,000 rows.
   - Integration of starter features and game-advanced rolling features into the feature engineering pipeline.

2. **Phase 2 (Pending):**
   - Player tracking stats ingestion using the BoxScorePlayerTrackV3 endpoint, capturing metrics such as speed, distance, touches, and contested shots.
   - Hustle stats ingestion from LeagueHustleStatsPlayer endpoint, including deflections, loose balls, and box outs.
   - Basketball Reference integration to scrape advanced metrics like Win Shares (WS), Box Plus/Minus (BPM), and Value Over Replacement Player (VORP).

3. **Phase 3 and 4 (Pending):**
   - Incorporation of game lines, enhanced prop bets, Rotowire lineups, clutch stats, defensive tracking, standings, and rotation data.

The ingestion process involves:
- Writing ingestion functions for each data source.
- Backfilling historical data to ensure completeness.
- Adding new features to the feature builder pipeline.
- Deploying updated code and running migrations on the homelab server.
- Validating data integrity, coverage, and null values.
- Retraining models with the expanded feature set.
- Evaluating model performance improvements through metrics such as R² and hit rates.

This phased approach allows incremental integration and validation, reducing risk and enabling targeted improvements in predictive accuracy.

## Key Properties

- **Phased Implementation:** Data source expansion is divided into discrete phases (1A-4) to manage complexity and ensure systematic progress.
- **Data Integrity Checks:** Comprehensive validation includes null checks, coverage verification, and consistency across tables.
- **Feature Engineering Integration:** New data sources feed into the feature builder pipeline, adding rolling and advanced statistical features.
- **Deployment Environment:** Uses a homelab server with Docker containers for all services, enabling isolated, reproducible deployments.
- **API Rate Limits and Delays:** NBA API requires a 0.6s delay between requests to avoid IP blocking; CDN sources have faster access but some data approximations.

## Limitations

Data source expansion depends on external APIs and web scrapers, which may have rate limits, outages, or incomplete data. For example, the NBA API outage required fallback to CDN data, which uses team proxies for some metrics, reducing individual player accuracy. Some data fields initially had 100% null values requiring backfill. Integration of new sources requires careful validation to avoid corrupt or incomplete features. Additionally, scraping Basketball Reference is rate-limited (~20 requests/min) and requires delay management.

## Example

Pseudocode for a data ingestion function for player tracking stats:

```python
def ingest_game_tracking_stats(date):
    # Query BoxScorePlayerTrackV3 endpoint for the given date
    data = nba_api.get_box_score_player_track_v3(date)
    # Validate data integrity
    if not validate_data(data):
        raise ValueError('Data validation failed')
    # Insert data into player_tracking_stats table
    db.insert('player_tracking_stats', data)
    # Update feature builder with new rolling features
    features = build_tracking_rolling_features(data)
    db.update_features(features)
```

This function would be scheduled as part of the daily pipeline and also used for backfilling historical data.

## Relationship to Other Concepts

- **Feature Engineering Pipeline** — Data source expansion feeds new raw data into the feature engineering pipeline to create predictive features.
- **Model Retraining and Evaluation** — Expanded data sources enable retraining models with richer features and evaluating performance improvements.

## Practical Applications

This approach is applicable for any sports analytics platform aiming to improve prediction accuracy by integrating diverse data sources. It ensures systematic ingestion, validation, and feature integration, supporting continuous model improvement and deployment in production environments.

## Sources

- [[Copilot Session Checkpoint: Data Source Expansion Exploration]] — primary source for this concept
