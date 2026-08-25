---
title: "Prompt–Parameter Co-Evolution for Agentic Test-Time Compute"
type: concept
created: 2026-08-21
last_verified: 2026-08-21
source_hash: "d1895f71db35903195f0fd733f09cc0bf5ab228fae2764983f1c232d9d9b010d"
sources:
  - raw/2026-08-21-260817310v1pdf.md
quality_score: 87
concepts:
  - test-time-compute
  - prompt-space-optimization
  - parameter-space-optimization
  - skill-optimization
related:
  - "[[Agentic ESOpt for Long-Horizon LLM Fine-Tuning]]"
  - "[[Memory-Aware Test-Time Scaling]]"
tier: hot
tags: [test-time-compute, prompt-optimization, parameter-adaptation, skill-evolution, agentic-esopt]
---

# Prompt–Parameter Co-Evolution for Agentic Test-Time Compute

## Overview

Prompt–parameter co-evolution is an optimization pattern in which an agent’s external context and its model parameters are updated from the same trajectory data instead of keeping the model frozen throughout test-time search. In the Agentic ESOpt paper, the parameter update is supplied by forward-only evolution strategies, while an external optimizer updates a prompt, skill document, heuristic, or other context.

This pattern addresses a limitation of frozen-policy search: changing prompts can reweight behaviors already available to the model, but may not create the underlying policy changes required by a task.

## How It Works

At iteration t, the agent collects trajectories and scores in a dataset D_t. An ES update transforms model parameters using the current context:

```
θ_(t+1) = U_ES(θ_t, c_t, D_t)
```

An external update rule transforms the context using the same evidence:

```
c_(t+1) = U_c(c_t, D_t)
```

The two updates can be alternated inside an existing search scaffold. Agentic ESOpt supplies parameter-space adaptation; the outer procedure can remain responsible for skill evolution, heuristic mutation, candidate generation, or other prompt-space operations.

## Concrete Uses

- **Skill composition:** In WebArena-Lite, the paper combines a shared Agentic ESOpt parameter stage with a post-hoc Trace2Skill distillation stage. The combined Qwen3.5-27B result reaches 36.36% dataset-average success versus 33.94% for the Trace2Skill baseline. The paper explicitly describes this experiment as sequential shared-trajectory composition, not fully alternating joint optimization.
- **Automatic heuristic design:** Agentic ESOpt is attached to existing Sample and EoH procedures under matched evaluation budgets. For EoH, parameter updates are applied to mutation operators while the outer search and other operators remain intact. Across constructive and ACO-style settings, the method improves 28 of 36 matched method-budget comparisons.
- **Broader test-time scaling:** The pattern complements trajectory-based test-time exploration by making parameter adaptation another optimization dimension, alongside external skills or memories.

## Key Properties

- **Reuse of evidence:** Parameter and context updates can consume the same trajectory rewards, reducing the need for a separate data-collection pipeline.
- **Modular integration:** Existing prompt-space search procedures can be preserved, with parameter updates inserted at defined points.
- **Different adaptation scopes:** Context updates change external instructions or heuristics; parameter updates can alter the policy’s accessible behavior.
- **Budget sensitivity:** Results depend on the number of sampled directions, candidate evaluations, reward normalization, and the cost of executing the environment.
- **Partial co-evolution in current evidence:** The paper demonstrates composition and alternating-update formalism, but its WebArena skill combination is sequential and its strongest claim for fully coupled multi-step skill-parameter evolution remains future work.

## Limitations

Co-evolution increases the number of moving parts and introduces interactions between context quality, parameter updates, population size, and reward noise. It can also be expensive when each environment evaluation is costly. The paper’s reported results establish in-setting adaptation; continual learning, quantization-compatible perturbations, population scaling laws, and tightly coupled skill-parameter schedules remain open questions.

## Relationship to Other Concepts

- **[[Agentic ESOpt for Long-Horizon LLM Fine-Tuning]]** — Provides the parameter-space optimizer used in this pattern.
- **[[Memory-Aware Test-Time Scaling]]** — Explores how additional test-time trajectories can improve memory synthesis; co-evolution adds model-parameter updates to the external-context side of that loop.

## Sources

- [[Agentic ESOpt: Fine-Tuning Long-Horizon LLM Agents]] — Defines prompt-parameter co-evolution and reports WebArena-Lite and automatic-heuristic-design results.
