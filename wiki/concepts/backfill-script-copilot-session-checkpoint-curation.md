---
title: "Backfill Script for Copilot Session Checkpoint Curation"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "aa0a9fb971c2616e13c747864ac64e29a813db353a4b28896b78d03b5dff3a2a"
sources:
  - raw/2026-04-18-copilot-session-phase-5-backfill-script-written-6227b6ae.md
quality_score: 62
concepts:
  - backfill-script-copilot-session-checkpoint-curation
related:
  - "[[Phased Implementation Planning and Progress Tracking for LLM Wikis]]"
  - "[[Quality Evaluation of Auto-Ingested Wiki Content]]"
  - "[[Durable Copilot Session Checkpoint Promotion]]"
  - "[[Copilot Session Checkpoint: Phase 5 Backfill Script Written]]"
tier: hot
tags: [wiki-curation, checkpoint-management, quality-normalization, backfill-script, labs-wiki]
---

# Backfill Script for Copilot Session Checkpoint Curation

## Overview

The backfill script is a standalone tool designed to retroactively classify, normalize, and update Copilot session checkpoint pages in the labs-wiki. It automates the process of assigning checkpoint classes, retention modes, demoting compress-tier pages, and recalculating quality scores based on updated criteria. This script is central to Phase 5 of the checkpoint curation plan, ensuring consistency and improving the quality of wiki content.

## How It Works

The backfill script (`backfill_checkpoint_curation.py`) operates as an idempotent, stdlib-only utility for batch processing Copilot session checkpoint pages. Its primary entry point is the `main()` function, which supports both a dry-run mode and report generation via command-line flags (`--dry-run`, `--report PATH`). The script iterates over all target checkpoint files (matching `wiki/sources/copilot-session-checkpoint-*.md`), invoking `process_page(path)` for each.

Within `process_page`, the script leverages the `checkpoint_classifier` module to assign a checkpoint class and retention mode. For pages marked as 'compress', it updates their tier to 'archive', ensuring they are filtered out from 'hot' tier recommendations by downstream scripts like `build_hot.py`. Defensive logic ensures that any pages classified as 'skip' are also archived, even though historically no such pages were produced.

A critical feature is the quality score recalculation. The script mirrors the logic from `auto_ingest.py` (specifically `_compute_quality_score` at line 1529), assigning points based on:
- Required fields ratio (title, type, created, sources): 25 points
- Presence of wikilinks or related concepts: 25 points
- Non-empty sources field: 25 points
- Freshness (last_verified within 90 days): 25 points, or 12 if just present
This scoring system yields a maximum of 100, with most pages expected to land between 50–75 after backfill, given their metadata and wikilinks.

The script is designed for idempotency: it uses `upsert_fm_field` to regex-replace key lines or append them if missing, avoiding list-style values. This ensures safe repeated execution without risk of corrupting page metadata. The dry-run mode previews changes without modifying files, allowing for sanity checks before actual execution.

After the script runs, the wiki graph is rebuilt using `graph_builder.py` (with networkx and FastAPI in a dedicated venv), which recalculates checkpoint health and recommendation distributions. The expectation is that tier demotion and quality score normalization will improve the graph's synthesis neighbor ratio and filter out lower-quality pages from 'hot' tier recommendations.

The script also supports report generation, outputting a diff record per page and summarizing class/retention/score distributions. This report is intended for backlog review and planning next steps, including merging clusters and prioritizing further curation.

## Key Properties

- **Idempotency:** The script can be safely re-run multiple times, as it only replaces or appends key-value fields and avoids list-style values.
- **Quality Score Normalization:** Implements a scoring system based on required metadata, wikilinks, sources, and freshness, with a maximum score of 100.
- **Checkpoint Classification:** Uses `checkpoint_classifier` to assign checkpoint class and retention mode, demoting compress-tier pages to archive.
- **Dry-Run and Reporting:** Supports previewing changes and generating a report before actual execution, aiding verification and planning.

## Limitations

The script does not modify list-style values, which may limit its ability to handle more complex metadata structures. It relies on the accuracy of the checkpoint classifier and quality score logic, which may not capture nuanced page quality. The script does not create new synthesis pages, so synthesis neighbor ratio improvements are indirect. SQL schema issues (such as missing title constraints) must be resolved before phase gates can be properly inserted.

## Example

Example usage:

```bash
python3 scripts/backfill_checkpoint_curation.py --dry-run --report /tmp/phase5-dryrun.json
```

This command previews changes for all 52 checkpoint pages, showing which will be demoted to archive, their new quality scores, and generates a report for review.

## Relationship to Other Concepts

- **[[Phased Implementation Planning and Progress Tracking for LLM Wikis]]** — Phase 5 is part of a broader phased curation plan for labs-wiki.
- **[[Quality Evaluation of Auto-Ingested Wiki Content]]** — The backfill script directly implements quality normalization for auto-ingested pages.
- **[[Durable Copilot Session Checkpoint Promotion]]** — The script supports durable checkpoint promotion and tier demotion.

## Practical Applications

The script is used for large-scale wiki maintenance, ensuring that session checkpoints are properly classified, archived, and scored for quality. This improves the reliability of recommendations, filters out lower-quality pages, and supports ongoing curation and synthesis planning. It is particularly valuable in environments with frequent auto-ingest and evolving quality criteria.

## Sources

- [[Copilot Session Checkpoint: Phase 5 Backfill Script Written]] — primary source for this concept
