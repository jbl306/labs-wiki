---
title: "Dockerfile.graph-ui"
type: entity
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "b70af3041d4741db64a44777acc137226f83b7d150d6fbb3afbc693de05fc53a"
sources:
  - raw/2026-04-22-copilot-session-fixing-live-graph-taps-a2ede579.md
quality_score: 55
concepts:
  - dockerfile-graph-ui
related:
  - "[[Deployment Packaging Hardening for Static Web Assets]]"
  - "[[Copilot Session Checkpoint: Fixing Live Graph Taps]]"
  - "[[interaction-targets.js]]"
  - "[[pointer-gesture.js]]"
tier: hot
tags: [deployment, docker, static-assets, tool]
---

# Dockerfile.graph-ui

## Overview

Dockerfile.graph-ui is the deployment configuration file for the labs-wiki Graph UI, responsible for copying static assets into the nginx image. It was updated to use wildcard copying for JS modules, preventing repeated packaging regressions and ensuring all UI modules are included in production.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | 2026 |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

Central to deployment reliability; its improvement from hand-maintained lists to wildcards eliminated silent asset omissions and enabled robust regression testing for asset inclusion.

## Associated Concepts

- **[[Deployment Packaging Hardening for Static Web Assets]]** — Implements wildcard asset copying.

## Related Entities

- **labs-wiki Graph UI** — Deployment configuration for the graph UI.
- **[[interaction-targets.js]]** — co-mentioned in source (Tool)
- **[[pointer-gesture.js]]** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Fixing Live Graph Taps]] — where this entity was mentioned
