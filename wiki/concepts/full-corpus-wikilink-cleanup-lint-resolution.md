---
title: "Full-Corpus Wikilink Cleanup and Lint Resolution"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "adcb44e6a85c6d693fc04b4b6b334024ca4365e1b7518d6c877ff915a7141135"
sources:
  - raw/2026-04-18-copilot-session-phase-5-merged-graph-ui-next-48f23b63.md
quality_score: 100
concepts:
  - full-corpus-wikilink-cleanup-lint-resolution
related:
  - "[[Quality Evaluation of Auto-Ingested Wiki Content]]"
  - "[[Wiki Deduplication and Concept Merging in LLM Wikis]]"
  - "[[Copilot Session Checkpoint: Phase 5 Merged; Graph UI Next]]"
tier: hot
tags: [wiki, lint, cleanup, quality, links, batch]
---

# Full-Corpus Wikilink Cleanup and Lint Resolution

## Overview

Full-corpus wikilink cleanup and lint resolution is a systematic approach to repairing broken links and metadata inconsistencies across a large wiki repository. By aligning link resolution logic between lint scripts and graph builders, this process eliminates false negatives and ensures that all pages are valid, interconnected, and ready for synthesis and promotion.

## How It Works

The cleanup process begins by identifying the root causes of lint failures, which often stem from mismatches between how wikilinks are resolved in different parts of the system. In this session, `scripts/lint_wiki.py` validated links only by exact frontmatter title, while `wiki-graph-api/graph_builder.py` accepted both title and slug or filename tail. This discrepancy led to false lint errors for links that were actually resolvable in the graph.

To address this, the lint script was updated to use the same resolution logic as the graph builder, checking for both title and slug matches. Derived artifacts, such as `wiki/meta/hot-snapshot.md`, were excluded from lint checks to prevent irrelevant failures. The updated script was then integrated with the postprocessing helpers in `scripts/auto_ingest.py`, allowing for batch normalization of links and metadata across the entire wiki corpus.

A new script, `backfill_wiki_link_cleanup.py`, was created to automate the cleanup. This script scans all pages, fixes broken links, and normalizes metadata entries, ensuring that every page is valid and interconnected. The cleanup is run across hundreds of pages (507 in this session), reducing lint errors from over 100 to zero.

The process is designed to be idempotent, so repeated runs do not introduce conflicts or regressions. It also supports exclusion of derived artifacts and handles genuine legacy broken links by either fixing them or marking them as archived. The cleanup is tracked via reports and logs, providing transparency and traceability for each change.

By aligning link resolution logic and automating cleanup, the process ensures that the wiki corpus is ready for synthesis generation, checkpoint promotion, and further architectural improvements. It eliminates manual page rewrites and supports large-scale quality recovery.

## Key Properties

- **Alignment of Resolution Logic:** Lint scripts and graph builders use identical logic for wikilink resolution, preventing false negatives.
- **Idempotent Batch Cleanup:** Cleanup scripts can be run repeatedly without introducing conflicts or regressions.
- **Full-Corpus Coverage:** All wiki pages are scanned and normalized, not just recently edited or promoted ones.
- **Exclusion of Derived Artifacts:** Artifacts like `wiki/meta/hot-snapshot.md` are excluded from lint checks, focusing cleanup on canonical content.

## Limitations

Cleanup relies on accurate resolution logic; misalignment can still produce false positives or negatives. Genuine legacy broken links may require manual intervention if they cannot be resolved automatically. Exclusion rules must be carefully defined to avoid missing important artifacts. Large corpus size can make cleanup resource-intensive.

## Example

```python
# Example: Full-Corpus Wikilink Cleanup
from scripts.backfill_wiki_link_cleanup import cleanup_links
cleanup_links(wiki_dir='wiki/')
# Result: All pages scanned, broken links fixed, lint errors reduced to zero.
```

## Visual

No explicit diagrams, but lint reports show error counts dropping from 107 to 0 after cleanup.

## Relationship to Other Concepts

- **[[Quality Evaluation of Auto-Ingested Wiki Content]]** — Cleanup is a prerequisite for accurate quality evaluation.
- **[[Wiki Deduplication and Concept Merging in LLM Wikis]]** — Cleanup supports deduplication and merging by ensuring links are valid.

## Practical Applications

Essential for maintaining large-scale LLM wiki systems, especially after bulk ingestion or legacy migration. Supports checkpoint promotion, synthesis generation, and architectural audits by ensuring all pages are valid and interconnected. Reduces manual maintenance and improves overall wiki quality.

## Sources

- [[Copilot Session Checkpoint: Phase 5 Merged; Graph UI Next]] — primary source for this concept
