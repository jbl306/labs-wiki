---
title: "Auto-Type-Detection in API Ingest Requests"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "c4284a8516fc117385cc15ec1ab8aa86c6b6302f7cc15494065cd9252c71a0f5"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-fixing-android-share-ingest-api-bbff237c.md
quality_score: 100
concepts:
  - auto-type-detection-in-api-ingest-requests
related:
  - "[[Universal Ingest Endpoint for Flexible API Request Parsing]]"
  - "[[Copilot Session Checkpoint: Fixing Android Share Ingest API]]"
tier: hot
tags: [API Design, Heuristics, Content Classification]
---

# Auto-Type-Detection in API Ingest Requests

## Overview

Auto-type-detection is a server-side heuristic that infers the content type of an ingest request when the explicit `type` field is omitted. It improves usability by reducing required client parameters and handling ambiguous inputs gracefully.

## How It Works

When an ingest request arrives without a specified `type` field, the server inspects the `content` field to infer its type. The heuristic is simple:

- If the content string starts with the prefixes `http://` or `https://`, it is classified as a URL (`type = 'url'`).
- Otherwise, the content is classified as plain text (`type = 'text'`).

This approach leverages common URL schemes to distinguish URLs from arbitrary text without requiring clients to explicitly specify the type. It is implemented in the `_do_ingest()` function after parsing the request parameters.

This auto-detection enables clients to send minimal data and still have the server correctly interpret the content, especially useful for clients with limited ability to set custom fields or when users omit the type field by mistake.

The heuristic is intentionally simple to avoid complexity and maintain performance. It can be extended in the future to recognize other content types or patterns.

## Key Properties

- **Heuristic Rule:** Content starting with 'http://' or 'https://' → type 'url'; else 'text'.
- **Optional Type Field:** Clients may omit the `type` field; server infers it automatically.

## Limitations

The heuristic may misclassify content that looks like URLs but is not valid or vice versa. It does not handle other content types such as notes or files. Clients requiring precise typing must still specify the `type` field explicitly. The heuristic assumes UTF-8 encoded text and may fail with binary or malformed content.

## Example

Example logic snippet:

```python
if 'type' not in params or not params['type']:
    content = params.get('content', '')
    if content.startswith(('http://', 'https://')):
        params['type'] = 'url'
    else:
        params['type'] = 'text'
```

## Relationship to Other Concepts

- **[[Universal Ingest Endpoint for Flexible API Request Parsing]]** — Auto-type-detection is integrated into the universal ingest endpoint to handle missing type fields.

## Practical Applications

Auto-type-detection simplifies client implementations by reducing required parameters and improves fault tolerance in ingestion APIs. It is especially useful for mobile or scripting clients with limited parameter control. However, it should be complemented with explicit typing when possible for accuracy.

## Sources

- [[Copilot Session Checkpoint: Fixing Android Share Ingest API]] — primary source for this concept
