---
title: "MemPalace GitHub Repository"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "d08a3ffff055c78ea944afe2266f216cbdf096a7a4848a8aaca92dff7205ba1d"
sources:
  - raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md
quality_score: 86
concepts:
  - mempalace-memory-system
  - closet-index-layer
  - source-adapter-plugin-specification
related:
  - "[[MemPalace Memory System]]"
  - "[[Closet Index Layer]]"
  - "[[Source Adapter Plugin Specification]]"
  - "[[MemPalace]]"
  - "[[ChromaDB]]"
tier: hot
knowledge_state: executed
tags: [semantic-search, privacy, local-first, knowledge-graph, ai-memory, extensibility, retrieval, plugin, adapter, benchmarking]
---

# MemPalace GitHub Repository

## Summary

MemPalace is a local-first, open-source AI memory system that stores conversation history and project content verbatim, enabling high-recall semantic search without cloud dependencies or API calls. It features a structured, pluggable architecture with a focus on privacy, reproducible benchmarks, and extensibility via adapters and backends. The system achieves state-of-the-art retrieval recall on public benchmarks and provides advanced features such as a knowledge graph, agent diaries, and a robust index/search pipeline.

## Key Points

- MemPalace stores all user data verbatim, never summarizing or paraphrasing, and enables scoped semantic search via a structured index (wings, rooms, drawers, closets).
- The architecture is modular: retrieval backends are pluggable (default ChromaDB), and source adapters are formalized for extensibility and privacy control.
- Benchmarks show 96.6% R@5 recall on LongMemEval (raw mode, no LLM or cloud required), with hybrid and rerank pipelines reaching up to 99%+; all results are reproducible and methodology is transparent.

## Concepts Extracted

- **[[MemPalace Memory System]]** — MemPalace is a local-first AI memory system that stores user data verbatim and enables high-recall, privacy-preserving semantic search. Its architecture is structured around the concepts of wings, rooms, drawers, and closets, supporting pluggable backends and adapters for extensibility.
- **[[Closet Index Layer]]** — Closets are the index layer in MemPalace, storing compact pointers to verbatim content drawers. They enable fast, scoped semantic search by mapping topics, entities, and quotes to their corresponding content chunks.
- **[[Source Adapter Plugin Specification]]** — The Source Adapter Plugin Specification (RFC 002) defines a formal contract for integrating new data sources into MemPalace. It enables third-party adapters to provide content for mining and retrieval, supporting extensibility, privacy, and structured metadata.

## Entities Mentioned

- **[[MemPalace]]** — MemPalace is an open-source, local-first AI memory system that stores user data verbatim and enables high-recall semantic search. It is designed around a structured architecture (wings, rooms, drawers, closets) and supports pluggable backends, privacy, and extensibility via adapters.
- **[[ChromaDB]]** — ChromaDB is the default vector-store backend used by MemPalace for semantic search and retrieval. It stores both the index layer (closets) and verbatim content chunks (drawers), supporting fast, scoped queries.

## Notable Quotes

> "MemPalace stores your conversation history as verbatim text and retrieves it with semantic search. It does not summarize, extract, or paraphrase." — README
> "100% recall is the design requirement — the target every search path is measured against. Anything less means forgetting, and forgetting means starting over." — AGENTS.md
> "The only official sources for MemPalace are this GitHub repository, the PyPI package, and the docs site at mempalaceofficial.com. Any other domain — including mempalace.tech — is an impostor and may distribute malware." — README

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md` |
| Type | repo |
| Author | Unknown |
| Date | Unknown |
| URL | https://github.com/milla-jovovich/mempalace |
