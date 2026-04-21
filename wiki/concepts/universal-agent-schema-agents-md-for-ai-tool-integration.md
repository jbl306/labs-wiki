---
title: "Universal Agent Schema (AGENTS.md) for AI Tool Integration"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "bed95bb11bf69d800c6655091a905351b08f9bbfd77b74c912c1ee646e703b4f"
sources:
  - raw/2026-04-10-httpsgithubcommidudevautoskills.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-full-labs-wiki-implementation-complete-22f8c487.md
quality_score: 100
concepts:
  - universal-agent-schema-agents-md-for-ai-tool-integration
related:
  - "[[Agentic Context Engineering (ACE)]]"
  - "[[Agent-Ergonomic Tool Design Principles]]"
  - "[[Copilot Session Checkpoint: Full Labs-Wiki Implementation Complete]]"
tier: hot
tags: [Agent Schema, Workflow, Quality Scoring, AI Tool Integration, Agent Personas]
---

# Universal Agent Schema (AGENTS.md) for AI Tool Integration

## Overview

AGENTS.md is a universal schema file designed to be the authoritative configuration and knowledge constitution for the labs-wiki system. It standardizes conventions, workflows, frontmatter standards, lint rules, quality scoring, and agent personas, enabling seamless interoperability across multiple AI-assisted tools such as VS Code Copilot, Copilot CLI, and OpenCode.

## How It Works

AGENTS.md is a comprehensive markdown file (257 lines) that serves as the central schema for the labs-wiki project. It defines:

- **Wiki Conventions:** Naming, directory structures, frontmatter field requirements, and tagging standards.

- **Workflows:** Detailed descriptions of ingestion, querying, linting, updating, and orchestration workflows that agents follow to maintain and utilize the wiki.

- **Frontmatter Standards:** Required and optional metadata fields for different page types (sources, concepts, entities, synthesis), including fields like title, type, created, last_verified, source_hash, quality_score, and tags.

- **Lint Rules:** Automated checks for frontmatter completeness, broken links, orphan detection, and staleness, with a scoring system from 0 to 100 to quantify page quality.

- **Quality Scoring:** A formula combining completeness, cross-references, attribution, and recency, each contributing 25 points, to assess the health of wiki pages.

- **Agent Personas:** Definitions of roles such as researcher, compiler, curator, and auditor, each with specific responsibilities and permissions within the wiki maintenance lifecycle.

- **Skills Reference:** Links to skill definitions stored in `.github/skills/` that implement the workflows and operations defined in AGENTS.md.

This schema ensures that all AI tools interacting with the wiki have a consistent understanding of the wiki's structure, quality expectations, and operational procedures. It enables automated validation, incremental updates, and coordinated multi-agent workflows.

## Key Properties

- **Universal Schema:** Single source of truth for wiki conventions and workflows shared across multiple AI tools.
- **Comprehensive Workflows:** Defines ingestion, query, lint, update, and orchestration workflows for agents.
- **Quality Scoring System:** Automated scoring from 0-100 based on completeness, cross-references, attribution, and recency.
- **Agent Personas:** Role definitions for researcher, compiler, curator, auditor with assigned responsibilities.
- **Frontmatter Standards:** Mandatory and optional metadata fields for wiki pages to ensure consistency and machine-readability.

## Limitations

The AGENTS.md schema requires strict adherence to conventions; deviations can cause tooling errors or inconsistent wiki states. It assumes that all AI tools and human contributors understand and comply with the schema, which may require onboarding and training. The schema is static and may need updates as new features or workflows emerge, requiring coordinated versioning.

## Example

Excerpt from AGENTS.md defining a workflow step:

```markdown
## Ingest Workflow
- Step 1: Validate raw source frontmatter
- Step 2: Extract concepts and entities
- Step 3: Generate wiki pages
- Step 4: Update index and logs
```

Example agent persona snippet:

```markdown
### Researcher
- Role: Extract concepts and entities from raw sources
- Permissions: Read/write concepts and entities
- Tools: wiki-ingest, wiki-query
```

These definitions guide automated agents and human contributors in their tasks.

## Visual

No direct images included, but AGENTS.md contains structured markdown sections and tables that organize workflows, frontmatter fields, and persona roles clearly for human and machine consumption.

## Relationship to Other Concepts

- **[[Agentic Context Engineering (ACE)]]** — Shares principles of structured agent workflows and context management
- **[[Agent-Ergonomic Tool Design Principles]]** — Informs the design of schemas and workflows for agent usability

## Practical Applications

AGENTS.md enables consistent multi-agent coordination in the labs-wiki system, allowing different AI tools and human roles to collaborate effectively. It supports automated linting, quality scoring, and incremental updates, improving wiki reliability and maintainability. This schema approach can be adapted for other AI-powered knowledge management systems requiring multi-tool interoperability.

## Sources

- [[Copilot Session Checkpoint: Full Labs-Wiki Implementation Complete]] — primary source for this concept
- [[AutoSkills GitHub Repository]] — additional source
