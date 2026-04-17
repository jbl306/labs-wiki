---
name: wiki-save-before-compact
description: Snapshot the current task state to a MemPalace drawer BEFORE Copilot auto-compacts the conversation (which happens at ~95% tokens). Use when you notice the context window filling up on a long debugging/design session and you need the current state to survive the compaction.
allowed-tools:
  - read
  - write
  - bash
---

# /wiki-save-before-compact

Snapshot in-flight task state before Copilot auto-compacts.

## What It Does

1. Writes a **compact, structured summary** of the current task state to `~/projects/labs-wiki/raw/YYYY-MM-DD-precompact-<slug>.md`.
2. Frontmatter marks it `type: precompact-snapshot` so `auto_ingest.py` treats it as ephemeral-but-indexable.
3. The `mempalace-watcher` service picks it up within ~60s and mines it into the `copilot_sessions` wing (room: `planning`).
4. After the auto-compact, the new session can immediately `mempalace_search` for the snapshot to restore state.

## When to Use

Copilot has **no PreCompact hook**. You must invoke this manually when:

- The session has been running a while on one task and context is getting heavy.
- You're about to do something risky (major refactor, multi-file edit) and want a rollback marker.
- The user says "save the state" or "we're getting compacted soon".

If the user hasn't asked and the session is short: don't use this — it's noise.

## What to Capture

The snapshot must be **sufficient to resume the task cold**. Include:

1. **Task definition** — what are we trying to do, in one paragraph.
2. **Decisions made this session** — bullet list, each with rationale.
3. **Files touched** — paths, what was changed, why.
4. **Open action items** — specific next steps for a fresh agent to pick up.
5. **Active hypotheses / dead ends** — what we tried, what's ruled out.
6. **Key references** — file paths, URLs, wiki pages, related drawers.

Do **not** include: verbatim transcripts, raw tool output, full file contents. Summarize.

## Frontmatter Template

```yaml
---
title: "Pre-compact snapshot: <task summary>"
type: precompact-snapshot
captured: <ISO-8601 UTC>
source: wiki-save-before-compact
session_client: <copilot-cli | vscode>
task_id: <short-slug>
status: in-progress
tags: [<relevant domain tags>]
---
```

## Body Structure

```markdown
# Pre-compact snapshot: <task>

## Task
<One paragraph>

## Decisions This Session
- <decision — rationale>

## Files Touched
| Path | Change | Reason |
|------|--------|--------|
| ... | ... | ... |

## Open Action Items
- [ ] <specific next step>

## Hypotheses
- ✅ <confirmed>
- ❌ <ruled out>
- ⏳ <still testing>

## References
- <wiki / drawer / URL>
```

## Rules

- **Never overwrite.** If a snapshot for the same task already exists today, append `-2`, `-3`.
- **Keep it under 300 lines.** Link to long artifacts; don't inline them.
- **No secrets.** Redact before writing.
- **Do not manually mine.** The watcher handles it — just write the file and report.
- After writing, tell the user: "Pre-compact snapshot saved → `raw/<filename>`. Searchable in `copilot_sessions/planning` within ~60s."
