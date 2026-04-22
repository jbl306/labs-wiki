---
title: "Replacing FastAPI Proxy with Direct PostgreSQL Query for Historical Props Data"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "bda088556b526d765495b4eb44e9e07a7a9a83c274765d5b943d5a42aa248499"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-props-db-query-and-chart-refinement-402d70da.md
quality_score: 76
concepts:
  - replacing-fastapi-proxy-with-direct-postgresql-query-for-historical-props-data
related:
  - "[[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]]"
  - "[[Copilot Session Checkpoint: Props DB Query and Chart Refinement]]"
tier: hot
tags: [fastapi, postgresql, api-design, sports-analytics]
---

# Replacing FastAPI Proxy with Direct PostgreSQL Query for Historical Props Data

## Overview

The original FastAPI endpoint `/prop-edges` only returned data for the current day, causing the Props page to show no data on days without games. To provide comprehensive historical data and support date filtering, the endpoint was replaced with a direct PostgreSQL query within the BFF.

## How It Works

The FastAPI `/prop-edges` endpoint limitation was identified as the root cause of missing props data on days with no games. The solution involved:

- Writing a new SQL query that selects prop edges from the database filtered by a provided date parameter.
- Implementing a new BFF Express endpoint `/api/props` that executes this query directly against PostgreSQL.
- Returning both the filtered props data and the list of available dates to enable a date picker on the frontend.
- Updating the frontend PropsPage to include a date picker control that uses the available dates from the API and passes the selected date back to the API.
- This approach removes dependency on FastAPI for this data, reduces latency, and provides richer historical access.

The new SQL query supports filtering by game date, enabling users to explore props data across multiple days, not just today.

## Key Properties

- **Date Filtering:** Supports querying props data for arbitrary dates, not just today.
- **Direct DB Access:** Bypasses FastAPI proxy to improve data availability and control.
- **API Response Structure:** Includes props data and available dates for UI date picker.
- **Frontend Integration:** PropsPage updated to allow user selection of date filter.

## Limitations

Requires frontend and API coordination to handle date selection and data updates. The direct DB query must be maintained alongside FastAPI endpoints to avoid duplication. Potential for increased query complexity and load on the database if date ranges are large.

## Example

Example new API endpoint snippet:

```typescript
app.get('/api/props', async (req, res) => {
  const date = req.query.date || getMostRecentDate();
  const propsData = await db.query(`SELECT * FROM prop_edges WHERE game_date = $1`, [date]);
  const dates = await db.query(`SELECT DISTINCT game_date FROM prop_edges ORDER BY game_date DESC`);
  res.json({ props: numericRow(propsData.rows), dates: dates.rows.map(r => r.game_date) });
});
```

Frontend uses `dates` to populate a date picker and fetches props data accordingly.

## Relationship to Other Concepts

- **[[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]]** — BFF implements the new direct DB query endpoint
- **PostgreSQL Data Querying** — SQL query filters props data by date

## Practical Applications

Enables users to explore historical props data in sports analytics dashboards, overcoming limitations of single-day API endpoints. Improves data freshness and user experience by providing richer filtering options.

## Sources

- [[Copilot Session Checkpoint: Props DB Query and Chart Refinement]] — primary source for this concept
