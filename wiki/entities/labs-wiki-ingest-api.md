---
title: "Labs-Wiki Ingest API"
type: entity
created: 2026-04-18
last_verified: 2026-04-22
source_hash: "c4284a8516fc117385cc15ec1ab8aa86c6b6302f7cc15494065cd9252c71a0f5"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-fixing-android-share-ingest-api-bbff237c.md
quality_score: 63
concepts:
  - labs-wiki-ingest-api
related:
  - "[[Universal Ingest Endpoint for Flexible API Request Parsing]]"
  - "[[Auto-Type-Detection in API Ingest Requests]]"
  - "[[Copilot Session Checkpoint: Fixing Android Share Ingest API]]"
  - "[[HTTP Shortcuts]]"
tier: hot
tags: [API, Wiki, Content Ingestion]
---

# Labs-Wiki Ingest API

## Overview

The labs-wiki ingest API is a server-side service that accepts shared content from various clients, including Android apps, for automatic wiki page creation. It originally expected JSON Pydantic model bodies but was enhanced with a universal ingest endpoint to handle multiple input formats and auto-type-detection. It includes debug endpoints and verbose logging to facilitate troubleshooting.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

The ingest API is the backend service that was fixed and improved during this session to handle Android share requests robustly despite client quirks. It is central to the labs-wiki content ingestion workflow.

## Associated Concepts

- **[[Universal Ingest Endpoint for Flexible API Request Parsing]]** — The ingest API was refactored to include this endpoint.
- **[[Auto-Type-Detection in API Ingest Requests]]** — Implemented within the ingest API for content type inference.

## Related Entities

- **[[HTTP Shortcuts]]** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Fixing Android Share Ingest API]] — where this entity was mentioned
