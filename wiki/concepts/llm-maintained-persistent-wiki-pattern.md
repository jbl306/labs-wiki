---
title: "LLM-Maintained Persistent Wiki Pattern"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "dc3efe98ae62f23dd08acad13aba2e95287beb20b6bec2f4af0423557fe37401"
sources:
  - raw/2026-04-07-llm-wiki.md
quality_score: 100
concepts:
  - llm-maintained-persistent-wiki-pattern
related:
  - "[[LLM Wiki]]"
tier: hot
tags: [llm, wiki, knowledge-base, automation, personal-knowledge-management]
---

# LLM-Maintained Persistent Wiki Pattern

## Overview

The LLM-maintained persistent wiki pattern is an approach to building personal or organizational knowledge bases where a large language model (LLM) incrementally constructs, updates, and maintains a structured, interlinked wiki from raw source documents. Unlike traditional retrieval-augmented generation (RAG) systems, this pattern focuses on knowledge accumulation, synthesis, and maintenance, enabling the wiki to become richer and more useful over time.

## How It Works

At its core, the LLM-maintained persistent wiki pattern leverages the capabilities of LLMs to automate the tedious aspects of knowledge base upkeep. The process begins with a curated collection of immutable raw sources—articles, papers, images, and data files—which serve as the foundation for knowledge extraction. When a new source is added, the LLM reads and processes it, extracting key concepts, entities, and relationships. It then integrates this information into the existing wiki, updating relevant pages, cross-references, and synthesis summaries. This incremental approach ensures that the wiki reflects the most current and comprehensive understanding of the domain.

The architecture is organized into three distinct layers:

1. **Raw Sources**: These are the original documents and files, unmodified and serving as the source of truth. The LLM accesses but does not alter these.
2. **The Wiki**: This is a directory of markdown files generated and maintained by the LLM. It includes summaries, entity pages, concept pages, comparisons, overviews, and synthesis articles. The LLM is responsible for creating, updating, and cross-referencing these pages, ensuring consistency and coherence across the knowledge base.
3. **The Schema**: A configuration document (e.g., CLAUDE.md or AGENTS.md) that defines the structure, conventions, and workflows for the wiki. It guides the LLM in how to ingest sources, answer queries, and maintain the wiki, evolving alongside the knowledge base as requirements change.

The operational workflow involves several key actions:
- **Ingest**: When a new source is introduced, the LLM processes it, discusses key takeaways with the user, writes a summary page, updates the index, revises entity and concept pages, and logs the event. This can be done interactively (one source at a time) or in batches, depending on user preference.
- **Query**: Users ask questions against the wiki, and the LLM synthesizes answers from relevant pages, providing citations and potentially generating new wiki pages (e.g., comparisons, analyses) as a result. This ensures that valuable insights are preserved and contribute to the compounding knowledge base.
- **Lint**: Periodic health checks by the LLM identify contradictions, stale claims, orphan pages, missing cross-references, and data gaps. The LLM can suggest new questions and sources to keep the wiki robust and up-to-date.

Navigation and history are facilitated by two special files:
- **index.md**: A content-oriented catalog listing all wiki pages with summaries and metadata, organized by category. It enables efficient lookup and navigation, especially at moderate scales.
- **log.md**: A chronological, append-only record of ingests, queries, and lint passes, providing a timeline of the wiki's evolution and aiding in understanding recent activity.

Optional CLI tools, such as local search engines (e.g., qmd), can enhance the LLM's ability to operate on the wiki efficiently as it grows. Plugins like Obsidian Web Clipper, Marp, and Dataview further streamline source ingestion, presentation generation, and dynamic querying.

The pattern is inspired by Vannevar Bush's Memex vision—a personal, curated knowledge store with associative trails. The LLM solves the maintenance challenge by automating cross-referencing, updating summaries, and flagging contradictions, making the wiki sustainable and valuable over time.

## Key Properties

- **Incremental Knowledge Accumulation:** The wiki grows richer with every new source and query, compounding knowledge rather than rediscovering it each time.
- **Automated Maintenance:** LLMs handle cross-referencing, updating summaries, and flagging contradictions, reducing the human burden and keeping the wiki consistent.
- **Structured, Interlinked Artifact:** The wiki is composed of markdown files organized by entities, concepts, comparisons, and synthesis, with persistent cross-references.
- **Configurable Schema:** A schema document guides the LLM in maintaining the wiki, allowing customization for different domains and workflows.

## Limitations

The pattern relies on the LLM's ability to accurately extract, synthesize, and maintain knowledge, which may be limited by model capabilities, prompt design, and schema clarity. Large-scale wikis may require additional tooling (e.g., search engines) to remain navigable. Image handling is clunky, as LLMs cannot natively process markdown with inline images in one pass. The approach is abstract and requires adaptation for specific domains, with potential challenges in schema evolution and workflow optimization.

## Example

Suppose a researcher is studying climate change. As they read papers and articles, they drop each source into the raw collection. The LLM processes each source, extracts key findings, updates relevant entity pages (e.g., 'Greenhouse Gases'), concept pages (e.g., 'Carbon Cycle'), and synthesis summaries (e.g., 'Recent Trends in Atmospheric CO2'). Contradictions between sources are flagged, and the index.md is updated to reflect new content. The researcher queries the wiki for 'Impact of methane emissions,' and the LLM synthesizes an answer, citing relevant pages and filing the answer as a new wiki page.

## Visual

The source mentions Obsidian's graph view as a visualization tool, showing the connections between wiki pages, hubs, and orphan nodes. No explicit diagram is included.

## Relationship to Other Concepts

- **Retrieval-Augmented Generation (RAG)** — Contrasts with RAG by emphasizing persistent knowledge accumulation and maintenance rather than rediscovery at query time.
- **Memex** — Inspired by Memex's vision of a curated knowledge store with associative trails, but solves the maintenance challenge with LLM automation.

## Practical Applications

Personal knowledge tracking (health, goals, self-improvement), research wikis (incrementally building comprehensive topic coverage), book companion wikis (characters, themes, plot threads), business/team internal wikis (meeting transcripts, project docs), competitive analysis, trip planning, course notes, and hobby deep-dives. Useful whenever ongoing knowledge accumulation and organization are needed.

## Sources

- [[LLM Wiki]] — primary source for this concept
