---
title: "Handling PostgreSQL NUMERIC Type in Node.js with pg Library"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "bda088556b526d765495b4eb44e9e07a7a9a83c274765d5b943d5a42aa248499"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-props-db-query-and-chart-refinement-402d70da.md
quality_score: 100
concepts:
  - handling-postgresql-numeric-type-in-nodejs-pg-library
related:
  - "[[Express.js]]"
  - "[[Copilot Session Checkpoint: Props DB Query and Chart Refinement]]"
tier: hot
tags: [postgresql, nodejs, pg-library, data-type-handling]
---

# Handling PostgreSQL NUMERIC Type in Node.js with pg Library

## Overview

PostgreSQL's NUMERIC type is used for exact numeric values but is returned by the `pg` Node.js library as strings by default. This can cause runtime errors in JavaScript when numeric operations are expected. Proper handling and conversion are necessary to maintain type safety and avoid frontend crashes.

## How It Works

The `pg` library returns PostgreSQL NUMERIC and other arbitrary precision types as strings to avoid precision loss inherent in JavaScript's Number type. However, when the frontend or server code expects numeric values (e.g., for `.toFixed()` calls or arithmetic), this leads to errors.

To address this, a helper function `numericRow()` is introduced in the BFF server code. This function iterates over query result rows and converts string fields representing numeric values into JavaScript numbers using `parseFloat()` or similar methods.

This conversion must be done cautiously because:

- Some NUMERIC values may exceed JavaScript's safe integer range, risking precision loss.
- The conversion should be applied only to known numeric fields, not all strings.
- The helper must be integrated consistently across all endpoints returning NUMERIC data.

In this project, the helper was applied to all DB query results involving `ROUND()` or NUMERIC columns, fixing frontend crashes caused by `.toFixed()` calls on strings.

## Key Properties

- **Type Conversion:** Converts NUMERIC strings to JavaScript numbers to enable numeric operations.
- **Selective Application:** Applied only to fields known to be numeric to avoid incorrect conversions.
- **Integration Point:** Used as a post-processing step after DB query results are fetched.

## Limitations

Converting NUMERIC to JavaScript Number can cause precision loss for very large or precise values. For financial or scientific applications requiring exact precision, alternative libraries or string handling may be necessary. Also, improper conversion can cause data corruption or runtime errors.

## Example

Example `numericRow()` helper snippet:

```typescript
function numericRow(rows: any[]) {
  return rows.map(row => {
    for (const key in row) {
      if (typeof row[key] === 'string' && isNumericString(row[key])) {
        row[key] = parseFloat(row[key]);
      }
    }
    return row;
  });
}

function isNumericString(value: string) {
  return /^\d+(\.\d+)?$/.test(value);
}
```
This ensures numeric strings are safely converted before sending to frontend.

## Relationship to Other Concepts

- **PostgreSQL Data Types** — NUMERIC type handling in Node.js
- **[[Express.js]]** — Helper used in Express BFF server

## Practical Applications

Critical for any Node.js backend querying PostgreSQL databases with numeric or decimal columns, especially when frontend expects numeric types for calculations or formatting. Prevents common bugs and runtime errors in data-driven web applications.

## Sources

- [[Copilot Session Checkpoint: Props DB Query and Chart Refinement]] — primary source for this concept
