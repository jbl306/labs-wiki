---
title: Agent Workflow Memory
type: entity
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "15e0d38d97945d4e58427c03622de24ec2191b5d77cc532159579b7444219a6d"
sources:
  - raw/2026-04-22-reasoningbank-enabling-agents-to-learn-from-experience.md
quality_score: 69
concepts:
  - agent-memory-frameworks
related:
  - "[[ReasoningBank]]"
  - "[[Agent Memory]]"
tier: warm
tags: [agent-memory, workflow-memory, prior-art]
---

# Agent Workflow Memory

## Overview

Agent Workflow Memory (AWM) is a prior agent memory approach that documents and stores workflows summarized from successful task attempts only. Referenced in ReasoningBank research as an example approach that overlooks learning opportunities from failures.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Agent Memory Framework |
| Created | 2025-09 |
| Creator | Google Research |
| URL | https://arxiv.org/abs/2509.25140 |
| Status | Active (referenced in current research) |
## Context in ReasoningBank

Agent Workflow Memory is distinguished from ReasoningBank by:
- **Scope**: Stores only successful workflows vs. both successful and failed experiences
- **Learning Signal**: Misses learning opportunity from failures—the primary source of learning from mistakes

ReasoningBank's key innovation includes actively distilling preventative lessons from failures, addressing this limitation.

## Related Entities

- **[[ReasoningBank]]** — Framework that extends AWM concept to include failure learning
- **[[Synapse]]** — Another prior approach
