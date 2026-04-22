---
title: "Quality Score Recalibration and Validation in Wiki Content"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "40292bde8e67742a9065472377321ae8e20a3e97bc5553b8be87b1e5dc987e85"
sources:
  - raw/2026-04-22-copilot-session-implementing-full-review-r1-r19-recommendations-884f7926.md
quality_score: 59
concepts:
  - quality-score-recalibration-validation-wiki-content
related:
  - "[[Quality Score Normalization for Wiki Session Checkpoints]]"
  - "[[Quality Evaluation of Auto-Ingested Wiki Content]]"
  - "[[Copilot Session Checkpoint: Implementing Full-Review R1-R19 Recommendations]]"
tier: hot
tags: [quality, validation, wiki, scoring, automation]
---

# Quality Score Recalibration and Validation in Wiki Content

## Overview

Quality score recalibration is the process of updating and validating the quality metrics for wiki pages based on new algorithms and criteria. This ensures that content quality is accurately reflected, supports automated validation gates, and enables data-driven improvements.

## How It Works

The recalibration process starts by rewriting the quality score computation algorithm in `scripts/lint_wiki.py`. The new `compute_quality_score` function takes into account multiple factors: inbound/outbound degree (link structure), body-length band (content size), sources count (reference richness), staleness curve (timeliness), knowledge_state (claim presence), and whether the page has a claim. The CLI flag `--write-scores` updates the `quality_score:` field in each page's frontmatter.

Prior to recalibration, pages had uniform scores (e.g., 75/100) or autostamped values (100) regardless of actual quality. After recalibration, scores are distributed across 52 distinct values, with modal buckets at 64 and 90, minimum 38, maximum 95. This distribution is validated by running `python3 scripts/lint_wiki.py --wiki-dir . --write-scores` and checking the output.

The recalibrated scores are used in API endpoints such as `/graph/health`, which reports the average quality score (dropped from 99.93 to 70.55 after recalibration). These scores also inform UI overlays and filters, enabling users to visualize and filter content based on quality metrics.

Validation is performed by running lint checks, verifying that all pages pass with zero errors, and confirming that the recalibrated scores are correctly written to frontmatter. Endpoint responses are checked to ensure that quality metrics are accurately reported and used in downstream features (e.g., semantic search, node positioning).

## Key Properties

- **Multi-Factor Scoring Algorithm:** Quality score computation incorporates link structure, content size, reference count, staleness, claim presence, and knowledge state.
- **Automated Frontmatter Update:** Scores are written directly to page frontmatter using the `--write-scores` CLI flag.
- **Validation via Lint and API Endpoints:** Lint checks and API endpoint responses are used to validate score accuracy and distribution.
- **Data-Driven UI Integration:** Scores inform UI overlays and filters, supporting quality-driven content navigation.

## Limitations

Initial recalibration may reveal previously hidden quality issues, causing average scores to drop and exposing content gaps. Requires robust validation to ensure scores are correctly written and used. Uniform autostamping (e.g., 100) can mask quality differences and must be avoided.

## Example

```python
# Recalibrate scores
python3 scripts/lint_wiki.py --wiki-dir . --write-scores
# Validate via API
curl http://127.0.0.1:8765/graph/health
# Output: avg_quality_score dropped from 99.93 to 70.55
```

## Visual

No charts included, but session notes describe score distribution: 52 distinct values, modal buckets at 64 and 90, min 38, max 95.

## Relationship to Other Concepts

- **[[Quality Score Normalization for Wiki Session Checkpoints]]** — Both address quality score computation and normalization for wiki content.
- **[[Quality Evaluation of Auto-Ingested Wiki Content]]** — Quality scores are used to evaluate and filter auto-ingested content.

## Practical Applications

Supports automated validation gates in wiki systems, enables quality-driven content navigation and filtering, and informs data-driven improvements in content management workflows.

## Sources

- [[Copilot Session Checkpoint: Implementing Full-Review R1-R19 Recommendations]] — primary source for this concept
