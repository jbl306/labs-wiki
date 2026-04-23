---
title: "ReasoningBank: Enabling agents to learn from experience"
type: source
created: '2026-04-21'
last_verified: '2026-04-22'
source_hash: 15e0d38d97945d4e58427c03622de24ec2191b5d77cc532159579b7444219a6d
sources:
  - raw/2026-04-22-reasoningbank-enabling-agents-to-learn-from-experience.md
source_url: https://research.google/blog/reasoningbank-enabling-agents-to-learn-from-experience/
tags:
  - google-research
  - agent-memory
  - reasoning
  - llm-agents
tier: warm
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 65
---

# ReasoningBank: Enabling agents to learn from experience

## Summary

Google Research's blog post introducing [[ReasoningBank]], a novel agent memory framework that enables LLM-based agents to learn from both successful and failed experiences. The framework distills generalizable reasoning strategies through a continuous loop of memory retrieval, experience interaction, self-assessment, and memory consolidation. It also introduces [[Memory-Aware Test-Time Scaling]] (MaTTS) to accelerate learning through scaled exploration.

## Key Points

- **Agent Learning Problem**: Long-running agents fail to learn from accumulated interaction history, repeatedly making the same strategic errors despite having valuable experience.
- **ReasoningBank Core Idea**: A memory framework that distills reasoning strategies from both successful and failed experiences, enabling test-time self-evolution.
- **Key Difference from Prior Art**: Unlike existing approaches such as [[Synapse]] trajectory memory and [[Agent Workflow Memory]], ReasoningBank:
  - Distills high-level reasoning patterns instead of storing detailed action traces
  - Actively learns from failures, not just successes
  - Uses structured memory items (title, description, content)
- **Memory Workflow**: Retrieval → Action → Self-Judgment → Extraction → Consolidation (closed loop)
- **Self-Judgment Mechanism**: LLM-as-a-judge evaluates trajectory outcomes; robust to judgment noise
- **Learning from Failures**: Generates counterfactual signals and preventative lessons (e.g., "verify page identifier first to avoid infinite scroll traps")
- **Memory-Aware Test-Time Scaling (MaTTS)**: Links memory with test-time scaling—scaled exploration generates rich contrastive signals that feed back into ReasoningBank
- **MaTTS Forms**: Parallel scaling (multiple trajectories) and sequential scaling (iterative refinement within single trajectory)
- **Benchmarks Tested**: [[WebArena]], [[SWE-Bench-Verified]]
- **Performance Gains**: 8.3% success rate improvement on [[WebArena]], 4.6% on [[SWE-Bench-Verified]]; 3 fewer steps per task; MaTTS adds 3% further improvement
- **Emergent Behavior**: Agent memories evolve from simple procedural checklists to advanced compositional structures with preventative logic
- **Model Used**: Gemini 2.5 Flash

## Key Concepts

- [[Agent Memory Frameworks]]
- [[Memory-Aware Test-Time Scaling]]
- Experience-Driven Learning
- LLM-as-a-Judge
- Self-Evolution
- Reasoning Distillation
- Trajectory Analysis

## Related Entities

- **[[ReasoningBank]]** — The framework itself (tool/research)
- **[[Google Research]]** — Publisher
- **[[Synapse]]** — Prior art in agent memory (trajectory memory)
- **[[Agent Workflow Memory]]** — Prior art (successful workflows only)
- **[[WebArena]]** — Benchmark
- **[[SWE-Bench-Verified]]** — Benchmark
