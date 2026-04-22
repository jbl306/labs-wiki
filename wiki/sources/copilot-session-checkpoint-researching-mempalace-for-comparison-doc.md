---
title: "Copilot Session Checkpoint: Researching MemPalace for Comparison Doc"
type: source
created: 2026-04-11
last_verified: 2026-04-21
source_hash: "2770380bae93c0904afb7c4a75ef624686ada74d9cdbacc49e9643375baa6ced"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-researching-mempalace-for-comparison-doc-50987160.md
quality_score: 90
concepts:
  - mempalace-architecture-memory-system
  - comparison-mempalace-labs-wiki-openmemory
related:
  - "[[Comparison of MemPalace, Labs-Wiki, and OpenMemory]]"
  - "[[MemPalace]]"
  - "[[Labs-Wiki]]"
  - "[[OpenMemory]]"
  - "[[Homelab]]"
tier: hot
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki, mempalace, graph, agents, vector-search, knowledge-graph, personal-knowledge-management, memory-systems]
checkpoint_class: durable-architecture
retention_mode: retain
knowledge_state: validated
---

# Copilot Session Checkpoint: Researching MemPalace for Comparison Doc

## Summary

The user is working on labs-wiki, a personal LLM-powered knowledge wiki. This session spanned: (1) comparing labs-wiki against graphify and creating an integration plan, (2) evaluating quality of auto-ingested content, (3) implementing post-ingest quality fixes in auto_ingest.py, (4) rebuilding/deploying the Docker sidecar, and (5) deeply researching mempalace (github.com/milla-jovovich/mempalace) to evaluate whether it should replace or complement labs-wiki and openmemory. The current task is writing a comprehensive comparison doc between mempalace, labs-wiki, and openmemory for the plans/ directory.

## Key Points

- All 3 explore agents completed with full results
- mempalace README fully read and analyzed (architecture, AAAK, benchmarks, 19 MCP tools)
- Core modules analyzed (knowledge_graph.py, layers.py, mcp_server.py, palace_graph.py, etc.)
- Integrations analyzed (.claude-plugin, .codex-plugin, hooks, openclaw, gemini)
- User's openmemory setup analyzed (compose.memory.yml, config.json, Qdrant)
- User asked to compare labs-wiki vs graphify and create a plan

## Execution Snapshot

**Files created (committed):**
- `plans/graphify-integration.md`: Comparison plan with 3-phase integration roadmap (commit 97eb713)
- `plans/quality-evaluation-2026-04-10.md`: Quality evaluation report (commit 5859670)

**Files modified (committed):**
- `scripts/auto_ingest.py`: 4 major changes — prompt hardening, entity template, postprocessor, pipeline integration (commit e8dcd26)
- 191 wiki pages: Wiki-wide cleanup (broken links, self-refs, dedup, quality scores) (commit e8dcd26)

**Docker deployment:**
- wiki-auto-ingest container rebuilt and redeployed (running, watching raw/)

**Files NOT YET created (in progress):**
- `plans/mempalace-evaluation.md`: The comparison doc — research complete, writing not started

**Current state:**
- [x] All 3 explore agents completed with full results
- [x] mempalace README fully read and analyzed (architecture, AAAK, benchmarks, 19 MCP tools)
- [x] Core modules analyzed (knowledge_graph.py, layers.py, mcp_server.py, palace_graph.py, etc.)
- [x] Integrations analyzed (.claude-plugin, .codex-plugin, hooks, openclaw, gemini)
- [x] User's openmemory setup analyzed (compose.memory.yml, config.json, Qdrant)
- [ ] **NOT STARTED: Writing the comparison document to plans/**
- [ ] **NOT STARTED: Committing and pushing the document**

## Technical Details

- **Philosophy**: "Store everything verbatim, make it findable" — opposite of labs-wiki's "compile once, maintain"
- **Storage**: ChromaDB (vector DB, local) + SQLite (knowledge graph, WAL-enabled)
- **Palace metaphor**: Wings (person/project) → Rooms (topics) → Closets (summaries) → Drawers (verbatim content)
- Halls = memory types within a wing (facts, events, discoveries, preferences, advice)
- Tunnels = cross-wing connections (same room name in different wings)
- **4-Layer Memory Stack**:
- L0: Identity (~100 tokens, always loaded from identity.txt)
- L1: Essential Story (~500-800 tokens, auto-generated from highest-weight drawers)
- L2: On-Demand (~200-500 tokens, filtered by wing/room)
- L3: Deep Search (unlimited, semantic via ChromaDB embeddings)
- **Wake-up cost**: ~170 tokens (L0+L1), vs labs-wiki which has no wake-up protocol
- **AAAK Dialect**: Experimental lossy abbreviation system. Honestly benchmarks WORSE than raw (84.2% vs 96.6% on LongMemEval). Authors acknowledge this openly.
- **Knowledge Graph**: SQLite temporal triples (subject, predicate, object, valid_from, valid_to, confidence). Like Zep Graphiti but local/free. No transitive queries.
- **Benchmarks**: 96.6% LongMemEval R@5 (raw mode, zero API calls) — highest published free score
- **19 MCP Tools**: Status/discovery (3), taxonomy (1), search (2), graph traversal (3), drawer ops (2), KG (5), agent diary (2)
- **Auto-Save Hooks**: Save every 15 messages + PreCompact emergency save. Claude Code / Codex hooks.
- **Specialist Agents**: Agents get their own wing + diary (reviewer, architect, ops)
- **Mining modes**: projects (code/docs), convos (conversation exports), general (auto-classify)
- **Dedup**: Embedding similarity threshold 0.9, can lower to 0.85-0.87
- **Entity detection**: Auto-detects people and projects from content, creates entity codes ### Key Differences: MemPalace vs labs-wiki vs OpenMemory | Dimension | MemPalace | labs-wiki | OpenMemory | |-----------|-----------|-----------|------------| | Storage | ChromaDB + SQLite (local) | Markdown files on disk | Qdrant + SQLite (Docker) | | Model | Verbatim storage + semantic search | LLM-compiled knowledge pages | Vector memory with LLM extraction | | Source | Conversations + project files | URLs, papers, GitHub repos | Conversation-derived facts | | Query | 19 MCP tools + CLI | Wiki read + index search | 4 MCP tools (search/save/update/delete) | | Wake-up | 170 tokens (L0+L1) | No wake-up protocol | Memories injected per-query | | Graph | SQLite temporal KG + palace navigation | Wikilinks (planned: NetworkX) | None | | Auto-save | Hooks every 15 msgs + precompact | Docker sidecar watches raw/ | Manual save_memory calls | | Provenance | source_closet string ref | Full sources: chain + source_hash | Memory IDs only | | Quality | No scoring | 0-100 quality_score + lint | No scoring | | Cost | $0 (fully local) | ~$0 (GitHub Models API free tier) | ~$0 (GitHub Models API free tier) | ### User's Current Setup
- **OpenMemory**: Running on homelab (Qdrant + MCP server + UI), uses gpt-4o-mini + text-embedding-3-small via GitHub Models API
- **labs-wiki**: 200 compiled wiki pages, auto-ingest Docker sidecar, GPT-4.1 extraction
- **Gap**: No sync between openmemory and labs-wiki — they're separate islands ### My Assessment (to be written in doc)
- MemPalace excels at **conversational memory** (what was discussed, decided, debugged)
- labs-wiki excels at **knowledge compilation** (research papers, tools, concepts)
- OpenMemory is the weakest of the three — simple key-value memory without structure
- Recommendation will likely be: **Keep labs-wiki + Add MemPalace + Consider replacing OpenMemory** ### Explore Agent Output Locations
- mempalace-core-modules results: `/tmp/1775876490891-copilot-tool-output-kpz0i8.txt` (43.9 KB, read first 200 lines)
- mempalace-integrations results: Read inline (full output captured in history)
- openmemory-analysis results: Read inline (full output captured in history)
- mempalace README: `/tmp/1775876289790-copilot-tool-output-zqytkw.txt` (33KB, read lines 1-700) ### Remaining Core Modules Output (not yet read)
- The core modules agent output at `/tmp/1775876490891-copilot-tool-output-kpz0i8.txt` was only read through line 200 (out of ~800+)
- Lines 200+ contain: remaining MCP server analysis, palace_graph.py, entity_detector.py, entity_registry.py, convo_miner.py, miner.py, dialect.py, searcher.py, dedup.py, palace.py analysis
- Should read the rest before writing the comparison doc

## Important Files

- `plans/mempalace-evaluation.md` (TO BE CREATED)
- The deliverable for this task — comprehensive comparison of mempalace vs labs-wiki vs openmemory
- Will include: deep technical analysis, pros/cons, recommendation, homelab deployment plan
- Not yet written — all research is complete, synthesis needed

- `scripts/auto_ingest.py`
- Core auto-ingest pipeline — all quality fixes from earlier in session are committed
- postprocess_created_pages() at ~line 1310-1415
- Committed in e8dcd26, deployed to Docker

- `plans/graphify-integration.md`
- Earlier deliverable — graphify comparison (committed 97eb713)
- Relevant context: graphify planned NetworkX graph layer for labs-wiki

- `plans/quality-evaluation-2026-04-10.md`
- Quality evaluation that drove the auto_ingest.py fixes (committed 5859670)

- `/tmp/1775876490891-copilot-tool-output-kpz0i8.txt`
- Full core modules technical analysis from explore agent (43.9 KB)
- Only read through line 200 — need to read lines 200+ for remaining module analysis

- `/tmp/1775876289790-copilot-tool-output-zqytkw.txt`
- Full mempalace README (33 KB) — read through line 700

- `/home/jbl/projects/homelab/compose/compose.wiki.yml`
- Docker compose for wiki services (wiki-ingest-api + wiki-auto-ingest)
- Used for rebuild/deploy earlier in session

- `/home/jbl/projects/homelab/compose/compose.memory.yml`
- Docker compose for openmemory (Qdrant + MCP + UI)
- Analyzed by openmemory-analysis agent

## Next Steps

**Remaining work:**
1. **Read remaining core modules output** — lines 200+ of `/tmp/1775876490891-copilot-tool-output-kpz0i8.txt` contain palace_graph, entity_detector, entity_registry, convo_miner, miner, dialect, searcher, dedup, palace analyses
2. **Write the comparison document** — `plans/mempalace-evaluation.md` synthesizing all research:
- Deep technical analysis of mempalace architecture
- Three-way comparison: mempalace vs labs-wiki vs openmemory
- Pros/cons of each system
- Recommendation: keep all 3, replace openmemory, or merge
- Homelab deployment plan for mempalace
- Integration strategy (how mempalace + labs-wiki can complement each other)
3. **Commit and push** the document to labs-wiki repo

**Immediate next actions:**
- Read remaining explore agent output (lines 200-end of core modules file)
- Write comprehensive markdown doc to `plans/mempalace-evaluation.md`
- `git add plans/mempalace-evaluation.md && git commit && git push`

**Key decisions to address in the doc:**
- Should mempalace replace openmemory? (Likely yes — mempalace is strictly more capable)
- Should mempalace replace labs-wiki? (Likely no — different purposes: conversational memory vs compiled knowledge)
- How to deploy mempalace in homelab? (Docker container or native install?)
- How to bridge mempalace ↔ labs-wiki? (Conversation insights → raw/ sources?)

## Related Wiki Pages

- [[Comparison of MemPalace, Labs-Wiki, and OpenMemory]]
- [[MemPalace]]
- [[Labs-Wiki]]
- [[OpenMemory]]
- [[Homelab]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-researching-mempalace-for-comparison-doc-50987160.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-04-11 |
| URL | N/A |
