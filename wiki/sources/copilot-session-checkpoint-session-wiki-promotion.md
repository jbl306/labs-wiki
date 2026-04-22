---
title: "Copilot Session Checkpoint: Session Wiki Promotion"
type: source
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "c65fce884e028922d59862433952d95e905dc7bcd8639c99bbaa0493de3d3fbb"
sources:
  - raw/2026-04-18-copilot-session-session-wiki-promotion-405414ae.md
quality_score: 87
concepts:
  - durable-copilot-session-checkpoint-promotion
  - source-aware-model-routing-wiki-ingestion-pipelines
related:
  - "[[Durable Copilot Session Checkpoint Promotion]]"
  - "[[Source-Aware Model Routing in Wiki Ingestion Pipelines]]"
  - "[[MemPalace]]"
  - "[[Karpathy Compile-Once Wiki Principle]]"
tier: hot
tags: [mempalace, checkpoint, agents, knowledge-management, nba-ml-engine, wiki-ingestion, efficiency, model-routing, labs-wiki, homelab, fileback, durable-knowledge, graph, karpathy-principle, session-curation, copilot, copilot-session]
checkpoint_class: durable-debugging
retention_mode: retain
knowledge_state: validated
---

# Copilot Session Checkpoint: Session Wiki Promotion

## Summary

This checkpoint documents a multi-phase workflow for promoting durable Copilot session knowledge into a Karpathy-style labs-wiki, focusing on efficient compile-time ingestion using GitHub Models. The process involved UI improvements, graph deduplication, agent upgrades, and the implementation of a session-curator script to bridge Copilot checkpoints into the wiki. The technical details emphasize source-aware routing, priority queueing, and local-only mining/search, aligning with Karpathy's compile-once principle.

## Key Points

- Durable Copilot session checkpoints are promoted into labs-wiki for compile-once ingestion.
- Mobile-friendly graph UI and wiki deduplication were implemented, addressing structural and community splits.
- A session-curator script was developed to export checkpoint summaries, with source-aware routing and priority queueing for efficient GitHub Models usage.

## Concepts Extracted

- **[[Durable Copilot Session Checkpoint Promotion]]** — Durable Copilot session checkpoint promotion is a workflow for extracting and distilling knowledge from Copilot session checkpoints and integrating them into a persistent wiki system. This process ensures that only meaningful, curated summaries—not raw conversational transcripts—are promoted, aligning with the Karpathy compile-once principle for knowledge management.
- **[[Source-Aware Model Routing in Wiki Ingestion Pipelines]]** — Source-aware model routing is a technique for dynamically assigning incoming raw knowledge sources to specialized model lanes during wiki ingestion. By classifying sources (e.g., Copilot session checkpoints, MemPalace exports, standard text, images), the system optimizes compile-time efficiency and ensures appropriate model selection and resource allocation.

## Entities Mentioned

- **[[MemPalace]]** — MemPalace is a memory mining and bridging architecture used to extract, curate, and inject knowledge from Copilot session-state and wiki sources. It acts as the central hub for mining conversational memory, exporting durable checkpoint summaries, and reinjecting compiled wiki pages for robust retrieval and search.
- **[[Karpathy Compile-Once Wiki Principle]]** — The Karpathy Compile-Once Wiki Principle advocates for a persistent knowledge base where conversational memory is kept raw and local, while only distilled, durable knowledge is promoted for compile-once ingestion. This principle guides the design of efficient, agentic wiki systems and aligns with best practices for knowledge management.

## Notable Quotes

> "Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion." — Session Checkpoint Overview
> "The overall strategy was: keep mining/search/graph/retrieval local, promote only durable checkpoint summaries from Copilot sessions into raw, and use GitHub Models only for the compile step that turns raw sources into durable wiki pages." — Durable Session Summary

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-18-copilot-session-session-wiki-promotion-405414ae.md` |
| Type | note |
| Author | Unknown |
| Date | 2026-04-18 |
| URL | N/A |
