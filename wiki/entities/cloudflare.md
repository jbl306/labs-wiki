---
title: "Cloudflare"
type: entity
created: 2026-04-18
last_verified: 2026-04-22
source_hash: "9087cb7649f7304dd2917525af12c2fd1f436fd5b0eb12bcf0b6c9787bb8f3f4"
sources:
  - raw/2026-04-20-agents-that-remember-introducing-agent-memory.md
  - raw/2026-04-20-cloudflare-launches-code-mode-mcp-server-to-optimize-token-u.md
  - raw/2026-04-18-copilot-session-knightcrawler-done-routing-traced-7bbbddcd.md
quality_score: 80
concepts:
  - cloudflare
related:
  - "[[Homelab Media Domain Routing: LAN and Public HTTPS Diagnostics]]"
  - "[[Copilot Session Checkpoint: Knightcrawler done, routing traced]]"
  - "[[KnightCrawler]]"
  - "[[Caddy]]"
tier: hot
tags: [dns, tls, tunnel, homelab]
---

# Cloudflare

## Overview

Cloudflare provides DNS, TLS termination, and tunnel services for the homelab environment, enabling secure public access to internal media services. It manages public DNS records and forwards HTTPS requests to the homelab's HTTP-only proxy.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | 2026 |
| Creator | Unknown |
| URL | https://blog.cloudflare.com/introducing-agent-memory/ |
| Status | Active |

## Relevance

Cloudflare is critical for enabling public HTTPS access to homelab services while allowing the internal proxy (Caddy) to remain HTTP-only. Its DNS and tunnel configuration are key to resolving LAN and public routing issues.

## Associated Concepts

- **[[Homelab Media Domain Routing: LAN and Public HTTPS Diagnostics]]** — Handles public DNS and TLS termination in the routing stack.

## Related Entities

- **[[KnightCrawler]]** — co-mentioned in source (Tool)
- **Opencode** — co-mentioned in source (Tool)
- **[[Caddy]]** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Knightcrawler done, routing traced]] — where this entity was mentioned
- [[Cloudflare Launches Code Mode MCP Server to Optimize Token Usage for AI Agents]] — additional source
- [[Agents that remember: introducing Agent Memory]] — additional source
