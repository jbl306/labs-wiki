---
title: "Copilot Session Checkpoint: Fixing Android Share Ingest API"
type: source
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "c4284a8516fc117385cc15ec1ab8aa86c6b6302f7cc15494065cd9252c71a0f5"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-fixing-android-share-ingest-api-bbff237c.md
quality_score: 100
concepts:
  - universal-ingest-endpoint-for-flexible-api-request-parsing
  - http-shortcuts-android-app-scripting-api-quirks
  - auto-type-detection-in-api-ingest-requests
related:
  - "[[Universal Ingest Endpoint for Flexible API Request Parsing]]"
  - "[[HTTP Shortcuts Android App Scripting API Quirks]]"
  - "[[Auto-Type-Detection in API Ingest Requests]]"
  - "[[HTTP Shortcuts]]"
  - "[[Labs-Wiki Ingest API]]"
tier: hot
tags: [labs-wiki, Server-Side, Android, fileback, checkpoint, copilot-session, API, homelab, Debugging, HTTP Shortcuts, Ingest, durable-knowledge]
---

# Copilot Session Checkpoint: Fixing Android Share Ingest API

## Summary

This session checkpoint documents the debugging and resolution process for a 422 Unprocessable Entity error encountered when sharing URLs from the Android HTTP Shortcuts app to the labs-wiki ingest API. The investigation revealed quirks in the HTTP Shortcuts scripting API's request body handling, leading to server-side improvements including a universal ingest endpoint, auto-type-detection, and enhanced debug logging. Ultimately, the user discovered they had been using the wrong share button, and the original scripting shortcut approach was restored with the backend improvements retained.

## Key Points

- Initial 422 error caused by HTTP Shortcuts sending empty request bodies, incompatible with JSON Pydantic model expectations.
- Server-side fix introduced a universal ingest endpoint handling query params, JSON, form-encoded, and raw body formats with auto-type-detection.
- Debug endpoint and verbose logging were added to diagnose request contents and assist troubleshooting.
- User error (clicking wrong share button) was the root cause; original scripting shortcut method was restored in docs.
- Backend improvements remain deployed for robustness and future debugging.

## Concepts Extracted

- **[[Universal Ingest Endpoint for Flexible API Request Parsing]]** — A universal ingest endpoint is designed to robustly handle multiple request body formats for an API that ingests shared content. This approach addresses client-side inconsistencies and limitations by sequentially attempting to parse query parameters, JSON bodies, form-encoded data, and raw body content, providing graceful fallback and auto-type detection.
- **[[HTTP Shortcuts Android App Scripting API Quirks]]** — The HTTP Shortcuts Android app provides scripting capabilities to automate HTTP requests, but its scripting API exhibits a known quirk where the `sendHttpRequest()` function sends empty request bodies for both JSON and form-encoded data. This behavior complicates integration with APIs expecting structured request bodies.
- **[[Auto-Type-Detection in API Ingest Requests]]** — Auto-type-detection is a server-side heuristic that infers the content type of an ingest request when the explicit `type` field is omitted. It improves usability by reducing required client parameters and handling ambiguous inputs gracefully.

## Entities Mentioned

- **[[HTTP Shortcuts]]** — HTTP Shortcuts is an Android app that allows users to create customizable shortcuts to execute HTTP requests with scripting capabilities. It supports both regular shortcuts and scripting shortcuts, enabling automation of HTTP interactions. However, its scripting API has known limitations, including sending empty request bodies when using `sendHttpRequest()` for JSON or form-encoded data.
- **[[Labs-Wiki Ingest API]]** — The labs-wiki ingest API is a server-side service that accepts shared content from various clients, including Android apps, for automatic wiki page creation. It originally expected JSON Pydantic model bodies but was enhanced with a universal ingest endpoint to handle multiple input formats and auto-type-detection. It includes debug endpoints and verbose logging to facilitate troubleshooting.

## Notable Quotes

> ""HTTP Shortcuts `sendHttpRequest()` body behavior: Both JSON and form-encoded bodies arrive as completely empty (`body_len=0`). This is a known quirk of the scripting API."" — Durable Session Summary
> ""If `type` field is omitted, server checks if content starts with `http://` or `https://` → 'url', else → 'text'"" — Technical Details

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-fixing-android-share-ingest-api-bbff237c.md` |
| Type | note |
| Author | Unknown |
| Date | 2026-04-18T03:23:51.483387Z |
| URL | N/A |
