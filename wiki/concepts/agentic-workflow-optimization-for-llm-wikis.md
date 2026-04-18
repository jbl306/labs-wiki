---
title: "Agentic Workflow Optimization for LLM Wikis"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "499ac65895e3b4c5dbf581d0dac3942433dcc90dd7be66960430f78040b8df5a"
sources:
  - raw/2026-04-18-copilot-session-mobile-graph-ui-wiki-dedup-39a4d74e.md
quality_score: 100
concepts:
  - agentic-workflow-optimization-for-llm-wikis
related:
  - "[[LLM Wiki Architecture]]"
  - "[[Copilot Session Checkpoint: Mobile Graph UI + Wiki Dedup]]"
tier: hot
tags: [agentic-workflow, llm-wiki, curation, automation, graph-aware]
---

# Agentic Workflow Optimization for LLM Wikis

## Overview

Agentic workflow optimization involves upgrading wiki agents (curator, lint, query) to be graph-aware, support file-back actions, and enforce log prefix standards. This enables more robust, self-improving wiki environments where agents can proactively maintain structure, suggest implicit concepts, and facilitate persistent knowledge ingestion.

## How It Works

The optimization begins by reviewing agent specifications and identifying gaps compared to Karpathy's principles: agents should compile-once and keep current, propose file-back actions for good answers, lint for implicit concepts and missing cross-refs, and enforce log prefix standards for traceability.

Current agents include wiki-query (read-only), wiki-lint (checks for explicit issues), and wiki-curator (not graph-aware). The session outlines upgrades: wiki-query should propose file-back actions, wiki-lint should detect implicit concepts, graph orphans, and source-hash duplicates, and wiki-curator should leverage graph statistics to suggest merges and lateral links. Prompts in `.agent.md` files are edited to encode these behaviors.

Technical implementation involves integrating graph API endpoints for stats, communities, god-nodes, and surprises, allowing agents to reason about graph structure. Agents can use SQL todos to track merges, edits, and rebuilds, and append entries to the audit log with standardized prefixes (`## [YYYY-MM-DD] op | Title`).

Permission and deployment issues are considered: agents must be able to edit files owned by root (via sudo chown or sed -i), and containerized environments must expose the necessary APIs and tokens. Agents are also tasked with demoting publisher entities in the graph builder, reducing their edge weights to prevent false adjacency and improve community detection.

The workflow is iterative: agents execute tasks in phases (deduplication, fuzzy merge, prompt upgrades, publisher demotion), rebuilding the wiki index and graph after each phase. This ensures the wiki remains current, connected, and self-improving, aligned with Karpathy's compile-once principle.

## Key Properties

- **Graph-Aware Agent Prompts:** Agents leverage graph statistics and structure to suggest merges, lateral links, and community improvements.
- **File-Back Actions:** Agents propose new or updated wiki pages based on query results and lint findings.
- **Implicit Concept Detection:** Lint agent checks for concepts implied but not explicitly documented, suggesting new pages or cross-refs.
- **Log Prefix Enforcement:** All agent actions are logged with standardized prefixes for auditability and traceability.

## Limitations

Agents require access to graph APIs and file system permissions, which may be blocked in containerized environments. Prompt upgrades must be carefully designed to avoid false positives or excessive merges. Publisher demotion may impact graph connectivity if not tuned properly.

## Example

The wiki-curator agent detects that 'attention-mechanism-in-large-language-models.md' and 'transformer-architecture.md' should be linked. It proposes edits, updates the graph, and logs the action with a standardized prefix.

## Visual

No explicit diagrams, but agent workflows are tracked via SQL todos and audit log entries, reflecting iterative improvements.

## Relationship to Other Concepts

- **[[LLM Wiki Architecture]]** — Agentic workflows are integral to maintaining and evolving the wiki's knowledge structure.

## Practical Applications

Supports persistent knowledge codification, automated curation, and self-improving wiki environments for research and engineering teams. Enables scalable maintenance of large LLM Wikis and knowledge graphs.

## Sources

- [[Copilot Session Checkpoint: Mobile Graph UI + Wiki Dedup]] — primary source for this concept
