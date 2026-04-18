---
title: "Durable Copilot Session Checkpoint Promotion"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "c65fce884e028922d59862433952d95e905dc7bcd8639c99bbaa0493de3d3fbb"
sources:
  - raw/2026-04-18-copilot-session-fixing-mempalace-timeouts-d94dbf3b.md
  - raw/2026-04-18-copilot-session-session-wiki-promotion-405414ae.md
quality_score: 100
concepts:
  - durable-copilot-session-checkpoint-promotion
related:
  - "[[Karpathy Compile-Once Wiki Principle]]"
  - "[[Agentic Wiki Optimization per Karpathy Compile-Once Principles]]"
  - "[[MemPalace]]"
  - "[[Copilot Session Checkpoint: Session Wiki Promotion]]"
tier: hot
tags: [copilot, wiki-ingestion, knowledge-management, karpathy-principle, session-curation, mempalace]
---

# Durable Copilot Session Checkpoint Promotion

## Overview

Durable Copilot session checkpoint promotion is a workflow for extracting and distilling knowledge from Copilot session checkpoints and integrating them into a persistent wiki system. This process ensures that only meaningful, curated summaries—not raw conversational transcripts—are promoted, aligning with the Karpathy compile-once principle for knowledge management.

## How It Works

The workflow begins with Copilot sessions, which generate conversational memory stored as checkpoint markdown files under `~/.copilot/session-state`. Rather than ingesting raw transcripts, the system focuses on promoting durable checkpoint summaries, which capture the distilled essence of a session's knowledge, decisions, and outcomes.

A dedicated script, `mempalace-session-curator.py`, scans these checkpoint files, computes content hashes, and exports only new or modified summaries into the wiki's `raw/` directory. This ensures that the wiki remains up-to-date with relevant session knowledge without flooding it with redundant or outdated information. The script maintains a state file in `~/.local/state/mempalace/session-curator-state.json`, tracking exported checkpoints and their hashes, and uses an `initialized_at` timestamp to avoid backfilling old checkpoints after adoption.

Once exported, these summaries are compiled into durable wiki pages using the `wiki-auto-ingest` pipeline. This pipeline leverages GitHub Models exclusively at the compile step, maintaining local-only mining, search, and graph operations. The compile step is source-aware: Copilot session checkpoints are routed through a 'light' lane, with model and character caps tailored for efficient processing. The route classifier assigns priorities, ensuring interactive sources are processed ahead of backlog.

The system also integrates with MemPalace, a memory architecture that mines session-state and bridges knowledge into the wiki. After promotion, the wiki pages are injected back into MemPalace, closing the loop and enabling retrieval and search across both systems. The workflow includes guardrails such as inflight suppression (preventing duplicate concurrent processing) and priority sorting, ensuring robustness and efficiency.

This approach is tightly aligned with Karpathy's LLM Wiki principle: conversational memory is kept raw and local, while only distilled, durable knowledge is promoted for persistent, compile-once ingestion. The process is observable, with logs and metrics tracking promotion, compilation, and injection events. Edge cases, such as permission issues or non-writable state files, are handled by relocating state and using passwordless sudo where necessary.

## Key Properties

- **Source-Aware Routing:** Checkpoints are classified by source type (e.g., Copilot session, MemPalace export, standard URL/text, image-bearing) and routed to the appropriate model lane ('light', 'default', 'vision') with tailored caps and priorities.
- **Durable Checkpoint Summaries:** Only distilled checkpoint summaries are promoted, avoiding raw transcript ingestion and ensuring persistent, meaningful wiki entries.
- **Priority Queueing and Inflight Suppression:** Pending raw files are sorted by route priority, and an in-memory inflight set prevents duplicate concurrent processing.
- **Compile-Once Principle:** Mining, search, and graph operations are local-only; only the compile step calls GitHub Models, maximizing efficiency and minimizing external dependency.

## Limitations

The workflow depends on accurate checkpoint summarization; if session summaries are incomplete or poorly distilled, important knowledge may be lost. The system requires careful state management to avoid backfilling or missing new checkpoints. Permission issues or misconfigured environment variables can disrupt promotion or compilation. The approach assumes that durable summaries are preferable to raw transcripts, which may not suit all use cases.

## Example

Example workflow:

1. Copilot session generates checkpoint markdown at `~/.copilot/session-state/7b3d52f4-aa5d-4c83-b782-5fb7570f5498/checkpoints/002-session-wiki-promotion.md`.
2. `mempalace-session-curator.py` scans, hashes, and exports the summary to `~/projects/labs-wiki/raw/2026-04-18-copilot-session-002-session-wiki-promotion.md`.
3. `wiki-auto-ingest` compiles the raw summary into a durable wiki page using GitHub Models.
4. The compiled page is injected back into MemPalace for retrieval.
5. Logs and metrics track the promotion, compilation, and injection events.

## Visual

No diagrams or charts are present in the source.

## Relationship to Other Concepts

- **[[Karpathy Compile-Once Wiki Principle]]** — Implements the principle by promoting only distilled, durable knowledge for persistent ingestion.
- **[[Agentic Wiki Optimization per Karpathy Compile-Once Principles]]** — Optimizes agent workflows to align with compile-once knowledge management.
- **[[MemPalace]]** — Acts as the memory mining and bridging architecture for session knowledge.

## Practical Applications

This workflow is ideal for teams or individuals managing persistent knowledge bases, ensuring that only meaningful, curated session knowledge is promoted for long-term reference. It supports efficient compile-time ingestion, minimizes redundant data, and enables robust retrieval across conversational and wiki systems. The approach is particularly suited for environments with strict model boundaries (e.g., Copilot Pro+ / GitHub Models-only) and aligns with best practices for agentic documentation and knowledge distillation.

## Sources

- [[Copilot Session Checkpoint: Session Wiki Promotion]] — primary source for this concept
- [[Copilot Session Checkpoint: Fixing MemPalace Timeouts]] — additional source
