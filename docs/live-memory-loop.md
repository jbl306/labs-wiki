# Live Memory Loop

> Historical transcript-watcher architecture. Runtime configuration and service health
> are not verified by this document. Current Codex policy is owned by the global
> `AGENTS.md` and [selective checkpoint contract](codex-session-memory.md).

## Goals

1. **Sub-minute freshness** — a decision made at 2:00pm is searchable via `mempalace_search` by 2:01pm.
2. **Shared retrieval tools** — clients can use MemPalace and the curated wiki when relevant to the task.
3. **Zero model calls in the live memory loop** — mining, embedding, and hot-cache refresh stay local; only source compilation uses the configured ingest backend.
4. **Graceful degradation** — a periodic full-sweep catches anything the watcher missed.

## Architecture

The diagram below describes the existing transcript watcher path. Codex also
has a separate [selective checkpoint path](codex-durable-memory.md): the agent
stages durable Labs Wiki facts, then native Stop/PreCompact hooks save them
through the connected MemPalace server. That path does not mine transcripts or
publish wiki pages. Watcher configuration and service health were not reverified
during the 2026-09-07 checkpoint integration.

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Codex/Copilot   │  │  VS Code Copilot│  │    OpenCode     │
│ CLI sessions    │  │   workspace     │  │  ~/.opencode/   │
│ ~/.codex|copilot│  │   storage       │  │  session logs   │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │ inotify            │ inotify            │ inotify
         └────────────┬───────┴────────────────────┘
                      │
         ┌────────────▼────────────┐
         │ mempalace-watcher       │  systemd --user service
         │ (homelab/scripts/       │  60s debounce
         │  mempalace-watcher.py)  │  no LLM calls
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │ mempalace mine          │  local ChromaDB + local embedder
         │ --wing <auto-routed>    │
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │ build_hot.py            │  pure Python, no LLM
         │ → wiki/hot.md           │  git log + mtime + mempalace wake-up
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │ Optional hot-cache read │
         │  when task-relevant     │
         └─────────────────────────┘
```

## Components

### 1. Watcher service

- **Script:** [homelab/scripts/mempalace-watcher.py](../../homelab/scripts/mempalace-watcher.py)
- **Unit:** [homelab/scripts/mempalace-watcher.service](../../homelab/scripts/mempalace-watcher.service)
- **Behavior:** debounced (60s default); per-path mine action; refreshes `wiki/hot.md` after every mine.
- **Content-hash skip** (plan Part 5 Q1 proposed-answer): before each mine fires, a lightweight stat-based fingerprint of recently-modified files under the watched root is computed. If it matches the previous fire, the mine is skipped — this absorbs editor-metadata writes, `.git/` internal churn, and other noop events without hitting mempalace.
- **Watched paths:**
  - `~/.codex/sessions` and/or `~/.copilot/session-state` → wing `copilot_sessions` (convos mode)
  - `~/projects/labs-wiki/raw` → wing `labs_wiki` + wiki injection
  - `~/projects/labs-wiki/wiki` → wing `labs_wiki` + wiki injection (ignores `hot.md`)
  - `~/projects/homelab` → wing `homelab` (covers `homelab/config/opencode/` and `homelab/opencode/` — the two homelab opencode containers; user-level `~/.opencode/` is **not** watched, as it's not in use on this host)
  - `~/projects/nba-ml-engine` → wing `nba_ml_engine`

### 2. Hot cache generator

- **Script:** [scripts/build_hot.py](../scripts/build_hot.py)
- **Output:** `wiki/hot.md` — **gitignored** per plan Part 5 Q2 proposed-answer (rewritten hourly, too noisy for git).
- **Optional snapshot:** [scripts/snapshot_hot.py](../scripts/snapshot_hot.py) copies `hot.md` → `wiki/meta/hot-snapshot.md` when you want to checkpoint the hot set. The snapshot **is** committed, giving git history of "what was hot" without the hourly churn.
- **Size target:** ~600-1200 tokens.
- **Inputs (all free):**
  - `git log` on `wiki/` — last 10 touched pages
  - `stat` on `raw/` — last 10 captured sources
  - Frontmatter scan — pages with `tier: hot`
  - `tasks/todo.md` — first unchecked item per project
  - `mempalace wake-up --wing <W>` — L0+L1 context per active wing (compacted to ≤800 chars/wing)

### 3. Scoped retrieval

Global `/home/jbl/.codex/AGENTS.md` owns knowledge routing. Use MemPalace for
relevant prior sessions, the bounded Wiki MCP reader for curated research, and
current primary sources for changing external facts. `wiki/hot.md` is optional
task context. The previous mandatory startup ladder and cross-project snippet
injection are retired.

### 4. Native Codex checkpoints

Codex uses native SessionStart, Stop, and PreCompact hooks for selective Labs
Wiki memory. SessionStart supplies the policy; Stop and PreCompact save staged
facts through `mempalace_durable_hook`. See the [implementation and verification
guide](codex-durable-memory.md).

Publishing a summary as a wiki source requires explicit authorization for that content. Use an authorized [capture channel](capture-sources.md) for the selected summary. To refresh the local hot cache, run `python3 scripts/build_hot.py`.

### 5. Weekly safety-net cron

- **Script:** [homelab/scripts/mempalace-remine.sh](../../homelab/scripts/mempalace-remine.sh)
- **Schedule:** Sunday 4am (moved from 3am so the watcher has its full week before the sweep runs).
- **Purpose:** catches orphan files the watcher missed (e.g., crashes, startup gaps) and re-runs `wiki_to_mempalace.py` injection.
- **MemPalace sync behavior:** `wiki_to_mempalace.py` upserts current wiki pages and prunes orphaned drawers for renamed/deleted pages, so `labs_wiki_knowledge` stays aligned with the filesystem.

## Installation

The commands below describe the legacy watcher installation; verify the owning
homelab configuration and authorized capture scope before using them. They do
not configure the native Codex checkpoint path.

```bash
# 1. Install the systemd user service
mkdir -p ~/.config/systemd/user
cp /home/jbl/projects/homelab/scripts/mempalace-watcher.service \
   ~/.config/systemd/user/mempalace-watcher.service
systemctl --user daemon-reload
systemctl --user enable --now mempalace-watcher.service

# 2. Allow it to run while you're logged out (once per machine)
loginctl enable-linger "$USER"

# 3. Verify
systemctl --user status mempalace-watcher
tail -f ~/logs/mempalace-watcher.log

# 4. Seed hot.md for the first time
python /home/jbl/projects/labs-wiki/scripts/build_hot.py

```

## Troubleshooting

| Symptom | Check | Fix |
|---------|-------|-----|
| Watcher not firing | `systemctl --user status mempalace-watcher` | `systemctl --user restart mempalace-watcher` |
| hot.md stale | timestamp in frontmatter | Run `python3 scripts/build_hot.py` |
| Mine thrashing (CPU high) | `journalctl --user -u mempalace-watcher -f` | Increase `MEMPALACE_WATCHER_DEBOUNCE` in the service unit |
| New project not watched | `WATCHES` list in `mempalace-watcher.py` | Add entry, restart the service |
| Self-trigger loop on hot.md | Confirm `ignore_substrings` for `labs-wiki-wiki` watch includes `hot.md` | Already in code; pull latest |

## Why this works without an LLM key

`mempalace mine` is pure local indexing: SHA hashing, markdown parsing, drawer generation, and embedding via local sentence-transformers into ChromaDB. No OpenAI/Anthropic calls. The only model-calling component — `auto_ingest.py`'s compile step — runs inside the `wiki-auto-ingest` Docker sidecar through the configured ingest backend, now Codex CLI by default, with source-aware priority and reasoning-effort routing.

## Historical watcher targets

1. Retrieval is scoped to the task under the current global `AGENTS.md` policy.
2. `hot.md` timestamp is always within the last hour during active work.
3. Make an explicitly authorized wiki capture searchable via `mempalace_search` within 60 seconds.
4. Weekly full-sweep finds ≤ 5% novel content (proving the watcher caught the rest).
