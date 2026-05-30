---
title: "Headless Worktree Orchestration for Agent Runtimes"
type: concept
created: 2026-05-30
last_verified: 2026-05-30
source_hash: "7b7a48368fe8d078200fe28918cd8c362958e9589982ef978feca3a9c2d5e9f8"
sources:
  - raw/2026-05-30-copilot-session-building-jbl-dev-kit-multiagent-workflow-697863e5.md
related:
  - "[[Worktree-Based Subagent-Driven Development]]"
  - "[[Orchestrator-Workers Workflow]]"
  - "[[The Token Economy Principle]]"
tier: hot
tags: [worktrees, orchestration, headless-execution, runtime-agnostic, token-ledger, automation]
---

# Headless Worktree Orchestration for Agent Runtimes

## Overview

Headless worktree orchestration is a runtime-neutral execution pattern in which coding agents are launched non-interactively against isolated git worktrees, with each run recorded as an explicit artifact. In the jbl-dev-kit checkpoint, this concept matters because the project is not only compiling workflow files across runtimes; it is also trying to run those runtimes safely from a homelab VM against sibling repositories.

## How It Works

The pattern starts from a simple operational constraint: if an agent is going to modify a real repository unattended, the system needs a safer boundary than "run the command in the main checkout and hope for the best." Git worktrees provide that boundary. A worktree gives the orchestrator a fresh directory attached to a dedicated branch, so a headless agent can inspect files, stage changes, run tests, and leave artifacts without touching the user's primary working tree. In the checkpoint, that boundary is wrapped by `worktree.mjs`, which exposes `isClean(repoPath)`, `addWorktree(repoPath, worktreePath, branch)`, and `removeWorktree(...)`. The presence of `isClean()` is important: the orchestration model assumes the tool should refuse or warn before branching from a dirty repository state.

The second layer is run bookkeeping. The source lists `ledger.mjs` as the module responsible for `makeRunId(jobName)`, `createRun(runsDir, meta)`, `finalizeRun(dir, result)`, `readRun(dir)`, and `parseTokens(output)`. This means a job is not treated as an ephemeral subprocess call; it becomes a structured record stored under `orchestrator/runs/<id>/metadata.json`. That decision has several consequences. It makes runs inspectable after the fact, lets the orchestrator provide a `list` view instead of relying on shell history, and turns cost accounting into a first-class feature because token usage can be parsed and attached to the run record. In a multi-agent system, observability is usually the difference between a debuggable tool and a spooky one.

The third layer is runtime adaptation. The checkpoint's `runner.mjs` introduces `buildCommand(runtime, {prompt, model})`, which normalizes the headless entry points for several agents: Claude uses `-p`, Codex uses `exec`, Copilot uses `-p`, and OpenCode uses `run`, with per-runtime model flags such as `--model` or `-m`. This is a smaller problem than full workflow compilation, but it matters just as much operationally. A headless orchestrator cannot rely on one universal command-line interface. It needs a deterministic translation layer that can turn one orchestration request into the right invocation for each host. That keeps the higher-level job planner runtime-agnostic while acknowledging that the actual CLIs are not.

The source also indicates a deliberate dry-run bias. The intended `orchestrator.mjs` rewrite was supposed to default to printing the planned steps and require `--execute` before it actually adds worktrees, spawns processes, or mutates anything. This is a strong design choice. In automation systems, dry-run is often treated as documentation sugar. Here it acts as a policy boundary. The orchestrator is expected to create the run record, verify preconditions, describe which branch and worktree it would create, show which runtime command it would invoke, and only then proceed when the operator explicitly opts in. That lowers the blast radius in a homelab setting where one mistake could affect multiple sibling repos.

A full execution path under this model looks like a deterministic state machine. First, the orchestrator creates a run directory and writes metadata such as job name, target repo, chosen runtime, model, and timestamps. Second, it checks whether the source repo is clean enough to branch from. Third, if execution is enabled, it creates a temporary worktree and branch. Fourth, it builds the runtime-specific headless command and spawns it inside that worktree. Fifth, it captures stdout and stderr into the run directory, extracts token usage when the runtime exposes it, and finalizes the run record with outcome metadata. Sixth, it may clean up the worktree or preserve it for inspection depending on flags. Even before the CLI is fully wired, the checkpoint already defines almost every component needed for this loop.

What makes this concept distinct from [[Worktree-Based Subagent-Driven Development]] is that the emphasis is not on parallel human-supervised feature branches or review workflows. It is on **repeatable, non-interactive job execution** with strong metadata capture. The worktree is no longer just a collaboration aid; it becomes an execution sandbox. Likewise, it differs from the generic [[Orchestrator-Workers Workflow]] because the dynamic LLM decomposition pattern is not the core issue here. The central issue is operational harnessing: isolating filesystem effects, adapting to multiple CLIs, and leaving behind enough run state that the system can be audited or resumed.

The token-ledger piece matters for strategy as well as logging. The checkpoint explicitly ties the project to tiered context and a "single-agent first" scaling posture. If every run records its token profile, the orchestrator can eventually compare workflows empirically rather than ideologically. That is exactly the kind of measurement discipline advocated by [[The Token Economy Principle]]: scale when the data justifies it, not just because parallelism sounds more advanced.

In condensed form, the execution loop is:

```text
create run record
  -> verify repo cleanliness
  -> create isolated worktree/branch
  -> build runtime-specific headless command
  -> execute and capture output
  -> parse token usage
  -> finalize run metadata
  -> optionally clean up worktree
```

## Key Properties

- **Isolated execution surface:** each job can run inside its own git worktree rather than the main checkout.
- **Runtime-neutral planner:** orchestration logic stays generic while `buildCommand()` handles CLI differences.
- **Run observability:** metadata, logs, and token counts are stored per run.
- **Dry-run by default:** mutation requires an explicit execution switch.
- **Lifecycle hooks:** worktree creation, run finalization, and cleanup are modeled as explicit steps.

## Limitations

This approach depends on git worktrees being available and on the target repo being branchable from a stable state. Runtime CLIs may expose different output formats, so token parsing can be fragile until standardized. Headless execution also narrows the feedback channel compared with interactive sessions; if a runtime expects live input or ambiguous approval prompts, the orchestrator must either emulate them or fail fast. Finally, preserving worktrees for debugging can consume disk space if cleanup policy is not enforced.

## Examples

```text
job: "upgrade-agent-skill-routing"
runtime: "copilot"
repo: "~/projects/labs-wiki"
mode: dry-run

1. createRun(...)
2. isClean("~/projects/labs-wiki")
3. would add worktree ".worktrees/upgrade-agent-skill-routing"
4. would run: copilot -p --model gpt-5.4 "<prompt>"
5. write planned command + metadata to orchestrator/runs/<id>/
```

With `--execute`, the same plan becomes a real subprocess run inside the isolated worktree.

## Practical Applications

Headless worktree orchestration is well suited to homelab job runners, scheduled maintenance agents, multi-repo batch updates, and evaluation harnesses where agent runs must be reproducible and inspectable. It is especially useful when one workspace mixes several coding runtimes but wants one job runner, one audit trail, and one safe execution model.

## Related Concepts

- **[[Worktree-Based Subagent-Driven Development]]**: both use git worktrees, but headless orchestration focuses on unattended execution and run capture.
- **[[Orchestrator-Workers Workflow]]**: orchestration here is operational rather than primarily decomposition-driven.
- **[[The Token Economy Principle]]**: token ledgers make scaling decisions measurable instead of intuitive.

## Sources

- [[Copilot Session Checkpoint: Building jbl-dev-kit multiagent workflow]] — primary source for the run ledger, command builder, and worktree-based orchestrator design.
