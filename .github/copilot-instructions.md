## labs-wiki

Personal LLM-powered knowledge wiki: `raw/` sources → `wiki/` compiled pages → `AGENTS.md` schema.

**Read `AGENTS.md` for the full authoritative schema.** This file is a lightweight index.

### Directory Map

```
raw/                  → Immutable source documents (never edit)
wiki/                 → Compiled knowledge (sources/, concepts/, entities/, synthesis/)
agents/               → Agent persona definitions (researcher, compiler, curator, auditor)
templates/            → Page templates for each wiki page type
scripts/              → Python utilities (lint_wiki.py, compile_index.py, scaffold.py)
wiki-ingest-api/      → FastAPI capture service (Docker)
docs/                 → Architecture, workflows, setup guides
```

### Custom Agents (invoke with @agent-name in chat)

| Agent | Purpose |
|-------|---------|
| `@wiki-capture` | Quick-capture a URL or text into `raw/` |
| `@wiki-ingest` | Two-phase pipeline: extract concepts → compile pages |
| `@wiki-query` | Search and synthesize answers from wiki pages |
| `@wiki-lint` | Quality audit, broken links, staleness checks |
| `@wiki-update` | Revise pages with new info, preserve provenance |
| `@wiki-curator` | Gap analysis, synthesis creation, tier promotion |
| `@wiki-orchestrate` | Multi-step workflows (delegates to above agents) |

### Scoped Instructions (auto-loaded by file pattern)

| Pattern | Applies |
|---------|---------|
| `wiki/**/*.md` | Frontmatter rules, wikilinks, quality standards |
| `raw/**/*.md` | Immutability rules, raw source format |
| `scripts/**/*.py` | Python conventions, CLI patterns |
| `templates/**/*.md` | Template variable conventions |
| `wiki-ingest-api/**` | FastAPI endpoint patterns |
| `agents/**/*.md` | Persona structure format |

### Prompt Files (invoke from chat prompt picker)

| Prompt | Purpose |
|--------|---------|
| `ingest-source` | Capture a URL/text as raw source |
| `wiki-status` | Health dashboard with stats |
| `find-gaps` | Coverage analysis and missing concepts |
| `daily-maintenance` | Full maintenance cycle |

### Core Rules

- Every wiki fact must trace to a `sources:` entry (provenance)
- Never modify `raw/` files (immutable inbox)
- Log all operations to `wiki/log.md`; rebuild `wiki/index.md` after changes
- Run `python3 scripts/lint_wiki.py` or use `@wiki-lint` to validate
