---
title: Compound Engineering Workflow
type: concept
created: '2026-04-23'
last_verified: '2026-04-23'
source_hash: 47dca59f5e85d3b968b39b0119e3e03fe82d3bc935cfa91eaa1b03d60cf1aeeb
sources:
  - raw/2026-04-23-httpsgithubcomeveryinccompound-engineering-plugin.md
quality_score: 88
related:
  - "[[The Specialized Review Principle]]"
  - "[[Phased Implementation Planning and Progress Tracking for LLM Wikis]]"
  - "[[Cross-Platform Agent Plugin Conversion]]"
tier: hot
tags:
  - ai-agents
  - code-review
  - planning
  - workflow-design
  - knowledge-capture
---

# Compound Engineering Workflow

## Overview

The Compound Engineering Workflow is a planning-first, review-heavy agentic development loop designed so that each completed task leaves behind reusable leverage for the next one. Instead of treating engineering as a one-shot "prompt -> code" interaction, it decomposes work into ideation, requirements capture, planning, execution, review, and knowledge compounding. The key claim is that long-term velocity comes from reducing rediscovery cost, not from accelerating raw keystrokes.

## How It Works

The workflow starts from a strong bias against premature execution. In the repository's framing, most engineering value is created before code is merged: in clarifying what the task really is, in shrinking ambiguous scope, in surfacing likely failure modes, and in deciding what "good" looks like before the implementation begins. That is why the front half of the loop is dominated by `/ce-ideate`, `/ce-brainstorm`, and `/ce-plan` rather than by coding commands. The system assumes vague work produces vague code, so it spends tokens turning fuzzy intent into explicit artifacts first.

The optional `/ce-ideate` phase is the broadest aperture. It is meant for tasks where the hard part is not implementation detail but selecting which idea is worth pursuing at all. The skill generates and critiques candidate ideas, then narrows toward one that deserves requirements work. This is different from planning: ideation produces alternatives and trade-off framing, not the execution recipe itself. By separating ideation from planning, the workflow keeps "what should we build?" distinct from "how should we build it?"

Once an idea is chosen, `/ce-brainstorm` runs an interactive question-and-answer pass that tries to expose missing assumptions while the cost of changing direction is still low. The output is a requirements document rather than code. That shift matters because a requirements artifact can be reviewed, edited, versioned, and reused by later agents. It also creates a durable checkpoint that the implementation phase can be measured against. In other words, the workflow externalizes intent before it starts externalizing changes.

`/ce-plan` then transforms that requirements artifact into a structured plan. The important design choice here is that plans are treated as first-class operational objects, not as throwaway notes. Plans let the team define sequencing, likely dependencies, validation steps, and rollout concerns before the work spreads across files or services. This is where the workflow most resembles disciplined software delivery methods already used in systems like `labs-wiki`, but Compound Engineering pushes the artifact idea further by making plan generation a named, reusable capability inside the plugin rather than an ad hoc habit.

Execution is deliberately split between normal feature work and bug-oriented work. `/ce-work` handles implementation when the plan is already clear. `/ce-debug` handles failure investigation when the real challenge is establishing causal truth. The README describes `/ce-debug` as reproducing failures, tracing root causes, forming testable hypotheses, and implementing fixes against those hypotheses. That distinction is subtle but valuable: feature work optimizes for controlled progress through a plan, while debugging optimizes for epistemic rigor under uncertainty. By giving them different entry points, the workflow avoids collapsing both into the same generic "do work" prompt.

Another important element is delegation control. The local config example in `.compound-engineering/config.local.example.yaml` exposes work delegation knobs such as `work_delegate`, `work_delegate_consent`, `work_delegate_sandbox`, `work_delegate_model`, and `work_delegate_effort`. That means execution is not just a single agent doing everything directly; it can become an orchestrated system in which the project owner explicitly chooses whether and how another agent runtime should participate. This makes the workflow configurable instead of dogmatic.

Review is the quality fulcrum of the entire loop. `/ce-code-review` does not assume a single omniscient reviewer. Instead, the plugin ships a large panel of role-specific reviewers: security, performance, testing, maintainability, project standards, data migrations, CLI-agent readiness, and more. This aligns tightly with [[The Specialized Review Principle]]: the workflow tries to route each review problem to an agent whose vocabulary and anti-pattern inventory match the domain. In effect, Compound Engineering bakes review specialization into the workflow itself rather than treating it as optional polish.

The loop closes with `/ce-compound`, which is the memory-formation stage. This step is crucial because it explains the name of the method. The goal is not simply to finish the current ticket; it is to encode the learning so that the next task begins from a stronger local prior. A brainstorm makes the next brainstorm better. A plan makes future planning sharper. A review teaches future reviewers what to look for. A compound note saves the next agent from paying the same discovery cost again. The workflow is therefore recursive in the positive sense: every cycle should increase organizational context density.

This is also why the repository emphasizes durable artifact locations like `docs/brainstorms/`, `docs/plans/`, `docs/solutions/`, and `docs/specs/`. The workflow does not want learnings trapped in ephemeral chat context. It wants those learnings promoted into stable documents that can be cited, refreshed, or compared later. In that sense, the method is as much a documentation discipline as an agent discipline.

Putting all of that together, the Compound Engineering Workflow is best understood as a state machine for reducing rediscovery. It moves from idea selection to requirements, from requirements to plans, from plans to execution, from execution to specialist review, and from review to durable memory. The more faithfully a team follows the loop, the more future work inherits prior reasoning instead of reconstructing it from scratch.

## Key Properties

- **Planning-first bias**: The workflow insists on requirements and plans before substantial implementation work.
- **Separate feature and debugging lanes**: `/ce-work` and `/ce-debug` encode different epistemic modes for building versus diagnosing.
- **Specialist review as a default**: Review is delegated to narrowly scoped personas rather than a single generalist.
- **Durable artifact trail**: Brainstorms, plans, solutions, and specs become reusable project memory.
- **Configurable delegation**: Local config can control whether work is delegated, to which runtime, under what sandbox, and with what effort level.

## Limitations

The workflow adds process overhead, which can be wasteful for very small tasks where the implementation is genuinely obvious and low-risk. It also assumes teams are willing to maintain the artifact trail; if brainstorms, plans, and compound notes are generated mechanically and never revisited, the workflow degrades into ceremony. The review model depends on having good specialist prompts, so stale or weak reviewer definitions can create false confidence. Finally, the method is strongest when teams already value documentation and explicit process; in highly improvisational environments, adoption friction may be high.

## Examples

A feature request like "make background job retries safer" would move through the workflow roughly like this:

```text
/ce-ideate                           # optional, if several retry strategies are plausible
/ce-brainstorm "make background job retries safer"
/ce-plan docs/brainstorms/background-job-retry-safety-requirements.md
/ce-work
/ce-code-review
/ce-compound
```

The artifact progression matters:

1. Brainstorm identifies failure modes such as duplicate execution or infinite retry storms.
2. Plan turns those into concrete tasks such as idempotency keys, retry caps, and metrics.
3. Work implements the plan.
4. Review dispatches reliability, correctness, and performance specialists.
5. Compound records what retry safeguards and reviewer heuristics proved useful.

## Practical Applications

The workflow is well suited to teams using AI agents for non-trivial software delivery, especially when planning mistakes and repeated review misses are more expensive than the overhead of an extra artifact or two. It fits internal tooling, platform engineering, backend feature work, and any codebase where institutional memory matters. In a workspace like `labs-wiki`, it is especially useful as a reference model for turning ephemeral agent work into durable, inspectable project knowledge.

## Related Concepts

- **[[The Specialized Review Principle]]**: Compound Engineering operationalizes this principle through its reviewer catalog.
- **[[Phased Implementation Planning and Progress Tracking for LLM Wikis]]**: Both workflows value explicit plans, but the wiki workflow is more phase-and-validation driven while Compound Engineering adds ideation and compounding.
- **[[Cross-Platform Agent Plugin Conversion]]**: This is the packaging layer that makes the workflow portable across agent runtimes.

## Sources

- [[EveryInc/compound-engineering-plugin]] — primary source for the workflow definition and skill inventory
