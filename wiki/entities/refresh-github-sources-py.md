---
title: "refresh_github_sources.py"
type: entity
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "0a4ff72c02c43a07f603a8baab32716ef2cb63b6d31b3dd941b64676f49cd7bd"
sources:
  - raw/2026-04-22-copilot-session-mobile-node-viewer-and-richer-github-ingestion-8b1dee20.md
quality_score: 100
concepts:
  - refresh-github-sources-py
related:
  - "[[Self-Synthesizing GitHub Source Re-Ingestion Workflow]]"
  - "[[Copilot Session Checkpoint: Mobile Node Viewer And Richer GitHub Ingestion]]"
  - "[[auto_ingest.py]]"
tier: hot
tags: [self-synthesis, github-ingestion, provenance]
---

# refresh_github_sources.py

## Overview

refresh_github_sources.py is a new script for deterministic, skill-driven re-ingestion of GitHub-sourced wiki pages. It refreshes content blocks, ensures provenance, and writes structured source pages without LLM or GitHub Models API calls.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

Enables reproducible, self-synthesizing documentation workflows for technical sources. Supports audit, provenance, and deterministic content refresh in the labs-wiki system.

## Associated Concepts

- **[[Self-Synthesizing GitHub Source Re-Ingestion Workflow]]** — Implements the re-ingestion logic and content block refresh.

## Related Entities

- **[[auto_ingest.py]]** — Uses helpers for content block management.
- **wiki-graph-api** — co-mentioned in source (Tool)
- **wiki-graph-ui** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Mobile Node Viewer And Richer GitHub Ingestion]] — where this entity was mentioned
