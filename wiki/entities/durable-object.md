---
title: "Durable Object"
type: entity
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "6d3926b294fd189631a5b0192148c2460f4f4d037b2814c551620137e4a5fae8"
sources:
  - raw/2026-04-20-agents-that-remember-introducing-agent-memory.md
quality_score: 100
concepts:
  - durable-object
related:
  - "[[Agents that remember: introducing Agent Memory]]"
  - "[[Agent Memory]]"
  - "[[Cloudflare]]"
  - "[[Vectorize]]"
  - "[[Workers AI]]"
tier: hot
tags: [durable-object, storage, isolation, cloudflare]
---

# Durable Object

## Overview

Durable Object is a Cloudflare primitive providing isolated, scalable storage for agent memory profiles. Each memory profile is mapped to its own Durable Object instance, backed by SQLite, ensuring strong tenant isolation and transactional writes.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Cloudflare |
| URL | N/A |
| Status | Active |

## Relevance

Durable Objects enable Agent Memory to scale efficiently, isolate memory profiles, and maintain transactional integrity. They handle FTS indexing, supersession chains, and ensure sensitive memories are strongly separated between tenants.

## Associated Concepts

- **Agent Memory Architecture** — Durable Objects are the storage and isolation layer.

## Related Entities

- **[[Agent Memory]]** — Uses Durable Objects for memory profile storage.
- **[[Cloudflare]]** — Developer and provider.
- **[[Vectorize]]** — co-mentioned in source (Tool)
- **[[Workers AI]]** — co-mentioned in source (Tool)

## Sources

- [[Agents that remember: introducing Agent Memory]] — where this entity was mentioned
