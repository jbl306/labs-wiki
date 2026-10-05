---
title: "Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning"
type: source
created: 2026-08-28
last_verified: 2026-08-28
source_hash: "2f7c92afa7dc8de052baf3a33e81fb82a645865dd92eb7e7a058436ad50d3fb5"
sources:
  - raw/2026-08-28-260823318v1pdf.md
quality_score: 92
concepts:
  - gaussian-guidance
  - hint-based-reinforcement-learning
  - guidance-depth-scheduling
  - long-horizon-agentic-reinforcement-learning
related:
  - "[[Gaussian Guidance for Agentic Reinforcement Learning]]"
  - "[[Agent-G²]]"
  - "[[Agentic ESOpt for Long-Horizon LLM Fine-Tuning]]"
  - "[[Evolution Strategies vs Agentic RL for Long-Horizon Agents]]"
tier: hot
tags:
  - agentic-reinforcement-learning
  - hint-based-rl
  - gaussian-guidance
  - long-horizon-agents
  - arxiv
---

# Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning

## Summary

This paper introduces Agent-G², a hint-based reinforcement-learning framework for long-horizon agentic tasks. Instead of assigning one deterministic expert-prefix depth to every task or paying for per-sample probing, it samples a guidance ratio per task from a Gaussian whose center and spread are estimated online from existing policy-optimization rollouts. The paper reports strong results on ALFWorld and WebShop with Qwen2.5-1.5B-Instruct and Qwen2.5-7B-Instruct, without probe rollouts or a learned depth predictor.

## Key Points

- Hint-based RL retains a prefix of an expert trajectory so exploration starts closer to a successful state, but the useful guidance depth varies across tasks.
- Diagnostic experiments find that informative guidance spans a band of depths; the aligned training-signal profile is approximately Gaussian, with reported fit sigma = 0.22 and R² = 0.92.
- Agent-G² maintains a global guidance baseline plus per-cluster exponential-moving-average estimates of success level and within-cluster variance. Expert-trajectory length is used offline as a proxy for task difficulty.
- One Gaussian guidance ratio is sampled per task, converted into an expert-prefix length, and used to initialize all independent rollouts for that task.
- The same rollouts update both the GRPO policy objective and the schedule statistics, so schedule adaptation adds no probe rollouts or learned depth predictor.
- The joint objective combines GRPO with a teacher-forced loss on sampled expert prefixes; removing GRPO reduces the method to sampled-prefix SFT and sharply lowers performance.
- On ALFWorld, Agent-G² reaches 95.3% overall success with Qwen2.5-1.5B-Instruct and 98.4% with Qwen2.5-7B-Instruct. On WebShop it reports a 92.3 reward score and 78.9% / 84.4% final-purchase success at the two scales.

## Concepts Extracted

- **[[Gaussian Guidance for Agentic Reinforcement Learning]]** — Samples per-task guidance depths from rollout-adapted Gaussian distributions to cover an informative band rather than target one scalar depth.
- **Hint-based reinforcement learning** — Uses an expert trajectory prefix to reduce reward sparsity in long-horizon agentic rollouts.
- **Adaptive guidance-depth scheduling** — Combines a global progress signal with difficulty-cluster statistics to set the distribution center and spread.

## Entities Mentioned

- **[[Agent-G²]]** — Proposed Gaussian guidance framework.
- **ALFWorld** — Text-based embodied benchmark with multi-step household tasks and sparse terminal rewards.
- **WebShop** — Web-navigation benchmark whose reward is issued at final purchase.
- **Qwen2.5-1.5B-Instruct and Qwen2.5-7B-Instruct** — Base models used in the experiments.

## Notable Quotes

> "The right guidance depth is not a point to be found, but a neighborhood to be covered." — Agent-G² paper

## Source Details

| Field | Value |
|-------|-------|
| Original | raw/2026-08-28-260823318v1pdf.md |
| Type | Paper |
| Author | Zixuan Wang; Yanrui Miao; Zhengxi Lu; Teng Pan; Yiwen Qiu; Hongxing Li; Peng Qiu; Ruiqing Zhang; Yongliang Shen |
| Date | Not stated in the fetched content |
| URL | https://arxiv.org/pdf/2608.23318 |
