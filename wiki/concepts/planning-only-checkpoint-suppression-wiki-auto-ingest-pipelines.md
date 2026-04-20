---
title: "Planning-Only Checkpoint Suppression in Wiki Auto-Ingest Pipelines"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "6d9e0eba162a694001ac48a61830fb7a5d3740b481f8691d5ba2c7bd6a7488d2"
sources:
  - raw/2026-04-20-copilot-session-wiki-audit-followups-92b1089b.md
quality_score: 100
concepts:
  - planning-only-checkpoint-suppression-wiki-auto-ingest-pipelines
related:
  - "[[Quality Evaluation of Auto-Ingested Wiki Content]]"
  - "[[Durable Copilot Session Checkpoint Promotion]]"
  - "[[Karpathy Compile-Once Wiki Principle]]"
  - "[[Copilot Session Checkpoint: Wiki Audit Followups]]"
tier: hot
tags: [wiki-ingestion, planning-suppression, durable-knowledge, auto-ingest, checkpoint-curation]
---

# Planning-Only Checkpoint Suppression in Wiki Auto-Ingest Pipelines

## Overview

Planning-only checkpoint suppression is a process improvement in labs-wiki's auto-ingest pipeline that prevents the creation of concept, entity, and synthesis pages from session checkpoints containing only planning or project-progress material. This ensures that the wiki remains focused on durable, actionable knowledge rather than ephemeral planning artifacts, aligning with Karpathy-style compile-once principles for knowledge systems.

## How It Works

The auto-ingest pipeline in labs-wiki is responsible for converting Copilot session checkpoints into structured wiki pages. Historically, all checkpoints—including those focused solely on planning, audits, or project progress—were promoted into concept, entity, and synthesis pages. This led to an overabundance of pages with little actionable content, diluting the value of the wiki and making maintenance more difficult.

To address this, a heuristic was implemented in `scripts/auto_ingest.py` to detect planning-only checkpoints. The heuristic uses both title and body cues: titles containing keywords like 'planning', 'audit', 'exploration', and bodies with phrases such as '<next_steps>', 'open questions', 'plan + tracker', or 'sql todos seeded'. It also checks for the absence of execution signals, such as completed implementation, tests, deployment, or merges. If a checkpoint is classified as planning-only, the pipeline suppresses concept/entity/synthesis extraction, retaining only the source summary page.

This suppression mechanism is crucial for maintaining the quality and durability of the wiki. By filtering out ephemeral planning material, the wiki focuses on checkpoints that document real debugging, implementation, or operational changes. The process also normalizes metadata fields like `checkpoint_class`, `retention_mode`, and `tier` on checkpoint source pages, ensuring consistent classification and easier downstream processing.

The suppression logic was validated on recent checkpoint files, confirming that planning-only sessions were correctly identified and did not generate unnecessary pages. This aligns with the recommendations in `plans/copilot-session-checkpoint-curation.md`, which advocate for retaining durable checkpoints while compressing project-progress material. The approach also supports efficient memory management in MemPalace by preventing orphaned drawers linked to transient planning pages.

Edge cases include checkpoints that mix planning and execution. The heuristic is designed to avoid suppressing content with clear evidence of completed work, ensuring that valuable operational knowledge is not lost. Trade-offs involve the risk of missing some borderline cases, but the process is tuned to err on the side of durability and actionable content.

## Key Properties

- **Heuristic-Based Classification:** Uses title and body cues to identify planning-only checkpoints, including keywords and phrases indicative of project-progress material.
- **Suppression of Concept/Entity/Synthesis Extraction:** Prevents creation of non-durable wiki pages from planning-only checkpoints, retaining only the source summary.
- **Metadata Normalization:** Ensures consistent classification of checkpoint pages by normalizing fields like checkpoint_class, retention_mode, and tier.
- **Validation Coverage:** Heuristic validated on multiple checkpoint files, confirming correct suppression behavior.

## Limitations

Borderline checkpoints with mixed planning and execution may be misclassified, potentially suppressing valuable content. The heuristic relies on textual cues, so unconventional checkpoint formats or ambiguous language can reduce accuracy. Suppression is only as effective as the quality of the classification logic; ongoing tuning may be required as project conventions evolve.

## Example

Suppose a Copilot session checkpoint titled 'Sprint 61 Planning + Audit' contains only planning notes and open questions, with no code changes or deployment. The auto-ingest pipeline detects this as planning-only and suppresses concept/entity extraction, creating only a source summary page:

```python
if is_planning_only_checkpoint(checkpoint):
    suppress_concept_entity_synthesis_extraction()
    create_source_summary_page(checkpoint)
else:
    extract_concepts_entities_synthesis(checkpoint)
```

## Relationship to Other Concepts

- **[[Quality Evaluation of Auto-Ingested Wiki Content]]** — Suppression improves quality scoring by filtering out non-durable content.
- **[[Durable Copilot Session Checkpoint Promotion]]** — Suppression ensures only durable checkpoints are promoted.
- **[[Karpathy Compile-Once Wiki Principle]]** — Suppression aligns with compile-once durability goals.

## Practical Applications

Used in labs-wiki and similar knowledge systems to maintain a high-quality, durable wiki by preventing proliferation of ephemeral planning pages. Supports efficient memory management in MemPalace and reduces maintenance overhead by focusing on actionable, executed knowledge.

## Sources

- [[Copilot Session Checkpoint: Wiki Audit Followups]] — primary source for this concept
