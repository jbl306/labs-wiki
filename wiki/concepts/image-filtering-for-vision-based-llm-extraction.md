---
title: "Image Filtering for Vision-Based LLM Extraction"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "e2f4e2c57a91e050124e6a177d9272a75a50ab4d9ee6cb6bb30f2ad73e5652bb"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-github-crawling-and-richer-extraction-a4ef6de5.md
quality_score: 100
concepts:
  - image-filtering-for-vision-based-llm-extraction
related:
  - "[[Auto-Ingest Pipeline for Wiki Markdown Processing]]"
  - "[[Copilot Session Checkpoint: GitHub Crawling and Richer Extraction]]"
tier: hot
tags: [image-filtering, vision-api, llm-extraction, ingest-pipeline]
---

# Image Filtering for Vision-Based LLM Extraction

## Overview

Image filtering improves the quality and success of vision-based LLM extraction by excluding unsupported or irrelevant image formats such as SVGs and site chrome images (logos, favicons, badges). This prevents ingestion failures and reduces noise in extracted content.

## How It Works

The vision API used (GPT-4.1 via GitHub Models) accepts only specific image MIME types: PNG, JPEG, WEBP, and GIF. SVG images cause 400 errors that fail retries because the same unsupported images are repeatedly sent.

To address this, a two-layer filtering system was implemented:

1. **URL Pattern Filtering:** Skips images whose URLs match patterns associated with logos, icons, favicons, badges, avatars, or SVG files. This prevents common site chrome images from being processed.

2. **MIME Type Whitelist:** After downloading images, only those with MIME types in the whitelist (`image/png`, `image/jpeg`, `image/webp`, `image/gif`) are passed to the vision API. Others, including SVGs, are rejected.

This filtering ensures that only vision-compatible images are processed, preventing ingestion failures and improving pipeline robustness.

Additionally, the system collects the first image from `og:image` meta tags, which sometimes bypasses URL pattern filtering. This may allow small site favicons to pass, which could be addressed in the future by size-based filtering.

The filtering changes led to successful ingestion of a GeeksforGeeks ML algorithms article that previously failed due to SVG logos.

## Key Properties

- **Supported MIME Types:** PNG, JPEG, WEBP, GIF only; SVGs and others rejected.
- **URL Pattern Filtering:** Skips images with URLs matching logo/icon/favicon/badge/avatar/svg patterns.
- **Error Prevention:** Prevents 400 errors from vision API caused by unsupported image formats.

## Limitations

Does not currently filter images based on size or dimensions, allowing some small favicons to pass. The first image from `og:image` meta tags is not filtered by URL pattern, which may introduce unwanted images. Future improvements could add size-based heuristics or more sophisticated filtering.

## Example

Example of MIME whitelist check in image download function:

```python
_VISION_MIMES = {"image/png", "image/jpeg", "image/webp", "image/gif"}

if image_mime_type not in _VISION_MIMES:
    skip_image()
else:
    process_image()
```

## Relationship to Other Concepts

- **[[Auto-Ingest Pipeline for Wiki Markdown Processing]]** — Image filtering is part of the auto-ingest pipeline's content processing.

## Practical Applications

Improves reliability of LLM vision-based extraction in knowledge ingestion pipelines by preventing failures due to unsupported image formats. Useful in any automated content ingestion system that integrates images for richer wiki or documentation pages.

## Sources

- [[Copilot Session Checkpoint: GitHub Crawling and Richer Extraction]] — primary source for this concept
