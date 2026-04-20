---
title: "Caddy"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "047e464d50e32062c5eb82637072ff9ad4eca8476f8f0c7369fe4664be464407"
sources:
  - raw/2026-04-18-copilot-session-knightcrawler-done-routing-traced-7bbbddcd.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-resource-optimization-opencode-bash-fix-c00d8543.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-ntfy-notifications-galloping-bot-alerts-monitor--27e974be.md
quality_score: 100
concepts:
  - caddy
related:
  - "[[Caddy handle_path Directive and URL Token Injection]]"
  - "[[Copilot Session Checkpoint: ntfy Notifications, Galloping-Bot Alerts, Monitor Fixes]]"
  - "[[Ntfy]]"
  - "[[Uptime Kuma]]"
  - "[[KnightCrawler]]"
  - "[[Galloping-Bot]]"
tier: hot
tags: [web-server, proxy, routing]
---

# Caddy

## Overview

Caddy is a modern, general-purpose web server known for automatic HTTPS, easy configuration, and powerful routing capabilities. The `handle_path` directive allows matching and stripping URL path prefixes before proxying requests upstream. This feature is leveraged in the homelab to gate access to services like KnightCrawler via tokenized URL prefixes.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | https://caddyserver.com |
| Status | Active |

## Relevance

Caddy's path handling and proxying features are critical for secure and flexible routing in containerized homelab environments, but require careful handling of URL rewriting to avoid access errors.

## Associated Concepts

- **[[Caddy handle_path Directive and URL Token Injection]]** — Core proxy behavior and fix

## Related Entities

- **[[Ntfy]]** — co-mentioned in source (Tool)
- **[[Uptime Kuma]]** — co-mentioned in source (Tool)
- **[[KnightCrawler]]** — co-mentioned in source (Tool)
- **[[Galloping-Bot]]** — co-mentioned in source (Tool)
- **Docker Compose** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: ntfy Notifications, Galloping-Bot Alerts, Monitor Fixes]] — where this entity was mentioned
- [[Copilot Session Checkpoint: Resource Optimization, Opencode Bash Fix]] — additional source
- [[Copilot Session Checkpoint: Knightcrawler done, routing traced]] — additional source
