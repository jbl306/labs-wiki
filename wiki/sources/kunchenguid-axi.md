---
title: kunchenguid/axi
type: source
created: '2026-04-21'
last_verified: '2026-04-22'
source_hash: 6dd89f7d2364f447f5299cd56b1ec6be904b2016a0fffce1a341595860f22d1a
sources:
- raw/2026-04-10-httpsgithubcomkunchenguidaxi.md
source_url: https://github.com/kunchenguid/axi
tags:
- github
- typescript
tier: warm
knowledge_state: ingested
ingest_method: manual-reprocess-github-2026-04-22
quality_score: 80
concepts:
- axi-design-principles-for-agent-ergonomic-cli-tools
- agent-ergonomic-tool-design-principles
---

# kunchenguid/axi

## What it is

AXI ("Agent eXperience Interface") is a set of 10 design principles for building CLI tools that LLM agents can use efficiently — not just survive. It treats the agent's token budget as a first-class constraint and ships two reference implementations: `gh-axi` (GitHub operations) and `chrome-devtools-axi` (browser automation). In its own benchmarks against Claude Sonnet 4.6, `gh-axi` hits 100% success at $0.050 average vs ~$0.148 for the GitHub MCP (425 runs, 17 tasks); `chrome-devtools-axi` hits 100% at $0.074 vs $0.101 for the equivalent MCP server (490 runs).

## Why it matters

Direct counter-position to the MCP-everywhere default. For our own custom skills and any future workspace CLI tooling (the `gh-axi` model is especially relevant given we use `gh` heavily), AXI's principles are a concrete checklist for building agent-ergonomic tools that are cheaper and faster than MCP equivalents. The `axi` skill in `npx skills add kunchenguid/axi` is a drop-in design guide.

## Key concepts

- **Token budget as a primary constraint** — The 10 principles all reduce tokens consumed per task. See [[axi-design-principles-for-agent-ergonomic-cli-tools]] and [[agent-ergonomic-tool-design-principles]].
- **TOON output format** — Token-Oriented Object Notation; ~40% smaller than JSON for the same data.
- **Minimal default schemas** — 3–4 fields per list item by default, with `--full` as an escape hatch.
- **Pre-computed aggregates** — Counts and statuses included in the default output to eliminate follow-up calls.
- **Definitive empty states** — Explicit "0 results" instead of an empty stdout.
- **Ambient context** — AXI tools self-install into session hooks so the agent sees state before invoking.
- **Content-first defaults** — Running with no args shows live data, not help text.
- **Contextual disclosure** — Each output ends with next-step suggestions.
- **Idempotent mutations + structured errors** — No interactive prompts; structured error JSON; meaningful exit codes.

## How it works

- An AXI is a normal CLI tool that conforms to the 10 principles — no runtime, no daemon.
- The agent invokes it like any other shell command; output is TOON or compact JSON.
- The agent's `CLAUDE.md` / `AGENTS.md` is told to prefer the AXI tool over the heavier MCP equivalent.
- A benchmark harness in `bench-browser/` and `bench-github/` runs head-to-head comparisons across MCP, plain CLI, and AXI conditions.
- The published `axi` skill ships SKILL.md guidelines + scaffolding for building new AXIs.

## Setup

```bash
npm install -g gh-axi
npm install -g chrome-devtools-axi

# Add the AXI design skill to your agent
npx skills add kunchenguid/axi
```

Add to `CLAUDE.md` / `AGENTS.md`:

```
Use `gh-axi` for GitHub and `chrome-devtools-axi` for browser automation.
```

## Integration notes

Reference design for any custom tool we build for the Copilot CLI / OpenCode environment. `gh-axi` is the most actionable adoption candidate — we currently lean on plain `gh` and the GitHub MCP, both of which AXI's benchmark beats on cost/latency. The `axi` skill complements `agent-ergonomic-tool-design-principles` already in our skill library.

## Caveats / Gotchas

- Benchmarks were run only with Claude Sonnet 4.6; cost/latency results may not transfer 1:1 to other models.
- AXI is a design pattern, not a framework — adopting it means refactoring tool output, not adding a dependency.
- Reference AXIs (`gh-axi`, `chrome-devtools-axi`) live in separate repos; this repo is the spec + benchmark harness.

## Repo metadata

| Field | Value |
|---|---|
| Stars | 763 |
| Primary language | TypeScript |
| Topics | (none) |
| License | (see upstream) |

## Source

- Raw dump: `raw/2026-04-10-httpsgithubcomkunchenguidaxi.md`
- Upstream: https://github.com/kunchenguid/axi
