---
title: "Copilot Session Checkpoint: Building jbl-dev-kit multiagent workflow"
type: source
created: '2026-05-30'
last_verified: '2026-05-30'
source_hash: 7b7a48368fe8d078200fe28918cd8c362958e9589982ef978feca3a9c2d5e9f8
sources:
  - raw/2026-05-30-copilot-session-building-jbl-dev-kit-multiagent-workflow-697863e5.md
tags: [copilot-session, jbl-dev-kit, multiagent-workflow, runtime-agnostic, worktrees, agent-orchestration, token-optimization]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 76
---

# Copilot Session Checkpoint: Building jbl-dev-kit multiagent workflow

## Summary

This checkpoint captures the design and early implementation of `jbl-dev-kit`, a runtime-agnostic development kit for compiling one workflow definition into Claude Code, Codex, Copilot CLI, and OpenCode artifacts. The session established the compiler-first architecture, shipped the first two implementation plans, and outlined a VM-native orchestrator based on git worktrees, headless runtime commands, and per-run token ledgers.

## Key Points

- **Primary goal**: create a new canonical repository, `~/projects/jbl-dev-kit`, that can manage agent workflows once and emit them to multiple runtimes instead of maintaining separate hand-authored setups.
- **Core architecture**: neutral Markdown+frontmatter source files in `source/` feed adapters in `compile/targets/*`, which emit runtime-specific artifacts into `dist/<runtime>/` or installation scopes.
- **Runtime coverage**: Plan 1 and Plan 2 completed support for Claude Code, Codex, Copilot CLI, and OpenCode emitters, with 11 tests passing after the second implementation pass.
- **Artifact model**: each generated item carries `name`, `kind`, `summary`, `targets`, `tier`, `model_hint`, and `tools`, giving the compiler a small normalized schema for agents, skills, commands, and context.
- **Installation scopes**: the compiler supports `dist`, `global`, and `project` targets, with global installs aimed at `~/.claude/` and `~/.codex/`, while project installs use managed blocks to preserve local repo content.
- **Managed-file behavior**: project-scope writes are designed to be idempotent through `<!-- jbl-dev-kit:start --> ... <!-- jbl-dev-kit:end -->` sections so sync and rollback can be deterministic.
- **Plan 3 direction**: the orchestrator design centers on `ledger.mjs`, `runner.mjs`, and `worktree.mjs`, introducing run IDs, metadata files, runtime-specific headless commands, and git worktree lifecycle helpers.
- **Execution stance**: the orchestrator is intended to default to dry-run planning, then require `--execute` for real runs, reducing accidental side effects in sibling repositories.
- **Token strategy**: the kit bakes in tiered context, scoped subagent prompts, and a bias toward single-agent execution until scaling is justified by the source's stated `~45%` threshold logic.
- **Open work**: the new orchestration libraries and tests had been written but not yet wired into `orchestrator.mjs`, committed, or pushed when the session checkpoint was exported.

## Key Concepts

- [[Cross-Platform Agent Plugin Conversion]]
- [[Managed-Block Layering for Cross-Repo Agent Installs]]
- [[Headless Worktree Orchestration for Agent Runtimes]]
- [[Worktree-Based Subagent-Driven Development]]
- [[The Token Economy Principle]]

## Related Entities

- **[[jbl-dev-kit]]** — the repository being designed and implemented in this session.
- **[[Copilot CLI]]** — one of the supported target runtimes and the runtime used during the session itself.
- **[[Claude Code]]** — a primary output target that influenced the kit's artifact model and global install surface.
- **[[OpenCode]]** — another emission target, notable because it requires its own directory and config shape.
- **[[MemPalace]]** — part of the surrounding knowledge workflow that informed durable checkpoint promotion and memory capture.
