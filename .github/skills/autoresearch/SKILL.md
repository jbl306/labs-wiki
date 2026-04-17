---
name: autoresearch
description: Run a bounded multi-round research loop on a topic, ending with a filed labs-wiki source. Use when the user asks to "research X", "find out about Y", or when you need to synthesize information from multiple sources before answering. Uses current Copilot session tokens — no extra API key required.
allowed-tools:
  - read
  - write
  - bash
  - webSearch
  - fetch
---

# /autoresearch

Bounded, configurable research loop. Inspired by claude-obsidian's `/autoresearch`, re-implemented to run against the **current Copilot agent's token budget** so no extra LLM API key is needed.

## What It Does

Drives a 3-round research loop controlled by `labs-wiki/program.md`:

1. **Round 1 — Discover.** Use `wiki_search` + `mempalace_search` to check what we already know. If the wiki already covers it well (hot.md or tier:hot page exists), stop and report — no new research needed.
2. **Round 2 — Gather.** For gaps, web-fetch 3-5 authoritative sources. Prefer primary sources (papers, official docs, reference implementations) over blog posts.
3. **Round 3 — Synthesize.** Write a labs-wiki `raw/` source with structured findings, citations, confidence notes, and open questions. The watcher auto-mines it within 60s; the auto-ingest sidecar then compiles it into wiki pages.

The loop **stops early** when:

- The wiki already has a recent (< 30 day), high-quality (score ≥ 70) page on the topic.
- No authoritative sources can be found after round 2 (report gracefully, don't hallucinate).
- The user interrupts.

## When to Use

- User says "research <topic>", "find out about <X>", "compile what we know about <Y>".
- You need to answer a domain question but hot.md and mempalace_search both come up empty.
- Before recommending a technology/pattern the user hasn't referenced before.

**Do NOT use for:**
- Simple lookups with one authoritative answer already known.
- Anything covered by `hot.md` or a recent wiki page — read those instead.
- Topics outside the vault's scope (generic language syntax, etc.) — just answer from training.

## Configuration: `program.md`

The research behavior is controlled by `~/projects/labs-wiki/program.md` (create if absent). Read it **before** starting the loop; it defines:

- Preferred sources (e.g., arXiv > official docs > GitHub > blogs).
- Max rounds.
- Confidence floor before filing (e.g., "don't file if < 2 independent sources agree").
- Topics to always deep-dive vs. skim.

If `program.md` is missing, use the defaults above (3 rounds, 3-5 sources, prefer primary).

## Output

A single file: `~/projects/labs-wiki/raw/YYYY-MM-DD-<topic-slug>.md` with frontmatter:

```yaml
---
title: "<topic>"
type: research
captured: <ISO-8601 UTC>
source: autoresearch
rounds: <N>
sources:
  - url: <url-1>
    title: <title>
    quality: <primary | secondary | blog>
  - ...
confidence: <high | medium | low>
tags: [<domain tags>]
status: pending
---
```

Body sections:

```markdown
# <Topic>

## Summary
<One paragraph — the TL;DR>

## Key Findings
- <Finding — (source citation)>

## Mechanisms / How It Works
<For technical topics>

## Trade-offs
<When to use, when not to>

## Open Questions
- <Unresolved>

## Sources
<Full list with quality tags>
```

## Rules

- **Token discipline.** You're running inside the user's Copilot session. After round 2, check remaining context. If tight, compress findings aggressively in round 3.
- **Cite everything.** Every non-trivial claim needs a source tag.
- **Label confidence honestly.** Low confidence + a filed page is still useful; hallucinated certainty is harmful.
- **Don't re-research.** If wiki already has a fresh high-quality page, link to it and stop.
- **No secrets in research queries** — strip API keys / tokens from any example URLs.

## Wrap-Up

When done, report:

> Researched `<topic>` over N rounds. Filed → `raw/<filename>` (confidence: <level>, <K> sources). Auto-mine ETA ~60s; wiki compile ETA ~2-5m. Key finding: <one sentence>.
