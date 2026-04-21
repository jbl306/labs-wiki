---
title: "Copilot Session Checkpoint: Graphify Comparison and Quality Evaluation"
type: source
created: 2026-04-10
last_verified: 2026-04-21
source_hash: "8569d239f29d3a3edd5d15d9e9f3fcf1f4cd252be8b9dbbc7c751bf7b2fced19"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-graphify-comparison-and-quality-evaluation-6949c984.md
quality_score: 100
concepts:
  - labs-wiki-architecture
  - graphify-features-for-knowledge-graph-integration
  - quality-evaluation-of-auto-ingested-wiki-content
related:
  - "[[Labs-Wiki Architecture]]"
  - "[[Graphify Features for Knowledge Graph Integration]]"
  - "[[Quality Evaluation of Auto-Ingested Wiki Content]]"
  - "[[Labs-Wiki]]"
  - "[[AutoSkills]]"
  - "[[Homelab]]"
tier: hot
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki, graph, agents, graphify, auto-ingest, quality-evaluation, knowledge-graph]
checkpoint_class: durable-architecture
retention_mode: retain
knowledge_state: validated
---

# Copilot Session Checkpoint: Graphify Comparison and Quality Evaluation

## Summary

The user is working on labs-wiki, a personal LLM-powered knowledge wiki that auto-ingests sources (URLs, papers, repos) into compiled wiki pages. They asked me to: (1) compare labs-wiki against graphify (safishamsi/graphify) and create an integration plan, (2) push it to GitHub, and (3) evaluate the quality of wiki content ingested today (April 10, 2026) against the original raw sources. The third task was in progress when compaction occurred.

## Key Points

- Deep analysis of graphify codebase (all key modules)
- Feature-by-feature comparison with labs-wiki
- Created integration plan with 3 phases (P0-P3 priorities)
- Pushed plan to GitHub (commit 97eb713 on main)
- Identified today's 5 raw sources and 26 generated wiki pages
- Fetched ground truth from arXiv for 2 papers

## Execution Snapshot

**Files created:**
- `plans/graphify-integration.md`: Full comparison plan between labs-wiki and graphify with integration roadmap

**Work completed:**
- [x] Deep analysis of graphify codebase (all key modules)
- [x] Feature-by-feature comparison with labs-wiki
- [x] Created integration plan with 3 phases (P0-P3 priorities)
- [x] Pushed plan to GitHub (commit 97eb713 on main)
- [x] Identified today's 5 raw sources and 26 generated wiki pages
- [x] Fetched ground truth from arXiv for 2 papers
- [ ] **IN PROGRESS**: Quality evaluation of today's wiki content vs raw sources

**Background agents launched (may have completed):**
- `eval-lottery-ticket` — reading 6 wiki pages from Lottery Ticket Hypothesis ingest
- `eval-llm-reasoning` — reading 6 wiki pages from LLM Reasoning Failures ingest
- `eval-axi-repo` — reading 7 wiki pages from AXI repo ingest
- `eval-autoskills` — reading 7 wiki pages from autoskills repo ingest

## Technical Details

- Three-layer: `raw/` (immutable sources) → `wiki/` (compiled pages in concepts/, entities/, sources/, synthesis/) → `AGENTS.md` (schema)
- Auto-ingest Docker sidecar watches `raw/` for `status: pending`, processes via GPT-4.1 (GitHub Models API)
- Smart URL handlers: Twitter/X (fxtwitter), GitHub repos (REST API + README), HTML + vision
- MCP server (`scripts/wiki_mcp_server.py`) with wiki_search, wiki_read, wiki_list tools
- ~175 wiki pages in index.md, all currently tier: hot, score: 0 ### graphify Key Features Worth Adopting (from plan)
- **P0**: NetworkX knowledge graph, Leiden community detection, graph-aware MCP tools (BFS/DFS/shortest_path)
- **P1**: God node analysis, surprising connections, confidence labels (EXTRACTED/INFERRED/AMBIGUOUS), interactive HTML vis.js graph, GRAPH_REPORT.md, memory feedback loop, semantic similarity edges, SHA256 extraction cache
- **P2-P3**: Token benchmark, Obsidian vault enhancement, git hooks, Neo4j/GraphML export ### What NOT to Adopt from graphify
- tree-sitter AST extraction (labs-wiki is knowledge articles, not code)
- 19-language code support, parallel subagent extraction, `graphify install` CLI, `--watch` (labs-wiki has Docker sidecar) ### Today's Raw Sources (2026-04-10)
- All 5 are minimal: just URL + frontmatter via Android share, no pre-fetched content
- Raw files are ~300 bytes each — the auto-ingest pipeline fetches actual content
- 1803.03635 = Lottery Ticket Hypothesis (Frankle & Carbin, ICLR 2019)
- 2602.06176 = LLM Reasoning Failures survey (Song et al., TMLR 2026)
- 2512.24601 = Unknown paper (ingested but missing from log — may have just been processed or failed silently)
- kunchenguid/axi = Agent eXperience Interface CLI tool
- midudev/autoskills = Automated AI skill stack installer for Claude Code ### Architecture Decision from Plan
- Graph becomes "Layer 2.5" — derived FROM wiki pages, not from raw sources directly
- Lives at `wiki/graph/` (graph.json, graph.html, GRAPH_REPORT.md, cache/)
- New scripts: graph_extract.py, graph_build.py, graph_analyze.py, graph_report.py, graph_export.py
- Dependencies: networkx>=3.0, graspologic>=3.0 (Leiden, optional) ### Quirks Discovered
- The 5th raw source (2512.24601) has `status: ingested` but no entry in wiki/log.md — possibly processed after the log was last checked, or a race condition
- All wiki pages have quality_score: 0 and tier: hot — scoring/promotion not yet implemented
- Homelab deployment: wiki-ingest-api runs as Docker service, proxied at wiki-ingest.jbl-lab.com via Caddy

## Important Files

- `plans/graphify-integration.md`
- Created this session: full comparison plan between labs-wiki and graphify
- 267 lines covering feature comparison, architecture, 3-phase implementation plan
- Pushed to GitHub as commit 97eb713

- `wiki/log.md`
- Audit log of all ingest operations; used to identify today's 4 successful ingests (26 pages)
- Missing entry for 2512.24601 source

- `wiki/index.md`
- Auto-generated catalog of ~175 wiki pages
- All pages currently tier: hot, score: 0

- `raw/2026-04-10-*.md` (5 files)
- Today's raw sources being evaluated; all minimal URL stubs via Android share

- `scripts/auto_ingest.py`
- The pipeline that processed today's sources; key for understanding extraction quality
- Uses GPT-4.1 via GitHub Models API

- `scripts/wiki_mcp_server.py`
- Current MCP server with wiki_search/read/list; will be extended with graph tools per plan

- `scripts/lint_wiki.py`
- Health check script; complementary to the graph analysis planned

- `AGENTS.md`
- Universal schema for all AI agents; will need updating when graph layer is added

## Next Steps

**Remaining work (immediate — quality evaluation):**
- Read results from 4 background explore agents (eval-lottery-ticket, eval-llm-reasoning, eval-axi-repo, eval-autoskills) — they may have completed
- If agents didn't complete, manually read the 26 generated wiki pages
- Fetch ground truth for remaining sources: arxiv.org/abs/2512.24601, github.com/kunchenguid/axi README, github.com/midudev/autoskills README
- Compare each wiki page's claims against source material
- Score each ingest on: factual accuracy, completeness of extraction, cross-reference quality, frontmatter compliance, concept coverage
- Synthesize overall quality assessment and identify systematic issues

**Evaluation dimensions to check:**
1. **Factual accuracy** — do claims match the actual paper/repo content?
2. **Completeness** — are key concepts/entities captured or missed?
3. **Cross-references** — do wikilinks connect to real, relevant pages?
4. **Frontmatter compliance** — required fields present per AGENTS.md schema?
5. **Depth** — substantive content or just surface-level summaries?
6. **The 5th source mystery** — check if 2512.24601 generated wiki pages or failed

**Open questions:**
- What paper is arxiv 2512.24601? Need to fetch its abstract
- Why is 2512.24601 missing from log.md despite status: ingested?

## Related Wiki Pages

- [[Labs-Wiki Architecture]]
- [[Graphify Features for Knowledge Graph Integration]]
- [[Quality Evaluation of Auto-Ingested Wiki Content]]
- [[Labs-Wiki]]
- [[AutoSkills]]
- [[Homelab]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-graphify-comparison-and-quality-evaluation-6949c984.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-04-10 |
| URL | N/A |
