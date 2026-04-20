---
title: "AdGuard"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "5d62c5ec9d154108bd891ed92b71cf061018b412b20cfcfc2b686c64b646c9e9"
sources:
  - raw/2026-04-20-copilot-session-scheduler-dns-agents-cleanup-2222559c.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-nba-ml-agents-and-homelab-fixes-646cf99a.md
quality_score: 100
concepts:
  - adguard
related:
  - "[[AdGuard Memory Out-Of-Memory (OOM) Diagnosis and Fix]]"
  - "[[Copilot Session Checkpoint: NBA-ML Agents and Homelab Fixes]]"
  - "[[Copilot CLI]]"
  - "[[KnightCrawler]]"
tier: hot
tags: [adguard, docker, homelab, network-filtering]
---

# AdGuard

## Overview

A network-level ad and tracker blocking service running as a Docker container in the homelab environment. It manages large filter lists to block unwanted content and DNS queries, configured with resource limits and restart policies to maintain uptime.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

Subject of an OOM crash diagnosis and memory limit fix during this session, critical for homelab DNS filtering functionality.

## Associated Concepts

- **[[AdGuard Memory Out-Of-Memory (OOM) Diagnosis and Fix]]** — The session resolved AdGuard container memory issues.

## Related Entities

- **NBA-ML Engine** — co-mentioned in source (Tool)
- **[[Copilot CLI]]** — co-mentioned in source (Tool)
- **[[KnightCrawler]]** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: NBA-ML Agents and Homelab Fixes]] — where this entity was mentioned
- [[Copilot Session Checkpoint: Scheduler DNS Agents Cleanup]] — additional source
