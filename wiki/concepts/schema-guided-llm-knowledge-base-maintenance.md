---
title: "Schema-Guided LLM Knowledge Base Maintenance"
type: concept
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "a402e64fc0c46e618b01acc3502f18a992b4a42222bfd7f87c9abbee3801c98f"
sources:
  - raw/2026-04-07-llm-wiki.md
quality_score: 100
concepts:
  - schema-guided-llm-knowledge-base-maintenance
related:
  - "[[LLM Wiki Architecture]]"
  - "[[LLM Wiki]]"
tier: hot
tags: [schema, llm, maintenance, workflow, knowledge-base]
---

# Schema-Guided LLM Knowledge Base Maintenance

## Overview

Schema-guided maintenance is a methodology where a configuration document defines the structure, conventions, and workflows for an LLM-maintained wiki. This schema acts as the operational blueprint, ensuring that the LLM follows consistent procedures for ingesting sources, updating pages, answering queries, and maintaining the knowledge base.

## How It Works

The schema (e.g., CLAUDE.md or AGENTS.md) is a living document that specifies how the wiki is organized, what types of pages exist (entities, concepts, sources, syntheses), and what workflows the LLM should follow. It may include:

- Directory structure and naming conventions.
- Page formats (frontmatter, sections, tags).
- Rules for cross-referencing, contradiction detection, and synthesis filing.
- Operational procedures for ingest, query, lint, and logging.
- Criteria for when to create new pages, update existing ones, or flag issues.

When a new source is ingested, the schema guides the LLM in extracting relevant information, updating appropriate pages, and maintaining consistency. For queries, it defines how answers should be synthesized, cited, and filed back into the wiki. During lint passes, it outlines checks for contradictions, stale claims, orphan pages, and missing cross-references.

The schema is co-evolved by the user and the LLM. As workflows change or new requirements emerge, the schema is updated to reflect best practices and domain-specific needs. This enables the LLM to operate as a disciplined wiki maintainer rather than a generic chatbot.

**Benefits:**
- Ensures consistent, high-quality maintenance of the wiki.
- Enables domain-specific customization and workflow optimization.
- Reduces ambiguity and error by providing explicit operational guidance.

**Edge Cases:**
- If the schema is too rigid, it may limit adaptability; if too loose, it may lead to inconsistency.
- Schema evolution requires ongoing collaboration between user and LLM.

**Trade-Offs:**
- Schema complexity vs. operational flexibility.
- Manual schema updates vs. automated schema learning.

## Key Properties

- **Operational Blueprint:** Defines workflows, page formats, and maintenance procedures for the LLM.
- **Co-Evolution:** Schema is updated collaboratively as workflows and requirements change.
- **Consistency and Quality:** Ensures the LLM maintains the wiki with consistent structure and high quality.

## Limitations

Schema-guided maintenance depends on the clarity and completeness of the schema. Poorly defined schemas can lead to inconsistent wiki updates. Overly complex schemas may hinder adaptability. Ongoing schema evolution requires user involvement and may not scale well in highly dynamic domains.

## Example

A team maintains a business wiki with a schema specifying entity pages for customers, concept pages for products, and synthesis pages for market analyses. The schema outlines how meeting transcripts are ingested, how cross-references are updated, and how contradictions are flagged. The LLM follows these rules, ensuring the wiki remains current and consistent.

## Relationship to Other Concepts

- **LLM Wiki Pattern** — Schema-guided maintenance is a core operational principle of the LLM Wiki Pattern.
- **[[LLM Wiki Architecture]]** — The schema defines the architecture and workflows for the wiki.

## Practical Applications

Schema-guided maintenance is useful for any LLM-powered wiki where consistency, quality, and domain-specific workflows are critical. It is especially valuable in business, research, and collaborative environments where multiple users and sources require structured integration.

## Sources

- [[LLM Wiki]] — primary source for this concept
