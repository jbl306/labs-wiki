# Copilot Pro+ / GitHub Models Efficiency Plan

> Created: 2026-04-18
> Scope: make the labs-wiki + MemPalace + session-curation loop work efficiently with **Copilot Pro+** and **GitHub Models only** — no OpenAI/Anthropic API keys.

---

## Goal

Use the existing stack to achieve Karpathy-style **compile-once, keep-current** knowledge management while minimizing GitHub Models usage:

- **Local-first** for mining, search, graph rebuilds, and recall
- **GitHub Models only** for durable knowledge compilation
- **No transcript dumping** into the wiki
- **No query-time re-synthesis unless the wiki genuinely lacks coverage**

The target outcome is: **good session outputs become wiki knowledge once, then future sessions read from memory/wiki instead of calling the model again.**

---

## Constraints

1. **No separate LLM API keys** — only `GITHUB_MODELS_TOKEN`
2. **Copilot Pro+ is the budget envelope** — treat GitHub Models as scarce enough to route carefully
3. **MemPalace mining must remain local** — no model calls in the live memory loop
4. **labs-wiki remains canonical** for compiled knowledge
5. **copilot_sessions remains raw memory**, not a second wiki

---

## Current State

### Already true

- `mempalace mine` is local-only (hashing, parsing, embedding, ChromaDB)
- `mempalace-watcher.py` keeps `copilot_sessions`, `homelab`, `labs_wiki`, and `nba_ml_engine` fresh without LLM calls
- `wiki-auto-ingest` already compiles `raw/` sources via **GitHub Models**
- Copilot session checkpoints are now promoted into `labs-wiki/raw/` by:
  - `homelab/scripts/mempalace-session-curator.py`
  - `homelab/scripts/mempalace-watcher.py`
  - `homelab/scripts/mempalace-remine.sh`

### Current inefficiency risk

The pipeline is structurally correct, but it can still waste GitHub Models budget if:

- low-value sources are compiled with the same model as high-value sources
- checkpoint exports flood the ingest queue
- query-time answers rely on fresh synthesis instead of retrieval
- image/vision paths run on sources that do not need them
- duplicate raw files or near-duplicates reach the model too often

---

## Design Principles

### 1. Compile once, read many

GitHub Models should be used to turn new raw sources into durable wiki pages.
After that, retrieval should come from:

1. `wiki/hot.md`
2. `mempalace_search`
3. `wiki_search` / `wiki_read`
4. only then, fresh model-assisted synthesis if the wiki does not cover the topic

### 2. Promote summaries, not transcripts

For Copilot sessions, the correct unit of promotion is the **checkpoint markdown**:

- distilled enough to be durable
- rich enough to preserve decisions, fixes, and lessons
- small enough to avoid wasting model calls

### 3. Route by source value and cost

Not every source needs the same model quality:

- **Session checkpoints** → cheaper text-only compile path
- **Web articles / GitHub repos / code-heavy sources** → standard compile path
- **image-heavy / PDF / vision sources** → expensive path only when necessary

### 4. Keep retrieval local

The system should get smarter by reusing the wiki and MemPalace, not by
re-querying GitHub Models for repeat questions.

### 5. Preserve provenance

Every promoted checkpoint should remain traceable back to:

- session ID
- checkpoint file path
- export timestamp
- raw source file
- generated wiki pages

---

## Target Architecture

```text
Copilot session-state
  -> checkpoint markdowns
  -> session curator
  -> labs-wiki/raw/
  -> auto-ingest (GitHub Models only here)
  -> wiki pages
  -> wiki injected back into MemPalace

Future sessions:
  -> hot.md / MemPalace / wiki read first
  -> GitHub Models only on true gaps or new source compilation
```

---

## Implementation Plan

## Phase 1 — Separate cheap vs expensive compile paths

**Goal:** stop treating all raw sources equally.

### Changes

- Add source-class detection in `auto_ingest.py`:
  - `copilot-session-curator`
  - `mempalace-bridge`
  - `web/article`
  - `github-repo`
  - `pdf/image-heavy`
- Add model-routing configuration, e.g.:
  - `GITHUB_MODELS_MODEL_DEFAULT`
  - `GITHUB_MODELS_MODEL_LIGHT`
  - `GITHUB_MODELS_MODEL_VISION`
- Default behavior:
  - session checkpoints use **light text model**
  - standard sources use current default
  - vision only runs when images are present and worth analyzing

### Files likely touched

- `labs-wiki/scripts/auto_ingest.py`
- `labs-wiki/scripts/watch_raw.py`
- `homelab/compose/compose.wiki.yml`
- `labs-wiki/docs/architecture.md`
- `labs-wiki/docs/workflows.md`

### Success criteria

- checkpoint exports do not consume the same path as image-heavy research ingests
- model choice is explicit and configurable

---

## Phase 2 — Add backpressure and budget guardrails

**Goal:** avoid burning GitHub Models quota on bursts.

### Changes

- Add per-source-type queueing / concurrency controls:
  - maximum concurrent ingest jobs
  - lower concurrency for expensive paths
- Add debounce/dedup before model call:
  - source hash
  - fuzzy duplicate title check
  - pending-file suppression
- Add a **soft budget mode**:
  - if queue depth is high, prefer session checkpoint backlog to wait
  - prioritize explicit user captures and high-value research sources

### Files likely touched

- `labs-wiki/scripts/watch_raw.py`
- `labs-wiki/scripts/auto_ingest.py`
- `homelab/compose/compose.wiki.yml`

### Success criteria

- bursts of session exports do not starve user-submitted research sources
- duplicate raw sources are filtered before LLM extraction

---

## Phase 3 — Make query-time behavior retrieval-first

**Goal:** save GitHub Models usage by answering from compiled knowledge.

### Changes

- strengthen the retrieval ladder in AGENTS/instructions:
  1. `hot.md`
  2. MemPalace
  3. wiki search/read
  4. model only if coverage is missing
- update wiki-query behavior to treat model synthesis as a last resort
- ensure every useful answer produces a file-back proposal rather than a repeated future synthesis

### Files likely touched

- `labs-wiki/.github/agents/wiki-query.agent.md`
- `labs-wiki/AGENTS.md`
- `projects/.github/copilot-instructions.md`
- `labs-wiki/docs/live-memory-loop.md`

### Success criteria

- repeat questions are answered from local knowledge most of the time
- model usage shifts toward new source compilation, not re-answering old topics

---

## Phase 4 — Tune session promotion for quality, not volume

**Goal:** ensure Copilot sessions produce high-signal raw sources.

### Changes

- keep checkpoint promotion as the canonical path
- add promotion heuristics:
  - minimum content length
  - title / tag-based priority
  - recent-only bootstrap
  - per-run export cap
- optionally add future promotion filters:
  - only export checkpoints mentioning code changes, incidents, architectural decisions, or merged fixes
  - skip pure planning checkpoints unless they contain durable technical decisions

### Files likely touched

- `homelab/scripts/mempalace-session-curator.py`
- `homelab/docs/12-mempalace-setup.md`

### Success criteria

- session promotion yields durable wiki concepts/syntheses, not noisy trivia
- the raw queue remains readable and reviewable

---

## Phase 5 — Add observability

**Goal:** prove the system is efficient.

### Metrics to track

- raw sources created per day by source type
- model calls per source type
- average ingest latency
- duplicate-suppression count
- queue depth during bursts
- ratio of:
  - pages compiled from new sources
  - answers served from local retrieval
  - model-assisted fresh synthesis

### Files likely touched

- `labs-wiki/scripts/watch_raw.py`
- `labs-wiki/scripts/auto_ingest.py`
- `homelab/docs/12-mempalace-setup.md`
- optional dashboard docs or Grafana panels later

### Success criteria

- session promotion remains cheap and incremental
- most repeat knowledge requests are served locally

---

## Implementation Order

1. **Phase 1** — model routing by source class
2. **Phase 2** — queue / backpressure / dedup guardrails
3. **Phase 3** — retrieval-first query discipline
4. **Phase 4** — tighter checkpoint promotion heuristics
5. **Phase 5** — metrics and dashboarding

This order matters: source classification and routing are the biggest efficiency win.

---

## Risks / Open Questions

1. **GitHub Models model availability may vary** by account/plan, so routing must degrade gracefully if only one approved model is available.
2. **Vision paths are expensive** relative to plain text extraction; image detection should be conservative.
3. **Auto-ingest queue contention** could delay high-value research sources if session promotion is too aggressive.
4. **Over-filtering checkpoints** could miss important architectural or debugging lessons.
5. **Ingest duplication** needs careful handling because watcher events can race with manual/safety-net runs.

---

## Success Definition

This plan is successful when:

1. **MemPalace and wiki stay fresh locally** without model calls
2. **GitHub Models is used primarily for compile-time knowledge creation**
3. **Copilot sessions feed the wiki through distilled checkpoints**
4. **repeat answers come from the wiki/memory stack**
5. **no new external API keys are introduced**

---

## Concrete Next Step

Implement **Phase 1** first:

- teach `auto_ingest.py` to classify incoming raw sources
- add separate model env vars for light/default/vision paths
- route `copilot-session-curator` exports to the light path by default

That is the cleanest way to make the current architecture efficient under Copilot Pro+.
