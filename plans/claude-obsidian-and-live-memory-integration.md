# Claude-Obsidian Integration + Live MemPalace Memory (No LLM Key)

> **Goal:** Fold the best ideas from [AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) into labs-wiki, and replace the weekly MemPalace cron with a near-real-time, LLM-key-free update loop that works across VS Code Copilot, Copilot CLI, and OpenCode.
>
> **Sibling plans:**
> - [labs-wiki.md](labs-wiki.md) — core wiki architecture
> - [graphify-integration.md](graphify-integration.md) — graph layer
> - [mempalace-next-steps.md](mempalace-next-steps.md) — current cron-based mining

---

## Part 1 — What to Steal from claude-obsidian

claude-obsidian (1.6k stars) is Karpathy-wiki-pattern turned into a polished Obsidian vault with 10 skills, hot cache, contradiction flagging, and autoresearch. Labs-wiki already has most of the compilation pipeline; claude-obsidian has the **retrieval UX, session continuity, and cross-project reuse** patterns we lack.

### Feature adoption matrix

| # | Feature | claude-obsidian pattern | Value for labs-wiki | Priority |
|---|---------|-------------------------|---------------------|---------:|
| 1 | **`wiki/hot.md` session cache** | Single file updated every session end with "what's recent + what matters now". First file every agent reads. | Replaces per-session memory loss. Works across Copilot CLI, VS Code, OpenCode without any MCP call. | **P0** |
| 2 | **SessionStart + Stop hooks (`hooks/hooks.json`)** | Auto-refresh hot cache at session start; append summary at stop. | Direct blueprint for Copilot CLI + VS Code equivalents (see Part 2). | **P0** |
| 3 | **Cross-project "power move" CLAUDE.md snippet** | Any project's instructions point agents at the central vault with a read-order (hot.md → index.md → domain sub-index → specific page). | Gives every one of your 11 projects free access to the wiki without duplicating content. | **P0** |
| 4 | **`/save` skill** | Files the current conversation as a wiki note with auto-naming, frontmatter, cross-references. | Converts ephemeral chat into durable knowledge. Complements MemPalace drawers with richer markdown. | **P0** |
| 5 | **`/autoresearch` configurable program** | 3-round research loop (search → fetch → synthesize → file) with `program.md` controlling sources, confidence rules, max rounds. | Turns labs-wiki from a passive sink into an active researcher. program.md = domain-tunable research agent. | **P1** |
| 6 | **Contradiction flagging (`[!contradiction]` callouts)** | Lint surfaces conflicting claims across pages with source citations. | Raises wiki trustworthiness. Easy bolt-on to existing `lint_wiki.py`. | **P1** |
| 7 | **Hot cache + lint + ingest as one "wiki mode"** | Six wiki modes (Website / GitHub / Business / Personal / Research / Book) with tailored scaffolds. | Labs-wiki is currently "Personal + Research" only. Adding "GitHub" mode gives every code project a first-class wiki scaffold. | **P1** |
| 8 | **Seeded vault** | Ships with example concept/entity pages so graph view looks alive on first open. | Makes the "clone and go" story real for anyone forking the repo. | **P2** |
| 9 | **Obsidian Bases dashboard (`wiki/meta/dashboard.base`)** | Native Obsidian v1.9.10+ database view over the vault — replaces Dataview. | Zero-JS, native UI for browsing wiki pages by tier/type/quality/staleness. | **P2** |
| 10 | **Batch ingestion via parallel subagents** | `ingest all of these` spawns N parallel agents, then reconciles cross-references in a final pass. | Much faster bulk ingestion. Fits our existing `scripts/auto_ingest.py` — just parallelize over files. | **P2** |
| 11 | **Banner / canvas / color-coded CSS** | Visual polish — full-width banners, Wiki Map canvas, 3-color explorer CSS. | Optional aesthetic upgrade. Our vault is already Obsidian-compatible; these are two hours of config. | **P3** |
| 12 | **Plugin distribution** | Published as Claude plugin marketplace entry. | Not useful for a private repo. Skip. | **Skip** |

### What labs-wiki already has (don't re-build)

| claude-obsidian feature | Labs-wiki equivalent |
|-------------------------|----------------------|
| Ingest skill → wiki pages | `scripts/auto_ingest.py` + `wiki-ingest-api/` (Docker) |
| Index + log | `wiki/index.md` + `wiki/log.md` |
| Lint | `scripts/lint_wiki.py` (quality + staleness + orphans) |
| MCP for vault | `scripts/wiki_mcp_server.py` |
| Frontmatter standards | Already richer (source_hash, quality_score, tier, provenance) |
| Graph view | Obsidian reads our `[[wikilinks]]` natively; graphify-integration.md extends this |

---

## Part 2 — Live MemPalace Updates (No LLM Key)

### Current state

`homelab/scripts/mempalace-remine.sh` runs **weekly** (Sunday 3am) via cron and re-mines homelab + labs-wiki + nba-ml-engine + Copilot CLI session-state + wiki pages. This has two problems:

1. **Staleness window up to 7 days** — a decision made Monday isn't in MemPalace search results until the following Sunday.
2. **No mid-session capture** — nothing snapshots context before auto-compact at 95% tokens.

### Why "no LLM key" is fine

MemPalace mining is **pure file indexing**: SHA hashing, markdown parsing, drawer generation, embedding into ChromaDB (which uses a local sentence-transformers model, not OpenAI/Anthropic). `mempalace mine` does not call any paid model. The "LLM key only" constraint (GitHub Copilot Pro+) simply means we can't spawn an LLM agent from inside a hook — but indexing, re-mining, and cache generation don't need one.

### What this Copilot CLI runtime gives us

Validated against the current runtime plus installed hook tooling (2026-04-18):

| Capability | Copilot CLI (this environment) | Why it matters |
|------------|--------------------------------|----------------|
| SessionStart hook | ✅ observed in `events.jsonl`; installed plugins use `hooks/hooks.json` | Good place to write a tiny project-scoped "session opened" note or refresh hot context |
| Stop / SessionEnd hook | ✅ hook tooling supports it; runtime also emitted `agentStop` events | Good place for lightweight handoff notes |
| PreCompact hook | ⚠ documented by installed hook tooling, but not yet observed firing in this session | Use opportunistically if reliable; do not make the pipeline depend on it |
| Session state on disk | ✅ `~/.copilot/session-state/` with `events.jsonl`, `checkpoints/*.md`, `plan.md` | Canonical local source of session artifacts |
| Compaction summary artifact | ✅ `session.compaction_complete` carries `summaryContent`, `checkpointPath`, and checkpoint number | Best durable summary source for wiki promotion |
| Slash commands / skills | ✅ | Manual save fallback when a user wants explicit capture |
| MCP server / local tooling | ✅ | Lets the watcher, MemPalace, and wiki pipeline stay local-first |

**Revised conclusion:** Copilot CLI is better than "no hooks," but the safest durable artifact is still the **official compaction/checkpoint summary**, not a homegrown event-log synthesis.

Recommended layering:

1. **User-level hook pack** (all projects) writes small project-scoped pre-capture markdowns on `SessionStart` and stop-like events (`agentStop` / `SessionEnd`).
2. **Optional `PreCompact` hook** writes an extra pre-summary note only if it proves reliable in this runtime.
3. **External watcher + curator** continue to promote official checkpoint markdowns or `session.compaction_complete.summaryContent` into `labs-wiki/raw/`.
4. **`/wiki-save`** remains the manual override when the user wants immediate explicit filing.

This means hooks should **augment** checkpoint promotion, not replace it.

### Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                     LIVE MEMPALACE UPDATE LOOP                        │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Copilot CLI    │     │  VS Code Copilot│     │    OpenCode     │
│  session-state  │     │  workspace      │     │  session logs   │
│  ~/.copilot/    │     │  storage        │     │  ~/.opencode/   │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │ inotify             │ inotify                │ inotify
         └──────────┬──────────┴────────────────────────┘
                    │
          ┌─────────▼──────────┐
          │ mempalace-watcher  │  ← systemd user service (NEW)
          │  Python/inotify    │     debounced: 60s quiet window
          │  no LLM calls      │     skips unchanged files via hash
          └─────────┬──────────┘
                    │
          ┌─────────▼──────────┐
          │ mempalace mine     │  ← local ChromaDB + local embedder
          │ --wing <auto>      │     no API keys needed
          └─────────┬──────────┘
                    │
          ┌─────────▼──────────┐
          │ hot.md regenerator │  ← pure Python, no LLM
          │  scripts/          │     mempalace_search top-N + git log
          │    build_hot.py    │     + recent raw/ + recent wiki edits
          └─────────┬──────────┘
                    │
          ┌─────────▼──────────┐
          │ wiki/hot.md        │  ← loaded by every session everywhere
          │  (600-800 tokens)  │     via AGENTS.md pointer
          └────────────────────┘

At session start (any client):
   AGENTS.md says: "Read labs-wiki/wiki/hot.md first, then mempalace_search"

At mid-session:
   User: "/wiki-save this conversation as <name>"
   → skill uses current agent tokens, writes markdown to labs-wiki/raw/
   → watcher picks it up, mines into MemPalace within 60s
```

### Component specs

#### 2.1 `mempalace-watcher` systemd user service (P0)

Python script using `watchdog` (inotify on Linux). Subscribes to:

- `~/.copilot/session-state/` — every Copilot CLI session write
- `~/.opencode/` — OpenCode session logs (when present)
- `~/projects/labs-wiki/raw/` — new sources from capture channels
- `~/projects/labs-wiki/wiki/` — wiki page changes

Behavior:

- Debounce window: 60 seconds of quiet before re-mine fires (prevents thrashing during active typing).
- Per-path wing routing: reuses the same wing names as `mempalace-remine.sh`.
- On mine completion, triggers `scripts/build_hot.py` to refresh `wiki/hot.md`.
- Logs to `~/logs/mempalace-watcher.log` with rotation.
- Runs as **systemd --user** service (no root, survives logout via `loginctl enable-linger`).

Deliverables:

```
homelab/scripts/
  mempalace-watcher.py              # watchdog + debounce + mine dispatch
  mempalace-watcher.service         # systemd unit (user scope)
homelab/scripts/mempalace-remine.sh  # KEPT as weekly full-sweep safety net (cron stays)
```

#### 2.2 `wiki/hot.md` generator (P0)

`labs-wiki/scripts/build_hot.py` — no LLM, pure heuristics:

1. Last 10 wiki pages modified (from git log of `wiki/`).
2. Last 10 raw/ sources captured (from filesystem mtime).
3. Top 5 MemPalace drawers from the last 7 days per active wing.
4. Any wiki page with `tier: hot` in frontmatter.
5. Latest entry from each project's `tasks/todo.md` (in-progress items).

Output: `wiki/hot.md` (~600–800 tokens), frontmatter:

```yaml
---
generated: 2026-04-17T12:34:00Z
generator: scripts/build_hot.py
ttl_hours: 24
---
```

Triggered by: watcher (after any mine), cron (hourly failsafe), manually via `/wiki-refresh-hot`.

#### 2.3 AGENTS.md cross-project snippet (P0)

Drop this into **every project's root `AGENTS.md`** (add to `.github/copilot-instructions.md` and `opencode.json` via `setup.sh`):

```markdown
## Knowledge Base (labs-wiki + MemPalace)

Before answering domain questions, consume context in this order (cheapest first):

1. Read `~/projects/labs-wiki/wiki/hot.md` — recent context, ~600 tokens.
2. If still short, `mempalace_search(query=<topic>, wing=<project_wing>)`.
3. If wiki-relevant, read `~/projects/labs-wiki/wiki/index.md`, then the specific page.
4. Only web-search if the wiki doesn't cover it.

Do NOT read the wiki for unrelated generic coding questions.
```

This mirrors claude-obsidian's "Cross-Project Power Move" and makes all three clients (Copilot CLI, VS Code, OpenCode) behave identically.

#### 2.4 User-invoked skills (P0 / P1)

Four new skills that act as manual hook substitutes. Authored once in `.github/skills/`, symlinked to `.opencode/skills/`:

| Skill | Replaces | Action | LLM cost |
|-------|----------|--------|----------|
| `/wiki-save` (P0) | Stop hook | Writes current conversation as `raw/YYYY-MM-DD-<slug>.md`; watcher then auto-mines. | Current session tokens only (no extra API key). |
| `/wiki-refresh-hot` (P0) | SessionStart hook | Runs `scripts/build_hot.py`; agent reads result. | Zero (pure script). |
| `/wiki-save-before-compact` (P1) | PreCompact hook | Agent snapshots current task state into a drawer before `/compact`. | Current session tokens. |
| `/wiki-contradict` (P1) | Lint enhancement | Scans wiki for `[!contradiction]` callouts added by `auto_ingest.py`. | Zero (uses existing lint). |

#### 2.5 Keep the weekly cron as a safety net (P0)

`mempalace-remine.sh` stays. It catches:

- Machines where the watcher crashed overnight.
- Orphan session files the watcher missed during startup.
- The `wiki_to_mempalace.py` full injection (cheap enough to run weekly).

Move it to **Sunday 4am** (after the watcher has ingested the week's work).

---

## Part 3 — Unified Retrieval UX Across Clients

End state: whether you're in Copilot CLI, VS Code chat, or OpenCode, asking "what do I know about RoPE?" produces the same answer, pulled from the same sources.

### Retrieval ladder (cheapest → priciest, every client)

```
1. wiki/hot.md                   always-loaded, ~600 tokens
2. mempalace_search              local vector search, <100ms
3. wiki_search MCP               index.md + BM25 over wiki/
4. wiki_read MCP                 specific page read
5. wiki_graph_query MCP          (once graphify-integration lands)
6. Web fetch                     last resort
```

All six steps are already available via MCP after this plan lands. The ladder is encoded in the AGENTS.md snippet so every agent follows it.

### Per-client setup

| Client | Config file | What gets added |
|--------|-------------|-----------------|
| Copilot CLI | `~/.copilot/mcp-config.json` + `~/.copilot/AGENTS.md` (user-level) | MemPalace MCP (exists), labs-wiki MCP (exists), AGENTS.md snippet from §2.3 |
| VS Code Copilot | `.vscode/mcp.json` + `.github/copilot-instructions.md` | Same two MCPs + snippet in workspace instructions |
| OpenCode | `opencode.json` + symlinked skills | Same MCPs + `/wiki-save` skill available |

`labs-wiki/setup.sh` will be extended to generate all three configurations from a single source.

---

## Part 4 — Implementation Todos

### Phase A — Live memory loop (P0, biggest win)

- [ ] `watcher-script` — `homelab/scripts/mempalace-watcher.py` with watchdog, debounce, per-path wing routing
- [ ] `watcher-service` — `mempalace-watcher.service` systemd user unit + install instructions
- [ ] `hot-generator` — `labs-wiki/scripts/build_hot.py` (git log + mtime + mempalace_search; no LLM)
- [ ] `hot-cron` — hourly failsafe cron entry for `build_hot.py`
- [ ] `agents-snippet` — canonical AGENTS.md snippet + `setup.sh` injection into all projects
- [ ] `watcher-docs` — `labs-wiki/docs/live-memory-loop.md` architecture diagram + troubleshooting

### Phase B — Claude-obsidian feature adoption (P0/P1)

- [ ] `skill-wiki-save` — `/wiki-save` skill: conversation → `raw/` markdown (P0)
- [ ] `skill-refresh-hot` — `/wiki-refresh-hot` skill wraps `build_hot.py` (P0)
- [ ] `skill-save-before-compact` — `/wiki-save-before-compact` drawer snapshot (P1)
- [ ] `autoresearch-skill` — port `/autoresearch` with `program.md` configurability (P1)
- [ ] `lint-contradictions` — add `[!contradiction]` detection to `lint_wiki.py` (P1)
- [ ] `github-wiki-mode` — scaffold template for "GitHub codebase wiki" mode (P1)

### Phase C — Polish (P2/P3)

- [ ] `bases-dashboard` — `wiki/meta/dashboard.base` Obsidian Bases view (P2)
- [ ] `parallel-ingest` — parallelize `auto_ingest.py` over raw/ batch (P2)
- [ ] `seeded-examples` — seed 3 concept + 1 entity page for fresh clones (P2)
- [ ] `vault-colors-css` — `.obsidian/snippets/vault-colors.css` (P3)

---

## Part 5 — Open Questions / Decisions Needed

1. **Watcher granularity for Copilot session-state** — re-mine on every write (noisy) or only on file-close? Proposed: debounce 60s + skip if content_hash unchanged.
2. **hot.md in git?** — commit every hour = noisy history; but losing it on a fresh clone hurts the "instant context" story. Proposed: commit only daily snapshot, `.gitignore` the hourly rewrites.
3. **OpenCode session log format** — are there exportable transcripts yet, or still just package metadata? (Last check 2026-04-11: metadata only.) Re-evaluate before enabling that path in the watcher.
4. **Graph integration ordering** — does graphify-integration.md land before or after this plan? If before, add `wiki_graph_*` MCP tools to the retrieval ladder immediately; if after, it's a drop-in later.

---

## Success Criteria

1. A new session in any of the three clients starts with `wiki/hot.md` already in context — zero manual setup.
2. A decision recorded at 2pm is searchable via `mempalace_search` by 2:01pm.
3. `/wiki-save` at the end of a debugging session produces a well-structured `raw/` page that auto-mines within 60 seconds.
4. Weekly `mempalace-remine.sh` full sweep finds ≤ 5% new content (proving the watcher is catching everything).
5. The AGENTS.md retrieval ladder is followed: token usage on repeat questions drops measurably because agents hit `hot.md` before spinning up web search.
6. Zero LLM API keys beyond the existing GitHub Copilot Pro+ subscription are introduced.
