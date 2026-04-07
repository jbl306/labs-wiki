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

- Raw sources are processed by the `/wiki-ingest` pipeline
- Phase 1 (EXTRACT) reads raw sources and extracts concepts/entities
- Phase 2 (COMPILE) generates wiki pages from extracted data
- Use `status: pending` for unprocessed sources
