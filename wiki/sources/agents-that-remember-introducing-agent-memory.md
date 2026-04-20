---
title: "Agents that remember: introducing Agent Memory"
type: source
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "ff2f3f0e50ba800ba4152364d06f58e56c64b711b9e147a7fd61c9a75dfb1a8a"
sources:
  - raw/2026-04-20-agents-that-remember-introducing-agent-memory.md
quality_score: 100
concepts:
  - agent-memory-ingestion-pipeline
  - agent-memory-retrieval-pipeline
  - memory-supersession-chains
  - hybrid-retrieval-agent-memory-systems
related:
  - "[[Agent Memory Ingestion Pipeline]]"
  - "[[Agent Memory Retrieval Pipeline]]"
  - "[[Memory Supersession Chains]]"
  - "[[Hybrid Retrieval in Agent Memory Systems]]"
  - "[[Agent Memory]]"
  - "[[Cloudflare]]"
  - "[[Durable Object]]"
  - "[[Vectorize]]"
  - "[[Workers AI]]"
tier: hot
knowledge_state: validated
tags: [persistent-memory, cloudflare, agent-memory, hybrid-retrieval, AI-agents, supersession, retrieval]
---

# Agents that remember: introducing Agent Memory

## Summary

This article introduces Agent Memory, a managed service by Cloudflare that provides persistent, retrieval-based memory for AI agents. It details the architecture, ingestion and retrieval pipelines, practical use cases, and the rationale behind design choices, emphasizing production readiness and data portability. The post also discusses integration with Cloudflare's platform and highlights the challenges and solutions in agentic memory systems.

## Key Points

- Agent Memory solves context rot and persistent recall for AI agents by extracting, storing, and retrieving relevant information outside the context window.
- The system uses deterministic ID generation, multi-stage extraction, verification, classification, and a hybrid retrieval pipeline fused with Reciprocal Rank Fusion.
- It is designed for production workloads, supports bulk ingestion at compaction, direct tool use, and ensures data portability and isolation.

## Concepts Extracted

- **[[Agent Memory Ingestion Pipeline]]** — The Agent Memory ingestion pipeline is a multi-stage process that extracts, verifies, classifies, and stores memories from agent conversations. It ensures persistent, deduplicated, and structured memory storage for future retrieval, addressing context rot and information loss during context compaction.
- **[[Agent Memory Retrieval Pipeline]]** — The retrieval pipeline in Agent Memory is a hybrid, multi-channel system that surfaces relevant memories by fusing results from full-text, vector, fact-key, and hypothetical document embedding searches. It ensures robust recall for diverse query types and synthesizes natural-language answers.
- **[[Memory Supersession Chains]]** — Memory supersession chains are versioned links between memories in Agent Memory, ensuring that updates to facts or instructions create forward pointers from old to new memories. This enables durable, traceable knowledge evolution and prevents deletion of historical context.
- **[[Hybrid Retrieval in Agent Memory Systems]]** — Hybrid retrieval combines multiple search modalities—full-text, vector, fact-key, and hypothetical document embedding—to maximize recall accuracy and robustness in agent memory systems. It addresses the limitations of single-method retrieval and supports diverse query types.

## Entities Mentioned

- **[[Agent Memory]]** — Agent Memory is a managed service by Cloudflare that provides persistent, retrieval-based memory for AI agents. It extracts, stores, and retrieves relevant information from agent conversations, enabling durable recall and smarter agents over time. The service integrates with Cloudflare Workers and exposes a REST API for external agents.
- **[[Cloudflare]]** — Cloudflare is a connectivity cloud platform providing infrastructure, security, and developer tools for Internet-scale applications. It hosts Agent Memory and offers primitives like Durable Objects, Vectorize, and Workers AI for building agentic memory systems.
- **[[Durable Object]]** — Durable Object is a Cloudflare infrastructure primitive providing isolated, SQLite-backed storage for agent memory profiles. It supports FTS indexing, supersession chains, and transactional writes, ensuring strong tenant isolation.
- **[[Vectorize]]** — Vectorize is a Cloudflare infrastructure primitive providing vector search capabilities for embedded memories in Agent Memory. It stores and indexes memory embeddings for efficient semantic recall.
- **[[Workers AI]]** — Workers AI is a Cloudflare infrastructure primitive running LLMs and embedding models for Agent Memory. It supports extraction, classification, and synthesis pipelines, with session affinity for prompt caching.

## Notable Quotes

> "It gives AI agents persistent memory, allowing them to recall what matters, forget what doesn't, and get smarter over time." — Tyson Trautmann, Rob Sutter
> "The primary agent should never burn context on storage strategy. The tool surface it sees is deliberately constrained so that memory stays out of the way of the actual task." — Tyson Trautmann, Rob Sutter
> "Agent Memory is a managed service, but your data is yours. Every memory is exportable, and we're committed to making sure the knowledge your agents accumulate on Cloudflare can leave with you if your needs change." — Tyson Trautmann, Rob Sutter

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-20-agents-that-remember-introducing-agent-memory.md` |
| Type | article |
| Author | Tyson Trautmann, Rob Sutter |
| Date | 2026-04-17 |
| URL | https://blog.cloudflare.com/introducing-agent-memory/ |
