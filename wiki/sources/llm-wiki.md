---
title: "LLM Wiki"
type: source
created: 2026-04-07
last_verified: 2026-04-07
source_hash: "dc3efe98ae62f23dd08acad13aba2e95287beb20b6bec2f4af0423557fe37401"
sources:
  - raw/2026-04-07-llm-wiki.md
quality_score: 0
concepts:
  - llm-wiki
  - schema-for-llm-wiki
  - ingest-operation-llm-wiki
  - query-operation-llm-wiki
  - lint-operation-llm-wiki
related:
  - "[[LLM Wiki]]"
  - "[[Schema for LLM Wiki]]"
  - "[[Ingest Operation in LLM Wiki]]"
  - "[[Query Operation in LLM Wiki]]"
  - "[[Lint Operation in LLM Wiki]]"
  - "[[Obsidian]]"
  - "[[qmd]]"
  - "[[Vannevar Bush]]"
  - "[[Memex]]"
tier: hot
tags: [query, automation, knowledge-management, history, linting, search, schema, tools, wiki, obsidian, llm, ingestion]
---

# LLM Wiki

## Summary

This document outlines a pattern for building personal knowledge bases using large language models (LLMs). The approach focuses on creating a persistent, compounding wiki of interlinked markdown files that is maintained and updated by an LLM, reducing the manual effort required for knowledge management. The system is designed to be flexible and adaptable to various use cases, such as personal development, research, and business knowledge management.

## Key Points

- The LLM Wiki approach differs from traditional Retrieval-Augmented Generation (RAG) by creating a persistent, evolving knowledge base instead of rediscovering information for every query.
- The wiki is structured into three layers: raw sources, the LLM-generated wiki, and a schema that guides the LLM's operations.
- Key operations include ingesting new sources, answering queries, and performing periodic maintenance (linting) to ensure the wiki remains accurate and useful.

## Concepts Extracted

- **[[LLM Wiki]]** — LLM Wiki is a method for building a personal knowledge base using large language models (LLMs) to create and maintain a persistent, interlinked collection of markdown files. This approach emphasizes incremental knowledge accumulation and synthesis.
- **[[Schema for LLM Wiki]]** — The schema is a configuration document that defines the structure, conventions, and workflows for the LLM Wiki. It ensures the LLM acts as a disciplined wiki maintainer.
- **[[Ingest Operation in LLM Wiki]]** — The ingest operation involves adding new sources to the LLM Wiki, where the LLM processes the content and updates the wiki accordingly.
- **[[Query Operation in LLM Wiki]]** — The query operation allows users to ask questions against the LLM Wiki and receive synthesized answers with citations.
- **[[Lint Operation in LLM Wiki]]** — The lint operation is a periodic health check for the LLM Wiki to ensure consistency, accuracy, and completeness.

## Entities Mentioned

- **[[Obsidian]]** — Obsidian is a note-taking and knowledge management application that uses markdown files and offers features like graph views, plugins, and local storage.
- **[[qmd]]** — qmd is a local search engine for markdown files that supports hybrid BM25/vector search and LLM re-ranking.
- **[[Vannevar Bush]]** — Vannevar Bush was an American engineer and inventor, best known for proposing the concept of the Memex, a personal knowledge management system.
- **[[Memex]]** — The Memex is a conceptual device proposed by Vannevar Bush in 1945 as a personal knowledge store with associative trails between documents.

## Notable Quotes

> "The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping." — Andrej Karpathy
> "The wiki stays maintained because the cost of maintenance is near zero." — Andrej Karpathy

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-07-llm-wiki.md` |
| Type | gist |
| Author | Andrej Karpathy |
| Date | Unknown |
| URL | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f |
