---
title: "Copilot Session Checkpoint: labs-wiki full review report"
type: text
captured: 2026-04-22T01:18:45.642126Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki, mempalace, graph, agents]
checkpoint_class: durable-architecture
checkpoint_class_rule: "body:graph-api"
retention_mode: retain
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** labs-wiki full review report
**Session ID:** `2546cc45-af25-449e-b2c3-e9f68612693d`
**Checkpoint file:** `/home/jbl/.copilot/session-state/2546cc45-af25-449e-b2c3-e9f68612693d/checkpoints/001-labs-wiki-full-review-report.md`
**Checkpoint timestamp:** 2026-04-22T01:11:03.491506Z
**Exported:** 2026-04-22T01:18:45.642126Z
**Checkpoint class:** `durable-architecture` (rule: `body:graph-api`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user requested a full review of the labs-wiki project — code, functionality, plans, prior reports, and Karpathy's LLM Wiki gist — to produce a summary report and recommendations covering wiki content, agent flow/processes, and graph UI. The output was a single markdown report saved under `labs-wiki/reports/`. The work was read-only: no source code, scripts, or wiki pages were modified.
</overview>

<history>
1. The user asked for a full review of labs-wiki against its plans, reports, and Karpathy's gist, with a written summary and recommendations.
   - Explored repo structure: `plans/` (17 docs), `reports/` (4 prior), `docs/`, `scripts/`, `wiki-graph-api/`, `wiki-graph-ui/`, `wiki-ingest-api/`, `wiki/` (326 concepts, 172 entities, 162 sources, 35 synthesis, 89 raw).
   - Read README, AGENTS.md, program.md, key plans (labs-wiki, homelab-graph-ui, copilot-session-wiki-memory-audit-2026-04-19, quality-evaluation-2026-04-10, second-curation-report-2026-04-20, wiki-audit-followups-summary-2026-04-20, checkpoint-curation-phase5-report), reports (checkpoint-graph-tracker, url-raw-*).
   - Fetched Karpathy's gist (gist:442a6bf555914893e9891c11519de94f) for the canonical pattern.
   - Audited live state: tier distribution (602 hot / 56 archive / 2 established / 0 core), quality_score distribution (324 of 327 concepts at 100), near-duplicate concept slugs (adaboost x2, atomic-save x3, auto-ingest x2, caddy-handle-path x2, autoagent x2, worktree-* x3), synthesis composition (6 of 35 are "Recurring Checkpoint Patterns: ..."), SSE wiring confirmed in `app.js`, lint scoring rubric inspected.
   - Queried MemPalace `labs_wiki` wing for prior context on graph UI / dedup / agent flow.
   - Wrote the final report at `reports/full-review-2026-04-21.md`.
</history>

<work_done>
Files created:
- `/home/jbl/projects/labs-wiki/reports/full-review-2026-04-21.md` — the deliverable. ~17.8 KB. Sections: Method, What's faithful to the plans, Where the system has drifted, 19 numbered recommendations (R1–R19) bucketed into Wiki content / Agent flow / Graph UI / Cross-cutting, and Bottom line with three priority actions.

Work completed:
- [x] Repo + plans + reports + docs survey
- [x] Karpathy gist read
- [x] Live wiki audit (tiers, scores, dupes, synthesis composition)
- [x] Code review of `auto_ingest.py`, `lint_wiki.py`, `graph_builder.py`, `wiki-graph-api/main.py`, `wiki-graph-ui/{app.js,index.html}`
- [x] MemPalace recall for prior session context
- [x] Final report written and saved
</work_done>

<technical_details>
Key findings driving the recommendations:
- **Quality score is broken**: `scripts/lint_wiki.py::compute_quality_score` is a binary 4×25 rubric; every auto-ingested page satisfies all four conditions on day one → 324/327 concepts pinned at 100. Differentiation is gone (April-10 eval said "stuck at 0," April-21 says "stuck at 100" — same problem inverted).
- **Tier promotion unenforced**: `docs/memory-model.md` defines hot→established→core rules but no cron/agent runs them. 602 pages stuck in `hot`, only 2 `established`, 0 `core`.
- **Dedupe leak in ingest**: `auto_ingest.py` has fuzzy matching (rapidfuzz optional) but only blocks byte-identical content. Real near-duplicates (adaboost-adaptive-boosting vs adaboost-algorithm) pass through.
- **Graph tracker is shelf-ware**: `reports/checkpoint-graph-tracker.md` shows 22/61 disagreements (18 compress→keep, 4 keep→compress) with no skill, agent, or protocol for triage. Generated on every graph build but never acted on.
- **Synthesis colonized by checkpoints**: 6 of 35 synthesis pages titled `Recurring Checkpoint Patterns: ...` — synthesis layer is leaking source mechanism instead of being topic-shaped.
- **Graph UI shipped MVP only**: pure Canvas + JS Fruchterman-Reingold (O(n²) per iteration × 120 iterations on every filter change at ~700 nodes); plan called for SvelteKit + Cosmograph. Missing: community filter, stale-only filter, path mode, NL query box, MCP surface, saved views.
- **SSE works**: `EventSource(/events)` listens for `graph-updated`, calls `loadGraph()` on event. Full reload, not incremental.
- **`tasks/progress.md` is stale**: Tier-1 features marked `⬜ Pending` despite being shipped.
- **`tasks/lessons.md` is empty** (12 lines, no real entries) despite multiple post-incident reports that should have produced lessons.
- **Agent persona docs conflict**: `plans/labs-wiki.md` describes 4 personas (researcher/compiler/curator/auditor); `AGENTS.md` lists 7 (`.github/agents/wiki-*`). Recommended keeping the 7.
- **`scripts/wiki_mcp_server.py`** exists but does not talk to the graph API — graph MCP tools promised in `plans/homelab-graph-ui.md` are unbuilt.
- **Knowledge state work landed correctly**: April-19 audit added `knowledge_state: planned|executed|validated`, April-20 second curation extended; `wiki_to_mempalace.py` now prunes orphans. These changes are sound and should be preserved.
</technical_details>

<important_files>
- `/home/jbl/projects/labs-wiki/reports/full-review-2026-04-21.md`
  - The deliverable. Structured as: §1 Method, §2 Where faithful, §3 Where drifted (3.1–3.7), §4 Recommendations R1–R19, §5 Bottom line with 3 priority pairs.
  - Top priorities flagged: R1+R2 (semantic dedupe + sweep), R6+R7 (graph tracker → editorial action + tier-promotion cron), R12+R13+R16 (Graph UI filters + path mode + MCP).
- `/home/jbl/projects/labs-wiki/AGENTS.md`
  - The Layer-3 schema. Defines 7 agent personas, validation rules, workflows.
- `/home/jbl/projects/labs-wiki/scripts/auto_ingest.py` (3254 lines)
  - Ingest pipeline. Site of the dedupe leak (R1). Already does source-aware model routing and `knowledge_state` stamping.
- `/home/jbl/projects/labs-wiki/scripts/lint_wiki.py` lines 85–110
  - The broken `compute_quality_score`. Target of R3.
- `/home/jbl/projects/labs-wiki/wiki-graph-api/{graph_builder.py,main.py}`
  - Graph backend. Missing `/graph/query` (R14), `/graph/health` (R19), MCP surface (R16).
- `/home/jbl/projects/labs-wiki/wiki-graph-ui/app.js` (633 lines)
  - Static Canvas UI. Force-directed layout at lines 73–121, SSE at the bottom. Targets of R12–R15.
- `/home/jbl/projects/labs-wiki/reports/checkpoint-graph-tracker.md`
  - Auto-generated read-only artifact. 22/61 disagreements awaiting triage. Drives R6.
- `/home/jbl/projects/labs-wiki/plans/homelab-graph-ui.md`
  - Original Graph UI spec — gap between plan and shipped UI is the basis for R12–R17.
- `/home/jbl/projects/labs-wiki/plans/copilot-session-wiki-memory-audit-2026-04-19.md` and `plans/second-curation-report-2026-04-20.md`
  - Most recent prior reports. Established the editorial-state work that landed correctly and named the still-open items (synthesis backfill, graph-aware editorial scoring) that R4 and R6 close.
</important_files>

<next_steps>
The user's request is fully complete — the review report has been written and saved to `reports/full-review-2026-04-21.md`. No further action is required unless the user wants to:
- Begin executing one of the recommendations (R1+R2 semantic dedupe is the highest-impact starting point).
- File the report itself back into the wiki via the auto-ingest path.
- Update `tasks/progress.md` (R10) or seed `tasks/lessons.md` (R9) as a follow-up housekeeping pass.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
