---
title: "tmp_free_tier_url_backfill.py"
type: entity
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "6d1d5390738d68e0aaef5baf1126bb8caaff561e8e8b9d0084a6fcafd3d0555f"
sources:
  - raw/2026-04-21-copilot-session-free-tier-backfill-runner-a2d20186.md
quality_score: 50
concepts:
  - tmp-free-tier-url-backfill-py
related:
  - "[[Free-Tier-Constrained Backfill Runner Design]]"
  - "[[Copilot Session Checkpoint: Free Tier Backfill Runner]]"
tier: hot
tags: [backfill, tool, python, automation]
---

# tmp_free_tier_url_backfill.py

## Overview

A temporary Python script developed for the labs-wiki project to perform conservative, free-tier-constrained backfill of URL-based wiki raws. It implements dry-run preview, candidate ranking, batch execution with rate-limit detection, and phase cutoffs for high-value and full backfill runs. The script is security-hardened to avoid token leakage and is designed for integration with homelab scheduling and notification systems.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | 2026 |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

This runner is central to enabling durable, low-risk ingestion of valuable web content into the labs-wiki under strict API quota constraints. It provides a template for secure, auditable, and resilient automation in environments with limited API access.

## Associated Concepts

- **[[Free-Tier-Constrained Backfill Runner Design]]** — Implements the design and operational logic described in the concept.

## Related Entities

- **auto_ingest.py** — Ingestion engine invoked by the runner for actual content fetching and processing.

## Sources

- [[Copilot Session Checkpoint: Free Tier Backfill Runner]] — where this entity was mentioned
