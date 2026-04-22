---
title: "scripts/auto_ingest.py"
type: entity
created: 2026-04-20
last_verified: 2026-04-22
source_hash: "58f7e891b3f357ec9e293d8dfe365b373ec7a7fbe3eba4e22a93947cc4d024c4"
sources:
  - raw/2026-04-20-copilot-session-url-followup-pass-b53bba3e.md
  - raw/2026-04-20-copilot-session-pilot-worktree-baseline-10f2a2a8.md
quality_score: 47
concepts:
  - scripts-auto-ingest-py
related:
  - "[[Worktree-Based Baseline Verification for Durable Workflow Pilots]]"
  - "[[Copilot Session Checkpoint: Pilot Worktree Baseline]]"
tier: hot
tags: [ingestion, python, artifact-generation, pilot]
---

# scripts/auto_ingest.py

## Overview

scripts/auto_ingest.py is the central ingestion script in labs-wiki, responsible for fetching URL content, processing raw sources, and updating wiki artifacts. It currently supports live-fetching content from various sources but does not persist fetched content back into raw files.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | 2026 |
| Creator | Unknown |
| URL | https://github.com/jbl306/labs-wiki/blob/main/scripts/auto_ingest.py |
| Status | Active |

## Relevance

This script is the main target for implementing the URL raw preservation pilot. Its functions and constraints, such as fetch_url_content and ingest_raw_source, define the technical seam for pilot execution.

## Associated Concepts

- **[[Worktree-Based Baseline Verification for Durable Workflow Pilots]]** — auto_ingest.py is the primary script verified in baseline before pilot implementation.

## Related Entities

- **labs-wiki** — Parent project/repository

## Sources

- [[Copilot Session Checkpoint: Pilot Worktree Baseline]] — where this entity was mentioned
- [[Copilot Session Checkpoint: URL Followup Pass]] — additional source
