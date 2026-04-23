---
title: EveryInc/compound-engineering-plugin
type: source
created: '2026-04-23'
last_verified: '2026-04-23'
source_hash: 47dca59f5e85d3b968b39b0119e3e03fe82d3bc935cfa91eaa1b03d60cf1aeeb
sources:
  - raw/2026-04-23-httpsgithubcomeveryinccompound-engineering-plugin.md
source_url: https://github.com/EveryInc/compound-engineering-plugin
tags:
  - ai-agents
  - code-review
  - compound-engineering
  - github
  - plugin
  - typescript
  - workflow-automation
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 89
concepts:
  - compound-engineering-workflow
  - cross-platform-agent-plugin-conversion
related:
  - "[[Compound Engineering]]"
  - "[[Claude Code]]"
  - "[[Copilot CLI]]"
  - "[[GitHub Copilot]]"
  - "[[OpenCode]]"
---

# EveryInc/compound-engineering-plugin

## What it is

`EveryInc/compound-engineering-plugin` is the official repository for Compound Engineering: a workflow plugin plus a Bun/TypeScript CLI that packages planning, implementation, review, and knowledge-capture routines for coding agents. The root README frames the method as an 80/20 split where most leverage comes from better planning and review, not from typing code faster. The repo ships Claude-compatible plugin manifests, dozens of reusable skills, 50+ specialist agents, and a converter/install toolchain that carries the same workflow into Codex, Copilot, OpenCode, Pi, Gemini CLI, Kiro, Cursor, Droid, and Qwen Code.

## Why it matters

For this workspace, the repo matters less as a deployable library and more as a reusable operating model for agentic development. It is directly relevant to `labs-wiki` because it formalizes the same patterns we already care about — explicit planning, specialist review, durable learnings, and cross-agent portability — and it includes native install paths for [[Copilot CLI]] plus direct compatibility with [[Claude Code]]-style plugin manifests.

## Architecture / Technical model

**Compound loop** — The core workflow is `ideate -> brainstorm -> plan -> work/debug -> code-review -> compound`. Each pass is meant to make the next unit of work cheaper by leaving behind sharper requirements, cleaner plans, and reusable learnings.

> See [[Compound Engineering Workflow]].

**Skill layer** — User-facing entry points are slash skills such as `/ce-ideate`, `/ce-brainstorm`, `/ce-plan`, `/ce-work`, `/ce-debug`, `/ce-code-review`, `/ce-compound`, and `/ce-setup`. The root README says the plugin currently ships 36 skills and 51 agents; the plugin README advertises 42+ skills and 50+ agents, so the exact catalog is still evolving.

**Agent layer** — Skills delegate to specialist subagents grouped by role: review, document review, research, design, workflow, and docs. Review alone spans security, performance, testing, data migration, maintainability, API contracts, and project-standards personas rather than a single generalist reviewer.

**Claude plugin manifest** — Source-of-truth metadata lives in `.claude-plugin/marketplace.json` for the marketplace and in `plugins/compound-engineering/.claude-plugin/plugin.json` for the plugin package itself. The manifest carries name, version, author, keywords, optional hooks, MCP server definitions, and the directories that contain agents, commands, and skills.

> See [[Cross-Platform Agent Plugin Conversion]].

**Claude plugin parser** — `src/parsers/claude.ts` resolves the plugin root, reads `.claude-plugin/plugin.json`, walks `agents/`, `commands/`, and `skills/`, parses frontmatter from Markdown components, merges hook definitions, and loads `.mcp.json` or manifest-declared MCP server config. `src/types/claude.ts` defines the in-memory schema, including `ce_platforms` filtering for skills that only apply on specific targets.

> See [[Cross-Platform Agent Plugin Conversion]].

**Converter pipeline** — The Bun CLI entry point in `src/index.ts` exposes `convert`, `install`, `list`, `cleanup`, and `plugin-path`. Under the hood, `src/converters/claude-to-{codex,copilot,droid,gemini,kiro,opencode,pi}.ts` remap Claude plugin content into target-specific bundles.

> See [[Cross-Platform Agent Plugin Conversion]].

**Target writers** — `src/targets/index.ts` registers the implemented write targets: `opencode`, `codex`, `pi`, `gemini`, and `kiro`. Each target has a dedicated writer (`src/targets/*.ts`) rather than one giant conditional exporter.

**Managed artifact layouts** — The repo is opinionated about where converted content lands. `AGENTS.md` explicitly says OpenCode output stays at `opencode.json` and `.opencode/{agents,skills,plugins}`, while the README notes Codex skills live under `~/.codex/skills/compound-engineering/` and should not spray new CE-managed files back into `~/.agents`.

> See [[Cross-Platform Agent Plugin Conversion]].

**Legacy cleanup registry** — `src/utils/legacy-cleanup.ts` and `src/data/plugin-legacy-artifacts.ts` track stale pre-v3 artifact names so upgrades can back up or remove orphaned skills and agents after naming migrations such as `git-commit -> ce-commit`.

**Local delegation config** — `.compound-engineering/config.local.example.yaml` defines per-project overrides for delegated work, including `work_delegate: codex`, consent gating, sandbox mode (`yolo` or `full-auto`), model (`gpt-5.4` by default), and effort level (`minimal` through `xhigh`).

**Durable workflow artifacts** — The repo treats brainstorms, plans, solutions, and specs as first-class outputs. `docs/brainstorms/`, `docs/plans/`, `docs/solutions/`, and `docs/specs/` are the durable memory surfaces that make the workflow compound over time.

> See [[Compound Engineering Workflow]].

## How it works

1. **Install on the target platform** — Claude Code, Copilot CLI, Cursor, Droid, and Qwen Code can consume the repo's existing Claude-compatible plugin manifests directly. Codex is a hybrid case: native plugin install handles skills, but the README still requires a Bun follow-up to install custom agents. OpenCode, Pi, Gemini CLI, and Kiro use the converter-backed install path via `@every-env/compound-plugin`.

2. **Bootstrap the project with `/ce-setup`** — After install, the workflow starts with `/ce-setup`. The repo describes this as the environment diagnostic and bootstrap pass: it checks for missing tools, wires project config, and prepares the repo for later delegation. On the implementation side, `src/utils/detect-tools.ts` probes concrete install surfaces such as `~/.codex`, `~/.copilot`, `~/.config/opencode`, `~/.pi`, `~/.factory`, `~/.gemini`, and `~/.kiro`.

3. **Turn vague work into explicit requirements** — `/ce-ideate` is the optional big-idea stage, and `/ce-brainstorm` is the first mandatory narrowing step for feature work. Instead of jumping straight into code, the workflow pushes the agent to ask questions, trim scope, and produce a right-sized requirements document in `docs/brainstorms/`.

4. **Convert requirements into an executable plan** — `/ce-plan` takes that brainstorm artifact and emits a concrete implementation plan. The point is to shrink the execution phase before any code is written: dependencies, likely edge cases, and rollout logic are surfaced here rather than halfway through implementation.

5. **Execute in a controlled workspace** — `/ce-work` handles the actual implementation phase, with worktrees and task tracking as first-class supports rather than afterthoughts. The optional local config in `.compound-engineering/config.local.yaml` lets teams route work to Codex with explicit consent, sandbox, model, and effort controls.

6. **Use a separate bug path when reality disagrees** — `/ce-debug` is the failure-oriented sibling of `/ce-work`. The README frames it as a root-cause workflow that reproduces the issue, traces causal chains, forms testable hypotheses, and fixes the real failure mode instead of just patching symptoms.

7. **Run specialist review before merge** — `/ce-code-review` dispatches a panel of narrowly scoped review agents. The plugin README lists reviewers for security, performance, maintainability, API contracts, CLI-agent readiness, data migrations, testing, project standards, adversarial failure analysis, and more. That makes the repository a concrete implementation of [[The Specialized Review Principle]] instead of a generic "review me" prompt.

8. **Capture the lesson, not just the diff** — `/ce-compound` is the loop-closing step. Once work ships, the workflow expects the agent to document what was learned so that future tasks start with stronger local context. `/ce-compound-refresh` exists to revisit stale or drifting learnings rather than letting institutional memory rot silently.

9. **Represent the plugin as data, then translate it** — For converted targets, `src/parsers/claude.ts` loads the Claude-style plugin structure into typed objects: manifest metadata, Markdown-defined agents, Markdown commands with `allowed-tools`, `SKILL.md` skills, merged hook configs, and MCP server declarations. This gives the repo a normalized internal model before any target-specific writing begins.

10. **Convert and write per target** — `src/targets/index.ts` registers implemented handlers for OpenCode, Codex, Pi, Gemini, and Kiro. The convert step maps the normalized Claude plugin into a target bundle; the writer step emits files at stable locations such as `opencode.json`, `.opencode/`, or `~/.codex/skills/compound-engineering/`, depending on platform semantics.

11. **Repair stale installs during upgrades** — `cleanup` and the legacy-artifact registries exist because target runtimes can shadow new installs with old renamed artifacts. The repo's upgrade story is therefore not just "write new files" but also "sweep old CE-managed paths into `compound-engineering/legacy-backup/` so the runtime sees the intended catalog."

12. **Repeat with better context** — The entire design assumes that every pass leaves behind better scaffolding for the next pass: clearer requirements, more accurate plans, stronger review expectations, and durable notes. That is the "compound" in Compound Engineering.

## API / interface surface

| Surface | Interface | Purpose |
|---|---|---|
| Bun CLI | `compound-plugin convert <plugin> --to <target>` | Convert a Claude-style plugin into a target bundle |
| Bun CLI | `compound-plugin install <plugin> --to <target>` | Install the converted or local plugin into the chosen target |
| Bun CLI | `compound-plugin cleanup --target <tool>` | Back up stale CE artifacts from older install schemes |
| Bun CLI | `compound-plugin list` | List available plugins/components |
| Bun CLI | `compound-plugin plugin-path <plugin> --branch <name>` | Resolve deterministic cached paths for branch-based testing |
| Core workflow skills | `/ce-ideate`, `/ce-brainstorm`, `/ce-plan`, `/ce-work`, `/ce-debug`, `/ce-code-review`, `/ce-compound`, `/ce-setup` | Ideation, requirements, planning, execution, debugging, review, knowledge capture, environment bootstrap |
| Review agents | `ce-security-reviewer`, `ce-performance-reviewer`, `ce-testing-reviewer`, `ce-maintainability-reviewer`, `ce-adversarial-reviewer`, etc. | Specialist review personas delegated by workflow skills |
| Parser model | `ClaudeManifest`, `ClaudeAgent`, `ClaudeCommand`, `ClaudeSkill`, `ClaudeHooks`, `ClaudeMcpServer` | Internal typed representation of a Claude plugin before conversion |

## Setup

```bash
# Copilot CLI native plugin install
copilot plugin marketplace add EveryInc/compound-engineering-plugin
copilot plugin install compound-engineering@compound-engineering-plugin

# Converter-backed install example
bunx @every-env/compound-plugin install compound-engineering --to opencode

# After install, inside a project
/ce-setup
/ce-brainstorm "make background job retries safer"
/ce-plan docs/brainstorms/background-job-retry-safety-requirements.md
/ce-work
/ce-code-review
/ce-compound
```

## Integration notes

This repo is a good pattern library for `labs-wiki`, `homelab`, and the booking bots whenever we want stricter planning/review structure without inventing a workflow from scratch. The most transferable pieces are the specialist review catalog, the brainstorm -> plan -> work -> compound artifact chain, and the multi-platform packaging model for teams that mix [[Claude Code]], [[Copilot CLI]], and [[OpenCode]]. It is less a runtime dependency than a reference implementation for how to package agent workflows as portable tools.

## Caveats / Gotchas

- Codex native plugin install still does **not** register custom agents by itself; the README requires a Bun follow-up until Codex's native plugin spec catches up.
- OpenCode, Pi, Gemini CLI, and Kiro installs are converter-backed, so their generated output may need to change as those host formats evolve.
- Upgrades can leave stale CE artifacts behind; the documented `cleanup` flow exists specifically to avoid old skills shadowing new ones.
- The repo reserves version bumps and release-note ownership for release automation, not for routine feature PRs.
- Pi requires `pi-subagents` and benefits from `pi-ask-user`; without them, skills that depend on subagent dispatch or blocking questions degrade.
- The maintainer explicitly says outside PRs may be useful as illustrations but are not merged directly.

## Repo metadata

| Field | Value |
|---|---|
| Stars | 15,263 |
| Primary language | TypeScript |
| Topics | compound, engineering |
| License | MIT |

## Related concepts

- [[Compound Engineering Workflow]] — the planning/review/compounding loop encoded by the plugin
- [[Cross-Platform Agent Plugin Conversion]] — how the repo treats Claude-compatible plugin definitions as source-of-truth and emits target-specific bundles
- [[The Specialized Review Principle]] — the review philosophy most directly instantiated by the plugin's specialist reviewer catalog

## Source

- Raw dump: `raw/2026-04-23-httpsgithubcomeveryinccompound-engineering-plugin.md`
- Upstream: https://github.com/EveryInc/compound-engineering-plugin
