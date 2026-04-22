---
title: "Quality Score Rubric and Its Failure Modes"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "09970c2d6bf98521e8acf64359beba6cb07e02f1015bc2504f2dd8846bbc0c93"
sources:
  - raw/2026-04-22-copilot-session-labs-wiki-full-review-report-b585f2e1.md
quality_score: 100
concepts:
  - quality-score-rubric-failure-modes
related:
  - "[[Quality Evaluation of Auto-Ingested Wiki Content]]"
  - "[[Copilot Session Checkpoint: labs-wiki full review report]]"
tier: hot
tags: [quality-control, rubric, wiki-management, evaluation]
---

# Quality Score Rubric and Its Failure Modes

## Overview

A quality score rubric is a systematic framework for evaluating wiki pages, typically used to drive editorial triage and promotion. The labs-wiki review highlights a critical failure mode: binary scoring logic that results in undifferentiated scores, undermining its purpose.

## How It Works

The labs-wiki pipeline uses `scripts/lint_wiki.py::compute_quality_score`, a binary 4×25 rubric. Each auto-ingested page is evaluated against four conditions, and if all are satisfied, the page is assigned a score of 100. The review finds that every auto-ingested page satisfies all four conditions on day one, resulting in 324 out of 327 concepts pinned at 100. This eliminates differentiation and renders the quality score useless for triage or promotion.

A robust quality score rubric should:
- **Include Multiple Dimensions**: Editorial completeness, synthesis coverage, reference density, clarity, and canonical status.
- **Allow Partial Credit**: Scores should reflect gradations, not just binary pass/fail.
- **Surface Failure Modes**: Pages failing certain dimensions are flagged for improvement.
- **Drive Editorial Action**: Scores inform triage, tier promotion, and synthesis backfill.

Edge cases arise when rubric dimensions are poorly defined or when automation cannot accurately assess nuanced editorial quality. Trade-offs include balancing rubric complexity with usability and ensuring that scoring logic evolves with the wiki's needs.

The report recommends fixing the quality score logic (R3), moving from binary to granular scoring, and integrating it with tier promotion and editorial workflows.

## Key Properties

- **Multi-Dimensional Evaluation:** Scores reflect multiple aspects of quality, not just binary conditions.
- **Granular Scoring:** Allows partial credit and nuanced differentiation between pages.
- **Editorial Integration:** Scores inform triage, promotion, and synthesis workflows.
- **Failure Mode Detection:** Flags pages that fail specific rubric dimensions for targeted improvement.

## Limitations

Binary scoring eliminates differentiation and undermines triage. Overly complex rubrics can be hard to maintain and automate. Automated scoring may miss editorial nuances, requiring human oversight.

## Example

A page on 'Random Forests' is scored on completeness (25), synthesis coverage (20), reference density (15), clarity (20), and canonical status (20). If it lacks synthesis coverage, its score is 80, flagging it for editorial backfill.

## Relationship to Other Concepts

- **[[Quality Evaluation of Auto-Ingested Wiki Content]]** — Quality score rubric is the mechanism for evaluation.

## Practical Applications

Used in automated and editorial triage of wiki content, guiding curation, promotion, and synthesis workflows. Essential for maintaining high standards in collaborative or auto-ingested knowledge bases.

## Sources

- [[Copilot Session Checkpoint: labs-wiki full review report]] — primary source for this concept
