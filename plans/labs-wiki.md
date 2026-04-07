# labs-wiki — Implementation Plan (v3)

## Problem Statement

Build a personal LLM-powered wiki (labs-wiki) that functions as a **living second brain** — combining Karpathy's LLM Wiki compilation pattern with persistent memory management and multi-agent orchestration. Optimized for **VS Code (Copilot), Copilot CLI, and OpenCode**.

This plan synthesizes the best elements from:
- **Karpathy's LLM Wiki** — three-layer compile pattern (raw → wiki → schema)
- **Top 10 community implementations** — incremental compilation, lint, context cost optimization
- **rohitg00/agentmemory** — 4-tier memory pipeline, hybrid retrieval, staleness tracking, provenance
- **NicholasSpisak/second-brain** — idempotent wizard setup, multi-platform skill distribution, Obsidian integration
- **NicholasSpisak/claude-code-subagents** — 76+ specialized agent personas, priority hierarchies, orchestration patterns

## Target Toolchain

| Tool | Role | Config Discovery |
|------|------|-----------------|
| **VS Code + Copilot** | Primary IDE — editing, browsing, Obsidian-like preview | `.github/copilot-instructions.md`, `.github/skills/`, `.github/hooks/` |
| **Copilot CLI** | Terminal agent — ingest, query, lint operations | `AGENTS.md`, `.github/skills/`, `~/.copilot/` |
| **OpenCode** | Alt terminal agent — multi-model orchestration | `AGENTS.md`, `.opencode/skills/`, `opencode.json` |

### Config Compatibility Strategy

All three tools read `AGENTS.md` at the repo root — the **universal schema**. Skills follow the [Agent Skills standard](https://agentskills.io) (`SKILL.md` with YAML frontmatter) and are symlinked into each tool's discovery path via `setup.sh`.

```
AGENTS.md                        ← Read by ALL three tools (universal schema)
.github/copilot-instructions.md  ← VS Code Copilot always-on instructions
.github/skills/wiki-*/SKILL.md   ← Copilot CLI + VS Code skill discovery
.opencode/skills/wiki-*/SKILL.md ← OpenCode skill discovery (symlinked)
```

---

## Research Summary

### Source 1: Karpathy's Core Pattern
Three layers: **Raw sources** (immutable docs) → **Wiki** (LLM-compiled Markdown) → **Schema** (AGENTS.md conventions). Operations: Ingest, Query, Lint. Key insight: knowledge is compiled once and kept current, not re-derived on every query.

### Source 2: Top 10 Community Implementations

| Repo | Stars | Key Strength |
|------|-------|-------------|
| sdyckjq-lab/llm-wiki-skill | 145 | Multi-platform adapter, web scraping |
| Ar9av/obsidian-wiki | 127 | 6+ agent compatibility via symlinks |
| atomicmemory/llm-wiki-compiler | 101 | Standalone TS CLI, hash-based incremental compile |
| ussumant/llm-wiki-compiler | 100 | 90% context cost reduction, Claude plugin |
| lewislulu/llm-wiki-skill | 62 | Best reference docs, Python lint/scaffold scripts |
| Astro-Han/karpathy-llm-wiki | 60 | Simplest single-skill, lowest learning curve |
| lucasastorian/llmwiki | 36 | Full-stack SaaS, MCP server, Supabase |
| kfchou/wiki-skills | 27 | Claude marketplace plugin distribution |
| tashisleepy/knowledge-engine | 19 | Wiki + Memvid semantic memory bridge, <5ms search |
| toolboxmd/karpathy-wiki | ref | Dual-mode (general + project), hook-driven |

### Source 3: rohitg00/agentmemory (Key Architecture Insights)

A production-grade persistent memory system for AI coding agents. **627 tests, 43 MCP tools, 103 REST endpoints.** Core innovations worth adapting:

| Pattern | What It Does | Labs-Wiki Adaptation |
|---------|-------------|---------------------|
| **4-tier pipeline** | Observe → Compress → Store → Retrieve | Raw source → Extract concepts → Wiki page → Query answer |
| **Hybrid retrieval** | BM25 + vector + knowledge graph, fused via RRF@K=60 | Start with BM25 (index.md), add vector when wiki exceeds ~100 pages |
| **Staleness tracking** | Cascading invalidation when source material changes | Frontmatter `source_hash` — flag stale pages when raw source is updated |
| **Provenance chain** | Every memory traces back to raw observation via `sourceObservationIds` | Every wiki page links back to `raw/` source via frontmatter `sources:` |
| **Quality scoring** | LLM output scored 0-100, retry if below threshold | Lint skill validates page quality (completeness, accuracy, cross-refs) |
| **Consolidation tiers** | Working → Episodic → Semantic → Procedural | Hot pages (recent) → Established pages → Core concepts → Workflows |
| **Ebbinghaus decay** | `S(t) = strength × e^(-t/λ)` for memory freshness | Page `last_verified` date — lint flags pages not reviewed in 90+ days |
| **Audit trail** | Every operation logged with timestamp, function, targets | `log.md` already covers this — enhance with structured YAML entries |

### Source 4: NicholasSpisak/second-brain

An LLM-maintained Obsidian wiki with 4 installable skills. Key innovations:

| Pattern | What It Does | Labs-Wiki Adaptation |
|---------|-------------|---------------------|
| **Idempotent wizard** | `/second-brain` skill walks through 5-step vault setup | `/wiki-setup` skill — non-destructive initialization |
| **Multi-agent config gen** | Auto-generates CLAUDE.md, AGENTS.md, .cursor/rules/ | `setup.sh` generates all tool configs from single source |
| **`qmd` search integration** | Optional fast local markdown search CLI | Add as optional dependency for large wikis |
| **Web Clipper pipeline** | Obsidian Web Clipper → `raw/` folder auto-ingest | Support URL sources in ingest skill |
| **Skill distribution via npm** | `npx skills add second-brain` | Future: publish skills as npm package |
| **Sub-organized wiki** | `wiki/sources/`, `wiki/entities/`, `wiki/concepts/`, `wiki/synthesis/` | Adopt subdirectory structure for better navigation |

### Source 5: NicholasSpisak/claude-code-subagents

76+ YAML-defined specialized agent personas across 13 categories. Key patterns:

| Pattern | What It Does | Labs-Wiki Adaptation |
|---------|-------------|---------------------|
| **Priority hierarchies** | Each agent has ranked priorities (e.g., UX > a11y > perf) | Wiki agents: accuracy > completeness > brevity |
| **Context-aware activation** | Domain keywords auto-trigger appropriate specialist | Skill routing: "ingest" → ingest skill, "outdated" → update skill |
| **Orchestrator agent** | `product-manager-orchestrator` coordinates multi-agent workflows | `/wiki-orchestrate` meta-skill for complex operations |
| **Evidence-based emphasis** | Every recommendation cites sources, frameworks, measurements | Wiki pages require `sources:` frontmatter with citations |
| **Agent categories** | `core/`, `research/`, `design/`, `ops/`, etc. | Agent personas: `researcher`, `compiler`, `curator`, `auditor` |
| **Pure markdown specs** | No build step — agents defined as `.md` files | Agent personas as `.md` in `agents/` directory |

---

## Merged Feature Set (Best-of-Breed)

### Tier 1: Core (Must-Have)

| # | Feature | Origin | Description |
|---|---------|--------|-------------|
| 1 | Three-layer architecture | Karpathy | `raw/` → `wiki/` → schema (AGENTS.md) |
| 2 | Hash-based incremental compilation | atomicmemory | SHA-256 of source content in frontmatter; skip unchanged |
| 3 | Two-phase ingest pipeline | atomicmemory + agentmemory | Phase 1: concept extraction → Phase 2: page generation |
| 4 | Structured audit log | Karpathy + agentmemory | `log.md` with YAML entries (timestamp, operation, targets, status) |
| 5 | Index with summaries | Karpathy | `index.md` — one-line summary per page, LLM-navigable |
| 6 | Health lint system | all repos | Orphans, broken wikilinks, missing frontmatter, stale pages |
| 7 | Wikilink cross-references | universal | `[[concept]]` linking, Obsidian-compatible |
| 8 | Portable Agent Skills | agentskills.io | SKILL.md with YAML frontmatter, cross-tool compatible |
| 9 | Provenance tracking | agentmemory | Every wiki page traces to source via `sources:` frontmatter |
| 10 | Staleness detection | agentmemory | `source_hash` + `last_verified` — flag pages when source changes |

### Tier 2: Enhanced (Should-Have)

| # | Feature | Origin | Description |
|---|---------|--------|-------------|
| 11 | Idempotent setup wizard | second-brain | `/wiki-setup` skill — safe to re-run, non-destructive |
| 12 | Sub-organized wiki | second-brain | `wiki/sources/`, `wiki/concepts/`, `wiki/entities/`, `wiki/synthesis/` |
| 13 | Multi-tool bootstrap | Ar9av + second-brain | `setup.sh` creates symlinks, generates tool configs |
| 14 | Agent personas | subagents | `agents/researcher.md`, `agents/compiler.md`, `agents/auditor.md` |
| 15 | Orchestrator meta-skill | subagents | `/wiki-orchestrate` — coordinates multi-step workflows |
| 16 | Quality scoring | agentmemory | Lint scores pages 0-100 on completeness, accuracy, cross-refs |
| 17 | Context cost optimization | ussumant | Topic clustering in index.md — 90% token savings on queries |
| 18 | Hook-driven automation | toolboxmd + agentmemory | Post-edit hooks trigger index rebuild, drift detection |

### Tier 3: Advanced (Nice-to-Have)

| # | Feature | Origin | Description |
|---|---------|--------|-------------|
| 19 | Freshness decay | agentmemory | Ebbinghaus-inspired: pages not verified in 90+ days flagged |
| 20 | Consolidation tiers | agentmemory | Hot (recent) → Established → Core → Workflow classification |
| 21 | Hybrid retrieval | agentmemory | BM25 first; add vector search when wiki > 100 pages |
| 22 | Web/URL extraction | sdyckjq-lab + second-brain | Ingest from URLs, not just local files |
| 23 | Obsidian integration | Karpathy + second-brain | Graph view, Dataview frontmatter, vault config |
| 24 | OpenMemory MCP bridge | homelab | Connect wiki to existing homelab OpenMemory service |
| 25 | Python utility scripts | lewislulu | `scaffold.py`, `lint_wiki.py`, `compile_index.py` for offline/CI |

---

## Proposed Architecture

```
labs-wiki/
├── README.md                         # Project overview, quickstart, architecture diagram
├── LICENSE                           # MIT
├── AGENTS.md                         # Universal schema (read by all 3 tools)
├── opencode.json                     # OpenCode agent/model configuration
├── setup.sh                          # Bootstrap: symlinks, tool configs, deps validation
│
├── raw/                              # Layer 1: Immutable source documents
│   └── .gitkeep
│
├── wiki/                             # Layer 2: LLM-compiled knowledge pages
│   ├── index.md                      # Auto-generated catalog (topic-clustered)
│   ├── log.md                        # Structured audit log (YAML entries)
│   ├── sources/                      # Source summaries (1:1 with raw/)
│   ├── concepts/                     # Concept/technique deep-dives
│   ├── entities/                     # Named entities (tools, people, orgs)
│   └── synthesis/                    # Cross-cutting analysis, comparisons
│
├── agents/                           # Agent persona definitions (subagents pattern)
│   ├── researcher.md                 # Deep research, source evaluation
│   ├── compiler.md                   # Raw → wiki page compilation
│   ├── curator.md                    # Cross-referencing, gap analysis
│   └── auditor.md                    # Quality scoring, staleness checks
│
├── .github/                          # VS Code Copilot + Copilot CLI
│   ├── copilot-instructions.md       # Always-on Copilot instructions
│   ├── skills/                       # Canonical skill location
│   │   ├── wiki-setup/
│   │   │   └── SKILL.md             # /wiki-setup — idempotent initialization
│   │   ├── wiki-ingest/
│   │   │   └── SKILL.md             # /wiki-ingest — two-phase source processing
│   │   ├── wiki-query/
│   │   │   └── SKILL.md             # /wiki-query — search & synthesize
│   │   ├── wiki-lint/
│   │   │   └── SKILL.md             # /wiki-lint — health + quality scoring
│   │   ├── wiki-update/
│   │   │   └── SKILL.md             # /wiki-update — revise with provenance
│   │   └── wiki-orchestrate/
│   │       └── SKILL.md             # /wiki-orchestrate — multi-step workflows
│   └── hooks/                        # Copilot lifecycle hooks
│       └── post-edit.json            # Auto-actions after wiki edits
│
├── .opencode/                        # OpenCode (symlinked from .github/skills)
│   └── skills/ → ../.github/skills   # Symlink — single source of truth
│
├── scripts/                          # Utility scripts (offline/CI use)
│   ├── scaffold.py                   # Initialize wiki structure
│   ├── lint_wiki.py                  # Standalone lint (broken links, orphans, staleness)
│   └── compile_index.py              # Rebuild index.md with topic clustering
│
├── templates/                        # Page templates with frontmatter standards
│   ├── source-summary.md             # Template for raw/ → wiki/sources/ pages
│   ├── concept-page.md               # Template for concept deep-dives
│   ├── entity-page.md                # Template for named entities
│   └── synthesis-page.md             # Template for cross-cutting analysis
│
└── docs/                             # Meta-documentation
    ├── architecture.md               # How labs-wiki works (mermaid diagrams)
    ├── memory-model.md               # Staleness, provenance, quality scoring
    ├── workflows.md                  # Ingest, query, lint, update workflows
    ├── obsidian-setup.md             # Obsidian vault integration guide
    └── tool-setup.md                 # VS Code, Copilot CLI, OpenCode setup
```

### Wiki Page Frontmatter Standard

Every wiki page includes structured frontmatter (adapted from agentmemory's provenance pattern):

```yaml
---
title: "RoPE Positional Encoding"
type: concept                        # source | concept | entity | synthesis
created: 2025-07-17
last_verified: 2025-07-17            # staleness tracking (agentmemory)
source_hash: "a1b2c3d4"             # SHA-256 of source content (incremental compilation)
sources:                             # provenance chain (agentmemory)
  - raw/arxiv-rope-paper.pdf
  - raw/karpathy-lecture-notes.md
quality_score: 85                    # 0-100 lint score (agentmemory)
concepts:                            # extracted concepts (agentmemory compression)
  - positional-encoding
  - transformer-architecture
  - sequence-length-generalization
related:                             # wikilinks for graph view
  - "[[Transformer Architecture]]"
  - "[[Attention Mechanisms]]"
tier: established                    # hot | established | core | workflow (agentmemory)
tags: [ml, architecture, nlp]
---
```

### Two-Phase Ingest Pipeline

Adapted from atomicmemory's compiler + agentmemory's observe→compress pattern:

```
Phase 1: EXTRACT (observe + compress)
┌──────────┐    ┌──────────────┐    ┌───────────────┐
│ raw/doc  │ →  │ Hash check   │ →  │ LLM extracts  │
│ (source) │    │ (skip if     │    │ concepts,      │
│          │    │  unchanged)  │    │ entities, facts│
└──────────┘    └──────────────┘    └───────────────┘

Phase 2: COMPILE (store)
┌───────────────┐    ┌──────────────┐    ┌──────────────┐
│ Extracted     │ →  │ LLM generates│ →  │ Update       │
│ concepts &    │    │ wiki pages   │    │ index.md +   │
│ entities      │    │ with cross-  │    │ log.md       │
│               │    │ references   │    │              │
└───────────────┘    └──────────────┘    └──────────────┘
```

### Agent Personas

Inspired by NicholasSpisak/claude-code-subagents. Each persona is a markdown file in `agents/` defining:

```markdown
# Researcher Agent

## Identity
You are a deep research specialist focused on source evaluation and knowledge extraction.

## Priority Hierarchy
1. Accuracy — verify claims against primary sources
2. Completeness — extract all relevant concepts and entities
3. Attribution — every fact traces to a source
4. Brevity — concise but not at the expense of accuracy

## Activation
Triggered by: /wiki-ingest (Phase 1), /wiki-query (deep research mode)

## Allowed Tools
Read, Grep, Glob, Bash (curl), Web search
```

Four core personas:
- **Researcher** — source evaluation, concept extraction, fact verification
- **Compiler** — raw → wiki page generation, cross-referencing, index maintenance
- **Curator** — gap analysis, consolidation, synthesis page creation
- **Auditor** — quality scoring, staleness detection, broken link repair

### Tool-Specific Config Details

**AGENTS.md** (universal — all tools read this):
- Wiki conventions, page formats, naming rules
- Ingest/query/lint/update/orchestrate workflow definitions
- Index and log maintenance rules
- Frontmatter standards (provenance, staleness, quality)
- Agent persona references

**`.github/copilot-instructions.md`** (VS Code Copilot):
- Compact always-on instructions pointing to AGENTS.md
- VS Code-specific behaviors (Markdown preview, workspace search)

**`opencode.json`** (OpenCode):
- Agent definitions: primary wiki-maintainer + research subagent
- Model assignments (primary on gpt-5.1-codex, research on sonar-pro)
- Tool permissions (write, edit, bash enabled for primary agent)

**Skill portability:**
- Skills authored once in `.github/skills/` (Copilot canonical path)
- Symlinked to `.opencode/skills/` for OpenCode discovery
- All SKILL.md files use agentskills.io YAML frontmatter

---

## Implementation Todos

### Phase 1: Foundation
- `repo-setup` — Create directory structure, LICENSE, .gitignore
- `readme` — README with architecture diagram, quickstart, memory model overview
- `schema` — AGENTS.md universal schema (conventions, workflows, frontmatter standards)
- `copilot-instructions` — .github/copilot-instructions.md for VS Code
- `opencode-config` — opencode.json agent/model configuration
- `templates` — Page templates with frontmatter (source, concept, entity, synthesis)
- `agent-personas` — agents/ directory with researcher, compiler, curator, auditor specs

### Phase 2: Skills & Automation
- `skill-setup` — wiki-setup SKILL.md (idempotent wizard, from second-brain)
- `skill-ingest` — wiki-ingest SKILL.md (two-phase: extract → compile, with hash-based skip)
- `skill-query` — wiki-query SKILL.md (index search → page read → synthesize answer)
- `skill-lint` — wiki-lint SKILL.md (quality scoring, staleness, orphans, broken links)
- `skill-update` — wiki-update SKILL.md (revise with provenance, source_hash update)
- `skill-orchestrate` — wiki-orchestrate SKILL.md (multi-step: ingest → lint → update index)
- `hooks` — .github/hooks/ for post-edit automation (index rebuild, drift detection)

### Phase 3: Tooling
- `scaffold-script` — Python scaffold.py to initialize wiki structure
- `lint-script` — Python lint_wiki.py (quality scoring, staleness checks, broken links)
- `index-script` — Python compile_index.py (rebuild with topic clustering)
- `setup-script` — Bash setup.sh (create symlinks, generate tool configs, validate deps)

### Phase 4: Documentation
- `arch-doc` — docs/architecture.md with mermaid diagrams (data flow, pipeline)
- `memory-doc` — docs/memory-model.md (staleness, provenance, quality, consolidation tiers)
- `workflow-doc` — docs/workflows.md with step-by-step guides
- `obsidian-doc` — docs/obsidian-setup.md integration guide
- `tool-setup-doc` — docs/tool-setup.md for VS Code, Copilot CLI, OpenCode

### Phase 5: Seed Content & Ship
- `seed-index` — Create initial wiki/index.md and wiki/log.md
- `push` — Commit all files, push to GitHub

## Dependencies
- Phase 2 depends on Phase 1 (schema + templates must exist before skills reference them)
- Phase 3 can run parallel with Phase 2
- Phase 4 can run parallel with Phase 2-3
- Phase 5 depends on all others

---

## Key Design Decisions

1. **AGENTS.md as single source of truth** — Universal schema read by VS Code Copilot, Copilot CLI, and OpenCode
2. **Two-phase ingest with hash-based skip** — Extract concepts first, then compile pages; skip unchanged sources (atomicmemory + agentmemory)
3. **Provenance + staleness in frontmatter** — Every page traces to sources and tracks freshness (agentmemory pattern, adapted to markdown)
4. **Agent personas over monolithic prompts** — Specialized agents (researcher, compiler, curator, auditor) with priority hierarchies (subagents pattern)
5. **Sub-organized wiki** — `sources/`, `concepts/`, `entities/`, `synthesis/` subdirectories (second-brain pattern)
6. **Quality scoring as first-class feature** — Lint produces 0-100 scores per page; below threshold triggers re-compilation
7. **Markdown-first, no databases** — All knowledge in git-trackable Markdown; BM25 via index.md at small scale
8. **Incremental by convention** — Log + index + source_hash lets the LLM know what's processed and what's stale
9. **Obsidian-compatible** — `[[wikilinks]]`, YAML frontmatter, graph-viewable structure
10. **Skills over scripts** — Primary interaction through slash commands; Python scripts for offline/CI use
11. **Human curates, LLM maintains** — User adds sources and asks questions; LLM does all bookkeeping, cross-referencing, and maintenance

## Comparison: v2 → v3 Changes

| Aspect | v2 (Previous) | v3 (Current) |
|--------|---------------|-------------|
| Ingest pipeline | Single-phase | Two-phase extract → compile (atomicmemory + agentmemory) |
| Provenance | Not tracked | Every page links to raw sources via frontmatter |
| Staleness | Not tracked | `source_hash` + `last_verified` + Ebbinghaus decay |
| Quality | Lint pass/fail | 0-100 quality scoring per page |
| Wiki structure | Flat `wiki/` | Sub-organized: sources, concepts, entities, synthesis |
| Agent model | Generic LLM | 4 specialized personas with priority hierarchies |
| Skills | 4 skills | 6 skills (+setup wizard, +orchestrator) |
| Setup | Manual | Idempotent `/wiki-setup` wizard (second-brain pattern) |
| Consolidation | None | Hot → Established → Core → Workflow tiers |
| Documentation | 4 docs | 5 docs (+memory-model.md) |

---

## References

### Primary Sources
- [Karpathy's LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory) — Persistent memory for AI agents (4-tier pipeline, hybrid retrieval)
- [NicholasSpisak/second-brain](https://github.com/NicholasSpisak/second-brain) — LLM-maintained Obsidian wiki
- [NicholasSpisak/claude-code-subagents](https://github.com/NicholasSpisak/claude-code-subagents) — 76+ specialized agent personas

### Community Implementations
- [sdyckjq-lab/llm-wiki-skill](https://github.com/sdyckjq-lab/llm-wiki-skill) (145⭐)
- [Ar9av/obsidian-wiki](https://github.com/Ar9av/obsidian-wiki) (127⭐)
- [atomicmemory/llm-wiki-compiler](https://github.com/atomicmemory/llm-wiki-compiler) (101⭐)
- [ussumant/llm-wiki-compiler](https://github.com/ussumant/llm-wiki-compiler) (100⭐)
- [lewislulu/llm-wiki-skill](https://github.com/lewislulu/llm-wiki-skill) (62⭐)
- [lucasastorian/llmwiki](https://github.com/lucasastorian/llmwiki) (36⭐)
- [tashisleepy/knowledge-engine](https://github.com/tashisleepy/knowledge-engine) (19⭐)
- [toolboxmd/karpathy-wiki](https://github.com/toolboxmd/karpathy-wiki)

### Standards & Documentation
- [Agent Skills Standard](https://agentskills.io)
- [Copilot CLI Custom Instructions](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)
- [OpenCode Skills Docs](https://opencode.ai/docs/skills)
- [VS Code Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [MindStudio: AI Second Brain with Claude Code & Obsidian](https://www.mindstudio.ai/blog/build-ai-second-brain-claude-code-obsidian)
