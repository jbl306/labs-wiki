---
title: jbl-dev-kit
type: entity
created: 2026-05-30
last_verified: 2026-05-30
source_hash: 7b7a48368fe8d078200fe28918cd8c362958e9589982ef978feca3a9c2d5e9f8
sources:
  - raw/2026-05-30-copilot-session-building-jbl-dev-kit-multiagent-workflow-697863e5.md
concepts:
  - managed-block-layering-cross-repo-agent-installs
  - headless-worktree-orchestration-agent-runtimes
  - cross-platform-agent-plugin-conversion
related:
  - "[[Copilot CLI]]"
  - "[[Claude Code]]"
  - "[[OpenCode]]"
  - "[[MemPalace]]"
tier: hot
tags: [multiagent, runtime-agnostic, developer-tooling, nodejs, worktrees, orchestration, compiler]
---

# jbl-dev-kit

## Overview

jbl-dev-kit is a new repository intended to serve as a canonical, runtime-agnostic toolkit for agent-driven software development across sibling repositories in `~/projects`. Instead of hand-maintaining separate instructions, skills, and agent files for each host runtime, the project treats workflow content as normalized source material that can be compiled into runtime-specific outputs for Claude Code, Codex, Copilot CLI, and OpenCode.

The source checkpoint makes clear that the repo is not just a format converter. It also aims to support homelab-friendly, headless execution, cross-repo installation, rollback-safe project overlays, and token-optimized orchestration. In that sense, jbl-dev-kit combines a workflow compiler, an installer, and a VM-native orchestration layer into one system.

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

The emitted surfaces differ by runtime. Claude output folds context and skills into `CLAUDE.md` and companion `.claude/agents/` and `.claude/commands/` files. Codex uses a single `AGENTS.md`. Copilot output lands in `.github/copilot-instructions.md` plus `.github/skills/<name>/SKILL.md`, while OpenCode uses `.opencode/skills/<name>/SKILL.md` and `.opencode/opencode.json`. This keeps source authoring unified while preserving each runtime's conventions.

## Install Model

One of jbl-dev-kit's differentiators is its layered install model. The compiler supports `dist`, `global`, and `project` scopes. Global install targets are meant to turn the kit on across all `~/projects` repositories by writing into user-level runtime directories such as `~/.claude/` and `~/.codex/`.

Project installs are more conservative. The checkpoint states that they use managed blocks of the form `<!-- jbl-dev-kit:start --> ... <!-- jbl-dev-kit:end -->`, written through `writeManagedFile()`, so generated content can be inserted idempotently without trampling repo-local hand-written material. That choice matters because the user explicitly wanted a strategy for existing setups, rollback, and sync.

## Orchestration Model

The in-progress Plan 3 work adds a second surface beyond compilation: a headless orchestrator. The source lists three new modules. `ledger.mjs` creates run IDs, stores metadata in `orchestrator/runs/<id>/metadata.json`, and parses token usage from runtime output. `runner.mjs` builds headless commands for Claude (`-p`), Codex (`exec`), Copilot (`-p`), and OpenCode (`run`), including model flags. `worktree.mjs` wraps `git worktree` operations so sibling repositories can be run in isolated branches.

This orchestration model is deliberately safety-biased. The checkpoint's intended next step was to rewrite `orchestrator.mjs` so it defaults to dry-run planning, only performs real work when `--execute` is present, checks for clean repositories before branching, and records the run before and after execution. That makes the repo closer to an agent operations platform than a simple prompt-packaging tool.

## Current State

At the time of the checkpoint, research, evaluation, the design spec, repository scaffold, and the first two implementation plans were already complete. All four runtime emitters were working and covered by tests. The orchestration libraries and their tests existed but had not yet been run, wired into the CLI, committed, or pushed to GitHub.

## Related Work

jbl-dev-kit is closely aligned with [[Cross-Platform Agent Plugin Conversion]], but the source frames it as a lighter-weight Node 20 ESM kit tailored to this workspace rather than a general marketplace plugin. It also contrasts with the repo-local approach documented in [[Custom Copilot CLI Agents]]: instead of authoring separate agent definitions directly inside each repository, jbl-dev-kit centralizes workflow authoring and distributes managed outputs to downstream repos.

## Impact

If completed as described, jbl-dev-kit would become the workspace's control plane for portable agent workflows: one place to define instructions, one compiler to emit them across runtimes, and one orchestrator to run them headlessly in homelab-managed repos.
