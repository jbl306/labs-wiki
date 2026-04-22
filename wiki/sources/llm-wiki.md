---
title: "LLM Wiki"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "a402e64fc0c46e618b01acc3502f18a992b4a42222bfd7f87c9abbee3801c98f"
sources:
  - raw/2026-04-07-llm-wiki.md
quality_score: 90
concepts:
  - llm-wiki-pattern
  - schema-guided-llm-knowledge-base-maintenance
  - automated-wiki-linting-contradiction-detection
related:
  - "[[Schema-Guided LLM Knowledge Base Maintenance]]"
  - "[[Obsidian]]"
  - "[[Obsidian Web Clipper]]"
  - "[[Marp]]"
  - "[[Dataview]]"
  - "[[qmd]]"
tier: hot
knowledge_state: validated
tags: [wiki, obsidian, maintenance, pattern, automation, llm, schema, knowledge-base]
---

# LLM Wiki

## Summary

This document outlines a pattern for building personal knowledge bases using LLMs, emphasizing persistent, compounding wiki artifacts rather than ephemeral retrieval. It describes the architecture, operational workflows, and practical tips for maintaining a structured, interlinked markdown wiki, with the LLM handling all maintenance and synthesis. The approach is modular and adaptable, designed to reduce human bookkeeping and leverage LLMs for scalable knowledge management.

## Key Points

- LLM Wiki pattern replaces traditional RAG workflows with persistent, evolving knowledge bases.
- Architecture consists of raw sources, LLM-generated wiki, and a schema guiding workflows.
- Operations include ingest, query, lint, indexing, and logging, with optional CLI tools for scaling.

## Concepts Extracted

- **LLM Wiki Pattern** — The LLM Wiki Pattern is a methodology for building and maintaining personal or organizational knowledge bases using large language models. Unlike traditional retrieval-augmented generation (RAG) systems, which treat source documents as static and rediscover knowledge on every query, the LLM Wiki Pattern compiles knowledge into a persistent, evolving wiki. This wiki is structured, interlinked, and maintained automatically by the LLM, enabling compounding synthesis, cross-referencing, and contradiction detection.
- **[[Schema-Guided LLM Knowledge Base Maintenance]]** — Schema-guided maintenance is a methodology where a configuration document defines the structure, conventions, and workflows for an LLM-maintained wiki. This schema acts as the operational blueprint, ensuring that the LLM follows consistent procedures for ingesting sources, updating pages, answering queries, and maintaining the knowledge base.
- **Automated Wiki Linting and Contradiction Detection** — Automated wiki linting and contradiction detection is a process where the LLM periodically audits the wiki for inconsistencies, stale claims, orphan pages, missing cross-references, and data gaps. This ensures the knowledge base remains healthy, current, and reliable, with contradictions flagged and resolved as new sources are integrated.

## Entities Mentioned

- **[[Obsidian]]** — Obsidian is a markdown-based note-taking and knowledge management tool, serving as the IDE for browsing and interacting with LLM-generated wiki content. It supports plugins for graph visualization, web clipping, slide deck generation, and dynamic querying, making it a powerful platform for personal and collaborative knowledge bases.
- **[[Obsidian Web Clipper]]** — Obsidian Web Clipper is a browser extension that converts web articles into markdown files, streamlining the ingestion of new sources into the LLM Wiki's raw collection. It supports local image downloading and integration with Obsidian's directory structure.
- **[[Marp]]** — Marp is a markdown-based slide deck format, with an Obsidian plugin that enables users to generate presentations directly from wiki content. It supports dynamic, LLM-generated slide decks for research, teaching, or business applications.
- **[[Dataview]]** — Dataview is an Obsidian plugin that runs queries over page frontmatter, generating dynamic tables and lists from wiki metadata such as tags, dates, and source counts. It enhances navigation and analysis within the LLM-maintained wiki.
- **[[qmd]]** — qmd is a local search engine for markdown files, offering hybrid BM25/vector search and LLM re-ranking. It operates on-device, with both CLI and MCP server interfaces, enabling scalable search as the wiki grows.

## Notable Quotes

> "The wiki is a persistent, compounding artifact. The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read." — LLM Wiki
> "The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping. LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass." — LLM Wiki

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-07-llm-wiki.md` |
| Type | gist |
| Author | Unknown |
| Date | Unknown |
| URL | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f |
