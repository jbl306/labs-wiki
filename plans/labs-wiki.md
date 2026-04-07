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
├── raw/                              # Layer 1: Immutable source documents (inbox)
│   ├── assets/                       # Binary files (images, PDFs) from ingest API
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
├── wiki-ingest-api/                  # FastAPI capture service (Docker)
│   ├── Dockerfile
│   ├── app.py                        # POST /api/ingest — text, URL, file
│   ├── requirements.txt
│   └── README.md                     # API docs, auth setup
│
├── .github/                          # VS Code Copilot + Copilot CLI + CI
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
│   ├── hooks/                        # Copilot lifecycle hooks
│   │   └── post-edit.json            # Auto-actions after wiki edits
│   └── workflows/                    # GitHub Actions
│       └── ingest-from-issue.yml     # Issue-based source capture
│
├── .opencode/                        # OpenCode (symlinked from .github/skills)
│   └── skills/ → ../.github/skills   # Symlink — single source of truth
│
├── scripts/                          # Utility scripts (offline/CI use)
│   ├── scaffold.py                   # Initialize wiki structure
│   ├── lint_wiki.py                  # Standalone lint (broken links, orphans, staleness)
│   ├── compile_index.py              # Rebuild index.md with topic clustering
│   └── ntfy-wiki-watcher.sh          # ntfy → ingest API bridge
│
├── templates/                        # Page templates with frontmatter standards
│   ├── source-summary.md             # Template for raw/ → wiki/sources/ pages
│   ├── concept-page.md               # Template for concept deep-dives
│   ├── entity-page.md                # Template for named entities
│   └── synthesis-page.md             # Template for cross-cutting analysis
│
├── docs/                             # Meta-documentation
│   ├── architecture.md               # How labs-wiki works (mermaid diagrams)
│   ├── memory-model.md               # Staleness, provenance, quality scoring
│   ├── capture-sources.md            # Multi-device ingestion setup guide
│   ├── workflows.md                  # Ingest, query, lint, update workflows
│   ├── obsidian-setup.md             # Obsidian vault integration guide
│   └── tool-setup.md                 # VS Code, Copilot CLI, OpenCode setup
│
└── plans/                            # Implementation plans
    └── labs-wiki.md                  # This file
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

## Multi-Device Source Ingestion

The hardest part of any second brain is **getting stuff into it**. If adding a source requires SSH-ing into a server and running commands, you won't do it. This section defines a frictionless multi-channel capture system that feeds `raw/` from any device.

### Design Principles

1. **< 10 seconds from "I found something" to captured** — share sheet, bookmarklet, or CLI one-liner
2. **Works from any device** — phone (iOS/Android), laptop browser, terminal, tablet
3. **All roads lead to `raw/`** — every channel writes to the same inbox directory
4. **Server-side processing** — capture is dumb (just save); compilation is smart (LLM ingest skill)
5. **Leverage existing infra** — use ntfy (already deployed), Caddy (already proxying), homelab server

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    CAPTURE CHANNELS                      │
├──────────┬──────────┬──────────┬──────────┬─────────────┤
│📱 Phone  │💻 Browser│⌨️ Terminal│📧 Email  │🔗 GitHub    │
│  Share   │  Book-   │  CLI     │  Forward │  Issue /    │
│  Sheet   │  marklet │  `wa`    │  (future)│  PR comment │
└────┬─────┴────┬─────┴────┬─────┴────┬─────┴──────┬──────┘
     │          │          │          │            │
     ▼          ▼          ▼          ▼            ▼
┌─────────────────────────────────────────────────────────┐
│              WIKI INGEST API (FastAPI)                    │
│         POST /api/ingest — homelab container             │
│     Accepts: text, URL, file upload, image               │
│     Auth: Bearer token from .env                         │
│     Writes to: ~/projects/labs-wiki/raw/                 │
│     Notifies: ntfy topic on capture                      │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   raw/ INBOX                             │
│     YYYY-MM-DD-<slug>.md (auto-generated frontmatter)   │
│     raw/assets/<uuid>.<ext> (images, PDFs)              │
└────────────────────────┬────────────────────────────────┘
                         │ (manual or cron-triggered)
                         ▼
┌─────────────────────────────────────────────────────────┐
│          /wiki-ingest SKILL (LLM compilation)            │
│     Two-phase: extract concepts → generate wiki pages   │
└─────────────────────────────────────────────────────────┘
```

### Channel Details

#### 1. Wiki Ingest API (the hub)

A lightweight FastAPI container on the homelab server. All other channels POST to this.

```python
# POST /api/ingest
# Content-Type: application/json or multipart/form-data
#
# JSON body:
{
  "type": "url" | "text" | "note",    # what kind of source
  "content": "https://...",            # the URL, text, or note body
  "title": "Optional title",          # auto-generated if omitted
  "tags": ["ml", "transformers"],      # optional tags
  "source": "phone-share"             # which channel sent this
}
#
# File upload (multipart):
#   file: <binary>
#   title: "Optional title"
#   tags: "ml,transformers"
```

**What it does:**
- Validates + sanitizes input
- For URLs: fetches page title, saves URL + metadata as markdown
- For text/notes: wraps in markdown with frontmatter
- For files: saves to `raw/assets/`, creates markdown reference
- Writes `raw/YYYY-MM-DD-<slug>.md` with standardized frontmatter
- Sends ntfy notification: "📥 New source captured: <title>"
- Returns `{ "status": "ok", "path": "raw/2026-04-07-rope-encoding.md" }`

**Deployment:** Docker container in homelab, reverse-proxied via Caddy at `wiki-api.jbl.sh` (or similar internal domain).

```yaml
# compose/compose.wiki.yml (new stack)
services:
  wiki-ingest-api:
    build: ./wiki-ingest-api
    container_name: wiki-ingest-api
    restart: unless-stopped
    volumes:
      - ${LABS_WIKI_PATH:-/home/jbl/projects/labs-wiki}/raw:/app/raw
    environment:
      - WIKI_API_TOKEN=${WIKI_API_TOKEN}
      - NTFY_SERVER=${NTFY_SERVER:-https://ntfy.sh}
      - NTFY_TOPIC=${NTFY_TOPIC}
    deploy:
      resources:
        limits:
          memory: 128M
          cpus: '0.25'
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
    labels:
      caddy: wiki-api.internal
      caddy.reverse_proxy: "{{upstreams 8000}}"
```

#### 2. 📱 Phone — iOS Shortcut / Android Share Sheet

**iOS Shortcut** (appears in Share Sheet):
1. Receive input from Share Sheet (URL, text, image)
2. `Get Contents of URL` → POST to `https://wiki-api.jbl.sh/api/ingest`
3. Set headers: `Authorization: Bearer <token>`
4. Body: `{ "type": "url", "content": "<shared URL>", "source": "ios-share" }`
5. Show notification: "✅ Captured to wiki"

**Android** (via HTTP Shortcuts app or Tasker):
- Same POST request, configured as a share target
- [HTTP Shortcuts](https://http-shortcuts.rto.ch/) is free/open-source and perfect for this

**Usage:** See an interesting article → Share → "Add to Wiki" → done in 3 taps.

#### 3. 💻 Browser — Bookmarklet

A JavaScript bookmarklet that captures the current page:

```javascript
// "Add to Wiki" bookmarklet
javascript:void(fetch('https://wiki-api.jbl.sh/api/ingest',{
  method:'POST',
  headers:{'Content-Type':'application/json','Authorization':'Bearer TOKEN'},
  body:JSON.stringify({type:'url',content:location.href,title:document.title,source:'bookmarklet'})
}).then(r=>r.json()).then(d=>alert('✅ '+d.path)).catch(e=>alert('❌ '+e)))
```

Works on any browser (laptop, tablet, phone browser). One click capture.

#### 4. ⌨️ Terminal — CLI Function `wa` (wiki-add)

A shell function for terminal users (laptop or SSH'd into server):

```bash
# Add to ~/.bashrc or ~/.zshrc
wa() {
  local type="${1:-text}"
  local content="$2"
  local title="${3:-}"

  if [[ "$type" == "url" && -z "$content" ]]; then
    echo "Usage: wa url <URL> [title]"; return 1
  fi

  if [[ "$type" == "text" && -z "$content" ]]; then
    # Read from stdin (pipe support)
    content=$(cat)
  fi

  curl -s -X POST "https://wiki-api.jbl.sh/api/ingest" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $WIKI_API_TOKEN" \
    -d "$(jq -n --arg t "$type" --arg c "$content" --arg ti "$title" \
      '{type:$t, content:$c, title:$ti, source:"cli"}')" \
    | jq -r '.path // .error'
}

# Upload a file
waf() {
  local file="$1"
  local title="${2:-$(basename "$file")}"
  curl -s -X POST "https://wiki-api.jbl.sh/api/ingest" \
    -H "Authorization: Bearer $WIKI_API_TOKEN" \
    -F "file=@$file" \
    -F "title=$title" \
    -F "source=cli" \
    | jq -r '.path // .error'
}
```

**Usage examples:**
```bash
wa url "https://arxiv.org/abs/2104.09864" "RoFormer paper"
wa text "Key insight: RoPE encodes position in rotation angle"
echo "Some long notes..." | wa text
waf screenshot.png "VRAM usage chart"
```

#### 5. 🔗 GitHub Issues as Inbox (zero-infra option)

For when you're already in GitHub (e.g., reading code):
- Create an issue in `jbl306/labs-wiki` with label `ingest`
- A GitHub Actions workflow picks it up, writes to `raw/`, closes the issue

```yaml
# .github/workflows/ingest-from-issue.yml
name: Ingest from Issue
on:
  issues:
    types: [labeled]
jobs:
  ingest:
    if: contains(github.event.label.name, 'ingest')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Create raw source
        run: |
          SLUG=$(echo "${{ github.event.issue.title }}" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]//g')
          DATE=$(date +%Y-%m-%d)
          cat > "raw/${DATE}-${SLUG}.md" << 'EOF'
          ---
          title: "${{ github.event.issue.title }}"
          captured: "${DATE}"
          source: github-issue
          issue: ${{ github.event.issue.number }}
          tags: []
          ---

          ${{ github.event.issue.body }}
          EOF
      - name: Commit and close
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add raw/
          git commit -m "ingest: ${{ github.event.issue.title }}"
          git push
          gh issue close ${{ github.event.issue.number }} --comment "✅ Ingested to wiki"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

#### 6. 🔄 ntfy.sh as Transport (leverage existing infra)

Since ntfy is already running on the homelab, you can send sources via any ntfy client:

```bash
# From any device with ntfy CLI or app
curl -d "https://arxiv.org/abs/2104.09864" \
  -H "Title: RoFormer paper" \
  -H "Tags: ingest,ml" \
  ntfy.sh/jbl-wiki-ingest
```

A watcher script on the server subscribes to the topic and feeds to the ingest API:

```bash
#!/usr/bin/env bash
# scripts/ntfy-wiki-watcher.sh — runs as systemd service or Docker sidecar
ntfy subscribe jbl-wiki-ingest --from-config | while read -r msg; do
  content=$(echo "$msg" | jq -r '.message')
  title=$(echo "$msg" | jq -r '.title // empty')
  curl -s -X POST "http://localhost:8000/api/ingest" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $WIKI_API_TOKEN" \
    -d "$(jq -n --arg c "$content" --arg t "$title" \
      '{type:"text", content:$c, title:$t, source:"ntfy"}')"
done
```

### Channel Comparison

| Channel | Device | Friction | Supports | Best For |
|---------|--------|----------|----------|----------|
| **iOS Shortcut** | iPhone/iPad | ⭐ 3 taps | URLs, text, images | Browsing on phone |
| **Android Share** | Android | ⭐ 3 taps | URLs, text, images | Browsing on phone |
| **Bookmarklet** | Any browser | ⭐ 1 click | Current page URL | Laptop research |
| **CLI `wa`** | Terminal | ⭐⭐ typing | URLs, text, files, pipes | Devs, SSH sessions |
| **GitHub Issue** | GitHub UI | ⭐⭐ new issue | Text, markdown | Reading code/repos |
| **ntfy** | Any ntfy client | ⭐⭐ send msg | Text, URLs | Quick capture anywhere |

### Raw Source Format (auto-generated by ingest API)

Every captured source lands as a markdown file with consistent frontmatter:

```yaml
---
title: "RoFormer: Enhanced Transformer with Rotary Position Embedding"
type: url                             # url | text | note | file
captured: 2026-04-07T03:15:00Z
source: ios-share                     # which channel
url: "https://arxiv.org/abs/2104.09864"
content_hash: "sha256:a1b2c3..."      # for incremental compilation
tags: [ml, transformers, positional-encoding]
status: pending                       # pending | ingested | failed
---

# RoFormer: Enhanced Transformer with Rotary Position Embedding

Source: https://arxiv.org/abs/2104.09864

<!-- Content fetched at capture time (for URLs) or pasted content (for text/notes) -->
```

### Security Considerations

- **Bearer token auth** on all API endpoints (token stored in homelab `.env`)
- **Caddy HTTPS** termination + rate limiting
- **No public exposure** — API accessible only via Cloudflare Tunnel or LAN
- **Input sanitization** — validate URLs, limit file sizes (15MB max), strip scripts
- **ntfy topic auth** — use authenticated topic for wiki ingest channel

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

### Phase 5: Multi-Device Ingestion
- `ingest-api` — FastAPI app: POST /api/ingest endpoint (text, URL, file upload)
- `ingest-docker` — Dockerfile + compose stack (compose.wiki.yml) for ingest API
- `ingest-cli` — Shell functions `wa` and `waf` for terminal capture
- `ingest-bookmarklet` — JavaScript bookmarklet for browser capture
- `ingest-ios-shortcut` — iOS Shortcut instructions + export file
- `ingest-github-action` — .github/workflows/ingest-from-issue.yml
- `ingest-ntfy-watcher` — scripts/ntfy-wiki-watcher.sh for ntfy channel
- `ingest-doc` — docs/capture-sources.md (setup guide for all channels)

### Phase 6: Seed Content & Ship
- `seed-index` — Create initial wiki/index.md and wiki/log.md
- `push` — Commit all files, push to GitHub

## Dependencies
- Phase 2 depends on Phase 1 (schema + templates must exist before skills reference them)
- Phase 3 can run parallel with Phase 2
- Phase 4 can run parallel with Phase 2-3
- Phase 5 depends on Phase 1 (repo-setup for raw/ directory)
- Phase 5 can run parallel with Phase 2-4
- Phase 6 depends on all others

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
12. **Multi-channel capture with single API hub** — All devices POST to one FastAPI endpoint; capture is dumb, compilation is smart
13. **< 10 second capture** — Every channel optimized for minimum friction (3 taps on phone, 1 click in browser, one-liner in terminal)

## Comparison: v3 → v3.1 Changes

| Aspect | v3 (Previous) | v3.1 (Current) |
|--------|---------------|----------------|
| Source capture | Manual — drop files in `raw/` | 6 channels: iOS, Android, bookmarklet, CLI, GitHub Issues, ntfy |
| Ingest API | None | FastAPI container on homelab, auth'd, Caddy-proxied |
| Phone capture | Not supported | iOS Shortcut + Android Share Sheet → API |
| Browser capture | Not supported | One-click bookmarklet |
| Terminal capture | Manual file creation | `wa` / `waf` shell functions |
| Notifications | None on capture | ntfy push on every new source |
| Architecture | No API layer | `wiki-ingest-api/` Docker service + `compose.wiki.yml` |
| Phases | 5 phases | 6 phases (+multi-device ingestion) |
| Docs | 5 docs | 6 docs (+capture-sources.md) |

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
