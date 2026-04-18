---
title: "Post-Ingest Quality Fixes in Auto-Ingest Pipelines"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "b63d1672165b80d7c8439cbcccceb1221f2692ca78875b666163fda03d13e59a"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-implementing-post-ingest-quality-fixes-1de9c8cc.md
quality_score: 100
concepts:
  - post-ingest-quality-fixes-auto-ingest-pipelines
related:
  - "[[Auto-Ingest Pipeline for Wiki Markdown Processing]]"
  - "[[Quality Evaluation of Auto-Ingested Wiki Content]]"
  - "[[Durable Copilot Session Checkpoint Promotion]]"
  - "[[Copilot Session Checkpoint: Implementing Post-Ingest Quality Fixes]]"
tier: hot
tags: [auto-ingest, quality-fixes, post-processing, wiki, LLM]
---

# Post-Ingest Quality Fixes in Auto-Ingest Pipelines

## Overview

Post-ingest quality fixes are critical steps applied after automatic ingestion of source content into a knowledge wiki to ensure data integrity, link validity, and overall content quality. These fixes enhance the reliability and usability of the generated wiki pages by addressing common issues such as broken links, duplicate references, and insufficient metadata.

## How It Works

The post-ingest quality fixes process involves several key mechanisms integrated into the auto-ingest pipeline:

1. **Prompt Hardening:** The language model prompt used for extraction is enhanced with strict rules to ensure provenance and accuracy. This includes prohibiting fabrication of dates, disallowing external URLs not present in the source, and restricting related concepts and entities to those extracted or existing within the source context.

2. **Richer Entity Templates:** Entity JSON schemas are expanded to include reciprocal related entities, improving cross-linking between pages. This ensures that entity pages reference each other appropriately, enhancing navigability and semantic connections.

3. **Post-Processing Function:** A dedicated function (`postprocess_created_pages()`) is introduced to validate and clean the generated wiki pages after initial creation. It performs:
   - **Wikilink Validation:** Scans the body of each page to remove any wikilinks that do not correspond to valid existing pages, preventing broken navigation.
   - **Self-Reference and Duplicate Removal:** Cleans the frontmatter related entities list by removing self-referential links and duplicate entries.
   - **Quality Scoring:** Computes a quality score for each page based on presence of required fields, cross-references, source attribution, and staleness. This score helps monitor and maintain content quality.

4. **Pipeline Integration:** The post-processing step is integrated into the main ingest pipeline, ensuring that all generated pages undergo these fixes before final indexing and logging.

5. **Permission Handling:** Since wiki files are created by a Docker sidecar process running as root, manual permission fixes (`chown`) are necessary to allow local scripts to modify files during post-processing.

This approach addresses systemic issues identified in quality evaluations, such as broken wikilinks caused by the LLM generating related links without existence checks, and thin entity pages lacking sufficient related entity prompts. By automating these fixes, the pipeline improves the accuracy, completeness, and navigability of the knowledge wiki content.

## Key Properties

- **Prompt Hardening Rules:** Includes prohibitions on external URLs not in source, no date fabrication (use null), no external citations, and limits on related concepts/entities.
- **Post-Processing Steps:** Wikilink validation, self-reference removal, duplicate related entity removal, and quality score computation.
- **Quality Score Computation:** Scores up to 100 points based on required fields, cross-references, source attribution, and staleness.
- **Pipeline Integration Point:** Post-processing occurs after page generation and before log/index/status updates.

## Limitations

The post-processing relies on accurate detection of valid page titles and may miss edge cases if the frontmatter parser or wikilink detection has limitations. Permission issues due to Docker file ownership require manual intervention, which could disrupt automation. The quality scoring is heuristic and may not fully capture semantic quality or completeness. The fixes are currently applied only to new ingests; a wiki-wide cleanup is considered but not yet implemented.

## Example

Pseudocode for post-processing function:

```python
def postprocess_created_pages(all_entities, wiki_dir):
    valid_titles = collect_all_valid_page_titles(wiki_dir)
    for page in created_pages:
        # Remove broken wikilinks in page body
        page.body = remove_links_not_in(valid_titles, page.body)
        # Clean frontmatter related entities
        page.related = remove_self_and_duplicates(page.related, page.title)
        page.related = filter_links_not_in(valid_titles, page.related)
        # Compute quality score
        page.quality_score = compute_quality_score(page)
        write_page(page)
```

This function ensures that each page is internally consistent and linked only to valid pages, improving overall wiki quality.

## Relationship to Other Concepts

- **[[Auto-Ingest Pipeline for Wiki Markdown Processing]]** — Post-ingest quality fixes are a critical step within the overall auto-ingest pipeline.
- **[[Quality Evaluation of Auto-Ingested Wiki Content]]** — Quality evaluation identifies issues that post-ingest fixes address.
- **[[Durable Copilot Session Checkpoint Promotion]]** — This checkpoint documents the durable promotion of the fixes into the labs-wiki environment.

## Practical Applications

This concept is applied in personal or organizational knowledge wiki systems that automatically ingest and generate content from diverse sources. It ensures that the resulting wiki pages are accurate, well-linked, and maintain high quality without manual cleanup. The approach is especially relevant when using LLMs for content extraction, which can produce hallucinated or broken links. Post-ingest fixes improve user experience, searchability, and maintainability of large-scale auto-generated knowledge bases.

## Sources

- [[Copilot Session Checkpoint: Implementing Post-Ingest Quality Fixes]] — primary source for this concept
