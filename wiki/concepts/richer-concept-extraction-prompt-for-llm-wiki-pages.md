---
title: "Richer Concept Extraction Prompt for LLM Wiki Pages"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "e2f4e2c57a91e050124e6a177d9272a75a50ab4d9ee6cb6bb30f2ad73e5652bb"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-github-crawling-and-richer-extraction-a4ef6de5.md
quality_score: 100
concepts:
  - richer-concept-extraction-prompt-for-llm-wiki-pages
related:
  - "[[Auto-Ingest Pipeline for Wiki Markdown Processing]]"
  - "[[Copilot Session Checkpoint: GitHub Crawling and Richer Extraction]]"
tier: hot
tags: [llm-prompt-engineering, concept-extraction, knowledge-wiki, richer-content]
---

# Richer Concept Extraction Prompt for LLM Wiki Pages

## Overview

Enhancing the LLM extraction prompt to demand richer, more detailed concept pages improves the quality and usefulness of generated wiki content. This includes multi-paragraph explanations, specific details, limitations, examples, and visual descriptions, trading off quantity of concepts for depth and clarity.

## How It Works

The extraction prompt was rewritten to instruct the LLM to produce concept pages with 3-5 paragraphs in the 'how_it_works' section, emphasizing specifics over summaries. New fields were added to the extraction schema:

- `limitations`: Describes known weaknesses or failure modes.
- `example`: Provides concrete examples or code snippets.
- `visual_description`: Describes any relevant diagrams or images.

The concept page template was updated to conditionally render these optional sections if present.

To accommodate the richer output, the maximum token limit for LLM responses was increased from 8,000 to 16,000 tokens.

This richer prompt results in fewer concepts extracted from the same source (e.g., 10 vs 20) but with substantially more detailed and useful content. For example, the Linear Regression concept page now includes a multi-paragraph explanation, computational complexity (O(n×d²)), a scikit-learn code example, a visual description of a scatter plot, and a limitations section.

The tradeoff is increased LLM processing time, approximately 90 seconds compared to 50 seconds previously, due to the larger output size and complexity.

This approach improves the wiki's value as a knowledge resource by providing deeper understanding rather than shallow glossaries.

## Key Properties

- **Prompt Depth:** Requires 3-5 paragraphs in 'how_it_works' with specifics, not summaries.
- **New Extraction Fields:** Includes 'limitations', 'example', and 'visual_description' for richer content.
- **Token Limit:** Max tokens increased to 16,000 to support longer outputs.
- **Output Quality vs Quantity:** Fewer concepts extracted but each is richer and more useful.

## Limitations

Longer LLM processing time increases latency and resource usage. The richer prompt may require more careful prompt engineering to avoid verbosity or off-topic content. Existing orphan pages with old slugs remain and require manual cleanup to avoid confusion.

## Example

Excerpt of prompt instructions:

```
Please produce concept pages with the following fields:
- how_it_works: 3-5 paragraphs with detailed explanation
- limitations: known weaknesses or failure modes
- example: concrete example or code snippet
- visual_description: description of any diagrams or images

Use specifics and avoid shallow summaries.
```

Example snippet of generated concept content:

```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
```

## Visual

Describes a scatter plot showing linear regression fit, illustrating the relationship between variables.

## Relationship to Other Concepts

- **[[Auto-Ingest Pipeline for Wiki Markdown Processing]]** — Richer extraction is part of the auto-ingest pipeline's content generation.

## Practical Applications

Improves the educational and reference value of personal or organizational knowledge wikis by providing deeper, more actionable explanations. Useful for technical documentation, learning resources, and knowledge bases where understanding 'how' and 'why' is critical.

## Sources

- [[Copilot Session Checkpoint: GitHub Crawling and Richer Extraction]] — primary source for this concept
