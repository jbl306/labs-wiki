---
title: "Edge Gating and Stat-Specific Thresholds in ML Prediction Pipelines"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "f8d0a04a06d081eb78a648694aa8e0e839423db4ece7d887aafeef2087fa93fe"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-retrained-models-deploying-improvements-59ba9a6c.md
  - raw/2026-04-18-copilot-session-sprint-55-implementation-and-deployment-2d04e4e0.md
quality_score: 100
concepts:
  - edge-gating-stat-specific-thresholds-ml-prediction-pipelines
related:
  - "[[Stat Exclusion Policy In ML Prediction Pipelines]]"
  - "[[Copilot Session Checkpoint: Sprint 55 Implementation and Deployment]]"
tier: hot
tags: [prediction-filtering, stat-thresholds, confidence-gating]
---

# Edge Gating and Stat-Specific Thresholds in ML Prediction Pipelines

## Overview

Edge gating and stat-specific thresholds are mechanisms for filtering predictions in ML pipelines, ensuring that only predictions with sufficient confidence and statistical significance are surfaced. Sprint 55 introduced min/max edge caps, confidence gating, and minutes gating to improve prediction quality and reduce noise.

## How It Works

Edge gating refers to the process of applying minimum and maximum thresholds to prediction edges (the difference between predicted and actual values) in ML pipelines. In Sprint 55, new configuration parameters were added to enforce stat-specific edge caps, such as STAT_EDGE_MAX_ABSOLUTE and raised STAT_EDGE_ABSOLUTE thresholds for points, rebounds, assists, etc.

The prediction pipeline (`src/inference/predictor.py`) was modified so that the `passes_edge_filter()` function checks both minimum and maximum edge values. Predictions outside these bounds are filtered out, preventing extreme or low-confidence predictions from reaching downstream consumers.

Confidence gating was also introduced, requiring predicted probability P > 0.55 for a prediction to be considered valid. This ensures that only predictions with sufficient model confidence are surfaced. Minutes gating was added to filter predictions based on minimum predicted playing time (e.g., MIN_PREDICTED_MINUTES=15), reducing noise from players with uncertain participation.

These gating mechanisms are applied in both the predictor pipeline and the prop matching/filtering pipeline (`src/applications/prop_finder.py`). The main prop loop now includes checks for edge caps, confidence, and minutes, ensuring that only high-quality predictions are considered.

Edge cases include tuning thresholds for each stat to balance coverage and precision. Too strict thresholds may reduce the number of valid predictions, while too loose thresholds may allow noisy outputs. The gating logic is configurable, allowing for rapid iteration and adjustment based on live metrics.

Trade-offs involve the risk of excluding borderline predictions that may still be valuable. However, the overall improvement in prediction quality and reduction in false positives justifies the approach, especially in high-stakes environments like sports betting.

## Key Properties

- **Stat-Specific Thresholds:** Different min/max edge caps for each stat (points, rebounds, assists, etc.), configurable in `config.py`.
- **Confidence Gating:** Requires predicted probability P > 0.55 for inclusion.
- **Minutes Gating:** Filters out predictions for players with less than minimum predicted playing time.

## Limitations

Thresholds must be carefully tuned; overly strict gating may reduce coverage, while loose gating may allow noise. Requires ongoing monitoring and adjustment based on live metrics.

## Example

```python
def passes_edge_filter(edge, stat):
    min_edge = STAT_EDGE_ABSOLUTE[stat]
    max_edge = STAT_EDGE_MAX_ABSOLUTE[stat]
    return min_edge <= abs(edge) <= max_edge

if passes_edge_filter(edge, stat) and confidence > 0.55 and minutes >= 15:
    # Prediction is valid
```

## Relationship to Other Concepts

- **[[Stat Exclusion Policy In ML Prediction Pipelines]]** — Both involve filtering predictions based on statistical criteria.

## Practical Applications

Used in ML prediction pipelines for sports analytics, finance, and healthcare to ensure only high-confidence, statistically significant predictions are surfaced. Reduces false positives and improves actionable insights.

## Sources

- [[Copilot Session Checkpoint: Sprint 55 Implementation and Deployment]] — primary source for this concept
- [[Copilot Session Checkpoint: Retrained Models, Deploying Improvements]] — additional source
