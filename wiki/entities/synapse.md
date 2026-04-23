---
title: Synapse
type: entity
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "15e0d38d97945d4e58427c03622de24ec2191b5d77cc532159579b7444219a6d"
sources:
  - raw/2026-04-22-reasoningbank-enabling-agents-to-learn-from-experience.md
quality_score: 64
concepts:
  - agent-memory-frameworks
related:
  - "[[ReasoningBank]]"
  - "[[Agent Memory]]"
tier: warm
tags: [agent-memory, trajectory-memory, prior-art]
---

# Synapse

## Overview

Synapse is a prior agent memory approach that stores exhaustive trajectory records of all actions taken by an agent. Referenced in ReasoningBank research as an example of trajectory memory.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Agent Memory Framework |
| Created | 2025-09 |
| Creator | Google Research |
| URL | https://arxiv.org/abs/2509.25140 |
| Status | Active (referenced in current research) |
## Context in ReasoningBank

Synapse is mentioned as a primary prior art in agent memory, distinguished from ReasoningBank by:
- **Storage Approach**: Stores detailed action traces vs. distilled reasoning patterns
- **Failure Learning**: No explicit learning from failures

ReasoningBank improves upon this approach by distilling high-level reasoning strategies and actively learning from failed experiences.

## Related Entities

- **[[ReasoningBank]]** — Framework that improves upon Synapse's approach
- **[[Agent Workflow Memory]]** — Another prior approach
