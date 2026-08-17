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

> **Primary path:** The `wiki-auto-ingest` Docker sidecar automatically processes pending sources within ~5 seconds using the configured agent CLI backend (Codex CLI by default). It handles Twitter/X, GitHub repos, HTML pages, MarkItDown-backed document conversion, and images with vision support. Use this skill as a fallback for manual re-processing or quality improvements.

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

1. Create or update `wiki/sources/<slug>.md` using `templates/source-summary.md`
   - Create a new page when no canonical source page exists.
   - When another raw capture represents the same upstream document (for example an arXiv abstract URL followed by its PDF URL), update the existing canonical source page instead of creating a duplicate. Preserve prior `sources`, accumulated metadata, and the original `created` date while using the richer proposed body and current source hash.
   - Set `source_hash` to the computed SHA-256
   - Set `tier: hot` only for new pages; preserve an existing page's established tier
2. For each new concept extracted:
   - Check if `wiki/concepts/<slug>.md` exists
   - If not → create using `templates/concept-page.md`
   - If yes — including when a concurrent ingest created it after proposal generation — update it with new information while preserving prior body content, provenance, and metadata
3. For each new entity extracted:
   - Check if `wiki/entities/<slug>.md` exists
   - If not → create using `templates/entity-page.md`
   - If yes — including a same-path concurrent-ingest collision — update with new information while preserving prior body content, provenance, and metadata
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
- Treat an exact-path collision for the same titled source as an update candidate only when the current raw capture's normalized upstream identity matches the canonical page (including modern and legacy arXiv abstract/PDF IDs), or, for captures without URL identity, the source hash matches; retain every contributing raw path in `sources:`
- Require the deterministic current-raw preflight hash for every reconciled source/concept/entity collision, bind each mutation's `source_hash` to it, and never trust a model-proposed copied hash as identity proof; fail closed when the deterministic hash is absent or invalid
- Compare colliding page titles case-insensitively with whitespace normalization only; punctuation remains identity-significant (`C` and `C++` are different titles)
- Treat explicit `update` proposals as untrusted input too: require matching canonical/proposed type and title, deterministic current-raw hash and provenance, and current-raw upstream identity for source-page updates; merge accumulated provenance, metadata, and body content instead of allowing replacement
- Keep source-page provenance identity-closed: reject a canonical source with conflicting upstream identities and reject any newly proposed raw provenance that is neither the current raw nor independently normalized to the same upstream document; concepts/entities may still aggregate multiple identities
- Finalize deterministic duplicate and retention skips as observable publication outcomes: outside validation mode update the raw status, append the wiki log, require a successful manifest-scoped commit, and only then notify; on false/exception commit outcomes restore raw/log state and leave the source retryable
- Every wiki page must have valid frontmatter (see AGENTS.md)
- Every fact must trace to a source via the `sources:` field
- Update `wiki/log.md` and `wiki/index.md` after every operation
- Mark processed raw sources by updating their `status: ingested` in frontmatter
