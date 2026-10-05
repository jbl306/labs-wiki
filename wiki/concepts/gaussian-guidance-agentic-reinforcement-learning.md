---
title: "Gaussian Guidance for Agentic Reinforcement Learning"
type: concept
created: 2026-08-28
last_verified: 2026-08-28
source_hash: "2f7c92afa7dc8de052baf3a33e81fb82a645865dd92eb7e7a058436ad50d3fb5"
sources:
  - raw/2026-08-28-260823318v1pdf.md
quality_score: 91
concepts:
  - gaussian-guidance
  - hint-based-reinforcement-learning
  - guidance-depth-scheduling
  - long-horizon-agentic-reinforcement-learning
related:
  - "[[Agent-G²]]"
  - "[[Agentic ESOpt for Long-Horizon LLM Fine-Tuning]]"
  - "[[Evolution Strategies vs Agentic RL for Long-Horizon Agents]]"
tier: hot
tags:
  - agentic-reinforcement-learning
  - hint-based-rl
  - gaussian-guidance
  - curriculum-learning
---

# Gaussian Guidance for Agentic Reinforcement Learning

## Overview

Gaussian guidance treats the amount of an expert trajectory retained before an agent rollout as a distributional scheduling problem. Agent-G² argues that useful prefix depths form a neighborhood around a task-specific effective depth, so sampling nearby depths can provide more reliable learning signal than selecting one shared or supposedly optimal scalar.

## How It Works

A task has an expert trajectory of length L and a guidance ratio r in [0, 1]. The scheduler converts the ratio into a prefix length:

n = min(ceil(rL), L - 1)

The first n expert actions are executed in the environment, and the policy then performs R independent rollouts from the resulting state. Their binary terminal rewards produce an empirical success rate p-hat for the task.

Agent-G² first partitions tasks offline by expert-trajectory length into difficulty clusters. For each batch it maintains:

- A global guidance baseline, shifted upward when batch success is below the midpoint target 0.5 and downward when success is above it.
- A per-cluster exponential moving average A_k of empirical success rates.
- A per-cluster exponential moving average V_k of the variance of task success rates within that cluster.

For a task in cluster k, the Gaussian parameters are:

- mu_i = clip(mu_global + lambda(0.5 - A_k), 0, 1)
- sigma_i = max(gamma V_k, sigma_min)

The center therefore moves toward deeper guidance for clusters with lower success, while the spread expands when tasks in a cluster respond unevenly. The scheduler draws z_i from N(mu_i, sigma_i²), clips it to [0, 1], and uses that sampled ratio for the task's shared rollout prefix.

The policy is trained with a joint objective:

L = L_GRPO + eta L_aux

where GRPO learns from terminal-reward differences among the post-prefix rollouts, and L_aux is a teacher-forced loss on the sampled expert-prefix actions. Terminal rewards from those same rollouts refresh the global and cluster statistics for the next batch.

## Key Properties

- **Band coverage rather than point estimation:** The method targets a range of informative depths. Its diagnostic profile is approximately Gaussian around the depth where empirical success is near 0.5.
- **Global-local adaptation:** A global progress baseline tracks overall policy development, while clusters correct for task-difficulty differences and within-cluster variance.
- **Task-level stochasticity:** Independent Gaussian draws create depth variation across tasks without running extra probes for each candidate depth.
- **Rollout reuse:** Policy optimization and schedule adaptation consume the same rollouts, avoiding a separate depth-search budget.
- **Joint learning signal:** GRPO supplies the main post-prefix reinforcement signal, while prefix imitation stabilizes learning.

## Trade-offs and Limitations

Gaussian guidance adds schedule state, clustering, and per-task sampling overhead compared with a fixed schedule. It is modestly slower per training step than simple scheduled baselines in the reported ALFWorld measurement, although it is substantially cheaper than probing-based methods. The method also depends on one expert trajectory per training task, and its Gaussian parameterization was empirically motivated on ALFWorld and WebShop rather than established for arbitrary depth profiles. Fixed clusters based on trajectory length may become stale as policy-relative difficulty changes; multimodal or skewed profiles may require a richer distribution family.

The ablations show that the stochastic coverage and adaptive moments matter: deterministic mean sampling, variance-matched uniform sampling, removing cluster-aware centering, removing adaptive spread, and collapsing clusters all reduce performance. Removing GRPO is especially damaging because sampled-prefix imitation alone does not learn effectively from post-prefix states.

## Concrete Example

On Qwen2.5-1.5B-Instruct with ALFWorld, the full method reaches 95.3% overall success. Deterministic mean sampling falls to 89.8%, variance-matched uniform sampling to 88.3%, and removing cluster-aware centering to 91.4%. Removing adaptive spread gives 93.8% overall but drops Long-task success from 94.7% to 78.3%; removing GRPO reduces overall success to 26.6%. These results support the mechanism's central claim: both stochastic depth coverage and reinforcement learning on sampled post-prefix states are necessary.

## Relationship to Other Concepts

- **[[Agent-G²]]** — The named framework that implements this scheduling mechanism.
- **[[Agentic ESOpt for Long-Horizon LLM Fine-Tuning]]** — Another long-horizon agent optimization method that addresses sparse rewards through trajectory-level parameter perturbations rather than expert-prefix depth scheduling.
- **[[Evolution Strategies vs Agentic RL for Long-Horizon Agents]]** — Existing synthesis on the regime-dependent trade-offs of long-horizon agent optimization; Agent-G² provides additional evidence about adaptive rollout guidance.

## Practical Applications

This mechanism is suited to agent training where expert demonstrations exist, rewards are sparse or terminal, and task difficulty varies within a batch. It is especially useful when per-sample depth probing is too expensive and a shared schedule is too coarse, such as multi-step household interaction or web-navigation tasks.

## Sources

- [[Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning]] — Primary paper summary and reported ablations.
