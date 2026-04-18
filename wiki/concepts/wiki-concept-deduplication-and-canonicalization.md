---
title: "Wiki Concept Deduplication and Canonicalization"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "18966277cc2d851def0d3ab62f0f8bc086251d5a0cc524d2697ef2d9766a9892"
sources:
  - raw/2026-04-18-copilot-session-mobile-graph-ui-wiki-dedup-39a4d74e.md
quality_score: 100
concepts:
  - wiki-concept-deduplication-and-canonicalization
related:
  - "[[Structured Artifact Chains]]"
  - "[[Copilot Session Checkpoint: Mobile Graph UI + Wiki Dedup]]"
tier: hot
tags: [wiki, deduplication, canonicalization, knowledge-management, llm]
---

# Wiki Concept Deduplication and Canonicalization

## Overview

Deduplication and canonicalization are processes for merging duplicate wiki concept pages and establishing a single authoritative entry. This is critical for maintaining clarity, preventing fragmentation, and ensuring that cross-references and synthesis pages are accurate.

## How It Works

The deduplication process begins with identifying duplicate concept pages, which can arise from LLM auto-ingest mechanisms that split similar content across multiple files (e.g., 'linear-regression' vs 'linear-regression-algorithm'). Detection is typically based on identical source hashes, but can be enhanced with fuzzy matching algorithms such as RapidFuzz's token_set_ratio.

Once duplicates are identified, the canonical page is selected (usually the one with broader coverage or more established tier). The merging process involves:
- Appending all source references from the duplicate to the canonical entry
- Expanding content sections (e.g., complexity analysis, related concepts)
- Updating tags and related links across the wiki to point to the canonical slug
- Deleting the duplicate file

Bidirectional links are added between related concepts, especially when synthesis pages bridge topics but underlying concepts lack lateral links. Sed or scripting tools are used for sweeping references across multiple files, ensuring consistency.

Audit logs are updated to record merges, preserving historical references for traceability. The wiki index is rebuilt to reflect the new structure, and community detection in the knowledge graph is re-run to verify improved clustering and reduced fragmentation.

Technical challenges include permission errors (e.g., EACCES when files are owned by containers), which require chown or sudo operations before edits. The deduplication logic is implemented in scripts such as auto_ingest.py, with fuzzy matching added before concept creation to merge near-duplicates.

## Key Properties

- **Source Hash Matching:** Identifies duplicates by exact content hash, ensuring only identical sources are merged.
- **Fuzzy Title Matching:** Uses token_set_ratio (RapidFuzz) ≥85 to merge near-duplicate concept titles.
- **Canonicalization:** Establishes a single authoritative page, expands content, and updates cross-references.
- **Audit Logging:** Records all merges and deletions for traceability and historical reference.

## Limitations

Exact hash matching can miss near-duplicates with minor edits. Fuzzy matching may incorrectly merge distinct concepts if thresholds are not carefully tuned. Permission issues can block edits, requiring manual intervention. Deduplication may disrupt existing synthesis or cross-reference pages if not coordinated.

## Example

The session merged 'linear-regression-algorithm.md' into 'linear-regression.md', appending sources and expanding complexity analysis. All references across 9 files were updated via sed, and the duplicate file was deleted. The wiki index was rebuilt to reflect the canonical structure.

## Visual

No explicit diagrams, but the process is described as a sweep across multiple files and a rebuild of the wiki index.

## Relationship to Other Concepts

- **[[Structured Artifact Chains]]** — Both aim to reduce fragmentation and improve traceability in agentic workflows.

## Practical Applications

Deduplication ensures that knowledge bases, wikis, and agent-driven documentation remain coherent and navigable. It is vital for collaborative environments, LLM-powered ingest pipelines, and any system where automated content creation risks fragmentation.

## Sources

- [[Copilot Session Checkpoint: Mobile Graph UI + Wiki Dedup]] — primary source for this concept
