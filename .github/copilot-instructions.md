## labs-wiki

Personal LLM-powered knowledge wiki: `raw/` sources → `wiki/` compiled pages → `AGENTS.md` schema.

**Read `AGENTS.md` for the full authoritative schema.** This file is a lightweight index.

### Directory Map

```
raw/                  → Immutable source documents (never edit)
wiki/                 → Compiled knowledge (sources/, concepts/, entities/, synthesis/)
.github/agents/       → Copilot agent definitions (wiki-capture, wiki-ingest, wiki-query, etc.)
templates/            → Page templates for each wiki page type
scripts/              → Python utilities (auto_ingest.py, watch_raw.py, lint_wiki.py, compile_index.py)
wiki-ingest-api/      → FastAPI capture service (Docker)
docs/                 → Architecture, workflows, setup guides
```

### Auto-Ingest Pipeline

Sources are processed **automatically** by the `wiki-auto-ingest` Docker sidecar:

- **Watches** `raw/` for new files with `status: pending`
- **Smart URL handlers**: Twitter/X (fxtwitter API), GitHub repos (REST API + README), HTML pages
- **Vision support**: Downloads images → base64 → GPT-4.1 multimodal analysis (charts, diagrams, screenshots)
- **Model**: GPT-4.1 via GitHub Models API (149 req/min, vision-capable)
- **Notifications**: ntfy alerts on success/failure

### Custom Agents (invoke with @agent-name in chat)

| Agent | Purpose |
|-------|---------|
| `@wiki-capture` | Quick-capture a URL or text into `raw/` (auto-ingest processes it) |
| `@wiki-ingest` | Manual fallback: two-phase pipeline when auto-ingest unavailable |
| `@wiki-query` | Search and synthesize answers from wiki pages |
| `@wiki-lint` | Quality audit, broken links, staleness checks |
| `@wiki-update` | Revise pages with new info, preserve provenance |
| `@wiki-curator` | Gap analysis, synthesis creation, tier promotion |
| `@wiki-orchestrate` | Maintenance workflows: audit + lint + gap analysis |

### Scoped Instructions (auto-loaded by file pattern)

| Pattern | Applies |
|---------|---------|
| `wiki/**/*.md` | Frontmatter rules, wikilinks, quality standards |
| `raw/**/*.md` | Immutability rules, raw source format |
| `scripts/**/*.py` | Python conventions, CLI patterns |
| `templates/**/*.md` | Template variable conventions |
| `wiki-ingest-api/**` | FastAPI endpoint patterns |

### Prompt Files (invoke from chat prompt picker)

| Prompt | Purpose |
|--------|---------|
| `ingest-source` | Capture a URL/text as raw source (auto-processed) |
| `wiki-status` | Health dashboard with stats |
| `find-gaps` | Coverage analysis and missing concepts |
| `daily-maintenance` | Audit + lint + stale review cycle |

### Core Rules

- Every wiki fact must trace to a `sources:` entry (provenance)
- Never modify `raw/` files (immutable inbox, except `status` field)
- Log all operations to `wiki/log.md`; rebuild `wiki/index.md` after changes
- Run `python3 scripts/lint_wiki.py` or use `@wiki-lint` to validate
