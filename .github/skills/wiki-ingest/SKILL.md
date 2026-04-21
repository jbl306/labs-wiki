---
name: wiki-ingest
description: Manually process raw sources into wiki pages (fallback — auto-ingest handles this automatically).
allowed-tools:
  - read
  - write
  - edit
  - bash
  - grep
  - glob
  - web_search
---

# /wiki-ingest

Manually process one or more raw sources from `raw/` into wiki pages. Uses a **two-phase pipeline** with hash-based incremental compilation.

> **Primary path:** The `wiki-auto-ingest` Docker sidecar automatically processes pending sources within ~5 seconds using GPT-4.1. It handles Twitter/X, GitHub repos, HTML pages, MarkItDown-backed document conversion, and images with vision support. Use this skill as a fallback for manual re-processing or quality improvements.

## Usage

```
/wiki-ingest                    # Process all pending sources in raw/
/wiki-ingest raw/2025-07-17-rope-paper.md  # Process a specific source
```

## Two-Phase Pipeline

### Phase 1: EXTRACT

Use the **Researcher** persona (`agents/researcher.md`).

1. Read the raw source file
2. Compute SHA-256 hash of the source content
3. Check if a `wiki/sources/` page already exists with the same `source_hash`
   - If hash matches → **skip** (source unchanged, no work needed)
   - If hash differs or no page exists → continue
4. Extract from the source:
   - **Concepts** — ideas, techniques, patterns (will become `wiki/concepts/` pages)
   - **Entities** — tools, people, organizations (will become `wiki/entities/` pages)
   - **Facts** — key claims, data points, quotes (will be included in pages)
   - **Relationships** — how extracted items relate to each other and existing wiki pages
5. Check existing wiki pages for overlap — avoid creating duplicate pages

### Phase 2: COMPILE

Use the **Compiler** persona (`agents/compiler.md`).

1. Create `wiki/sources/<slug>.md` using `templates/source-summary.md`
   - Always 1:1 with the raw source
   - Set `source_hash` to the computed SHA-256
   - Set `tier: hot` for new pages
2. For each new concept extracted:
   - Check if `wiki/concepts/<slug>.md` exists
   - If not → create using `templates/concept-page.md`
   - If yes → update with new information (append, don't overwrite)
3. For each new entity extracted:
   - Check if `wiki/entities/<slug>.md` exists
   - If not → create using `templates/entity-page.md`
   - If yes → update with new information
4. Add `[[wikilinks]]` in both directions between related pages
5. Update `sources:` field in all affected pages
6. Append operation to `wiki/log.md`:
   ```yaml
   - timestamp: 2025-07-17T14:30:00Z
     operation: ingest
     agent: compiler
     targets:
       - wiki/sources/rope-paper.md
       - wiki/concepts/positional-encoding.md
     source: raw/2025-07-17-rope-paper.md
     status: success
   ```
7. Rebuild `wiki/index.md` with updated page list

## Rules

- Never manually modify files in `raw/`; the only automated exception is replacing the deterministic fetched-content block for `type: url` sources or deterministic extracted-content block for `type: file` asset-backed sources, plus the `status` field
- Always check hash before processing — skip unchanged sources
- Every wiki page must have valid frontmatter (see AGENTS.md)
- Every fact must trace to a source via the `sources:` field
- Update `wiki/log.md` and `wiki/index.md` after every operation
- Mark processed raw sources by updating their `status: ingested` in frontmatter
