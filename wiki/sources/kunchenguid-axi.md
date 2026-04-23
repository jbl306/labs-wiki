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
- agent-ergonomic-cli
- design-principles
tier: warm
knowledge_state: ingested
ingest_method: manual-deepen-github-2026-04-22
quality_score: 53
concepts:
- axi-design-principles-for-agent-ergonomic-cli-tools
---

# kunchenguid/axi

## What it is

AXI ("Agent eXperience Interface") is a set of 10 design principles for building CLI tools that LLM agents can use efficiently — not just survive. It treats the agent's token budget as a first-class constraint and ships two reference implementations: `gh-axi` (GitHub operations) and `chrome-devtools-axi` (browser automation). In its own benchmarks against Claude Sonnet 4.6, `gh-axi` hits 100% success at $0.050 average vs ~$0.148 for the GitHub MCP (425 runs, 17 tasks); `chrome-devtools-axi` hits 100% at $0.074 vs $0.101 for the equivalent MCP server (490 runs).

## Why it matters

Direct counter-position to the MCP-everywhere default. For our own custom skills and any future workspace CLI tooling (the `gh-axi` model is especially relevant given we use `gh` heavily), AXI's principles are a concrete checklist for building agent-ergonomic tools that are cheaper and faster than MCP equivalents. The `axi` skill in `npx skills add kunchenguid/axi` is a drop-in design guide.

## Architecture / Technical model

**AXI is a design pattern, not a framework** — No runtime, no daemon, no wire protocol. It's a checklist for building agent-ergonomic CLI tools.

> See [[axi-design-principles-for-agent-ergonomic-cli-tools]] for the full 10 principles.

**TOON (Token-Oriented Object Notation)** — Custom output format achieving ~40% token savings over JSON. Compact, tabular, agent-readable. Example: `tasks[2]{id,title,status}: "1",Fix bug,open \n "2",Add feat,closed`. Spec at [toonformat.dev](https://toonformat.dev/).

**Minimal default schemas** — List outputs default to 3–4 fields (e.g. `id`, `title`, `status`, `updated_at`). Full schemas available via `--full` or `--fields id,title,body,labels`.

**Pre-computed aggregates** — Counts and status summaries included in default output. Example: `issues[3]{...} total=47 open=12 closed=35`. Eliminates follow-up calls for summary stats.

**Definitive empty states** — Explicit "0 results" with context. Never ambiguous empty stdout. Example: `issues[0] query="label:bug" total=0`.

**Idempotent mutations + structured errors** — Mutations succeed if desired state already exists (exit 0). Errors output structured text on stdout: `error: --title required\nhelp: gh-axi issues create --title "..." --body "..."`. No interactive prompts. Non-zero exit codes only for genuine failures.

**Ambient context via session hooks** — AXI tools can self-install into agent session start hooks, providing compact dashboards before the agent acts. Example: `gh-axi` hook outputs repo state, PR count, CI status in 5 lines.

**Content-first defaults** — Running with no args shows live data, not help. `gh-axi` shows current repo summary. `gh-axi --help` for help text.

**Contextual disclosure** — Each output ends with next-step suggestions: `try: gh-axi pr list`, `see: gh-axi issue 42`.

**Consistent help** — Concise per-subcommand reference. `gh-axi issues --help` shows only issues subcommands, not global options.

## How it works

**Design, not deployment**:
1. Build a normal CLI tool (Node, Python, Go, Rust, whatever).
2. Apply the 10 AXI principles to output format, error handling, defaults, and help text.
3. Agent invokes it like any shell command — no special protocol.

**Reference implementations**:
- `gh-axi` — GitHub operations (issues, PRs, repos, releases)
- `chrome-devtools-axi` — Browser automation via Chrome DevTools Protocol

**Benchmarking**:
- Harnesses in `bench-browser/` and `bench-github/` compare AXI vs MCP vs plain CLI across 14–17 tasks, 5 repeats per condition.
- Metrics: success rate, average cost, average duration, average turns.
- LLM judge grades results for correctness.
- Published results: 490 runs (browser), 425 runs (GitHub).

**Browser benchmark** (Claude Sonnet 4.6, 490 runs):
| Condition | Success | Avg Cost | Avg Duration | Avg Turns |
|---|---|---|---|---|
| **chrome-devtools-axi** | **100%** | **$0.074** | **21.5s** | **4.5** |
| dev-browser | 99% | $0.078 | 28.6s | 4.9 |
| agent-browser | 99% | $0.088 | 24.6s | 4.8 |
| chrome-devtools-mcp-compressed | 100% | $0.091 | 29.7s | 7.6 |
| chrome-devtools-mcp-search | 99% | $0.096 | 29.4s | 7.5 |
| chrome-devtools-mcp | 99% | $0.101 | 26.0s | 6.2 |
| chrome-devtools-mcp-code | 100% | $0.120 | 36.2s | 6.4 |

**GitHub benchmark** (Claude Sonnet 4.6, 425 runs):
| Condition | Success | Avg Cost | Avg Duration | Avg Turns |
|---|---|---|---|---|
| **gh-axi** | **100%** | **$0.050** | **15.7s** | **3** |
| gh (CLI) | 86% | $0.054 | 17.4s | 3 |
| GitHub MCP | 87% | $0.148 | 34.2s | 6 |
| GitHub MCP + ToolSearch | 82% | $0.147 | 41.1s | 8 |
| MCP + Code Mode | 84% | $0.101 | 43.4s | 7 |

**Takeaway**: AXI wins on all three axes: **higher success rate**, **lower cost**, **fewer turns**.

## API / interface surface

### The 10 Principles (quick reference)

1. **Token-efficient output** — Use TOON format (~40% savings over JSON)
2. **Minimal default schemas** — 3–4 fields per list item, not 10
3. **Content truncation** — Truncate large text with size hints; `--full` for complete
4. **Pre-computed aggregates** — Include counts/statuses to eliminate round trips
5. **Definitive empty states** — Explicit "0 results", never ambiguous empty output
6. **Structured errors & exit codes** — Idempotent mutations, structured errors, no interactive prompts
7. **Ambient context** — Self-install into session hooks; agents see state before invoking
8. **Content first** — No args shows live data, not help text
9. **Contextual disclosure** — Include next-step suggestions after each output
10. **Consistent way to get help** — Concise per-subcommand reference when needed

### gh-axi CLI surface

```bash
gh-axi                      # show repo summary (content-first)
gh-axi issues               # list issues (minimal schema)
gh-axi issues --full        # list issues (full schema)
gh-axi issues --fields id,title,labels  # custom fields
gh-axi issue 42             # show issue #42
gh-axi issue 42 --full      # show issue #42 with full body
gh-axi pr list              # list PRs
gh-axi pr 10                # show PR #10
gh-axi repo info            # show repo metadata
gh-axi releases             # list releases
```

### chrome-devtools-axi CLI surface

```bash
chrome-devtools-axi navigate <url>
chrome-devtools-axi click <selector>
chrome-devtools-axi type <selector> <text>
chrome-devtools-axi screenshot [--selector <sel>]
chrome-devtools-axi eval <js-expression>
chrome-devtools-axi wait-for <selector>
```

### AXI skill (for building your own)

```bash
npx skills add kunchenguid/axi
# Installs .agents/skills/axi/SKILL.md
# Contains: design guidelines, TOON spec, examples for each principle
```

## Setup

```bash
# Install reference AXI tools
npm install -g gh-axi
npm install -g chrome-devtools-axi

# Add AXI design skill to your agent
npx skills add kunchenguid/axi
```

Add to `CLAUDE.md` or `AGENTS.md`:

```markdown
Use `gh-axi` for GitHub operations and `chrome-devtools-axi` for browser automation.
```

### Building your own AXI

The `axi` skill (`.agents/skills/axi/SKILL.md`) provides:
- Full specification of each principle with examples
- TOON format grammar
- Structured error format
- Session hook template
- Anti-patterns to avoid (verbose JSON, missing aggregates, ambiguous empty states, etc.)

## Integration notes

**Direct counter-position to MCP** — AXI's benchmarks show 2–3× cost savings and higher success rates vs MCP for the same tasks. For custom workspace tools, apply AXI principles instead of wrapping in MCP.

**Adoption candidates**:
- `gh-axi` replaces plain `gh` + GitHub MCP for our GitHub workflows
- Custom CLIs for labs-wiki, homelab ops, nba-ml-engine — apply AXI principles at design time
- Skill design: `axi` skill complements existing `agent-ergonomic-tool-design-principles` in our skill library

**When not to use AXI**:
- Human-facing tools where verbosity aids understanding
- Tools that already output structured JSON consumed by other programs (not agents)
- Highly interactive workflows (AXI forbids interactive prompts — by design)

## Caveats / Gotchas

- **Benchmarks are Claude Sonnet 4.6-specific** — Cost/latency gains may not transfer 1:1 to other models (GPT-4, Gemini, etc.). Sonnet's token pricing and context handling are the baseline.
- **AXI is a design pattern, not a framework** — No `npm install axi` runtime. You refactor tool output yourself. The `axi-sdk-js` exists but is minimal (v0.1.4, April 2026) — just argument parsing helpers.
- **TOON spec is informal** — No formal grammar document yet; examples in README and skill are the spec. TOON is not a registered IANA media type.
- **Session hook installation is manual** — Tools don't auto-install hooks; agents or users must configure them. No standard hook API across agent platforms (Claude Code, OpenCode, etc.).
- **Reference AXIs live in separate repos** — `gh-axi` at github.com/kunchenguid/gh-axi, `chrome-devtools-axi` at github.com/kunchenguid/chrome-devtools-axi. This repo is spec + benchmarks only.
- **Open issues**: #32 (JSON output mode?), #31 (Google Workspace AXI feedback).

## Repo metadata

| Field | Value |
|---|---|
| Stars | 763 |
| Primary language | TypeScript (93.8%), HTML (5.8%), JavaScript (0.4%) |
| Topics | (none) |
| License | (see upstream — not specified in dump) |
| Latest release | axi-sdk-js v0.1.4 (2026-04-03) |
| Contributors | ~5 (kunchenguid, themightychris, others) |
| Benchmark harnesses | bench-browser/ (490 runs), bench-github/ (425 runs) |
| Published results | bench-browser/published-results/report.md, bench-github/published-results/STUDY.md |

## Related concepts

- [[axi-design-principles-for-agent-ergonomic-cli-tools]] — full treatment of the 10 principles

## Source

- Raw dump: `raw/2026-04-10-httpsgithubcomkunchenguidaxi.md`
- Upstream: https://github.com/kunchenguid/axi
- Website: https://axi.md
- TOON spec: https://toonformat.dev
- Skill definition: `.agents/skills/axi/SKILL.md`
- Browser benchmark study: bench-browser/published-results/STUDY.md
- GitHub benchmark study: bench-github/published-results/STUDY.md
