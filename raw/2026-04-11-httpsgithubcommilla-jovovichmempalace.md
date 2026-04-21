---
title: "https://github.com/milla-jovovich/mempalace"
type: url
captured: 2026-04-11T02:52:45.994256+00:00
source: android-share
url: "https://github.com/milla-jovovich/mempalace"
content_hash: "sha256:3cfa7f681a7ba97a77f7fbb7f6e2bed4f9fd968965970ff03664cb47281076a6"
tags: []
status: ingested
---

https://github.com/milla-jovovich/mempalace

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T00:03:42+00:00
- source_url: https://github.com/milla-jovovich/mempalace
- resolved_url: https://github.com/milla-jovovich/mempalace
- content_type: application/vnd.github+json
- image_urls: []

## Fetched Content
Repository: MemPalace/mempalace
Description: The best-benchmarked open-source AI memory system. And it's free.
Stars: 48478
Language: Python
Topics: ai, chromadb, llm, mcp, memory, python

## README

> [!CAUTION]
> **Scam alert.** The only official sources for MemPalace are this
> [GitHub repository](https://github.com/MemPalace/mempalace), the
> [PyPI package](https://pypi.org/project/mempalace/), and the docs site at
> **[mempalaceofficial.com](https://mempalaceofficial.com)**. Any other
> domain — including `mempalace.tech` — is an impostor and may distribute
> malware. Details and timeline: [docs/HISTORY.md](docs/HISTORY.md).

<div align="center">

<img src="assets/mempalace_logo.png" alt="MemPalace" width="240">

# MemPalace

Local-first AI memory. Verbatim storage, pluggable backend, 96.6% R@5 raw on LongMemEval — zero API calls.

[![][version-shield]][release-link]
[![][python-shield]][python-link]
[![][license-shield]][license-link]
[![][discord-shield]][discord-link]

</div>

---

## What it is

MemPalace stores your conversation history as verbatim text and retrieves
it with semantic search. It does not summarize, extract, or paraphrase.
The index is structured — people and projects become *wings*, topics
become *rooms*, and original content lives in *drawers* — so searches
can be scoped rather than run against a flat corpus.

The retrieval layer is pluggable. The current default is ChromaDB; the
interface is defined in [`mempalace/backends/base.py`](mempalace/backends/base.py)
and alternative backends can be dropped in without touching the rest of
the system.

Nothing leaves your machine unless you opt in.

Architecture, concepts, and mining flows:
[mempalaceofficial.com/concepts/the-palace](https://mempalaceofficial.com/concepts/the-palace.html).

---

## Install

```bash
pip install mempalace
mempalace init ~/projects/myapp
```

## Quickstart

```bash
# Mine content into the palace
mempalace mine ~/projects/myapp                    # project files
mempalace mine ~/.claude/projects/ --mode convos   # Claude Code sessions (scope with --wing per project)

# Search
mempalace search "why did we switch to GraphQL"

# Load context for a new session
mempalace wake-up
```

For Claude Code, Gemini CLI, MCP-compatible tools, and local models, see
[mempalaceofficial.com/guide/getting-started](https://mempalaceofficial.com/guide/getting-started.html).

---

## Benchmarks

All numbers below are reproducible from this repository with the commands
in [`benchmarks/BENCHMARKS.md`](benchmarks/BENCHMARKS.md). Full
per-question result files are committed under `benchmarks/results_*`.

**LongMemEval — retrieval recall (R@5, 500 questions):**

| Mode | R@5 | LLM required |
|---|---|---|
| Raw (semantic search, no heuristics, no LLM) | **96.6%** | None |
| Hybrid v4, held-out 450q (tuned on 50 dev, not seen during training) | **98.4%** | None |
| Hybrid v4 + LLM rerank (full 500) | ≥99% | Any capable model |

The raw 96.6% requires no API key, no cloud, and no LLM at any stage. The
hybrid pipeline adds keyword boosting, temporal-proximity boosting, and
preference-pattern extraction; the held-out 98.4% is the honest
generalisable figure.

The rerank pipeline promotes the best candidate out of the top-20
retrieved sessions using an LLM reader. It works with any reasonably
capable model — we have reproduced it with Claude Haiku, Claude Sonnet,
and minimax-m2.7 via Ollama Cloud (no Anthropic dependency). The gap
between raw and reranked is model-agnostic; we do not headline a "100%"
number because the last 0.6% was reached by inspecting specific wrong
answers, which `benchmarks/BENCHMARKS.md` flags as teaching to the test.

**Other benchmarks (full results in [`benchmarks/BENCHMARKS.md`](benchmarks/BENCHMARKS.md)):**

| Benchmark | Metric | Score | Notes |
|---|---|---|---|
| LoCoMo (session, top-10, no rerank) | R@10 | 60.3% | 1,986 questions |
| LoCoMo (hybrid v5, top-10, no rerank) | R@10 | 88.9% | Same set |
| ConvoMem (all categories, 250 items) | Avg recall | 92.9% | 50 per category |
| MemBench (ACL 2025, 8,500 items) | R@5 | 80.3% | All categories |

We deliberately do not include a side-by-side comparison against Mem0,
Mastra, Hindsight, Supermemory, or Zep. Those projects publish different
metrics on different splits, and placing retrieval recall next to
end-to-end QA accuracy is not an honest comparison. See each project's
own research page for their published numbers.

**Reproducing every result:**

```bash
git clone https://github.com/MemPalace/mempalace.git
cd mempalace
pip install -e ".[dev]"
# see benchmarks/README.md for dataset download commands
python benchmarks/longmemeval_bench.py /path/to/longmemeval_s_cleaned.json
```

---

## Knowledge graph

MemPalace includes a temporal entity-relationship graph with validity
windows — add, query, invalidate, timeline — backed by local SQLite.
Usage and tool reference:
[mempalaceofficial.com/concepts/knowledge-graph](https://mempalaceofficial.com/concepts/knowledge-graph.html).

## MCP server

29 MCP tools cover palace reads/writes, knowledge-graph operations,
cross-wing navigation, drawer management, and agent diaries. Installation
and the full tool list:
[mempalaceofficial.com/reference/mcp-tools](https://mempalaceofficial.com/reference/mcp-tools.html).

## Agents

Each specialist agent gets its own wing and diary in the palace.
Discoverable at runtime via `mempalace_list_agents` — no bloat in your
system prompt:
[mempalaceofficial.com/concepts/agents](https://mempalaceofficial.com/concepts/agents.html).

## Auto-save hooks

Two Claude Code hooks save periodically and before context compression:
[mempalaceofficial.com/guide/hooks](https://mempalaceofficial.com/guide/hooks.html).

---

## Requirements

- Python 3.9+
- A vector-store backend (ChromaDB by default)
- ~300 MB disk for the default embedding model

No API key is required for the core benchmark path.

## Docs

- Getting started → [mempalaceofficial.com/guide/getting-started](https://mempalaceofficial.com/guide/getting-started.html)
- CLI reference → [mempalaceofficial.com/reference/cli](https://mempalaceofficial.com/reference/cli.html)
- Python API → [mempalaceofficial.com/reference/python-api](https://mempalaceofficial.com/reference/python-api.html)
- Full benchmark methodology → [benchmarks/BENCHMARKS.md](benchmarks/BENCHMARKS.md)
- Release notes → [CHANGELOG.md](CHANGELOG.md)
- Corrections and public notices → [docs/HISTORY.md](docs/HISTORY.md)

## Contributing

PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).

<!-- Link Definitions -->
[version-shield]: https://img.shields.io/badge/version-3.3.0-4dc9f6?style=flat-square&labelColor=0a0e14
[release-link]: https://github.com/MemPalace/mempalace/releases
[python-shield]: https://img.shields.io/badge/python-3.9+-7dd8f8?style=flat-square&labelColor=0a0e14&logo=python&logoColor=7dd8f8
[python-link]: https://www.python.org/
[license-shield]: https://img.shields.io/badge/license-MIT-b0e8ff?style=flat-square&labelColor=0a0e14
[license-link]: https://github.com/MemPalace/mempalace/blob/main/LICENSE
[discord-shield]: https://img.shields.io/badge/discord-join-5865F2?style=flat-square&labelColor=0a0e14&logo=discord&logoColor=5865F2
[discord-link]: https://discord.com/invite/ycTQQCu6kn


## File: docs/CLOSETS.md

```
# Closets — The Searchable Index Layer

## What closets are

Drawers hold your verbatim content. Closets are the index — compact pointers that tell the searcher which drawers to open.

```
CLOSET: "built auth system|Ben;Igor|→drawer_api_auth_a1b2c3"
         ↑ topic           ↑ entities  ↑ points to this drawer
```

An agent searching "who built the auth?" hits the closet first (fast scan of short text), then opens the referenced drawer to get the full verbatim content.

## Lifecycle

### When are closets created?

Closets are created during `mempalace mine`. For each file mined:
1. Content is chunked into drawers (verbatim, ~800 chars each)
2. Topics, entities, and quotes are extracted from the content
3. A closet is created with pointer lines to those drawers

### What's inside a closet?

Each line is one atomic topic pointer:
```
topic description|entity1;entity2|→drawer_id_1,drawer_id_2
"verbatim quote from the content"|entity1|→drawer_id_3
```

Topics are never split across closets. If adding a topic would exceed 1,500 characters, a new closet is created.

### When do closets update?

When a file is re-mined (content changed, or `NORMALIZE_VERSION` was bumped), the miner first deletes every closet for that source file (`purge_file_closets`) and then writes a fresh set. Stale topics from the prior mine are gone — closets are always a snapshot of the current content, never an accumulation across runs.

### What about stale topics?

There are no stale topics: each re-mine is a clean rebuild for that source file. If a file gets larger and produces fewer or more closets than last time, the leftover numbered closets from the larger run are still purged because the delete is done by `source_file`, not by ID.

### Do closets survive palace rebuilds?

Closets are stored in the `mempalace_closets` ChromaDB collection alongside `mempalace_drawers`. If you delete and rebuild the palace, closets are recreated during the next `mempalace mine`.

## How search uses closets

```
Query → search mempalace_closets (fast, small documents)
         ↓
    top closet hits → parse `→drawer_id_a,drawer_id_b` pointers
         ↓
    fetch exactly those drawers from mempalace_drawers (verbatim content)
         ↓
    apply max_distance filter
         ↓
    return chunk-level results (same shape as direct search)
```

Hits carry `matched_via: "closet"` (or `"drawer"` for the fallback path) plus a `closet_preview` field showing the line that surfaced them.

If no closets exist (palace created before this feature) — or all closet hits get filtered out by `max_distance` — search falls back to direct drawer search. Closets are created on next mine.

> **BM25 hybrid re-rank** is on the roadmap (deferred to a follow-up PR alongside generic `LLM_*` env-var support); the current closet search ranks purely by ChromaDB cosine distance against the closet text.

## Limits

| Setting | Value | Reason |
|---------|-------|--------|
| Max closet size | 1,500 chars (`CLOSET_CHAR_LIMIT`) | Leaves buffer under ChromaDB's working limit |
| Source content scanned | 5,000 chars (`CLOSET_EXTRACT_WINDOW`) | Caps regex extraction cost on long files; back-of-file content is currently invisible to closet extraction (tracked for follow-up) |
| Max topics per file | 12 | Keeps closets focused |
| Max quotes per file | 3 | Most relevant only |
| Max entities per pointer | 5 | Top names by frequency, after stoplist filtering |

## For developers

Closet functions live in `mempalace/palace.py`:
- `get_closets_collection()` — get the closets ChromaDB collection
- `build_closet_lines()` — extract topics/entities/quotes into pointer lines
- `upsert_closet_lines()` — write lines to closets respecting the char limit (overwrites existing IDs; does not append — call `purge_file_closets` first when re-mining)
- `purge_file_closets()` — delete every closet for a given source file before rebuild
- `CLOSET_CHAR_LIMIT` / `CLOSET_EXTRACT_WINDOW` — size constants

The closet-first search path lives in `mempalace/searcher.py`:
- `_extract_drawer_ids_from_closet()` — parse `→drawer_a,drawer_b` pointers out of a closet document
- `_closet_first_hits()` — query closets, parse pointers, hydrate matching drawers, return chunk-level hits or `None` to fall back

Note: only the project miner (`miner.py::process_file`) builds closets today. Conversation-mined wings (Claude Code JSONL, ChatGPT export, etc.) will keep using direct drawer search via the searcher fallback until the convo-closet PR lands.

```


## File: docs/HISTORY.md

```
# MemPalace — History, Corrections, and Public Notices

This file is the canonical record of post-launch corrections, public notices,
and retractions that affect MemPalace's public claims. Newest first.

---

## 2026-04-14 — Benchmark table rewrite (issue [#875](https://github.com/MemPalace/mempalace/issues/875))

A community audit identified a category error in the public benchmark tables
on `README.md` and `mempalaceofficial.com`: MemPalace's retrieval recall
numbers (R@5, R@10) were listed in the same columns as competitors'
end-to-end QA accuracy numbers. They are different metrics and are not
comparable — a system can have 100% retrieval recall and 40% QA accuracy.

The audit also found that the retracted "+34% palace boost" claim (see the
April 7 note below) was still present in multiple surfaces despite that
retraction, and that two competitor numbers (`Mem0 ~85%`, `Zep ~85%`) had no
published source and did not match the metrics those projects actually
publish.

What changed in this PR:

- The headline number on all surfaces is now **96.6% R@5 on LongMemEval in
  raw mode**, independently reproduced on Linux x86_64 against the tagged
  v3.3.0 release on 2026-04-14. Result JSONLs are committed under
  `benchmarks/results_*.jsonl` (see PR description for the scorecard).
- The **"100% with Haiku rerank"** claim has been removed from all public
  comparison tables. It reproduces on our machines and with a different LLM
  family (minimax-m2.7 via Ollama Cloud: 99.2% R@5 / 100.0% R@10 on the full
  500-question LongMemEval set) — but the 99.4% → 100% step was developed
  by inspecting three specific wrong answers (`benchmarks/BENCHMARKS.md` has
  called this "teaching to the test" since February). It belongs in the
  methodology document, not in a headline.
- The **honest held-out number** for the hybrid pipeline — 98.4% R@5 on 450
  questions that `hybrid_v4` was never tuned on, deterministic seed — is now
  the comparable figure when an LLM rerank is involved.
- The **retracted "+34% palace boost"** has been removed from
  `README.md`, `website/concepts/the-palace.md`,
  `website/guide/searching.md`, and `website/reference/contributing.md`.
  Wing and room filters remain useful — they're standard metadata filters —
  but they are not presented as a novel retrieval improvement.
- **Competitor comparison tables** mixing retrieval recall with QA accuracy
  have been removed from `README.md` and `website/reference/benchmarks.md`.
  Where MemPalace can be fairly compared on the same metric, we link to the
  cited source. Otherwise we report our own numbers and let readers draw
  their own conclusions.
- **Reproduction instructions** in `benchmarks/BENCHMARKS.md` and
  `benchmarks/README.md` were pointing at a defunct branch
  (`aya-thekeeper/mempal`); they now point at `MemPalace/mempalace`.
- The **LoCoMo 100% R@10 with top-50 rerank** row has been removed from
  public comparison surfaces. With per-conversation session counts of 19–32
  and `top_k=50`, the retrieval stage returns every session in the
  conversation by construction, so the number measures an LLM's
  reading comprehension over the whole conversation, not retrieval.

Thanks to [@dial481](https://github.com/MemPalace/mempalace/issues/875) for
the detailed audit and to [@rohitg00](https://github.com/rohitg00) for the
parallel write-up in Discussion #747.

---

## 2026-04-11 — Impostor domains and malware

Several community members (issues #267, #326, #506) reported fake MemPalace
websites distributing malware. The only official surfaces for this project
are:

- This GitHub repository: [github.com/MemPalace/mempalace](https://github.com/MemPalace/mempalace)
- The PyPI package: [pypi.org/project/mempalace](https://pypi.org/project/mempalace/)
- The docs site: [mempalaceofficial.com](https://mempalaceofficial.com)

Any other domain — `mempalace.tech` being the one most commonly reported —
is not ours. Never run install scripts from unofficial sites.

Thanks to our community members for flagging the problem.

---

## 2026-04-07 — A Note from Milla & Ben

> The community caught real problems in this README within hours of launch
> and we want to address them directly.
>
> **What we got wrong:**
>
> - **The AAAK token example was incorrect.** We used a rough heuristic
>   (`len(text)//3`) for token counts instead of an actual tokenizer. Real
>   counts via OpenAI's tokenizer: the English example is 66 tokens, the
>   AAAK example is 73. AAAK does not save tokens at small scales — it's
>   designed for *repeated entities at scale*, and the README example was a
>   bad demonstration of that. We're rewriting it.
>
> - **"30x lossless compression" was overstated.** AAAK is a lossy
>   abbreviation system (entity codes, sentence truncation). Independent
>   benchmarks show AAAK mode scores **84.2% R@5 vs raw mode's 96.6%** on
>   LongMemEval — a 12.4 point regression. The honest framing is: AAAK is
>   an experimental compression layer that trades fidelity for token
>   density, and **the 96.6% headline number is from RAW mode, not AAAK**.
>
> - **"+34% palace boost" was misleading.** That number compares unfiltered
>   search to wing+room metadata filtering. Metadata filtering is a
>   standard feature of the underlying vector store, not a novel retrieval
>   mechanism. Real and useful, but not a moat.
>
> - **"Contradiction detection"** exists as a separate utility
>   (`fact_checker.py`) but is not currently wired into the knowledge graph
>   operations as the README implied.
>
> - **"100% with Haiku rerank"** is real (we have the result files) but
>   the rerank pipeline is not in the public benchmark scripts. We're
>   adding it.
>
> **What's still true and reproducible:**
>
> - **96.6% R@5 on LongMemEval in raw mode**, on 500 questions, zero API
>   calls — independently reproduced on M2 Ultra in under 5 minutes by
>   [@gizmax](https://github.com/MemPalace/mempalace/issues/39).
> - Local, free, no subscription, no cloud, no data leaving your machine.
> - The architecture (wings, rooms, closets, drawers) is real and useful,
>   even if it's not a magical retrieval boost.
>
> **What we're doing:**
>
> 1. Rewriting the AAAK example with real tokenizer counts and a scenario
>    where AAAK actually demonstrates compression
> 2. Adding `mode raw / aaak / rooms` clearly to the benchmark
>    documentation so the trade-offs are visible
> 3. Wiring `fact_checker.py` into the KG ops so the contradiction
>    detection claim becomes true
> 4. Pinning the vector store dependency to a tested range (issue #100),
>    fixing the shell injection in hooks (#110), and addressing the macOS
>    ARM64 segfault (#74)
>
> **Thank you to everyone who poked holes in this.** Brutal honest
> criticism is exactly what makes open source work, and it's what we asked
> for. Special thanks to
> [@panuhorsmalahti](https://github.com/MemPalace/mempalace/issues/43),
> [@lhl](https://github.com/MemPalace/mempalace/issues/27),
> [@gizmax](https://github.com/MemPalace/mempalace/issues/39), and everyone
> who filed an issue or a PR in the first 48 hours. We're listening, we're
> fixing, and we'd rather be right than impressive.
>
> — *Milla Jovovich & Ben Sigman*

```


## File: docs/rfcs/002-source-adapter-plugin-spec.md

```
# RFC 002 — Source Adapter Plugin Specification

- **Status:** Draft
- **Tracking issue:** [#989](https://github.com/MemPalace/mempalace/issues/989)
- **Related:** [#274](https://github.com/MemPalace/mempalace/issues/274), [#23](https://github.com/MemPalace/mempalace/pull/23), [#169](https://github.com/MemPalace/mempalace/pull/169), [#232](https://github.com/MemPalace/mempalace/pull/232), [#567](https://github.com/MemPalace/mempalace/pull/567), [#98](https://github.com/MemPalace/mempalace/pull/98), [#591](https://github.com/MemPalace/mempalace/pull/591), [#592](https://github.com/MemPalace/mempalace/pull/592), [#702](https://github.com/MemPalace/mempalace/pull/702), [#981](https://github.com/MemPalace/mempalace/issues/981), [#244](https://github.com/MemPalace/mempalace/pull/244), [#419](https://github.com/MemPalace/mempalace/pull/419), [#300](https://github.com/MemPalace/mempalace/pull/300), [#952](https://github.com/MemPalace/mempalace/pull/952), [#389](https://github.com/MemPalace/mempalace/pull/389), [#434](https://github.com/MemPalace/mempalace/pull/434)
- **Sibling spec:** [RFC 001 — Storage Backend Plugin Specification](001-storage-backend-plugin-spec.md)
- **Spec version:** `1.0`

## Summary

A formal contract for MemPalace source adapters so third parties can ship `pip install mempalace-source-<name>` packages (Cursor, OpenCode, git, Slack, Notion, email, calendar, Whisper transcripts, …) that drop into `mempalace mine` without patching core. The spec defines the adapter interface, record shape, metadata schema contract, privacy class, entry-point registration, incremental-ingest semantics, closet integration, a declared-transformation model that replaces the informal "verbatim" promise with a verifiable one, conformance tests, and the refactor of the existing file and conversation miners into first-party adapters on the same contract.

RFC 001 formalized the write side (where drawers are stored). This RFC formalizes the read side (where content comes from). Both are required for MemPalace to function as a durable daemon managing heterogeneous palaces across many source types.

## Motivation

Six source ingesters are currently in flight, each solving the same problem a different way:

| PR / Issue | Source | Mechanism |
|---|---|---|
| [#274](https://github.com/MemPalace/mempalace/issues/274) | Cursor | `workspaceStorage/*.vscdb` SQLite extraction |
| [#23](https://github.com/MemPalace/mempalace/pull/23) | OpenCode | SQLite session database |
| [#169](https://github.com/MemPalace/mempalace/pull/169) | Pi agent | JSONL session normalizer |
| [#232](https://github.com/MemPalace/mempalace/pull/232) | Cursor (JSONL variant) | JSONL normalizer |
| [#567](https://github.com/MemPalace/mempalace/pull/567), [#98](https://github.com/MemPalace/mempalace/pull/98) | Git | `git log` + `gh pr view` with structured diff summary |
| [#591](https://github.com/MemPalace/mempalace/pull/591), [#592](https://github.com/MemPalace/mempalace/pull/592) | Delphi Oracle | Real-time intelligence signals |
| [#702](https://github.com/MemPalace/mempalace/pull/702) | Cursor + factory.ai | Combined session miners |

Plus three ingesters already grafted into core:

- `mempalace/miner.py` — filesystem project miner, fixed char-window chunking, keyword hall routing
- `mempalace/convo_miner.py` — chat transcript miner with exchange-pair chunking
- `mempalace/normalize.py` — format detection for four chat-export shapes (Claude Code JSONL, Codex JSONL, Claude.ai / ChatGPT / Slack JSON)

Plus one open proposal for a different ingest semantic:

- [#981](https://github.com/MemPalace/mempalace/issues/981) — path-level descriptions: mine metadata-as-content instead of raw bytes for matched paths. This is a legitimate third ingest mode (alongside chunked-content and whole-record) that the current architecture has no home for.

Each contributor has reinvented source discovery, source-item identity, incremental-ingest bookkeeping, metadata shape, and chunking strategy. Format detection for new chat exports lands in `normalize.py` as one more branch in an `if` chain. There is no shared abstraction, no conformance suite, and no contract new adapter authors can build against.

This is the same situation RFC 001 addresses for storage backends: a pattern that emerged organically, now needs a specification so the community can contribute cleanly and enterprises can build against a stable surface.

### Why this matters beyond developer tooling

The adapter pattern is source-agnostic. What has so far shown up as "Cursor transcripts" and "git commits" generalizes to:

- **Knowledge work** — Notion, Obsidian, Logseq, Google Docs, iA Writer, Zettlr
- **Communications** — Slack, Discord, Teams, Signal backups, mbox/eml email, iMessage
- **Research** — arXiv PDFs, Zotero libraries, bookmarked articles, Kindle highlights, web archives
- **Creator workflows** — YouTube captions, podcast transcripts (Whisper/Deepgram), Descript projects
- **Regulated domains** — medical records, legal filings, financial statements (all gated on §6 privacy class)

Enterprises key on their own domain metadata — `repo/PR/SHA` for engineering, `patient/encounter/CPT` for healthcare, `case/docket/jurisdiction` for legal. The schema lives in the adapter; the content lives in the drawer. This is how structured-data use cases are served without violating the byte-preservation commitments adapters make.

## Goals

1. A source adapter ships as a standalone Python package; `pip install mempalace-source-<name>` is sufficient to use it.
2. `mempalace mine` and the MCP mine tool are source-agnostic — all extraction goes through registered adapters. No `if source_type == 'foo'` branches in core.
3. Content transformations are **declared** (§1.4): each adapter advertises the set of transformations it applies to source bytes. Byte-preserving adapters declare the empty set. Consumers can programmatically determine what happened to their data.
4. Incremental ingest is cheap and correct: re-running mine only touches items whose source-side version changed, using the palace itself as the cursor (no sidecar).
5. Each adapter declares a structured metadata schema. Enterprises index and filter on that schema. Core is schema-agnostic beyond the universal fields in §5.1.
6. The existing `miner.py` and `convo_miner.py` become the first two first-party adapters on the new contract. Drawer metadata fields and field names are preserved — the spec adds fields, does not rename them.
7. A privacy class is declarable at the adapter boundary so sensitive sources (medical, financial, personal comms) are handled with explicit policy rather than implicit trust.

## Non-goals

- Defining chunking. Each adapter owns its chunking strategy — tree-sitter for code, exchange-pair for chat, whole-record for a PR. Core does not impose a chunk size.
- Defining live-stream / webhook shapes (the Delphi Oracle pattern of continuous signal ingestion). That is a separate future RFC; v1 is pull-mode.
- Defining LLM-based structured extraction. Adapters MAY use an LLM; the spec does not mandate or standardize this.
- Defining cross-adapter dedup. When the same content appears via two adapters (e.g., a PR body mined via `git` and as a conversation quote mined via `claude-code`), both drawers land. Deduplication policy is a separate concern handled at query time by `searcher.py`.
- Defining closet construction. Core continues to build closets from adapter-yielded drawers (§1.7); the closet-building algorithm itself is not part of this spec.

---

## 1. Source adapter contract

### 1.1 Required method

All adapters implement `BaseSourceAdapter` with a single kwargs-only ingest method:

```python
class BaseSourceAdapter(ABC):
    @abstractmethod
    def ingest(
        self,
        *,
        source: SourceRef,
        palace: PalaceContext,
    ) -> Iterator[IngestResult]:
        """Enumerate and extract content from a source.

        Yields a stream of IngestResult values
```


## File: .gitignore

```
*.egg-info/
dist/
build/
__pycache__/
*.pyc
.pytest_cache/
mempal.yaml
.a5c/
.claude/
.codex/
.codex

# Environment
.env
.env.*

# OS
.DS_Store
Thumbs.db

# IDEs
.idea/
.vscode/
*.swp
*.swo
*~

# Coverage
htmlcov/
.coverage
coverage.xml

# Virtual environments
.venv/
venv/

# ChromaDB local data
*.sqlite3-journal

```


## File: .pre-commit-config.yaml

```
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    # Keep in lock-step with the ruff version pinned in .github/workflows/ci.yml
    # (>=0.4.0,<0.5). Using a newer rev here produces a different formatter
    # output than CI and breaks `ruff format --check` in the lint job.
    rev: v0.4.10
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

```


## File: AGENTS.md

```
# CLAUDE.md

## The Mission

Memory is identity. When an AI forgets everything between conversations, it cannot build real understanding — of you, your work, your people, your life.

MemPalace exists to solve this. It is a memory system — not a search engine, not a RAG pipeline, not a vector database wrapper. It treats every word you have shared as sacred, stores it verbatim, and makes it instantly available. Your data never leaves your machine. We never summarize. We never paraphrase. We return your exact words.

100% recall is the design requirement — the target every search path is measured against. Anything less means forgetting, and forgetting means starting over.

The name comes from the ancient "method of loci" — the memory palace technique used for thousands of years to organize and recall vast amounts of information by placing it in imagined rooms of an imagined building. We were also inspired by the Zettelkasten method (created by German sociologist Niklas Luhmann) — small cross-referenced index cards that point to each other. We apply both ideas to AI memory:

- **Wings** for broad categories (people, projects, topics)
- **Rooms** for time-based groupings (days, sessions)
- **Drawers** for full verbatim content (your exact words)
- **AAAK compression** for the index layer — a compact symbolic format (via `dialect.py`) that lets an LLM scan thousands of entries instantly and know exactly which drawer to open

## Design Principles

These are non-negotiable. Every PR, every feature, every refactor must honor them.

- **Verbatim always** — Never summarize, paraphrase, or lossy-compress user data. The system searches the index and returns the original words. If a user said it, we store exactly what they said. This is the foundational promise.
- **Incremental only** — Append-only ingest after initial build. Never destroy existing data to rebuild. A crash mid-operation must leave the existing palace untouched.
- **Entity-first** — Everything is keyed by real names with disambiguation by DOB, ID, or context. People matter more than topics.
- **Local-first, zero API** — All extraction, chunking, and embedding happens on the user's machine. No cloud dependency for memory operations. No API keys required.
- **Performance budgets** — Hooks under 500ms. Startup injection under 100ms. Memory should feel instant.
- **Privacy by architecture** — The system physically cannot send your data because it never leaves your machine. No telemetry, no phone-home, no external service dependencies for core operations.
- **Background everything** — Filing, indexing, timestamps, and pipeline work happen via hooks in the background. Nothing interrupts the user's conversation. Zero tokens spent on bookkeeping in the chat window.

## Contributing

We welcome bug fixes, performance improvements, new language support, better entity disambiguation, documentation, and test coverage.

We do not accept summarization of user content, cloud storage/sync features, telemetry or analytics, features requiring API keys for core memory, or shortcuts that bypass verbatim storage.

## Setup

```bash
pip install -e ".[dev]"
```

## Commands

```bash
# Run tests
python -m pytest tests/ -v --ignore=tests/benchmarks

# Run tests with coverage
python -m pytest tests/ -v --ignore=tests/benchmarks --cov=mempalace --cov-report=term-missing

# Lint
ruff check .

# Format
ruff format .

# Format check (CI mode)
ruff format --check .
```

## Project Structure

```
mempalace/
├── mcp_server.py        # MCP server — all read/write tools
├── cli.py               # CLI dispatcher
├── config.py            # Configuration + input validation
├── miner.py             # Project file miner
├── convo_miner.py       # Conversation transcript miner
├── searcher.py          # Semantic search (hybrid BM25 + vector)
├── knowledge_graph.py   # Temporal entity-relationship graph (SQLite)
├── palace.py            # Shared palace operations
├── palace_graph.py      # Room traversal + cross-wing tunnels
├── backends/            # Pluggable storage backends (ChromaDB default)
│   ├── base.py          # Abstract interface — implement this for new backends
│   └── chroma.py        # ChromaDB implementation
├── dialect.py           # AAAK compression dialect
├── normalize.py         # Transcript format detection + normalization
├── entity_detector.py   # Auto-detect people/projects from content
├── entity_registry.py   # Entity storage and disambiguation
├── layers.py            # L0-L3 memory wake-up stack
├── onboarding.py        # Interactive first-run setup
├── repair.py            # Palace repair and consistency checks
├── dedup.py             # Deduplication
├── migrate.py           # ChromaDB version migration
├── spellcheck.py        # Auto-correct user messages
├── exporter.py          # Palace data export
├── hooks_cli.py         # Hook management CLI
├── query_sanitizer.py   # Prompt contamination prevention
├── split_mega_files.py  # Split concatenated transcript files
└── version.py           # Single source of truth for version

hooks/                   # Claude Code hook scripts
├── mempal_save_hook.sh        # Stop: triggers diary save
└── mempal_precompact_hook.sh  # PreCompact: saves state before compression
```

## Conventions

- **Python style**: snake_case for functions/variables, PascalCase for classes
- **Linter**: ruff with E/F/W rules
- **Formatter**: ruff format, double quotes
- **Commits**: conventional commits (`fix:`, `feat:`, `test:`, `docs:`, `ci:`)
- **Tests**: `tests/test_*.py`, fixtures in `tests/conftest.py`
- **Coverage**: 85% threshold (80% on Windows due to ChromaDB file lock cleanup)

## Architecture

```
User → CLI / MCP Server → Storage Backend (ChromaDB default, pluggable)
                        → SQLite (knowledge graph)

Palace structure:
  WING (person/project)
    └── ROOM (day/topic)
          └── DRAWER (verbatim text chunk)

Index layer (AAAK):
  Compressed pointers → DRAWER locations
  Scanned by LLM to find relevant drawers without reading all content

Knowledge Graph:
  ENTITY → PREDICATE → ENTITY (with valid_from / valid_to dates)
```

## Key Files for Common Tasks

- **Adding an MCP tool**: `mempalace/mcp_server.py` — add handler function + TOOLS dict entry
- **Changing search**: `mempalace/searcher.py`
- **Modifying mining**: `mempalace/miner.py` (project files) or `mempalace/convo_miner.py` (transcripts)
- **Adding a storage backend**: subclass `mempalace/backends/base.py`, register in `backends/__init__.py`
- **Input validation**: `mempalace/config.py` — `sanitize_name()` / `sanitize_content()`
- **Tests**: mirror source structure in `tests/test_<module>.py`

```


## File: CHANGELOG.md

```
# Changelog

All notable changes to [MemPalace](https://github.com/MemPalace/mempalace) are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased] — v3.3.0 (on develop)

### New Features
- Closet layer — a compact searchable index of pointers to verbatim drawers, enabling fast topical lookup without reading all content (#788)
- BM25 hybrid search — closets boost ranking, drawers remain the source of truth (#795, #829)
- Entity metadata on every drawer for filterable search (#829)
- Diary ingest — day-based rooms for conversation transcripts (#829)
- Cross-wing tunnels — explicit links between rooms in different wings for multi-project agents (#829)
- Drawer-grep — returns the best-matching chunk plus adjacent context drawers (#829)
- Offline fact checker against the entity registry and knowledge graph (#829)
- LLM-based closet regeneration — optional, bring-your-own endpoint, no mandatory API key (#793)
- Hall detection — routes drawer content to `emotions` / `technical` / `family` / `memory` / `identity` / `consciousness` / `creative` halls, enabling hall-based graph connectivity within wings (#835)

### Bug Fixes
- Set `hnsw:space=cosine` metadata on all collection creation sites — fixes broken similarity scoring under ChromaDB's default L2 distance (#807, #218)
- File-level locking prevents duplicate drawers when agents mine the same file concurrently (#784, #826)
- Hybrid closet+drawer retrieval — closets boost ranking, never gate results (#795)
- Stop hooks from making agents write in chat — saves tokens on every turn (#786)
- Strip system tags, hook output, and Claude UI chrome from drawers before filing (#785)
- Verbatim-safe `strip_noise` scoped to Claude Code JSONL only (#785)
- Prevent diary entry ID collisions via microsecond timestamp and full content hash (#819)
- Auto-rebuild stale drawers via `NORMALIZE_VERSION` schema gate
- Enforce atomic topics in closets and extract richer pointers
- Sync `version.py` to match `pyproject.toml` (#820)
- Remove unused `main` import from `mempalace/__init__.py` (#827)
- README audit — fix 7 stale claims (tool count, version badge, wake-up token cost, `dialect.py` lossless disclaimer, `pyproject.toml` version) with 42 regression-guard tests (#835)

### Improvements
- Optimize entity detection with regex caching and pre-compilation (#828)
- Extract locked filing block into helper to keep `mine_convos` under C901 complexity

### Documentation
- Add `docs/CLOSETS.md` — closet layer overview
- Fix stale `milla-jovovich/*` org URLs in website and plugin manifests (#787)
- Fix remaining stale org URLs in contributor docs (#808)
- Rewrite `README.md` and `mempalaceofficial.com` benchmark pages to remove category-error cross-system comparisons (R@5 retrieval recall had been listed next to competitor QA accuracy under one column), remove the retracted "+34% palace boost" claim from the surfaces where it had remained, replace the `100%` Haiku-rerank headline with the honest held-out `98.4%` R@5, drop the LoCoMo `100%` top-50 row (retrieval-bypass artefact), and fix the broken `aya-thekeeper/mempal` reproduction URL (#875)
- Add `docs/HISTORY.md` as the canonical home for corrections, retractions, and public notices; move the 2026-04-07 "Note from Milla & Ben" and the 2026-04-11 impostor-domain notice out of `README.md`
- Add v3.3.0 reproduction result JSONLs and the deterministic `seed=42` 50/450 LongMemEval split under `benchmarks/` — every BENCHMARKS.md claim reproduces exactly

### Internal
- Add test coverage for `mine_lock`, closets, entity metadata, BM25, and diary
- Verify `mine_lock` via disjoint critical-section intervals
- Serialize `mine_lock` concurrency test with multiprocessing
- Make diary state path assertion platform-neutral
- Add `TestTunnels` coverage for cross-wing tunnel operations
- Ruff format with CI-pinned version (0.4.x); format `mempalace/palace.py`

---

## [3.2.0] — 2026-04-12

### Packaging
- Remove `chromadb<0.7` upper bound — unblocks installs against chromadb 1.x palaces (#690)
- Bump version to 3.2.0 across `pyproject.toml`, `mempalace/version.py`, README badge, and OpenClaw SKILL (#761)

### Security
- Harden palace deletion, WAL redaction, and MCP search input handling (#739)
- Consistent input validation, argument whitelisting, concurrency safety, and WAL fixes (#647)
- Remove hardcoded credential paths from benchmark runners (#177)
- Remove global SSL verification bypass in convomem_bench (#176)

### Bug Fixes
- Parse Claude.ai privacy export with `messages` key and sender field (#685, #677)
- Detect mtime changes in `_get_client` to prevent stale HNSW index (#757)
- Hash full content in `tool_add_drawer` drawer ID — stable re-mines (#716)
- Remove 10k drawer cap from status display (#707, #603)
- Correct typo in entity_detector interactive classification prompt (#755)
- Prevent convo_miner from re-processing 0-chunk files on every run (#732, #654)
- Remove silent 8-line AI response truncation in convo_miner (#708, #692)
- Store full AI response in convo_miner exchange chunking (#695)
- Fix `mine --dry-run` TypeError on files with room=None (#687, #586)
- Skip arg whitelist for handlers accepting `**kwargs` (#684, #572)
- Allow Unicode in `sanitize_name()` — Latvian, CJK, Cyrillic (#683, #637)
- Auto-repair BLOB seq_ids from chromadb 0.6→1.5 migration (#664)
- Remove no-op `ORT_DISABLE_COREML` env var (#653, #397)
- Disambiguate hook block reasons to name MemPalace explicitly (#666)
- Use epsilon comparison for mtime to prevent unnecessary re-mining (#610)
- Correct token count estimate in compress summary (#609)
- Implement MCP ping health checks (#600)
- Align `cmd_compress` dict keys with `compression_stats()` return values (#569)
- Skip unreachable reparse points in `detect_rooms_from_folders` on Windows (#558)
- Prevent HNSW index bloat from duplicate `add()` calls (#544, #525)
- Purge stale drawers before re-mine to avoid hnswlib segfault (#544)
- Mitigate system prompt contamination in search queries (#385, #333)
- Count Codex `user_message` turns in `_count_human_messages` (#373, #347)
- Paginate large collection reads and surface errors in MCP tools (#371, #339, #338)
- Expand `~` in split command directory argument (#361)
- Ignore `wait_for_previous` argument to support Gemini MCP clients (#322)
- Close KnowledgeGraph SQLite connections in test fixtures (#450)
- Remove duplicate cache variable declarations in mcp_server.py (#449)
- Add `--yes` flag to init instructions for non-interactive use (#682, #534)
- Add `mcp` command with setup guidance (#315)

### New Features
- i18n support — 8 languages (en, es, fr, de, ja, ko, zh-CN, zh-TW) (#718)
- New MCP tools: get/list/update drawer, hook settings, export (#667, #635)
- `mempalace migrate` — recover palaces from different ChromaDB versions (#502)
- Add OpenClaw/ClawHub skill (#491)
- Backend seam for pluggable storage backends (#413)

### Improvements
- Disable broken auto-bump workflow (#414)
- Improve agent readiness — AGENTS.md, dependabot, CODEOWNERS, labels (#497)

### Documentation
- Add CLAUDE.md and mission/principles to AGENTS.md (#720)
- Add VitePress documentation site (#439)
- Add warning about fake MemPalace websites (#598)
- Fix stale org URLs and PR branch target in contributor docs (#679)
- Fix misaligned architecture diagram (#734, #733)
- Add ROADMAP.md — v3.1.1 stability patch and v4.0.0-alpha plan

### Internal
- ruff format convo_miner.py (#741)
- ruff format all Python files (#675)
- CI: trigger tests on develop branch PRs and pushes (#674)
- CI: fix GitHub Pages publishing (#691)

---

## [3.1.0] — 2026-04-09

### Security
- Harden inputs, fix shell injection, optimize DB access (#387)
- Sanitize SESSION_ID in save hook to prevent path traversal (#141)
- Sanitize error responses and remove `sys.exit` from library code (#139)
- Shell injection fix i
```


(… 216 more files omitted due to size limit)
<!-- fetched-content:end -->
