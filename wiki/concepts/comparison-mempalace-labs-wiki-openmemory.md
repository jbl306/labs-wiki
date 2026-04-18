---
title: "Comparison of MemPalace, Labs-Wiki, and OpenMemory"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "2770380bae93c0904afb7c4a75ef624686ada74d9cdbacc49e9643375baa6ced"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-researching-mempalace-for-comparison-doc-50987160.md
quality_score: 100
concepts:
  - comparison-mempalace-labs-wiki-openmemory
related:
  - "[[Labs-Wiki Architecture]]"
  - "[[OpenMemory]]"
  - "[[Copilot Session Checkpoint: Researching MemPalace for Comparison Doc]]"
tier: hot
tags: [knowledge-management, personal-wiki, memory-systems, homelab]
---

# Comparison of MemPalace, Labs-Wiki, and OpenMemory

## Overview

This concept details the comparative analysis of three personal knowledge and memory systems: MemPalace, Labs-Wiki, and OpenMemory. It highlights architectural differences, storage methods, query capabilities, and use case suitability to guide integration and deployment decisions.

## How It Works

The comparison spans multiple dimensions:

- Storage:
  - MemPalace uses a combination of ChromaDB (vector DB) and SQLite (knowledge graph) locally.
  - Labs-Wiki stores compiled markdown files on disk.
  - OpenMemory uses Qdrant vector DB plus SQLite, running in Docker.

- Model and Content:
  - MemPalace stores verbatim conversational content with semantic search.
  - Labs-Wiki compiles knowledge from URLs, papers, and GitHub repos into curated wiki pages.
  - OpenMemory is a simple key-value vector memory derived from conversations.

- Query and Tools:
  - MemPalace offers 19 MCP tools for rich querying and graph traversal.
  - Labs-Wiki supports wiki page reading and index search.
  - OpenMemory provides 4 MCP tools for basic memory operations.

- Wake-Up Protocol:
  - MemPalace loads ~170 tokens (L0+L1) at wake-up.
  - Labs-Wiki has no wake-up protocol.
  - OpenMemory injects memories per query.

- Graph and Provenance:
  - MemPalace uses a temporal knowledge graph and palace navigation.
  - Labs-Wiki plans to use NetworkX for graph representation.
  - OpenMemory has no graph structure.

- Auto-Save and Quality:
  - MemPalace auto-saves every 15 messages and pre-compaction.
  - Labs-Wiki uses a Docker sidecar watching raw sources.
  - OpenMemory requires manual save calls.
  - Labs-Wiki has quality scoring and linting; MemPalace and OpenMemory do not.

- Cost and Deployment:
  - All are zero or near-zero cost, running locally or on homelab infrastructure.

User assessment concludes MemPalace excels at conversational memory, Labs-Wiki excels at knowledge compilation, and OpenMemory is the least capable. The recommendation is to keep Labs-Wiki, add MemPalace, and consider replacing OpenMemory.

## Key Properties

- **Storage Types:** MemPalace: ChromaDB + SQLite; Labs-Wiki: Markdown files; OpenMemory: Qdrant + SQLite.
- **Query Tools:** MemPalace: 19 MCP tools; Labs-Wiki: wiki read + index search; OpenMemory: 4 MCP tools.
- **Wake-Up Costs:** MemPalace: ~170 tokens; Labs-Wiki: none; OpenMemory: per-query injection.
- **Provenance and Quality:** Labs-Wiki tracks full source provenance and quality scores; MemPalace tracks source closet strings; OpenMemory tracks memory IDs only.

## Limitations

OpenMemory lacks structure and advanced querying, limiting its utility. Labs-Wiki lacks a wake-up protocol and relies on compiled knowledge, making it less suited for conversational memory. MemPalace's wake-up token cost and complexity may add overhead. Integration between systems is currently lacking, requiring development for synchronization.

## Example

Use case:
- For capturing detailed conversations and decisions, MemPalace is preferred due to verbatim storage and rich querying.
- For compiling and referencing research papers and tools, Labs-Wiki provides curated, high-quality markdown pages.
- OpenMemory can serve as a lightweight memory but lacks advanced features.

A homelab user runs Labs-Wiki for research knowledge, deploys MemPalace for conversational memory, and plans to replace OpenMemory with MemPalace for unified memory management.

## Visual

A comparison table is provided in the source showing key dimensions side-by-side: Storage, Model, Source, Query, Wake-up, Graph, Auto-save, Provenance, Quality, and Cost.

## Relationship to Other Concepts

- **MemPalace Architecture and Memory System** — One of the compared systems.
- **[[Labs-Wiki Architecture]]** — One of the compared systems.
- **[[OpenMemory]]** — One of the compared systems.

## Practical Applications

This comparison guides personal knowledge management system selection and integration in homelab environments. It informs decisions on which system to deploy for conversational memory versus knowledge compilation and how to plan migration or coexistence strategies. It also supports roadmap planning for feature integration and synchronization.

## Sources

- [[Copilot Session Checkpoint: Researching MemPalace for Comparison Doc]] — primary source for this concept
