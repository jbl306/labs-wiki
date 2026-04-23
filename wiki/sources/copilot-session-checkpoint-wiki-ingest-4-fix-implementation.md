---
title: "Copilot Session Checkpoint: Wiki Ingest Pipeline 4-Fix Implementation"
type: source
created: '2026-04-22'
last_verified: '2026-04-22'
source_hash: e1abec72ac6d1d4aced535dcadb22b76009a9cea5bca69c6840036ee63725044
sources:
  - raw/2026-04-22-copilot-session-wiki-ingest-pipeline-4-fix-implementation-6262ab1b.md
concepts:
  - jsonl-sidecar-kg-fact-replay-containerized-ingest
  - automatic-git-commits-after-successful-wiki-ingest
  - source-aware-model-routing-wiki-ingestion-pipelines
related:
  - "[[JSONL Sidecar Knowledge-Graph Fact Replay for Containerized Ingest Pipelines]]"
  - "[[Automatic Git Commits After Successful Wiki Ingest]]"
  - "[[Source-Aware Model Routing in Wiki Ingestion Pipelines]]"
  - "[[scripts/replay_kg_facts.py]]"
  - "[[scripts/auto_ingest.py]]"
  - "[[MemPalace]]"
tags: [copilot-session, labs-wiki, auto-ingest, mempalace, knowledge-graph, git-automation, copilot-cli]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 65
checkpoint_class: durable-architecture
checkpoint_class_rule: "body:graph-api"
retention_mode: retain
---

# Copilot Session Checkpoint: Wiki Ingest Pipeline 4-Fix Implementation

## Summary

This checkpoint records a hardening pass on the Labs-Wiki `wiki-auto-ingest` pipeline after an evaluation found three operational gaps: synthesis pages were under-produced, MemPalace facts could not be written from the container, and successful ingests stopped at file generation instead of committing durable results. The implementation adds a JSONL-based deferred knowledge-graph handoff, automatic wiki commits on success, and effort auto-routing that defaults to `medium` but escalates PDF sources to `high`.

## Key Points

- **Evaluation-driven fixes**: The session began with a review of live ingest quality and identified missing synthesis generation, missing MemPalace fact writes, stale on-disk graph artifacts, and over-aggressive default reasoning effort for ordinary HTML sources.
- **Prompt hardening for synthesis**: `scripts/prompts/wiki_ingest_prompt.md` was updated so synthesis pages are now the default when two or more same-family concepts are created, instead of only when an ingest bridges already-existing pages.
- **Deferred KG write path**: Because the `wiki-auto-ingest` container cannot call MemPalace MCP tools directly, ingests now append fact payloads to `wiki/.kg-pending.jsonl` for later host-side replay.
- **Replay worker added**: A new host utility, [[scripts/replay_kg_facts.py]], drains the JSONL sidecar and writes triples through `mempalace.knowledge_graph.KnowledgeGraph.add_triple`.
- **Dual replay strategy**: `scripts/auto_ingest.py` now prefers HTTP replay if `MEMPALACE_API_URL` exists, falls back to direct Python replay if the `mempalace` package is available, and otherwise leaves pending lines intact for the host cron job.
- **Automatic durability step**: Successful ingests now stage only `wiki/` and `raw/`, create a Git commit with the Copilot co-author trailer, and skip cleanly if there is nothing new to commit.
- **Effort auto-routing**: `_compute_effort_for_raw()` inspects `url`, `source`, and file type so PDF raws are promoted to `high` effort while ordinary markdown and HTML sources use `medium`.
- **Deployment detail**: `homelab/compose/compose.wiki.yml` changed `${WIKI_INGEST_EFFORT:-xhigh}` to `${WIKI_INGEST_EFFORT:-}` so the script's auto-routing logic is not masked by an environment default.
- **Validation signal captured**: The redeployed container showed `WIKI_INGEST_EFFORT=` in its environment and logged `effort=medium` for an in-flight markdown checkpoint, confirming that the new routing path was active.
- **Open verification items remained**: At checkpoint time, synthesis emission on a live ingest, JSONL append behavior, host-side KG drain, and PDF-to-`high` routing still needed end-to-end confirmation.

## Key Concepts

- [[JSONL Sidecar Knowledge-Graph Fact Replay for Containerized Ingest Pipelines]]
- [[Automatic Git Commits After Successful Wiki Ingest]]
- [[Source-Aware Model Routing in Wiki Ingestion Pipelines]]
- [[Post-Ingest Quality Fixes in Auto-Ingest Pipelines]]

## Related Entities

- **[[scripts/replay_kg_facts.py]]** — Host-side worker that drains pending KG facts and writes them into [[MemPalace]] outside the restricted ingest container.
- **[[scripts/auto_ingest.py]]** — The pipeline entrypoint where the new success-path hooks, effort routing, and replay logic were wired together.
- **[[MemPalace]]** — The downstream temporal knowledge graph that could not be reached directly from the container and therefore motivated the JSONL sidecar pattern.
- **[[Copilot CLI]]** — The compile backend whose reasoning effort is now routed by source type rather than fixed globally.
- **[[Homelab]]** — The deployment environment where the compose default was cleared and the rebuilt `wiki-auto-ingest` service was validated.
