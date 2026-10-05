---
title: "Agent-G²"
type: entity
created: 2026-08-28
last_verified: 2026-08-28
source_hash: "2f7c92afa7dc8de052baf3a33e81fb82a645865dd92eb7e7a058436ad50d3fb5"
sources:
  - raw/2026-08-28-260823318v1pdf.md
quality_score: 86
concepts:
  - gaussian-guidance
  - hint-based-reinforcement-learning
  - long-horizon-agentic-reinforcement-learning
related:
  - "[[Gaussian Guidance for Agentic Reinforcement Learning]]"
  - "[[Agentic ESOpt for Long-Horizon LLM Fine-Tuning]]"
tier: hot
tags:
  - agentic-reinforcement-learning
  - hint-based-rl
  - gaussian-guidance
  - research-method
---

# Agent-G²

## Overview

Agent-G² is a Gaussian guidance framework for hint-based reinforcement learning on long-horizon agentic tasks. It samples expert-prefix depth per task and adapts the sampling distribution online from rollout statistics, combining a global guidance baseline with difficulty-cluster corrections.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Research method / agentic reinforcement-learning framework |
| Created | Unknown; not stated in the fetched content |
| Creator | Zixuan Wang; Yanrui Miao; Zhengxi Lu; Teng Pan; Yiwen Qiu; Hongxing Li; Peng Qiu; Ruiqing Zhang; Yongliang Shen |
| URL | https://arxiv.org/pdf/2608.23318 |
| Status | Research method; code and training scripts stated to be released under the MIT License upon publication |

## Relevance

Agent-G² addresses a specific failure mode in hint-based RL: a single guidance depth cannot match heterogeneous tasks, while per-sample depth probing spends additional rollouts. Its Gaussian schedule uses already-collected policy-optimization rollouts to vary depth by task without a learned depth predictor or separate probe budget. The paper evaluates it on ALFWorld and WebShop with Qwen2.5-1.5B-Instruct and Qwen2.5-7B-Instruct.

## Associated Concepts

- **[[Gaussian Guidance for Agentic Reinforcement Learning]]** — Describes the adaptive Gaussian depth schedule, rollout reuse, and joint GRPO-plus-prefix objective.
- **[[Agentic ESOpt for Long-Horizon LLM Fine-Tuning]]** — A related long-horizon agent optimization method with a different optimization interface.

## Related Entities

- No additional entity page is proposed because the paper's benchmark and backbone names are mentioned as experimental settings rather than as entities needed for this compilation.

## Sources

- [[Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning]] — Primary source for the method and its reported experiments.
