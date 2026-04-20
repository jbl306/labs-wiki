---
title: "Agents that remember: introducing Agent Memory"
type: source
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "6d3926b294fd189631a5b0192148c2460f4f4d037b2814c551620137e4a5fae8"
sources:
  - raw/2026-04-20-agents-that-remember-introducing-agent-memory.md
quality_score: 100
concepts:
  - agent-memory-architecture
  - agent-memory-ingestion-pipeline
  - agent-memory-retrieval-pipeline
related:
  - "[[Agent Memory Ingestion Pipeline]]"
  - "[[Agent Memory Retrieval Pipeline]]"
  - "[[Agent Memory]]"
  - "[[Cloudflare]]"
  - "[[Durable Object]]"
  - "[[Vectorize]]"
  - "[[Workers AI]]"
tier: hot
tags: [context-management, ai-agents, cloudflare, retrieval, memory-architecture, agent-memory]
---

# Agents that remember: introducing Agent Memory

## Summary

Cloudflare introduces Agent Memory, a managed service that provides persistent, retrieval-based memory for AI agents. The service addresses context rot and the limitations of context window size by extracting, verifying, and storing memories from agent conversations, enabling agents to recall relevant information without bloating context. Agent Memory integrates tightly with agent harnesses, supports bulk ingestion and direct tool use, and is designed for production workloads requiring durable, scalable, and exportable memory.

## Key Points

- Agent Memory is a managed, opinionated, retrieval-based memory service for AI agents.
- It solves context rot and context window limitations by extracting and storing memories outside the agent's main context.
- The ingestion and retrieval pipelines use deterministic ID generation, multi-stage extraction, verification, classification, and multi-channel retrieval with reciprocal rank fusion.

## Concepts Extracted

- **Agent Memory Architecture** — Agent Memory is a managed service that provides persistent, retrieval-based memory for AI agents, addressing the challenges of context rot and context window limitations. Its architecture is designed to extract, verify, classify, and store memories from agent conversations, enabling efficient recall without bloating the agent's context.
- **[[Agent Memory Ingestion Pipeline]]** — The ingestion pipeline in Agent Memory is responsible for extracting, verifying, classifying, and storing memories from agent conversations. It ensures that relevant information is persistently captured, deduplicated, and structured for efficient retrieval.
- **[[Agent Memory Retrieval Pipeline]]** — The retrieval pipeline in Agent Memory enables agents to recall relevant memories efficiently by fusing results from multiple retrieval channels. It combines query analysis, embedding, and reciprocal rank fusion to synthesize natural-language answers to agent queries.

## Entities Mentioned

- **[[Agent Memory]]** — Agent Memory is a managed, retrieval-based memory service for AI agents, developed by Cloudflare. It provides persistent memory by extracting, verifying, classifying, and storing information from agent conversations, enabling efficient recall without bloating the context window.
- **[[Cloudflare]]** — Cloudflare is a global connectivity cloud platform that protects corporate networks, accelerates web applications, and provides infrastructure for AI agent development. It offers primitives like Durable Objects, Vectorize, and Workers AI, enabling rapid prototyping and production deployment of services like Agent Memory.
- **[[Durable Object]]** — Durable Object is a Cloudflare primitive providing isolated, scalable storage for agent memory profiles. Each memory profile is mapped to its own Durable Object instance, backed by SQLite, ensuring strong tenant isolation and transactional writes.
- **[[Vectorize]]** — Vectorize is a Cloudflare primitive providing vector search over embedded memories in Agent Memory. It enables semantic retrieval by indexing memory embeddings and supporting upserts and deletions for superseded memories.
- **[[Workers AI]]** — Workers AI is a Cloudflare primitive for running LLMs and embedding models used in Agent Memory. It supports local model inference for extraction, verification, classification, and synthesis tasks within the memory pipeline.

## Notable Quotes

> "Agent Memory gives AI agents persistent memory, allowing them to recall what matters, forget what doesn't, and get smarter over time." — Tyson Trautmann, Rob Sutter
> "The critical moment in an agent’s context lifecycle is compaction, when the harness decides to shorten context to stay within a model's limits or to avoid context rot. Today, most agents discard information permanently. Agent Memory preserves knowledge on compaction instead of losing it." — Tyson Trautmann, Rob Sutter

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-20-agents-that-remember-introducing-agent-memory.md` |
| Type | article |
| Author | Tyson Trautmann, Rob Sutter |
| Date | 2026-04-17 |
| URL | https://blog.cloudflare.com/introducing-agent-memory/ |
