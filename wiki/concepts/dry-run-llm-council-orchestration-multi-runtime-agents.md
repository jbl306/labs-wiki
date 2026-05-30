---
title: "Dry-Run LLM Council Orchestration for Multi-Runtime Agents"
type: concept
created: 2026-05-30
last_verified: 2026-05-30
source_hash: "1e5d1918b741d826e423e9404d456c2e9d9b94ea731fae6a5591d18f7669ee34"
sources:
  - raw/2026-05-30-copilot-session-extending-jbl-dev-kit-workflow-toolkit-c56bdb5a.md
related:
  - "[[Headless Worktree Orchestration for Agent Runtimes]]"
  - "[[The Token Economy Principle]]"
  - "[[Custom Agents in VS Code]]"
tier: hot
tags: [llm-council, multi-agent, orchestration, runtime-agnostic, token-optimization, jbl-dev-kit]
---

# Dry-Run LLM Council Orchestration for Multi-Runtime Agents

## Overview

Dry-run LLM council orchestration is a multi-agent execution pattern in which several coding runtimes answer the same task independently and a designated chairman runtime synthesizes the final plan or recommendation, but only after the orchestrator has first shown the full plan and required an explicit execution opt-in. In the jbl-dev-kit checkpoint, this concept matters because the toolkit already has the primitives for runtime-neutral command building, worktree isolation, and token ledgers; the proposed council feature turns those primitives into a deliberate escalation path rather than making multi-agent execution the default.

## How It Works

The starting point is the toolkit's existing headless runtime abstraction. jbl-dev-kit already models Claude, Codex, Copilot, and OpenCode as interchangeable execution targets through a runner layer that knows each runtime's non-interactive command shape. That means the orchestrator can formulate one high-level task and then materialize it as several concrete member commands, one per runtime. The council pattern reuses that layer instead of inventing a separate debate stack: each member is just a normal runtime invocation with a shared task envelope and possibly a model override.

What changes is the execution topology. In ordinary [[Headless Worktree Orchestration for Agent Runtimes]], one runtime acts on one task in one isolated worktree and the system records the run. In council orchestration, the orchestrator first builds a *plan of plans*: which member runtimes will answer, which prompt each will receive, where their outputs will be stored, and which chairman runtime will synthesize the result. The source explicitly says this should begin as a pure planning flow and stay dry-run by default. That is important because multi-agent execution multiplies both risk and cost. Before the toolkit spends tokens or mutates any repository state, the operator should see the member lineup and approve the run.

The checkpoint also defines the council structure in concrete terms inspired by Karpathy's "LLM council" framing: multiple members answer independently, then critique or at least provide diverse solution candidates, and a chairman LLM synthesizes the final answer. In jbl-dev-kit's context, the main value is not theatrical debate transcripts. It is controlled diversity across runtimes. Claude, Codex, Copilot, and OpenCode differ in prompt behavior, tool wiring, and model families, so independent answers can expose blind spots that a single runtime might miss. The chairman step converts that diversity into one artifact the operator can review.

The dry-run requirement shifts council mode from "parallel by default" to "escalate with intent." A dry-run council command should show at least the target repo, whether worktrees would be created, the member runtimes selected, the chairman runtime, and the estimated token multiplier. The checkpoint is explicit about the cost model: a council run is roughly `N members + 1 chairman`, not a free improvement. That cost framing aligns the feature with [[The Token Economy Principle]]. The council exists because some tasks benefit from structured diversity, not because multi-agent execution is inherently more advanced.

Operationally, a safe council flow looks like a staged pipeline. First, the orchestrator records a run and prints the plan. Second, if `--execute` is present, it creates isolated worktrees or scratch directories as needed for the participating members. Third, it launches each member runtime with the same task framing but without letting them overwrite one another's state. Fourth, it captures every member output as a durable artifact. Fifth, it builds the chairman prompt from those outputs and runs the chairman synthesis step. Sixth, it writes the synthesized recommendation back into the run ledger along with all member outputs so the operator can inspect the full evidence chain.

This artifact discipline is what keeps council mode useful. Without preserved member outputs, the chairman result becomes another opaque answer that merely *claims* to have considered alternatives. With preserved outputs, the council run becomes auditable. An operator can inspect where the chairman agreed with one member, rejected another, or merged multiple proposals. That is especially important for developer tooling, where subtle implementation trade-offs matter more than surface-level answer fluency.

The checkpoint also narrows the intended use case. The council is described as a prototype for planning and evaluation, not as the default mutation path for routine repo changes. That distinction matters. A single runtime in an isolated worktree is still the right tool for most deterministic coding jobs. Council mode becomes attractive when the task is ambiguous, high-stakes, or design-heavy: comparing architectural approaches, stress-testing a spec, or asking whether a proposed workflow change improves quality enough to justify extra tokens. In those settings, the extra cost buys epistemic diversity and a better chance of surfacing non-obvious concerns before code is written.

At a deeper level, dry-run council orchestration is a governance pattern for multi-agent systems. It takes the raw power of multi-runtime execution and wraps it in explicit planning, isolation, logging, and opt-in semantics. That makes the feature suitable for homelab and sibling-repo automation, where unbounded autonomous debate would be expensive and operationally messy. The council is not just "many agents." It is a measured escalation path with visible cost, visible structure, and visible artifacts.

## Key Properties

- **Dry-run-first execution**: the full member/chairman plan is shown before any expensive or mutating work occurs.
- **Runtime diversity**: different coding runtimes can contribute independent solution candidates to the same task.
- **Chairman synthesis**: a final runtime consolidates member outputs into one reviewable artifact.
- **Ledger-backed observability**: member outputs, token usage, and the chairman result can all be stored under one run record.
- **Escalation, not default**: council mode exists as a higher-cost option for ambiguous or high-value tasks.

## Limitations

Council mode can easily become wasteful if used on tasks that a single runtime could handle well. It also adds operational complexity: more subprocesses, more artifacts, and more opportunities for divergence in environment assumptions across runtimes. If the chairman prompt is weak, the synthesis step may wash out the strongest member insight instead of preserving it. Finally, the approach improves diversity at inference time, but it does not remove the need for good evaluation criteria; a council can still converge on a polished but wrong answer.

## Examples

```text
council plan
  target repo: ~/projects/jbl-dev-kit
  mode: dry-run
  members: claude, codex, copilot
  chairman: claude
  task: evaluate whether Copilot output should switch to .github/agents/*.agent.md

1. print member commands and estimated cost
2. if --execute, run each member in isolation
3. save member outputs under orchestrator/runs/<id>/
4. ask chairman to synthesize one recommendation
5. persist final recommendation + all evidence
```

In that example, the operator can inspect the proposed commands and decide whether the expected quality gain is worth paying for three member passes plus one chairman pass.

## Practical Applications

This pattern is most useful for architecture reviews, spec evaluation, policy trade-off analysis, and other tasks where diverse reasoning is more valuable than a single fast answer. In a toolkit like jbl-dev-kit, it is a natural fit for comparing adapter strategies, evaluating workflow quality improvements, or generating recommendation documents before making repo-wide changes.

## Related Concepts

- **[[Headless Worktree Orchestration for Agent Runtimes]]**: council mode extends single-runtime orchestration by coordinating several member runs and a synthesis pass.
- **[[The Token Economy Principle]]**: council mode is only justified when the quality gain merits the `N + 1` token multiplier.
- **[[Custom Agents in VS Code]]**: both patterns formalize specialized roles, but council orchestration focuses on runtime-level answer diversity rather than persistent workspace personas.

## Sources

- [[Copilot Session Checkpoint: Extending jbl-dev-kit workflow toolkit]] — source of the dry-run requirement, member/chairman design, and explicit token-cost warning.

