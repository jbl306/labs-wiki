---
title: "Copilot Session Checkpoint: Auto-ingest fix + arxiv loop"
type: source
created: '2026-04-22'
last_verified: '2026-04-22'
source_hash: "2891509eeeb6f460f36e066b83e7d36224ed3b0603e0d3b84da6ffc73ecc97ed"
sources:
  - raw/2026-04-22-copilot-session-auto-ingest-fix-arxiv-loop-4990d381.md
concepts:
  - deterministic-key-facts-autofill-wiki-ingestion-pipelines
related:
  - "[[Deterministic Key Facts Autofill in Wiki Ingestion Pipelines]]"
  - "[[Post-Ingest Quality Fixes in Auto-Ingest Pipelines]]"
  - "[[Source-Aware Model Routing in Wiki Ingestion Pipelines]]"
  - "[[scripts/auto_ingest.py]]"
  - "[[GitHub Models API]]"
  - "[[ReasoningBank]]"
  - "[[Labs-Wiki]]"
  - "[[Homelab]]"
tags: [copilot-session, checkpoint, durable-knowledge, labs-wiki, auto-ingest, arxiv, debugging, metadata]
tier: hot
checkpoint_class: durable-debugging
retention_mode: retain
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 74
---

# Copilot Session Checkpoint: Auto-ingest fix + arxiv loop

## Summary

This debugging checkpoint captures a multi-part investigation into the Labs-Wiki ingest stack after sparse entity Key Facts and a crashing `wiki-auto-ingest` container surfaced together. It records the confirmed crash cause, the follow-on arXiv retry loop on paper `2509.25140`, and a concrete proposal for deterministic metadata repair so URL, Creator, and Created fields can be filled more reliably without depending on [[GitHub Models API]].

## Key Points

- **Crash root cause**: the running `wiki-auto-ingest` image was missing `bs4`, even though `beautifulsoup4>=4.12.0` was already present in `scripts/requirements-auto-ingest.txt`; rebuilding the wiki stack resolved the container restart loop.
- **Primary code surface**: the checkpoint identifies [[scripts/auto_ingest.py]] as the key file because it imports `BeautifulSoup`, owns the arXiv URL handler, and contains the `call_llm` / `call_llm_synthesis` paths that currently route through GitHub Models.
- **Follow-on failure**: after rebuild, the container stayed up but repeatedly retried `https://arxiv.org/html/2509.25140`, indicating an arXiv HTML fallback path that was not terminating cleanly when HTML was unavailable.
- **Watcher seam**: `scripts/watch_raw.py` is called out as the place to inspect whether a failed raw is re-queued indefinitely instead of being marked failed or backed off.
- **No-GitHub-Models constraint**: the checkpoint notes that manual recovery of the pending ReasoningBank and arXiv raws would require a deterministic or subagent-driven path because the default pipeline's extraction calls are bound to [[GitHub Models API]].
- **Workflow improvement proposal**: add a deterministic post-processing pass that repairs missing Key Facts in entity pages after extraction instead of relying only on prompt quality.
- **Heuristic 1**: if an entity has no URL and the raw source URL clearly refers to that entity, reuse the source URL as the entity URL.
- **Heuristic 2**: if the source URL is a GitHub repository and the entity title matches the repo, infer Creator from the repository owner.
- **Heuristic 3**: if the source is arXiv and `created_year` is missing, derive the year from the arXiv identifier prefix rather than leaving the Key Facts table sparse.
- **Operational context**: the checkpoint was prompted by two newly added sources, including [[ReasoningBank]], and ties ingestion reliability directly to durable knowledge quality in [[Labs-Wiki]].

## Key Concepts

- Deterministic Key Facts Autofill in Wiki Ingestion Pipelines
- Post-Ingest Quality Fixes in Auto-Ingest Pipelines
- Source-Aware Model Routing in Wiki Ingestion Pipelines
- Durable Copilot Session Checkpoint Promotion

## Related Entities

- **[[scripts/auto_ingest.py]]** — Core ingest script where the crash, arXiv fallback behavior, and metadata autofill seam all converge.
- **[[GitHub Models API]]** — Model endpoint the existing pipeline depends on for extraction and the dependency the checkpoint tries to bypass for reprocessing.
- **[[ReasoningBank]]** — One of the new raw sources whose processing status motivated the debugging pass.
- **[[Labs-Wiki]]** — The knowledge base whose ingest quality and operational resilience this checkpoint is trying to improve.
- **[[Homelab]]** — Deployment environment where the wiki services were rebuilt and observed after the crash fix.
