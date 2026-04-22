---
title: "Wiki Deduplication and Concept Merging in LLM Wikis"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "499ac65895e3b4c5dbf581d0dac3942433dcc90dd7be66960430f78040b8df5a"
sources:
  - raw/2026-04-18-copilot-session-mobile-graph-ui-wiki-dedup-39a4d74e.md
quality_score: 76
concepts:
  - wiki-deduplication-and-concept-merging-in-llm-wikis
related:
  - "[[LLM Wiki Architecture]]"
  - "[[Copilot Session Checkpoint: Mobile Graph UI + Wiki Dedup]]"
tier: hot
tags: [deduplication, concept-merging, llm-wiki, knowledge-graph, curation]
---

# Wiki Deduplication and Concept Merging in LLM Wikis

## Overview

Wiki deduplication is the process of identifying and merging duplicate concept pages within an LLM Wiki, ensuring canonical references and reducing fragmentation. This is crucial for maintaining a coherent knowledge structure, improving graph community detection, and supporting agentic workflows that rely on accurate cross-linking.

## How It Works

Deduplication begins with a review of the wiki and its associated knowledge graph, using both explicit source hashes and concept name similarity to identify duplicates. In this session, duplicate pairs such as 'linear-regression' and 'linear-regression-algorithm', as well as 'llm-wiki-architecture' and 'llm-maintained-persistent-wiki-pattern', were detected by matching identical source_hash values and content overlap.

The merging process involves selecting a canonical page (e.g., 'linear-regression.md'), expanding its frontmatter with additional sources and complexity analysis, and deleting the redundant file. All references across the wiki are swept using tools like `sed` to update wikilinks and tags, ensuring that the merged concept is consistently referenced. Bidirectional links are added to related concepts to strengthen graph connectivity, as seen with the transformer-attention relationship.

Technical implementation leverages scripts such as `auto_ingest.py`, which checks for full source-hash matches before creating new concept files. Future improvements include integrating fuzzy matching (e.g., rapidfuzz token_set_ratio ≥ 85) to catch near-duplicate concept names before file creation. The deduplication process is logged in an audit file (`wiki/log.md`) to preserve historical references and maintain transparency.

Deduplication impacts the knowledge graph by reducing node count, improving community detection, and lowering false adjacency caused by publisher entities acting as god-nodes. It also enables more accurate agent workflows, as agents can propose file-back actions, lint for implicit concepts, and curate graph-aware relationships. After deduplication, scripts like `compile_index.py` rebuild the wiki index to reflect the updated structure.

Edge cases include permission issues (e.g., EACCES errors when files are owned by root due to containerized auto-ingest), which require manual intervention (sudo chown or sed -i). Deduplication must also account for synthesis pages that bridge concepts, ensuring underlying concepts are properly lateral-linked.

## Key Properties

- **Source Hash Matching:** Identifies duplicates by comparing source_hash values, ensuring content-level deduplication.
- **Fuzzy Concept Name Matching:** Planned integration of rapidfuzz token_set_ratio ≥ 85 to catch near-duplicate concept titles.
- **Canonical Reference Updating:** All wikilinks and tags are updated to point to the merged concept, preserving graph integrity.
- **Audit Logging:** All merges and edits are recorded in wiki/log.md for transparency and historical traceability.

## Limitations

Current deduplication only checks exact source_hash matches; fuzzy matching is pending. Permission issues may block edits in containerized environments. Synthesis pages may require manual review to ensure proper lateral linking after merges.

## Example

The concepts 'linear-regression-algorithm.md' and 'linear-regression.md' are merged. All references to the former are replaced with the latter, and the redundant file is deleted. The wiki index is rebuilt to reflect the change.

## Visual

No explicit diagrams, but the process involves updating files, references, and graph structure to consolidate duplicate nodes.

## Relationship to Other Concepts

- **[[LLM Wiki Architecture]]** — Deduplication strengthens the underlying architecture by reducing fragmentation and improving graph connectivity.

## Practical Applications

Ensures LLM Wikis remain coherent and navigable, supporting research, agentic workflows, and persistent knowledge codification. Improves graph-based community detection and reduces false adjacency from publisher entities.

## Sources

- [[Copilot Session Checkpoint: Mobile Graph UI + Wiki Dedup]] — primary source for this concept
