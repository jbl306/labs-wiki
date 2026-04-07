# labs-wiki — Implementation Plan

## Problem Statement

Build a personal LLM-powered wiki (labs-wiki) based on Karpathy's LLM Wiki pattern, incorporating the best features from the top 10 community implementations on GitHub.

## Research Summary

### Karpathy's Core Pattern
Three layers: **Raw sources** (immutable docs) → **Wiki** (LLM-compiled Markdown) → **Schema** (CLAUDE.md/AGENTS.md conventions). Operations: Ingest, Query, Lint. Key insight: knowledge is compiled once and kept current, not re-derived on every query.

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
8. ✅ Claude Code skills with slash commands (kfchou, Astro-Han)

**Nice-to-Have:**
9. 🎯 Multi-agent bootstrap with setup.sh (Ar9av) — Claude, Codex, Copilot, Cursor
10. 🎯 Context cost optimization via INDEX + topic clustering (ussumant) — 90% token savings
11. 🎯 Python utility scripts: scaffold.py, lint_wiki.py (lewislulu) — local debugging
12. 🎯 Hook-driven automation: auto-ingest, drift detection (toolboxmd)
13. 🎯 Obsidian integration: graph view, Dataview frontmatter, Marp slides (Karpathy tips)
14. 🎯 Web/URL source extraction (sdyckjq-lab)

**Differentiators for labs-wiki:**
15. 🚀 Homelab-focused seed content — use my actual homelab knowledge as first wiki domain
16. 🚀 MCP integration for OpenMemory — bridge wiki with my existing memory system
17. 🚀 Comprehensive README with architecture diagrams — learner-friendly like jbl306/claude repo

## Proposed Architecture

```
labs-wiki/
├── README.md                    # Project overview, setup, usage guide
├── LICENSE                      # MIT
├── CLAUDE.md                    # Schema: wiki conventions, workflows, rules
├── AGENTS.md                    # Codex/OpenCode compatibility
├── setup.sh                     # One-command bootstrap for multiple agents
│
├── raw/                         # Layer 1: Immutable source documents
│   └── .gitkeep
│
├── wiki/                        # Layer 2: LLM-compiled knowledge pages
│   ├── index.md                 # Auto-generated catalog of all pages
│   ├── log.md                   # Chronological operation log
│   └── .gitkeep
│
├── .claude/                     # Claude Code integration
│   ├── settings.json            # Hooks configuration
│   └── skills/                  # Slash command skills
│       ├── wiki-ingest/
│       │   └── SKILL.md         # /wiki-ingest — process new sources
│       ├── wiki-query/
│       │   └── SKILL.md         # /wiki-query — search & answer
│       ├── wiki-lint/
│       │   └── SKILL.md         # /wiki-lint — health checks
│       └── wiki-update/
│           └── SKILL.md         # /wiki-update — revise existing pages
│
├── scripts/                     # Utility scripts
│   ├── scaffold.py              # Initialize new wiki structure
│   ├── lint_wiki.py             # Standalone lint (broken links, orphans)
│   └── compile_index.py         # Rebuild index.md from wiki/ pages
│
├── templates/                   # Page templates
│   ├── source-summary.md        # Template for source summaries
│   ├── concept-page.md          # Template for concept/entity pages
│   └── comparison.md            # Template for comparison pages
│
└── docs/                        # Meta-documentation
    ├── architecture.md          # How labs-wiki works (with diagrams)
    ├── workflows.md             # Ingest, query, lint workflows
    ├── obsidian-setup.md        # Obsidian vault integration guide
    └── multi-agent.md           # Setup for Claude, Codex, Cursor, etc.
```

## Implementation Todos

### Phase 1: Foundation
- `repo-setup` — Create GitHub repo, directory structure, LICENSE, .gitignore
- `readme` — Write comprehensive README with architecture diagram, quickstart, usage
- `schema` — Write CLAUDE.md schema defining wiki conventions, page formats, workflows
- `agents-md` — Write AGENTS.md for Codex/OpenCode compatibility
- `templates` — Create page templates (source-summary, concept, comparison)

### Phase 2: Skills & Automation
- `skill-ingest` — Create wiki-ingest skill (process raw sources → wiki pages)
- `skill-query` — Create wiki-query skill (search index, read pages, synthesize answer)
- `skill-lint` — Create wiki-lint skill (orphans, broken links, contradictions, gaps)
- `skill-update` — Create wiki-update skill (revise pages with new info)
- `hooks` — Configure .claude/settings.json hooks (auto-format, session reminders, drift detection)

### Phase 3: Tooling
- `scaffold-script` — Python scaffold.py to initialize wiki structure
- `lint-script` — Python lint_wiki.py for standalone health checks
- `index-script` — Python compile_index.py to rebuild index from wiki pages
- `setup-script` — Bash setup.sh for multi-agent bootstrap (symlinks for Claude, Codex, Cursor)

### Phase 4: Documentation
- `arch-doc` — docs/architecture.md with mermaid diagrams
- `workflow-doc` — docs/workflows.md with step-by-step guides
- `obsidian-doc` — docs/obsidian-setup.md integration guide
- `multi-agent-doc` — docs/multi-agent.md setup for different agents

### Phase 5: Seed Content & Ship
- `seed-index` — Create initial wiki/index.md and wiki/log.md
- `push` — Push to GitHub as public repo

## Dependencies
- Phase 2 depends on Phase 1
- Phase 3 can run parallel with Phase 2
- Phase 4 can run parallel with Phase 2-3
- Phase 5 depends on all others

## Key Design Decisions

1. **Markdown-first**: All knowledge in git-trackable Markdown — no databases, no embeddings at small scale
2. **Agent-agnostic schema**: CLAUDE.md + AGENTS.md so any LLM agent can maintain the wiki
3. **Incremental by convention**: Log + index pattern lets the LLM know what's already processed
4. **Obsidian-compatible**: `[[wikilinks]]`, YAML frontmatter, graph-viewable structure
5. **Skills over scripts**: Primary interaction through Claude Code slash commands; Python scripts for offline use
6. **Human curates, LLM maintains**: User adds sources and asks questions; LLM does all bookkeeping

## References

- [Karpathy's LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [toolboxmd/karpathy-wiki](https://github.com/toolboxmd/karpathy-wiki)
- [sdyckjq-lab/llm-wiki-skill](https://github.com/sdyckjq-lab/llm-wiki-skill) (145⭐)
- [Ar9av/obsidian-wiki](https://github.com/Ar9av/obsidian-wiki) (127⭐)
- [atomicmemory/llm-wiki-compiler](https://github.com/atomicmemory/llm-wiki-compiler) (101⭐)
- [ussumant/llm-wiki-compiler](https://github.com/ussumant/llm-wiki-compiler) (100⭐)
- [lucasastorian/llmwiki](https://github.com/lucasastorian/llmwiki) (36⭐)
- [tashisleepy/knowledge-engine](https://github.com/tashisleepy/knowledge-engine) (19⭐)
