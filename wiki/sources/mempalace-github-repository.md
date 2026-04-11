---
title: "MemPalace GitHub Repository"
type: source
created: 2026-04-11
last_verified: 2026-04-11
source_hash: "101bef9011616b455e60e17998c3f1b308c5cab895c27a19c5a6f4d028ffcfb8"
sources:
  - raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md
quality_score: 100
concepts:
  - palace-memory-architecture
  - aaak-compression-dialect
  - contradiction-detection-utility
related:
  - "[[Palace Memory Architecture]]"
  - "[[AAAK Compression Dialect]]"
  - "[[Contradiction Detection Utility]]"
  - "[[MemPalace]]"
  - "[[ChromaDB]]"
  - "[[MCP (MemPalace Control Protocol)]]"
tier: hot
tags: [ai, llm, knowledge-management, retrieval, compression, memory, open-source]
---

# MemPalace GitHub Repository

## Summary

MemPalace is an open-source, local-first AI memory system that organizes conversations and project data into a navigable structure inspired by the ancient memory palace technique. It achieves state-of-the-art recall on the LongMemEval benchmark by storing raw verbatim exchanges and leveraging semantic search, rather than relying on LLM-driven summarization. The system features a hierarchical architecture (wings, rooms, closets, drawers) and an experimental AAAK compression dialect for efficient token usage.

## Key Points

- MemPalace stores all user-AI interactions verbatim, avoiding lossy summarization.
- Its palace-inspired structure (wings, rooms, halls, closets, drawers) enables efficient, context-rich retrieval.
- Achieves 96.6% recall on LongMemEval in raw mode, outperforming summary-based approaches.
- AAAK dialect is an experimental, lossy abbreviation system for token compression, not default storage.
- Runs entirely locally, requiring no cloud or API keys, and is highly adaptable.

## Concepts Extracted

- **[[Palace Memory Architecture]]** — The Palace Memory Architecture is a hierarchical, spatially-inspired system for organizing AI memory, modeled after the ancient mnemonic technique of the memory palace. It divides user-AI interactions into wings, rooms, halls, closets, and drawers, enabling efficient, context-rich retrieval and navigation of vast conversational histories.
- **[[AAAK Compression Dialect]]** — AAAK is an experimental, lossy abbreviation system designed to compress repeated entities and relationships in AI memory into fewer tokens. It is readable by any LLM without a decoder and aims to optimize context loading for large-scale, repeated data.
- **[[Contradiction Detection Utility]]** — Contradiction Detection Utility is a separate tool in MemPalace that checks assertions against stored entity facts, identifying conflicts, stale data, and attribution errors in conversational memory. It enhances reliability by dynamically validating knowledge graph claims.

## Entities Mentioned

- **[[MemPalace]]** — MemPalace is an open-source, local-first AI memory system designed to organize and retrieve conversational and project data with high fidelity. It employs a palace-inspired hierarchical structure and achieves state-of-the-art recall on the LongMemEval benchmark by storing raw verbatim exchanges and leveraging semantic search. The system is adaptable, runs entirely on the user's machine, and integrates with popular AI tools via MCP.
- **[[AAAK Compression Dialect]]** — AAAK is an experimental abbreviation system for compressing repeated entities and relationships in AI memory. It is designed for context injection in LLM workflows, trading some fidelity for token efficiency, and is readable by any LLM without a decoder.
- **[[ChromaDB]]** — ChromaDB is a vector database used by MemPalace for semantic search and storage of raw verbatim exchanges. It enables efficient retrieval of conversational and project data based on similarity and metadata filtering.
- **[[MCP (MemPalace Control Protocol)]]** — MCP is the protocol/interface that allows AI agents (Claude, ChatGPT, Gemini CLI) to interact with MemPalace, enabling automated mining, searching, and context injection. It exposes 19 tools for AI workflows.

## Notable Quotes

> "MemPalace takes a different approach: store everything, then make it findable." — README
> "The architecture (wings, rooms, closets, drawers) is real and useful, even if it's not a magical retrieval boost." — A Note from Milla & Ben
> "AAAK is a lossy abbreviation dialect for packing repeated entities into fewer tokens at scale." — README

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md` |
| Type | repo |
| Author | Milla Jovovich & Ben Sigman |
| Date | 2026-04-07 |
| URL | https://github.com/milla-jovovich/mempalace |
