---
title: "Primary Prop Line Selection to Avoid Alternate Line Contamination"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "d12567d0a0a05fa3d657bf2e2ec6bb6e9fa482a9676eee6bf73ec13f8bbf53c0"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-dashboard-alt-line-accuracy-fixes-466ff308.md
quality_score: 73
concepts:
  - primary-prop-line-selection-to-avoid-alternate-line-contamination
related:
  - "[[Copilot Session Checkpoint: Dashboard Alt-Line Accuracy Fixes]]"
tier: hot
tags: [sports-betting, data-cleaning, sql, dashboard-accuracy]
---

# Primary Prop Line Selection to Avoid Alternate Line Contamination

## Overview

In sports betting data, alternate or game-prop lines can distort model confidence scores and profit-and-loss (P&L) calculations if not properly filtered. This concept addresses the problem of selecting the correct primary prop line from multiple lines per player and stat, especially when data sources provide alternate lines that differ significantly from primary market lines.

## How It Works

The SportsGameOdds (SGO) DraftKings data source includes both primary and alternate prop lines for player statistics such as assists, rebounds, and blocks. The ingestion pipeline originally used a `setdefault()` method keyed by `(player_id, date, source, stat_name)` which causes the first line encountered to be selected. Since alternate lines often appear first, they contaminate the dataset, resulting in inflated confidence scores and unrealistic P&L calculations.

To fix this, a SQL Common Table Expression (CTE) named `primary_props` was introduced. This CTE selects the prop line closest to the model's predicted value for each player and stat. The selection uses the SQL clause `DISTINCT ON (player_id, stat_name) ORDER BY ABS(predicted_value - line) ASC` to pick the line minimizing the absolute difference from the prediction. This approach naturally favors primary market lines over alternate lines, which tend to be more extreme.

In the history queries, a `ranked_snaps` CTE uses `ROW_NUMBER()` partitioned by player, game date, and stat name, ordered by the absolute difference between predicted value and line, to select the top-ranked line (`WHERE rn = 1`). This ensures that only the most relevant prop line per player/stat/date is used for confidence and P&L calculations.

This SQL-level deduplication and line selection corrects the contamination issue without requiring changes in the upstream data source. It also harmonizes the overview, history, and props page queries to use consistent primary lines.

This method is robust to the presence of multiple alternate lines and adapts dynamically to model prediction changes. It also reduces manual filtering and error-prone heuristics.

Trade-offs include reliance on accurate model predictions for line selection and potential edge cases where the closest line is still an alternate line. However, manual spot checks showed only 0.2% edge cases with minor discrepancies.

Overall, this approach significantly improves dashboard data accuracy and user trust.

## Key Properties

- **SQL Query Pattern:** `DISTINCT ON (player_id, stat_name) ORDER BY ABS(predicted_value - line) ASC` selects closest line to prediction.
- **Partitioning and Ranking:** `ROW_NUMBER() OVER (PARTITION BY player_id, game_date, stat_name ORDER BY ABS(predicted_value - line) ASC)` ranks lines for filtering.
- **Effect on Metrics:** Corrected hit rate from 61.0% to 53.5%, P&L from +309u to +99u, reflecting realistic performance.

## Limitations

Depends on model prediction accuracy; if predictions are off, closest line selection may still pick an alternate line. Does not fix upstream data ingestion ordering, which may cause other subtle issues. Requires SQL support for advanced window functions.

## Example

```sql
WITH primary_props AS (
  SELECT DISTINCT ON (player_id, stat_name) *
  FROM prop_lines
  ORDER BY player_id, stat_name, ABS(predicted_value - line) ASC
)
SELECT * FROM primary_props;
```

## Relationship to Other Concepts

- **Kelly Bankroll Simulator** — Uses corrected confidence and P&L data from primary prop line selection.
- **One-Sided Prop Line Filtering** — Complementary data cleaning to remove invalid prop lines.

## Practical Applications

Used in sports betting ML dashboards to ensure accurate confidence scoring and P&L tracking by filtering out misleading alternate prop lines. Applicable to any multi-line sports betting data ingestion where alternate lines exist.

## Sources

- [[Copilot Session Checkpoint: Dashboard Alt-Line Accuracy Fixes]] — primary source for this concept
