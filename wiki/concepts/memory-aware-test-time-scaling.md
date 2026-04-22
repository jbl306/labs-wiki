---
title: "Memory-Aware Test-Time Scaling"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "23657eb3935efc0dbc400af97abfe6e9aa4c98d3cc6aac876d7a0ed1195b3b92"
sources:
  - raw/2026-04-22-250925140v2pdf.md
quality_score: 75
concepts:
  - test-time-scaling
  - agent-memory-frameworks
related:
  - "[[ReasoningBank]]"
  - "[[Test-Time Scaling]]"
  - "[[Agent Memory Frameworks]]"
tier: warm
tags: [test-time-scaling, agent-memory, scaling, inference]
---

# Memory-Aware Test-Time Scaling

## Overview

Memory-Aware Test-Time Scaling (MaTTS) is a framework that bridges agent memory and test-time compute scaling, establishing a powerful synergy where scaled exploration generates rich contrastive signals for memory synthesis, and high-quality memory in turn guides more effective exploration.

## Core Insight

Traditional test-time scaling in reasoning tasks (math, competitive programming) discards the exploration trajectory, treating only the final answer as useful output. In agentic environments, the exploration trajectory contains rich information:
- Diverse attempted strategies
- Contrasts between successful and failed approaches
- Intermediate reasoning steps
- Lessons from false starts

MaTTS explicitly captures this trajectory information to accelerate memory-based learning.

## Two Scaling Modes

### Parallel Scaling
**Approach**: Generate multiple distinct trajectories for the same task, all guided by current memory

**Mechanism**:
1. Agent generates N different solution paths (k parallel attempts)
2. ReasoningBank compares successful vs. spuriously reasoned trajectories
3. Contrastive analysis distills more robust strategies
4. High-quality memories are synthesized

**Effect**: Breadth of exploration; contrastive learning signals

### Sequential Scaling
**Approach**: Iteratively refine reasoning within a single trajectory

**Mechanism**:
1. Agent attempts a task and refines its approach
2. Intermediate reasoning and improvements are captured
3. Trial-and-error patterns become high-quality memory items
4. Progressive improvement insights are retained

**Effect**: Depth of exploration; progressive learning signals

## The Synergy

```
Better Memory → More Effective Exploration → Richer Signals
                  ↑                              ↓
              ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
```

1. High-quality memory steers scaled exploration toward promising strategies
2. Scaled interactions generate abundant, diverse experiences
3. Contrastive signals synthesize even higher-quality memory
4. Cycle repeats, enabling emergent behaviors

## Empirical Results (ReasoningBank)

**WebArena**:
- ReasoningBank alone: 8.3% success improvement
- ReasoningBank + MaTTS (k=5 parallel): additional 3% improvement
- Efficiency: MaTTS reduces aimless exploration

**SWE-Bench-Verified**:
- ReasoningBank alone: 4.6% improvement, 3 fewer steps
- ReasoningBank + MaTTS: further gains

## Implementation Notes

- **Judgment Robustness**: System is robust to imperfect self-judgment (LLM-as-judge)
- **Memory Consolidation**: Scaling generates abundant memories; consolidation strategy left for future work (currently append-based)
- **Compute Trade-off**: k parallel attempts = k× compute; demonstrates compute-efficiency tradeoff

## Implications

MaTTS establishes memory-driven experience scaling as a new scaling dimension, complementary to:
- Model scaling (pre-training compute)
- Chain-of-thought scaling (reasoning depth)
- Test-time scaling (inference compute)

This enables agents to self-evolve with emergent behaviors arising naturally from experience.

## Related Concepts

- Agent Memory Frameworks — Memory systems that benefit from MaTTS
- ReasoningBank — Implementation framework
