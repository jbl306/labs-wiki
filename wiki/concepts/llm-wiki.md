---
title: "LLM Wiki"
type: concept
created: 2026-04-07
last_verified: 2026-04-07
source_hash: "dc3efe98ae62f23dd08acad13aba2e95287beb20b6bec2f4af0423557fe37401"
sources:
  - raw/2026-04-07-llm-wiki.md
quality_score: 0
concepts:
  - llm-wiki
related:
  - "[[Retrieval-Augmented Generation]]"
  - "[[Memex]]"
  - "[[LLM Wiki]]"
tier: hot
tags: [knowledge-management, llm, wiki, automation]
---

# LLM Wiki

## Overview

LLM Wiki is a method for building a personal knowledge base using large language models (LLMs) to create and maintain a persistent, interlinked collection of markdown files. This approach emphasizes incremental knowledge accumulation and synthesis.

## How It Works

The LLM Wiki system consists of three layers: raw sources (immutable documents), the wiki (a directory of LLM-generated markdown files), and a schema (a configuration file guiding the LLM's operations). The LLM reads new sources, extracts key information, and integrates it into the wiki by creating or updating pages, maintaining cross-references, and noting contradictions. The wiki grows richer over time as new sources are added and questions are asked. Users focus on sourcing and guiding the LLM, while the LLM handles the maintenance and synthesis.

## Key Properties

- **Persistence:** The wiki is a durable and evolving artifact that accumulates knowledge over time.
- **Automation:** The LLM automates the creation, updating, and maintenance of the wiki, reducing manual effort.
- **Schema-Driven:** A schema guides the LLM in structuring the wiki and performing operations.
- **Interlinked Knowledge:** The wiki consists of interconnected pages that synthesize information from multiple sources.
- **Flexible Use Cases:** The system can be adapted for personal, research, business, and other contexts.

## Relationship to Other Concepts

- **[[Retrieval-Augmented Generation]]** — LLM Wiki is presented as an alternative to RAG for knowledge management.
- **[[Memex]]** — LLM Wiki is inspired by Vannevar Bush's vision of a personal, curated knowledge store.

## Practical Applications

Used for personal knowledge management, research, business wikis, competitive analysis, trip planning, and more, where a persistent and organized knowledge base is beneficial.

## Sources

- [[LLM Wiki]] — primary source for this concept
