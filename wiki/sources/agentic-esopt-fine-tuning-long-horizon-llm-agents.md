---
title: "Agentic ESOpt: Fine-Tuning Long-Horizon LLM Agents"
type: source
created: 2026-08-21
last_verified: 2026-08-21
source_hash: "d1895f71db35903195f0fd733f09cc0bf5ab228fae2764983f1c232d9d9b010d"
sources:
  - raw/2026-08-21-260817310v1pdf.md
quality_score: 89
concepts:
  - agentic-esopt
  - evolution-strategies
  - long-horizon-credit-assignment
  - prompt-parameter-co-evolution
related:
  - "[[Agentic ESOpt for Long-Horizon LLM Fine-Tuning]]"
  - "[[Prompt–Parameter Co-Evolution for Agentic Test-Time Compute]]"
  - "[[Memory-Aware Test-Time Scaling]]"
  - "[[WebArena]]"
tier: hot
tags: [evolution-strategies, llm-agents, fine-tuning, long-horizon-reasoning, test-time-compute]
---

# Agentic ESOpt: Fine-Tuning Long-Horizon LLM Agents

## Summary

This paper proposes Agentic ESOpt, a full-parameter evolution-strategy framework for fine-tuning long-horizon LLM agents with inference-level GPU memory. It replaces backpropagation through multi-turn trajectories with forward-only parameter perturbations, scalar trajectory rewards, and reward-weighted updates, targeting the memory and credit-assignment limits of agentic reinforcement learning. The paper evaluates the method on long-horizon Sudoku, ReAct-style Math and DocVQA, WebArena-Lite, and automatic heuristic design, reporting a horizon-dependent advantage over RL and improvements in 28 of 36 matched test-time heuristic-search comparisons.

## Key Points

- Agentic ESOpt samples full-parameter Gaussian perturbations, evaluates each perturbed agent with a scalar environment reward, normalizes rewards within the population, and applies an online reward-weighted update.
- The forward-only update stores perturbation seeds and uses in-place parameter changes, so the method requires inference-level GPU memory rather than activation, optimizer-state, and backpropagation memory.
- Its trajectory-level parameter attribution avoids the explicit sum of action-score terms that the paper’s simplified comparison associates with increasing long-horizon policy-gradient variance.
- A cosine schedule decreases the perturbation radius: train-time optimization retains a nonzero terminal radius for exploration and smoothing, while test-time optimization decays the terminal radius to zero for finer adaptation.
- In controlled Sudoku, Agentic ESOpt is not uniformly strongest: PPO leads at minimum successful horizon 5, GRPO leads at horizon 10, and Agentic ESOpt leads at horizon 15 with 53.13% versus 40.63% for the strongest GRPO configuration.
- The method improves Qwen3.5-4B results over matched Agentic GRPO baselines on ReAct-style Math and DocVQA, raises Qwen3.5-27B WebArena-Lite No Skill success from 29.47% to 36.16%, and improves the Trace2Skill baseline from 33.94% to 36.36%.
- In automatic heuristic design, it attaches parameter-space updates to existing Sample and EoH search procedures and improves 28 of 36 matched method-budget comparisons under the reported fixed evaluation budgets.

## Concepts Extracted

- **[[Agentic ESOpt for Long-Horizon LLM Fine-Tuning]]** — Forward-only full-parameter evolution-strategy optimization for sparse-reward, multi-turn agents.
- **[[Prompt–Parameter Co-Evolution for Agentic Test-Time Compute]]** — Alternating optimization of model parameters and external prompts, skills, or heuristic contexts during test-time search.
- **Long-horizon credit assignment** — The paper’s mechanism-level comparison between action-space policy gradients and trajectory-level parameter perturbations.

## Entities Mentioned

- **Agentic ESOpt** — Proposed framework introduced by the paper.
- **Qwen3.5-4B and Qwen3.5-27B** — LLM backbones used in the train-time and WebArena-Lite experiments.
- **[[WebArena]]-Lite** — Browser-agent benchmark used to evaluate adaptation of Qwen3.5-27B.
- **Trace2Skill** — Skill-distillation procedure composed with Agentic ESOpt in selected experiments.
- **EoH and Sample** — Existing automatic-heuristic-design search scaffolds augmented with parameter updates.
- **Zhi Zheng, Rongsheng Chen, Yunpeng Ba, Zhenkun Wang, Yee Whye Teh, and Wee Sun Lee** — Listed authors.

## Notable Quotes

> "ES performs trajectory-level parameter attribution without decomposing rewards across horizons."

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-08-21-260817310v1pdf.md` |
| Type | Paper |
| Author | Zhi Zheng; Rongsheng Chen; Yunpeng Ba; Zhenkun Wang; Yee Whye Teh; Wee Sun Lee |
| Date | Not stated in the fetched content |
| URL | https://arxiv.org/pdf/2608.17310 |
