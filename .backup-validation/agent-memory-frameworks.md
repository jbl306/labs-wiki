---
title: "Agent Memory Frameworks"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "15e0d38d97945d4e58427c03622de24ec2191b5d77cc532159579b7444219a6d"
sources:
  - raw/2026-04-22-reasoningbank-enabling-agents-to-learn-from-experience.md
  - raw/2026-04-22-250925140v2pdf.md
quality_score: 75
concepts:
  - agent-memory-frameworks
related:
  - "[[ReasoningBank]]"
  - "[[Agent Memory]]"
  - "[[Test-Time Scaling]]"
tier: warm
tags: [agent-memory, learning, frameworks, llm-agents]
---

# Agent Memory Frameworks

## Overview

Agent memory frameworks are mechanisms that enable persistent LLM agents to store, retrieve, and leverage past experiences to improve performance over time. The evolution of these frameworks reflects a fundamental challenge: how to distill experiences into forms that are both generalizable and actionable.

## Key Concept

As LLM agents move from batch-mode inference to persistent, long-running roles in real-world systems, they encounter continuous task streams. Without effective memory mechanisms, agents:
- Repeatedly make the same strategic errors
- Discard valuable insights from past interactions
- Fail to develop emergent strategies over time

## Historical Approaches

### Trajectory Memory (Synapse)
- **Approach**: Store exhaustive records of all actions taken
- **Limitation**: Records detailed actions rather than distilling higher-level patterns
- **Result**: Verbose, low-level memories that don't transfer well

### Workflow Memory (Agent Workflow Memory)
- **Approach**: Summarize workflows from successful task attempts only
- **Limitation**: Overlooks learning from failures, the primary source of lesson distillation
- **Result**: Incomplete learning signal, inability to develop preventative strategies

### Reasoning-Based Memory (ReasoningBank)
- **Approach**: Distill generalizable reasoning strategies from both successful and failed experiences
- **Structure**: Structured memory items with title, description, reasoning steps
- **Innovation**: Active failure analysis for counterfactual learning
- **Result**: High-level, transferable strategies; emergent strategic maturity

## Core Functions

1. **Retrieval**: Access relevant past experience given current context
2. **Experience Generation**: Interact with environment and record outcomes
3. **Self-Assessment**: Evaluate success or failure (e.g., LLM-as-a-Judge)
4. **Extraction**: Distill generalizable insights from trajectories
5. **Consolidation**: Integrate new learnings into memory structure

## Memory-Aware Test-Time Scaling

Recent work (ReasoningBank's MaTTS) demonstrates that memory and test-time scaling form a powerful synergy:
- High-quality memory steers exploration toward promising strategies
- Scaled exploration generates richer contrastive signals
- Better signals feed back into improved memory

## Emerging Properties

As agent memory systems mature, they enable:
- **Emergent Strategic Maturity**: Simple procedural rules evolve into compositional structures with preventative logic
- **Continuous Self-Evolution**: Agents improve over time without retraining
- **Failure-Driven Learning**: Mistakes become structured preventative lessons

## Implications

Agent memory frameworks represent a shift from batch learning (pre-training) to continuous, test-time learning. This unlocks a new scaling dimension for AI agents: memory-driven experience scaling.

## Related Concepts

- Agent Memory — Broader concept
- LLM-as-a-Judge — Self-assessment mechanism (pattern, not specific entity)
