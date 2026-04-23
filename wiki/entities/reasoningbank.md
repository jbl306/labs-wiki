---
title: ReasoningBank
type: entity
created: 2026-04-21
last_verified: 2026-04-22
source_hash: "15e0d38d97945d4e58427c03622de24ec2191b5d77cc532159579b7444219a6d"
sources:
  - raw/2026-04-22-reasoningbank-enabling-agents-to-learn-from-experience.md
  - raw/2026-04-22-250925140v2pdf.md
quality_score: 81
concepts:
  - agent-memory-frameworks
  - test-time-scaling
related:
  - "[[Agent Memory]]"
  - "[[Google Research]]"
  - "[[LLM Agents]]"
tier: hot
tags: [agent-memory, reasoning, framework, google-research, iclr-2026]
---

# ReasoningBank

## Overview

ReasoningBank is a novel agent memory framework developed by Google Research that enables large language model (LLM) agents to learn from both successful and failed experiences during test time. It distills generalizable reasoning strategies into structured memory items and introduces Memory-Aware Test-Time Scaling (MaTTS) to accelerate learning through scaled exploration.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Research Framework & Tool |
| Created | 2026-04-21 |
| Creator | Google Research (Siru Ouyang, Jun Yan, Chen-Yu Lee, et al.) |
| URL | https://github.com/google-research/reasoning-bank |
| Status | Active |

## Core Concept

ReasoningBank addresses a critical limitation in persistent, long-running LLM agents: their inability to learn from accumulated interaction history. Rather than storing exhaustive action traces (like Synapse) or only successful workflows (like Agent Workflow Memory), ReasoningBank:

1. **Distills High-Level Patterns**: Converts experiences into structured memories with title, description, and reasoning content
2. **Learns from Failures**: Actively analyzes failed experiences to extract counterfactual signals and preventative lessons
3. **Operates in Closed Loop**: Retrieval → Interaction → Self-Judgment → Extraction → Consolidation

The self-judgment mechanism uses an LLM-as-a-judge pattern to evaluate trajectory outcomes and is robust to judgment noise.

## Memory-Aware Test-Time Scaling (MaTTS)

MaTTS establishes a synergy between memory and test-time scaling:
- **Parallel Scaling**: Generate multiple distinct trajectories; ReasoningBank compares successful and spurious trajectories to distill robust strategies
- **Sequential Scaling**: Iteratively refine reasoning within a single trajectory; capture intermediate insights as high-quality memory
- **Result**: Scaled exploration generates rich contrastive signals; better memory steers more effective exploration

## Performance & Evaluation

**Benchmarks**: WebArena, SWE-Bench-Verified

**Results**:
- 8.3% success rate improvement on WebArena vs. memory-free baseline
- 4.6% improvement on SWE-Bench-Verified
- ~3 fewer execution steps per task (SWE-Bench-Verified)
- MaTTS (parallel scaling, k=5) adds 3% further success rate boost

**Emergent Behavior**: Agent memories evolve from simple procedural checklists into advanced compositional structures with preventative logic

## Research Foundation

- **Venue**: ICLR 2026
- **Lead Authors**: Siru Ouyang, Jun Yan, Chen-Yu Lee, Tomas Pfister
- **Paper**: "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory"
- **Code**: https://github.com/google-research/reasoning-bank
- **Blog**: https://research.google/blog/reasoningbank-enabling-agents-to-learn-from-experience/

## Related Work

- **[[Synapse]]** — Prior trajectory memory approach
- **[[Agent Workflow Memory]]** — Prior workflow memory approach (successful runs only)

## Impact

ReasoningBank establishes memory-driven experience scaling as a new scaling dimension for agents, demonstrating that persistent learning during test-time enables agents to achieve emergent strategic maturity.
