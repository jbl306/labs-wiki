# Live Memory Loop

> How labs-wiki and MemPalace stay in sync across VS Code Copilot, Copilot CLI, and OpenCode sessions — with no LLM API key beyond the existing GitHub Copilot Pro+ subscription.

## Goals

1. **Sub-minute freshness** — a decision made at 2:00pm is searchable via `mempalace_search` by 2:01pm.
2. **Uniform behavior across clients** — VS Code, Copilot CLI, and OpenCode all read the same hot cache and follow the same retrieval ladder.
3. **Zero additional LLM cost** — no paid API keys beyond Copilot Pro+.
4. **Graceful degradation** — weekly cron full-sweep catches anything the watcher missed.

## Architecture

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Copilot CLI    │  │  VS Code Copilot│  │    OpenCode     │
│  ~/.copilot/    │  │   workspace     │  │  ~/.opencode/   │
│  session-state  │  │   storage       │  │  session logs   │
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
         │ Every new session reads │  via AGENTS.md snippet
         │  wiki/hot.md first      │
         └─────────────────────────┘
```

## Components

### 1. Watcher service

- **Script:** [homelab/scripts/mempalace-watcher.py](../../homelab/scripts/mempalace-watcher.py)
- **Unit:** [homelab/scripts/mempalace-watcher.service](../../homelab/scripts/mempalace-watcher.service)
- **Behavior:** debounced (60s default); per-path mine action; refreshes `wiki/hot.md` after every mine.
- **Content-hash skip** (plan Part 5 Q1 proposed-answer): before each mine fires, a lightweight stat-based fingerprint of recently-modified files under the watched root is computed. If it matches the previous fire, the mine is skipped — this absorbs editor-metadata writes, `.git/` internal churn, and other noop events without hitting mempalace.
- **Watched paths:**
  - `~/.copilot/session-state` → wing `copilot_sessions` (convos mode)
  - `~/projects/labs-wiki/raw` → wing `labs_wiki` + wiki injection
  - `~/projects/labs-wiki/wiki` → wing `labs_wiki` + wiki injection (ignores `hot.md`)
  - `~/projects/homelab` → wing `homelab` (covers `homelab/config/opencode/` and `homelab/opencode/` — the two homelab opencode containers; user-level `~/.opencode/` is **not** watched, as it's not in use on this host)
  - `~/projects/nba-ml-engine` → wing `nba_ml_engine`

### 2. Hot cache generator

- **Script:** [scripts/build_hot.py](../scripts/build_hot.py)
- **Output:** `wiki/hot.md` — **gitignored** per plan Part 5 Q2 proposed-answer (rewritten hourly, too noisy for git).
- **Daily snapshot:** [scripts/snapshot_hot.py](../scripts/snapshot_hot.py) copies `hot.md` → `wiki/meta/hot-snapshot.md` once a day. The snapshot **is** committed, giving git history of "what was hot" without the hourly churn.
- **Size target:** ~600-1200 tokens.
- **Inputs (all free):**
  - `git log` on `wiki/` — last 10 touched pages
  - `stat` on `raw/` — last 10 captured sources
  - Frontmatter scan — pages with `tier: hot`
  - `tasks/todo.md` — first unchecked item per project
  - `mempalace wake-up --wing <W>` — L0+L1 context per active wing (compacted to ≤800 chars/wing)

### 3. Retrieval ladder

Encoded in [agents-snippet.md](agents-snippet.md) and injected into every project's `AGENTS.md`:

1. `wiki/hot.md` (always loaded)
2. `mempalace_search`
3. `wiki_search` / `wiki_read` MCP
4. Web fetch (last resort)

### 4. Manual hook substitutes (skills)

| Skill | Substitutes for | Trigger |
|-------|-----------------|---------|
| [`/wiki-save`](../.github/skills/wiki-save/SKILL.md) | Stop hook | End-of-session capture |
| [`/wiki-refresh-hot`](../.github/skills/wiki-refresh-hot/SKILL.md) | SessionStart hook | Manual hot cache refresh |

Copilot CLI and VS Code Copilot have **no native SessionStart/Stop/PreCompact hooks**. The watcher + always-loaded `hot.md` + user-invoked skills give equivalent behavior without needing them.

### 5. Weekly safety-net cron

- **Script:** [homelab/scripts/mempalace-remine.sh](../../homelab/scripts/mempalace-remine.sh)
- **Schedule:** Sunday 4am (moved from 3am so the watcher has its full week before the sweep runs).
- **Purpose:** catches orphan files the watcher missed (e.g., crashes, startup gaps) and re-runs `wiki_to_mempalace.py` injection.
- **MemPalace sync behavior:** `wiki_to_mempalace.py` upserts current wiki pages and prunes orphaned drawers for renamed/deleted pages, so `labs_wiki_knowledge` stays aligned with the filesystem.

## Installation

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

# 5. Add the hourly hot.md failsafe cron
(crontab -l 2>/dev/null; echo "17 * * * * /usr/bin/python3 /home/jbl/projects/labs-wiki/scripts/build_hot.py >> /home/jbl/logs/build-hot.log 2>&1") | crontab -

# 6. Inject the AGENTS.md snippet into every project
bash /home/jbl/projects/labs-wiki/setup.sh --inject-snippet
```

## Troubleshooting

| Symptom | Check | Fix |
|---------|-------|-----|
| Watcher not firing | `systemctl --user status mempalace-watcher` | `systemctl --user restart mempalace-watcher` |
| hot.md stale | timestamp in frontmatter | Run `/wiki-refresh-hot` or `python scripts/build_hot.py` |
| Mine thrashing (CPU high) | `journalctl --user -u mempalace-watcher -f` | Increase `MEMPALACE_WATCHER_DEBOUNCE` in the service unit |
| New project not watched | `WATCHES` list in `mempalace-watcher.py` | Add entry, restart the service |
| Self-trigger loop on hot.md | Confirm `ignore_substrings` for `labs-wiki-wiki` watch includes `hot.md` | Already in code; pull latest |

## Why this works without an LLM key

`mempalace mine` is pure local indexing: SHA hashing, markdown parsing, drawer generation, and embedding via local sentence-transformers into ChromaDB. No OpenAI/Anthropic calls. The only model-calling component — `auto_ingest.py`'s compile step — runs inside the `wiki-auto-ingest` Docker sidecar using GitHub Models (already covered by Copilot Pro+), with source-aware routing so session checkpoints can use a lighter text lane and image-bearing sources use the vision lane only when needed.

## Success criteria

1. Any new session reads `wiki/hot.md` at start (via AGENTS.md snippet).
2. `hot.md` timestamp is always within the last hour during active work.
3. `/wiki-save` → searchable via `mempalace_search` within 60 seconds.
4. Weekly full-sweep finds ≤ 5% novel content (proving the watcher caught the rest).
