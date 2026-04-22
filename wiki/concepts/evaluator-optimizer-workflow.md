---
title: "Evaluator-Optimizer Workflow"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: ffc229d83891918f82064b92e6624a3de7bce686fc211cb123e4eb4a0cd488f1
sources:
  - raw/2026-04-22-test-html-anthropic-agents.md
related:
  - "[[Augmented LLM]]"
  - "[[Prompt Chaining Workflow]]"
  - "[[Orchestrator-Workers Workflow]]"
  - "[[The Observability Imperative]]"
  - "[[Anthropic’s 'Building Effective Agents' Guide]]"
tier: warm
tags: [evaluation, iterative-refinement, feedback-loops, llm-workflows, optimization]
---

# Evaluator-Optimizer Workflow

## Overview

The evaluator-optimizer workflow pairs one LLM that generates a candidate output with another LLM that critiques it and drives revision. It matters because some tasks improve substantially through iterative feedback, but only when the system has clear criteria for judging quality and a disciplined way to stop revising.

## How It Works

The workflow starts with role separation. One model invocation acts as the optimizer or generator, producing an initial answer, draft, plan, or search result. A second invocation acts as the evaluator, examining that output against explicit criteria. Anthropic positions this as a good fit when a human could articulate what is wrong with a draft and when an LLM can plausibly provide that same feedback. The evaluator is not there to produce a competing answer; it exists to locate weaknesses, omissions, and improvement opportunities in the current one.

The next step is rubric-driven critique. The evaluator needs a target: style guidelines, correctness constraints, completeness requirements, translation fidelity, evidence standards, or some other measurable notion of quality. Without such criteria, the loop degrades into vague self-criticism. With a rubric, the evaluator can produce actionable feedback such as "the translation preserved semantics but lost tone," "the search missed one obvious evidence source," or "the plan does not yet cover rollback." The optimizer then uses that critique to produce a revised candidate.

This creates an iterative loop:

1. Generate a candidate.
2. Evaluate it against explicit criteria.
3. Return concrete feedback.
4. Revise the candidate.
5. Stop when the output passes, stalls, or hits a budget limit.

The loop works because critique and creation place different cognitive demands on the model. A draft can be imperfect while still giving the evaluator something concrete to assess. In many domains, especially writing and research, that feedback cycle surfaces problems that would remain hidden in a single-pass response. Anthropic compares it to how a human writer iterates toward a polished result: produce, inspect, refine.

The main engineering challenge is termination. An evaluator-optimizer system can improve quality, but it can also chase diminishing returns indefinitely or oscillate between incompatible suggestions. Production systems therefore need stopping rules such as maximum rounds, minimum improvement thresholds, or "pass/fail" criteria that let the evaluator explicitly declare the output good enough. The pattern also benefits from logging each round, because evaluation loops can otherwise become opaque and difficult to debug, making [[The Observability Imperative]] especially relevant.

## Key Properties

- **Explicit critique loop**: Generation and evaluation are separated into distinct roles.
- **Criterion dependence**: The workflow works best when "better" can be defined clearly.
- **Incremental improvement**: Each round can repair defects that were invisible in the previous draft.
- **Budget sensitivity**: Quality gains must be weighed against extra latency and tokens.
- **Termination control**: Reliable stopping rules are essential to prevent runaway iteration.

## Limitations

Evaluator-optimizer loops fail when the rubric is vague, the evaluator is inconsistent, or the optimizer learns to satisfy superficial criteria without improving substance. They can also waste resources on tasks where one good pass is enough, or produce regressions if later revisions overfit evaluator preferences. When there is no meaningful standard for "better," the loop becomes expensive noise.

## Examples

Anthropic gives literary translation and complex search as strong examples.

```python
draft = writer_llm("Translate this passage into literary English.")
for _ in range(3):
    feedback = evaluator_llm(
        f"Critique this draft for tone, nuance, and fidelity:\n{draft}"
    )
    if "PASS" in feedback:
        break
    draft = writer_llm(f"Revise using this feedback:\n{feedback}\nDraft:\n{draft}")
```

The evaluator does not replace the writer. It sharpens the writer by turning implicit quality judgments into explicit revision instructions.

## Practical Applications

This workflow is effective for high-stakes writing, translation, retrieval-heavy research, plan refinement, policy drafting, and code review flows where the quality bar is high enough to justify multiple passes. It is especially useful when humans already improve the task by giving iterative feedback, because that usually signals the evaluator role can add real value.

## Related Concepts

- **[[Prompt Chaining Workflow]]**: Similar multi-step structure, but with fixed stages rather than iterative critique.
- **[[Orchestrator-Workers Workflow]]**: Can feed into evaluator-optimizer when synthesized outputs require polishing or validation.
- **[[The Observability Imperative]]**: Important for tracing why iterative refinement succeeds, stalls, or regresses.
