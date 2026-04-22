---
title: "Orchestrator-Workers Workflow"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: ffc229d83891918f82064b92e6624a3de7bce686fc211cb123e4eb4a0cd488f1
sources:
  - raw/2026-04-22-test-html-anthropic-agents.md
related:
  - "[[Augmented LLM]]"
  - "[[Prompt Chaining Workflow]]"
  - "[[Evaluator-Optimizer Workflow]]"
  - "[[Intelligent Resource Orchestration for LLM Agents]]"
  - "[[Anthropic’s 'Building Effective Agents' Guide]]"
tier: warm
tags: [orchestration, worker-models, task-decomposition, llm-workflows, coding-agents]
---

# Orchestrator-Workers Workflow

## Overview

The orchestrator-workers workflow uses a central LLM to decompose a task dynamically, assign subtasks to worker LLMs, and synthesize their outputs into a final result. It matters because many real tasks are too variable for fixed pipelines: the system must discover the needed subtasks at runtime rather than rely on a predefined chain.

## How It Works

The workflow begins with an orchestrator receiving the full task and deciding how to split it. Unlike prompt chaining, the decomposition is not hardcoded. The orchestrator examines the input, identifies subproblems, determines how many workers are needed, and specifies what each worker should produce. This makes the pattern especially useful for tasks where the shape of the work changes from case to case, such as code changes touching an unknown number of files or research tasks pulling from an unknown number of relevant sources.

Once the orchestrator creates subtask briefs, workers execute them independently. Each worker can be an [[Augmented LLM]] with access to retrieval, tools, or local context appropriate to its assignment. One worker may analyze one part of a repository, another may inspect tests, and a third may summarize a design constraint. Because the workers are focused, they can operate with narrower prompts and smaller local contexts than a single monolithic agent. This reduces cognitive overload and often improves coverage.

The synthesis phase is where the workflow becomes more than simple fan-out. The orchestrator must reconcile worker outputs, detect overlap or contradiction, fill obvious gaps, and combine the results into an integrated answer or plan. That synthesis may itself require another round of decomposition if the worker outputs reveal missing dependencies. In robust implementations, the orchestrator acts as both planner and integrator, maintaining the global objective while workers specialize locally.

Anthropic highlights the distinction between this pattern and parallelization. Both can involve multiple concurrent calls, but parallelization assumes the subtasks are known in advance, while orchestrator-workers determines them dynamically from the input. That flexibility is the main benefit and the main risk. The system adapts to novel tasks better than a fixed pipeline, but it also depends heavily on the orchestrator's ability to create good subtask boundaries and avoid redundant or conflicting work.

Operationally, this workflow benefits from explicit subtask contracts, bounded worker scope, and clear synthesis criteria. Without those controls, the orchestrator can generate vague assignments, workers can duplicate effort, and the final synthesis can collapse into a shallow summary rather than a real integration. Strong observability is important here because failures may arise from planning, delegation, execution, or synthesis, and each failure mode requires a different fix.

## Key Properties

- **Dynamic decomposition**: The system chooses subtasks at runtime instead of following a fixed script.
- **Specialization**: Workers operate on narrower briefs, improving local focus.
- **Scalability**: The pattern can expand to more workers as task breadth increases.
- **Global-local split**: The orchestrator owns the whole objective while workers own bounded subproblems.
- **Flexible topology**: The workflow can adapt to tasks whose structure is not known ahead of time.

## Limitations

This pattern is more expensive and operationally complex than fixed workflows. A weak orchestrator can create poor subtasks, miss dependencies, or overwhelm synthesis with fragmented outputs. Workers may also duplicate effort or produce incompatible assumptions. When the task actually is predictable, orchestrator-workers may be unnecessary overhead compared with a simpler chained or routed design.

## Examples

Anthropic gives coding and research as canonical fits.

```python
briefs = orchestrator_llm("Break this repo task into worker assignments.")
worker_outputs = [worker_llm(brief) for brief in briefs]
final_answer = orchestrator_llm(
    f"Synthesize these worker results into one final plan:\n{worker_outputs}"
)
```

In a coding setting, one worker might inspect relevant files, another might identify tests, and another might analyze edge cases before the orchestrator integrates the findings into a coordinated change plan.

## Practical Applications

This workflow is useful for multi-file software changes, broad research tasks, due-diligence analysis, complex support cases, incident triage, and any job where the number and type of subtasks cannot be known in advance. It is especially strong when a task naturally benefits from parallel expert viewpoints but still needs centralized integration.

## Related Concepts

- **[[Prompt Chaining Workflow]]**: Uses fixed step order; orchestrator-workers discovers steps dynamically.
- **[[Evaluator-Optimizer Workflow]]**: Can be layered on top when synthesized outputs still need critique and revision.
- **[[Intelligent Resource Orchestration for LLM Agents]]**: A broader orchestration concept that overlaps with dynamic worker allocation.
