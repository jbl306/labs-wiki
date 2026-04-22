---
title: "interaction-targets.js"
type: entity
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "b70af3041d4741db64a44777acc137226f83b7d150d6fbb3afbc693de05fc53a"
sources:
  - raw/2026-04-22-copilot-session-fixing-live-graph-taps-a2ede579.md
quality_score: 100
concepts:
  - interaction-targets-js
related:
  - "[[Mobile-Friendly Graph UI Tap Handling]]"
  - "[[Copilot Session Checkpoint: Fixing Live Graph Taps]]"
  - "[[pointer-gesture.js]]"
  - "[[Dockerfile.graph-ui]]"
tier: hot
tags: [graph-ui, hit-testing, tool]
---

# interaction-targets.js

## Overview

interaction-targets.js is a helper module in the labs-wiki Graph UI that defines shared geometry for label chips and tap targets, ensuring that rendered elements align with hit-testing logic. It was introduced to fix the first node-click bug, enabling reliable selection of visible nodes and labels.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

Critical for aligning rendered label chips with tap targets, solving the usability issue where taps missed nodes despite visual alignment. Its inclusion in the deployment image was guarded by regression tests after packaging errors.

## Associated Concepts

- **[[Mobile-Friendly Graph UI Tap Handling]]** — Provides shared geometry for tap targets.

## Related Entities

- **labs-wiki Graph UI** — Module used by the main graph UI.
- **[[pointer-gesture.js]]** — co-mentioned in source (Tool)
- **[[Dockerfile.graph-ui]]** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Fixing Live Graph Taps]] — where this entity was mentioned
