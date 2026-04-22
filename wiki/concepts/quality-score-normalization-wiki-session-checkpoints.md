---
title: "Quality Score Normalization for Wiki Session Checkpoints"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "aa0a9fb971c2616e13c747864ac64e29a813db353a4b28896b78d03b5dff3a2a"
sources:
  - raw/2026-04-18-copilot-session-phase-5-backfill-script-written-6227b6ae.md
quality_score: 59
concepts:
  - quality-score-normalization-wiki-session-checkpoints
related:
  - "[[Quality Evaluation of Auto-Ingested Wiki Content]]"
  - "[[Backfill Script for Copilot Session Checkpoint Curation]]"
  - "[[Copilot Session Checkpoint: Phase 5 Backfill Script Written]]"
tier: hot
tags: [quality-score, wiki-curation, metadata-evaluation, checkpoint-management]
---

# Quality Score Normalization for Wiki Session Checkpoints

## Overview

Quality score normalization is a systematic approach to evaluating and scoring Copilot session checkpoint pages based on metadata completeness, linkage, sources, and freshness. This process ensures that only high-quality pages are recommended and that archival decisions are grounded in objective criteria.

## How It Works

The quality score normalization logic is implemented in both `auto_ingest.py` and mirrored in the backfill script. The scoring formula assigns up to 100 points, distributed across four main criteria:

1. **Required Fields Ratio (25 points):** Pages are evaluated for the presence of essential metadata fields: `title`, `type`, `created`, and `sources`. The ratio of present fields to total required fields determines the score for this component.

2. **Wikilinks or Related Concepts (25 points):** If a page contains wikilinks or has related concepts, it receives full points for this criterion. This encourages interconnectedness within the wiki, improving discoverability and synthesis potential.

3. **Non-Empty Sources (25 points):** Pages with populated `sources` fields are awarded points, incentivizing proper attribution and provenance tracking.

4. **Freshness (25 points):** Pages with a `last_verified` timestamp within the past 90 days receive full points; those with just a present timestamp get 12 points. This ensures that recommendations prioritize recent and actively maintained content.

The normalization process is triggered by the backfill script, which recalculates scores for all checkpoint pages. Historically, all 52 Copilot session checkpoint pages had `quality_score: 0` due to post-processing predating the score logic. After normalization, most are expected to rise to 50–75, reflecting their metadata completeness and linkage.

Quality scores are used to filter recommendations, demote compress-tier pages to archive, and inform synthesis neighbor ratios in the wiki graph. The process is idempotent, allowing repeated recalculation as metadata evolves or new criteria are introduced.

The normalization also supports backlog reporting, enabling curators to prioritize merges, compressions, and archival actions based on objective quality metrics.

## Key Properties

- **Objective Scoring:** Scores are assigned based on explicit criteria, reducing subjective bias in curation decisions.
- **Metadata-Driven:** Relies on the presence and completeness of key metadata fields, wikilinks, sources, and freshness.
- **Idempotent Recalculation:** Scores can be recalculated safely as metadata changes, supporting ongoing maintenance.
- **Recommendation Filtering:** Quality scores are used to filter out lower-quality pages from 'hot' tier recommendations.

## Limitations

The scoring system may not capture nuanced aspects of page quality, such as depth of content or contextual relevance. Pages with minimal metadata but high substantive value could be underrated. The freshness criterion depends on accurate timestamping, which may not always reflect true content updates.

## Example

Quality score calculation pseudocode:

```python
def compute_quality_score(page):
    score = 0
    # Required fields
    required = ['title', 'type', 'created', 'sources']
    score += 25 * (sum(1 for f in required if page[f]) / len(required))
    # Wikilinks/related
    score += 25 if page['wikilinks'] or page['related'] else 0
    # Sources
    score += 25 if page['sources'] else 0
    # Freshness
    if page['last_verified'] and within_90_days(page['last_verified']):
        score += 25
    elif page['last_verified']:
        score += 12
    return score
```

## Relationship to Other Concepts

- **[[Quality Evaluation of Auto-Ingested Wiki Content]]** — Normalization is a direct implementation of quality evaluation for auto-ingested pages.
- **[[Backfill Script for Copilot Session Checkpoint Curation]]** — The backfill script triggers quality score normalization for all checkpoint pages.

## Practical Applications

Quality score normalization supports large-scale wiki maintenance, enabling curators to objectively filter, archive, and prioritize content. It is essential for recommendation systems, synthesis planning, and ensuring that wiki content remains fresh, interconnected, and well-attributed.

## Sources

- [[Copilot Session Checkpoint: Phase 5 Backfill Script Written]] — primary source for this concept
