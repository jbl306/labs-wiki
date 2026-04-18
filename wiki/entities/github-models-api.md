---
title: "GitHub Models API"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "1e682ce7421bcaeabd752a7742a3c49d999aeb75bc995c31118f12c24d1a690c"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-pipeline-enhancements-and-vision-support-deploye-5028ddea.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-auto-ingest-pipeline-built-and-docs-updated-f3b54c4f.md
quality_score: 100
concepts:
  - github-models-api
related:
  - "[[Auto-Ingest Pipeline for Wiki Markdown Processing]]"
  - "[[Copilot Session Checkpoint: Auto-ingest Pipeline Built and Docs Updated]]"
  - "[[Docker]]"
  - "[[Python Watchdog Library]]"
tier: hot
tags: [llm, api, github, gpt-4o]
---

# GitHub Models API

## Overview

An API service provided by GitHub that offers access to large language models such as GPT-4o. It supports OpenAI-compatible API calls and includes rate limits and billing tiers. The API is used here to process raw markdown content into structured JSON outputs for wiki page generation.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | GitHub |
| URL | N/A |
| Status | Active |

## Relevance

Central to the auto-ingest pipeline, this API enables LLM-powered extraction of concepts and entities from raw markdown files, facilitating automated wiki page creation. It integrates with the Copilot subscription and supports a free tier with specific rate limits.

## Associated Concepts

- **[[Auto-Ingest Pipeline for Wiki Markdown Processing]]** — Primary LLM service used for content extraction and generation.

## Related Entities

- **[[Docker]]** — co-mentioned in source (Tool)
- **[[Python Watchdog Library]]** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Auto-ingest Pipeline Built and Docs Updated]] — where this entity was mentioned
- [[Copilot Session Checkpoint: Pipeline Enhancements and Vision Support Deployed]] — additional source
