# Graphify Feature Integration Plan

> **Goal:** Incorporate the best ideas from [graphify](https://github.com/safishamsi/graphify) into labs-wiki to add graph-based knowledge navigation on top of the existing wiki compilation pipeline.

## Feature Comparison

### What graphify has that labs-wiki lacks

| # | Feature | graphify Implementation | Value for labs-wiki | Priority |
|---|---------|------------------------|--------------------|---------:|
| 1 | **Knowledge Graph (NetworkX)** | Builds `nx.Graph` from extracted nodes/edges, persisted as `graph.json` | Enables traversal queries, shortest-path, community detection — far richer than flat wikilink text search | **P0** |
| 2 | **Community Detection (Leiden/Louvain)** | Clusters nodes by edge density; splits oversized communities; reports cohesion scores | Auto-discovers topic clusters — replaces manual taxonomy; surfaces emergent groupings | **P0** |
| 3 | **God Node Analysis** | Ranks nodes by degree; filters out file-hub and method-stub noise | Identifies the "load-bearing abstractions" across the entire wiki — what everything connects through | **P1** |
| 4 | **Surprising Connections** | Cross-community/cross-file edges ranked by AMBIGUOUS → INFERRED → EXTRACTED | Surfaces non-obvious relationships between concepts — the "aha" moments a flat wiki misses | **P1** |
| 5 | **Confidence Labels** | Every edge tagged EXTRACTED / INFERRED / AMBIGUOUS with confidence scores (0.0–1.0) | Provenance at the *relationship* level, not just page level — always know what's fact vs guess | **P1** |
| 6 | **Interactive HTML Graph** | vis.js renderer with click-to-inspect, community colors, search, physics clustering | One-click visual exploration; massive UX improvement over reading `index.md` | **P1** |
| 7 | **Graph Query via MCP** | BFS/DFS traversal, `shortest_path`, `get_neighbors`, `get_community`, `god_nodes`, `graph_stats` | LLM agents can *navigate* the wiki by structure, not just keyword match | **P0** |
| 8 | **Token Benchmark** | Measures corpus tokens vs graph-query tokens; reports reduction ratio | Quantifies the value of compilation — "71x fewer tokens per query" is a killer metric | **P2** |
| 9 | **Suggested Questions** | Analyzes graph structure to generate 4-5 questions the graph can uniquely answer | Surfaces what's worth asking — useful for @wiki-query and daily review | **P2** |
| 10 | **Memory Feedback Loop** | Saves Q&A results to `memory/` dir; re-extracts into graph on `--update` | The wiki *learns from queries* — answers compound into the knowledge base automatically | **P1** |
| 11 | **Obsidian Vault Export** | Node-per-file with `[[wikilinks]]`, community tags, YAML frontmatter, Canvas layout | Labs-wiki already uses Obsidian-compatible links; a true vault export enables Obsidian graph view | **P2** |
| 12 | **Semantic Similarity Edges** | Cross-file conceptual links between structurally unrelated nodes | Connects related wiki pages that don't cite each other — e.g., "LSTM" ↔ "Transformer Architecture" | **P1** |
| 13 | **Hyperedges** | Group relationships connecting 3+ nodes (e.g., all ensemble methods, all attention variants) | Expresses "belongs to family" relationships that pairwise edges can't capture | **P2** |
| 14 | **SHA256 Extraction Cache** | Per-file `cache/{hash}.json` — re-runs skip unchanged files | Labs-wiki has `source_hash` but only at raw→wiki level; graph extraction cache is per-concept | **P1** |
| 15 | **Neo4j / GraphML Export** | Cypher generation and `--neo4j-push` for external graph databases | Enables Gephi/yEd/Neo4j exploration for larger knowledge bases | **P3** |
| 16 | **Git Hooks** | post-commit + post-checkout hooks auto-rebuild graph | Keeps graph in sync without Docker sidecar for local-only setups | **P2** |
| 17 | **Graph Report** | `GRAPH_REPORT.md` with god nodes, surprising connections, suggested questions | Single-page executive summary an agent reads before answering architecture questions | **P1** |

### What labs-wiki has that graphify lacks

| Feature | labs-wiki Implementation | Keep? |
|---------|--------------------------|-------|
| Docker auto-ingest pipeline | File watcher sidecar, always-on, GPT-4.1 via GitHub Models | ✅ Core strength |
| Smart URL handlers | Twitter/X (fxtwitter), GitHub repos (REST API + README), HTML + vision | ✅ Core strength |
| Page type taxonomy | source / concept / entity / synthesis with templates | ✅ Keep — maps to graph node types |
| Consolidation tiers | hot → established → core → workflow | ✅ Keep — enriches graph node metadata |
| Quality scoring (0-100) | Completeness + cross-refs + attribution + recency | ✅ Keep — becomes node weight in graph |
| Staleness tracking | `last_verified` + 90-day threshold | ✅ Keep — feeds graph analysis |
| Agent personas | Researcher, Compiler, Curator, Auditor | ✅ Keep — orchestration layer |
| ntfy notifications | Success/failure alerts on ingest | ✅ Keep — operational infra |
| HTTP API for capture | FastAPI with multiple input channels | ✅ Keep — graphify only has CLI |
| Lint system | Broken links, orphans, quality, staleness | ✅ Keep — complementary to graph analysis |

## Architecture: How to Integrate

### Principle: Graph as a *layer on top*, not a replacement

Labs-wiki's three-layer architecture (raw → wiki → schema) stays intact. The knowledge graph becomes **Layer 2.5** — derived from wiki pages, not from raw sources directly. This preserves the existing compilation pipeline and adds graph intelligence as a complementary view.

```
raw/            → Layer 1: Immutable source documents (unchanged)
wiki/           → Layer 2: LLM-compiled pages (unchanged)
wiki/graph/     → Layer 2.5: Knowledge graph derived from wiki pages (NEW)
  graph.json       Persistent NetworkX graph (node-link format)
  graph.html       Interactive vis.js visualization
  GRAPH_REPORT.md  God nodes, surprises, suggested questions
  cache/           Per-page extraction cache (SHA256-keyed)
AGENTS.md       → Layer 3: Schema and conventions (updated)
```

### Data Flow

```
                    ┌──────────────────────┐
                    │ wiki/**/*.md pages    │
                    │ (existing pipeline)   │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │ graph_extract.py      │
                    │ - Parse frontmatter   │
                    │ - Extract wikilinks   │
                    │ - LLM: infer edges    │
                    │ - Confidence labels   │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │ graph_build.py        │
                    │ - NetworkX graph      │
                    │ - Leiden clustering   │
                    │ - Cohesion scores     │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
    ┌─────────▼──────┐ ┌──────▼──────┐ ┌───────▼───────┐
    │ graph_analyze   │ │ graph_export│ │ graph_report  │
    │ - God nodes     │ │ - graph.json│ │ - REPORT.md   │
    │ - Surprises     │ │ - graph.html│ │ - Suggested   │
    │ - Questions     │ │ - Obsidian  │ │   questions   │
    └────────────────┘ └─────────────┘ └───────────────┘
```

## Implementation Plan

### Phase 1: Graph Foundation (P0)

Build the core graph from existing wiki pages — no LLM calls needed for the initial version.

#### 1.1 — `scripts/graph_extract.py`: Wiki → nodes + edges

- Parse every `wiki/**/*.md` page:
  - Each page = 1 node (id = filename slug, label = title, type = frontmatter type)
  - Node metadata: tier, quality_score, created, last_verified, concepts[], tags[]
  - Wikilinks `[[Page Title]]` in body = EXTRACTED edges (confidence 1.0, relation: `references`)
  - `related:` frontmatter entries = EXTRACTED edges (relation: `related_to`)
  - `sources:` entries = EXTRACTED edges to source nodes (relation: `derived_from`)
  - Same `concepts:` tags on two pages = INFERRED edge (relation: `shares_concept`, confidence 0.7)
- Output: `{nodes: [...], edges: [...]}` JSON
- Extraction cache: SHA256 of page content → `wiki/graph/cache/{hash}.json`

#### 1.2 — `scripts/graph_build.py`: Assemble NetworkX graph

- Port graphify's `build.py` pattern (idempotent node addition, edge dedup)
- Add Leiden community detection (graspologic) with Louvain fallback
- Oversized community splitting (>25% of graph)
- Cohesion score per community
- Persist as `wiki/graph/graph.json` (node-link format)

#### 1.3 — Integrate with auto-ingest pipeline

- After `auto_ingest.py` writes wiki pages, trigger graph rebuild
- Incremental: only re-extract changed pages (cache hit check)
- Update `wiki/graph/graph.json` in place

#### 1.4 — Extend MCP server (`wiki_mcp_server.py`)

Add graph-aware tools alongside existing search/read/list:

| Tool | Description |
|------|-------------|
| `wiki_graph_query` | BFS/DFS traversal from keyword-matched start nodes |
| `wiki_graph_path` | Shortest path between two concepts |
| `wiki_graph_neighbors` | Direct connections of a node with edge metadata |
| `wiki_graph_communities` | List communities with labels and cohesion scores |
| `wiki_graph_god_nodes` | Top-N most connected concepts |
| `wiki_graph_stats` | Node/edge counts, confidence breakdown, community count |

### Phase 2: Analysis & Visualization (P1)

#### 2.1 — `scripts/graph_analyze.py`: Analysis functions

Port from graphify's `analyze.py`:
- `god_nodes(G, top_n)` — highest-degree real concepts (filter out trivial nodes)
- `surprising_connections(G, communities)` — cross-community edges, ranked by unexpectedness
- `suggested_questions(G, communities)` — what the graph is uniquely positioned to answer
- `knowledge_gaps(G, communities)` — communities with low cohesion or isolated nodes

#### 2.2 — `scripts/graph_report.py`: Generate GRAPH_REPORT.md

Write `wiki/graph/GRAPH_REPORT.md`:
- God nodes section (top 10 with connection counts)
- Surprising connections (top 5 with explanations)
- Community summary (labeled clusters with sizes and cohesion)
- Suggested questions (4-5 auto-generated)
- Confidence audit (EXTRACTED/INFERRED/AMBIGUOUS breakdown)

#### 2.3 — `scripts/graph_export.py`: Visualization

- Interactive HTML graph (`wiki/graph/graph.html`) using vis.js
  - Node color by community, size by degree
  - Click-to-inspect panel with page metadata
  - Search box and community filter
- Port graphify's `to_html()` with labs-wiki styling

#### 2.4 — Confidence labels on edge extraction

- Enhance `graph_extract.py` with LLM pass:
  - For each pair of wiki pages in the same community, ask LLM if there's a semantic relationship
  - Tag as INFERRED with confidence score
  - Pages with shared concepts but no explicit wikilink = INFERRED
  - Explicit wikilinks = EXTRACTED

#### 2.5 — Semantic similarity edges

- After initial graph build, run LLM over pairs of pages without direct links
- If semantically related, add INFERRED edge with confidence score
- Budget: limit to top-N candidates by shared tags/concepts to control API cost

#### 2.6 — Memory feedback loop

- When `@wiki-query` answers a question:
  - Save Q&A to `wiki/graph/memory/` as markdown
  - On next graph rebuild, extract into nodes/edges
  - The wiki grows smarter from what you ask, not just what you add

### Phase 3: Polish & Exports (P2-P3)

#### 3.1 — Token benchmark

- `scripts/graph_benchmark.py`: compare raw wiki tokens vs graph-query tokens
- Report in GRAPH_REPORT.md and on ingest completion

#### 3.2 — Obsidian vault enhancement

- Labs-wiki already uses `[[wikilinks]]` — add:
  - Community tags in frontmatter
  - Obsidian Canvas layout JSON from community structure
  - `_COMMUNITY_*.md` overview notes (graphify pattern)

#### 3.3 — Git hooks (optional)

- `graphify hook install` equivalent: post-commit rebuilds graph
- Useful for local-only workflows without Docker sidecar

#### 3.4 — Neo4j / GraphML export (optional)

- Cypher generation for Neo4j import
- GraphML for Gephi/yEd

#### 3.5 — Graph report in AGENTS.md

- Add section telling agents to read `wiki/graph/GRAPH_REPORT.md` before answering cross-cutting questions
- Mirror graphify's PreToolUse hook pattern: "read the graph report first"

#### 3.6 — Suggested questions in daily maintenance

- Integrate `suggested_questions()` into `@wiki-orchestrate` maintenance workflow
- Surface in ntfy notifications alongside lint results

## Dependencies

```
# New Python dependencies (add to requirements-auto-ingest.txt)
networkx>=3.0
graspologic>=3.0        # Leiden community detection (optional, falls back to Louvain)
```

No new Docker services needed — graph operations run within the existing auto-ingest container or locally via scripts.

## What NOT to adopt from graphify

| Feature | Reason to skip |
|---------|---------------|
| tree-sitter AST extraction | Labs-wiki ingests knowledge articles, not codebases |
| 19-language code support | Not relevant — wiki pages are markdown |
| Parallel subagent extraction | Labs-wiki uses single-pass GPT-4.1 extraction — simpler, sufficient |
| `graphify install` CLI | Labs-wiki has its own `setup.sh` and Docker deployment |
| `--watch` file watcher | Labs-wiki already has `wiki-auto-ingest` Docker sidecar |
| PDF extraction via pypdf | Labs-wiki handles this via URL fetch + vision in auto-ingest |

## Success Metrics

1. **Graph builds from existing wiki** — all ~175 pages become nodes with correct edges
2. **Communities are meaningful** — Leiden clusters ML algorithms, agent patterns, transformer concepts separately
3. **God nodes match intuition** — "Transformer Architecture", "Decision Tree Algorithm" should be highly connected
4. **MCP query works** — `wiki_graph_path("LSTM", "Transformer")` returns a meaningful traversal
5. **GRAPH_REPORT.md is useful** — agents read it and navigate more efficiently than keyword search
6. **HTML graph loads** — interactive visualization with all nodes/communities renders in browser

## File Inventory (new files)

```
scripts/
  graph_extract.py     # Wiki pages → nodes + edges JSON
  graph_build.py       # Extraction → NetworkX → Leiden → graph.json
  graph_analyze.py     # God nodes, surprises, questions, gaps
  graph_report.py      # Generate GRAPH_REPORT.md
  graph_export.py      # HTML visualization, Obsidian enhancement
  graph_benchmark.py   # Token reduction measurement
wiki/graph/
  graph.json           # Persistent knowledge graph
  graph.html           # Interactive visualization
  GRAPH_REPORT.md      # Analysis report
  cache/               # Per-page extraction cache
  memory/              # Q&A feedback loop storage
```
