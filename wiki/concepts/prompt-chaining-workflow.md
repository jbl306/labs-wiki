---
title: "Prompt Chaining Workflow"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: ffc229d83891918f82064b92e6624a3de7bce686fc211cb123e4eb4a0cd488f1
sources:
  - raw/2026-04-22-test-html-anthropic-agents.md
related:
  - "[[Augmented LLM]]"
  - "[[Evaluator-Optimizer Workflow]]"
  - "[[Structured Artifact Chains]]"
  - "[[Anthropic’s 'Building Effective Agents' Guide]]"
tier: warm
tags: [prompt-chaining, workflows, llm-pipelines, decomposition, validation]
quality_score: 79
---

# Prompt Chaining Workflow

## Overview

Prompt chaining is a workflow pattern that decomposes a task into a fixed sequence of LLM calls, where each stage consumes the output of the previous stage. It matters because many tasks become easier, more reliable, and more observable when a model handles one bounded subproblem at a time instead of attempting an entire end-to-end job in a single pass.

## How It Works

Prompt chaining begins by choosing a decomposition that is stable enough to encode in software ahead of time. Rather than letting the model decide the entire execution path dynamically, the developer defines a series of stages such as plan, draft, verify, transform, or summarize. Each stage receives a narrower prompt than the full problem, and each output becomes an artifact that is passed forward. Anthropic describes this as a way to trade latency for accuracy: multiple smaller reasoning problems often outperform one large, overloaded prompt.

The key mechanism is progressive constraint. Early stages structure the task and remove ambiguity for later stages. For example, a first call may produce an outline, a second may check whether the outline meets explicit requirements, and a third may expand the approved outline into a full document. Because the steps are predetermined, developers can insert programmatic gates between them. A gate might reject malformed JSON, ensure that required sections are present, verify that a translation preserved key terms, or stop the chain entirely if a quality threshold is not met. This gives the workflow a hybrid character: LLM reasoning inside each stage, deterministic control between stages.

This structure also improves observability. Each intermediate artifact is inspectable, which means debugging does not require reading a long conversational transcript and guessing where the system drifted. If the chain fails, the failure can usually be localized to a particular step or interface boundary. That makes prompt chaining compatible with [[Structured Artifact Chains]] and other audit-friendly workflow designs. The granularity of the artifacts matters: each stage should produce something concrete enough to validate, not just vague prose that leaves the next stage underspecified.

Prompt chaining works best when the subtask boundaries are known in advance. That is the defining trade-off. The developer gains predictability, testability, and easier prompt optimization, but loses the flexibility of runtime decomposition. If the task shape changes dramatically from one input to another, a rigid chain becomes brittle. Anthropic therefore positions prompt chaining as a good fit for tasks that "cleanly decompose" into fixed subtasks, not for open-ended cases where the number and nature of subtasks must be inferred from the input itself.

In practice, the workflow is often stronger when each stage has a different contract. One call may reason broadly, another may normalize into schema-constrained output, and another may act as a verifier. The chain is not just "ask again with more text"; it is a disciplined separation of concerns. That separation makes each prompt easier to tune, each stage easier to monitor, and the entire workflow easier to evolve over time.

## Key Properties

- **Fixed decomposition**: The sequence of stages is decided in code, not invented by the model at runtime.
- **Intermediate validation**: Developers can insert gates after each stage to catch drift early.
- **Higher reliability through simplification**: Each LLM call solves a narrower problem than the full task.
- **Auditability**: Intermediate artifacts provide a trail of evidence for what happened.
- **Latency trade-off**: Reliability typically improves at the cost of multiple sequential calls.

## Limitations

Prompt chaining can introduce serial latency, amplify early-stage mistakes downstream, and become cumbersome if the chain is over-segmented. It also struggles when a task cannot be decomposed cleanly in advance or when later steps reveal that the early framing was wrong. Poorly designed stage boundaries can create handoff loss, where each step technically succeeds but the overall workflow misses the user's real goal.

## Examples

Anthropic gives two representative examples: generate marketing copy and then translate it, or write an outline, validate the outline, and then expand it into a document.

```python
outline = llm("Create an outline for the report.")
assert passes_outline_checks(outline)
draft = llm(f"Write the full report from this outline:\n{outline}")
final = llm(f"Polish the draft for executive tone:\n{draft}")
```

Each stage has a distinct responsibility, and the validation point prevents low-quality structure from contaminating the rest of the pipeline.

## Practical Applications

Prompt chaining is effective in content pipelines, summarization-and-transformation jobs, document generation, ETL-style information extraction, compliance review, and any workflow where structured intermediate artifacts improve reliability. It is also useful in coding pipelines where a model first drafts a plan or patch outline and only later writes the implementation once the structure has been checked.

## Related Concepts

- **[[Augmented LLM]]**: The primitive each stage often uses when retrieval or tools are needed.
- **[[Evaluator-Optimizer Workflow]]**: Similar in being multi-step, but centered on critique loops rather than fixed linear stages.
- **[[Structured Artifact Chains]]**: Provides the inspectable handoff discipline that makes chained workflows debuggable.
