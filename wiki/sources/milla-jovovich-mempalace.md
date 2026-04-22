---
title: milla-jovovich/mempalace
type: source
created: '2026-04-21'
last_verified: '2026-04-22'
source_hash: 4115e693a8792354734b4787ecc07e7c46fda61b3c6c67260af0d7efcc0f9df0
sources:
- raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md
source_url: https://github.com/milla-jovovich/mempalace
tags:
- ai
- chromadb
- github
- llm
- mcp
- memory
- python
tier: warm
knowledge_state: ingested
ingest_method: manual-deepen-github-2026-04-22
quality_score: 90
concepts:
- mempalace-memory-system
- palace-memory-architecture
- hybrid-retrieval-agent-memory-systems
- agent-memory-frameworks
- aaak-compression-dialect
- closet-index-layer
- wing-room-drawer-topology
- hybrid-v4-retrieval
- mempalace-mcp-tool-inventory
---

# milla-jovovich/mempalace

## What it is

MemPalace is a local-first AI memory system that stores conversation history as verbatim text and retrieves it with semantic search — no summarization, no extraction, no paraphrasing. Content is filed into a structured index of *wings* (people, projects), *rooms* (topics), and *drawers* (the original verbatim text), so retrieval can be scoped instead of running flat over the whole corpus. The retrieval backend is pluggable; ChromaDB is the default. Nothing leaves your machine unless you opt in.

## Why it matters

This is the memory layer we already use across every agent in this workspace — Copilot CLI, OpenCode, the labs-wiki MCP, and per-project session diaries all file into MemPalace. It's the only open-source memory project that publishes a 96.6% R@5 raw score on LongMemEval without an LLM in the retrieval path, which is what makes it credible as the substrate for cross-session continuity rather than a toy demo.

## Architecture / Technical model

**Wings** — Top-level partitions for people/projects (e.g., `homelab`, `nba_ml_engine`, `copilot_sessions`). Queries can be scoped to a wing to avoid cross-project contamination.
> See [[wing-room-drawer-topology]] for the full treatment.

**Rooms** — Topic/time-based groupings within a wing (e.g., `backend`, `decisions`, day-based for conversations). Auto-detected from folder structure (70+ patterns in `room_detector_local.py`) or conversation content. Max 5,000 characters scanned per file for room classification.

**Halls** — Semantic corridors connecting related rooms within a wing (`hall_facts`, `hall_events`, `hall_discoveries`, `hall_preferences`, `hall_advice`, `emotions`, `technical`, `family`, `memory`, `identity`, `consciousness`, `creative`). Used for graph-based navigation via `palace_graph.py`.

**Closets** — Compact index layer storing topic pointers → drawer IDs. Each closet line: `topic|entity1;entity2|→drawer_id_1,drawer_id_2`. Capped at 1,500 chars; max 12 topics, 3 quotes, 5 entities per file. Search hits closets first (fast), then hydrates verbatim drawers. Direct drawer fallback if closets miss.
> See [[closet-index-layer]] for the full treatment.

**Drawers** — Verbatim content chunks (~800 chars for project files, exchange-pair for conversations). Never summarized. Identified by MD5(content + source_file + chunk_index). Stored in ChromaDB `mempalace_drawers` collection with `hnsw:space=cosine` distance.

**Tunnels** — Explicit cross-wing links for rooms that appear in multiple projects. BFS traversal via `palace_graph.py::traverse()` follows tunnels to retrieve related context across wings.

**Knowledge graph** — Temporal entity-relationship triples in SQLite with `valid_from` / `valid_to` dates. `KnowledgeGraph::add()` / `query_relationship()` / `invalidate()` / `timeline()`. WAL mode enabled. Thread-safe locks on close, query, timeline, stats.

**Hybrid v4 retrieval** — Layers keyword (BM25-like), temporal-proximity, and preference-pattern extraction on top of raw semantic search. Held-out 98.4% R@5 on 450 unseen LongMemEval questions (tuned on 50 dev, deterministic seed=42).
> See [[hybrid-v4-retrieval]] for the full treatment.

**MCP server** — 29 tools via `mempalace.mcp_server:main` entry point (accessible as `mempalace-mcp`). Grouped: palace ops (status, search, add_drawer, get_drawer, list_drawers, update_drawer, delete_drawer), KG ops (kg_add, kg_query, kg_invalidate, kg_timeline, kg_stats), navigation (traverse, find_tunnels, graph_stats), drawer mgmt (check_duplicate), diaries (diary_write, diary_read, list_agents).
> See [[mempalace-mcp-tool-inventory]] for the full treatment.

**AAAK compression** — 30x lossless entity-code shorthand for repeated names at scale. `dialect.py`. **WARNING: AAAK mode scores 84.2% R@5 vs raw mode's 96.6%** — it is a lossy abbreviation system (entity codes, sentence truncation). The 96.6% headline figure is from RAW mode, not AAAK.
> See [[aaak-compression-dialect]] for the full treatment.

**Pluggable backends** — `BaseBackend` interface in `backends/base.py`. ChromaDB is default (`backends/chroma.py`). Entry-point group `mempalace.backends` for third-party stores. RFC 001 formalizes the storage contract.

## How it works

1. **Mining** — `mempalace mine <path>` walks directories (respecting .gitignore), reads files with `utf8_replace_invalid` error handling, chunks by paragraph (~800 char target for code, exchange-pair for conversations). For each file: check mtime against palace metadata → skip if unchanged (epsilon comparison to avoid float drift) → chunk → extract topics/entities/quotes → build closet lines (max 1,500 chars per closet, max 12 topics/3 quotes/5 entities per file, first 5,000 chars scanned) → upsert closets → upsert drawers. File-level lock (`mine_lock`) prevents concurrent writes to same file.

2. **Embedding** — Local sentence-transformer model (~300 MB, no API key). Embeddings computed during mine and indexed in ChromaDB with `hnsw:space=cosine` distance (critical — L2 default breaks similarity scoring). Collections: `mempalace_closets` and `mempalace_drawers`.

3. **Search (closet-first hybrid)** — Query → semantic search on closets (small docs, fast) → parse `→drawer_id_a,drawer_id_b` pointers → fetch those exact drawers from `mempalace_drawers` → apply `max_distance` filter → return chunk-level results with `matched_via: "closet"` + `closet_preview`. If no closets exist or all filtered out → fall back to direct drawer search (`matched_via: "drawer"`). Results carry wing/room/hall metadata for scoped retrieval.

4. **Hybrid v4 pipeline** (opt-in) — On top of semantic search: (a) keyword boosting (BM25-like term frequency), (b) temporal-proximity boosting (recent drawers favored), (c) preference-pattern extraction (user likes/dislikes mined from past exchanges). Held-out 98.4% R@5 on 450 LongMemEval questions unseen during dev (tuned on 50-question dev split, seed=42). No LLM in retrieval path.

5. **Optional LLM rerank** — Top-20 semantic candidates → LLM reader promotes best match → ≥99% R@5. Works with Claude Haiku, Claude Sonnet, minimax-m2.7 via Ollama Cloud (no Anthropic dependency). The 99.4% → 100% step inspected specific wrong answers (flagged as "teaching to the test" in `benchmarks/BENCHMARKS.md`), so 98.4% is the honest generalizable figure.

6. **Knowledge graph queries** — Separate from semantic search. `KnowledgeGraph::query_relationship(entity, as_of=date)` → temporal entity-relationship triples valid at that date. `timeline(entity)` → chronological fact sequence. `invalidate(subject, predicate, object, ended=date)` → mark fact as no longer true. Backed by SQLite with WAL mode, thread-safe locks.

7. **MCP tool dispatch** — Agent calls e.g. `mempalace_search(query="database decision", wing="homelab")` → Python MCP server → closet-first search → JSON result with drawer content + metadata. 29 tools total. Auto-teach AAAK spec on first `mempalace_status` call. Palace Protocol handshake via `mempalace_get_aaak_spec`.

8. **Benchmarks** — Fully reproducible from repo. `python benchmarks/longmemeval_bench.py <data.json>` → 96.6% R@5 raw mode, 5 min on Apple Silicon, zero API calls. `--mode aaak` → 84.2%. `--mode rooms` → 89.4%. LoCoMo: 60.3% R@10 session-granularity, 88.9% with hybrid v5. ConvoMem: 92.9% avg recall across 6 categories (50 items each). MemBench (ACL 2025): 80.3% R@5 on 8,500 items.

9. **Auto-save hooks** — `hooks/mempal_save_hook.sh` (Stop event, every 15 messages) + `hooks/mempal_precompact_hook.sh` (PreCompact, before context window fills). Both auto-mine transcript → palace (tool output captured), then block AI with reason message to save topics/decisions/quotes. `stop_hook_active` flag prevents infinite loops. `MEMPAL_DIR` env var triggers auto-run of `mempalace mine <dir>` on each save. Hooks resolve repo root automatically; use `MEMPAL_PYTHON` override for venv python path (hooks need `python3` on PATH for internal JSON parsing).

## API / interface surface

**CLI commands** (via `mempalace` entry point):
- `init <path>` — Initialize palace in directory, guided onboarding for identity/wings/AAAK bootstrap
- `mine <path> [--mode {files|convos}] [--wing NAME] [--dry-run]` — Ingest content. Modes: `files` (project code/docs), `convos` (Claude Code/ChatGPT/Codex JSONL, Claude.ai/Slack JSON).
- `search QUERY [--wing WING] [--room ROOM] [--top-k N]` — Semantic search with optional scoping
- `status` — Palace overview (wings, rooms, drawer counts, ChromaDB health, KG stats)
- `compress` — AAAK-encode palace for token-efficient context injection
- `wake-up` — L0-L3 memory stack injection (identity, critical facts, room recall, deep search)
- `repair` — Consistency checks + HNSW index quarantine after crashes
- `migrate` — Recover palaces from different ChromaDB versions
- `split <file>` — Split concatenated transcript into per-session files
- `mcp` — Launch MCP server (or use `mempalace-mcp` entry point directly)

**MCP tools** (29 total, accessible when MCP server running):
| Tool | Purpose |
|---|---|
| `mempalace_status` | Wing/room/drawer counts, ChromaDB health, auto-teaches AAAK spec |
| `mempalace_search` | Closet-first semantic search, wing/room scoping |
| `mempalace_add_drawer`, `get_drawer`, `list_drawers`, `update_drawer`, `delete_drawer` | Drawer CRUD |
| `mempalace_kg_add`, `kg_query`, `kg_invalidate`, `kg_timeline`, `kg_stats` | Knowledge graph ops |
| `mempalace_traverse`, `find_tunnels`, `graph_stats` | Palace graph navigation |
| `mempalace_check_duplicate` | Pre-filing duplicate check (threshold 0.0–1.0) |
| `mempalace_diary_write`, `diary_read`, `list_agents` | Per-agent diary (AAAK format) |
| `mempalace_get_aaak_spec` | Return AAAK dialect reference for agent self-teaching |
| `mempalace_list_wings`, `list_rooms`, `get_taxonomy` | Palace structure introspection |

**Python API** (importable modules):
- `from mempalace.cli import main` — CLI entry point
- `from mempalace.mcp_server import main` — MCP server
- `from mempalace.searcher import search` — Programmatic search
- `from mempalace.knowledge_graph import KnowledgeGraph` — Direct KG access
- `from mempalace.dialect import aaak_encode, aaak_decode` — AAAK compression
- `from mempalace.palace import get_closets_collection, build_closet_lines, upsert_closet_lines` — Closet ops
- `from mempalace.backends.base import BaseBackend` — For custom storage backends

## Setup

```bash
pip install mempalace
mempalace init ~/projects/myapp

# Mine content into the palace
mempalace mine ~/projects/myapp                    # project files
mempalace mine ~/.claude/projects/ --mode convos   # Claude Code sessions
mempalace mine ~/.codex/sessions/ --mode convos    # Codex CLI sessions

# Search and load context
mempalace search "why did we switch to GraphQL"
mempalace search "database decision" --wing homelab --top-k 10
mempalace wake-up                                   # L0-L3 memory injection
```

**MCP integration** (automatic via plugin or manual):
```json
# ~/.copilot/mcp-config.json or .vscode/mcp.json
{
  "mcpServers": {
    "mempalace": {
      "command": "mempalace-mcp",
      "args": ["--palace", "/home/user/.mempalace"]
    }
  }
}
```

**Hooks** (Claude Code auto-save):
```json
# .claude/settings.local.json
{
  "hooks": {
    "Stop": [{
      "matcher": "*",
      "hooks": [{ "type": "command", "command": "/path/to/hooks/mempal_save_hook.sh", "timeout": 30 }]
    }],
    "PreCompact": [{
      "hooks": [{ "type": "command", "command": "/path/to/hooks/mempal_precompact_hook.sh", "timeout": 30 }]
    }]
  }
}
```

## Integration notes

This is the system already wired into our environment via the `mempalace` MCP server (`~/.copilot/mcp-config.json`, `.vscode/mcp.json`). Wings in active use: `homelab`, `nba_ml_engine`, `labs_wiki`, `copilot_sessions`, `copilot_cli`, `opencode`, `ops`. Session protocol mandates a `mempalace_status` + `mempalace_search` at the start of any project-scoped task and a `mempalace_diary_write` (AAAK format) at the end. The `wiki_to_mempalace.py` script in labs-wiki bridges compiled wiki pages into palace drawers.

Plugin manifests: `.claude-plugin/plugin.json` (Claude Code marketplace), `.codex-plugin/plugin.json` (Codex CLI). Slash commands: `/mempalace:init`, `/mempalace:search`, `/mempalace:mine`, `/mempalace:status`, `/mempalace:help`.

**Backfill past conversations**: One-time `mempalace mine ~/.claude/projects/ --mode convos` scans all prior JSONL transcripts → 50K–200K drawers on typical dev machine with months of history.

## Caveats / Gotchas

- **Scam alert** — Only `github.com/MemPalace/mempalace`, PyPI `mempalace`, and `mempalaceofficial.com` are official. `mempalace.tech` domain is impostor/malware (see `docs/HISTORY.md`).
- **AAAK is lossy** — AAAK mode scores **84.2% R@5 vs raw mode's 96.6%**. Entity codes + sentence truncation trade fidelity for density. The 96.6% headline is from RAW mode. AAAK is an experimental compression layer, not the default retrieval path.
- **"+34% palace boost" retracted** — Wing/room filtering is standard metadata filtering, not a novel retrieval mechanism. Useful but not a moat. Removed from all public surfaces per 2026-04-14 audit (issue #875, `docs/HISTORY.md`).
- **"100% with Haiku rerank" not headlined** — Reproduces on test machines (also 99.2% R@5 with minimax-m2.7 via Ollama Cloud), but the 99.4% → 100% step inspected specific wrong answers → flagged as "teaching to the test". Honest held-out figure: **98.4% R@5** on 450 unseen questions.
- **Concurrent writers corrupt palace** — Issue #1092. Hooks + MCP server + CLI running simultaneously on ChromaDB 1.5.8 → sparse-file bloat + SIGSEGV. File-level lock (`mine_lock`) mitigates same-file collisions; palace-wide lock pending.
- **Runaway HNSW index** — Issue #1091. Adding drawer to new room in large wing → 582 GB `link_lists.bin`. Quarantine logic in v3.3.2 detects stale HNSW after SIGSEGV; `mempalace repair` purges and rebuilds.
- **Hooks break in venv projects** — Issue #1049. Hooks hardcode `python3`; fails in projects with active venv. Set `MEMPAL_PYTHON=/path/to/venv/bin/python` override. Also: `mempalace-mcp` entry point missing from v3.3.2 `pyproject.toml` despite `plugin.json` requiring it → MCP fails fresh install (issue #1093).
- **Conversation closets not yet implemented** — Only project-mined wings (via `miner.py`) build closets today. Conversation-mined wings (Claude Code JSONL, ChatGPT export) use direct drawer search until convo-closet PR lands.
- **5,000-char extraction window** — Closet topic/entity extraction scans first 5,000 chars per file. Back-of-file content invisible to closet index (tracked for follow-up).
- **Stop hook triggers runaway mine** — Issue #1083. Stop + PreCompact hooks auto-run `mempalace mine` on transcript parent with default flags → polluted mega-wing, no opt-out. Set `MEMPAL_DIR` explicitly or unset to disable auto-mine.
- **Requires Python 3.9+** — ~300 MB disk for default embedding model. ChromaDB 1.5.4+ required (v3.2.0 removed `<0.7` upper bound to unblock chromadb 1.x palaces).
- **Windows encoding** — v3.3.2 replaces Unicode checkmark with ASCII for Windows terminal compatibility. Reparse points skipped in `detect_rooms_from_folders` on Windows.
- **macOS ARM64 segfault** — Issue #74. ORT_DISABLE_COREML no-op removed in v3.1.0 (didn't fix issue). Silence ChromaDB telemetry warnings separately.

## Repo metadata

| Field | Value |
|---|---|
| Stars | 48,804 |
| Primary language | Python (89.1%) |
| Topics | ai, chromadb, llm, mcp, memory, python |
| License | MIT |
| Latest release | v3.3.2 (2026-04-21) |
| Python support | 3.9, 3.10, 3.11, 3.12, 3.13, 3.14 |

## Related concepts

- [[mempalace-memory-system]] — MCP server, tool inventory, Palace Protocol
- [[palace-memory-architecture]] — Wing/room/hall/drawer hierarchy, tunnels, halls
- [[aaak-compression-dialect]] — 30x entity-code shorthand (lossy, 84.2% R@5 vs 96.6% raw)
- [[hybrid-retrieval-agent-memory-systems]] — Hybrid v4 pipeline, BM25 + temporal + preference boosting
- [[closet-index-layer]] — Compact topic pointers → drawer IDs, closet-first search path
- [[agent-memory-frameworks]] — Comparative positioning vs Mem0, Mastra, Hindsight, Supermemory, Zep
- [[wing-room-drawer-topology]] — Full definitions: wings, rooms, halls, closets, drawers, tunnels
- [[hybrid-v4-retrieval]] — Keyword + temporal + preference layered over semantic (98.4% R@5 held-out)
- [[mempalace-mcp-tool-inventory]] — 29 MCP tools grouped by category (palace/KG/navigation/diaries)

## Source

- Raw dump: `raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md`
- Upstream: https://github.com/milla-jovovich/mempalace
- Docs: https://mempalaceofficial.com
- Benchmarks: `benchmarks/BENCHMARKS.md` (fully reproducible)
- Corrections: `docs/HISTORY.md` (retractions, public notices)
