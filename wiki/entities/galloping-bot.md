---
title: "Galloping-Bot"
type: entity
created: 2026-04-18
last_verified: 2026-04-26
source_hash: "047e464d50e32062c5eb82637072ff9ad4eca8476f8f0c7369fe4664be464407"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-optimizing-snipe-book-then-retry-flow-a86837aa.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-ntfy-notifications-galloping-bot-alerts-monitor--27e974be.md
  - raw/2026-04-26-copilot-session-oom-mitigation-and-follow-up-93744ca8.md
quality_score: 74
concepts:
  - galloping-bot
related:
  - "[[Ntfy Push Notifications for Service Monitoring]]"
  - "[[Copilot Session Checkpoint: ntfy Notifications, Galloping-Bot Alerts, Monitor Fixes]]"
  - "[[Ntfy]]"
  - "[[Caddy]]"
  - "[[Uptime Kuma]]"
  - "[[KnightCrawler]]"
tier: hot
tags: [automation, cron, notifications]
---

# Galloping-Bot

## Overview

Galloping-Bot is a cron-invoked containerized script that snipes golf tee time bookings. It runs once per week, logs booking confirmations, and has wrapper-side notification logic that turns its output into actionable ntfy alerts about booking success, booking failure, and wrapper-level errors.

Later operational review added another durable reliability detail: because `docker compose run` does not rebuild an existing image automatically, the wrapper now performs a cached `compose build galloping-bot` before each cron-run execution. That closes a stale-image drift path where the bot could keep running week-old code even though the cron wrapper itself was healthy.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

Galloping-Bot is a useful example of how cron reliability problems are often semantic rather than binary. The 2026-04-26 session preserved the lesson that a scheduled automation can appear operational while still executing an outdated image, so freshness guardrails sometimes belong in the wrapper script rather than only in the application code.

## Associated Concepts

- **[[Ntfy Push Notifications for Service Monitoring]]** — Notification integration

## Related Entities

- **[[Ntfy]]** — co-mentioned in source (Tool)
- **[[Caddy]]** — co-mentioned in source (Tool)
- **[[Uptime Kuma]]** — co-mentioned in source (Tool)
- **[[KnightCrawler]]** — co-mentioned in source (Tool)
- **Docker Compose** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: ntfy Notifications, Galloping-Bot Alerts, Monitor Fixes]] — where this entity was mentioned
- [[Copilot Session Checkpoint: Optimizing Snipe Book-Then-Retry Flow]] — additional source
- [[Copilot Session Checkpoint: OOM Mitigation and Follow-Up]] — records the review and push decision for the build-before-run wrapper fix
