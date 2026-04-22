---
title: "Karpathy LLM Wiki Pattern"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "26f254b5e6c65170bfc0d1bbf80f2de1aafe3266407d54a0e3243b0e1600d156"
sources:
  - raw/2026-04-07-llm-wiki.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-creating-claude-and-labs-wiki-repos-cccb14d5.md
quality_score: 83
concepts:
  - karpathy-llm-wiki-pattern
related:
  - "[[Agentic Context Engineering (ACE)]]"
  - "[[Natural Language-Driven Agent Creation]]"
  - "[[Copilot Session Checkpoint: Creating Claude and Labs-Wiki Repos]]"
tier: hot
tags: [llm-wiki, knowledge-management, karpathy-pattern, llm]
---

# Karpathy LLM Wiki Pattern

## Overview

The Karpathy LLM Wiki pattern is a structured approach to organizing and managing knowledge for large language models, emphasizing layered content management and efficient context usage. It is foundational for building scalable LLM wikis without requiring complex vector databases at moderate scale.

## How It Works

The Karpathy LLM Wiki pattern organizes knowledge into three distinct layers:

1. **raw/**: This layer contains immutable source documents, serving as the original input data for the wiki.
2. **wiki/**: This layer holds the LLM-compiled markdown files generated from the raw sources, effectively serving as the processed knowledge base.
3. **schema (AGENTS.md)**: This is the configuration and schema layer that defines agents, skills, and workflows interacting with the wiki.

Operations supported include:
- **Ingest**: Processing raw sources into the wiki markdown.
- **Query**: Retrieving and interacting with wiki content.
- **Lint**: Validating and maintaining wiki content quality.

Key files such as `index.md` provide a content catalog, while `log.md` maintains a chronological audit trail of changes. The pattern leverages Obsidian as a frontend for viewing and editing, with the LLM acting as the 'programmer' and the wiki as the 'codebase'.

A notable design choice is avoiding vector databases for moderate scale (<100 sources), relying instead on the `index.md` for efficient indexing and retrieval. This reduces complexity and resource requirements while maintaining effective knowledge management.

This pattern supports incremental compilation and modular knowledge updates, enabling scalable and maintainable LLM wiki systems.

## Key Properties

- **Layered Architecture:** Separates raw sources, compiled wiki markdown, and agent schema for modularity and clarity.
- **Operations:** Supports ingest, query, and lint operations to manage wiki lifecycle.
- **Indexing:** Uses a content catalog (index.md) instead of vector DB for moderate scale.
- **Frontend Integration:** Uses Obsidian for user-friendly viewing and editing.

## Limitations

The pattern is optimized for moderate scale and may not perform efficiently beyond ~100 source documents without integrating vector-based retrieval. It assumes a relatively static source base and may require additional mechanisms for real-time updates or large-scale semantic search.

## Example

A typical Karpathy LLM Wiki setup would have a directory structure:

```
raw/          # Immutable source files
wiki/         # Compiled markdown files
AGENTS.md     # Agent and skill schema
index.md      # Content catalog
log.md        # Change audit trail
```

An ingest operation reads raw files, compiles them into markdown pages under wiki/, updates index.md, and logs changes in log.md. Queries are resolved by referencing wiki/ markdown files guided by index.md.

## Relationship to Other Concepts

- **[[Agentic Context Engineering (ACE)]]** — Karpathy's LLM Wiki pattern can be a foundation for agentic context engineering by structuring knowledge for agents.
- **[[Natural Language-Driven Agent Creation]]** — The schema layer (AGENTS.md) supports natural language-driven agent workflows.

## Practical Applications

Used to build scalable, maintainable knowledge bases for LLM-powered agents and wikis, especially when integrating with developer tools like VS Code and Copilot CLI. Enables efficient knowledge ingestion, querying, and maintenance without complex vector DB dependencies.

## Sources

- [[Copilot Session Checkpoint: Creating Claude and Labs-Wiki Repos]] — primary source for this concept
- [[LLM Wiki]] — additional source
