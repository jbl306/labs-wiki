---
title: "Odds API Quota Optimization"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "c4cd8c8e81648711e1dbceea098279d1120878d54e1d8ae18c7015937060ae6d"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-odds-api-quota-optimization-sgo-investigation-f4c98efb.md
quality_score: 76
concepts:
  - odds-api-quota-optimization
related:
  - "[[Durable Copilot Session Checkpoint Promotion]]"
  - "[[Copilot Session Checkpoint: Odds API Quota Optimization, SGO Investigation]]"
tier: hot
tags: [api, quota, optimization, sports-betting]
---

# Odds API Quota Optimization

## Overview

Odds API quota optimization is the process of reducing the number of external API calls made to a sports betting odds provider to stay within a limited monthly quota. This is critical to prevent service disruptions due to quota exhaustion, which causes unauthorized errors and stale data in dependent systems.

## How It Works

The optimization involves analyzing the existing API call patterns and identifying inefficiencies such as redundant fetches and suboptimal request chunking. In this case, the system was making approximately 51 API calls per day due to two separate fetches (pipeline and props-refresh) and a low number of markets requested per API call (3 markets/request). This resulted in about 1,530 calls per month, exceeding the 500 calls/month quota.

To optimize, the following steps were taken:

1. **Eliminate Redundant Fetches:** The morning pipeline fetch of prop lines was removed, leaving only the props-refresh fetch at 22:00 UTC.
2. **Increase Markets Per Request:** The configuration was changed to request 8 markets per API call instead of 3, reducing the number of calls needed per game.
3. **Raise Minimum Requests Remaining Threshold:** The threshold to stop making calls when nearing quota exhaustion was increased from 5 to 50 remaining requests to avoid hitting the quota unexpectedly.
4. **Add Quota Usage Logging:** To monitor API call consumption and detect anomalies early.

These changes reduced the daily calls to about 10, or 300 per month, well within the quota. The quota resets monthly at midnight UTC, so careful monitoring is necessary to avoid hitting limits.

This optimization requires understanding the API usage patterns, the quota limits, and the business logic around when and how often data needs to be refreshed. It also involves code changes in the data fetching modules and configuration adjustments.

## Key Properties

- **Quota Limit:** 500 API calls per month for the Odds API key in use.
- **Old Call Rate:** ~51 calls per day due to double fetching and 3 markets/request chunking.
- **New Call Rate:** ~10 calls per day after removing redundant fetch and increasing markets/request to 8.
- **Quota Reset:** Quota resets on the 1st of each month at 12:00 AM UTC.

## Limitations

The optimization assumes that increasing markets per request does not degrade data quality or increase latency beyond acceptable limits. Removing one of the fetches assumes that the remaining fetch provides sufficiently fresh data for all use cases. If the API provider changes quota policies or data structures, the optimization may need revisiting. Also, the system must handle quota exhaustion gracefully if unexpected spikes occur.

## Example

Pseudocode for quota-aware fetching:

```python
if odds_api_requests_remaining > ODDS_API_MIN_REQUESTS_REMAINING:
    fetch_prop_lines(markets=ODDS_API_MARKETS_PER_REQUEST)
else:
    log('Quota limit reached, skipping fetch')
```

Configuration changes:
```python
ODDS_API_MARKETS_PER_REQUEST = 8
ODDS_API_MIN_REQUESTS_REMAINING = 50
```

Removal of redundant fetch in pipeline:
```python
# Removed prop fetch from morning pipeline to avoid double-fetching
# Previously called fetch_prop_lines() twice daily
```

## Relationship to Other Concepts

- **[[Durable Copilot Session Checkpoint Promotion]]** — This optimization was part of a durable checkpoint promoted for long-term reference.

## Practical Applications

This optimization is applicable in any system consuming third-party APIs with strict rate limits or quotas, especially in sports data, financial data, or other real-time data domains. It helps maintain service availability and data freshness while controlling costs and avoiding service interruptions.

## Sources

- [[Copilot Session Checkpoint: Odds API Quota Optimization, SGO Investigation]] — primary source for this concept
