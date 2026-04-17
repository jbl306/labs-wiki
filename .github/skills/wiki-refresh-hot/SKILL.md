---
name: wiki-refresh-hot
description: Regenerate labs-wiki/wiki/hot.md — the cross-session hot cache read by every Copilot CLI, VS Code, and OpenCode session. Zero LLM cost. Run this at session start if you suspect hot.md is stale, or after a big wiki ingest.
allowed-tools:
  - bash
  - read
---

# /wiki-refresh-hot

Regenerate the labs-wiki hot cache.

## What It Does

Runs `python ~/projects/labs-wiki/scripts/build_hot.py`. The script:

1. Pulls the last 10 wiki edits from git log.
2. Lists the last 10 sources captured to `raw/`.
3. Finds all wiki pages tagged `tier: hot` in frontmatter.
4. Extracts the current top in-progress task from each project's `tasks/todo.md`.
5. Calls `mempalace wake-up --wing <W>` for each active wing to pull L0+L1 context.
6. Writes the assembled markdown to `~/projects/labs-wiki/wiki/hot.md`.

No LLM API calls. Pure file I/O + mempalace CLI + git log. Runs in a few seconds.

## When to Use

- **Session start** — if the timestamp in hot.md is more than a few hours old and you're about to ask domain questions.
- **After big ingest** — just saved a bunch of sources via `/wiki-save` or the ingest API and want them reflected immediately.
- **Troubleshooting** — when you suspect the cross-session "recent context" isn't showing what you expect.

## When NOT to Use

- The `mempalace-watcher` systemd service already refreshes `hot.md` after every mine and there's an hourly cron failsafe. Manual refresh is only needed when you *know* the automation didn't fire (e.g., watcher was down).

## Steps

1. Run `python /home/jbl/projects/labs-wiki/scripts/build_hot.py`.
2. Read the reported size/token estimate from stdout.
3. Read `~/projects/labs-wiki/wiki/hot.md` to confirm it's well-formed.
4. Report: "hot.md refreshed (<N> bytes, ~<T> tokens)."

## Rules

- Never edit `hot.md` by hand — it's auto-generated and will be overwritten.
- If the script fails, report the error. Do not paper over it — a broken hot cache silently degrades every future session.
