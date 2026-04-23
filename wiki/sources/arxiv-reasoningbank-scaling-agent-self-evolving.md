---
title: "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory"
type: source
created: '2025-09-29'
last_verified: '2026-04-22'
source_hash: 23657eb3935efc0dbc400af97abfe6e9aa4c98d3cc6aac876d7a0ed1195b3b92
sources:
  - raw/2026-04-22-250925140v2pdf.md
source_url: https://arxiv.org/abs/2509.25140
tags:
  - arxiv
  - agent-memory
  - reasoning
  - test-time-scaling
  - iclr-2026
tier: warm
knowledge_state: ingested
ingest_method: self-synthesis-no-llm
quality_score: 61
---

# ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory

## Summary

ICLR 2026 paper introducing ReasoningBank, a memory framework enabling LLM agents to learn from successful and failed experiences through continuous self-evolution. The paper presents Memory-Aware Test-Time Scaling (MaTTS), demonstrating how scaled exploration generates rich contrastive signals for high-quality memory synthesis. Evaluation on WebArena and SWE-Bench-Verified shows significant improvements in both effectiveness and efficiency.

## Key Points

- **Core Problem**: Persistent LLM agents in real-world roles encounter continuous task streams but fail to learn from accumulated interaction history.
- **Solution**: ReasoningBank distills generalizable reasoning strategies from self-judged successful and failed experiences.
- **Memory Structure**: Structured items containing title, description, and distilled reasoning steps/decision rationales.
- **Workflow**: Closed-loop process—retrieval, interaction, self-assessment (LLM-as-judge), extraction, consolidation.
- **Failure Learning**: Actively analyzes failed experiences to source counterfactual signals and preventative lessons—key differentiator from prior work.
- **Memory-Aware Test-Time Scaling (MaTTS)**: Bridges memory with test-time scaling; scaled exploration provides contrastive signals.
- **MaTTS Mechanisms**: Parallel scaling (multiple trajectories under memory guidance), Sequential scaling (iterative refinement with intermediate rationale capture).
- **Synergy**: High-quality memory steers exploration; scaled interactions generate richer learning signals that improve memory.
- **Evaluation**: Tested on dynamic environments (WebArena, SWE-Bench-Verified) with strong baselines including Synapse and Agent Workflow Memory.
- **Results**: Superior success rates, reduced steps, emergent strategic maturity in memory evolution.
- **Code**: Available at https://github.com/google-research/reasoning-bank

## Key Concepts

- Agent Self-Evolution
- Memory-Driven Experience Scaling
- Test-Time Scaling (TTS)
- Contrastive Memory Synthesis
- Self-Judgment Mechanism
- Trajectory Analysis
- Agentic Learning

## Related Entities

- **[[ReasoningBank]]** — Research framework (paper + code)
- **[[Google Research]]** — Institution
- **[[WebArena]]** — Evaluation benchmark
- **[[SWE-Bench-Verified]]** — Evaluation benchmark
