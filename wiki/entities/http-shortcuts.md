---
title: "HTTP Shortcuts"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "c4284a8516fc117385cc15ec1ab8aa86c6b6302f7cc15494065cd9252c71a0f5"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-fixing-android-share-ingest-api-bbff237c.md
quality_score: 100
concepts:
  - http-shortcuts
related:
  - "[[HTTP Shortcuts Android App Scripting API Quirks]]"
  - "[[Copilot Session Checkpoint: Fixing Android Share Ingest API]]"
  - "[[Labs-Wiki Ingest API]]"
tier: hot
tags: [Android, HTTP Client, Scripting]
---

# HTTP Shortcuts

## Overview

HTTP Shortcuts is an Android app that allows users to create customizable shortcuts to execute HTTP requests with scripting capabilities. It supports both regular shortcuts and scripting shortcuts, enabling automation of HTTP interactions. However, its scripting API has known limitations, including sending empty request bodies when using `sendHttpRequest()` for JSON or form-encoded data.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | http-shortcuts.rmy.ch |
| Status | Active |

## Relevance

HTTP Shortcuts is the client app involved in the reported issue where sharing URLs to the labs-wiki ingest API resulted in empty request bodies and 422 errors. Understanding its scripting API behavior was critical to diagnosing and fixing the ingestion workflow.

## Associated Concepts

- **[[HTTP Shortcuts Android App Scripting API Quirks]]** — Describes the scripting API behavior causing empty request bodies.

## Related Entities

- **[[Labs-Wiki Ingest API]]** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Fixing Android Share Ingest API]] — where this entity was mentioned
