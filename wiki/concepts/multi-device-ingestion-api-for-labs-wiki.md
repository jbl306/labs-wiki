---
title: "Multi-Device Ingestion API for Labs-Wiki"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "bed95bb11bf69d800c6655091a905351b08f9bbfd77b74c912c1ee646e703b4f"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-full-labs-wiki-implementation-complete-22f8c487.md
quality_score: 67
concepts:
  - multi-device-ingestion-api-for-labs-wiki
related:
  - "[[Auto-Ingest Pipeline for Wiki Markdown Processing]]"
  - "[[Universal Ingest Endpoint for Flexible API Request Parsing]]"
  - "[[Copilot Session Checkpoint: Full Labs-Wiki Implementation Complete]]"
tier: hot
tags: [Ingestion API, FastAPI, Multi-Device Capture, Security, Notifications]
---

# Multi-Device Ingestion API for Labs-Wiki

## Overview

The multi-device ingestion API is a FastAPI-based service designed to centralize and secure knowledge capture from diverse sources including iOS, Android, browsers, CLI tools, and GitHub issues. It supports JSON and multipart file uploads with authentication, sanitization, and notification features to ensure robust and safe ingestion into the labs-wiki system.

## How It Works

The ingestion API is implemented in a FastAPI application (`app.py`) with the following features:

- **Endpoints:**
  - `/health`: Simple health check endpoint.
  - `/api/ingest`: Accepts JSON payloads containing source data.
  - `/api/ingest/file`: Accepts multipart file uploads.

- **Authentication:** Uses bearer token authentication with the token provided via the `WIKI_API_TOKEN` environment variable.

- **Security Measures:**
  - Filename sanitization using regex and `Path.name` to prevent path traversal attacks.
  - File size limits of 15MB enforced both by file size and content length checks.

- **Frontmatter Generation:** Generates SHA-256 hash-based frontmatter metadata for each ingested source to ensure immutability and traceability.

- **Notifications:** Integrates with ntfy.sh for non-blocking notifications on capture events; failures in notification do not block ingestion.

- **Deployment:** The API is containerized with a Dockerfile for easy deployment, though deployment to the user's homelab server is pending.

This API enables seamless capture of knowledge from multiple devices and platforms into a centralized ingestion hub, facilitating consistent and secure updates to the labs-wiki knowledge base.

## Key Properties

- **FastAPI Framework:** Lightweight, asynchronous Python web framework enabling high-performance API endpoints.
- **Bearer Token Authentication:** Secures API access using tokens stored in environment variables.
- **Filename Sanitization:** Prevents directory traversal and injection attacks by strict filename validation.
- **File Size Limit:** 15MB maximum file size enforced to prevent resource exhaustion.
- **Notification Integration:** Non-blocking ntfy notifications on successful captures.

## Limitations

The 15MB file size limit may restrict ingestion of very large documents or datasets. The API currently requires manual deployment and configuration in the user's homelab environment. Notification failures do not block ingestion but may lead to missed alerts. Authentication relies on a single token, which may not support fine-grained access control or multi-user scenarios.

## Example

Example curl command to upload a file:

```bash
curl -X POST \
  -H "Authorization: Bearer $WIKI_API_TOKEN" \
  -F "file=@mydoc.md" \
  http://localhost/api/ingest/file
```

Example JSON payload for `/api/ingest`:

```json
{
  "title": "Example Source",
  "content": "This is the content of the source document.",
  "tags": ["example", "test"]
}
```

Response includes status and generated hash metadata.

## Visual

No images included; the source code file `app.py` contains endpoint definitions and middleware for authentication, file handling, and notification logic.

## Relationship to Other Concepts

- **[[Auto-Ingest Pipeline for Wiki Markdown Processing]]** — Related concept for automated ingestion and processing of markdown wiki content
- **[[Universal Ingest Endpoint for Flexible API Request Parsing]]** — Shares design goals of flexible and secure ingestion APIs

## Practical Applications

This ingestion API enables users to capture knowledge from multiple devices and platforms into a centralized wiki system, supporting workflows where knowledge is generated or collected in diverse environments. It is suitable for personal knowledge management, research data capture, and collaborative documentation systems requiring secure, authenticated, and scalable ingestion.

## Sources

- [[Copilot Session Checkpoint: Full Labs-Wiki Implementation Complete]] — primary source for this concept
