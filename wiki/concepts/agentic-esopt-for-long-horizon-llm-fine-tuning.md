---
title: "Agentic ESOpt for Long-Horizon LLM Fine-Tuning"
type: concept
created: 2026-08-21
last_verified: 2026-08-21
source_hash: "d1895f71db35903195f0fd733f09cc0bf5ab228fae2764983f1c232d9d9b010d"
sources:
  - raw/2026-08-21-260817310v1pdf.md
quality_score: 91
concepts:
  - evolution-strategies
  - long-horizon-agents
  - sparse-reward-optimization
  - parameter-space-optimization
related:
  - "[[Prompt–Parameter Co-Evolution for Agentic Test-Time Compute]]"
  - "[[WebArena]]"
  - "[[Memory-Aware Test-Time Scaling]]"
tier: hot
tags: [agentic-esopt, evolution-strategies, llm-fine-tuning, sparse-rewards, long-horizon-agents]
---

# Agentic ESOpt for Long-Horizon LLM Fine-Tuning

## Overview

Agentic ESOpt is a full-parameter evolution-strategy method for adapting LLM agents that interact with an environment over many turns and often receive only a terminal or trajectory-level reward. It searches around the current model parameters with random perturbations, evaluates complete agent trajectories, and converts the resulting scalar rewards into an online parameter update without differentiating through the agent-environment interaction.

The method is motivated by two problems in long-horizon agentic reinforcement learning: full-parameter updates require substantial activation, optimizer-state, and backpropagation memory, while sparse terminal outcomes are difficult to assign to individual actions as the trajectory grows.

## How It Works

For an agent with parameters θ and external context c, the paper defines the expected trajectory return as J(θ; c). Agentic ESOpt samples a full-parameter perturbation ε from a standard Gaussian distribution and evaluates the agent at θ + σε. The resulting scalar trajectory rewards are normalized within the sampled population. The implemented update is:

```
θ_(t+1) = θ_t + (α / G) Σ_i [ normalized_reward_i * ε_i ]
```

The implementation is forward-only. It stores the random-noise seed for each perturbation and uses in-place addition and subtraction when evaluating perturbed agents, avoiding storage of a differentiable trajectory for backpropagation. The perturbation radius σ follows a cosine schedule. A larger radius early in optimization encourages exploration and supplies stronger smoothing; a smaller radius later reduces smoothing bias. Train-time runs retain a nonzero terminal radius, while test-time runs decay the terminal radius to zero.

## Why It Helps on Long Horizons

The paper’s simplified variance analysis contrasts two estimators. A policy-gradient estimator multiplies a centered terminal return by a sum of per-turn policy-score terms, so its parameter-score contribution grows with the number of turns under weak-correlation assumptions. Agentic ESOpt assigns the same terminal outcome to one coherent parameter perturbation; its parameter-score term does not contain that explicit sum over turns.

This does not make ES universally horizon-independent or guaranteed to win. Sparse rewards may still become less discriminative as tasks lengthen, and the method remains sensitive to parameter dimension, perturbation radius, population size, and the local geometry of the smoothed objective. The paper therefore presents a relative scaling argument, not a claim that total optimization variance is independent of horizon.

## Key Properties

- **Inference-level memory:** Full-parameter adaptation uses memory comparable to inference because the update is forward-only.
- **Black-box feedback:** The method needs scalar trajectory scores and does not require a differentiable environment or retained rollout graph.
- **Trajectory-level attribution:** A complete trajectory outcome is associated with a parameter perturbation rather than decomposed across every action.
- **Composability:** The same trajectory feedback can be reused by skill-space optimization and test-time search.
- **Scheduled exploration:** Cosine decay balances broad early exploration against later exploitation and reduced smoothing bias.

## Concrete Example

In the controlled Sudoku experiment, Qwen3.5-4B is trained with terminal success rewards at minimum successful horizons of 5, 10, and 15 turns. PPO leads at horizon 5, GRPO leads at horizon 10, and Agentic ESOpt leads at horizon 15 with 53.13% success versus 40.63% for the strongest GRPO configuration. The result supports a horizon-dependent crossover rather than uniform dominance.

On WebArena-Lite, the paper scales full-parameter adaptation to Qwen3.5-27B on four NVIDIA H100 80GB GPUs. Agentic ESOpt raises the No Skill dataset average from 29.47% to 36.16%, demonstrating the practical value of its inference-level memory requirement for a larger agent.

## Trade-offs and Limitations

Agentic ESOpt exchanges some backpropagation and reference-model costs for more independent environment evaluations. That exchange is favorable when model-side memory and compute dominate, but can be less favorable when environment evaluation is extremely expensive. It also introduces perturbation-radius hyperparameters, leaves continual-learning behavior unresolved, and has only preliminary evidence about how population size should scale with model capability.

## Relationship to Other Concepts

- **[[Prompt–Parameter Co-Evolution for Agentic Test-Time Compute]]** — Extends the core ES update into loops where model parameters and external context evolve together.
- **[[Memory-Aware Test-Time Scaling]]** — Provides a related view of using additional test-time interaction and trajectory information, while Agentic ESOpt adapts model parameters as an additional optimization space.
- **[[WebArena]]** — The broader benchmark family contains the WebArena-Lite evaluation used for large-model adaptation.

## Sources

- [[Agentic ESOpt: Fine-Tuning Long-Horizon LLM Agents]] — Primary paper summary and reported experiments.
