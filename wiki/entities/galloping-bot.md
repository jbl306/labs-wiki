---
title: "Galloping-Bot"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "047e464d50e32062c5eb82637072ff9ad4eca8476f8f0c7369fe4664be464407"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-optimizing-snipe-book-then-retry-flow-a86837aa.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-ntfy-notifications-galloping-bot-alerts-monitor--27e974be.md
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

Galloping-Bot is a cron-invoked containerized script that snipes golf tee time bookings. It runs once per week and logs booking confirmations. The bot's output is captured and parsed to send ntfy notifications with booking results and error alerts, enabling real-time operational awareness.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

Galloping-Bot automation benefits from ntfy notifications to provide immediate feedback on booking success or failure, improving user responsiveness.

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
