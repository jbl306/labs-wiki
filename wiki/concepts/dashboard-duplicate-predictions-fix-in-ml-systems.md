---
title: "Dashboard Duplicate Predictions Fix in ML Systems"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "1544a9390c8a215aeb38b788d3103fd5a18163dc8ce9182c4c6fc36fbb638e43"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-implementing-critical-ml-fixes-sprint-28-9cff218d.md
quality_score: 100
concepts:
  - dashboard-duplicate-predictions-fix-in-ml-systems
related:
  - "[[Copilot Session Checkpoint: Implementing Critical ML Fixes Sprint 28]]"
tier: hot
tags: [dashboard, data deduplication, frontend, sql]
---

# Dashboard Duplicate Predictions Fix in ML Systems

## Overview

Duplicate predictions in dashboards can confuse users and degrade trust in ML system outputs. Fixing duplication involves addressing root causes in data queries, API responses, and frontend rendering logic.

## How It Works

The root cause of duplicate predictions was identified as a SQL join fan-out issue. The `prediction_blend` Common Table Expression (CTE) grouped predictions by `(player_id, game_date, stat_name)`, producing one row per player/stat. However, the `prop_lines` table contained multiple rows per `(player_id, game_date, stat_name, source)` due to multiple sportsbooks providing lines for the same player/stat. Joining these tables caused multiple rows per player/stat, resulting in duplicates.

The fix involved several coordinated changes:

- **SQL**: Increased the `LIMIT` on the `best_predictions` query from 10 to 30 to allow more data for deduplication.

- **TypeScript**: Added deduplication logic using a `Set` keyed by the combination of `player_name` and `stat_name`. This filters out duplicate entries before slicing to the final 10 results.

- **React**: Changed the `key` prop in React components rendering prediction lists from a `source` string (which could be duplicated) to the list index (`key={idx}`) to prevent React warnings about duplicate keys.

This multi-layered approach ensures duplicates are removed both at the data retrieval and UI rendering stages.

Trade-offs include slightly increased data retrieval volume and reliance on frontend deduplication logic, which is simpler than complex SQL DISTINCT ON queries with template literals.

Edge cases include new data sources adding unexpected duplicates and potential performance impacts from larger SQL limits.

## Key Properties

- **SQL Join Fan-Out:** Multiple sportsbook lines cause join to produce multiple rows per player/stat.
- **TypeScript Deduplication:** Uses a Set keyed by `player_name-stat_name` to filter duplicates.
- **React Key Fix:** Uses list index as React key to avoid duplicate key warnings.
- **SQL Limit Increase:** Increased from 10 to 30 to allow sufficient data for deduplication.

## Limitations

Frontend deduplication may mask underlying data issues; ideally, deduplication should be handled as early as possible. Increasing SQL limits may affect query performance. React key by index can cause rendering inefficiencies if list order changes frequently.

## Example

```typescript
// TypeScript deduplication example
const seen = new Set<string>();
const deduped = predictions.filter(p => {
  const key = `${p.player_name}-${p.stat_name}`;
  if (seen.has(key)) return false;
  seen.add(key);
  return true;
}).slice(0, 10);

// React key fix
{deduped.map((item, idx) => <PredictionRow key={idx} data={item} />)}
```

## Relationship to Other Concepts

- **Data Pipeline Debugging** — Fixing duplicates involves debugging data joins and frontend rendering.

## Practical Applications

Improves user experience and trust in ML dashboards by ensuring unique, accurate prediction displays. Applicable in any ML system with multi-source data aggregation and UI presentation.

## Sources

- [[Copilot Session Checkpoint: Implementing Critical ML Fixes Sprint 28]] — primary source for this concept
