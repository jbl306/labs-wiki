---
applyTo: "raw/**/*.md"
---
# Raw Source Document Rules

Files in `raw/` are **immutable source documents**. They are the ground truth for the wiki.

## CRITICAL: Never Modify Raw Sources

- Files in `raw/` must NEVER be edited after initial creation
- If a source needs correction, create a new file with today's date
- The only allowed change is updating `status: pending` → `ingested` or `failed`

## Raw Source Frontmatter

```yaml
---
title: "Source Title"
type: url | text | note | file
captured: 2025-07-17T03:15:00Z
source: ios-share | browser | terminal | github-issue | ntfy | manual
url: "https://..."          # for url type
content_hash: "sha256:..."
tags: [topic, subtopic]
status: pending | ingested | failed
---
```

## Naming Convention

- Format: `YYYY-MM-DD-<descriptive-slug>.md`
- Example: `2026-04-07-attention-mechanisms-survey.md`
- Binary files go in `raw/assets/<uuid>.<ext>`

## Processing

- Raw sources are **automatically processed** by the `wiki-auto-ingest` Docker service
- The service watches `raw/` and triggers within ~5 seconds of a new file
- Processing: GPT-4.1 extracts concepts/entities → generates wiki pages → updates index/log
- **Smart URL handlers**: Twitter/X tweets, GitHub repos, HTML pages with image extraction
- **Vision support**: Charts, diagrams, and text-in-images are analyzed via GPT-4.1 multimodal
- Manual alternative: `python3 scripts/auto_ingest.py` or `/wiki-ingest` skill
- Use `status: pending` for unprocessed sources (auto-ingest only picks up pending)
