---
title: https://github.com/milla-jovovich/mempalace
type: url
captured: 2026-04-11 02:52:45.994256+00:00
source: android-share
url: https://github.com/milla-jovovich/mempalace
content_hash: sha256:292adb6a15044843688d62e79f812fa01f743df73377c8a2c7f8e61040bf08c3
tags: []
status: ingested
last_refreshed: '2026-04-22T02:44:33+00:00'
---

https://github.com/milla-jovovich/mempalace

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-22T02:44:33+00:00
- source_url: https://github.com/milla-jovovich/mempalace
- resolved_url: https://github.com/milla-jovovich/mempalace
- content_type: application/vnd.github+json
- image_urls: []

## Fetched Content
Repository: MemPalace/mempalace
Description: The best-benchmarked open-source AI memory system. And it's free.
Stars: 48804
Language: Python
Topics: ai, chromadb, llm, mcp, memory, python

## README

> [!CAUTION]
> **Scam alert.** The only official sources for MemPalace are this
> [GitHub repository](https://github.com/MemPalace/mempalace), the
> [PyPI package](https://pypi.org/project/mempalace/), and the docs site at
> **[mempalaceofficial.com](https://mempalaceofficial.com)**. Any other
> domain — including `mempalace.tech` — is an impostor and may distribute
> malware. Details and timeline: [docs/HISTORY.md](docs/HISTORY.md).

<div align="center">

<img src="assets/mempalace_logo.png" alt="MemPalace" width="240">

# MemPalace

Local-first AI memory. Verbatim storage, pluggable backend, 96.6% R@5 raw on LongMemEval — zero API calls.

[![][version-shield]][release-link]
[![][python-shield]][python-link]
[![][license-shield]][license-link]
[![][discord-shield]][discord-link]

</div>

---

## What it is

MemPalace stores your conversation history as verbatim text and retrieves
it with semantic search. It does not summarize, extract, or paraphrase.
The index is structured — people and projects become *wings*, topics
become *rooms*, and original content lives in *drawers* — so searches
can be scoped rather than run against a flat corpus.

The retrieval layer is pluggable. The current default is ChromaDB; the
interface is defined in [`mempalace/backends/base.py`](mempalace/backends/base.py)
and alternative backends can be dropped in without touching the rest of
the system.

Nothing leaves your machine unless you opt in.

Architecture, concepts, and mining flows:
[mempalaceofficial.com/concepts/the-palace](https://mempalaceofficial.com/concepts/the-palace.html).

---

## Install

```bash
pip install mempalace
mempalace init ~/projects/myapp
```

## Quickstart

```bash
# Mine content into the palace
mempalace mine ~/projects/myapp                    # project files
mempalace mine ~/.claude/projects/ --mode convos   # Claude Code sessions (scope with --wing per project)

# Search
mempalace search "why did we switch to GraphQL"

# Load context for a new session
mempalace wake-up
```

For Claude Code, Gemini CLI, MCP-compatible tools, and local models, see
[mempalaceofficial.com/guide/getting-started](https://mempalaceofficial.com/guide/getting-started.html).

---

## Benchmarks

All numbers below are reproducible from this repository with the commands
in [`benchmarks/BENCHMARKS.md`](benchmarks/BENCHMARKS.md). Full
per-question result files are committed under `benchmarks/results_*`.

**LongMemEval — retrieval recall (R@5, 500 questions):**

| Mode | R@5 | LLM required |
|---|---|---|
| Raw (semantic search, no heuristics, no LLM) | **96.6%** | None |
| Hybrid v4, held-out 450q (tuned on 50 dev, not seen during training) | **98.4%** | None |
| Hybrid v4 + LLM rerank (full 500) | ≥99% | Any capable model |

The raw 96.6% requires no API key, no cloud, and no LLM at any stage. The
hybrid pipeline adds keyword boosting, temporal-proximity boosting, and
preference-pattern extraction; the held-out 98.4% is the honest
generalisable figure.

The rerank pipeline promotes the best candidate out of the top-20
retrieved sessions using an LLM reader. It works with any reasonably
capable model — we have reproduced it with Claude Haiku, Claude Sonnet,
and minimax-m2.7 via Ollama Cloud (no Anthropic dependency). The gap
between raw and reranked is model-agnostic; we do not headline a "100%"
number because the last 0.6% was reached by inspecting specific wrong
answers, which `benchmarks/BENCHMARKS.md` flags as teaching to the test.

**Other benchmarks (full results in [`benchmarks/BENCHMARKS.md`](benchmarks/BENCHMARKS.md)):**

| Benchmark | Metric | Score | Notes |
|---|---|---|---|
| LoCoMo (session, top-10, no rerank) | R@10 | 60.3% | 1,986 questions |
| LoCoMo (hybrid v5, top-10, no rerank) | R@10 | 88.9% | Same set |
| ConvoMem (all categories, 250 items) | Avg recall | 92.9% | 50 per category |
| MemBench (ACL 2025, 8,500 items) | R@5 | 80.3% | All categories |

We deliberately do not include a side-by-side comparison against Mem0,
Mastra, Hindsight, Supermemory, or Zep. Those projects publish different
metrics on different splits, and placing retrieval recall next to
end-to-end QA accuracy is not an honest comparison. See each project's
own research page for their published numbers.

**Reproducing every result:**

```bash
git clone https://github.com/MemPalace/mempalace.git
cd mempalace
pip install -e ".[dev]"
# see benchmarks/README.md for dataset download commands
python benchmarks/longmemeval_bench.py /path/to/longmemeval_s_cleaned.json
```

---

## Knowledge graph

MemPalace includes a temporal entity-relationship graph with validity
windows — add, query, invalidate, timeline — backed by local SQLite.
Usage and tool reference:
[mempalaceofficial.com/concepts/knowledge-graph](https://mempalaceofficial.com/concepts/knowledge-graph.html).

## MCP server

29 MCP tools cover palace reads/writes, knowledge-graph operations,
cross-wing navigation, drawer management, and agent diaries. Installation
and the full tool list:
[mempalaceofficial.com/reference/mcp-tools](https://mempalaceofficial.com/reference/mcp-tools.html).

## Agents

Each specialist agent gets its own wing and diary in the palace.
Discoverable at runtime via `mempalace_list_agents` — no bloat in your
system prompt:
[mempalaceofficial.com/concepts/agents](https://mempalaceofficial.com/concepts/agents.html).

## Auto-save hooks

Two Claude Code hooks save periodically and before context compression:
[mempalaceofficial.com/guide/hooks](https://mempalaceofficial.com/guide/hooks.html).

---

## Requirements

- Python 3.9+
- A vector-store backend (ChromaDB by default)
- ~300 MB disk for the default embedding model

No API key is required for the core benchmark path.

## Docs

- Getting started → [mempalaceofficial.com/guide/getting-started](https://mempalaceofficial.com/guide/getting-started.html)
- CLI reference → [mempalaceofficial.com/reference/cli](https://mempalaceofficial.com/reference/cli.html)
- Python API → [mempalaceofficial.com/reference/python-api](https://mempalaceofficial.com/reference/python-api.html)
- Full benchmark methodology → [benchmarks/BENCHMARKS.md](benchmarks/BENCHMARKS.md)
- Release notes → [CHANGELOG.md](CHANGELOG.md)
- Corrections and public notices → [docs/HISTORY.md](docs/HISTORY.md)

## Contributing

PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).

<!-- Link Definitions -->
[version-shield]: https://img.shields.io/badge/version-3.3.0-4dc9f6?style=flat-square&labelColor=0a0e14
[release-link]: https://github.com/MemPalace/mempalace/releases
[python-shield]: https://img.shields.io/badge/python-3.9+-7dd8f8?style=flat-square&labelColor=0a0e14&logo=python&logoColor=7dd8f8
[python-link]: https://www.python.org/
[license-shield]: https://img.shields.io/badge/license-MIT-b0e8ff?style=flat-square&labelColor=0a0e14
[license-link]: https://github.com/MemPalace/mempalace/blob/main/LICENSE
[discord-shield]: https://img.shields.io/badge/discord-join-5865F2?style=flat-square&labelColor=0a0e14&logo=discord&logoColor=5865F2
[discord-link]: https://discord.com/invite/ycTQQCu6kn

Languages: Python 89.1%, HTML 4.5%, CSS 3.1%, Vue 1.4%, JavaScript 0.9%, Shell 0.8%, TypeScript 0.3%

## Recent Releases

### v3.3.2 (2026-04-21)

## What's Changed

### Bug fixes
- **PID file guard** — prevents stacking mine processes (#1023)
- **Quarantine stale HNSW** — recover from HNSW/sqlite drift, fixes SIGSEGV crash (#1000)
- **Windows Unicode** — replace Unicode checkmark with ASCII for Windows encoding (#681)

### Copilot review fixes
- Address Copilot review on release/3.3.2 (#1045)

**Full Changelog**: https://github.com/MemPalace/mempalace/compare/v3.3.1...v3.3.2

### v3.3.1 (2026-04-18)

## MemPalace v3.3.1

### Highlights

- **Multi-language entity detection** — 5 new locales (Portuguese, Russian, Italian, Hindi, Indonesian) with full entity-detection patterns
- **Script-aware word boundaries** — fixes name truncation for Devanagari, Arabic, Hebrew, Thai, Tamil, Khmer scripts
- **Case-insensitive BCP 47 language codes** — `--lang PT-BR`, `zh-cn`, `Pt-Br` all resolve correctly
- **KG thread safety** — lock on `close()`, `query_relationship`, `timeline`, `stats`
- **entity_registry.research()** defaults to local-only (no outbound Wikipedia calls without opt-in)
- **Precompact h…

### v3.3.0 (2026-04-14)

**Visit [mempalaceofficial.com](https://www.mempalaceofficial.com) for the full story behind this release and a visual guide to the architecture.**



---

## Highlights

### Closets are here

The architecture we designed — wings, rooms, closets, drawers — is finally complete. Closets are the searchable index layer: compact AAAK pointers that tell the searcher which drawer to open. Search hits closets first (fast), then hydrates the full verbatim content from drawers.

Closets are a **boost signal, not a gate** — direct drawer search always runs as the floor. Closets can only improve results, …

### v3.1.0 (2026-04-09)

First PyPI cut since v3.0.0 on 2026-04-06 — **39 merged PRs**. This release closes the pip/plugin version drift (#290, #296) and lands the first-week community fixes.

## 🔒 Security
- **#387** Input validation at MCP entry points, shell-injection fix in save hook, file size guard + symlink skip, SQLite connection leak fix, WAL audit trail, hardened file perms
- **#141** Sanitize `SESSION_ID` in save hook
- **#139** Sanitize MCP error responses, remove `sys.exit` from library code

## 🐛 Bug fixes (highlights)
- **#399** MCP null args hang, `cmd_repair` infinite recursion, 500 MB OOM guard
- **#…

### v3.0.0 (2026-04-06)

## MemPalace v3.0.0

The highest-scoring AI memory system ever benchmarked. And it's free.

### Install

```bash
pip install mempalace
```

**PyPI:** https://pypi.org/project/mempalace/

### Highlights

- **96.6% LongMemEval R@5** — highest published score with zero API calls
- **100% LongMemEval R@5** — with optional Haiku rerank
- **Palace architecture** — wings, rooms, halls, tunnels, closets, drawers — +34% retrieval from structure alone
- **AAAK compression** — 30x lossless shorthand dialect, works with any LLM (Claude, GPT, Gemini, Llama, Mistral)
- **Knowledge graph** — temporal entity-…

## Recent Commits

- 2026-04-22 9b35d9f Ben Sigman: Merge pull request #661 from jphein/perf/graph-cache
- 2026-04-22 23ee2a0 Ben Sigman: Merge pull request #673 from jphein/feat/deterministic-hook-save
- 2026-04-22 02aafc0 Ben Sigman: Merge pull request #1021 from jphein/upstream-fix/silent-save-visibility
- 2026-04-22 810f9a5 Ben Sigman: Merge pull request #851 from vnguyen-lexipol/fix/status-paginate-large-palaces
- 2026-04-21 74e9cbc jp: feat: deterministic hook saves — zero data loss via silent Python API
- 2026-04-21 1b00f93 Igor Lins e Silva: Merge pull request #833 from MemPalace/fix/hooks-python-resolution
- 2026-04-13 48eb627 Igor Lins e Silva: fix(hooks): MEMPAL_PYTHON override for .sh hooks' internal python3 calls
- 2026-04-21 5522d34 Igor Lins e Silva: Merge pull request #340 from messelink/fix/mcp-pipx-compat
- 2026-04-16 9e53228 Pim Messelink: test: update test_cli assertions for mempalace-mcp entry point
- 2026-04-16 982d421 Pim Messelink: fix: update mempalace mcp command to use mempalace-mcp entry point
- 2026-04-16 67a0677 Pim Messelink: fix: use mempalace CLI in top-level hook scripts
- 2026-04-09 be89e49 Pim Messelink: fix: use mempalace CLI in hook scripts instead of python3 -m
- 2026-04-09 9f5b8f5 Pim Messelink: fix: add mempalace-mcp console entry point for pipx/uv compatibility
- 2026-04-21 4fb0ee5 Igor Lins e Silva: Merge pull request #942 from fatkobra/fix-hooks-resolve-claude-plugin
- 2026-04-21 1a180cd Igor Lins e Silva: Merge pull request #1051 from itfarrier/feat/i18n-belarusian
- 2026-04-21 6d42f61 Igor Lins e Silva: Merge pull request #1001 from mvalentsev/feat/i18n-de-es-fr-entity
- 2026-04-21 2a5914b Igor Lins e Silva: Merge pull request #945 from lmanchu/feat/zh-entity-detection
- 2026-04-19 54c314d Dzmitry Padabed: feat(i18n): add Belarusian
- 2026-04-19 d657626 jp: style: ruff format — collapse AttributeError log call to single line
- 2026-04-19 2629ae5 jp: fix(hooks): default silent_guard=True — config-read failure must not suppress saves

## Open Issues (top 10)

- #1082 MCP tool_search returns "Error finding id" when wing-scoped to a convos-mined wing (CLI works, unscoped MCP works) (by raphaelsamy)
- #1049 Hooks and MCP server break in projects with Python venv (hardcoded `python3`) (by sergesha)
- #1093 v3.3.2 release defect: `mempalace-mcp` entry point missing from `pyproject.toml` despite `plugin.json` requiring it — MCP server fails to start on fresh install (by jphein)
- #101 feat: Multipass -- multi-hop paths through the Mem Palace (by M0nkeyFl0wer)
- #1092 Concurrent writers (hooks + MCP server + CLI) corrupt the palace on chromadb 1.5.8 — sparse-file bloat + SIGSEGV (by AndreyBelyy)
- #1088 proposal: concurrent mining via ThreadPoolExecutor + `bulk_check_mined()` pre-fetch (by jphein)
- #1091 Runaway HNSW index explosion (582 GB link_lists.bin) on add_drawer to new room in large wing (by marcel10100)
- #1083 Stop + PreCompact hooks auto-run `mempalace mine` on chat transcript parent with default flags → polluted mega-wing, no opt-out (by raphaelsamy)
- #357 Parallel mining corrupts ChromaDB HNSW index — no warning, silent failure (by fubak)

## Recently Merged PRs (top 10)

- #661 perf: graph cache with write-invalidation in build_graph() (merged 2026-04-22)
- #673 feat: deterministic hook saves — zero data loss via silent Python API (merged 2026-04-22)
- #1021 fix(hooks): restore silent-save visibility on Claude Code 2.1.114 (merged 2026-04-22)
- #851 fix(status): paginate metadata fetch to support large palaces (merged 2026-04-22)
- #833 fix(hooks): real python-resolution for .sh hooks, with MEMPAL_PYTHON override (merged 2026-04-21)
- #340 fix: add mempalace-mcp entry point for pipx/uv compatibility (merged 2026-04-21)
- #942 fix(hooks): resolve Claude plugin hook runner cross-platform (merged 2026-04-21)
- #1051 feat(i18n): add Belarusian (merged 2026-04-21)
- #1001 feat(i18n): add entity detection to German, Spanish, and French locales (merged 2026-04-21)
- #945 feat(i18n): add Traditional + Simplified Chinese entity detection (merged 2026-04-21)


## File: .claude-plugin/README.md

```
# MemPalace Claude Code Plugin

A Claude Code plugin that gives your AI a persistent memory system. Mine projects and conversations into a searchable palace backed by ChromaDB, with 19 MCP tools, auto-save hooks, and 5 guided skills.

## Prerequisites

- Python 3.9+

## Installation

### Claude Code Marketplace

```bash
claude plugin marketplace add MemPalace/mempalace
claude plugin install --scope user mempalace
```

### Local Clone

```bash
claude plugin add /path/to/mempalace
```

## Post-Install Setup

After installing the plugin, run the init command to complete setup (pip install, MCP configuration, etc.):

```
/mempalace:init
```

## Available Slash Commands

| Command | Description |
|---------|-------------|
| `/mempalace:help` | Show available tools, skills, and architecture |
| `/mempalace:init` | Set up MemPalace -- install, configure MCP, onboard |
| `/mempalace:search` | Search your memories across the palace |
| `/mempalace:mine` | Mine projects and conversations into the palace |
| `/mempalace:status` | Show palace overview -- wings, rooms, drawer counts |

## Hooks

MemPalace registers two hooks that run automatically:

- **Stop** -- Saves conversation context every 15 messages.
- **PreCompact** -- Preserves important memories before context compaction.

Set the `MEMPAL_DIR` environment variable to a directory path to automatically run `mempalace mine` on that directory during each save trigger.

## MCP Server

The plugin automatically configures a local MCP server with 19 tools for storing, searching, and managing memories. No manual MCP setup is required -- `/mempalace:init` handles everything.

## Full Documentation

See the main [README](../README.md) for complete documentation, architecture details, and advanced usage.

```


## File: .codex-plugin/README.md

```
# MemPalace - Codex CLI Plugin

Give your AI a persistent memory -- mine projects and conversations into a searchable palace backed by ChromaDB, with 19 MCP tools, auto-save hooks, and guided skills.

## Prerequisites

- Python 3.9+
- Codex CLI installed and configured
- `pip install mempalace`

## Installation

### Local Install

1. Copy or symlink the `.codex-plugin` directory into your project root:

```bash
cp -r .codex-plugin /path/to/your/project/.codex-plugin
```

2. Verify the plugin is detected:

```bash
codex --plugins
```

3. Initialize your palace:

```bash
codex /init
```

### Git Install

1. Clone the MemPalace repository:

```bash
git clone https://github.com/MemPalace/mempalace.git
cd mempalace
```

2. Install the Python package:

```bash
pip install -e .
```

3. The `.codex-plugin` directory is already in the repo root. Codex CLI will detect it automatically when you run Codex from inside the repository.

4. Initialize your palace:

```bash
codex /init
```

## Available Skills

| Skill | Description |
|-------|-------------|
| `/help` | Show available commands and usage tips |
| `/init` | Initialize a new memory palace |
| `/search` | Semantic search across all mined memories |
| `/mine` | Mine a project or conversation into your palace |
| `/status` | Show palace status, room counts, and health |

## Hooks

The plugin includes auto-save hooks that run on session stop (every 15 messages) and before context compaction, automatically preserving conversation context into your palace.

Set the `MEMPAL_DIR` environment variable to a directory path to automatically run `mempalace mine` on that directory during each save trigger.

## Support

- Repository: https://github.com/MemPalace/mempalace
- Issues: https://github.com/MemPalace/mempalace/issues

```


## File: .gitignore

```
*.egg-info/
dist/
build/
__pycache__/
*.pyc
.pytest_cache/
mempal.yaml
.a5c/
.claude/
.codex/
.codex

# Environment
.env
.env.*

# OS
.DS_Store
Thumbs.db

# IDEs
.idea/
.vscode/
*.swp
*.swo
*~

# Coverage
htmlcov/
.coverage
coverage.xml

# Virtual environments
.venv/
venv/

# ChromaDB local data
*.sqlite3-journal

```


## File: benchmarks/README.md

```
# MemPalace Benchmarks — Reproduction Guide

Run the exact same benchmarks we report. Clone, install, run.

## Setup

```bash
git clone https://github.com/MemPalace/mempalace.git
cd mempalace
pip install -e ".[dev]"
```

## Benchmark 1: LongMemEval (500 questions)

Tests retrieval across ~53 conversation sessions per question. The standard benchmark for AI memory.

```bash
# Download data
mkdir -p /tmp/longmemeval-data
curl -fsSL -o /tmp/longmemeval-data/longmemeval_s_cleaned.json \
  https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned/resolve/main/longmemeval_s_cleaned.json

# Run (raw mode — our headline 96.6% result)
python benchmarks/longmemeval_bench.py /tmp/longmemeval-data/longmemeval_s_cleaned.json

# Run with AAAK compression (84.2%)
python benchmarks/longmemeval_bench.py /tmp/longmemeval-data/longmemeval_s_cleaned.json --mode aaak

# Run with room-based boosting (89.4%)
python benchmarks/longmemeval_bench.py /tmp/longmemeval-data/longmemeval_s_cleaned.json --mode rooms

# Quick test on 20 questions first
python benchmarks/longmemeval_bench.py /tmp/longmemeval-data/longmemeval_s_cleaned.json --limit 20

# Turn-level granularity
python benchmarks/longmemeval_bench.py /tmp/longmemeval-data/longmemeval_s_cleaned.json --granularity turn
```

**Expected output (raw mode, full 500):**
```
Recall@5:  0.966
Recall@10: 0.982
NDCG@10:   0.889
Time:      ~5 minutes on Apple Silicon
```

## Benchmark 2: LoCoMo (1,986 QA pairs)

Tests multi-hop reasoning across 10 long conversations (19-32 sessions each, 400-600 dialog turns).

```bash
# Clone LoCoMo
git clone https://github.com/snap-research/locomo.git /tmp/locomo

# Run (session granularity — our 60.3% result)
python benchmarks/locomo_bench.py /tmp/locomo/data/locomo10.json --granularity session

# Dialog granularity (harder — 48.0%)
python benchmarks/locomo_bench.py /tmp/locomo/data/locomo10.json --granularity dialog

# Higher top-k (77.8% at top-50)
python benchmarks/locomo_bench.py /tmp/locomo/data/locomo10.json --top-k 50

# Quick test on 1 conversation
python benchmarks/locomo_bench.py /tmp/locomo/data/locomo10.json --limit 1
```

**Expected output (session, top-10, full 10 conversations):**
```
Avg Recall: 0.603
Temporal:   0.692
Time:       ~2 minutes
```

## Benchmark 3: ConvoMem (Salesforce, 75K+ QA pairs)

Tests six categories of conversational memory. Downloads from HuggingFace automatically.

```bash
# Run all categories, 50 items each (our 92.9% result)
python benchmarks/convomem_bench.py --category all --limit 50

# Single category
python benchmarks/convomem_bench.py --category user_evidence --limit 100

# Quick test
python benchmarks/convomem_bench.py --category user_evidence --limit 10
```

**Categories available:** `user_evidence`, `assistant_facts_evidence`, `changing_evidence`, `abstention_evidence`, `preference_evidence`, `implicit_connection_evidence`

**Expected output (all categories, 50 each):**
```
Avg Recall: 0.929
Assistant Facts: 1.000
User Facts:      0.980
Time:            ~2 minutes
```

## What Each Benchmark Tests

| Benchmark | What it measures | Why it matters |
|---|---|---|
| **LongMemEval** | Can you find a fact buried in 53 sessions? | Tests basic retrieval quality — the "needle in a haystack" |
| **LoCoMo** | Can you connect facts across conversations over weeks? | Tests multi-hop reasoning and temporal understanding |
| **ConvoMem** | Does your memory system work at scale? | Tests all memory types: facts, preferences, changes, abstention |

## Results Files

Raw results are in `benchmarks/results_*.jsonl` and `benchmarks/results_*.json`. Each file contains every question, every retrieved document, and every score — fully auditable.

## Requirements

- Python 3.9+
- `chromadb` (the only dependency)
- ~300MB disk for LongMemEval data
- ~5 minutes for each full benchmark run
- No API key. No internet during benchmark (after data download). No GPU.

## Next Benchmarks (Planned)

- **Scale testing** — ConvoMem at 50/100/300 conversations per item
- **Hybrid AAAK** — search raw text, deliver AAAK-compressed results
- **End-to-end QA** — retrieve + generate answer + measure F1 (needs LLM API key)

```


## File: hooks/README.md

```
# MemPalace Hooks — Auto-Save for Terminal AI Tools

These hook scripts make MemPalace save automatically. No manual "save" commands needed.

## What They Do

| Hook | When It Fires | What Happens |
|------|--------------|-------------|
| **Save Hook** | Every 15 human messages | Auto-mines transcript (tool output included), then blocks the AI to save topics/decisions/quotes |
| **PreCompact Hook** | Right before context compaction | Auto-mines transcript, then emergency save — forces the AI to save EVERYTHING before losing context |

**Two-layer capture:** Hooks auto-mine the JSONL transcript directly into the palace (capturing raw tool output — Bash results, search findings, build errors). They also block the AI with a reason message telling it to save verbatim tool output and key context. Belt and suspenders — tool output gets stored even if the AI summarizes instead of quoting.

## Install — Claude Code

Add to `.claude/settings.local.json`:

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "/absolute/path/to/hooks/mempal_save_hook.sh",
        "timeout": 30
      }]
    }],
    "PreCompact": [{
      "hooks": [{
        "type": "command",
        "command": "/absolute/path/to/hooks/mempal_precompact_hook.sh",
        "timeout": 30
      }]
    }]
  }
}
```

Make them executable:
```bash
chmod +x hooks/mempal_save_hook.sh hooks/mempal_precompact_hook.sh
```

## Install — Codex CLI (OpenAI)

Add to `.codex/hooks.json`:

```json
{
  "Stop": [{
    "type": "command",
    "command": "/absolute/path/to/hooks/mempal_save_hook.sh",
    "timeout": 30
  }],
  "PreCompact": [{
    "type": "command",
    "command": "/absolute/path/to/hooks/mempal_precompact_hook.sh",
    "timeout": 30
  }]
}
```

## Configuration

Edit `mempal_save_hook.sh` to change:

- **`SAVE_INTERVAL=15`** — How many human messages between saves. Lower = more frequent saves, higher = less interruption.
- **`STATE_DIR`** — Where hook state is stored (defaults to `~/.mempalace/hook_state/`)
- **`MEMPAL_DIR`** — Optional. Set to a conversations directory to auto-run `mempalace mine <dir>` on each save trigger. Leave blank (default) to let the AI handle saving via the block reason message.
- **`MEMPALACE_PYTHON`** — Optional env var. Python interpreter with mempalace + chromadb installed. Auto-detects: `MEMPALACE_PYTHON` env var → repo `venv/bin/python3` → system `python3`. Set this if your venv is in a non-standard location.

### mempalace CLI

The relevant commands are:

```bash
mempalace mine <dir>               # Mine all files in a directory
mempalace mine <dir> --mode convos # Mine conversation transcripts only
```

The hooks resolve the repo root automatically from their own path, so they work regardless of where you install the repo.

## How It Works (Technical)

### Save Hook (Stop event)

```
User sends message → AI responds → Claude Code fires Stop hook
                                            ↓
                                    Hook counts human messages in JSONL transcript
                                            ↓
                              ┌─── < 15 since last save ──→ echo "{}" (let AI stop)
                              │
                              └─── ≥ 15 since last save
                                            ↓
                                    Auto-mine transcript → palace (tool output captured)
                                            ↓
                                    {"decision": "block", "reason": "save tool output verbatim..."}
                                            ↓
                                    AI saves to palace (topics, decisions, quotes)
                                            ↓
                                    AI tries to stop again
                                            ↓
                                    stop_hook_active = true
                                            ↓
                                    Hook sees flag → echo "{}" (let it through)
```

The `stop_hook_active` flag prevents infinite loops: block once → AI saves → tries to stop → flag is true → we let it through.

### PreCompact Hook

```
Context window getting full → Claude Code fires PreCompact
                                        ↓
                                Find transcript (from input or session_id lookup)
                                        ↓
                                Auto-mine transcript → palace (tool output captured)
                                        ↓
                                {"decision": "block", "reason": "save tool output verbatim..."}
                                        ↓
                                AI saves everything
                                        ↓
                                Compaction proceeds
```

No counting needed — compaction always warrants a save. The auto-mine captures raw tool output before the AI gets a chance to summarize it away.

## Debugging

Check the hook log:
```bash
cat ~/.mempalace/hook_state/hook.log
```

Example output:
```
[14:30:15] Session abc123: 12 exchanges, 12 since last save
[14:35:22] Session abc123: 15 exchanges, 15 since last save
[14:35:22] TRIGGERING SAVE at exchange 15
[14:40:01] Session abc123: 18 exchanges, 3 since last save
```

## Known Limitations

**Hooks require session restart after install.** Claude Code loads hooks from `settings.json` at session start only. If you run `mempalace init` or manually edit hook config mid-session, the hooks won't fire until you restart Claude Code. This is a Claude Code limitation.

**`MEMPAL_PYTHON` override for the hook's internal Python calls.** The save hook parses its JSON input and counts transcript messages with `python3`. When the harness is launched from a GUI on macOS — `open -a`, Spotlight, the dock — its `PATH` is the minimal `/usr/bin:/bin:/usr/sbin:/sbin` inherited from `launchd`, not your shell PATH. If `python3` isn't on that PATH, those internal calls fail and the hook can't count exchanges.

Point the hook at any Python 3 interpreter to fix it:

```bash
export MEMPAL_PYTHON="/usr/bin/python3"                   # system Python is fine
export MEMPAL_PYTHON="$HOME/.venvs/mempalace/bin/python"  # or your venv
```

Resolution priority: `$MEMPAL_PYTHON` (if set and executable) → `$(command -v python3)` → bare `python3`. The interpreter only needs `json` and `sys` from the standard library — `mempalace` itself does not need to be installed in it.

Note: the `mempalace mine` auto-ingest runs via the `mempalace` CLI, so that command also needs to be on the hook's `PATH`. Installing with `pipx install mempalace` or `uv tool install mempalace` puts it on a stable global location; otherwise extend the hook environment's `PATH` to include your venv's `bin/`.

## Backfill Past Conversations

The hooks only capture conversations going forward. To mine **past** Claude Code sessions into your palace, run a one-time backfill:

```bash
mempalace mine ~/.claude/projects/ --mode convos
```

This scans all JSONL transcripts from previous sessions and files them into the `conversations` wing. On a typical developer machine with months of history, this can yield 50K–200K drawers.

For Codex CLI sessions:
```bash
mempalace mine ~/.codex/sessions/ --mode convos
```

This only needs to be done once — after that, the hooks auto-mine each session as you go.

## Cost

**Zero extra tokens.** The hooks notify the AI that saves happened in the background — the AI doesn't need to write anything in the chat. All filing is handled automatically. Previous versions asked the AI to write diary entries and drawer content in the chat window, which cost ~$1/session in retransmitted tokens.

```


## File: LICENSE

```
MIT License

Copyright (c) 2026 MemPalace Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```


## File: mempalace/README.md

```
# mempalace/ — Core Package

The Python package that powers MemPalace. All modules, all logic.

## Modules

| Module | What it does |
|--------|-------------|
| `cli.py` | CLI entry point — routes to mine, search, init, compress, wake-up |
| `config.py` | Configuration loading — `~/.mempalace/config.json`, env vars, defaults |
| `normalize.py` | Converts 5 chat formats (Claude Code JSONL, Claude.ai JSON, ChatGPT JSON, Slack JSON, plain text) to standard transcript format |
| `miner.py` | Project file ingest — scans directories, chunks by paragraph, stores to ChromaDB |
| `convo_miner.py` | Conversation ingest — chunks by exchange pair (Q+A), detects rooms from content |
| `searcher.py` | Semantic search via ChromaDB vectors — filters by wing/room, returns verbatim + scores |
| `layers.py` | 4-layer memory stack: L0 (identity), L1 (critical facts), L2 (room recall), L3 (deep search) |
| `dialect.py` | AAAK compression — entity codes, emotion markers, 30x lossless ratio |
| `knowledge_graph.py` | Temporal entity-relationship graph — SQLite, time-filtered queries, fact invalidation |
| `palace_graph.py` | Room-based navigation graph — BFS traversal, tunnel detection across wings |
| `mcp_server.py` | MCP server — 19 tools, AAAK auto-teach, Palace Protocol, agent diary |
| `onboarding.py` | Guided first-run setup — asks about people/projects, generates AAAK bootstrap + wing config |
| `entity_registry.py` | Entity code registry — maps names to AAAK codes, handles ambiguous names |
| `entity_detector.py` | Auto-detect people and projects from file content |
| `general_extractor.py` | Classifies text into 5 memory types (decision, preference, milestone, problem, emotional) |
| `room_detector_local.py` | Maps folders to room names using 70+ patterns — no API |
| `spellcheck.py` | Name-aware spellcheck — won't "correct" proper nouns in your entity registry |
| `split_mega_files.py` | Splits concatenated transcript files into per-session files |

## Architecture

```
User → CLI → miner/convo_miner → ChromaDB (palace)
                                     ↕
                              knowledge_graph (SQLite)
                                     ↕
User → MCP Server → searcher → results
                  → kg_query → entity facts
                  → diary    → agent journal
```

The palace (ChromaDB) stores verbatim content. The knowledge graph (SQLite) stores structured relationships. The MCP server exposes both to any AI tool.

```


## File: pyproject.toml

```
[project]
name = "mempalace"
version = "3.3.0"
description = "Give your AI a memory — mine projects and conversations into a searchable palace. No API key required."
readme = "README.md"
requires-python = ">=3.9"
license = "MIT"
authors = [
    {name = "milla-jovovich"},
]
keywords = [
    "ai", "memory", "llm", "rag", "chromadb", "mcp",
    "vector-database", "claude", "chatgpt", "embeddings",
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Utilities",
]
dependencies = [
    "chromadb>=1.5.4,<2",
    "pyyaml>=6.0,<7",
]

[project.urls]
Homepage = "https://github.com/MemPalace/mempalace"
Repository = "https://github.com/MemPalace/mempalace"
"Bug Tracker" = "https://github.com/MemPalace/mempalace/issues"

[project.scripts]
mempalace = "mempalace.cli:main"
mempalace-mcp = "mempalace.mcp_server:main"

[project.entry-points."mempalace.backends"]
chroma = "mempalace.backends.chroma:ChromaBackend"

# RFC 002 source-adapter entry-point group. Core publishes no first-party
# adapters under this group yet; ``miner.py`` and ``convo_miner.py`` migrate
# onto ``BaseSourceAdapter`` in a follow-up PR. Third-party adapter packages
# (``mempalace-source-cursor``, ``mempalace-source-git``, …) register here.
[project.entry-points."mempalace.sources"]

[project.optional-dependencies]
dev = ["pytest>=7.0", "pytest-cov>=4.0", "ruff>=0.4.0", "psutil>=5.9"]
spellcheck = ["autocorrect>=2.0"]

[dependency-groups]
dev = ["pytest>=7.0", "pytest-cov>=4.0", "ruff>=0.4.0", "psutil>=5.9"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["mempalace"]

[tool.ruff]
line-length = 100
target-version = "py39"
extend-exclude = ["benchmarks"]

[tool.ruff.lint]
select = ["E", "F", "W", "C901"]
ignore = ["E501"]

[tool.ruff.lint.mccabe]
max-complexity = 25

[tool.ruff.format]
quote-style = "double"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
addopts = "-m 'not benchmark and not slow and not stress'"
markers = [
    "benchmark: scale/performance benchmark tests",
    "slow: tests that take more than 30 seconds",
    "stress: destructive scale tests (100K+ drawers)",
]

[tool.coverage.run]
source = ["mempalace"]

[tool.coverage.report]
fail_under = 85
show_missing = true
exclude_lines = [
    "if __name__",
    "pragma: no cover",
]

```


## File: tests/benchmarks/README.md

```
# MemPalace Scale Benchmark Suite

106 tests that benchmark mempalace at scale to validate real-world performance limits.

## Why

MemPalace has strong academic scores (96.6% R@5 on LongMemEval) but no empirical data on how it behaves at scale. Key unknowns:

- `tool_status()` loads ALL metadata into memory — at what palace size does this OOM?
- `PersistentClient` is re-instantiated on every MCP call — what's the overhead?
- Modified files are never re-ingested — what's the skip-check cost at scale?
- How does query latency degrade as the palace grows from 1K to 100K drawers?
- Does wing/room filtering actually improve retrieval, and by how much?
- At what per-room drawer count does recall break regardless of filtering?

This suite finds those answers.

## Quick Start

```bash
# Fast smoke test (~2 min)
uv run pytest tests/benchmarks/ -v --bench-scale=small -m "benchmark and not slow"

# Full small scale (~35 min)
uv run pytest tests/benchmarks/ -v --bench-scale=small

# Medium scale with JSON report
uv run pytest tests/benchmarks/ -v --bench-scale=medium --bench-report=results.json

# Stress test (local only, very slow)
uv run pytest tests/benchmarks/ -v --bench-scale=stress -m stress
```

## Scale Levels

| Level   | Drawers | Wings | Rooms/Wing | KG Triples | Use case            |
|---------|---------|-------|------------|------------|---------------------|
| small   | 1,000   | 3     | 5          | 200        | CI, quick checks    |
| medium  | 10,000  | 8     | 12         | 2,000      | Pre-release testing |
| large   | 50,000  | 15    | 20         | 10,000     | Scale limit finding |
| stress  | 100,000 | 25    | 30         | 50,000     | Breaking point      |

## Test Modules

### Critical Path

| File | What it tests |
|------|--------------|
| `test_mcp_bench.py` | MCP tool response times, unbounded metadata fetch, client re-instantiation overhead |
| `test_chromadb_stress.py` | ChromaDB breaking point, query degradation curve, batch vs sequential insert |
| `test_memory_profile.py` | RSS/heap growth over repeated operations, leak detection |

### Performance Baselines

| File | What it tests |
|------|--------------|
| `test_ingest_bench.py` | Mining throughput (files/sec, drawers/sec), peak RSS, chunking speed, re-ingest skip overhead |
| `test_search_bench.py` | Query latency vs palace size, recall@k with planted needles, concurrent queries, n_results scaling |

### Architectural Validation

| File | What it tests |
|------|--------------|
| `test_palace_boost.py` | Retrieval improvement from wing/room filtering at different scales |
| `test_recall_threshold.py` | Per-room recall ceiling — isolates embedding model limit with all drawers in one bucket |
| `test_knowledge_graph_bench.py` | Triple insertion rate, temporal query accuracy, SQLite concurrent access |
| `test_layers_bench.py` | MemoryStack wake-up cost, Layer1 unbounded fetch, token budget compliance |

## Architecture

```
tests/benchmarks/
  conftest.py              # --bench-scale / --bench-report CLI options, fixtures, markers
  data_generator.py        # Deterministic data factory (seeded RNG, planted needles)
  report.py                # JSON report writer + regression checker
  test_*.py                # 9 test modules (106 tests total)
```

### Data Generator

`PalaceDataGenerator(seed=42, scale="small")` produces deterministic, realistic test data:

- **`generate_project_tree()`** — writes real files + `mempalace.yaml` for `mine()` to ingest
- **`populate_palace_directly()`** — bypasses mining, inserts directly into ChromaDB (10-100x faster for search/MCP benchmarks)
- **`generate_kg_triples()`** — entity-relationship triples with temporal validity
- **`generate_search_queries()`** — queries with known-good answers for recall measurement

**Planted needles**: Unique identifiable content (e.g., `NEEDLE_0042: PostgreSQL vacuum autovacuum threshold...`) seeded into specific wings/rooms. Search queries target these needles, enabling recall@k measurement without an LLM judge.

### JSON Reports

When run with `--bench-report=path.json`, produces machine-readable output:

```json
{
  "timestamp": "2026-04-07T...",
  "git_sha": "abc123",
  "scale": "small",
  "system": {"os": "linux", "cpu_count": 8},
  "results": {
    "mcp_status": {"latency_ms_at_1000": 45.2, "rss_delta_mb_at_5000": 12.3},
    "search": {"avg_latency_ms_at_5000": 23.1, "recall_at_5": 0.92},
    "chromadb_insert": {"sequential_ms": 8500, "batched_ms": 1200, "speedup_ratio": 7.1}
  }
}
```

### Regression Detection

```python
from tests.benchmarks.report import check_regression

regressions = check_regression("current.json", "baseline.json", threshold=0.2)
# Returns list of metric descriptions that degraded beyond 20%
```

## CI Integration

The GitHub Actions workflow runs benchmarks on PRs at small scale:

```yaml
benchmark:
  runs-on: ubuntu-latest
  if: github.event_name == 'pull_request'
  # Runs: pytest tests/benchmarks/ -m "benchmark and not stress and not slow" --bench-scale=small
```

Existing unit tests are isolated with `--ignore=tests/benchmarks`.

## Markers

- `@pytest.mark.benchmark` — all benchmark tests
- `@pytest.mark.slow` — tests taking >30s even at small scale
- `@pytest.mark.stress` — tests that should only run at large/stress scale

## Dependencies

Only one new dependency beyond the existing dev stack: `psutil` (for cross-platform RSS measurement). `tracemalloc` and `resource` are stdlib.

```


## File: website/.gitignore

```
# dependencies (bun install)
node_modules

# output
out
dist
.vitepress/dist
.vitepress/cache
.vitepress/.temp
*.tgz

# code coverage
coverage
*.lcov

# logs
logs
*.log
report.[0-9]_.[0-9]_.[0-9]_.[0-9]_.json

# dotenv environment variable files
.env
.env.development.local
.env.test.local
.env.production.local
.env.local

# caches
.eslintcache
.cache
*.tsbuildinfo

# IntelliJ based IDEs
.idea

# Finder (MacOS) folder config
.DS_Store

```


## File: website/package.json

```
{
  "name": "mempalace-docs",
  "private": true,
  "type": "module",
  "scripts": {
    "docs:dev": "vitepress dev",
    "docs:build": "vitepress build",
    "docs:preview": "vitepress preview"
  },
  "devDependencies": {
    "@lucide/vue": "^1.8.0",
    "mermaid": "^11.14.0",
    "vitepress": "^1.6.4",
    "vitepress-plugin-mermaid": "^2.0.17",
    "vue": "^3.5.32"
  }
}

```


## File: docs/CLOSETS.md

```
# Closets — The Searchable Index Layer

## What closets are

Drawers hold your verbatim content. Closets are the index — compact pointers that tell the searcher which drawers to open.

```
CLOSET: "built auth system|Ben;Igor|→drawer_api_auth_a1b2c3"
         ↑ topic           ↑ entities  ↑ points to this drawer
```

An agent searching "who built the auth?" hits the closet first (fast scan of short text), then opens the referenced drawer to get the full verbatim content.

## Lifecycle

### When are closets created?

Closets are created during `mempalace mine`. For each file mined:
1. Content is chunked into drawers (verbatim, ~800 chars each)
2. Topics, entities, and quotes are extracted from the content
3. A closet is created with pointer lines to those drawers

### What's inside a closet?

Each line is one atomic topic pointer:
```
topic description|entity1;entity2|→drawer_id_1,drawer_id_2
"verbatim quote from the content"|entity1|→drawer_id_3
```

Topics are never split across closets. If adding a topic would exceed 1,500 characters, a new closet is created.

### When do closets update?

When a file is re-mined (content changed, or `NORMALIZE_VERSION` was bumped), the miner first deletes every closet for that source file (`purge_file_closets`) and then writes a fresh set. Stale topics from the prior mine are gone — closets are always a snapshot of the current content, never an accumulation across runs.

### What about stale topics?

There are no stale topics: each re-mine is a clean rebuild for that source file. If a file gets larger and produces fewer or more closets than last time, the leftover numbered closets from the larger run are still purged because the delete is done by `source_file`, not by ID.

### Do closets survive palace rebuilds?

Closets are stored in the `mempalace_closets` ChromaDB collection alongside `mempalace_drawers`. If you delete and rebuild the palace, closets are recreated during the next `mempalace mine`.

## How search uses closets

```
Query → search mempalace_closets (fast, small documents)
         ↓
    top closet hits → parse `→drawer_id_a,drawer_id_b` pointers
         ↓
    fetch exactly those drawers from mempalace_drawers (verbatim content)
         ↓
    apply max_distance filter
         ↓
    return chunk-level results (same shape as direct search)
```

Hits carry `matched_via: "closet"` (or `"drawer"` for the fallback path) plus a `closet_preview` field showing the line that surfaced them.

If no closets exist (palace created before this feature) — or all closet hits get filtered out by `max_distance` — search falls back to direct drawer search. Closets are created on next mine.

> **BM25 hybrid re-rank** is on the roadmap (deferred to a follow-up PR alongside generic `LLM_*` env-var support); the current closet search ranks purely by ChromaDB cosine distance against the closet text.

## Limits

| Setting | Value | Reason |
|---------|-------|--------|
| Max closet size | 1,500 chars (`CLOSET_CHAR_LIMIT`) | Leaves buffer under ChromaDB's working limit |
| Source content scanned | 5,000 chars (`CLOSET_EXTRACT_WINDOW`) | Caps regex extraction cost on long files; back-of-file content is currently invisible to closet extraction (tracked for follow-up) |
| Max topics per file | 12 | Keeps closets focused |
| Max quotes per file | 3 | Most relevant only |
| Max entities per pointer | 5 | Top names by frequency, after stoplist filtering |

## For developers

Closet functions live in `mempalace/palace.py`:
- `get_closets_collection()` — get the closets ChromaDB collection
- `build_closet_lines()` — extract topics/entities/quotes into pointer lines
- `upsert_closet_lines()` — write lines to closets respecting the char limit (overwrites existing IDs; does not append — call `purge_file_closets` first when re-mining)
- `purge_file_closets()` — delete every closet for a given source file before rebuild
- `CLOSET_CHAR_LIMIT` / `CLOSET_EXTRACT_WINDOW` — size constants

The closet-first search path lives in `mempalace/searcher.py`:
- `_extract_drawer_ids_from_closet()` — parse `→drawer_a,drawer_b` pointers out of a closet document
- `_closet_first_hits()` — query closets, parse pointers, hydrate matching drawers, return chunk-level hits or `None` to fall back

Note: only the project miner (`miner.py::process_file`) builds closets today. Conversation-mined wings (Claude Code JSONL, ChatGPT export, etc.) will keep using direct drawer search via the searcher fallback until the convo-closet PR lands.

```


## File: docs/HISTORY.md

```
# MemPalace — History, Corrections, and Public Notices

This file is the canonical record of post-launch corrections, public notices,
and retractions that affect MemPalace's public claims. Newest first.

---

## 2026-04-14 — Benchmark table rewrite (issue [#875](https://github.com/MemPalace/mempalace/issues/875))

A community audit identified a category error in the public benchmark tables
on `README.md` and `mempalaceofficial.com`: MemPalace's retrieval recall
numbers (R@5, R@10) were listed in the same columns as competitors'
end-to-end QA accuracy numbers. They are different metrics and are not
comparable — a system can have 100% retrieval recall and 40% QA accuracy.

The audit also found that the retracted "+34% palace boost" claim (see the
April 7 note below) was still present in multiple surfaces despite that
retraction, and that two competitor numbers (`Mem0 ~85%`, `Zep ~85%`) had no
published source and did not match the metrics those projects actually
publish.

What changed in this PR:

- The headline number on all surfaces is now **96.6% R@5 on LongMemEval in
  raw mode**, independently reproduced on Linux x86_64 against the tagged
  v3.3.0 release on 2026-04-14. Result JSONLs are committed under
  `benchmarks/results_*.jsonl` (see PR description for the scorecard).
- The **"100% with Haiku rerank"** claim has been removed from all public
  comparison tables. It reproduces on our machines and with a different LLM
  family (minimax-m2.7 via Ollama Cloud: 99.2% R@5 / 100.0% R@10 on the full
  500-question LongMemEval set) — but the 99.4% → 100% step was developed
  by inspecting three specific wrong answers (`benchmarks/BENCHMARKS.md` has
  called this "teaching to the test" since February). It belongs in the
  methodology document, not in a headline.
- The **honest held-out number** for the hybrid pipeline — 98.4% R@5 on 450
  questions that `hybrid_v4` was never tuned on, deterministic seed — is now
  the comparable figure when an LLM rerank is involved.
- The **retracted "+34% palace boost"** has been removed from
  `README.md`, `website/concepts/the-palace.md`,
  `website/guide/searching.md`, and `website/reference/contributing.md`.
  Wing and room filters remain useful — they're standard metadata filters —
  but they are not presented as a novel retrieval improvement.
- **Competitor comparison tables** mixing retrieval recall with QA accuracy
  have been removed from `README.md` and `website/reference/benchmarks.md`.
  Where MemPalace can be fairly compared on the same metric, we link to the
  cited source. Otherwise we report our own numbers and let readers draw
  their own conclusions.
- **Reproduction instructions** in `benchmarks/BENCHMARKS.md` and
  `benchmarks/README.md` were pointing at a defunct branch
  (`aya-thekeeper/mempal`); they now point at `MemPalace/mempalace`.
- The **LoCoMo 100% R@10 with top-50 rerank** row has been removed from
  public comparison surfaces. With per-conversation session counts of 19–32
  and `top_k=50`, the retrieval stage returns every session in the
  conversation by construction, so the number measures an LLM's
  reading comprehension over the whole conversation, not retrieval.

Thanks to [@dial481](https://github.com/MemPalace/mempalace/issues/875) for
the detailed audit and to [@rohitg00](https://github.com/rohitg00) for the
parallel write-up in Discussion #747.

---

## 2026-04-11 — Impostor domains and malware

Several community members (issues #267, #326, #506) reported fake MemPalace
websites distributing malware. The only official surfaces for this project
are:

- This GitHub repository: [github.com/MemPalace/mempalace](https://github.com/MemPalace/mempalace)
- The PyPI package: [pypi.org/project/mempalace](https://pypi.org/project/mempalace/)
- The docs site: [mempalaceofficial.com](https://mempalaceofficial.com)

Any other domain — `mempalace.tech` being the one most commonly reported —
is not ours. Never run install scripts from unofficial sites.

Thanks to our community members for flagging the problem.

---

## 2026-04-07 — A Note from Milla & Ben

> The community caught real problems in this README within hours of launch
> and we want to address them directly.
>
> **What we got wrong:**
>
> - **The AAAK token example was incorrect.** We used a rough heuristic
>   (`len(text)//3`) for token counts instead of an actual tokenizer. Real
>   counts via OpenAI's tokenizer: the English example is 66 tokens, the
>   AAAK example is 73. AAAK does not save tokens at small scales — it's
>   designed for *repeated entities at scale*, and the README example was a
>   bad demonstration of that. We're rewriting it.
>
> - **"30x lossless compression" was overstated.** AAAK is a lossy
>   abbreviation system (entity codes, sentence truncation). Independent
>   benchmarks show AAAK mode scores **84.2% R@5 vs raw mode's 96.6%** on
>   LongMemEval — a 12.4 point regression. The honest framing is: AAAK is
>   an experimental compression layer that trades fidelity for token
>   density, and **the 96.6% headline number is from RAW mode, not AAAK**.
>
> - **"+34% palace boost" was misleading.** That number compares unfiltered
>   search to wing+room metadata filtering. Metadata filtering is a
>   standard feature of the underlying vector store, not a novel retrieval
>   mechanism. Real and useful, but not a moat.
>
> - **"Contradiction detection"** exists as a separate utility
>   (`fact_checker.py`) but is not currently wired into the knowledge graph
>   operations as the README implied.
>
> - **"100% with Haiku rerank"** is real (we have the result files) but
>   the rerank pipeline is not in the public benchmark scripts. We're
>   adding it.
>
> **What's still true and reproducible:**
>
> - **96.6% R@5 on LongMemEval in raw mode**, on 500 questions, zero API
>   calls — independently reproduced on M2 Ultra in under 5 minutes by
>   [@gizmax](https://github.com/MemPalace/mempalace/issues/39).
> - Local, free, no subscription, no cloud, no data leaving your machine.
> - The architecture (wings, rooms, closets, drawers) is real and useful,
>   even if it's not a magical retrieval boost.
>
> **What we're doing:**
>
> 1. Rewriting the AAAK example with real tokenizer counts and a scenario
>    where AAAK actually demonstrates compression
> 2. Adding `mode raw / aaak / rooms` clearly to the benchmark
>    documentation so the trade-offs are visible
> 3. Wiring `fact_checker.py` into the KG ops so the contradiction
>    detection claim becomes true
> 4. Pinning the vector store dependency to a tested range (issue #100),
>    fixing the shell injection in hooks (#110), and addressing the macOS
>    ARM64 segfault (#74)
>
> **Thank you to everyone who poked holes in this.** Brutal honest
> criticism is exactly what makes open source work, and it's what we asked
> for. Special thanks to
> [@panuhorsmalahti](https://github.com/MemPalace/mempalace/issues/43),
> [@lhl](https://github.com/MemPalace/mempalace/issues/27),
> [@gizmax](https://github.com/MemPalace/mempalace/issues/39), and everyone
> who filed an issue or a PR in the first 48 hours. We're listening, we're
> fixing, and we'd rather be right than impressive.
>
> — *Milla Jovovich & Ben Sigman*

```


## File: docs/rfcs/002-source-adapter-plugin-spec.md

```
# RFC 002 — Source Adapter Plugin Specification

- **Status:** Draft
- **Tracking issue:** [#989](https://github.com/MemPalace/mempalace/issues/989)
- **Related:** [#274](https://github.com/MemPalace/mempalace/issues/274), [#23](https://github.com/MemPalace/mempalace/pull/23), [#169](https://github.com/MemPalace/mempalace/pull/169), [#232](https://github.com/MemPalace/mempalace/pull/232), [#567](https://github.com/MemPalace/mempalace/pull/567), [#98](https://github.com/MemPalace/mempalace/pull/98), [#591](https://github.com/MemPalace/mempalace/pull/591), [#592](https://github.com/MemPalace/mempalace/pull/592), [#702](https://github.com/MemPalace/mempalace/pull/702), [#981](https://github.com/MemPalace/mempalace/issues/981), [#244](https://github.com/MemPalace/mempalace/pull/244), [#419](https://github.com/MemPalace/mempalace/pull/419), [#300](https://github.com/MemPalace/mempalace/pull/300), [#952](https://github.com/MemPalace/mempalace/pull/952), [#389](https://github.com/MemPalace/mempalace/pull/389), [#434](https://github.com/MemPalace/mempalace/pull/434)
- **Sibling spec:** [RFC 001 — Storage Backend Plugin Specification](001-storage-backend-plugin-spec.md)
- **Spec version:** `1.0`

## Summary

A formal contract for MemPalace source adapters so third parties can ship `pip install mempalace-source-<name>` packages (Cursor, OpenCode, git, Slack, Notion, email, calendar, Whisper transcripts, …) that drop into `mempalace mine` without patching core. The spec defines the adapter interface, record shape, metadata schema contract, privacy class, entry-point registration, incremental-ingest semantics, closet integration, a declared-transformation model that replaces the informal "verbatim" promise with a verifiable one, conformance tests, and the refactor of the existing file and conversation miners into first-party adapters on the same contract.

RFC 001 formalized the write side (where drawers are stored). This RFC formalizes the read side (where content comes from). Both are required for MemPalace to function as a durable daemon managing heterogeneous palaces across many source types.

## Motivation

Six source ingesters are currently in flight, each solving the same problem a different way:

| PR / Issue | Source | Mechanism |
|---|---|---|
| [#274](https://github.com/MemPalace/mempalace/issues/274) | Cursor | `workspaceStorage/*.vscdb` SQLite extraction |
| [#23](https://github.com/MemPalace/mempalace/pull/23) | OpenCode | SQLite session database |
| [#169](https://github.com/MemPalace/mempalace/pull/169) | Pi agent | JSONL session normalizer |
| [#232](https://github.com/MemPalace/mempalace/pull/232) | Cursor (JSONL variant) | JSONL normalizer |
| [#567](https://github.com/MemPalace/mempalace/pull/567), [#98](https://github.com/MemPalace/mempalace/pull/98) | Git | `git log` + `gh pr view` with structured diff summary |
| [#591](https://github.com/MemPalace/mempalace/pull/591), [#592](https://github.com/MemPalace/mempalace/pull/592) | Delphi Oracle | Real-time intelligence signals |
| [#702](https://github.com/MemPalace/mempalace/pull/702) | Cursor + factory.ai | Combined session miners |

Plus three ingesters already grafted into core:

- `mempalace/miner.py` — filesystem project miner, fixed char-window chunking, keyword hall routing
- `mempalace/convo_miner.py` — chat transcript miner with exchange-pair chunking
- `mempalace/normalize.py` — format detection for four chat-export shapes (Claude Code JSONL, Codex JSONL, Claude.ai / ChatGPT / Slack JSON)

Plus one open proposal for a different ingest semantic:

- [#981](https://github.com/MemPalace/mempalace/issues/981) — path-level descriptions: mine metadata-as-content instead of raw bytes for matched paths. This is a legitimate third ingest mode (alongside chunked-content and whole-record) that the current architecture has no home for.

Each contributor has reinvented source discovery, source-item identity, incremental-ingest bookkeeping, metadata shape, and chunking strategy. Format detection for new chat exports lands in `normalize.py` as one more branch in an `if` chain. There is no shared abstraction, no conformance suite, and no contract new adapter authors can build against.

This is the same situation RFC 001 addresses for storage backends: a pattern that emerged organically, now needs a specification so the community can contribute cleanly and enterprises can build against a stable surface.

### Why this matters beyond developer tooling

The adapter pattern is source-agnostic. What has so far shown up as "Cursor transcripts" and "git commits" generalizes to:

- **Knowledge work** — Notion, Obsidian, Logseq, Google Docs, iA Writer, Zettlr
- **Communications** — Slack, Discord, Teams, Signal backups, mbox/eml email, iMessage
- **Research** — arXiv PDFs, Zotero libraries, bookmarked articles, Kindle highlights, web archives
- **Creator workflows** — YouTube captions, podcast transcripts (Whisper/Deepgram), Descript projects
- **Regulated domains** — medical records, legal filings, financial statements (all gated on §6 privacy class)

Enterprises key on their own domain metadata — `repo/PR/SHA` for engineering, `patient/encounter/CPT` for healthcare, `case/docket/jurisdiction` for legal. The schema lives in the adapter; the content lives in the drawer. This is how structured-data use cases are served without violating the byte-preservation commitments adapters make.

## Goals

1. A source adapter ships as a standalone Python package; `pip install mempalace-source-<name>` is sufficient to use it.
2. `mempalace mine` and the MCP mine tool are source-agnostic — all extraction goes through registered adapters. No `if source_type == 'foo'` branches in core.
3. Content transformations are **declared** (§1.4): each adapter advertises the set of transformations it applies to source bytes. Byte-preserving adapters declare the empty set. Consumers can programmatically determine what happened to their data.
4. Incremental ingest is cheap and correct: re-running mine only touches items whose source-side version changed, using the palace itself as the cursor (no sidecar).
5. Each adapter declares a structured metadata schema. Enterprises index and filter on that schema. Core is schema-agnostic beyond the universal fields in §5.1.
6. The existing `miner.py` and `convo_miner.py` become the first two first-party adapters on the new contract. Drawer metadata fields and field names are preserved — the spec adds fields, does not rename them.
7. A privacy class is declarable at the adapter boundary so sensitive sources (medical, financial, personal comms) are handled with explicit policy rather than implicit trust.

## Non-goals

- Defining chunking. Each adapter owns its chunking strategy — tree-sitter for code, exchange-pair for chat, whole-record for a PR. Core does not impose a chunk size.
- Defining live-stream / webhook shapes (the Delphi Oracle pattern of continuous signal ingestion). That is a separate future RFC; v1 is pull-mode.
- Defining LLM-based structured extraction. Adapters MAY use an LLM; the spec does not mandate or standardize this.
- Defining cross-adapter dedup. When the same content appears via two adapters (e.g., a PR body mined via `git` and as a conversation quote mined via `claude-code`), both drawers land. Deduplication policy is a separate concern handled at query time by `searcher.py`.
- Defining closet construction. Core continues to build closets from adapter-yielded drawers (§1.7); the closet-building algorithm itself is not part of this spec.

---

## 1. Source adapter contract

### 1.1 Required method

All adapters implement `BaseSourceAdapter` with a single kwargs-only ingest method:

```python
class BaseSourceAdapter(ABC):
    @abstractmethod
    def ingest(
        self,
        *,
        source: SourceRef,
        palace: PalaceContext,
    ) -> Iterator[IngestResult]:
        """Enumerate and extract content from a source.

        Yields a stream of IngestResult values. Lazy adapters yield
        `SourceItemMetadata` ahead of the drawers for that item, so core
        can report progress and check `is_current` before the adapter
        commits to the fetch. Adapters with no lazy-fetch benefit may
        interleave `SourceItemMetadata` and `DrawerRecord` items freely.
        """

    @abstractmethod
    def describe_schema(self) -> AdapterSchema:
        """Declare the structured metadata this adapter attaches.

        Returned value is stable for a given adapter version. Enterprises
        index on this schema; core uses it to validate adapter output.
        """
```

The single-method `ingest()` contract was chosen over a `discover` / `extract` split. Most current ingesters have no meaningful laziness benefit (filesystem walking is cheap, transcript normalizing is cheap). Adapters that do (git-mine's `gh pr list` vs `gh pr view`; hypothetical Slack/Notion API) express laziness by yielding `SourceItemMetadata` first and deferring fetch until core confirms staleness via `is_current()`.

### 1.2 Optional methods (default implementations on the ABC)

```python
def is_current(
    self,
    *,
    item: SourceItemMetadata,
    existing_metadata: dict | None,
) -> bool:
    """Return True if the palace already has an up-to-date copy.

    Called by core after querying the palace for existing drawers with
    matching source_file. The adapter compares its version token against
    the stored metadata and returns True to skip extraction.

    Default implementation: returns False (always re-extract). Adapters
    advertising `supports_incremental` override this.
    """
    return False

def source_summary(self, *, source: SourceRef) -> SourceSummary:
    """Describe a source without extracting (e.g., 'git repo mempalace,
    847 commits, 132 PRs'). Default: returns empty summary."""
    return SourceSummary(description=self.name)

def close(self) -> None:
    return None
```

Core's incremental loop (pseudocode):

```python
for result in adapter.ingest(source=source, palace=ctx):
    if isinstance(result, SourceItemMetadata):
        existing = ctx.collection.get(where={"source_file": result.source_file}, limit=1)
        if adapter.is_current(item=result, existing_metadata=existing):
            ctx.skip_current_item()   # adapter stops yielding drawers for this item
    elif isinstance(result, DrawerRecord):
        ctx.upsert_drawer(result)
```

### 1.3 Typed records

```python
@dataclass(frozen=True)
class SourceRef:
    """A handle to the source a user wants to ingest.

    local_path is for filesystem-rooted sources (project dir, mbox file).
    uri is for URL-like references (github.com/org/repo, slack://workspace/channel).
    options carries adapter-specific config (non-secret values only; §M2).
    """
    local_path: str | None = None
    uri: str | None = None
    options: dict = field(default_factory=dict)

@dataclass(frozen=True)
class SourceItemMetadata:
    """Lightweight pointer yielded before drawers for lazy-fetch adapters."""
    source_file: str                 # Logical identity — filesystem path, PR URI, etc.
    version: str                     # Source-side version token (mtime, commit SHA, ETag, rev id).
    size_hint: int | None = None     # Bytes, if known. Used for progress reporting.
    route_hint: RouteHint | None = None

@dataclass(frozen=True)
class DrawerRecord:
    """One drawer's worth of content plus metadata."""
    content: str                     # Subject to §1.4 declared transformations.
    source_file: str                 # Foreign key to SourceItemMetadata.source_file.
    chunk_index: int = 0             # 0 for single-drawer items; 0..N-1 for chunked items.
    metadata: dict = field(default_factory=dict)  # Flat: str/int/float/bool only. Must conform to adapter schema.
    route_hint: RouteHint | None = None

@dataclass(frozen=True)
class RouteHint:
    wing: str | None = None
    room: str | None = None
    hall: str | None = None

@dataclass(frozen=True)
class SourceSummary:
    description: str
    item_count: int | None = None

# IngestResult is the union type adapters yield.
IngestResult = SourceItemMetadata | DrawerRecord

# PalaceContext carries collection handles, palace config, and progress hooks
# into the adapter. Full definition in §9 (cleanup prerequisite).
```

### 1.4 Declared transformations

Adapters cannot silently alter content. Every adapter declares the set of transformations it applies:

```python
class BaseSourceAdapter(ABC):
    declared_transformations: ClassVar[frozenset[str]] = frozenset()
```

The invariant: **no transformation is applied that is not declared in this set**. Adapters declaring `frozenset()` are byte-preserving end-to-end (modulo the read, which may itself involve `utf8_replace_invalid` — see below).

Reserved transformation names (v1):

| Name | Meaning |
|---|---|
| `utf8_replace_invalid` | Undecodable bytes replaced with U+FFFD on read (equivalent to `open(..., errors="replace")`). |
| `newline_normalize` | CRLF / CR converted to LF. |
| `whitespace_trim` | Leading / trailing whitespace stripped at a record boundary. |
| `whitespace_collapse_internal` | Runs of three or more blank lines collapsed to two. |
| `line_trim` | Each line individually stripped of leading / trailing whitespace. |
| `line_join_spaces` | Adjacent lines joined with single spaces, newlines discarded. |
| `blank_line_drop` | Empty lines between non-empty lines dropped. |
| `strip_tool_chrome` | System tags, hook output, tool UI chrome removed (see `normalize.strip_noise`). |
| `tool_result_truncate` | Tool output heads/tails kept; middle replaced with a marker string. |
| `spellcheck_user` | User turns rewritten by spellcheck. |
| `synthesized_marker` | Adapter inserts its own strings (e.g., `[N lines omitted]`, `[registry] …`, Slack provenance footer). |
| `speaker_role_assignment` | Multi-party speakers alternately assigned `user` / `assistant` roles (Slack). |
| `tool_result_omitted` | Some tool outputs fully omitted from transcript (e.g., Read/Edit/Write results in `normalize._format_tool_result`). |

Adapters MAY define their own transformation names for behaviors the reserved list does not cover. Third-party names SHOULD be prefixed with the adapter name to avoid collisions (e.g., `cursor.composer_ordering`).

**Capability derivation:**
- `byte_preserving` — declared_transformations is empty AND output bytes equal input bytes for any source the adapter can read. Advertised via the `byte_preserving` capability (§2.1). MUST be verified by §7.2 round-trip test.
- `declared_lossy` — declared_transformations is non-empty. The adapter's output is reproducible from source by applying *only* the declared transformations. MUST be verified by §7.3 declared-transformation test.

**Existing code mapping (for the cleanup PR):**

| Module | Declared transformations |
|---|---|
| `filesystem` (current `miner.py`) | `utf8_replace_invalid`, `whitespace_trim` |
| `conversations` (current `convo_miner.py` + `normalize.py`) | `utf8_replace_invalid`, `newline_normalize`, `line_trim`, `line_join_spaces`, `blank_line_drop`, `whitespace_collapse_internal`, `strip_tool_chrome`, `tool_result_truncate`, `tool_result_omitted`, `spellcheck_user`, `synthesized_marker`, `speaker_role_assignment` |

The filesystem adapter is nearly byte-preserving today; the conversations adapter is extensively transformed. Both are honest after this spec lands because both are fully declared.

This replaces the MISSION.md promise of "verbatim always" with a stronger one: every adapter publishes what it does to your data, and the conformance suite verifies it hasn't lied. "Verbatim" becomes a capability some adapters hold (byte_preserving), not a global claim about a lossy pipeline.

### 1.5 Three ingest modes

A single adapter declares one or more of three modes via a class attribute:

```python
class BaseSourceAdapter(ABC):
    supported_modes: ClassVar[frozenset[Literal["chunked_content"
```


## File: examples/basic_mining.py

```
#!/usr/bin/env python3
"""Example: mine a project folder into the palace."""

import sys

project_dir = sys.argv[1] if len(sys.argv) > 1 else "~/projects/my_app"
print("Step 1: Initialize rooms from folder structure")
print(f"  mempalace init {project_dir}")
print("\nStep 2: Mine everything")
print(f"  mempalace mine {project_dir}")
print("\nStep 3: Search")
print("  mempalace search 'why did we choose this approach'")

```


## File: examples/convo_import.py

```
#!/usr/bin/env python3
"""Example: import Claude Code / ChatGPT conversations."""

print("Import Claude Code sessions:")
print("  mempalace mine ~/claude-sessions/ --mode convos --wing my_project")
print()
print("Import ChatGPT exports:")
print("  mempalace mine ~/chatgpt-exports/ --mode convos")
print()
print("Use general extractor for richer extraction:")
print("  mempalace mine ~/chats/ --mode convos --extract general")

```


## File: examples/gemini_cli_setup.md

```
# Gemini CLI Integration Guide

This guide explains how to set up MemPalace as a permanent memory for the [Gemini CLI](https://github.com/google/gemini-cli).

## Prerequisites

- Python 3.9+
- Gemini CLI installed and configured

## 1. Installation

On many Linux systems, installing Python packages globally is restricted. We recommend using a local virtual environment within the MemPalace directory.

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/MemPalace/mempalace.git
cd mempalace

# Create a virtual environment
python3 -m venv .venv

# Install dependencies and MemPalace in editable mode
.venv/bin/pip install -e .
```

## 2. Initialization

Set up your "Palace" (the database) and configure your identity.

```bash
# Initialize the palace in the current directory
.venv/bin/python3 -m mempalace init .
```

### Identity and Wings (Optional but Recommended)
You can manually define who you are and what projects you work on by creating/editing these files in `~/.mempalace/`:

- **`~/.mempalace/identity.txt`**: A plain text file describing your role and focus.
- **`~/.mempalace/wing_config.json`**: A JSON file mapping projects and name variants to "Wings".

## 3. Connect to Gemini CLI (MCP)

Register MemPalace as an MCP server so Gemini CLI can use its tools.

```bash
gemini mcp add mempalace /absolute/path/to/mempalace/.venv/bin/python3 -m mempalace.mcp_server --scope user
```
*Note: Use the absolute path to ensure it works from any directory.*

## 4. Enable Auto-Saving (Hooks)

To ensure the AI saves memories automatically when conversation history becomes too long, add a `PreCompress` hook to your Gemini CLI settings.

Edit your `~/.gemini/settings.json` and add the following:

```json
{
  "hooks": {
    "PreCompress": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/to/mempalace/hooks/mempal_precompact_hook.sh"
          }
        ]
      }
    ]
  }
}
```

Make sure the hook scripts are executable:
```bash
chmod +x hooks/*.sh
```

## 5. Usage

Once connected, Gemini CLI will automatically:
- Start the MemPalace server on launch.
- Use `mempalace_search` to find relevant past discussions.
- Use the `PreCompress` hook to save new memories before they are lost.

### Manual Mining
If you want the AI to learn from your existing code or docs immediately, run the "mine" command:
```bash
.venv/bin/python3 -m mempalace mine /path/to/your/project
```

### Verification
In a Gemini CLI session, you can run:
- `/mcp list`: Verify `mempalace` is `CONNECTED`.
- `/hooks panel`: Verify the `PreCompress` hook is active.

```


## File: examples/HOOKS_TUTORIAL.md

```
# How to Use MemPalace Hooks (Auto-Save)

MemPalace hooks act as an "Auto-Save" feature. They help your AI keep a permanent memory without you needing to run manual commands.

### 1. What are these hooks?
* **Save Hook** (`mempal_save_hook.sh`): Saves new facts and decisions every 15 messages.
* **PreCompact Hook** (`mempal_precompact_hook.sh`): Saves your context right before the AI's memory window fills up.

### 2. Setup for Claude Code
Add this to your configuration file to enable automatic background saving:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "", 
        "hooks": [{"type": "command", "command": "./hooks/mempal_save_hook.sh"}]
      }
    ],
    "PreCompact": [
      {
        "matcher": "", 
        "hooks": [{"type": "command", "command": "./hooks/mempal_precompact_hook.sh"}]
      }
    ]
  }
}
```

### 3. What changed (v3.1.0+)

Both hooks now have **two-layer capture**:

1. **Auto-mine**: Before blocking the AI, the hook runs the normalizer on the JSONL transcript and upserts chunks directly into the palace. This captures raw tool output (Bash results, search findings, build errors) that the AI would otherwise summarize away.

2. **Updated reason messages**: The block reason now explicitly tells the AI to save tool output verbatim — not just topics and decisions.

### 4. Backfill past conversations (one-time)

The hooks capture conversations going forward, but you probably have months of past sessions. Run this once to mine them all:

```bash
mempalace mine ~/.claude/projects/ --mode convos
```

### 5. Configuration

- **`SAVE_INTERVAL=15`** — How many human messages between saves
- **`MEMPALACE_PYTHON`** — Python interpreter with mempalace + chromadb. Auto-detects: env var → repo venv → system python3
- **`MEMPAL_DIR`** — Optional directory for auto-ingest via `mempalace mine`
```


## File: examples/mcp_setup.md

```
# MCP Integration — Claude Code

## Setup

Run the MCP server:

```bash
mempalace-mcp
```

Or add it to Claude Code:

```bash
claude mcp add mempalace -- mempalace-mcp
```

## Available Tools

The server exposes the full MemPalace MCP toolset. Common entry points include:

- **mempalace_status** — palace stats (wings, rooms, drawer counts)
- **mempalace_search** — semantic search across all memories
- **mempalace_list_wings** — list all projects in the palace

## Usage in Claude Code

Once configured, Claude Code can search your memories directly during conversations.

```


## File: .pre-commit-config.yaml

```
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    # Keep in lock-step with the ruff version pinned in .github/workflows/ci.yml
    # (>=0.4.0,<0.5). Using a newer rev here produces a different formatter
    # output than CI and breaks `ruff format --check` in the lint job.
    rev: v0.4.10
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

```


## File: AGENTS.md

```
# CLAUDE.md

## The Mission

Memory is identity. When an AI forgets everything between conversations, it cannot build real understanding — of you, your work, your people, your life.

MemPalace exists to solve this. It is a memory system — not a search engine, not a RAG pipeline, not a vector database wrapper. It treats every word you have shared as sacred, stores it verbatim, and makes it instantly available. Your data never leaves your machine. We never summarize. We never paraphrase. We return your exact words.

100% recall is the design requirement — the target every search path is measured against. Anything less means forgetting, and forgetting means starting over.

The name comes from the ancient "method of loci" — the memory palace technique used for thousands of years to organize and recall vast amounts of information by placing it in imagined rooms of an imagined building. We were also inspired by the Zettelkasten method (created by German sociologist Niklas Luhmann) — small cross-referenced index cards that point to each other. We apply both ideas to AI memory:

- **Wings** for broad categories (people, projects, topics)
- **Rooms** for time-based groupings (days, sessions)
- **Drawers** for full verbatim content (your exact words)
- **AAAK compression** for the index layer — a compact symbolic format (via `dialect.py`) that lets an LLM scan thousands of entries instantly and know exactly which drawer to open

## Design Principles

These are non-negotiable. Every PR, every feature, every refactor must honor them.

- **Verbatim always** — Never summarize, paraphrase, or lossy-compress user data. The system searches the index and returns the original words. If a user said it, we store exactly what they said. This is the foundational promise.
- **Incremental only** — Append-only ingest after initial build. Never destroy existing data to rebuild. A crash mid-operation must leave the existing palace untouched.
- **Entity-first** — Everything is keyed by real names with disambiguation by DOB, ID, or context. People matter more than topics.
- **Local-first, zero API** — All extraction, chunking, and embedding happens on the user's machine. No cloud dependency for memory operations. No API keys required.
- **Performance budgets** — Hooks under 500ms. Startup injection under 100ms. Memory should feel instant.
- **Privacy by architecture** — The system physically cannot send your data because it never leaves your machine. No telemetry, no phone-home, no external service dependencies for core operations.
- **Background everything** — Filing, indexing, timestamps, and pipeline work happen via hooks in the background. Nothing interrupts the user's conversation. Zero tokens spent on bookkeeping in the chat window.

## Contributing

We welcome bug fixes, performance improvements, new language support, better entity disambiguation, documentation, and test coverage.

We do not accept summarization of user content, cloud storage/sync features, telemetry or analytics, features requiring API keys for core memory, or shortcuts that bypass verbatim storage.

## Setup

```bash
pip install -e ".[dev]"
```

## Commands

```bash
# Run tests
python -m pytest tests/ -v --ignore=tests/benchmarks

# Run tests with coverage
python -m pytest tests/ -v --ignore=tests/benchmarks --cov=mempalace --cov-report=term-missing

# Lint
ruff check .

# Format
ruff format .

# Format check (CI mode)
ruff format --check .
```

## Project Structure

```
mempalace/
├── mcp_server.py        # MCP server — all read/write tools
├── cli.py               # CLI dispatcher
├── config.py            # Configuration + input validation
├── miner.py             # Project file miner
├── convo_miner.py       # Conversation transcript miner
├── searcher.py          # Semantic search (hybrid BM25 + vector)
├── knowledge_graph.py   # Temporal entity-relationship graph (SQLite)
├── palace.py            # Shared palace operations
├── palace_graph.py      # Room traversal + cross-wing tunnels
├── backends/            # Pluggable storage backends (ChromaDB default)
│   ├── base.py          # Abstract interface — implement this for new backends
│   └── chroma.py        # ChromaDB implementation
├── dialect.py           # AAAK compression dialect
├── normalize.py         # Transcript format detection + normalization
├── entity_detector.py   # Auto-detect people/projects from content
├── entity_registry.py   # Entity storage and disambiguation
├── layers.py            # L0-L3 memory wake-up stack
├── onboarding.py        # Interactive first-run setup
├── repair.py            # Palace repair and consistency checks
├── dedup.py             # Deduplication
├── migrate.py           # ChromaDB version migration
├── spellcheck.py        # Auto-correct user messages
├── exporter.py          # Palace data export
├── hooks_cli.py         # Hook management CLI
├── query_sanitizer.py   # Prompt contamination prevention
├── split_mega_files.py  # Split concatenated transcript files
└── version.py           # Single source of truth for version

hooks/                   # Claude Code hook scripts
├── mempal_save_hook.sh        # Stop: triggers diary save
└── mempal_precompact_hook.sh  # PreCompact: saves state before compression
```

## Conventions

- **Python style**: snake_case for functions/variables, PascalCase for classes
- **Linter**: ruff with E/F/W rules
- **Formatter**: ruff format, double quotes
- **Commits**: conventional commits (`fix:`, `feat:`, `test:`, `docs:`, `ci:`)
- **Tests**: `tests/test_*.py`, fixtures in `tests/conftest.py`
- **Coverage**: 85% threshold (80% on Windows due to ChromaDB file lock cleanup)

## Architecture

```
User → CLI / MCP Server → Storage Backend (ChromaDB default, pluggable)
                        → SQLite (knowledge graph)

Palace structure:
  WING (person/project)
    └── ROOM (day/topic)
          └── DRAWER (verbatim text chunk)

Index layer (AAAK):
  Compressed pointers → DRAWER locations
  Scanned by LLM to find relevant drawers without reading all content

Knowledge Graph:
  ENTITY → PREDICATE → ENTITY (with valid_from / valid_to dates)
```

## Key Files for Common Tasks

- **Adding an MCP tool**: `mempalace/mcp_server.py` — add handler function + TOOLS dict entry
- **Changing search**: `mempalace/searcher.py`
- **Modifying mining**: `mempalace/miner.py` (project files) or `mempalace/convo_miner.py` (transcripts)
- **Adding a storage backend**: subclass `mempalace/backends/base.py`, register in `backends/__init__.py`
- **Input validation**: `mempalace/config.py` — `sanitize_name()` / `sanitize_content()`
- **Tests**: mirror source structure in `tests/test_<module>.py`

```


## File: CHANGELOG.md

```
# Changelog

All notable changes to [MemPalace](https://github.com/MemPalace/mempalace) are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased] — v3.3.0 (on develop)

### New Features
- Closet layer — a compact searchable index of pointers to verbatim drawers, enabling fast topical lookup without reading all content (#788)
- BM25 hybrid search — closets boost ranking, drawers remain the source of truth (#795, #829)
- Entity metadata on every drawer for filterable search (#829)
- Diary ingest — day-based rooms for conversation transcripts (#829)
- Cross-wing tunnels — explicit links between rooms in different wings for multi-project agents (#829)
- Drawer-grep — returns the best-matching chunk plus adjacent context drawers (#829)
- Offline fact checker against the entity registry and knowledge graph (#829)
- LLM-based closet regeneration — optional, bring-your-own endpoint, no mandatory API key (#793)
- Hall detection — routes drawer content to `emotions` / `technical` / `family` / `memory` / `identity` / `consciousness` / `creative` halls, enabling hall-based graph connectivity within wings (#835)

### Bug Fixes
- Set `hnsw:space=cosine` metadata on all collection creation sites — fixes broken similarity scoring under ChromaDB's default L2 distance (#807, #218)
- File-level locking prevents duplicate drawers when agents mine the same file concurrently (#784, #826)
- Hybrid closet+drawer retrieval — closets boost ranking, never gate results (#795)
- Stop hooks from making agents write in chat — saves tokens on every turn (#786)
- Strip system tags, hook output, and Claude UI chrome from drawers before filing (#785)
- Verbatim-safe `strip_noise` scoped to Claude Code JSONL only (#785)
- Prevent diary entry ID collisions via microsecond timestamp and full content hash (#819)
- Auto-rebuild stale drawers via `NORMALIZE_VERSION` schema gate
- Enforce atomic topics in closets and extract richer pointers
- Sync `version.py` to match `pyproject.toml` (#820)
- Remove unused `main` import from `mempalace/__init__.py` (#827)
- README audit — fix 7 stale claims (tool count, version badge, wake-up token cost, `dialect.py` lossless disclaimer, `pyproject.toml` version) with 42 regression-guard tests (#835)

### Improvements
- Optimize entity detection with regex caching and pre-compilation (#828)
- Extract locked filing block into helper to keep `mine_convos` under C901 complexity

### Documentation
- Add `docs/CLOSETS.md` — closet layer overview
- Fix stale `milla-jovovich/*` org URLs in website and plugin manifests (#787)
- Fix remaining stale org URLs in contributor docs (#808)
- Rewrite `README.md` and `mempalaceofficial.com` benchmark pages to remove category-error cross-system comparisons (R@5 retrieval recall had been listed next to competitor QA accuracy under one column), remove the retracted "+34% palace boost" claim from the surfaces where it had remained, replace the `100%` Haiku-rerank headline with the honest held-out `98.4%` R@5, drop the LoCoMo `100%` top-50 row (retrieval-bypass artefact), and fix the broken `aya-thekeeper/mempal` reproduction URL (#875)
- Add `docs/HISTORY.md` as the canonical home for corrections, retractions, and public notices; move the 2026-04-07 "Note from Milla & Ben" and the 2026-04-11 impostor-domain notice out of `README.md`
- Add v3.3.0 reproduction result JSONLs and the deterministic `seed=42` 50/450 LongMemEval split under `benchmarks/` — every BENCHMARKS.md claim reproduces exactly

### Internal
- Add test coverage for `mine_lock`, closets, entity metadata, BM25, and diary
- Verify `mine_lock` via disjoint critical-section intervals
- Serialize `mine_lock` concurrency test with multiprocessing
- Make diary state path assertion platform-neutral
- Add `TestTunnels` coverage for cross-wing tunnel operations
- Ruff format with CI-pinned version (0.4.x); format `mempalace/palace.py`

---

## [3.2.0] — 2026-04-12

### Packaging
- Remove `chromadb<0.7` upper bound — unblocks installs against chromadb 1.x palaces (#690)
- Bump version to 3.2.0 across `pyproject.toml`, `mempalace/version.py`, README badge, and OpenClaw SKILL (#761)

### Security
- Harden palace deletion, WAL redaction, and MCP search input handling (#739)
- Consistent input validation, argument whitelisting, concurrency safety, and WAL fixes (#647)
- Remove hardcoded credential paths from benchmark runners (#177)
- Remove global SSL verification bypass in convomem_bench (#176)

### Bug Fixes
- Parse Claude.ai privacy export with `messages` key and sender field (#685, #677)
- Detect mtime changes in `_get_client` to prevent stale HNSW index (#757)
- Hash full content in `tool_add_drawer` drawer ID — stable re-mines (#716)
- Remove 10k drawer cap from status display (#707, #603)
- Correct typo in entity_detector interactive classification prompt (#755)
- Prevent convo_miner from re-processing 0-chunk files on every run (#732, #654)
- Remove silent 8-line AI response truncation in convo_miner (#708, #692)
- Store full AI response in convo_miner exchange chunking (#695)
- Fix `mine --dry-run` TypeError on files with room=None (#687, #586)
- Skip arg whitelist for handlers accepting `**kwargs` (#684, #572)
- Allow Unicode in `sanitize_name()` — Latvian, CJK, Cyrillic (#683, #637)
- Auto-repair BLOB seq_ids from chromadb 0.6→1.5 migration (#664)
- Remove no-op `ORT_DISABLE_COREML` env var (#653, #397)
- Disambiguate hook block reasons to name MemPalace explicitly (#666)
- Use epsilon comparison for mtime to prevent unnecessary re-mining (#610)
- Correct token count estimate in compress summary (#609)
- Implement MCP ping health checks (#600)
- Align `cmd_compress` dict keys with `compression_stats()` return values (#569)
- Skip unreachable reparse points in `detect_rooms_from_folders` on Windows (#558)
- Prevent HNSW index bloat from duplicate `add()` calls (#544, #525)
- Purge stale drawers before re-mine to avoid hnswlib segfault (#544)
- Mitigate system prompt contamination in search queries (#385, #333)
- Count Codex `user_message` turns in `_count_human_messages` (#373, #347)
- Paginate large collection reads and surface errors in MCP tools (#371, #339, #338)
- Expand `~` in split command directory argument (#361)
- Ignore `wait_for_previous` argument to support Gemini MCP clients (#322)
- Close KnowledgeGraph SQLite connections in test fixtures (#450)
- Remove duplicate cache variable declarations in mcp_server.py (#449)
- Add `--yes` flag to init instructions for non-interactive use (#682, #534)
- Add `mcp` command with setup guidance (#315)

### New Features
- i18n support — 8 languages (en, es, fr, de, ja, ko, zh-CN, zh-TW) (#718)
- New MCP tools: get/list/update drawer, hook settings, export (#667, #635)
- `mempalace migrate` — recover palaces from different ChromaDB versions (#502)
- Add OpenClaw/ClawHub skill (#491)
- Backend seam for pluggable storage backends (#413)

### Improvements
- Disable broken auto-bump workflow (#414)
- Improve agent readiness — AGENTS.md, dependabot, CODEOWNERS, labels (#497)

### Documentation
- Add CLAUDE.md and mission/principles to AGENTS.md (#720)
- Add VitePress documentation site (#439)
- Add warning about fake MemPalace websites (#598)
- Fix stale org URLs and PR branch target in contributor docs (#679)
- Fix misaligned architecture diagram (#734, #733)
- Add ROADMAP.md — v3.1.1 stability patch and v4.0.0-alpha plan

### Internal
- ruff format convo_miner.py (#741)
- ruff format all Python files (#675)
- CI: trigger tests on develop branch PRs and pushes (#674)
- CI: fix GitHub Pages publishing (#691)

---

## [3.1.0] — 2026-04-09

### Security
- Harden inputs, fix shell injection, optimize DB access (#387)
- Sanitize SESSION_ID in save hook to prevent path traversal (#141)
- Sanitize error responses and remove `sys.exit` from library code (#139)
- Shell injection fix in hooks, Claude Code mining, chromadb pin (#114)

### Bug Fixes
- MCP null args hang, repair infinite recursion, OOM on large files (#399)
- Release ChromaDB handles before rmtree on Windows (#392)
- Use `os.utime` in mtime test for Windows compatibility (#392)
- Negotiate MCP protocol version instead of hardcoding (#324)
- Use upsert and deterministic IDs to prevent data stagnation (#140)
- Make `drawer_id` deterministic for idempotent writes (#387)
- Honest AAAK stats — word-based token estimator, lossy labels (#147)
- Room detection checks keywords against folder paths (#145)
- Use actual detected room in mine summary stats (#165)
- Honour `--palace` flag in mcp_server (#264)
- Preserve default KG path when `--palace` not passed (#270)
- `--yes` flag skips all interactive prompts in init (#123)
- Repair command, split args, Claude export, room keywords (#119)
- Replace Unicode separator in convo_miner.py for Windows compatibility (#129)
- Coerce MCP integer arguments to native Python int (#84)
- Batch ChromaDB reads to avoid SQLite variable limit (#66)
- Respect nested .gitignore rules during mining (#78)
- Narrow bare `except Exception` to specific types where safe (#54)
- Mark MD5 as non-security in miner drawer ID generation (#53)
- Remove dead code and duplicate set items in entity_registry.py (#42)
- Silence ChromaDB telemetry warnings and CoreML segfault on Apple Silicon (#236)
- Unify package and MCP version reporting (#16)
- Fix broken AAAK Dialect link in README (#238)
- Update input prompt for entity confirmation (#83)
- Preserve CLI exit codes, log tracebacks, sanitize search errors (#139)
- Enable SQLite WAL mode and add consistent LIMIT to KG timeline (#136)
- Add limit=10000 safety cap to all unbounded ChromaDB `.get()` calls (#137)
- Re-mine modified files, idempotent `add_drawer`, cleanup ChromaDB handles (#140)
- Resolve formatting, regression logic, and pytest defaults (#270)
- Use `parse_known_args` to allow importing mcp_server during pytest (#270)

### New Features
- Package MemPalace as standard Claude and Codex plugins (#270)
- Add OpenAI Codex CLI JSONL normalizer (#61)
- Add Codex plugin support with hooks, commands, and documentation (#270)
- Add command documentation for help, init, mine, search, and status (#270)

### Improvements
- Cache ChromaDB `PersistentClient` instead of re-instantiating per call (#135)
- Tighten chromadb version range and add `py.typed` marker (#142)
- Consolidate split known-names config loading (#22)
- CI: add separate jobs for Windows and macOS testing
- CI: Upgrade GitHub Actions for Node 24 compatibility (#55)

### Documentation
- Add Gemini CLI setup guide and integration section (#106)
- Add beginner-friendly hooks tutorial (#103)
- Align MCP setup examples with shipped server (#21)
- Honest README update — own the mistakes, fix the claims

### Internal
- Expand test coverage from 20 to 92 tests, migrate to uv (#131)
- Add scale benchmark suite — 106 tests (#223)
- Increase test coverage from 30% to 85%, fix Windows encoding bugs (#281)
- Add WAL mode and entity timeline limit assertions
- Add coverage for `file_already_mined` mtime check

---

## [3.0.0] — 2026-04-06

Initial public release.

- Palace architecture with day-based rooms, drawers (verbatim), and closets (searchable index)
- AAAK compression dialect for memory folding
- Knowledge graph with entity detection and timeline queries
- MCP server for Claude, Codex, and Gemini integration
- CLI: `init`, `mine`, `search`, `status`, `compress`, `repair`, `split`
- Benchmark suite with recall and scale tests
- README with MCP flow, local model flow, and specialist agent documentation

---

[Unreleased]: https://github.com/MemPalace/mempalace/compare/v3.2.0...HEAD
[3.2.0]: https://github.com/MemPalace/mempalace/compare/v3.1.0...v3.2.0
[3.1.0]: https://github.com/MemPalace/mempalace/compare/v3.0.0...v3.1.0
[3.0.0]: https://github.com/MemPalace/mempalace/releases/tag/v3.0.0

```


(… 204 more files omitted due to size limit)
<!-- fetched-content:end -->
