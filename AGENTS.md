# labs-wiki — Agent Schema

> Universal schema for all AI agents operating in this repository.
> Read by: VS Code Copilot, Copilot CLI, OpenCode.

## Project Overview

labs-wiki is a personal LLM-powered knowledge wiki based on [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern. Sources go in, compiled knowledge pages come out.

### Three-Layer Architecture

```
raw/   → Layer 1: Immutable source documents (inbox)
wiki/  → Layer 2: LLM-compiled knowledge pages
AGENTS.md → Layer 3: Schema and conventions (this file)
```

---

## Wiki Conventions

### Page Types

| Type | Directory | Purpose |
|------|-----------|---------|
| `source` | `wiki/sources/` | 1:1 summary of a raw document |
| `concept` | `wiki/concepts/` | Deep-dive on a technique or idea |
| `entity` | `wiki/entities/` | Named thing (tool, person, org) |
| `synthesis` | `wiki/synthesis/` | Cross-cutting comparison or analysis |

### Naming Rules

- **Filenames:** `kebab-case.md` (e.g., `positional-encoding.md`)
- **Frontmatter titles:** Title Case (e.g., `"Positional Encoding"`)
- **Wikilinks:** `[[Page Title]]` — Obsidian-compatible
- **Raw sources:** `YYYY-MM-DD-<slug>.md` (e.g., `2025-07-17-rope-paper.md`)
- **Assets:** `raw/assets/<uuid>.<ext>` for binary files

### Wiki Page Frontmatter

Every page in `wiki/` must have this frontmatter:

```yaml
---
title: "Page Title"
type: concept                   # source | concept | entity | synthesis
created: 2025-07-17
last_verified: 2025-07-17       # staleness tracking
source_hash: "a1b2c3d4"        # SHA-256 of source content
sources:                        # provenance chain
  - raw/original-document.md
quality_score: 85               # 0-100 lint score
concepts:                       # extracted concepts for index clustering
  - concept-one
  - concept-two
related:                        # wikilinks for graph view
  - "[[Related Page]]"
tier: established               # hot | established | core | workflow
tags: [topic, subtopic]
---
```

**Required fields:** `title`, `type`, `created`, `sources`
**Auto-populated by skills:** `source_hash`, `quality_score`, `last_verified`, `concepts`, `related`

### Raw Source Frontmatter

Files in `raw/` have a different schema:

```yaml
---
title: "Source Title"
type: url                       # url | text | note | file
captured: 2025-07-17T03:15:00Z
source: ios-share               # capture channel
url: "https://..."              # for url type
content_hash: "sha256:a1b2c3..."
tags: [ml, transformers]
status: pending                 # pending | ingested | failed
---
```

### Consolidation Tiers

| Tier | Meaning | Criteria |
|------|---------|----------|
| `hot` | Recently added, not yet verified | Created within last 7 days |
| `established` | Verified, actively referenced | Has cross-references, verified within 90 days |
| `core` | Foundational knowledge | Referenced by 3+ pages, rarely changes |
| `workflow` | Operational procedures | Setup guides, how-tos, process docs |

---

## Workflows

### Ingest Workflow (`/wiki-ingest`)

Two-phase pipeline for processing raw sources into wiki pages:

**Phase 1: EXTRACT**
1. Read source from `raw/`
2. Compute SHA-256 hash — compare with `source_hash` in existing wiki page
3. If hash unchanged → skip (incremental compilation)
4. Extract: concepts, entities, facts, key claims
5. Identify which existing wiki pages are related

**Phase 2: COMPILE**
1. For each extracted concept/entity without a wiki page → create one using `templates/`
2. For existing wiki pages with new information → merge (don't overwrite, append with source attribution)
3. Create `wiki/sources/<slug>.md` — 1:1 summary of the raw source
4. Update `[[wikilinks]]` in all affected pages
5. Append operation to `wiki/log.md`
6. Rebuild `wiki/index.md`

**Rules:**
- Never modify files in `raw/` — they are immutable
- Every fact in a wiki page must trace to a source via `sources:` field
- One raw source may produce multiple wiki pages (concepts, entities)
- Always update `wiki/log.md` with timestamp, operation, and targets

### Query Workflow (`/wiki-query`)

1. Read `wiki/index.md` to identify relevant pages
2. Read identified pages
3. Synthesize answer from page content
4. Cite sources using `[[wikilinks]]`
5. If information is insufficient, say so — don't hallucinate

### Lint Workflow (`/wiki-lint`)

Check all pages in `wiki/` for:

| Check | Severity | Rule |
|-------|----------|------|
| Missing required frontmatter | Error | `title`, `type`, `created`, `sources` must exist |
| Broken wikilinks | Error | Every `[[Link]]` must resolve to an existing page |
| Orphan pages | Warning | Every page should appear in `index.md` |
| Stale pages | Warning | `last_verified` > 90 days ago |
| Missing provenance | Error | `sources:` must have at least one entry |
| Low quality score | Warning | `quality_score` < 50 flagged for review |

**Quality Score (0-100):**
- Completeness: all required frontmatter fields present (25 pts)
- Cross-references: has `related:` entries and `[[wikilinks]]` in body (25 pts)
- Source attribution: every claim traceable via `sources:` (25 pts)
- Recency: `last_verified` within 90 days (25 pts)

### Update Workflow (`/wiki-update`)

1. Identify the page to update
2. Make changes, preserving the provenance chain
3. Update `source_hash` if the underlying raw source changed
4. Bump `last_verified` to today
5. Update `related:` links if cross-references changed
6. Append operation to `wiki/log.md`

### Orchestrate Workflow (`/wiki-orchestrate`)

Multi-step coordination:
1. Scan `raw/` for `status: pending` sources → run `/wiki-ingest` on each
2. Run `/wiki-lint` → collect issues
3. Fix auto-fixable issues (rebuild index, update stale `last_verified`)
4. Report remaining issues requiring human review

---

## Index and Log Maintenance

### index.md

Auto-generated catalog of all wiki pages. Format:

```markdown
# Wiki Index

## Concepts
- [[Positional Encoding]] — How transformers encode sequence position (T1, score: 85)
- [[Attention Mechanisms]] — Multi-head attention deep-dive (T1, score: 90)

## Entities
- [[PyTorch]] — Deep learning framework by Meta (T1, score: 78)

## Sources
- [[RoPE Paper Summary]] — Summary of arxiv:2104.09864 (source, score: 72)

## Synthesis
- [[Attention vs SSM]] — Comparing attention and state-space models (synthesis, score: 88)
```

**Rules:**
- Cluster by page type (concepts, entities, sources, synthesis)
- Include one-line summary, tier, and quality score
- Sort alphabetically within each cluster
- Rebuild after every ingest or update operation

### log.md

Structured audit log. Every operation appends an entry:

```yaml
- timestamp: 2025-07-17T14:30:00Z
  operation: ingest
  agent: compiler
  targets:
    - wiki/concepts/positional-encoding.md
    - wiki/sources/rope-paper.md
  source: raw/2025-07-17-rope-paper.md
  status: success
  notes: "Created 2 new pages, updated index"
```

---

## Agent Personas

Four agent personas are defined in `agents/`. Each has:
- **Identity** — role and focus area
- **Priority Hierarchy** — ordered priorities (accuracy > completeness > attribution > brevity)
- **Activation** — which skills/workflows trigger this persona
- **Allowed Tools** — what the agent can use

| Persona | File | Primary Role |
|---------|------|-------------|
| Researcher | `agents/researcher.md` | Source evaluation, concept extraction, fact verification |
| Compiler | `agents/compiler.md` | Raw → wiki page generation, cross-referencing |
| Curator | `agents/curator.md` | Gap analysis, consolidation, synthesis creation |
| Auditor | `agents/auditor.md` | Quality scoring, staleness detection, link repair |

---

## Skills

Six skills are available in `.github/skills/wiki-*/SKILL.md`:

| Skill | Purpose |
|-------|---------|
| `wiki-setup` | Idempotent initialization — creates dirs, validates structure |
| `wiki-ingest` | Two-phase source processing (extract → compile) |
| `wiki-query` | Search index, read pages, synthesize answers |
| `wiki-lint` | Health checks: orphans, broken links, staleness, quality |
| `wiki-update` | Revise existing pages with provenance tracking |
| `wiki-orchestrate` | Multi-step workflows (bulk ingest, full audit) |

---

## Validation Rules

Before committing any changes:

1. All wiki pages have valid frontmatter with required fields
2. No broken `[[wikilinks]]` — every link resolves to an existing page
3. No orphan pages — every wiki page appears in `index.md`
4. Provenance intact — every wiki page has `sources:` with at least one entry
5. `wiki/log.md` has an entry for the operation
6. `wiki/index.md` reflects all current pages

Run `/wiki-lint` or `python scripts/lint_wiki.py` to check all rules.
