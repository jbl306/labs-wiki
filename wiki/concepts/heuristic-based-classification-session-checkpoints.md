---
title: "Heuristic-Based Classification of Session Checkpoints"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "6d9e0eba162a694001ac48a61830fb7a5d3740b481f8691d5ba2c7bd6a7488d2"
sources:
  - raw/2026-04-18-copilot-session-implementing-checkpoint-curation-phases-625f7a54.md
  - raw/2026-04-20-copilot-session-wiki-audit-followups-92b1089b.md
quality_score: 64
concepts:
  - heuristic-based-classification-session-checkpoints
related:
  - "[[Planning-Only Checkpoint Suppression in Wiki Auto-Ingest Pipelines]]"
  - "[[Copilot Session Checkpoint: Wiki Audit Followups]]"
tier: hot
tags: [heuristics, classification, checkpoint-curation, wiki-ingestion, automation]
---

# Heuristic-Based Classification of Session Checkpoints

## Overview

Heuristic-based classification is a method for categorizing Copilot session checkpoints as either planning-only or execution-based, using textual cues from titles and bodies. This enables automated suppression of non-durable content and ensures that only actionable knowledge is promoted into the wiki.

## How It Works

The classification process relies on a set of heuristics implemented in the auto-ingest pipeline. Titles are scanned for keywords such as 'planning', 'audit', 'exploration', while bodies are analyzed for phrases like '<next_steps>', 'open questions', 'plan + tracker', and 'sql todos seeded'. The absence of execution signals—such as completed implementation, tests, deployment, or merges—further reinforces the planning-only classification.

The pipeline uses these heuristics to decide whether to suppress concept/entity/synthesis extraction for a given checkpoint. If the checkpoint is classified as planning-only, only the source summary page is created. Otherwise, the pipeline proceeds with full extraction, generating durable wiki pages.

This method is robust against most conventional planning checkpoints, but may require ongoing tuning as project conventions evolve. The classification logic is centralized in `scripts/auto_ingest.py`, making it easy to update and validate. The process was tested on recent checkpoint files, confirming accurate suppression of planning-only material.

Edge cases include mixed checkpoints, where planning and execution are intertwined. The heuristics are designed to avoid suppressing content with clear evidence of completed work, but ambiguous cases may require manual review. Trade-offs involve balancing suppression accuracy with the risk of missing valuable operational knowledge.

## Key Properties

- **Keyword and Phrase Detection:** Uses textual cues in titles and bodies to classify checkpoints.
- **Automated Suppression Decision:** Enables automated suppression of non-durable content based on classification.
- **Centralized Logic:** Classification logic is centralized in the auto-ingest script for easy maintenance.

## Limitations

Ambiguous or unconventional checkpoint formats may reduce classification accuracy. Mixed checkpoints require careful tuning to avoid suppressing valuable content. Manual review may be needed for borderline cases.

## Example

A checkpoint titled 'Sprint 60 PTS Feature Planning' with body containing '<next_steps>' and no evidence of completed implementation is classified as planning-only:

```python
def is_planning_only_checkpoint(checkpoint):
    return ('planning' in checkpoint.title.lower() or
            '<next_steps>' in checkpoint.body or
            'no code changes made this session' in checkpoint.body)
```

## Relationship to Other Concepts

- **[[Planning-Only Checkpoint Suppression in Wiki Auto-Ingest Pipelines]]** — Classification is the basis for suppression logic.

## Practical Applications

Used in labs-wiki to automate checkpoint curation, ensuring only durable, actionable knowledge is promoted. Supports efficient wiki maintenance and memory management.

## Sources

- [[Copilot Session Checkpoint: Wiki Audit Followups]] — primary source for this concept
- [[Copilot Session Checkpoint: Implementing Checkpoint Curation Phases]] — additional source
