---
title: "Self-Synthesizing GitHub Source Re-Ingestion Workflow"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "0a4ff72c02c43a07f603a8baab32716ef2cb63b6d31b3dd941b64676f49cd7bd"
sources:
  - raw/2026-04-22-copilot-session-mobile-node-viewer-and-richer-github-ingestion-8b1dee20.md
quality_score: 72
concepts:
  - self-synthesizing-github-source-re-ingestion-workflow
related:
  - "[[Auto-Ingest Pipeline for LLM-Powered Knowledge Wiki]]"
  - "[[Copilot Session Checkpoint: Mobile Node Viewer And Richer GitHub Ingestion]]"
tier: hot
tags: [self-synthesis, github-ingestion, provenance, deterministic]
---

# Self-Synthesizing GitHub Source Re-Ingestion Workflow

## Overview

This workflow enables deterministic, skill-driven re-ingestion of GitHub-sourced wiki pages without relying on LLMs or the GitHub Models API. It refreshes content blocks, ensures provenance, and supports reproducible documentation for knowledge graphs.

## How It Works

Implemented in `scripts/refresh_github_sources.py`, the workflow scans raw GitHub source files using Python YAML, identifies those matching the expected pattern, and re-fetches their content using the `auto_ingest.fetch_url_content` interface. The script refreshes the `<!-- fetched-content -->` block in each file via the `upsert_fetched_content_block` helper, ensuring the latest data is included.

Content is written deterministically to `wiki/sources/<owner>-<repo>.md`, with structured sections for Summary, Repository Info, README Excerpt, Activity Snapshot, and Crawled Files. The ingest method is tracked in frontmatter as `self-synthesis-no-llm`, supporting audit and provenance. The script handles rate limits by using a valid `GITHUB_TOKEN` (obtained via `gh auth token`), retrying as needed. It skips repositories with less than 200 chars of content, avoiding empty or private repos.

The workflow is validated by running smoke tests and checking API responses (e.g., `/graph/page-content/sources/midudev-autoskills` returns a 7706-char body). The graph is updated with new nodes and edges, reflecting the refreshed sources. Collisions in raw files (e.g., HKUDS/AutoAgent appearing three times) are handled by slugification, with last-write-wins behavior; deduplication is recommended for upstream raw files.

Edge cases include handling private repos, slug collisions, and legacy source pages. The workflow is robust, but follow-up scripts for deduplication and QA are suggested.

## Key Properties

- **Deterministic Re-Ingestion:** Ensures reproducible, skill-driven refresh of source pages without LLM involvement.
- **Structured Content Blocks:** Uses helpers to build and upsert fetched content blocks, maintaining consistency.
- **Provenance Tracking:** Frontmatter records ingest method, supporting audit and reproducibility.
- **Rate Limit Handling:** Uses authenticated tokens to avoid API rate limits and retries as needed.

## Limitations

Private repos are skipped if inaccessible. Slug collisions and legacy source page deduplication are not fully automated. Real-device QA is pending for mobile UI integration.

## Example

Running `python3 scripts/refresh_github_sources.py` with `GITHUB_TOKEN` set re-ingests 12 GitHub sources, refreshing their content blocks and writing deterministic wiki pages. The graph updates to reflect new nodes and edges.

## Visual

No explicit diagrams, but the workflow results in updated wiki source pages with refreshed content blocks and structured sections. These are visible in the graph UI and node viewer.

## Relationship to Other Concepts

- **[[Auto-Ingest Pipeline for LLM-Powered Knowledge Wiki]]** — Contrasts with LLM-powered ingestion by relying on deterministic, skill-driven workflows.

## Practical Applications

Supports reproducible documentation, audit, and provenance in knowledge management systems. Useful for organizations needing deterministic, skill-based ingestion of technical sources without LLMs.

## Sources

- [[Copilot Session Checkpoint: Mobile Node Viewer And Richer GitHub Ingestion]] — primary source for this concept
