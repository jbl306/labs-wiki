---
title: "Labs-Wiki Architecture and Implementation"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "bed95bb11bf69d800c6655091a905351b08f9bbfd77b74c912c1ee646e703b4f"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-full-labs-wiki-implementation-complete-22f8c487.md
quality_score: 67
concepts:
  - labs-wiki-architecture-and-implementation
related:
  - "[[Agentic Context Engineering (ACE)]]"
  - "[[Durable Copilot Session Checkpoint Promotion]]"
  - "[[Copilot Session Checkpoint: Full Labs-Wiki Implementation Complete]]"
tier: hot
tags: [LLM Wiki, Knowledge Management, Personal Wiki, AI Integration, Multi-Device Ingestion]
---

# Labs-Wiki Architecture and Implementation

## Overview

Labs-Wiki is a personal knowledge wiki powered by large language models (LLMs), designed following Karpathy's LLM Wiki pattern. It is optimized for integration with VS Code Copilot, Copilot CLI, and OpenCode, enabling seamless knowledge ingestion, querying, and maintenance. The architecture emphasizes modularity, quality control, and multi-device ingestion.

## How It Works

The labs-wiki architecture is organized into three primary layers:

1. **Raw Layer (`raw/`)**: This layer stores immutable source documents that serve as the foundational knowledge inputs. Each raw source is tracked with metadata including title, type, capture timestamp, source URL, content hash, and tags.

2. **Wiki Layer (`wiki/`)**: This layer contains LLM-compiled wiki pages generated from the raw sources. It is subdivided into four page types:
   - **Sources**: One-to-one mappings with raw documents.
   - **Concepts**: Extracted ideas and methodologies.
   - **Entities**: Tools, people, organizations, datasets, and models.
   - **Synthesis**: Comparative or integrative analyses.

3. **Agent Schema (`AGENTS.md`)**: A universal schema file read by all integrated AI tools, defining conventions, workflows, frontmatter standards, linting rules, quality scoring, and agent personas.

The ingestion process is two-phased:
- **Phase 1 (Extract)**: Performs hash checks and extracts concepts from raw sources.
- **Phase 2 (Compile)**: Generates wiki pages and cross-references.

Quality and staleness are managed through a scoring system (0-100) based on completeness, cross-references, attribution, and recency, with a staleness threshold set at 90 days.

The project was implemented in six phases, each with validation gates ensuring correctness and completeness:
- Phase 1: Foundation setup including directory structure and universal schema.
- Phase 2: Skill definitions for wiki operations.
- Phase 3: Tooling scripts for scaffolding, linting, and indexing.
- Phase 4: Documentation including architecture and workflows.
- Phase 5: Multi-device ingestion API and automation.
- Phase 6: Seed content and final validations.

The implementation includes detailed frontmatter standards for wiki pages and raw sources, ensuring consistency and enabling automated quality checks. The system supports multi-device ingestion through a FastAPI app with bearer token authentication, filename sanitization, and file size limits. Notifications are integrated via ntfy for capture events.

This architecture supports extensibility, maintainability, and integration with multiple AI-assisted development tools, enabling a robust personal knowledge management system.

## Key Properties

- **Three-Layer Architecture:** Raw immutable sources, LLM-compiled wiki pages, and a universal agent schema.
- **Two-Phase Ingestion:** Phase 1 extract with hash checks and concept extraction; Phase 2 compile with page generation and cross-references.
- **Quality Scoring:** 0-100 scale based on completeness, cross-references, attribution, and recency; staleness threshold at 90 days.
- **Multi-Tool Integration:** Universal AGENTS.md schema read by VS Code Copilot, Copilot CLI, and OpenCode.
- **Multi-Device Ingestion API:** FastAPI app with bearer token auth, filename sanitization, 15MB file size limit, and ntfy notifications.

## Limitations

The system relies on accurate frontmatter metadata and consistent source hashing; errors in these can lead to stale or inconsistent wiki pages. The ingestion API has a 15MB file size limit, which may restrict very large documents. Deployment of the ingestion API is not yet automated in the user's homelab environment, requiring manual setup. The quality scoring system depends on predefined heuristics that may not capture all nuances of content quality.

## Example

Example of the ingestion API usage:

```python
import requests

headers = {'Authorization': 'Bearer <WIKI_API_TOKEN>'}
files = {'file': open('example.md', 'rb')}
response = requests.post('http://localhost/api/ingest/file', headers=headers, files=files)
print(response.status_code, response.json())
```

Example frontmatter for a wiki concept page:

```yaml
---
title: "Labs-Wiki Architecture"
type: "concept"
created: "2026-04-07"
sources: ["raw/labs-wiki-architecture.md"]
quality_score: 95
concepts: ["LLM Wiki Pattern", "Multi-Device Ingestion"]
tags: ["wiki", "architecture"]
---
```

## Visual

The source includes mermaid diagrams in README.md and architecture.md illustrating the three-layer wiki architecture and workflows, showing data flow from raw sources through extraction and compilation to final wiki pages, and integration points with AI tools. No direct images are included in the source text but diagrams are referenced.

## Relationship to Other Concepts

- **[[Agentic Context Engineering (ACE)]]** — Related methodology for evolving context in LLM workflows
- **[[Durable Copilot Session Checkpoint Promotion]]** — Mechanism for promoting durable checkpoints into persistent wiki storage

## Practical Applications

Labs-Wiki serves as a personal knowledge management system that leverages LLMs for knowledge extraction, synthesis, and querying. It is particularly useful for researchers, developers, and knowledge workers who want to maintain an evolving, high-quality, and well-structured knowledge base integrated with AI-assisted coding tools. The multi-device ingestion API enables capturing knowledge from diverse sources such as mobile devices, browsers, and CLI tools, centralizing knowledge capture and maintenance.

## Sources

- [[Copilot Session Checkpoint: Full Labs-Wiki Implementation Complete]] — primary source for this concept
