---
title: "One-Sided Prop Line Filtering in Sports Betting Data"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "d12567d0a0a05fa3d657bf2e2ec6bb6e9fa482a9676eee6bf73ec13f8bbf53c0"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-dashboard-alt-line-accuracy-fixes-466ff308.md
quality_score: 64
concepts:
  - one-sided-prop-line-filtering-in-sports-betting-data
related:
  - "[[Primary Prop Line Selection to Avoid Alternate Line Contamination]]"
  - "[[Copilot Session Checkpoint: Dashboard Alt-Line Accuracy Fixes]]"
tier: hot
tags: [data-cleaning, sports-betting, data-ingestion]
---

# One-Sided Prop Line Filtering in Sports Betting Data

## Overview

One-sided prop lines in sports betting data are those where either the over or under odds are missing (NULL), often representing non-standard bets like 'will the player get 3+ blocks?'. These lines can distort analytics and must be filtered out during data ingestion to maintain data quality.

## How It Works

The SportsGameOdds DraftKings data source includes many prop lines with missing odds on one side, especially in stats like steals (stl) and blocks (blk). For example, a block line at 2.5 may have over odds (+800) but no under odds, representing a one-sided bet.

Such lines are problematic because they do not represent a standard over/under market and can skew confidence calculations and P&L metrics.

To address this, a filter was added in the ingestion script (`prop_lines.py`) that rejects any prop line where either `over_odds` or `under_odds` is NULL. This is implemented as a simple conditional check during the extraction of prop rows:

```python
if over_odds is None or under_odds is None:
    continue  # skip one-sided prop line
```

Additionally, existing bad data with missing odds was cleaned from the database by deleting 814 prop lines and 1,840 prop line snapshots.

This filtering ensures that only valid, two-sided prop lines enter the prediction and dashboard pipelines, improving data consistency and reliability.

The filter is applied at ingestion, preventing contamination downstream. This complements the primary prop line selection logic by removing invalid lines before selection.

Trade-offs include potentially excluding some niche or specialized bets that are one-sided by nature, but this is acceptable for the goal of accurate modeling and dashboard reporting.

## Key Properties

- **Filter Condition:** Reject prop lines where `over_odds IS NULL OR under_odds IS NULL`.
- **Data Cleanup:** Deleted 814 prop_lines and 1,840 prop_line_snapshots with missing odds from DB.
- **Impact:** Removes 17.2% of prop lines with missing under odds, concentrated in stl/blk stats.

## Limitations

Excludes one-sided bets that might be valid in some contexts; assumes both sides of odds must be present for valid prop lines. Relies on accurate NULL detection in source data.

## Example

```python
def filter_prop_lines(prop_line):
    if prop_line.over_odds is None or prop_line.under_odds is None:
        return False  # reject
    return True
```

## Relationship to Other Concepts

- **[[Primary Prop Line Selection to Avoid Alternate Line Contamination]]** — Works together to ensure only valid, primary prop lines are used.

## Practical Applications

Applied in sports betting data ingestion pipelines to improve data quality by excluding invalid one-sided prop lines, thereby enhancing model prediction accuracy and dashboard reporting.

## Sources

- [[Copilot Session Checkpoint: Dashboard Alt-Line Accuracy Fixes]] — primary source for this concept
