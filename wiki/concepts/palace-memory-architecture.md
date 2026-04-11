---
title: "Palace Memory Architecture"
type: concept
created: 2026-04-11
last_verified: 2026-04-11
source_hash: "101bef9011616b455e60e17998c3f1b308c5cab895c27a19c5a6f4d028ffcfb8"
sources:
  - raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md
quality_score: 100
concepts:
  - palace-memory-architecture
related:
  - "[[Continuum Memory System]]"
  - "[[LLM-Maintained Persistent Wiki Pattern]]"
  - "[[MemPalace GitHub Repository]]"
tier: hot
tags: [memory, ai, knowledge-management, retrieval, architecture]
---

# Palace Memory Architecture

## Overview

The Palace Memory Architecture is a hierarchical, spatially-inspired system for organizing AI memory, modeled after the ancient mnemonic technique of the memory palace. It divides user-AI interactions into wings, rooms, halls, closets, and drawers, enabling efficient, context-rich retrieval and navigation of vast conversational histories.

## How It Works

The Palace Memory Architecture draws inspiration from the classical memory palace, where ideas are mentally placed in distinct rooms of an imaginary building for easy recall. MemPalace adapts this principle to digital AI memory by structuring all stored content into a multi-tiered hierarchy:

- **Wings**: Each wing represents a major domain, such as a person, project, or topic. For example, a wing could be 'Orion' (a project) or 'Kai' (a team member).

- **Rooms**: Within each wing, rooms correspond to specific subjects or aspects. For a project wing, rooms might include 'auth-migration', 'billing', or 'CI-pipeline'. Rooms are automatically detected during mining, but users can personalize them.

- **Halls**: These are corridors connecting related rooms within the same wing. Halls are standardized memory types (e.g., hall_facts, hall_events, hall_discoveries, hall_preferences, hall_advice), providing semantic organization and facilitating retrieval by context type.

- **Closets**: Each room contains closets, which are summaries or pointers to the original content. In v3.0.0, closets are plain-text summaries, but future versions will support AAAK-encoded closets for greater compression.

- **Drawers**: Drawers hold the original, verbatim files—every word, never summarized. This ensures maximum fidelity and enables precise recall.

- **Tunnels**: Tunnels link rooms across different wings, allowing cross-domain retrieval. For instance, if 'auth-migration' appears in both a person wing and a project wing, a tunnel connects them, enabling queries that span multiple contexts.

The architecture is implemented using ChromaDB for vector storage (semantic search) and SQLite for the temporal entity-relationship knowledge graph. The CLI and MCP server interface allow mining, searching, and context injection. The structure is not merely cosmetic; benchmark results show that filtering by wing and room yields a 34% improvement in retrieval accuracy compared to flat search.

Edge cases are handled by the flexible hierarchy: users can add new wings or rooms as needed, and the system automatically detects and links repeated topics across domains. The architecture supports both project and conversational mining modes, and can be extended to other datastores.

Trade-offs include the complexity of maintaining the hierarchy and the need for accurate room detection. However, the benefits in retrieval performance and context preservation are substantial, especially for long-term, multi-project AI workflows.

## Key Properties

- **Hierarchical Structure:** Organizes memory into wings, rooms, halls, closets, and drawers, mirroring a spatial mnemonic system.
- **Semantic Retrieval:** Uses ChromaDB vector search and metadata filtering to achieve high recall rates.
- **Cross-Domain Linking:** Tunnels connect rooms across wings, enabling queries that span projects, people, and topics.
- **Raw Verbatim Storage:** Stores every exchange without summarization, preserving full context and reasoning.
- **Retrieval Performance:** Filtering by palace structure yields up to 34% improvement in recall (94.8% vs 60.9% for flat search).

## Limitations

Requires accurate room and wing detection for optimal organization; complexity increases with scale and personalization. The structure relies on user input and mining patterns, which may introduce inconsistencies if not maintained. AAAK compression is not yet integrated into closets, so current summaries are plain text.

## Example

A solo developer mines conversations for three projects (Orion, Nova, Helios), creating wings for each. Searching for 'database decision' in the Orion wing retrieves the exact rationale for choosing Postgres, including the date and context. Cross-project searches link related decisions across wings via tunnels.

## Visual

A diagram (in README) shows two wings (Person, Project), each with rooms connected by halls, closets leading to drawers, and tunnels linking rooms across wings. The structure visually resembles a building with interconnected rooms and corridors.

## Relationship to Other Concepts

- **[[Continuum Memory System]]** — Both aim to preserve long-term AI memory, but Palace Memory Architecture uses spatial hierarchy for organization.
- **[[LLM-Maintained Persistent Wiki Pattern]]** — Both focus on persistent knowledge storage, but MemPalace emphasizes verbatim recall and navigable structure.

## Practical Applications

Used by AI agents (Claude Code, ChatGPT, Gemini CLI) to recall decisions, debugging sessions, and project history. Enables team leads to retrieve sprint work, cross-project rationale, and recommendations. Supports solo developers in remembering context across multiple projects and timeframes.

## Sources

- [[MemPalace GitHub Repository]] — primary source for this concept
