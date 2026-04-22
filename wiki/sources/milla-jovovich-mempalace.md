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
ingest_method: manual-reprocess-github-2026-04-22
quality_score: 80
concepts:
- mempalace-memory-system
- palace-memory-architecture
- hybrid-retrieval-agent-memory-systems
- agent-memory-frameworks
---

# milla-jovovich/mempalace

## What it is

MemPalace is a local-first AI memory system that stores conversation history as verbatim text and retrieves it with semantic search — no summarization, no extraction, no paraphrasing. Content is filed into a structured index of *wings* (people, projects), *rooms* (topics), and *drawers* (the original verbatim text), so retrieval can be scoped instead of running flat over the whole corpus. The retrieval backend is pluggable; ChromaDB is the default. Nothing leaves your machine unless you opt in.

## Why it matters

This is the memory layer we already use across every agent in this workspace — Copilot CLI, OpenCode, the labs-wiki MCP, and per-project session diaries all file into MemPalace. It's the only open-source memory project that publishes a 96.6% R@5 raw score on LongMemEval without an LLM in the retrieval path, which is what makes it credible as the substrate for cross-session continuity rather than a toy demo.

## Key concepts

- **Verbatim storage** — Drawers store the exact original text, never a summary. Summarization is the failure mode that other memory systems suffer from.
- **Wings / rooms / drawers** — Hierarchical scoping (people/projects → topics → content) that lets searches be narrowed without filters or post-processing. See [[palace-memory-architecture]].
- **Pluggable backend** — `mempalace/backends/base.py` defines the interface; ChromaDB is default and other vector stores can be dropped in.
- **Knowledge graph** — Temporal entity-relationship graph with validity windows (add / query / invalidate / timeline) backed by local SQLite, alongside the vector store.
- **MCP server** — 29 MCP tools cover palace reads/writes, knowledge-graph operations, cross-wing navigation, drawer management, and per-agent diaries. See [[mempalace-memory-system]].
- **Hybrid v4 retrieval** — Adds keyword boosting, temporal-proximity boosting, and preference-pattern extraction on top of raw semantic search; held-out 98.4% R@5. See [[hybrid-retrieval-agent-memory-systems]].
- **Agent diaries** — Each specialist agent gets its own wing and AAAK-compressed diary, discoverable at runtime via `mempalace_list_agents`.
- **Auto-save hooks** — Two Claude Code hooks save periodically and before context compression.

## How it works

- Content is mined from project files or chat session logs into the palace, partitioned by wing.
- Embeddings are computed locally (~300 MB default model) and indexed in ChromaDB.
- Queries hit the semantic index, optionally with hybrid boosting (keyword + recency + preference patterns).
- An optional LLM rerank stage promotes the best of the top-20 candidates — works with any capable model (Haiku, Sonnet, minimax-m2.7 via Ollama Cloud).
- The knowledge graph is queried separately for typed temporal facts (e.g., "what role did X have on date Y").
- All benchmarks (LongMemEval, LoCoMo, ConvoMem, MemBench) are reproducible from the repo.

## Setup

```bash
pip install mempalace
mempalace init ~/projects/myapp

# Mine content into the palace
mempalace mine ~/projects/myapp
mempalace mine ~/.claude/projects/ --mode convos

# Search and load context
mempalace search "why did we switch to GraphQL"
mempalace wake-up
```

## Integration notes

This is the system already wired into our environment via the `mempalace` MCP server (`~/.copilot/mcp-config.json`, `.vscode/mcp.json`). Wings in active use: `homelab`, `nba_ml_engine`, `labs_wiki`, `copilot_sessions`, `copilot_cli`, `opencode`, `ops`. Session protocol mandates a `mempalace_status` + `mempalace_search` at the start of any project-scoped task and a `mempalace_diary_write` (AAAK format) at the end. The `wiki_to_mempalace.py` script in labs-wiki bridges compiled wiki pages into palace drawers.

## Caveats / Gotchas

- A scam alert in the README warns that only `github.com/MemPalace/mempalace`, the PyPI package, and `mempalaceofficial.com` are official sources. The `mempalace.tech` domain is impostor / malware.
- Requires Python 3.9+ and ~300 MB disk for the default embedding model.
- The headline 96.6% raw R@5 requires no API key, but the hybrid v4 / rerank gains require either tuning data or an LLM.
- v3.3.2 includes a PID-file guard to prevent stacked `mine` processes and quarantine logic for stale HNSW indexes after SIGSEGV.

## Repo metadata

| Field | Value |
|---|---|
| Stars | 48,804 |
| Primary language | Python |
| Topics | ai, chromadb, llm, mcp, memory, python |
| License | MIT |

## Source

- Raw dump: `raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md`
- Upstream: https://github.com/milla-jovovich/mempalace
