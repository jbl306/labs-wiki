---
title: "Closet Index Layer"
type: concept
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "d08a3ffff055c78ea944afe2266f216cbdf096a7a4848a8aaca92dff7205ba1d"
sources:
  - raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md
quality_score: 76
concepts:
  - closet-index-layer
related:
  - "[[MemPalace Memory System]]"
  - "[[milla-jovovich/mempalace]]"
tier: hot
tags: [indexing, semantic-search, retrieval, memory-architecture]
---

# Closet Index Layer

## Overview

Closets are the index layer in MemPalace, storing compact pointers to verbatim content drawers. They enable fast, scoped semantic search by mapping topics, entities, and quotes to their corresponding content chunks.

## How It Works

Closets are created during the mining process (`mempalace mine`). For each file, the content is chunked into drawers (verbatim segments of ~800 characters). Topics, entities, and notable quotes are extracted from the content, and for each, a line is added to a closet document. Each closet line follows the format: `topic description|entity1;entity2|→drawer_id_1,drawer_id_2`, or for quotes: `"verbatim quote"|entity1|→drawer_id_3`.

Closets are designed to be small and fast to search. Each closet is capped at 1,500 characters (`CLOSET_CHAR_LIMIT`), and content scanned per file is limited to 5,000 characters (`CLOSET_EXTRACT_WINDOW`). If adding a topic would exceed the closet size limit, a new closet is created. Each closet line is atomic and points to one or more drawers by ID. Topics are never split across closets, ensuring that each topic's pointers are grouped together.

When a file is re-mined (e.g., content changes or normalization version is bumped), all closets for that file are purged and rebuilt, ensuring no stale topics persist. This is done by deleting all closets associated with the source file before writing new ones. Closets are stored in the `mempalace_closets` ChromaDB collection alongside drawers and are automatically recreated if the palace is rebuilt.

During search, the system first queries closets (small, fast documents) for matches to the user's query. For each closet hit, it parses the pointer lines to fetch the referenced drawers (verbatim content). A `max_distance` filter is applied to ensure relevance, and results are returned at the chunk (drawer) level. If no closets exist or all hits are filtered out, the system falls back to direct drawer search. Each search result indicates whether it was matched via closet or drawer, and includes a preview of the closet line that surfaced it.

Closet search currently ranks results by ChromaDB cosine distance. BM25 hybrid re-ranking is planned for future releases. The closet index layer is implemented in `mempalace/palace.py` (for building and updating closets) and `mempalace/searcher.py` (for search and retrieval).

## Key Properties

- **Atomic Topic Pointers:** Each closet line points to one or more drawers for a specific topic, entity, or quote.
- **Size Limits:** Closets are capped at 1,500 characters; max 12 topics, 3 quotes, and 5 entities per file.
- **Fast Search:** Closets are small, enabling rapid semantic search before fetching larger verbatim content.
- **No Stale Topics:** Closets are rebuilt on each mine, ensuring the index always matches current content.
- **Scoped Retrieval:** Searches can be scoped by topic or entity, avoiding flat corpus queries.

## Limitations

Currently, only project-mined content builds closets; conversation-mined content (e.g., chat transcripts) uses direct drawer search until future updates. The extraction window is limited to the first 5,000 characters of a file, so content beyond this is not indexed in closets. BM25 hybrid re-ranking and LLM-based closet ranking are not yet implemented.

## Example

A closet line example:

```
built auth system|Ben;Igor|→drawer_api_auth_a1b2c3
```

Search workflow:
- User queries "who built the auth?"
- System searches closets for matching topic/entity
- Finds the above line, fetches the referenced drawer for verbatim content

## Visual

No diagram, but the README and docs describe the mapping: Query → search closets (fast) → parse pointers → fetch drawers (verbatim) → apply filters → return results.

## Relationship to Other Concepts

- **[[MemPalace Memory System]]** — Closets are a core component of the MemPalace architecture, serving as the index layer.

## Practical Applications

Closets enable fast, scoped retrieval of relevant information in large corpora, supporting workflows such as codebase search, project documentation mining, and AI agent memory retrieval.

## Sources

- [[milla-jovovich/mempalace]] — primary source for this concept
