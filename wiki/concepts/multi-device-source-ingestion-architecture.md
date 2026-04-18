---
title: "Multi-Device Source Ingestion Architecture"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "a91441178b56106907798420bc2275beaedfb061aeaf034fb63296c7614e06f9"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-planning-and-progress-tracking-complete-d09b537d.md
quality_score: 100
concepts:
  - multi-device-source-ingestion-architecture
related:
  - "[[Copilot Session Checkpoint: Planning and Progress Tracking Complete]]"
tier: hot
tags: [multi-device-ingestion, api, knowledge-capture, fastapi, docker]
---

# Multi-Device Source Ingestion Architecture

## Overview

A system design enabling ingestion of knowledge content from multiple device platforms and input methods into a unified knowledge base. This architecture supports diverse capture channels funneling into a centralized API hub for consistent processing and storage.

## How It Works

The ingestion architecture uses a FastAPI-based API hub deployed in a Docker container orchestrated by Docker Compose (compose.wiki.yml). It exposes a single endpoint that accepts POST requests containing markdown content from various input channels.

The six supported capture channels are:

1. **iOS Shortcut:** A shortcut on iOS devices that sends selected content to the API.
2. **Android Share Sheet:** Android's native sharing mechanism to post content.
3. **Browser Bookmarklet:** A JavaScript bookmarklet that captures page content.
4. **CLI Commands:** Command-line interface commands `wa` and `waf` for quick content addition.
5. **GitHub Issues:** Label-triggered ingestion from GitHub Issues.
6. **ntfy.sh Notifications:** Integration with ntfy.sh for push notifications and content capture.

All incoming content is saved into a `raw/` directory with filenames formatted as `YYYY-MM-DD-<slug>.md`. The system uses bearer token authentication for security and is fronted by a Caddy reverse proxy enforcing resource limits (128MB memory, 0.25 CPU).

Upon ingestion, an ntfy notification is sent to alert downstream systems or users of new content availability.

This architecture centralizes diverse input methods into a consistent, secure, and scalable ingestion pipeline, enabling seamless multi-device knowledge capture.

## Key Properties

- **Centralized API Hub:** Single FastAPI endpoint for all ingestion channels, simplifying processing and storage.
- **Multi-Channel Support:** Supports iOS, Android, browser, CLI, GitHub, and ntfy.sh inputs.
- **Security:** Bearer token authentication and Caddy reverse proxy with resource limits.
- **File Storage:** Raw markdown files stored with date-stamped filenames in a raw/ directory.
- **Notification Integration:** ntfy.sh notifications sent on new content ingestion.

## Limitations

Requires proper configuration of each capture channel and secure token management. Resource limits may constrain ingestion throughput under heavy load. Reliance on external services like ntfy.sh and GitHub Issues introduces dependencies that may affect availability.

## Example

A user on Android selects text and shares it via the Android Share Sheet to the ingestion API. The API authenticates the request, saves the content as `raw/2026-04-07-android-share.md`, and sends an ntfy notification. Downstream agents detect the new file and begin processing it into the wiki.

## Relationship to Other Concepts

- **LLM-Powered Personal Knowledge Wiki Architecture** — Feeds raw content into the wiki architecture's raw layer for further processing.

## Practical Applications

Enables users to capture knowledge from any device or platform seamlessly into a centralized knowledge system. Useful for researchers, writers, and teams who work across multiple devices and want consistent, automated knowledge ingestion.

## Sources

- [[Copilot Session Checkpoint: Planning and Progress Tracking Complete]] — primary source for this concept
