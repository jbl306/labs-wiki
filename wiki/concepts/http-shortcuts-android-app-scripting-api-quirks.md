---
title: "HTTP Shortcuts Android App Scripting API Quirks"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "c4284a8516fc117385cc15ec1ab8aa86c6b6302f7cc15494065cd9252c71a0f5"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-fixing-android-share-ingest-api-bbff237c.md
quality_score: 72
concepts:
  - http-shortcuts-android-app-scripting-api-quirks
related:
  - "[[Universal Ingest Endpoint for Flexible API Request Parsing]]"
  - "[[Copilot Session Checkpoint: Fixing Android Share Ingest API]]"
tier: hot
tags: [Android, HTTP Shortcuts, API Integration, Scripting Quirks]
---

# HTTP Shortcuts Android App Scripting API Quirks

## Overview

The HTTP Shortcuts Android app provides scripting capabilities to automate HTTP requests, but its scripting API exhibits a known quirk where the `sendHttpRequest()` function sends empty request bodies for both JSON and form-encoded data. This behavior complicates integration with APIs expecting structured request bodies.

## How It Works

HTTP Shortcuts allows users to create shortcuts that execute HTTP requests with customizable methods, headers, and bodies. The scripting API includes a `sendHttpRequest()` function intended to send HTTP requests programmatically with dynamic content.

However, when using `sendHttpRequest()` to send JSON or form-encoded bodies, the request arrives at the server with an empty body (`body_len=0`). This means that although the client script attempts to send data, the server receives no content. This quirk is documented as a limitation of the scripting API.

The built-in Regular Shortcut HTTP client in the app behaves differently and can send bodies correctly, but scripting shortcuts do not. This discrepancy leads to errors when server endpoints expect JSON bodies validated by Pydantic models or form-encoded data.

To work around this, server-side API endpoints need to accept alternative input formats such as query parameters or raw body content and implement flexible parsing logic. On the client side, users are advised to avoid JSON encoding variables in scripting shortcuts or switch to Regular Shortcuts with plain text bodies.

This quirk requires careful debugging and documentation to prevent user confusion and ensure reliable integration with the labs-wiki ingest API.

## Key Properties

- **Empty Body Behavior:** `sendHttpRequest()` sends requests with empty bodies for JSON and form-encoded data.
- **Regular Shortcut HTTP Client Difference:** Regular Shortcut client sends bodies correctly, unlike scripting API.
- **Variable Access:** `getVariable()` in scripting raises errors if variable does not exist; exact key matches are required.

## Limitations

This scripting API quirk breaks compatibility with APIs expecting structured request bodies, causing 422 errors. It forces server-side workarounds and complicates client scripting. Users may also encounter errors setting variables with non-existent values. The quirk is intrinsic to the app's scripting implementation and cannot be fixed server-side.

## Example

User script snippet illustrating the issue:

```javascript
// Scripting shortcut
sendHttpRequest({
  url: 'https://wiki-ingest.jbl-lab.com/api/ingest',
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({type: 'url', content: shared_text})
});
// Results in empty body received by server
```

Workaround: Use Regular Shortcut with `text/plain` body and `{shared_text}` placeholder instead.

## Relationship to Other Concepts

- **[[Universal Ingest Endpoint for Flexible API Request Parsing]]** — Server-side universal parser was implemented to handle empty bodies caused by this quirk.

## Practical Applications

Developers integrating Android HTTP Shortcuts scripting with APIs must be aware of this quirk and design server endpoints to accept multiple input formats or advise users to use Regular Shortcuts. Documentation should clearly explain this behavior to prevent user confusion and failed integrations.

## Sources

- [[Copilot Session Checkpoint: Fixing Android Share Ingest API]] — primary source for this concept
