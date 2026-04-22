---
title: "Image Ranking and Extraction for Article Content"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "e5b02c64f03eff41baf89ddea2376fb47d6f03914f6c1c7d77afb1833f4012b2"
sources:
  - raw/2026-04-20-copilot-session-url-followup-pass-b53bba3e.md
quality_score: 56
concepts:
  - image-ranking-extraction-article-content
related:
  - "[[Content-Root Selection for Article Extraction]]"
  - "[[Copilot Session Checkpoint: URL Followup Pass]]"
tier: hot
tags: [image-extraction, html-parsing, wiki-ingestion, article-processing]
---

# Image Ranking and Extraction for Article Content

## Overview

Image ranking and extraction is a systematic approach to selecting the most relevant images from HTML articles, avoiding logos, icons, and unrelated thumbnails. By scoring images based on size, context, alt text, and article-locality, this method ensures that only substantive article images are included in durable wiki snapshots.

## How It Works

The image ranking and extraction process addresses the common problem of web pages containing numerous images, many of which are irrelevant to the main article (e.g., logos, app store badges, avatars, ads, or sidebar thumbnails). The extraction logic is implemented in the `scripts/auto_ingest.py` file, particularly around the `_score_img` and `extract_image_urls` functions.

The process begins by discovering all candidate images using a comprehensive set of attributes:
- `src`
- `data-src`
- `data-lazy-src`
- `data-original`
- `srcset` / `data-srcset`

Each candidate image is then scored based on several criteria:
- **Size Metadata:** Images with explicit width and height are preferred; tiny images are penalized. Size can also be parsed from URL patterns (e.g., `100x100`).
- **Contextual Relevance:** Images inside the selected article root or within a `figure` parent are given higher scores. Membership inside the article container is a strong positive signal.
- **Alt Text:** Substantive alt text increases the score, as it suggests the image is meaningful to the article.
- **Path Patterns:** Images with paths indicating logos, icons, badges, avatars, buttons, ads, promos, or trackers are penalized.
- **Article Resource Preference:** Images whose URLs match article resource paths are preferred.
- **SVG Handling:** SVG images are no longer blanket-dropped; only those that appear to be site chrome and not article-local or in-figure are penalized.

Additionally, the `og:image` meta tag is no longer blindly prepended; instead, it receives a bonus in the ranking but must compete with other images based on the scoring criteria.

After scoring, images are ranked, and the top-scoring images are selected for inclusion in the raw snapshot. This ensures that only relevant, substantive images are preserved, improving the fidelity of wiki ingestion.

Edge cases include lazy-loaded images, images with missing metadata, or articles where the main image is not marked with standard attributes. The extraction logic accounts for these by reading multiple attributes and parsing dimensions from URLs when necessary.

Trade-offs involve the risk of missing legitimate article diagrams if scoring is too aggressive, or including irrelevant images if penalties are insufficient. The process is designed to be extensible, allowing for adjustment of scoring weights and criteria as new patterns are observed.

## Key Properties

- **Multi-Attribute Image Discovery:** Extracts images using src, data-src, data-lazy-src, data-original, and srcset attributes.
- **Contextual and Size-Based Scoring:** Ranks images based on size, context (article root, figure), alt text, and path patterns.
- **Selective SVG Handling:** Penalizes SVG images only if they are non-article and appear to be site chrome.

## Limitations

Can miss images if they are not marked with recognized attributes or if scoring is too aggressive. May still include some boilerplate images if penalties are insufficient. Requires ongoing tuning as web page image patterns evolve.

## Example

```python
def _score_img(img):
    score = 0
    if img.width and img.height:
        score += img.width * img.height
    elif '100x100' in img.src:
        score -= 100  # Penalty for small size
    if img.parent.name == 'figure':
        score += 50
    if img.alt and len(img.alt) > 10:
        score += 20
    if 'logo' in img.src or 'badge' in img.src:
        score -= 200
    # ...additional scoring logic...
    return score

# Extract and rank images
images = extract_image_urls(article_root)
ranked_images = sorted(images, key=_score_img, reverse=True)
```

## Visual

No explicit diagram, but the process is illustrated in the code block and described in the session history.

## Relationship to Other Concepts

- **[[Content-Root Selection for Article Extraction]]** — Image ranking depends on accurate article-root selection to determine context and relevance.

## Practical Applications

Used in automated wiki ingestion pipelines to ensure that only relevant article images are included in durable snapshots. Critical for knowledge bases, documentation systems, and AI datasets where image fidelity impacts downstream tasks.

## Sources

- [[Copilot Session Checkpoint: URL Followup Pass]] — primary source for this concept
