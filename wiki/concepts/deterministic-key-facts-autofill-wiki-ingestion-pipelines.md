---
title: "Deterministic Key Facts Autofill in Wiki Ingestion Pipelines"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "2891509eeeb6f460f36e066b83e7d36224ed3b0603e0d3b84da6ffc73ecc97ed"
sources:
  - raw/2026-04-22-copilot-session-auto-ingest-fix-arxiv-loop-4990d381.md
related:
  - "[[Post-Ingest Quality Fixes in Auto-Ingest Pipelines]]"
  - "[[Auto-Ingest Pipeline for Wiki Markdown Processing]]"
  - "[[Source-Aware Model Routing in Wiki Ingestion Pipelines]]"
  - "[[Durable Copilot Session Checkpoint Promotion]]"
tier: hot
tags: [wiki-ingestion, metadata, post-processing, heuristics, auto-ingest, key-facts]
quality_score: 65
---

# Deterministic Key Facts Autofill in Wiki Ingestion Pipelines

## Overview

Deterministic Key Facts autofill is a metadata-repair technique for wiki ingestion systems that fills missing entity fields such as URL, Creator, and Created using explicit source-derived heuristics rather than another language-model call. In the checkpoint that introduced it, the technique is proposed as a hardening layer for Labs-Wiki after sparse Key Facts tables and a no-GitHub-Models recovery requirement made purely prompt-based extraction too fragile. It matters because it improves provenance and completeness while keeping the repair step auditable, cheap, and repeatable.

## How It Works

The core problem is straightforward: an ingest pipeline may successfully generate a page body, yet still leave the Key Facts table thin because certain fields were not extracted confidently enough. In Labs-Wiki, the entity schema already pushes the model to avoid fabrication by leaving `created_year`, `creator`, or `url` as `null` unless the source states them clearly. That protects against hallucination, but it also creates a second failure mode: the wiki accumulates many sparse entities even when the raw source or source URL contains enough structured evidence to recover the missing data deterministically.

Deterministic autofill inserts a repair pass after extraction and before the final page write, or immediately after page generation as part of a post-processing step. Instead of asking a model to "try again," the repair layer reads fields that are already present in the raw source frontmatter and combines them with narrow rules tied to known source families. In the checkpoint, the target fields were exactly the ones required by the entity Key Facts table: URL, Creator, and Created. The intent is not to infer arbitrary new knowledge, but to harvest structured facts the system already has in hand.

The first heuristic uses the raw source URL as the entity URL when the source is obviously about that entity. For example, if the raw frontmatter contains a `url:` or `source_url:` field and the normalized entity title aligns with the URL slug, then the pipeline can safely populate `entity.url` from that source URL. This is especially useful for article pages, research project pages, or single-tool GitHub repositories where the source itself is the canonical landing page. The important design constraint is conservatism: the autofill should only fire when the entity-source match is strong enough to avoid attaching a generic site URL to the wrong entity.

The second heuristic targets GitHub repository sources. If the raw source URL resolves to `github.com/<owner>/<repo>` and the extracted entity corresponds to that repository, the pipeline can derive two durable facts without another model round trip: the URL is the repository URL, and the creator is the repository owner. That does not claim that the owner is the sole human author of every line of code; it encodes the more limited and operationally useful fact that the repository is published under that owner namespace. This is valuable because many ingest pages describe tools, frameworks, or scripts whose public identity is inseparable from the repository that hosts them.

The third heuristic handles arXiv identifiers. arXiv IDs encode submission timing in the first four digits: `YYMM`. Given an ID like `2509.25140`, the pipeline can derive a year-month pair with

$$
\text{year} = 2000 + \text{int}(YY), \qquad \text{month} = \text{int}(MM)
$$

If the wiki schema only stores a year, the repair pass should preserve the coarse fact and write `2025` rather than fabricating a full publication date. This is a good example of deterministic enrichment staying inside the system's epistemic boundary: it extracts a real timestamp signal embedded in the identifier, but it does not pretend to know acceptance date, conference date, or journal publication date.

Operationally, the pass should run even when the original extractor returns `null` for these fields. That makes it different from ordinary validation. Validation only checks whether a field is present or missing; deterministic autofill actively repairs missing fields from known-safe evidence. In practice, the checkpoint proposes running this as a dedicated pass adjacent to `generate_entity_page()` so that the resulting frontmatter is corrected before quality scoring, log updates, and downstream graph ingestion. This is important because later stages should see the repaired page as the canonical artifact, not as a page that still requires manual cleanup.

The approach also improves recovery under model constraints. When the user explicitly wanted reprocessing without [[GitHub Models API]], deterministic autofill offered a path to preserve quality for at least a subset of fields without external inference. Combined with manual or rule-based content extraction, it creates a hybrid ingestion mode: models can still do the hard semantic work when available, but known-safe metadata does not need to pay model latency, cost, or quota. That makes the overall pipeline more resilient under outages, rate limits, or policy restrictions.

The technique works best when each heuristic is narrow, inspectable, and source-family-specific. A good autofill rule should answer three questions cleanly: what evidence triggers it, what field does it populate, and what ambiguity causes it to abstain? That abstention behavior is part of the design. The point is not to maximize filled fields at any cost; it is to reduce avoidable sparsity while preserving traceable provenance. In that sense, deterministic Key Facts autofill is a specialized extension of [[Post-Ingest Quality Fixes in Auto-Ingest Pipelines]] and a complement to [[Source-Aware Model Routing in Wiki Ingestion Pipelines]]: routing decides how to process a source, while autofill decides how to repair structured metadata when the source type exposes reliable patterns.

## Key Properties

- **Source-grounded repair**: Populates fields only from information already present in frontmatter, URL structure, or source-family conventions.
- **Low-cost execution**: Avoids extra model calls for metadata that can be derived deterministically.
- **Selective abstention**: Leaves fields blank when the title-to-source match is weak or the source family offers no safe rule.
- **Pipeline-friendly placement**: Fits naturally between extraction and final write, or inside a post-processing pass before quality scoring.
- **Improved resilience**: Preserves Key Facts quality even during model outages, rate limits, or manual no-LLM reprocessing.

## Limitations

Deterministic autofill is only as good as its trigger conditions. A weak title-to-URL match can attach the wrong URL to an entity, especially for broad landing pages or collections. GitHub owner inference captures namespace ownership, not necessarily authorship, so it can overstate "Creator" if the wiki intends that field to mean lead human author rather than publishing organization. arXiv-derived dates are approximate and should not be promoted beyond the precision actually encoded in the ID. More broadly, the method only repairs structured metadata; it cannot replace semantic extraction of overview text, relationships, or nuanced chronology.

## Examples

A conservative implementation can look like this:

```python
def autofill_key_facts(entity, raw_meta):
    source_url = raw_meta.get("url") or raw_meta.get("source_url")

    if not entity.url and source_url and slug_matches_title(source_url, entity.title):
        entity.url = source_url

    if not entity.creator and is_github_repo_url(source_url):
        owner, repo = parse_github_repo(source_url)
        if repo_matches_title(repo, entity.title):
            entity.creator = owner

    if not entity.created_year and is_arxiv_url(source_url):
        arxiv_id = extract_arxiv_id(source_url)  # e.g. 2509.25140
        entity.created_year = 2000 + int(arxiv_id[:2])

    return entity
```

For an arXiv source like `https://arxiv.org/pdf/2509.25140`, this logic can safely recover `created_year = 2025` even if the extractor left it blank. For a GitHub repo source like `https://github.com/google-research/reasoning-bank`, it can reuse the repo URL and infer creator `google-research` when the entity is clearly the repository-backed project.

## Practical Applications

This technique is useful in personal or team wikis that ingest heterogeneous sources at high volume, especially when entity pages must meet a fixed Key Facts schema. It is particularly effective for repository-backed tools, arXiv papers, and checkpoint-driven operational artifacts where the raw frontmatter already carries reliable structured metadata. It also supports fallback ingestion modes that deliberately avoid LLM calls, making it a good fit for quota-sensitive, privacy-sensitive, or outage-tolerant pipelines.

## Related Concepts

- **[[Post-Ingest Quality Fixes in Auto-Ingest Pipelines]]**: Deterministic autofill is a focused metadata-repair phase inside a broader post-processing discipline.
- **[[Auto-Ingest Pipeline for Wiki Markdown Processing]]**: The main orchestration pipeline provides the insertion point for the autofill pass.
- **[[Source-Aware Model Routing in Wiki Ingestion Pipelines]]**: Routing determines which sources are likely to benefit from specialized deterministic heuristics.
- **[[Durable Copilot Session Checkpoint Promotion]]**: Checkpoint raws often contain structured operational metadata that deterministic autofill can reuse directly.
