---
title: "Universal Ingest Endpoint for Flexible API Request Parsing"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "c4284a8516fc117385cc15ec1ab8aa86c6b6302f7cc15494065cd9252c71a0f5"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-fixing-android-share-ingest-api-bbff237c.md
quality_score: 100
concepts:
  - universal-ingest-endpoint-for-flexible-api-request-parsing
related:
  - "[[Copilot Session Checkpoint: Fixing Android Share Ingest API]]"
tier: hot
tags: [API Design, Request Parsing, Robustness, Debugging]
---

# Universal Ingest Endpoint for Flexible API Request Parsing

## Overview

A universal ingest endpoint is designed to robustly handle multiple request body formats for an API that ingests shared content. This approach addresses client-side inconsistencies and limitations by sequentially attempting to parse query parameters, JSON bodies, form-encoded data, and raw body content, providing graceful fallback and auto-type detection.

## How It Works

The universal ingest endpoint consolidates multiple ingestion routes into a single handler that attempts to parse incoming requests in a prioritized manner:

1. **Query Parameters Parsing:** The handler first checks if the required fields (`type`, `content`, `title`, `source`) are present as query parameters in the URL. This is the simplest and most direct method.

2. **JSON Body Parsing:** If query parameters are absent or incomplete, the handler attempts to parse the request body as JSON. This is the preferred format for structured data and aligns with the original Pydantic model expectations.

3. **Form-Encoded Body Parsing:** If JSON parsing fails or the body is empty, the handler tries to parse form-encoded data, which is common in HTML form submissions.

4. **Raw Body Fallback:** If all above fail, the handler treats the raw body as plain text content.

After extracting the content, the endpoint performs **auto-type-detection**: if the `type` field is missing, it inspects the content string to determine if it starts with "http://" or "https://" to classify it as a URL; otherwise, it defaults to text. This flexible parsing strategy ensures compatibility with diverse client behaviors, especially those with quirks like HTTP Shortcuts.

The endpoint also includes detailed debug logging for every ingest request, capturing method, URL, headers, and parsed parameters to facilitate troubleshooting. Additionally, a dedicated `/api/debug` endpoint returns a full dump of the incoming request for inspection without authentication requirements.

This design improves robustness by handling edge cases where clients send empty or malformed bodies, enabling seamless ingestion from various sources without client-side changes.

## Key Properties

- **Parsing Priority:** Query parameters → JSON body → form-encoded body → raw body fallback.
- **Auto-Type-Detection:** If `type` is omitted, content starting with 'http://' or 'https://' is classified as 'url'; otherwise 'text'.
- **Debug Logging:** Verbose logging on all ingest requests with method, URL, headers, and parsed parameters.
- **Debug Endpoint:** Unauthenticated `/api/debug` endpoint returns full request dump for troubleshooting.

## Limitations

The universal parser assumes that query parameters or body content can be meaningfully parsed in one of the supported formats; malformed or ambiguous inputs may still cause ingestion errors. Auto-type-detection is heuristic and may misclassify content that looks like URLs but is not, or vice versa. The debug endpoint exposes full request data without authentication, which may be a security risk if deployed in production environments without access controls.

## Example

Pseudocode for the universal parser:

```python
async def parse_ingest_params(request):
    # Try query params
    params = extract_query_params(request)
    if valid(params):
        return params

    # Try JSON body
    try:
        json_body = await request.json()
        if valid(json_body):
            return json_body
    except:
        pass

    # Try form-encoded
    form_body = await request.form()
    if valid(form_body):
        return form_body

    # Fallback to raw body
    raw_body = await request.body()
    return {'content': raw_body.decode('utf-8')}

# Auto-type-detection
if 'type' not in params:
    if params['content'].startswith(('http://', 'https://')):
        params['type'] = 'url'
    else:
        params['type'] = 'text'
```

## Relationship to Other Concepts

- **Auto-Type-Detection in API Ingest** — Auto-type-detection is implemented within the universal ingest endpoint to infer content type.
- **Debug Endpoint for API Request Inspection** — The debug endpoint complements the universal parser by providing raw request dumps for troubleshooting.

## Practical Applications

This universal ingest endpoint design is applicable in any API that must accept data from diverse clients with varying request formats and quirks, such as mobile apps with scripting limitations or third-party integrations. It improves robustness and reduces client-side requirements by handling multiple input formats server-side. The debug endpoint aids developers and operators in diagnosing ingestion issues without requiring client-side changes or complex logging setups.

## Sources

- [[Copilot Session Checkpoint: Fixing Android Share Ingest API]] — primary source for this concept
