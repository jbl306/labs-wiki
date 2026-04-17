---
name: wiki-save
description: Save the current conversation as a labs-wiki raw source for auto-ingest. Use at the end of a meaningful debugging, planning, or research session. The mempalace-watcher will auto-mine within 60 seconds.
allowed-tools:
  - read
  - write
  - bash
---

# /wiki-save

File the current conversation as a durable labs-wiki source.

## What It Does

1. Generates a slugified filename: `raw/YYYY-MM-DD-<slug>.md` in `~/projects/labs-wiki/raw/`.
2. Writes standardized frontmatter (type, captured, source, tags, status: pending).
3. Body contains a **condensed, structured summary** of the session — not a raw transcript.
4. Exits. The `mempalace-watcher` systemd service detects the new file and mines it into the `labs_wiki` wing within ~60 seconds. The `wiki-auto-ingest` Docker sidecar separately compiles it into wiki pages.

## When to Use

- End of a non-trivial debugging session where the root cause is worth remembering.
- After landing on an architectural decision you want searchable later.
- When research uncovers a pattern that will matter across future sessions.
- When the user says "save this" / "capture this" / "remember this".

**Do NOT use for:**
- Trivial single-command sessions.
- Sessions with PII/secrets in the transcript (strip first).
- Questions the user was just asking for reference — save the *answer synthesis*, not the Q&A.

## Slug Rules

- Lowercase, hyphen-separated.
- Extract 3-6 meaningful words from the session topic.
- Strip filler (`the`, `and`, `bug`, `fix`).
- Examples:
  - Debugging Docker + Caddy 502 → `caddy-502-upstream-unhealthy`
  - Writing labs-wiki plan → `live-memory-loop-plan`
  - NBA ML feature discussion → `player-prior-regularization`

## Frontmatter Template

```yaml
---
title: "<Human-readable title>"
type: note                        # note | synthesis | research
captured: <ISO-8601 UTC>
source: wiki-save
session_client: <copilot-cli | vscode | opencode>
tags: [<3-6 domain tags>]
status: pending
---
```

## Body Structure

```markdown
# <Title>

## Context
<2-3 sentences — what prompted the session>

## Key Findings
- <Bullet each real insight, not each step>
- <Be specific: "X breaks when Y > Z" not "we discussed X">

## Decisions / Outcomes
- <What we decided and why>

## Open Questions
- <Anything still unresolved>

## References
- <File paths touched, URLs consulted, wiki pages referenced via [[wikilinks]]>
```

## Rules

- Never overwrite an existing file — if the slug collides, append `-2`, `-3`, etc.
- Keep the body under 400 lines. Reference long artifacts instead of inlining them.
- Strip secrets before writing. If unsure, prompt the user to redact.
- Do NOT manually trigger mining — the watcher handles it. Just write the file.
- If the user specifies a name (e.g. `/wiki-save as foo`), use that as the slug.

## Example Invocation

User: `/wiki-save`

You:
1. Reflect on the session, compose title + slug.
2. Write `/home/jbl/projects/labs-wiki/raw/2026-04-17-caddy-502-upstream-unhealthy.md` with frontmatter + structured body.
3. Report: "Saved → `raw/2026-04-17-caddy-502-upstream-unhealthy.md`. Auto-mine ETA ~60s; wiki compile ETA ~2-5m."
