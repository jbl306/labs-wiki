---
title: "Memory Stack Recall Strategy: MemPalace vs Labs-Wiki for Cross-Session Project Recall"
date: 2026-04-24
author: copilot-cli (Claude Opus 4.7)
type: report
tags: [memory, mempalace, labs-wiki, agent-instructions, context-engineering]
---

# Memory Stack Recall Strategy

**Question:** With MemPalace already mining labs-wiki, should agent sessions (copilot-cli, opencode) depend solely on MemPalace MCP for cross-session project recall, or should agent instructions also wire in the labs-wiki index? Goal: effective recall without context rot.

**Answer (TL;DR):** Keep MemPalace as the **primary** recall mechanism in agent instructions (already wired). Add labs-wiki MCP as an **opt-in semantic library** — instruct agents to call `wiki_search`/`wiki_read` *on demand* for synthesized cross-project knowledge. Do **not** preload any wiki page list or index into hot-tier instructions. The two systems are complementary, not duplicative, and the natural division maps cleanly onto a three-tier memory model.

---

## 1. The two systems do different jobs

| Property | MemPalace | Labs-Wiki |
|---|---|---|
| Storage unit | Drawer (verbatim chunk, ~500 tokens) | Markdown page (concept / synthesis / source) |
| Total volume | 34,492 drawers across 10 wings | 790 curated pages |
| Retrieval | ChromaDB vector search + knowledge graph | Full-text search + direct page read |
| Authority | Episodic — what was said/done, in order | Semantic — distilled, deduped, synthesized |
| Temporal model | KG with `valid_from` / `invalidate` | Static markdown (frontmatter dates) |
| Per-call payload | 3 chunks (~1–2KB) tightly scoped by wing | Page list w/ leads (search) or full page (read) |
| Best for | "What did I decide on X?" "Who is Y?" "What broke last time?" | "What's the pattern across projects?" "What's the canonical write-up of Z?" |

MemPalace is **working + episodic memory** (raw, chronological, ever-growing). Labs-wiki is **semantic memory** (curated knowledge pages, the distilled output of mining episodic data). Critically, labs-wiki ingests *from* MemPalace and other raw sources — they aren't redundant; one is the kitchen, the other is the cookbook.

---

## 2. Use-case tests

Three project-recall queries, run against both systems back-to-back. Wing scoping applied to MemPalace where relevant.

### Test A — NBA-ML architecture decisions (timescale, training)

| System | Top hit | Verdict |
|---|---|---|
| MemPalace (`wing=nba_ml_engine`) | Verbatim excerpt of `comprehensive-ml-review_0324.md` — 12-layer audit, B grade, exact methodology line | ✅ Direct episodic recall — exactly the doc you'd want pasted into context |
| Labs-Wiki | Distilled `Copilot Session Checkpoint: Sprint 10` source pages with **decision-grade bullets**: two-repo split, quantile crossing fix (`np.min(np.stack(...))`), Optuna warmstart pattern | ✅ Cross-session synthesis surfaced patterns MemPalace returned only as raw chunks |

**Insight:** MemPalace gave the *document*; labs-wiki gave the *lessons* extracted from many such documents. Both useful, different shapes.

### Test B — Homelab Caddy reverse proxy

| System | Top hit | Verdict |
|---|---|---|
| MemPalace (`wing=homelab`) | Server inventory block (Beelink GTi13, IP, paths) + plan doc preamble | ✅ Context-establishing facts |
| Labs-Wiki | Concept page on `Caddy handle_path Directive and Its Impact on Upstream URL Construction` + synthesis page on **recurring** Caddy/handle_path failure patterns across projects | ✅✅ Synthesis is gold — captures cross-incident pattern MemPalace can't articulate |

**Insight:** For "have I hit this class of bug before?" questions, labs-wiki **synthesis** pages outperform raw MemPalace search. The synthesis layer is doing real work.

### Test C — Debrid / Real-Debrid / Torrentio (cross-project: debrid-downloader + homelab)

| System | Top hit | Verdict |
|---|---|---|
| MemPalace (no wing filter) | Mixed wings — debrid-first vs broadcaster-extractor synthesis (already lives in `labs_wiki` wing) + Knightcrawler plan from `homelab` wing | ⚠️ Returned wiki content via mining — meaning MemPalace is partially redundant for synthesized material |
| Labs-Wiki | Direct concept pages: `Real-Debrid InstantAvailability API and Playback Issues`, `Broadcaster Extractor Fallback`, `Anonymous Token to IP-Bound Manifest Handoff` — all linked, all distilled | ✅ Native habitat for this content |

**Insight:** MemPalace's `labs_wiki` wing (2,231 drawers) is essentially a vectorized mirror of the wiki. For synthesized topics, going to the wiki MCP directly is **higher fidelity** (full page > 500-token chunk) and avoids the "MemPalace returns a chopped version of the same wiki page" failure mode.

---

## 3. Failure modes if you pick wrong

### Mode 1: "MemPalace only" — what you lose
- Synthesis pages get chunked into drawers, losing the cross-cutting structure (entity links, comparison tables).
- Concept pages return as 500-token slices instead of complete write-ups.
- No way to *list* what knowledge exists on a topic — vector search returns the top-k it thinks match, you can't browse.

### Mode 2: "Wire labs-wiki page list into instructions" — context rot
- 790 pages × ~50 chars title + path = ~40KB just for the list. Burns through context budget for every session.
- Agent doesn't actually need to *know* the pages exist; it just needs to know the MCP exists and when to call it.
- Even a partial index biases the agent toward listed pages and away from MemPalace's stronger tools (KG, diary, wing-scoped search).

### Mode 3: "Use both blindly on every query" — duplication + noise
- Many topics return overlapping content (labs-wiki sources cite copilot session checkpoints which MemPalace also stored).
- Agent context fills with near-duplicates → harder to reason, slower turns.

---

## 4. Recommended division of labor

Three-tier recall, mapped to existing infrastructure:

```
TIER 1 — Hot context (always loaded)
  • .github/copilot-instructions.md (workspace constitution)
  • Project inventory, conventions, MCP server registry
  • Pointer: "MemPalace = episodic, Labs-Wiki = semantic"

TIER 2 — Episodic recall (per-session, default)
  • mempalace_status (once)
  • mempalace_search (wing-scoped) for the user's topic
  • mempalace_kg_query for any named entity
  • mempalace_diary_write at session end

TIER 3 — Semantic library (on-demand, opt-in)
  • wiki_search BEFORE doing fresh research on any cross-cutting topic
  • wiki_read for the full canonical write-up of a concept
  • Skip entirely for tasks that are purely "what did we just do" (Tier 2 covers it)
```

### Decision rule for the agent

> **"Did this question span more than one project, or is it asking about a *pattern* / *concept* / *comparison*?"**
>
> - **No** (single-project, episodic, "what did we decide", "who", "when"): MemPalace only.
> - **Yes** (cross-project, conceptual, "why does X always fail", "how does Y compare to Z"): MemPalace for context + `wiki_search` for the synthesis page.

### What to add to `copilot-instructions.md` / `AGENTS.md`

Append to the MCP guidance section (one paragraph, no page list):

```
**Labs-Wiki guidance:** Before doing fresh research on any
cross-project topic, pattern, or concept, call `wiki_search` —
the wiki may already contain a distilled synthesis page. Use
`wiki_read` for the canonical full write-up. For per-session
episodic recall (decisions, who-said-what, recent changes),
prefer MemPalace; the wiki is for *concepts that have been
deliberately compiled*, not the raw stream.
```

This is ~70 tokens of permanent context — a rounding error against the recall quality it unlocks.

---

## 5. Bonus: stop the drift

MemPalace's `labs_wiki` wing has 2,231 drawers — it's chunking the wiki into vector storage. Two failure modes to watch:

1. **Drift** — wiki pages get edited; MemPalace drawers don't auto-invalidate. Truth diverges silently.
2. **Duplication** — you query "torrentio cache issue" and get the same paragraph back from both systems.

**Recommendations:**
- Treat `labs_wiki` and `labs_wiki_knowledge` wings in MemPalace as **build artifacts**, not source of truth. When in doubt, `wiki_read` the actual file.
- Add a periodic re-ingest job (or hook into wiki updates) so MemPalace's mirror stays fresh — or, simpler, instruct agents to prefer `wiki_search` over MemPalace search when filters would route to the `labs_wiki` wing anyway.
- Keep authoring synthesis in the wiki. Keep authoring session diaries / KG facts in MemPalace. Don't cross the streams.

---

## 6. Action items

1. **Append the Labs-Wiki guidance paragraph** above to `~/.github/copilot-instructions.md` (Hot tier) and `~/projects/*/AGENTS.md` where applicable.
2. **Do not** add wiki page lists or topic indexes to any instruction file.
3. **Keep** MemPalace session-start protocol unchanged — it's the right episodic anchor.
4. **Add a lesson** to a relevant `tasks/lessons.md`: "When two memory systems return overlapping content, prefer the system that authored it (wiki for concepts, MemPalace for sessions)."
5. **Optional:** schedule a monthly `wiki_list` audit so the agent learns what categories exist (load *only* during periodic review sessions, never default).

---

## Verdict

> **Use MemPalace by default. Reach for labs-wiki on demand. Never index either into hot context.**

The complementary architecture is already in place — the only change needed is a 70-token instruction addendum telling agents *when* to choose the wiki MCP. Doing more than that re-introduces the very context rot you're trying to avoid.
