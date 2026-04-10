---
title: "LLM Wiki"
type: source
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "dc3efe98ae62f23dd08acad13aba2e95287beb20b6bec2f4af0423557fe37401"
sources:
  - raw/2026-04-07-llm-wiki.md
quality_score: 100
concepts:
  - llm-maintained-persistent-wiki-pattern
  - llm-wiki-architecture
related:
  - "[[LLM-Maintained Persistent Wiki Pattern]]"
  - "[[LLM Wiki Architecture]]"
  - "[[Obsidian]]"
  - "[[qmd]]"
  - "[[Obsidian Web Clipper]]"
  - "[[Marp]]"
  - "[[Dataview]]"
tier: hot
tags: [wiki, obsidian, knowledge-base, llm, personal-knowledge-management, automation]
---

# LLM Wiki

## Summary

This gist outlines a pattern for building personal knowledge bases using LLMs, where the LLM incrementally maintains a persistent, interlinked wiki from raw sources. The approach contrasts with traditional RAG systems by emphasizing knowledge accumulation and maintenance, allowing the wiki to grow richer and more useful over time. The document details the architecture, operations, and practical tips for implementing such a system, focusing on workflow, tooling, and the division of labor between human and LLM.

## Key Points

- LLMs can maintain a persistent, evolving wiki that compiles and organizes knowledge from raw sources.
- The system consists of three layers: raw sources, the wiki, and the schema guiding LLM behavior.
- Operations include ingesting sources, querying the wiki, periodic linting, and leveraging indexing and logging for navigation and history.

## Concepts Extracted

- **[[LLM-Maintained Persistent Wiki Pattern]]** — The LLM-maintained persistent wiki pattern is an approach to building personal or organizational knowledge bases where a large language model (LLM) incrementally constructs, updates, and maintains a structured, interlinked wiki from raw source documents. Unlike traditional retrieval-augmented generation (RAG) systems, this pattern focuses on knowledge accumulation, synthesis, and maintenance, enabling the wiki to become richer and more useful over time.
- **[[LLM Wiki Architecture]]** — The LLM Wiki Architecture defines the structural layers and operational workflow for building and maintaining a persistent knowledge base using LLMs. It delineates the roles of raw sources, the wiki, and the schema, ensuring clarity, modularity, and scalability.

## Entities Mentioned

- **[[Obsidian]]** — Obsidian is a markdown-based knowledge management tool that enables users to organize, link, and visualize notes and documents. It supports plugins for enhanced functionality, including graph view, slide deck generation, and dynamic querying.
- **[[qmd]]** — qmd is a local search engine for markdown files, supporting hybrid BM25/vector search and LLM re-ranking. It operates on-device and offers both CLI and MCP server interfaces.
- **[[Obsidian Web Clipper]]** — Obsidian Web Clipper is a browser extension that converts web articles to markdown, facilitating rapid source ingestion into the knowledge base.
- **[[Marp]]** — Marp is a markdown-based slide deck format, with an Obsidian plugin for generating presentations directly from wiki content.
- **[[Dataview]]** — Dataview is an Obsidian plugin that runs queries over page frontmatter, generating dynamic tables and lists based on metadata.

## Notable Quotes

> "The wiki is a persistent, compounding artifact. The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read." — Andrej Karpathy
> "The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping. LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass." — Andrej Karpathy

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-07-llm-wiki.md` |
| Type | gist |
| Author | Andrej Karpathy |
| Date | Unknown |
| URL | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f |
