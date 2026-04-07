# labs-wiki — Implementation Plan

## Problem Statement

Build a personal LLM-powered wiki (labs-wiki) based on Karpathy's LLM Wiki pattern, incorporating the best features from the top 10 community implementations on GitHub. **Optimized for three target tools: VS Code (Copilot), Copilot CLI, and OpenCode.**

## Target Toolchain

| Tool | Role | Config Discovery |
|------|------|-----------------|
| **VS Code + Copilot** | Primary IDE — editing, browsing, Obsidian-like preview | `.github/copilot-instructions.md`, `.github/skills/`, `.github/hooks/` |
| **Copilot CLI** | Terminal agent — ingest, query, lint operations | `AGENTS.md`, `.github/skills/`, `~/.copilot/` |
| **OpenCode** | Alt terminal agent — multi-model orchestration | `AGENTS.md`, `.opencode/skills/`, `opencode.json` |

### Config Compatibility Strategy

All three tools read `AGENTS.md` at the repo root — this is the **universal schema** that defines wiki conventions. Skills follow the [Agent Skills standard](https://agentskills.io) (`SKILL.md` with YAML frontmatter) and are symlinked into each tool's discovery path via `setup.sh`.

```
AGENTS.md                        ← Read by ALL three tools (universal schema)
.github/copilot-instructions.md  ← VS Code Copilot always-on instructions
.github/skills/wiki-*/SKILL.md   ← Copilot CLI + VS Code skill discovery
.opencode/skills/wiki-*/SKILL.md ← OpenCode skill discovery (symlinked)
```

## Research Summary

### Karpathy's Core Pattern
Three layers: **Raw sources** (immutable docs) → **Wiki** (LLM-compiled Markdown) → **Schema** (AGENTS.md conventions). Operations: Ingest, Query, Lint. Key insight: knowledge is compiled once and kept current, not re-derived on every query.

### Top 10 Implementations Analyzed

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

### Features to Incorporate (Best-of-Breed)

**Must-Have (from analysis):**
1. ✅ Three-layer architecture: `raw/` → `wiki/` → schema (Karpathy core)
2. ✅ Hash-based incremental compilation (atomicmemory) — don't reprocess unchanged sources
3. ✅ Two-phase pipeline: concept extraction → page generation (atomicmemory) — eliminates race conditions
4. ✅ Operation logging with `log.md` (Karpathy + Astro-Han) — full audit trail
5. ✅ Index file with one-line summaries per page (Karpathy) — LLM navigation without embeddings
6. ✅ Health lint system (all top repos) — orphans, broken links, contradictions, gaps
7. ✅ Wikilink cross-referencing `[[concept]]` (universal pattern)
8. ✅ Portable Agent Skills with SKILL.md (agentskills.io standard)

**Nice-to-Have:**
9. 🎯 Multi-tool bootstrap with setup.sh (Ar9av pattern) — symlink skills for Copilot, OpenCode
10. 🎯 Context cost optimization via INDEX + topic clustering (ussumant) — 90% token savings
11. 🎯 Python utility scripts: scaffold.py, lint_wiki.py (lewislulu) — local debugging
12. 🎯 Hook-driven automation: auto-ingest, drift detection (toolboxmd)
13. 🎯 Obsidian integration: graph view, Dataview frontmatter, Marp slides (Karpathy tips)
14. 🎯 Web/URL source extraction (sdyckjq-lab)

**Differentiators for labs-wiki:**
15. 🚀 Homelab-focused seed content — use my actual homelab knowledge as first wiki domain
16. 🚀 MCP integration for OpenMemory — bridge wiki with existing memory system
17. 🚀 Three-tool parity — identical wiki experience across VS Code, Copilot CLI, and OpenCode

## Proposed Architecture

```
labs-wiki/
├── README.md                         # Project overview, setup, usage guide
├── LICENSE                           # MIT
├── AGENTS.md                         # Universal schema (read by all 3 tools)
├── opencode.json                     # OpenCode agent/model configuration
├── setup.sh                          # Bootstrap: symlinks skills into each tool
│
├── raw/                              # Layer 1: Immutable source documents
│   └── .gitkeep
│
├── wiki/                             # Layer 2: LLM-compiled knowledge pages
│   ├── index.md                      # Auto-generated catalog of all pages
│   ├── log.md                        # Chronological operation log
│   └── .gitkeep
│
├── .github/                          # VS Code Copilot + Copilot CLI
│   ├── copilot-instructions.md       # Always-on Copilot instructions
│   ├── skills/                       # Canonical skill location
│   │   ├── wiki-ingest/
│   │   │   └── SKILL.md             # /wiki-ingest — process new sources
│   │   ├── wiki-query/
│   │   │   └── SKILL.md             # /wiki-query — search & answer
│   │   ├── wiki-lint/
│   │   │   └── SKILL.md             # /wiki-lint — health checks
│   │   └── wiki-update/
│   │       └── SKILL.md             # /wiki-update — revise existing pages
│   └── hooks/                        # Copilot lifecycle hooks
│       └── post-edit.json            # Auto-actions after file edits
│
├── .opencode/                        # OpenCode (symlinked from .github/skills)
│   └── skills/ → ../.github/skills   # Symlink — single source of truth
│
├── scripts/                          # Utility scripts
│   ├── scaffold.py                   # Initialize new wiki structure
│   ├── lint_wiki.py                  # Standalone lint (broken links, orphans)
│   └── compile_index.py              # Rebuild index.md from wiki/ pages
│
├── templates/                        # Page templates
│   ├── source-summary.md             # Template for source summaries
│   ├── concept-page.md               # Template for concept/entity pages
│   └── comparison.md                 # Template for comparison pages
│
└── docs/                             # Meta-documentation
    ├── architecture.md               # How labs-wiki works (with diagrams)
    ├── workflows.md                  # Ingest, query, lint workflows
    ├── obsidian-setup.md             # Obsidian vault integration guide
    └── tool-setup.md                 # VS Code, Copilot CLI, OpenCode setup
```

### Tool-Specific Config Details

**AGENTS.md** (universal — all tools read this):
- Wiki conventions, page formats, naming rules
- Ingest/query/lint/update workflow definitions
- Index and log maintenance rules
- Cross-referencing and frontmatter standards

**`.github/copilot-instructions.md`** (VS Code Copilot):
- Compact always-on instructions pointing to AGENTS.md
- VS Code-specific behaviors (e.g., Markdown preview, workspace search)

**`opencode.json`** (OpenCode):
- Agent definitions: primary wiki-maintainer agent + research subagent
- Model assignments (e.g., primary on gpt-5.1-codex, research on sonar-pro)
- Tool permissions (write, edit, bash enabled for primary agent)

**Skill portability:**
- Skills authored once in `.github/skills/` (Copilot canonical path)
- Symlinked to `.opencode/skills/` for OpenCode discovery
- All SKILL.md files use agentskills.io YAML frontmatter for cross-tool compat

## Implementation Todos

### Phase 1: Foundation
- `repo-setup` — Create directory structure, LICENSE, .gitignore
- `readme` — Write comprehensive README with architecture diagram, quickstart, usage
- `schema` — Write AGENTS.md universal schema (wiki conventions, page formats, workflows)
- `copilot-instructions` — Write .github/copilot-instructions.md for VS Code
- `opencode-config` — Write opencode.json agent/model configuration
- `templates` — Create page templates (source-summary, concept, comparison)

### Phase 2: Skills & Automation
- `skill-ingest` — Create wiki-ingest SKILL.md (process raw sources → wiki pages)
- `skill-query` — Create wiki-query SKILL.md (search index, read pages, synthesize)
- `skill-lint` — Create wiki-lint SKILL.md (orphans, broken links, contradictions, gaps)
- `skill-update` — Create wiki-update SKILL.md (revise pages with new info)
- `hooks` — Configure .github/hooks/ for post-edit automation

### Phase 3: Tooling
- `scaffold-script` — Python scaffold.py to initialize wiki structure
- `lint-script` — Python lint_wiki.py for standalone health checks
- `index-script` — Python compile_index.py to rebuild index from wiki pages
- `setup-script` — Bash setup.sh to bootstrap all tools (create symlinks, validate deps)

### Phase 4: Documentation
- `arch-doc` — docs/architecture.md with mermaid diagrams
- `workflow-doc` — docs/workflows.md with step-by-step guides
- `obsidian-doc` — docs/obsidian-setup.md integration guide
- `tool-setup-doc` — docs/tool-setup.md for VS Code, Copilot CLI, OpenCode

### Phase 5: Seed Content & Ship
- `seed-index` — Create initial wiki/index.md and wiki/log.md
- `push` — Commit all files, push to GitHub

## Dependencies
- Phase 2 depends on Phase 1 (schema must exist before skills reference it)
- Phase 3 can run parallel with Phase 2
- Phase 4 can run parallel with Phase 2-3
- Phase 5 depends on all others

## Key Design Decisions

1. **AGENTS.md as single source of truth**: Universal schema read by VS Code Copilot, Copilot CLI, and OpenCode — no duplicate config
2. **Canonical skills in `.github/skills/`**: Copilot-native location, symlinked to `.opencode/skills/` for OpenCode
3. **agentskills.io standard**: SKILL.md with YAML frontmatter ensures portability across current and future tools
4. **Markdown-first**: All knowledge in git-trackable Markdown — no databases, no embeddings at small scale
5. **Incremental by convention**: Log + index pattern lets the LLM know what's already processed
6. **Obsidian-compatible**: `[[wikilinks]]`, YAML frontmatter, graph-viewable structure
7. **Skills over scripts**: Primary interaction through slash commands; Python scripts for offline/CI use
8. **Human curates, LLM maintains**: User adds sources and asks questions; LLM does all bookkeeping

## References

- [Karpathy's LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [toolboxmd/karpathy-wiki](https://github.com/toolboxmd/karpathy-wiki)
- [sdyckjq-lab/llm-wiki-skill](https://github.com/sdyckjq-lab/llm-wiki-skill) (145⭐)
- [Ar9av/obsidian-wiki](https://github.com/Ar9av/obsidian-wiki) (127⭐)
- [atomicmemory/llm-wiki-compiler](https://github.com/atomicmemory/llm-wiki-compiler) (101⭐)
- [ussumant/llm-wiki-compiler](https://github.com/ussumant/llm-wiki-compiler) (100⭐)
- [lucasastorian/llmwiki](https://github.com/lucasastorian/llmwiki) (36⭐)
- [tashisleepy/knowledge-engine](https://github.com/tashisleepy/knowledge-engine) (19⭐)
- [Agent Skills Standard](https://agentskills.io)
- [Copilot CLI Custom Instructions](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)
- [OpenCode Skills Docs](https://opencode.ai/docs/skills)
- [VS Code Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
