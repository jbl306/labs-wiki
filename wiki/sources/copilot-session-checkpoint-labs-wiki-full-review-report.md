---
title: "Copilot Session Checkpoint: labs-wiki full review report"
type: source
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "09970c2d6bf98521e8acf64359beba6cb07e02f1015bc2504f2dd8846bbc0c93"
sources:
  - raw/2026-04-22-copilot-session-labs-wiki-full-review-report-b585f2e1.md
quality_score: 100
concepts:
  - semantic-deduplication-wiki-ingest-pipelines
  - tier-promotion-workflow-wiki-systems
  - quality-score-rubric-failure-modes
  - graph-tracker-artifacts-editorial-triage
related:
  - "[[Semantic Deduplication in Wiki Ingest Pipelines]]"
  - "[[Tier Promotion Workflow in Wiki Systems]]"
  - "[[Quality Score Rubric and Its Failure Modes]]"
  - "[[Graph Tracker Artifacts and Editorial Triage]]"
  - "[[Labs-Wiki]]"
  - "[[MemPalace]]"
  - "[[Copilot CLI]]"
tier: hot
checkpoint_class: durable-architecture
retention_mode: retain
tags: [agents, copilot-session, durable-knowledge, mempalace, labs-wiki, wiki-review, agentic-workflow, quality-control, homelab, deduplication, graph-management, graph, fileback, checkpoint]
---

# Copilot Session Checkpoint: labs-wiki full review report

## Summary

This document is a comprehensive review of the labs-wiki project, covering its codebase, functionality, plans, prior reports, and alignment with Karpathy's canonical LLM Wiki pattern. The review resulted in a structured report with 19 actionable recommendations focused on wiki content, agent flow, and graph UI, highlighting both areas of faithful implementation and points of system drift. The session was strictly read-only, producing a markdown report for future reference and improvement planning.

## Key Points

- Quality score mechanism is broken, resulting in undifferentiated scores across concepts.
- Tier promotion rules are defined but not enforced, causing most pages to remain in the 'hot' tier.
- Deduplication in the ingest pipeline is insufficient, allowing near-duplicate concepts to persist.
- Graph tracker artifacts are generated but not acted upon, leaving disagreements unresolved.
- Synthesis layer is dominated by checkpoint patterns rather than topic-driven synthesis.
- Graph UI shipped as MVP only, missing planned features like advanced filters and path mode.
- Agent persona documentation is inconsistent across plans and schema files.
- Knowledge state tracking and orphan pruning are correctly implemented.

## Concepts Extracted

- **[[Semantic Deduplication in Wiki Ingest Pipelines]]** — Semantic deduplication is a process for identifying and merging conceptually similar or near-duplicate wiki pages during ingestion, beyond simple byte-identical checks. It is critical for maintaining a high-quality, non-redundant knowledge base, especially in auto-ingest pipelines where content proliferation and subtle duplication are common.
- **[[Tier Promotion Workflow in Wiki Systems]]** — Tier promotion is a structured workflow for advancing wiki pages through quality and maturity levels, such as 'hot', 'established', and 'core'. It enforces editorial standards, ensures content validation, and guides curation efforts in persistent knowledge bases.
- **[[Quality Score Rubric and Its Failure Modes]]** — A quality score rubric is a systematic framework for evaluating wiki pages, typically used to drive editorial triage and promotion. The labs-wiki review highlights a critical failure mode: binary scoring logic that results in undifferentiated scores, undermining its purpose.
- **[[Graph Tracker Artifacts and Editorial Triage]]** — Graph tracker artifacts are auto-generated reports that surface disagreements or inconsistencies in wiki graph structure, intended to drive editorial triage and resolution. The labs-wiki review finds these artifacts are shelf-ware, generated but never acted upon.

## Entities Mentioned

- **[[Labs-Wiki]]** — Labs-Wiki is a persistent knowledge base and wiki system designed for agentic workflows, code documentation, and synthesis-driven curation. It features a multi-tier structure for concepts, entities, sources, and synthesis pages, and integrates with agent personas and graph UI for editorial and technical management.
- **[[MemPalace]]** — MemPalace is a memory system and context management tool integrated with labs-wiki, supporting orphan pruning, session recall, and editorial-state tracking. It provides a 'labs_wiki' wing for context retrieval and knowledge state management.
- **[[Copilot CLI]]** — Copilot CLI is a command-line tool for managing agentic workflows, session checkpoints, and durable architecture reviews. It is used to export session checkpoints and drive review processes in labs-wiki.

## Notable Quotes

> "Quality score is broken: scripts/lint_wiki.py::compute_quality_score is a binary 4×25 rubric; every auto-ingested page satisfies all four conditions on day one → 324/327 concepts pinned at 100. Differentiation is gone." — Full Review Report
> "Tier promotion unenforced: docs/memory-model.md defines hot→established→core rules but no cron/agent runs them. 602 pages stuck in hot, only 2 established, 0 core." — Full Review Report
> "Dedupe leak in ingest: auto_ingest.py has fuzzy matching (rapidfuzz optional) but only blocks byte-identical content. Real near-duplicates pass through." — Full Review Report

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-22-copilot-session-labs-wiki-full-review-report-b585f2e1.md` |
| Type | note |
| Author | Unknown |
| Date | 2026-04-22 |
| URL | N/A |
