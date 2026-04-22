---
title: "pointer-gesture.js"
type: entity
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "b70af3041d4741db64a44777acc137226f83b7d150d6fbb3afbc693de05fc53a"
sources:
  - raw/2026-04-22-copilot-session-fixing-live-graph-taps-a2ede579.md
quality_score: 46
concepts:
  - pointer-gesture-js
related:
  - "[[Mobile-Friendly Graph UI Tap Handling]]"
  - "[[Copilot Session Checkpoint: Fixing Live Graph Taps]]"
  - "[[interaction-targets.js]]"
  - "[[Dockerfile.graph-ui]]"
tier: hot
tags: [graph-ui, touch-interaction, tool]
---

# pointer-gesture.js

## Overview

pointer-gesture.js is a module in the labs-wiki Graph UI that encapsulates touch gesture handling, including pointer-type-specific tap slop and pan initiation logic. It was introduced to fix the second node-click bug, allowing slight finger drift on touch devices to still count as a tap.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

Essential for robust mobile tap handling, distinguishing between touch and mouse pointers, and preventing premature pan gestures. Its deployment was validated via regression tests and operational asset checks.

## Associated Concepts

- **[[Mobile-Friendly Graph UI Tap Handling]]** — Implements touch gesture tolerance.

## Related Entities

- **labs-wiki Graph UI** — Module used by the main graph UI.
- **[[interaction-targets.js]]** — co-mentioned in source (Tool)
- **[[Dockerfile.graph-ui]]** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Fixing Live Graph Taps]] — where this entity was mentioned
