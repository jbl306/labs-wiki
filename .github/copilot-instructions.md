## labs-wiki

Personal LLM-powered knowledge wiki based on [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern. Three-layer architecture: `raw/` sources → `wiki/` compiled pages → `AGENTS.md` schema.

### Architecture

```
raw/                  → Layer 1: Immutable source documents (inbox)
  assets/               Binary files (images, PDFs) from ingest API
wiki/                 → Layer 2: LLM-compiled knowledge pages
  sources/              Source summaries (1:1 with raw/)
  concepts/             Concept/technique deep-dives
  entities/             Named entities (tools, people, orgs)
  synthesis/            Cross-cutting analysis, comparisons
  index.md              Auto-generated topic-clustered catalog
  log.md                Structured audit log (YAML entries)
agents/               → Agent persona definitions
  researcher.md         Source evaluation, concept extraction
  compiler.md           Raw → wiki page compilation
  curator.md            Gap analysis, synthesis
  auditor.md            Quality scoring, staleness checks
wiki-ingest-api/      → FastAPI capture service (Docker)
templates/            → Page templates with frontmatter standards
scripts/              → Python utilities (scaffold, lint, compile_index)
docs/                 → Meta-documentation (architecture, workflows, setup)
.github/skills/       → Canonical skill location (6 skills)
.github/hooks/        → Post-edit automation hooks
.opencode/skills/     → Symlinked to .github/skills/
AGENTS.md             → Universal schema (read this for full conventions)
opencode.json         → OpenCode agent/model configuration
setup.sh              → Bootstrap: symlinks, tool configs, deps validation
```

### Wiki Conventions

**AGENTS.md is the authoritative schema.** Read it fully before any wiki operation. This file provides a quick reference.

#### Page Types

| Type | Directory | Purpose | Example |
|------|-----------|---------|---------|
| `source` | `wiki/sources/` | 1:1 summary of a raw document | `rope-paper.md` |
| `concept` | `wiki/concepts/` | Deep-dive on a technique or idea | `positional-encoding.md` |
| `entity` | `wiki/entities/` | Named thing (tool, person, org) | `pytorch.md` |
| `synthesis` | `wiki/synthesis/` | Cross-cutting comparison or analysis | `attention-vs-ssm.md` |

#### Frontmatter Standard

Every wiki page must have this frontmatter:

```yaml
---
title: "Page Title"
type: concept                   # source | concept | entity | synthesis
created: 2025-07-17
last_verified: 2025-07-17       # staleness tracking
source_hash: "a1b2c3d4"        # SHA-256 of source content
sources:                        # provenance chain — every fact traces here
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

#### Naming Rules

- Filenames: `kebab-case.md` (e.g., `positional-encoding.md`)
- Frontmatter titles: Title Case
- Wikilinks: `[[Page Title]]` format — Obsidian-compatible
- Raw sources: `YYYY-MM-DD-<slug>.md` (e.g., `2025-07-17-rope-paper.md`)

#### Consolidation Tiers

| Tier | Meaning | Example |
|------|---------|---------|
| `hot` | Recently added, not yet verified | New ingest from today |
| `established` | Verified, actively referenced | Well-linked concept page |
| `core` | Foundational knowledge, rarely changes | Architecture patterns |
| `workflow` | Operational procedures | Setup guides, how-tos |

### Ingest Workflow

Two-phase pipeline — never skip a phase:

```
Phase 1: EXTRACT
  raw/doc → hash check (skip if unchanged) → LLM extracts concepts, entities, facts

Phase 2: COMPILE
  extracted data → LLM generates wiki pages with cross-references → update index.md + log.md
```

**Rules:**
- Always check `source_hash` before reprocessing — skip unchanged sources
- One source → one `wiki/sources/` page (1:1)
- One source may create multiple concept/entity pages
- Log every operation to `wiki/log.md` with timestamp, operation type, and targets
- Update `wiki/index.md` after adding or modifying any page

#### Capture Channels

Sources reach `raw/` via a FastAPI ingest API (`wiki-ingest-api/`). See `docs/capture-sources.md` for full setup.

| Channel | Method |
|---------|--------|
| Phone (iOS/Android) | Share Sheet → ingest API |
| Browser | Bookmarklet → ingest API |
| Terminal | `wa` / `waf` shell functions → ingest API |
| GitHub | Issue with `ingest` label → Actions workflow |
| ntfy | Message → watcher script → ingest API |

Raw source frontmatter differs from wiki pages — see `templates/source-summary.md` for the raw capture format (`type: url|text|note|file`, `status: pending|ingested|failed`).

### Quality & Staleness

| Metric | Threshold | Action |
|--------|-----------|--------|
| Quality score | < 50 | Flag for review, add to lint report |
| Quality score | < 30 | Block from index until improved |
| Last verified | > 90 days | Mark as stale, add `⚠️ STALE` warning |
| Missing sources | Any | Provenance violation — must fix |
| Broken wikilinks | Any | Add to lint report |

**Quality score components:**
- Completeness (has all required frontmatter fields)
- Cross-references (links to related pages)
- Source attribution (every claim traces to a source)
- Recency (last_verified within threshold)

### Agent Personas

Use the appropriate agent persona from `agents/` for each task:

| Persona | When to Use | Primary Skills |
|---------|-------------|----------------|
| **Researcher** | Evaluating new sources, fact-checking, deep dives | `/wiki-ingest` Phase 1, `/wiki-query` |
| **Compiler** | Generating wiki pages from extracted data | `/wiki-ingest` Phase 2 |
| **Curator** | Finding gaps, creating synthesis pages, reorganizing | `/wiki-lint`, `/wiki-orchestrate` |
| **Auditor** | Quality scoring, staleness checks, broken link repair | `/wiki-lint`, `/wiki-update` |

Each persona in `agents/` defines a priority hierarchy — accuracy > completeness > attribution > brevity.

### Skills Reference

| Skill | Command | Purpose |
|-------|---------|---------|
| `wiki-setup` | `/wiki-setup` | Idempotent initialization — safe to re-run |
| `wiki-ingest` | `/wiki-ingest` | Two-phase source processing (extract → compile) |
| `wiki-query` | `/wiki-query` | Search index, read pages, synthesize answers |
| `wiki-lint` | `/wiki-lint` | Health checks: orphans, broken links, staleness, quality |
| `wiki-update` | `/wiki-update` | Revise existing pages with new information |
| `wiki-orchestrate` | `/wiki-orchestrate` | Multi-step workflows (bulk ingest, full audit) |

Skills are in `.github/skills/wiki-*/SKILL.md`. Each uses [agentskills.io](https://agentskills.io) YAML frontmatter for cross-tool compatibility.

### Toolchain

This repo is optimized for three tools that all read `AGENTS.md`:

| Tool | Config | Skills Path |
|------|--------|-------------|
| VS Code Copilot | This file + `AGENTS.md` | `.github/skills/` |
| Copilot CLI | `AGENTS.md` | `.github/skills/` |
| OpenCode | `AGENTS.md` + `opencode.json` | `.opencode/skills/` (symlinked) |

Run `./setup.sh` to create symlinks and validate tool compatibility.

#### VS Code Tips

- Use Markdown preview (`Ctrl+Shift+V`) to verify wikilinks render correctly
- Use workspace search (`Ctrl+Shift+F`) with `\[\[.*?\]\]` regex to find all wikilinks
- Install the Foam or Markdown Links extension for `[[wikilink]]` navigation
- The `[[Page Title]]` format is Obsidian-compatible — the wiki doubles as an Obsidian vault

### Validation Rules

Before committing any wiki changes:

1. **Frontmatter is valid** — all required fields present, correct types
2. **No broken wikilinks** — every `[[Link]]` resolves to an existing page
3. **No orphan pages** — every wiki page is referenced in `index.md`
4. **Provenance intact** — every wiki page has at least one entry in `sources:`
5. **Log updated** — `wiki/log.md` has an entry for the operation
6. **Index current** — `wiki/index.md` reflects all pages with one-line summaries

Run `/wiki-lint` or `python scripts/lint_wiki.py` to check all rules.

### Superpowers Integration

This project uses [obra/superpowers](https://github.com/obra/superpowers) skills:

| Situation | Skill to Invoke |
|-----------|----------------|
| Planning new wiki feature or workflow | `superpowers:brainstorming` → `superpowers:writing-plans` |
| Executing a multi-step plan | `superpowers:executing-plans` |
| Unexpected behavior during ingest/lint | `superpowers:systematic-debugging` |
| Claiming a task is complete | `superpowers:verification-before-completion` |
| Finishing a feature branch | `superpowers:finishing-a-development-branch` |
| Major implementation step done | `superpowers:code-reviewer` |
