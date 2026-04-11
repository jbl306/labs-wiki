# MemPalace vs labs-wiki vs OpenMemory: Evaluation & Integration Plan

> **Date:** 2026-04-10
> **Status:** Proposal
> **Repo evaluated:** [safishamsi/mempalace](https://github.com/milla-jovovich/mempalace) v3.1.0

---

## Executive Summary

Three memory systems currently serve (or could serve) this homelab's AI workflow:

| System | Core Philosophy | Storage | Status |
|--------|----------------|---------|--------|
| **labs-wiki** | Compile once, maintain forever | Markdown files on disk | ✅ Running (200+ pages) |
| **OpenMemory** | Save facts, search by embedding | Qdrant + SQLite (Docker) | ✅ Running |
| **MemPalace** | Store everything verbatim, make it findable | ChromaDB + SQLite (local) | ❌ Not deployed |

**Recommendation:** Deploy MemPalace for conversational memory. Keep labs-wiki for knowledge compilation. Replace OpenMemory — MemPalace is strictly more capable in every dimension OpenMemory covers.

---

## 1. Deep Technical Analysis: MemPalace

### Architecture

MemPalace uses a **4-pillar** system:

```
┌─────────────────────────────────────────────────────────┐
│                    MCP Server (19 tools)                  │
└─────────────────────────────────────────────────────────┘
         ↓              ↓              ↓              ↓
  ┌─────────────┐ ┌─────────────┐ ┌──────────────┐ ┌──────────┐
  │  ChromaDB   │ │ Knowledge   │ │  4-Layer      │ │ Palace   │
  │  Palace     │ │ Graph       │ │  Memory Stack │ │ Graph    │
  │  (vectors)  │ │ (SQLite KG) │ │  (L0-L3)     │ │ (rooms)  │
  └─────────────┘ └─────────────┘ └──────────────┘ └──────────┘
```

**Pillar 1 — ChromaDB Palace:** Vector store of "drawers" (content chunks) organized into wings (people/projects) → rooms (topics) → closets (summaries) → drawers (verbatim text). Uses all-MiniLM-L6-v2 embeddings (384-dim, local, no API key).

**Pillar 2 — Knowledge Graph:** SQLite temporal triples `(subject, predicate, object, valid_from, valid_to, confidence)`. Like Zep Graphiti but free/local. Supports entity queries, relationship traversal, and temporal validity windows. No transitive path queries.

**Pillar 3 — 4-Layer Memory Stack:**
- **L0 Identity** (~100 tokens): Always-loaded context from `identity.txt`
- **L1 Essential Story** (~500-800 tokens): Auto-generated from highest-weight drawers
- **L2 On-Demand** (~200-500 tokens): Wing/room-filtered retrieval per query
- **L3 Deep Search** (unlimited): Full semantic search via ChromaDB embeddings

Total wake-up cost: ~170 tokens (L0+L1). Elegant token budget management.

**Pillar 4 — Palace Graph:** Navigable graph where rooms are nodes, tunnels connect rooms across wings. BFS traversal up to N hops. Discovers unexpected cross-domain connections (e.g., "what topics bridge AI and hardware?").

### Ingestion Pipeline

Two miners handle different content types:

**Project Miner (`miner.py`):**
- Scans project directories respecting `.gitignore`
- Routes files to rooms via path/filename/content keyword matching
- 800-char chunks with 100-char overlap
- Incremental via mtime checking — only re-mines modified files
- Delete-before-insert avoids ChromaDB segfault on ARM

**Conversation Miner (`convo_miner.py`):**
- Supports 7+ chat formats: Claude Code JSONL, ChatGPT JSON, Slack JSON, Codex CLI, plain text
- Normalizes all to unified `> user / AI response` format
- Exchange-pair chunking (Q+A = one semantic unit)
- Idempotent per source file

### Entity System

**Entity Detector (`entity_detector.py`):** Two-pass regex detection — extract candidates via 15+ person signals and 14+ project signals, then classify with confidence scoring. Zero dependencies, pure regex. Stops 150+ common words.

**Entity Registry (`entity_registry.py`):** 3-tier lookup hierarchy: onboarding (user-declared) > learned (session-inferred) > researched (Wikipedia API). Hierarchical confidence prevents wrong classifications from overriding user knowledge.

### MCP Server (19 Tools)

| Category | Tools | Purpose |
|----------|-------|---------|
| Status/Discovery | 3 | Palace status, list wings, list rooms |
| Taxonomy | 1 | Set custom hall keywords |
| Search | 2 | Semantic search, traverse palace graph |
| Graph Traversal | 3 | Find tunnels, graph stats, neighbor rooms |
| Drawer Ops | 2 | Add drawer, delete drawer |
| Knowledge Graph | 5 | Add/query/evolve/delete triples, list entities |
| Agent Diary | 2 | Write/read diary entries per agent |
| AAAK Spec | 1 | Return dialect format specification |

### AAAK Dialect (Experimental)

Lossy compression format: entities → 3-letter codes, key quotes preserved, emotions tagged, flags assigned (DECISION, PIVOT, TECHNICAL, etc.). Benchmarks honestly report **worse** performance than raw text (84.2% vs 96.6% R@5 on LongMemEval). Authors acknowledge this — transparency is admirable.

### Auto-Save Hooks

Hooks into AI coding sessions (Copilot CLI, OpenCode, Claude Code, Codex):
- **Stop hook:** Every 15 human exchanges, blocks AI to save key topics/decisions
- **PreCompact hook:** Before context compaction, comprehensive save (urgent)
- **Session-start:** Initialize state tracking
- WAL (write-ahead log) for audit trail of all memory writes

### Benchmark Performance

- **96.6% R@5 on LongMemEval** (raw mode, zero API calls) — highest published free score
- Fully local — no API cost per query
- ChromaDB embedding: ~50ms per add, ~30ms per search (MiniLM-L6)

---

## 2. Three-Way Comparison

### Feature Matrix

| Dimension | MemPalace | labs-wiki | OpenMemory |
|-----------|-----------|-----------|------------|
| **Philosophy** | Store verbatim, search later | Compile knowledge, maintain | Save facts, search by vector |
| **Storage** | ChromaDB + SQLite (local) | Markdown files on disk | Qdrant + SQLite (Docker) |
| **Embedding Model** | all-MiniLM-L6-v2 (local) | None (text-based) | text-embedding-3-small (API) |
| **LLM** | None required | GPT-4.1 (GitHub Models) | gpt-4o-mini (GitHub Models) |
| **Source Types** | Conversations + project files | URLs, papers, GitHub repos | Conversation-derived facts |
| **Query Interface** | 19 MCP tools + CLI | Wiki read + index search | 4 MCP tools |
| **Wake-up Protocol** | 170 tokens (L0+L1) | None (read on demand) | Memories injected per-query |
| **Graph** | SQLite temporal KG + palace graph | Wikilinks (NetworkX planned) | None |
| **Auto-save** | Hooks every 15 msgs + precompact | Docker sidecar watches raw/ | Manual save_memory calls |
| **Provenance** | source_closet string ref | Full `sources:` chain + SHA-256 hash | Memory IDs only |
| **Quality Control** | Dedup (cosine similarity) | 0-100 quality_score + lint pipeline | None |
| **Staleness** | Temporal validity on KG triples | `last_verified` + 90-day warnings | None |
| **Cross-references** | Tunnels + wikilinks within KG | `[[wikilinks]]` + `related:` | None |
| **Format** | Vector embeddings + metadata | Human-readable Markdown | Vector embeddings |
| **Browsability** | CLI/MCP tools only | Obsidian / any Markdown viewer | Web UI |
| **Cost** | $0 (fully local) | ~$0 (GitHub Models free tier) | ~$0 (GitHub Models free tier) |
| **API Keys** | None | GITHUB_MODELS_TOKEN | GITHUB_MODELS_TOKEN |
| **Docker** | Not required (pip install) | Two containers (api + auto-ingest) | Three containers (Qdrant + MCP + UI) |

### Strengths Comparison

| Strength | MemPalace | labs-wiki | OpenMemory |
|----------|-----------|-----------|------------|
| Conversational memory | ★★★★★ | ★ | ★★★ |
| Knowledge compilation | ★ | ★★★★★ | ★ |
| Research paper ingestion | ★ | ★★★★★ | ★ |
| Entity relationships | ★★★★ | ★★★ | ★ |
| Graph navigation | ★★★★ | ★★ | ★ |
| Offline operation | ★★★★★ | ★★★ | ★★ |
| Human browsability | ★★ | ★★★★★ | ★★★ |
| Deduplication | ★★★★ | ★★ | ★ |
| Cross-domain discovery | ★★★★ | ★★ | ★ |
| AI agent integration | ★★★★★ | ★★★ | ★★★ |
| Audit trail | ★★★★ | ★★★★ | ★ |
| Setup simplicity | ★★★★ | ★★ | ★★★ |

### What Each Does Best

**MemPalace excels at:**
- Remembering what was discussed, decided, debugged across sessions
- Giving agents persistent identity and personality (L0 identity layer)
- Cross-domain discovery ("what topics bridge X and Y?")
- Agent-specific diaries (reviewer has different memory from architect)
- Mining existing conversations and project files retroactively

**labs-wiki excels at:**
- Compiling research papers, articles, GitHub repos into structured knowledge
- Maintaining an evolving, interlinked knowledge graph (Obsidian-compatible)
- Quality control (scoring, linting, staleness tracking, provenance)
- Human-readable browsing (Markdown files → Obsidian/VS Code)
- Incremental compilation (only re-process changed sources)

**OpenMemory excels at:**
- Simple key-value memory storage (low cognitive overhead)
- Web UI for browsing memories
- Quick integration (4 MCP tools, easy setup)

---

## 3. Do I Need All Three?

### OpenMemory vs MemPalace (Head-to-Head)

| Capability | OpenMemory | MemPalace | Winner |
|-----------|------------|-----------|--------|
| Memory storage | Vector embeddings (Qdrant) | Vector embeddings (ChromaDB) | Tie |
| Memory structure | Flat (key-value) | Hierarchical (wing/room/closet/drawer) | MemPalace |
| Knowledge graph | None | SQLite temporal KG | MemPalace |
| Navigation | Search only | Search + graph traversal + tunnels | MemPalace |
| Agent identity | None | L0 identity + L1 story | MemPalace |
| Agent diary | None | Per-agent diary entries | MemPalace |
| Deduplication | None | Cosine similarity dedup | MemPalace |
| Auto-save | Manual calls | Hooks every 15 msgs | MemPalace |
| Conversation mining | None | 7+ chat format support | MemPalace |
| Project mining | None | Full project scanner | MemPalace |
| MCP tools | 4 | 19 | MemPalace |
| Temporal validity | None | valid_from/valid_to on triples | MemPalace |
| Audit trail | None | WAL logging | MemPalace |
| Web UI | Yes (browse memories) | No | OpenMemory |
| External API | Required (embedding model) | None (local embeddings) | MemPalace |
| Docker footprint | 3 containers (Qdrant + MCP + UI) | 0 containers (pip install) | MemPalace |

**Verdict: MemPalace is strictly superior to OpenMemory in every dimension except the web UI.** OpenMemory provides a simple vector store with 4 tools. MemPalace provides the same plus hierarchical organization, knowledge graphs, temporal validity, auto-save hooks, conversation mining, project mining, agent identity, graph navigation, deduplication, and an audit trail — all with zero API costs.

### MemPalace vs labs-wiki (Complementary, Not Competing)

These serve fundamentally different purposes:

| Dimension | MemPalace | labs-wiki |
|-----------|-----------|-----------|
| **What it remembers** | Conversations, decisions, preferences | Research, concepts, tools, techniques |
| **How it stores** | Verbatim chunks + embeddings | LLM-compiled structured pages |
| **Compilation model** | Raw storage (no LLM needed) | LLM extraction + synthesis |
| **Output format** | Vector search results | Readable Markdown knowledge base |
| **Compounding** | Grows linearly (more chunks) | Compounds (cross-references, synthesis pages) |
| **Human value** | Low (raw chunks, not for reading) | High (Obsidian browsing, knowledge map) |
| **AI value** | High (context injection, identity) | High (compiled reference, concept lookup) |

**These systems are complementary.** MemPalace captures the ephemeral (what was said), labs-wiki captures the enduring (what was learned). Neither can replace the other.

### Recommendation

```
┌──────────────────────────────────────────────────────┐
│ KEEP:    labs-wiki    → Knowledge compilation         │
│ ADD:     MemPalace    → Conversational memory         │
│ RETIRE:  OpenMemory   → Replaced by MemPalace         │
└──────────────────────────────────────────────────────┘
```

**Rationale:**
1. MemPalace covers 100% of OpenMemory's functionality and adds 15+ capabilities
2. MemPalace runs local — eliminates Qdrant's 3-container Docker footprint
3. labs-wiki + MemPalace cover both knowledge dimensions: compiled research + conversational context
4. Reducing from 3 systems to 2 simplifies operations and reduces confusion about where to store what

---

## 4. Pros and Cons of Each Decision

### Keeping labs-wiki ✅

**Pros:**
- 200+ compiled pages represent significant invested knowledge
- Obsidian-compatible browsing is irreplaceable for human review
- Quality scoring and provenance chain are production-grade
- Auto-ingest pipeline is mature and running smoothly
- Compounding knowledge (synthesis pages, cross-references) gets more valuable over time

**Cons:**
- Requires LLM API calls for ingestion (cost, though minimal on free tier)
- No conversational memory capability (different problem space)
- Docker sidecar adds operational complexity

### Adding MemPalace ✅

**Pros:**
- Fills the conversational memory gap that labs-wiki and OpenMemory both miss
- 96.6% R@5 benchmark — highest published free score
- Fully local, no API keys, offline-capable
- 4-layer memory stack is elegant token budget management
- Agent diaries enable specialized agent memory (reviewer, architect, ops)
- Temporal KG provides "when was this true?" queries
- Mining existing Copilot CLI/OpenCode sessions retroactively recovers lost context
- Palace graph discovers unexpected cross-domain connections

**Cons:**
- New system to learn and maintain
- ChromaDB is less battle-tested than Qdrant at scale
- No web UI (CLI/MCP only) — less discoverable than OpenMemory's UI
- Regex-based entity detection is naive (will miss edge cases)
- AAAK dialect is worse than raw (author admits this)
- No multi-user support (single-user design)

### Retiring OpenMemory ❌

**Pros:**
- Simplifies stack from 3 memory systems to 2
- Eliminates 3 Docker containers (Qdrant, MCP server, UI)
- MemPalace provides superset of OpenMemory's features
- Reduces confusion about "where do I store this?"

**Cons:**
- Lose the web UI for browsing memories (MemPalace has no UI)
- Need to migrate any valuable memories currently in OpenMemory
- OpenMemory's simplicity (4 tools) was easy to use — MemPalace has 19 tools (steeper learning curve)
- Qdrant is more battle-tested at scale than ChromaDB

**Mitigation for web UI loss:** MemPalace data is in ChromaDB + SQLite — a simple Flask/FastAPI viewer could be built if needed. Or browse via MCP tools in Copilot CLI / OpenCode.

---

## 5. Integration Strategy: MemPalace ↔ labs-wiki

### Bridge Architecture

```
┌──────────────┐                    ┌──────────────┐
│  MemPalace   │ ←── Insights ───→  │  labs-wiki   │
│              │                    │              │
│ Conversations│   Bridge Script    │ Research     │
│ Decisions    │ ←────────────────→ │ Concepts     │
│ Preferences  │                    │ Entities     │
│ Debug logs   │                    │ Synthesis    │
└──────────────┘                    └──────────────┘
```

**Flow 1: MemPalace → labs-wiki** (conversation insights become knowledge)
- When a significant decision, architecture choice, or tool evaluation surfaces in conversation
- Agent creates a raw source in `raw/` tagged `source: mempalace`
- Auto-ingest compiles it into wiki pages
- Example: "We decided to use ChromaDB over Pinecone" → concept page + decision record

**Flow 2: labs-wiki → MemPalace** (compiled knowledge enhances conversations)
- Agent queries wiki for context before responding
- Wiki knowledge injected at L2 (on-demand) layer
- Example: "What do we know about attention mechanisms?" → pull from wiki, not re-derive

**Flow 3: Cross-reference** (entities appear in both)
- labs-wiki entity pages link to MemPalace wings
- MemPalace KG triples reference wiki page slugs
- Unified entity namespace prevents duplicate entries

### Implementation Priority

1. **Phase 1:** Deploy MemPalace standalone, mine existing Copilot CLI / OpenCode sessions
2. **Phase 2:** Build bridge script for MemPalace → labs-wiki flow
3. **Phase 3:** Add wiki context injection to MemPalace L2 layer

---

## 6. Homelab Deployment Plan

### Option A: Native Install (Recommended)

MemPalace is designed to run locally, not in Docker. It uses file-system paths for ChromaDB and SQLite.

```bash
# Install
pip install mempalace

# Initialize palace
mempalace init ~/projects --wing homelab

# Configure
cat > ~/.mempalace/config.json << 'EOF'
{
    "palace_path": "/home/jbl/.mempalace/palace",
    "collection_name": "mempalace_drawers"
}
EOF

# Write identity
cat > ~/.mempalace/identity.txt << 'EOF'
I am jbl's AI assistant operating on a homelab.
I help with infrastructure, ML research, and knowledge management.
Key projects: labs-wiki, homelab, trading systems.
EOF
```

**MCP Configuration (Copilot CLI — `~/.copilot/mcp-config.json`):**
```json
{
    "mcpServers": {
        "mempalace": {
            "type": "stdio",
            "command": "/home/jbl/.local/share/pipx/venvs/mempalace/bin/python",
            "args": ["-m", "mempalace.mcp_server"]
        }
    }
}
```

**MCP Configuration (OpenCode — `config/opencode/opencode.json`):**
```json
{
    "mcp": {
        "mempalace": {
            "command": "/home/jbl/.local/share/pipx/venvs/mempalace/bin/python",
            "args": ["-m", "mempalace.mcp_server"]
        }
    }
}
```

> **Note:** The MCP server is invoked via `python -m mempalace.mcp_server` (not `mempalace mcp` — that subcommand doesn't exist). Use the pipx venv Python binary directly.

### Option B: Docker Container

If isolation is preferred:

```yaml
# compose.memory.yml (replaces openmemory section)
services:
  mempalace-mcp:
    build:
      context: ../../labs-wiki  # or pip install mempalace
      dockerfile: Dockerfile.mempalace
    command: mempalace mcp --stdio
    volumes:
      - ${MEMPALACE_DATA_PATH:-/home/jbl/.mempalace}:/data/.mempalace
    environment:
      - MEMPAL_PALACE_PATH=/data/.mempalace/palace
    restart: unless-stopped
```

**Recommendation: Option A (native).** MemPalace's ChromaDB uses filesystem-level locking that works better natively. Docker adds complexity without clear benefit for a single-user local tool.

### Migration Steps

#### Step 1: Install & Initialize MemPalace
```bash
pip install mempalace
mempalace init ~/projects --wing homelab
```

#### Step 2: Mine Existing Data
```bash
# Mine labs-wiki project
mempalace mine ~/projects/labs-wiki --wing labs-wiki

# Mine homelab project
mempalace mine ~/projects/homelab --wing homelab

# Mine existing Copilot CLI session artifacts (if available)
mempalace mine ~/.copilot/session-state --mode convos --wing copilot-sessions

# Mine OpenCode session history (if exported)
mempalace mine ~/.opencode/sessions --mode convos --wing opencode-sessions
```

#### Step 3: Configure MCP for Copilot CLI and OpenCode
- **Copilot CLI:** Add MemPalace to `~/.copilot/mcp-config.json` (stdio transport)
- **OpenCode:** Add MemPalace to `config/opencode/opencode.json` MCP section

#### Step 4: Configure Auto-Save Hooks
```bash
# MemPalace hooks work with any MCP-connected client
# Both Copilot CLI and OpenCode can invoke mempalace_diary_write
# and mempalace_add_drawer via MCP during sessions
mempalace hook --setup  # if supported
```

#### Step 5: Verify Operation
```bash
# Check palace status
mempalace status

# Search for a known concept
mempalace search "Docker deployment" --wing homelab

# Verify MCP tools respond
# (test via Copilot CLI or OpenCode: "What's in your memory palace?")
```

#### Step 6: Retire OpenMemory
```bash
# Export any valuable memories first
# Then stop containers
cd ~/projects/homelab/compose
docker compose -f compose.memory.yml down

# Remove from compose config
# Keep data dir as backup for 30 days
```

### Resource Requirements

| Resource | OpenMemory (current) | MemPalace (proposed) |
|----------|---------------------|---------------------|
| Containers | 3 (Qdrant, MCP, UI) | 0 (native pip) |
| RAM | ~500MB (Qdrant) | ~100MB (ChromaDB in-process) |
| Disk | ~200MB (Qdrant index) | ~50MB (ChromaDB + SQLite) |
| CPU | Continuous (Qdrant) | On-demand only |
| API calls | Per-query (embedding) | Zero (local embeddings) |
| Ports | 3 (6333, 8765, 3000) | 0 (stdio MCP) |

**Net savings:** ~400MB RAM, 3 Docker containers, 3 network ports, all embedding API costs.

---

## 7. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| ChromaDB data corruption | Low | High | Regular backups of `~/.mempalace/` |
| MemPalace project abandoned | Medium | Medium | MIT licensed, can fork; core is simple |
| Learning curve (19 tools) | Medium | Low | Start with 5 core tools, expand gradually |
| Missing web UI | Medium | Low | Build simple viewer if needed; MCP tools suffice |
| Entity detection failures | High | Low | Supplement with manual entity registry |
| Palace grows too large | Low | Medium | Dedup aggressively; archive old wings |
| Breaking changes in updates | Medium | Low | Pin version; review changelogs before updating |

---

## 8. Timeline

### Phase 1: Deploy & Mine (immediate)
- Install MemPalace via pipx
- Initialize palace with identity
- Mine labs-wiki and homelab projects
- Configure MCP server for Copilot CLI and OpenCode
- Set up auto-save hooks
- Verify basic search and recall

### Phase 2: Migrate & Retire OpenMemory (after Phase 1 verified)
- Export valuable OpenMemory memories
- Import into MemPalace as a dedicated wing
- Stop OpenMemory Docker containers
- Update homelab compose files
- Monitor for 2 weeks before deleting OpenMemory data

### Phase 3: Bridge labs-wiki ↔ MemPalace (after Phase 2 stable)
- Build bridge script: significant MemPalace conversations → labs-wiki raw/
- Add wiki context injection to MemPalace L2 queries
- Create unified entity namespace
- Test cross-system queries

### Phase 4: Advanced Features (ongoing)
- Mine retroactive Copilot CLI / OpenCode sessions
- Set up agent-specific wings (copilot_cli, opencode, reviewer, ops)
- Configure palace graph for cross-domain discovery
- Evaluate AAAK dialect (likely skip — raw mode is better)
- Consider building simple web viewer for palace browsing

---

## Appendix: MemPalace Module Map

| Module | Purpose | Lines | Key Classes/Functions |
|--------|---------|-------|-----------------------|
| `knowledge_graph.py` | Temporal KG with SQLite | ~400 | `KnowledgeGraph`, `add_triple`, `query_entity` |
| `layers.py` | 4-layer memory stack | ~300 | `MemoryLayers`, `get_l0`, `get_l1`, `build_l2` |
| `mcp_server.py` | FastMCP server (19 tools) | ~600 | Tool handlers, WAL logging |
| `palace_graph.py` | Room graph + tunnel discovery | ~250 | `build_graph`, `traverse`, `find_tunnels` |
| `entity_detector.py` | Regex-based NER | ~200 | `extract_candidates`, `classify_entity` |
| `entity_registry.py` | 3-tier entity lookup | ~250 | `EntityRegistry`, `lookup`, `_wikipedia_lookup` |
| `convo_miner.py` | Conversation mining | ~300 | `mine_convos`, `chunk_exchanges`, `detect_room` |
| `miner.py` | Project file mining | ~350 | `mine`, `scan_project`, `detect_room` |
| `dialect.py` | AAAK lossy compression | ~200 | `Dialect.encode`, `decode_for_embedding` |
| `searcher.py` | Semantic search | ~150 | `search`, `search_memories` |
| `dedup.py` | Near-duplicate detection | ~200 | `dedup_source_group` |
| `palace.py` | Shared ChromaDB utilities | ~100 | `get_collection`, `file_already_mined` |
| `normalize.py` | Chat format normalization | ~300 | `normalize` (7+ format support) |
| `config.py` | Configuration management | ~200 | `MempalaceConfig`, `sanitize_name` |
| `hooks_cli.py` | Auto-save hooks | ~250 | Stop/precompact/session-start hooks |
