# labs-wiki — Agent Schema

> Universal schema for all AI agents operating in this repository.
> Read by: VS Code Copilot, Copilot CLI, OpenCode.

## Project Overview

labs-wiki is a personal LLM-powered knowledge wiki based on [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern. Sources go in, compiled knowledge pages come out. The LLM incrementally builds and maintains a persistent wiki — a structured, interlinked collection of markdown pages that compounds over time.

> "The wiki is a persistent, compounding artifact." — The key difference from RAG: knowledge is compiled once and kept current, not re-derived on every query.

### Three-Layer Architecture

```
raw/       → Layer 1: Source documents + durable URL/file snapshots (inbox)
wiki/      → Layer 2: LLM-compiled knowledge pages (the artifact)
AGENTS.md  → Layer 3: Schema, conventions, and workflows (this file)
```

- **Layer 1** is your source of truth — agents preserve captured content and may only update `status` plus the deterministic fetched-content block for `type: url` sources and deterministic extracted-content block for `type: file` asset-backed sources
- **Layer 2** is LLM-owned — it creates, updates, and maintains everything here
- **Layer 3** is co-evolved — you and the LLM refine the schema as patterns emerge

### How Sources Enter the Wiki

```
Android Share / Browser / CLI / API
        │
        ▼
  wiki-ingest-api (FastAPI, Docker)
        │
        ▼
  raw/YYYY-MM-DD-<slug>.md  (status: pending)
        │
        ▼
  wiki-auto-ingest (Docker sidecar, file watcher)
        ├── Detects new pending file (~5s)
        ├── Smart URL fetch (Twitter/GitHub/HTML+vision)
        ├── LLM extraction via GPT-4.1 (GitHub Models API)
        ├── Generates wiki pages from templates
        ├── Updates index, log, cross-references
        └── Marks raw source → status: ingested
```

**Primary path:** Fully automated. Drop a source → wiki pages appear.
**Manual fallback:** `/wiki-ingest` skill or `python3 scripts/auto_ingest.py` for targeted re-processing.

### Services

| Service | Container | Purpose |
|---------|-----------|---------|
| `wiki-ingest-api` | Docker | HTTP API for capturing sources into `raw/` |
| `wiki-auto-ingest` | Docker sidecar | Watches `raw/`, auto-processes pending sources via GPT-4.1 |

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
**Auto-populated by auto-ingest/skills:** `source_hash`, `quality_score`, `last_verified`, `concepts`, `related`

### Raw Source Frontmatter

Files in `raw/` have a different schema:

```yaml
---
title: "Source Title"
type: url                       # url | text | note | file
captured: 2025-07-17T03:15:00Z
source: android-share           # capture channel
url: "https://..."              # for url type
content_hash: "sha256:a1b2c3..."
tags: [ml, transformers]
status: pending                 # pending | ingested | failed
---
```

`type: url` sources may also carry a deterministic `fetched-content` block, and
`type: file` sources that reference `raw/assets/...` may carry a deterministic
`extracted-content` block. Those blocks are owned by the automation layer and
hold the durable markdown body used for wiki compilation.

### Consolidation Tiers

| Tier | Meaning | Criteria |
|------|---------|----------|
| `hot` | Recently added, not yet verified | Created within last 7 days |
| `established` | Verified, actively referenced | Has cross-references, verified within 90 days |
| `core` | Foundational knowledge | Referenced by 3+ pages, rarely changes |
| `workflow` | Operational procedures | Setup guides, how-tos, process docs |

---

## Workflows

### Auto-Ingest (Primary Path)

The `wiki-auto-ingest` Docker service handles source processing automatically:

1. File watcher detects new/modified `.md` in `raw/` with `status: pending`
2. **Smart URL fetch** based on URL type:
   - **Twitter/X** (twitter.com, x.com, t.co) → fxtwitter API for tweet text, author, media URLs
   - **GitHub repos** (github.com/owner/repo) → REST API for metadata + README
   - **GitHub gists** → raw content fetch
   - **HTML pages** → fetch + structure-aware normalization + og:image/img extraction
   - **Document binaries** (PDF, DOCX, PPTX, XLSX/XLS, EPUB) → MarkItDown conversion to markdown
3. **Vision processing** — downloads images (tweet photos, og:image), base64-encodes them, sends as multimodal content to GPT-4.1
4. **LLM extraction** (GitHub Models, source-aware lanes) → structured JSON: concepts, entities, source summary
5. **Page generation** from templates → source page + concept pages + entity pages
6. **Cross-referencing** — bidirectional `[[wikilinks]]` between related pages
7. **Index + log** — rebuilds `wiki/index.md`, appends to `wiki/log.md`
8. **Raw snapshot update** — URL sources persist a deterministic fetched-content block back into `raw/`; file sources pointing at `raw/assets/...` persist document extraction in a deterministic extracted-content block
9. **Status update** — marks raw source `status: ingested`
10. **Notification** — sends ntfy alert on success/failure

**Model routing:** session checkpoints / MemPalace exports → light text lane; standard sources → default lane; image-bearing sources → vision lane
**Config:** `GITHUB_MODELS_TOKEN`, `GITHUB_MODELS_MODEL_DEFAULT`, `GITHUB_MODELS_MODEL_LIGHT`, `GITHUB_MODELS_MODEL_VISION`, `GITHUB_MODELS_MODEL_OVERRIDE`, `DEBOUNCE_SECONDS`

### Manual Ingest (`/wiki-ingest`)

For targeted re-processing or when auto-ingest is not running:

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

**Deterministic checkpoint refresh:**
- For Copilot checkpoint raws that already contain durable structured summaries,
  prefer `python3 scripts/reprocess_checkpoint_raws.py` when you need to refresh
  `wiki/sources/copilot-session-checkpoint-*.md` without calling the GitHub
  Models compile path.

**Post-Ingest Entity Enrichment:**

After ingesting new sources, run `python3 scripts/enrich_entity_facts.py` to deterministically backfill null/Unknown values in the Key Facts tables of entity pages. The enricher:
- Parses each `wiki/entities/*.md` and identifies missing values (Created, Creator, URL, Status)
- Scans linked source pages for frontmatter (source_url, publication date, authors)
- Applies heuristics: GitHub URLs → Creator field; arxiv IDs → Created date; Google Research blog → Creator = "Google Research"
- No LLM calls — purely deterministic, stateless enrichment
- Reports stats: `enriched N entities, M fields filled`

This is useful after manual ingest or when sources already have rich metadata that can be extracted deterministically.

**Rules:**
- Never manually rewrite files in `raw/`; the only automated edits are `status` updates plus replacement of the deterministic fetched-content block for `type: url` sources and deterministic extracted-content block for `type: file` asset-backed sources
- Every fact in a wiki page must trace to a source via `sources:` field
- One raw source may produce multiple wiki pages (concepts, entities)
- Always update `wiki/log.md` with timestamp, operation, and targets, **unless running in `--validation-run` mode** (review-only reruns suppress log and notification noise)

### Validation-Run Mode

Use `--validation-run --force` (and optionally `--refresh-fetch`) for review-only reruns of a single raw
file, such as verifying improved extraction or image ranking after a follow-up pass. Behavior:

- Updates the raw fetched-content block and wiki pages as normal
- **Suppresses** `wiki/log.md` append and ntfy notifications
- Default production ingest path is unchanged; `--validation-run` must be passed explicitly

### Query Workflow (`/wiki-query`)

1. Read `wiki/index.md` to identify relevant pages
2. Read identified pages
3. Synthesize answer from page content
4. Cite sources using `[[wikilinks]]`
5. If information is insufficient, say so — don't hallucinate
6. **Good answers can be filed back as wiki pages** — comparisons, analyses, and connections should compound in the knowledge base

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

Multi-step coordination (note: auto-ingest handles pending sources automatically):

1. Run `/wiki-lint` → collect issues
2. Fix auto-fixable issues (rebuild index, update stale `last_verified`)
3. Delegate gap analysis to **Wiki Curator** for synthesis opportunities
4. Report remaining issues requiring human review

Orchestrate modes:
- `audit` — full quality audit with auto-fix
- `maintenance` — stale page review + tier promotion + index rebuild
- `ingest` — manually process any remaining pending sources (fallback)

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
- Rebuilt automatically after every ingest operation

### log.md

Structured audit log. Every operation appends an entry:

```yaml
- timestamp: 2025-07-17T14:30:00Z
  operation: ingest
  agent: auto-ingest
  targets:
    - wiki/concepts/positional-encoding.md
    - wiki/sources/rope-paper.md
  source: raw/2025-07-17-rope-paper.md
  status: success
  notes: "Created 2 new pages, updated index"
```

---

## Agent Personas

Seven agent specs are defined in `.github/agents/`. These are Copilot-format agent definitions with YAML frontmatter (name, description, tools, model).

| Agent | File | Primary Role |
|-------|------|-------------|
| wiki-capture | `.github/agents/wiki-capture.agent.md` | Quick-capture URLs/text into `raw/` |
| wiki-ingest | `.github/agents/wiki-ingest.agent.md` | Manual two-phase pipeline fallback |
| wiki-query | `.github/agents/wiki-query.agent.md` | Search and synthesize answers |
| wiki-lint | `.github/agents/wiki-lint.agent.md` | Quality audit, broken links, staleness |
| wiki-update | `.github/agents/wiki-update.agent.md` | Revise pages, preserve provenance |
| wiki-curator | `.github/agents/wiki-curator.agent.md` | Gap analysis, synthesis, consolidation |
| wiki-orchestrate | `.github/agents/wiki-orchestrate.agent.md` | Multi-step maintenance workflows |

---

## Skills

Project skills live in `.github/skills/` and include the cross-cutting
`task-observer` meta-skill alongside the wiki workflows:

| Skill | Purpose |
|-------|---------|
| `task-observer` | Observe task sessions, capture skill improvements, and drive proactive skill maintenance |
| `wiki-setup` | Idempotent initialization — creates dirs, validates structure |
| `wiki-ingest` | Manual source processing (fallback when auto-ingest unavailable) |
| `wiki-query` | Search index, read pages, synthesize answers |
| `wiki-lint` | Health checks: orphans, broken links, staleness, quality |
| `wiki-update` | Revise existing pages with provenance tracking |
| `wiki-orchestrate` | Audit, maintenance, and gap analysis workflows |

**Routing guide:**
- Task-oriented session start / skill maintenance? → `task-observer`
- Wiki sources / pages / quality? → wiki-* skills above
- Agent system / prompts? → context-engineering skills

## Task Observer Meta-Skill

- Install `task-observer` under `.github/skills/task-observer/`; OpenCode mirrors the same skill through `.opencode/skills/`.
- Invoke `task-observer` at the start of every task-oriented session before other skill or tool work.
- When loading any skill, check `skill-observations/log.md` for `OPEN` observations tagged to that skill and apply them during the current task.
- When `task-observer` surfaces safe, concrete improvements to local skills or instructions, update them in the same session and rerun `python3 /home/jbl/projects/update_opencode_skills_paths.py`.

---

## MemPalace — MANDATORY Session Protocol

Agents operating in this repo must query MemPalace before answering. Relevant wings: `labs_wiki` (~2200 drawers, ingest & pipeline content) and `labs_wiki_knowledge` (~150 drawers, curated knowledge).

**Session start:**
1. `mempalace_status`
2. `mempalace_search(query=<topic>, wing="labs_wiki")`
3. `mempalace_search(query=<topic>, wing="labs_wiki_knowledge")`
4. `mempalace_search(query=<topic>, wing="copilot_sessions")`
5. `mempalace_kg_query(entity=<name>)` for named things

**Recall split:** Use MemPalace for episodic recall: recent decisions, who said what, prior changes, and session history. Before fresh research on any cross-project topic, pattern, concept, or comparison, call `wiki_search`, then `wiki_read` for the canonical page. Do not preload wiki page lists or indexes into instruction files.

**During work:** `mempalace_add_drawer(wing="labs_wiki", room=<domain>, content=<verbatim>)` for significant findings. Use `mempalace_kg_add` / `mempalace_kg_invalidate` when facts change.

**End of session:** `mempalace_diary_write(agent_name="<agent>", entry=<AAAK summary>)`.

Never store secrets or credentials.

## Context-Engineering Skill Routing

- Agent instructions, prompt templates, and skill packaging → `context-fundamentals`, `tool-design`, `filesystem-context`
- Multi-agent wiki orchestration, memory flows, or hosted automation → `multi-agent-patterns`, `memory-systems`, `hosted-agents`, `project-development`, `latent-briefing`
- Context-debugging, compression, or evaluation loops → `context-degradation`, `context-compression`, `context-optimization`, `evaluation`, `advanced-evaluation`

## Validation Rules

Before committing any changes:

1. All wiki pages have valid frontmatter with required fields
2. No broken `[[wikilinks]]` — every link resolves to an existing page
3. No orphan pages — every wiki page appears in `index.md`
4. Provenance intact — every wiki page has `sources:` with at least one entry
5. `wiki/log.md` has an entry for the operation
6. `wiki/index.md` reflects all current pages

Run `/wiki-lint` or `python scripts/lint_wiki.py` to check all rules.

---

## Post-task hook: lessons.md

Any agent finishing a debugging session, an incident response, a corrective
follow-up, or any task where a user issued a correction **must** append a
lesson entry to `tasks/lessons.md` before declaring the task complete.

This file is the cross-session memory layer that keeps the same mistake from
recurring. Treat the append as part of the task definition of done — not as
optional cleanup.

Format follows [`.github/context/lesson-format.md`](../.github/context/lesson-format.md)
(linked authoritative spec). Each entry must include the following keys:

- **Date** — ISO date of the lesson
- **Pattern** — what went wrong or what was corrected
- **Root cause** — the actual underlying reason, not just the symptom
- **Prevention rule** — concrete, actionable rule to avoid recurrence
- **Affected files** — specific paths involved
- **Category** — one of: `architecture`, `convention`, `api`, `testing`, `tooling`, `knowledge-curation`, `auto-ingest`, `infrastructure`, `agents`, `other`

Never store secrets in a lesson. Never delete or rewrite existing entries —
the file is append-only.
