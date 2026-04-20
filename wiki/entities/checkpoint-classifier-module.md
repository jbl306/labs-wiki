---
title: "Checkpoint Classifier Module"
type: entity
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "f7f84608a56ca95ea16b47740648af8c3fa8d4783f1503e8d3a6c45e0d21b558"
sources:
  - raw/2026-04-18-copilot-session-phase-5-backfill-script-written-6227b6ae.md
  - raw/2026-04-18-copilot-session-implementing-checkpoint-curation-phases-625f7a54.md
quality_score: 100
concepts:
  - checkpoint-classifier-module
related:
  - "[[Heuristic-Based Classification of Session Checkpoints]]"
  - "[[Copilot Session Checkpoint: Implementing Checkpoint Curation Phases]]"
  - "[[Copilot CLI]]"
  - "[[MemPalace]]"
tier: hot
tags: [classifier, checkpoint-curation, wiki-ingestion, python-tool]
---

# Checkpoint Classifier Module

## Overview

The checkpoint classifier module is a shared Python script implementing deterministic, regex-based classification of Copilot session checkpoints. It defines a taxonomy of checkpoint classes and retention modes, supporting cross-repo integration and durable knowledge codification in LLM Wiki systems.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | 2026 |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

Central to the checkpoint curation workflow, the classifier enforces consistent taxonomy and retention policy across labs-wiki and homelab repositories. It enables automated checkpoint promotion, filtering, and quality gate verification, supporting scalable and durable wiki ingestion.

## Associated Concepts

- **[[Heuristic-Based Classification of Session Checkpoints]]** — Implements the classification logic described in the concept.
- **Checkpoint Curation Phases for Copilot Session Promotion** — Operationalizes classification and retention phases.

## Related Entities

- **[[Copilot CLI]]** — Source of session checkpoints classified by the module.
- **[[MemPalace]]** — Checkpoint classifier is integrated into MemPalace session curator for durable promotion.

## Sources

- [[Copilot Session Checkpoint: Implementing Checkpoint Curation Phases]] — where this entity was mentioned
- [[Copilot Session Checkpoint: Phase 5 Backfill Script Written]] — additional source
