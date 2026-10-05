---
title: "Contextual-Bandit-Guided Agent Skill Optimization"
type: concept
created: 2026-09-15
last_verified: 2026-09-15
source_hash: "dd436547ea18eace6464dcb20b924f525790f07a573a0b502cac2f52c5f89682"
sources:
  - raw/2026-09-15-260911682v1pdf.md
quality_score: 93
concepts:
  - contextual-bandits
  - agent-skill-optimization
  - evidence-grounded-evolution
  - evaluation-budget-allocation
related:
  - "[[COBRA-Skills]]"
  - "[[WikiSkill Framework]]"
  - "[[Cross-Model Transfer of Evolved Agent Skills]]"
  - "[[Skill Design Framework for AI Agents]]"
tier: hot
tags:
  - agent-skills
  - contextual-bandits
  - skill-optimization
  - evolutionary-search
  - llm-agents
---

# Contextual-Bandit-Guided Agent Skill Optimization

## Overview

Contextual-bandit-guided agent skill optimization allocates a limited number of target-agent evaluations across reusable procedural skills whose utilities are initially uncertain. In COBRA-Skills, each candidate is represented by a semantic embedding, scored using predicted reward plus an uncertainty bonus, and periodically replaced or refined using execution evidence.

The approach addresses two costs in skill optimization: executing every candidate to discover its value and repeatedly invoking a teaching model to rewrite skills. It makes candidate selection adaptive while retaining evidence-grounded refinement.

## How It Works

1. **Initialize a population.** The system collects no-skill trajectories from a small optimization set and uses them to generate an initial fixed-size population of candidate skills.
2. **Represent candidates.** Each skill is embedded with a fixed embedding model. COBRA-Skills uses L2-normalized Qwen3-Embedding-4B vectors.
3. **Predict reward and uncertainty.** A lightweight two-layer neural network predicts reward from the embedding. A LinearUCB-style bonus is larger in less-explored regions of the embedding space:

   ```text
   U_t(s) = f_theta(z_s) + nu * sqrt(z_s^T A_(t-1)^(-1) z_s)
   ```

   The predicted reward supports exploitation, while the bonus supports exploration.
4. **Evaluate selectively.** The candidate with the highest priority score is executed by the target agent on the optimization set. Its observed reward and trajectories are added to the history, and the predictor is refit on all observations.
5. **Evolve periodically.** At scheduled updates, the lowest-priority candidates are pruned. Vacant slots are filled by regeneration from no-skill trajectories, rollout mutation of the selected skill using successful and failed trajectories, and crossover using high- and low-performing skills as positive and negative evidence.
6. **Re-enter the evaluation loop.** Newly generated candidates inherit no reward. They must be evaluated by the same bandit procedure before they can influence retention or final selection.
7. **Select the result.** After the fixed optimization horizon, the system returns the evaluated skill with the highest mean observed reward.

In the reported configuration, COBRA-Skills used 30 rounds, a population of 10, three replacements at each evolutionary update, and one evaluation over all 50 optimization examples per round. Crossover was enabled after more than eight distinct skills had been evaluated.

## Key Properties

- **Budgeted evaluation:** Expensive target-agent execution is concentrated on candidates that are promising or insufficiently explored.
- **Semantic generalization:** Rewards observed for one skill can inform prioritization of semantically related candidates through their embeddings.
- **Dynamic candidate space:** Evolution changes the available arms, allowing the search to move beyond the initial population.
- **Evidence-grounded refinement:** Mutations and crossovers use actual successful and failed trajectories rather than relying only on plausible model-generated guidance.
- **Complementary exploration and exploitation:** The same priority score guides both evaluation allocation and population retention.
- **Scheduled teaching-model use:** Evolution occurs periodically, reducing repeated trajectory analysis and skill synthesis calls.

## Trade-offs and Limitations

The method still requires target-agent executions, and each selected candidate is evaluated across the full optimization set. Its efficiency therefore depends on the relative price of target-model execution, teaching-model calls, and environment interaction. The 50-example optimization set is intended to balance aggregate ranking reliability with task coverage, but it is a benchmark-specific design choice.

The neural reward predictor and uncertainty bonus can mis-rank candidates when semantic similarity is a poor proxy for utility or when the history is sparse. Exploration strength is sensitive to the LinearUCB coefficient: performance in the reported study peaked at `nu = 0.1` and declined moderately at larger values. The method provides empirical prioritization rather than a guarantee of global optimum discovery.

The reported results are limited to six benchmarks, three target models, and the evaluated harnesses. Comparisons with Trace2Skill and SkillOpt used larger optimization pools, so the results demonstrate a favorable reported efficiency trade-off rather than an isolation of every possible data-budget effect.

## Concrete Example

Under the native harness, COBRA-Skills improved Qwen3.6-35B-A3B’s six-benchmark average from the no-skill baseline of 60.4% to 73.5%, a gain of 13.1 percentage points. Its reported optimization cost was $54.10, compared with $121.02 for SkillOpt. On the same setup, removing bandit prioritization reduced average performance by 2.2 points, removing evolution reduced it by 2.4 points, and a fixed best-of-30 candidate pool underperformed the full method by 2.5 points.

## Relationship to Other Concepts

- **[[COBRA-Skills]]** — The named framework that implements this optimization loop.
- **[[WikiSkill Framework]]** — A related experience-driven skill-evolution framework; COBRA-Skills focuses specifically on adaptive evaluation allocation over a changing candidate population.
- **[[Cross-Model Transfer of Evolved Agent Skills]]** — COBRA-Skills reports transfer experiments showing that optimized skills can improve other target models.
- **[[Skill Design Framework for AI Agents]]** — Provides general guidance for authoring skills, whereas this concept focuses on automatically evaluating and evolving them.

## Practical Applications

This pattern is useful when agent skills can be evaluated through costly rollouts and the optimization budget is too small for exhaustive candidate testing. Suitable settings include tool-use agents, multi-turn task agents, reusable workflow libraries, and systems that need to refine procedures from both successful and failed executions.

## Sources

- [[COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization]] — Defines the contextual-bandit selection rule, evidence-grounded evolutionary operators, and benchmark results.