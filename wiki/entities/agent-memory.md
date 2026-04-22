---
title: "Agent Memory"
type: entity
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "6d3926b294fd189631a5b0192148c2460f4f4d037b2814c551620137e4a5fae8"
sources:
  - raw/2026-04-20-agents-that-remember-introducing-agent-memory.md
quality_score: 81
concepts:
  - agent-memory
related:
  - "[[Agent Memory Ingestion Pipeline]]"
  - "[[Agent Memory Retrieval Pipeline]]"
  - "[[Agents that remember: introducing Agent Memory]]"
  - "[[Cloudflare]]"
  - "[[Durable Object]]"
  - "[[Vectorize]]"
  - "[[Workers AI]]"
tier: hot
tags: [agent-memory, cloudflare, ai-agents, memory-service]
---

# Agent Memory

## Overview

Agent Memory is a managed, retrieval-based memory service for AI agents, developed by Cloudflare. It provides persistent memory by extracting, verifying, classifying, and storing information from agent conversations, enabling efficient recall without bloating the context window.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | 2026 |
| Creator | Cloudflare |
| URL | N/A |
| Status | Active |

## Relevance

Agent Memory addresses context rot and context window limitations in agent workflows, offering durable, scalable, and exportable memory for production workloads. It integrates with Cloudflare Workers, supports bulk ingestion and direct tool use, and enables memory sharing across agents, people, and tools.

## Associated Concepts

- **Agent Memory Architecture** — Agent Memory is the practical implementation of this architecture.
- **[[Agent Memory Ingestion Pipeline]]** — Agent Memory's ingestion pipeline is central to its operation.
- **[[Agent Memory Retrieval Pipeline]]** — Agent Memory's retrieval pipeline enables efficient recall.

## Related Entities

- **[[Cloudflare]]** — Parent organization and developer.
- **[[Durable Object]]** — Storage and isolation primitive used in Agent Memory.
- **[[Vectorize]]** — Provides vector search for embedded memories.
- **[[Workers AI]]** — Runs LLMs and embedding models for extraction and synthesis.

## Sources

- [[Agents that remember: introducing Agent Memory]] — where this entity was mentioned
