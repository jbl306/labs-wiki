---
title: jbl-dev-kit
type: entity
created: 2026-05-30
last_verified: 2026-05-30
source_hash: 1e5d1918b741d826e423e9404d456c2e9d9b94ea731fae6a5591d18f7669ee34
sources:
  - raw/2026-05-30-copilot-session-building-jbl-dev-kit-multiagent-workflow-697863e5.md
  - raw/2026-05-30-copilot-session-extending-jbl-dev-kit-workflow-toolkit-c56bdb5a.md
concepts:
  - managed-block-layering-cross-repo-agent-installs
  - headless-worktree-orchestration-agent-runtimes
  - cross-platform-agent-plugin-conversion
  - provenance-stamped-managed-blocks-upgrade-safe-agent-installs
  - dry-run-llm-council-orchestration-multi-runtime-agents
related:
  - "[[Copilot CLI]]"
  - "[[Claude Code]]"
  - "[[OpenCode]]"
  - "[[MemPalace]]"
  - "[[GitHub Copilot]]"
tier: hot
tags: [multiagent, runtime-agnostic, developer-tooling, nodejs, worktrees, orchestration, compiler]
---

# jbl-dev-kit

## Overview

jbl-dev-kit is a runtime-agnostic toolkit for agent-driven software development across sibling repositories in `~/projects`. Instead of hand-maintaining separate instructions, skills, and agent files for each host runtime, the project treats workflow content as normalized source material that can be compiled into runtime-specific outputs for Claude Code, Codex, Copilot CLI, and OpenCode.

The newer checkpoint shows the repository has already moved beyond the initial compiler sketch. Two implementation batches are complete, the test suite has climbed to 47/47 green, and the remaining roadmap is focused on operational polish: provenance-stamped installs, stronger token accounting, Copilot custom-agent emission, and a dry-run-first LLM council mode. In that sense, jbl-dev-kit combines a workflow compiler, an installer, and a VM-native orchestration layer into one system.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tooling repository & workflow kit |
| Created | 2026-05-30 |
| Creator | jbl with Copilot CLI |
| URL | N/A |
| Status | Active |

## Architecture

The checkpoint describes a compiler-first architecture. Neutral Markdown and YAML-frontmatter assets live in `source/`, then flow through `compile/targets/*` adapters that emit runtime-specific artifacts. The normalized artifact schema includes `name`, `kind`, `summary`, `targets`, `tier`, `model_hint`, and `tools`, giving the project one small contract that can be rendered into several host-specific file layouts.

The emitted surfaces differ by runtime. Claude output folds context and skills into `CLAUDE.md` and companion `.claude/agents/` and `.claude/commands/` files. Codex uses a single `AGENTS.md`. Copilot initially targeted `.github/copilot-instructions.md` plus `.github/skills/<name>/SKILL.md`, and the newer checkpoint proposes extending that target to `.github/agents/<name>.agent.md` custom agents so GitHub Copilot can consume first-class specialized agents rather than only prose folding. OpenCode uses `.opencode/skills/<name>/SKILL.md` and `.opencode/opencode.json`. This keeps source authoring unified while preserving each runtime's conventions.

## Install Model

One of jbl-dev-kit's differentiators is its layered install model. The compiler supports `dist`, `global`, and `project` scopes. Global install targets are meant to turn the kit on across all `~/projects` repositories by writing into user-level runtime directories such as `~/.claude/` and `~/.codex/`.

Project installs are more conservative. The checkpoints state that they use managed blocks of the form `<!-- jbl-dev-kit:start --> ... <!-- jbl-dev-kit:end -->`, written through `writeManagedFile()`, so generated content can be inserted idempotently without trampling repo-local hand-written material. The newer checkpoint extends that design with optional provenance stamps in the opening marker, allowing blocks to expose which toolkit version and date wrote them without changing payload comparisons.

## Orchestration Model

The repo's second major surface beyond compilation is a headless orchestrator. The source lists `ledger.mjs`, `runner.mjs`, and `worktree.mjs` as the core modules: ledger stores run IDs and token metadata, runner builds headless commands for Claude, Codex, Copilot, and OpenCode, and worktree helpers isolate execution in sibling repositories.

This orchestration model is deliberately safety-biased. The initial checkpoint's intended next step was to rewrite `orchestrator.mjs` so it defaults to dry-run planning, only performs real work when `--execute` is present, checks for clean repositories before branching, and records the run before and after execution. The later checkpoint keeps that stance and extends it further with a planned council mode where multiple runtimes answer independently and a chairman runtime synthesizes only after an explicit execution gate.

## Implementation Progress

The source history now documents two completed implementation batches beyond the original architecture work. The first batch added gate-aware orchestration, a pack selector, four new agent roles, five process skills, and a lessons/compound loop, bringing the suite to 33 tests. The second batch added policy-aware adapter outputs, Claude model/tool mapping, lint, doctor, sibling repo discovery, and CI, bringing the suite to 47 tests.

That progress matters because it changes the meaning of the repo. jbl-dev-kit is no longer just an idea for portable agent instructions. It already has a compiler pipeline, adapter-specific policy handling, operational tooling, and verification surfaces. The remaining work in the checkpoint is refinement rather than foundational rescue.

## Current State

At the time of the newer checkpoint, the repository had completed its first two implementation batches and was sitting at 47/47 passing tests with all changes still uncommitted on `master`. The outstanding final batch was clearly scoped: post-edit hooks, provenance-stamped managed blocks, harder ledger token parsing, Copilot custom-agent output, an LLM council prototype, two evaluation documents, a documentation refresh, and push hygiene.

That makes jbl-dev-kit a credible workspace control plane rather than a speculative toolkit. The repo already covers compile, install, lint, doctor, discover, CI, and headless orchestration primitives; the next steps are about making those primitives easier to trust, cheaper to evaluate, and better aligned with runtime-native agent surfaces.

## Related Work

jbl-dev-kit is closely aligned with [[Cross-Platform Agent Plugin Conversion]], but the sources frame it as a lighter-weight Node 20 ESM kit tailored to this workspace rather than a general marketplace plugin. It also contrasts with the repo-local approach documented in [[Custom Copilot CLI Agents]]: instead of authoring separate agent definitions directly inside each repository, jbl-dev-kit centralizes workflow authoring and distributes managed outputs to downstream repos.

## Impact

If completed as described, jbl-dev-kit becomes the workspace's control plane for portable agent workflows: one place to define instructions, one compiler to emit them across runtimes, and one orchestrator to run them headlessly or escalate them into measured multi-runtime deliberation when higher answer quality is worth the cost.
