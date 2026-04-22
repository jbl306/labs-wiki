---
title: "LLM Wiki Architecture"
type: concept
created: 2026-04-08
last_verified: 2026-04-17
source_hash: "dc3efe98ae62f23dd08acad13aba2e95287beb20b6bec2f4af0423557fe37401"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-planning-and-progress-tracking-complete-d09b537d.md
  - raw/2026-04-07-llm-wiki.md
quality_score: 90
concepts:
  - llm-wiki-architecture
  - llm-wiki-architecture
related:
  - "[[GitHub Copilot]]"
  - "[[Custom Agents in VS Code]]"
  - "[[LLM Wiki]]"
  - "[[Palace Memory Architecture]]"
  - "[[LLM Operating System Architecture]]"
tier: established
tags: [architecture, llm, wiki, knowledge-base, schema, automation, personal-knowledge-management]
---

# LLM Wiki Architecture

## Overview

The LLM Wiki Architecture defines the structural layers and operational workflow for building and maintaining a persistent knowledge base using LLMs. It delineates the roles of raw sources, the wiki, and the schema, ensuring clarity, modularity, and scalability.

## How It Works

The architecture is composed of three primary layers:

1. **Raw Sources**: This layer consists of the original, immutable documents—articles, papers, images, and data files. These serve as the foundation for knowledge extraction and are never modified by the LLM. The integrity of the raw sources is paramount, as they represent the source of truth for the knowledge base.

2. **The Wiki**: The wiki is a directory of markdown files generated and maintained entirely by the LLM. It includes various types of pages:
   - **Summaries**: Concise overviews of sources and topics.
   - **Entity Pages**: Detailed information about people, organizations, datasets, etc.
   - **Concept Pages**: Explanations of ideas, techniques, and methodologies.
   - **Comparisons and Syntheses**: Analytical pages that contrast or combine multiple sources or concepts.
   - **Index.md**: A catalog listing all pages, organized by category, with summaries and metadata.
   - **Log.md**: A chronological record of ingests, queries, and lint passes, providing a timeline and aiding navigation.
The LLM is responsible for creating, updating, cross-referencing, and maintaining consistency across all wiki pages. The wiki is the primary artifact consumed by the user.

3. **The Schema**: The schema is a configuration document (e.g., CLAUDE.md or AGENTS.md) that instructs the LLM on how to structure the wiki, what conventions to follow, and what workflows to implement. It evolves alongside the wiki, adapting to new requirements and user preferences. The schema ensures that the LLM acts as a disciplined maintainer rather than a generic chatbot, enforcing consistency and best practices.

Operational workflow is guided by the schema and includes:
- **Ingest**: Adding new sources, extracting knowledge, updating pages, and logging events.
- **Query**: Answering user questions by synthesizing information from relevant wiki pages, with answers filed back into the wiki.
- **Lint**: Periodic health checks to identify contradictions, stale claims, orphan pages, missing cross-references, and data gaps.

Optional tools and plugins (e.g., Obsidian Web Clipper, Marp, Dataview, qmd) enhance the architecture by streamlining source ingestion, presentation generation, dynamic querying, and search. The wiki is typically managed as a git repository, providing version history, branching, and collaboration capabilities.

## Key Properties

- **Layered Structure:** Three distinct layers—raw sources, wiki, schema—ensure modularity and clarity in maintenance and operations.
- **Immutable Raw Sources:** Raw sources are never modified, preserving the integrity and traceability of knowledge.
- **LLM-Owned Wiki:** The LLM exclusively manages the wiki layer, automating updates, cross-references, and consistency.
- **Evolving Schema:** The schema adapts to user needs and domain requirements, guiding the LLM's behavior and workflows.

## Limitations

The architecture's effectiveness depends on clear schema design and LLM capabilities. As the wiki grows, navigation may become challenging without additional tooling. Image handling requires workarounds, and schema evolution may introduce complexity. The abstract nature means implementation details must be tailored to specific domains, which can be labor-intensive.

## Example

A business team maintains an internal wiki. Meeting transcripts and project documents are added as raw sources. The LLM processes each, updates entity pages (e.g., 'Project X'), concept pages (e.g., 'Agile Methodology'), and synthesis summaries (e.g., 'Quarterly Review'). The schema specifies how to handle confidential information and update cross-references. Index.md catalogs all pages, and log.md records every ingest and query.

## Visual

Obsidian's graph view is recommended for visualizing the wiki's structure, showing connections between pages, hubs, and orphans. No explicit diagram is provided.

## Relationship to Other Concepts

- **[[GitHub Copilot]]** — Both leverage automation for code or knowledge management, but Copilot focuses on code completion while the LLM wiki architecture targets persistent knowledge bases.
- **[[Custom Agents in VS Code]]** — Custom agents automate workflows in VS Code; similarly, LLMs automate wiki maintenance in this architecture.
- **Retrieval-Augmented Generation (RAG)** — Contrasts with RAG by emphasizing persistent knowledge accumulation and maintenance rather than rediscovery at query time. Knowledge is *compiled once and kept current*, not re-derived per query.
- **Memex (Vannevar Bush, 1945)** — Inspired by Memex's vision of a curated knowledge store with associative trails. The unsolved part of Bush's vision was *who maintains it*; the LLM solves that.
- **[[Palace Memory Architecture]]** — Complementary memory model: MemPalace excels at verbatim recall and spatial navigation; the wiki excels at synthesis and cross-referencing.

## Practical Applications

Applicable to personal knowledge management, research wikis, business/team internal documentation, competitive analysis, trip planning, course notes, and hobby deep-dives. The architecture supports scalable, sustainable knowledge accumulation and organization.

## Sources

- [[LLM Wiki]] — primary source for this concept
- [[Copilot Session Checkpoint: Planning and Progress Tracking Complete]] — additional source
