---
title: "Full Review: Content, Agent Flow, Graph UI"
type: report
generated: 2026-04-21
reviewer: copilot-cli
scope: "labs-wiki end-to-end review against plans, prior reports, and Karpathy's LLM Wiki gist"
---

# Full Review — labs-wiki

## 1. Method

I read every document in `plans/` and `reports/`, the Karpathy gist (`gist:442a6bf555914893e9891c11519de94f`), `AGENTS.md`, `program.md`, the four core docs (`architecture`, `memory-model`, `workflows`, `live-memory-loop`), and walked the live code in `scripts/`, `wiki-graph-api/`, `wiki-graph-ui/`, and `wiki-ingest-api/`. I then audited the live wiki: 326 concepts, 172 entities, 162 sources, 35 synthesis pages, 89 raw files. I cross-checked tier distribution, quality scores, near-duplicate slugs, lint output, and SSE wiring.

This report names what is working, what has drifted from the plans, and what to do next. It is **report-only** — no wiki pages or scripts were modified.

---

## 2. Where the system is faithful to the plans and to Karpathy

1. **Three-layer split is intact.** `raw/` is immutable, `wiki/` is LLM-owned, `AGENTS.md` is the schema. This is the core Karpathy pattern and it survives.
2. **Provenance is real.** Every wiki page carries `sources:`. `wiki_to_mempalace.py` now also prunes orphans, so the MemPalace mirror does not grow stale on rename/delete.
3. **Source-aware ingest lanes are deployed.** Light / default / vision routing with deterministic `fetched-content` and `extracted-content` blocks matches `copilot-pro-plus-github-models-efficiency.md` and the auto-ingest section of `AGENTS.md`.
4. **Checkpoint policy is more honest.** `knowledge_state` (`planned | executed | validated`), `checkpoint_class`, and `retention_mode` together capture execution posture in a way `quality_score` never could. The April-19 audit and April-20 second curation report drove this in correctly.
5. **Graph layer ships.** Builder, FastAPI service, static UI, Caddy labels, Cloudflare Access, and homepage widget are all live. The "report-only" `checkpoint-graph-tracker.md` is exactly the right shape for evaluating heuristic vs graph signal before changing policy.
6. **Pipeline cost discipline is in place.** `backfill_checkpoint_cluster_synthesis.py` short-circuits on cluster-signature match — no model calls when a cluster already has a synthesis page.

---

## 3. Where the system has drifted from the plans

### 3.1 The wiki has stopped compounding — concept duplication is now a first-class problem

Karpathy's whole thesis is: "the wiki is a persistent, **compounding** artifact. The cross-references are already there. The contradictions have already been flagged." The current corpus violates that in several visible ways:

| Pattern | Examples on disk | Why it matters |
|---|---|---|
| Near-duplicate concepts | `adaboost-adaptive-boosting.md` + `adaboost-algorithm.md`; `atomic-model-artifact-saving-in-ml-training-loops.md` + `atomic-model-artifact-saving-via-atomic-pickle-dump.md` + `atomic-save-pattern-for-model-artifacts.md`; `auto-ingest-pipeline-for-llm-powered-knowledge-wiki.md` + `auto-ingest-pipeline-for-wiki-markdown-processing.md`; `caddy-handle-path-directive-and-its-impact-on-upstream-url-construction.md` + `caddy-handle-path-directive-and-url-token-injection.md`; `autoagent-framework-research.md` + `autoagent-framework-research-integration-planning.md` | Each new ingest is creating a fresh page rather than merging into an existing one. The "compile once, kept current" principle is being broken at the page-creation step. |
| Synthesis dominated by one mechanical pattern | 6 of 35 synthesis pages have titles starting with `Recurring Checkpoint Patterns: ...` | Synthesis was supposed to be cross-cutting topical analysis. It has become a checkpoint-cluster output. |
| Entity duplication via slug variants | `wiki-deduplication-and-concept-merging-in-llm` + `wiki-concept-deduplication-and...`; `worktree-based-debugging-deployment` + `worktree-based-baseline-verification-durable-workflow` + `worktree-based-subagent-driven` | Entity pages drift on minor phrasing. |

This is the same gap the April-10 quality evaluation flagged, the same gap the April-19 audit called "the system is still better at provenance than abstraction," and the same gap the Phase-5 report said the synthesis-first compression step would close. None of those have been actioned in the ingest path itself — the dedupe logic in `auto_ingest.py` (concept matching, fuzzy alias check) clearly is not catching these in practice. The ingest path only hard-rejects byte-identical content; near-duplicates pass through.

### 3.2 `quality_score` is now meaningless

| Bucket | Pages |
|---|---|
| `quality_score: 100` | 324 |
| `quality_score: 95` | 1 |
| `quality_score: 75` | 2 |

`scripts/lint_wiki.py::compute_quality_score` adds 25 for required frontmatter, 25 if any wikilink or `related:` exists, 25 if `sources:` is non-empty, 25 if verified within 90 days. Every auto-ingested page passes all four conditions on day one, so the score is permanently pinned at 100. The April-10 quality evaluation noted "all pages have `quality_score: 0` (not auto-populated)" — the auto-population has since been added, but the rubric was not. The signal has gone from "missing" to "uniform," which is no better.

### 3.3 Tier promotion is essentially broken

| Tier | Pages |
|---|---|
| `hot` | 602 |
| `archive` | 56 |
| `established` | 2 |
| `core` | 0 |
| `workflow` | 0 |

`docs/memory-model.md` defines clear promotion rules (`hot → established` after first verify + `related:` + score ≥ 50; `established → core` at 3+ inbound refs + score ≥ 70). 600 pages sitting in `hot` for weeks means no scheduled promotion job is running, and no agent persona owns the transition. The Curator persona is documented but is not on a recurring loop.

### 3.4 Graph-aware editorial scoring stopped at "tracker"

`reports/checkpoint-graph-tracker.md` is now reporting **22 out of 61 checkpoints in disagreement** between the heuristic baseline and the graph-derived recommendation, with the dominant transition being `compress→keep` (18 of those). The second-curation report explicitly proposed this as "Option 1 — graph-aware recommendation layer." The tracker exists; the reconciliation flow does not. There is no skill, agent, or even a written triage protocol for "review the disagreement table and act on it." The signal is generated and immediately becomes shelf-ware.

### 3.5 Synthesis backfill never finished the corpus

`backfill_checkpoint_cluster_synthesis.py` has been used in surgical mode (community 1 only). The graph tracker shows 6 communities (1, 3, 0, 11, 9, 8) carrying merge-cluster candidates, multiple with no synthesis neighbor. This is the "Phase 5 still open" item the April-19 audit named.

### 3.6 The Graph UI shipped at the MVP floor of the plan, not the target

Compared with `plans/homelab-graph-ui.md` (the explicit spec):

| Plan target | Shipped | Gap |
|---|---|---|
| SvelteKit + `@cosmograph/cosmograph` (WebGL, 1M+ nodes) | Pure Canvas + JS Fruchterman-Reingold | At ~700 nodes the layout is doing O(n²) per iter for 120 iters in JS on every filter change. Mobile is the weakest case. |
| Filters: type, tier, community, **stale-only** | type, tier, search, "highlight cross-community" | No community filter, no stale filter, no checkpoint-class filter |
| "Surprises" toggle | ✅ shipped | OK |
| **Path mode** (click A then B → shortest path) | not implemented | Missing |
| **NL query box** → `/graph/query` | endpoint not implemented in `main.py`, no UI | Missing on both sides |
| SSE live update on `graph-updated` | ✅ wired in `app.js` | Good — verify the full-reload UX is acceptable, otherwise switch to incremental patch |
| Saved views (URL-encoded filter state) | not implemented | Missing |
| MCP surface on the graph API | not implemented | Missing — `wiki_mcp_server.py` is a separate file that does not talk to the graph |

The MVP UI is genuinely usable, and the "ship a static-html-behind-nginx" pragmatism was the right call to get something on the network. But it is now the daily driver, and several of the plan's high-value features are still unbuilt.

### 3.7 Scaffolding documents are out of date

- `tasks/progress.md` still has Tier-1 features tracked as `⬜ Pending` even though all 10 of them are demonstrably shipped.
- `plans/labs-wiki.md` references a four-persona model (`researcher / compiler / curator / auditor`) but the live system uses the seven-agent table in `AGENTS.md`. The two are not reconciled.
- `tasks/lessons.md` is essentially empty (12 lines, no real entries) despite multiple post-incident reports that should have produced lessons.

---

## 4. Recommendations

Ordered by impact-to-effort. Each recommendation names a concrete artifact to change.

### 4.1 Wiki content — stop the compounding leak (highest impact)

**R1. Make ingest dedupe semantic, not syntactic.**
In `scripts/auto_ingest.py`, before creating a new concept page, embed the proposed title + first paragraph and cosine-compare against existing concept pages above a threshold (e.g. 0.82). On hit, route to `wiki-update` flow instead of `wiki-create`. The vector index can live in `wiki-graph-api/.cache/` since the graph builder already has a SHA-keyed cache shape.

**R2. Run a one-shot dedupe sweep on the existing corpus.**
Write `scripts/dedupe_concepts.py` that:

1. embeds every concept + entity title and the first 500 chars of body,
2. clusters at cosine ≥ 0.85,
3. emits a report of merge candidates to `reports/dedupe-candidates-2026-04-21.md` (do not auto-merge).

Then run `wiki-update` against accepted clusters with the older page winning the slug and the newer page's content merged under a "Sources" subsection. The visible target list to seed this on: `adaboost*`, `atomic-*model*save*`, `auto-ingest-pipeline-*`, `caddy-handle-path-*`, `autoagent-*`, `worktree-based-*`, `walk-forward-*`.

**R3. Replace the binary quality rubric.**
Rewrite `compute_quality_score` to produce a real distribution. Suggested signals:

- inbound wikilink count (graph degree from `graph.json`)
- outbound wikilink count
- body length within target band (700–4000 words gets full credit)
- has at least one specific, citable claim (regex for numbers, code blocks, or block-quoted lines)
- `sources:` count
- staleness curve from `docs/memory-model.md`
- `knowledge_state` for checkpoints (validated > executed > planned)

This restores the differentiation Karpathy assumes when he says "good answers can be filed back as wiki pages." Right now the system can't tell a thin entity stub from a 6-source synthesis.

**R4. Restart synthesis backfill, all communities.**
Run `backfill_checkpoint_cluster_synthesis.py` on all communities listed in the merge-cluster section of `reports/checkpoint-graph-tracker.md`, not just community 1. This was the open item in `checkpoint-curation-phase5-report.md` and the April-19 audit.

**R5. Demote synthesis-by-checkpoint pattern.**
Either (a) move `Recurring Checkpoint Patterns: *` pages out of `wiki/synthesis/` into `wiki/sources/cluster-summaries/`, or (b) re-author them as topical syntheses (e.g. "Recurring Pipeline-Resilience Patterns" instead of "Recurring Checkpoint Patterns: ..."). The current naming is leaking the source mechanism into a layer that should be topic-shaped.

### 4.2 Agent flow / processes (medium-high impact)

**R6. Wire the graph tracker into a recurring agent action.**
Add `/wiki-orchestrate triage-graph-disagreements` (or extend the `maintenance` mode). On run, read `reports/checkpoint-graph-tracker.md`, present each `compress→keep` and `keep→compress` row, and ask the user to ratify. Apply the ratified change and update both `retention_mode` and `tier`. Log to `wiki/log.md`. This converts the existing read-only signal into actual editorial movement and is the cheapest route to closing 22 stale disagreements.

**R7. Build the Curator promotion cron.**
Add a daily run (cron on the homelab) of `scripts/promote_tiers.py` (new) that applies the `docs/memory-model.md` rules:

- `hot → established` when `last_verified` exists and inbound degree ≥ 1
- `established → core` at inbound degree ≥ 3 and `quality_score ≥ 70` (after R3 makes the score meaningful)

Without this, the four-tier model in the docs is fiction. The current 602/2/0/0 distribution proves the rules are unenforced.

**R8. Reconcile the agent persona docs.**
Pick one model. Either (a) keep the seven Copilot agents in `.github/agents/` and delete the four-persona section from `plans/labs-wiki.md`, or (b) collapse the seven into the four conceptual roles. Right now both exist and any new agent author has to guess which to extend. Recommend (a) — the seven-agent set matches what's live.

**R9. Make `tasks/lessons.md` an artifact agents actually write to.**
Add a post-task hook in `AGENTS.md` that requires any agent finishing a debugging session to append a lesson entry following `.github/context/lesson-format.md`. The April-19 audit, the second-curation script bug, and the URL-raw preservation pilot were all worth a lesson and none of them produced one.

**R10. Update `tasks/progress.md` or retire it.**
The Tier-1 / Tier-2 / Tier-3 tracker is stale (Tier-1 marked pending while shipped). Either flip it to current state in one pass, or delete it and let `wiki/log.md` + `reports/` be the only progress surface.

**R11. Add a "stop creating new concept pages this session" guardrail.**
For sessions where a user is drilling on one topic, the ingest agent should be configurable to **only update existing pages**, never create. This matches Karpathy's posture ("the LLM does the bookkeeping, you guide the topic") and prevents another wave of `concept-x-variant-y.md` files.

### 4.3 Graph UI (medium impact)

**R12. Ship the missing filter set.**
Add `community`, `tier`, `checkpoint_class`, and `stale-only` filters. These are all already in the node frontmatter — the work is purely UI. Highest user value: `stale-only` directly surfaces the work the Curator should be doing.

**R13. Implement path mode.**
Two-click path selection: select node A, select node B, draw shortest path on the graph. The graph API has all the data; this is a BFS in `app.js` and one extra render pass. Useful for "how does concept X relate to concept Y" — the question Karpathy explicitly calls out as the wiki's superpower.

**R14. Add the NL query endpoint and box.**
Implement `POST /graph/query` in `wiki-graph-api/main.py`: take a natural-language query, embed it, return the top-K nodes plus their neighborhood as a subgraph JSON. UI renders the subgraph in place. This unblocks the "ask the graph" workflow that's been promised since `graphify-integration.md`.

**R15. Decide on Cosmograph vs current Canvas.**
At 700 nodes the current Fruchterman-Reingold layout takes a visible second on every filter change. At 1500–2000 nodes (which is the trajectory) the UX will degrade to "wait and stare." Either:

- swap renderer to `@cosmograph/cosmograph` per the original plan, or
- precompute the layout server-side once per rebuild (positions in `graph.json`) so the client only does pan/zoom.

Recommend the precompute path first — much smaller change, keeps the dependency-free static-image story, and removes the per-filter relayout cost.

**R16. Expose the graph as MCP tools.**
The plan promised `wiki_graph_neighbors`, `wiki_graph_shortest_path`, `wiki_graph_communities`, `wiki_graph_god_nodes`, `wiki_graph_surprises` over SSE/MCP. `scripts/wiki_mcp_server.py` exists but does not talk to the graph API. Either fold the graph tools into that server or add a `/mcp` endpoint to `wiki-graph-api/main.py`. This is the single biggest unlock for in-IDE wiki use.

**R17. Add a "checkpoint health" view.**
A dedicated UI mode that overlays `reports/checkpoint-graph-tracker.md` data on the graph: color nodes by `class`, highlight disagreement rows, allow click-to-ratify. Pairs directly with R6.

### 4.4 Cross-cutting

**R18. Add an end-to-end ingest evaluation harness.**
The April-10 evaluation was hand-graded against five sources. Make it a script: take a known-good source, run ingest, diff against a fixture wiki page, score on (concept count, broken-link count, accurate-date check, entity completeness). Run weekly. Regression-test the pipeline the same way the rest of the homelab is tested.

**R19. Track wiki growth as a metric, not just a count.**
Add to `wiki-graph-api/main.py`: `/graph/health` returning {orphan count, broken-link count, dedupe-candidate count, avg quality score, tier distribution, hot-page age p50/p95}. Surface in the homepage widget. Today these numbers can only be hand-computed.

---

## 5. Bottom line

**What is true:** the architecture matches the plans, the pipeline is operational, the graph and the editorial-state work that landed in the April-19 audit and the April-20 second curation are real progress.

**What is also true:** the wiki is starting to behave like an append-only log of pages rather than a compounding artifact. The dedupe path is not catching real duplicates, the quality score has lost its signal, tier promotion is unenforced, the graph-derived editorial recommendations are read-only, and the Graph UI shipped its MVP and stopped.

**Three actions that close the largest gaps:**

1. **R1 + R2** — semantic dedupe in the ingest path, plus a one-shot sweep of the existing corpus. This is the single most Karpathy-faithful change available.
2. **R6 + R7** — turn the graph tracker into an editorial action, and run a daily tier-promotion cron. This makes the existing memory model real instead of aspirational.
3. **R12 + R13 + R16** — finish the Graph UI to the spec it was planned at (filters, path mode, MCP tools). The infrastructure is already paid for.

If only one of those three is done, do the first.
