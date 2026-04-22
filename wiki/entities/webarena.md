---
title: WebArena
type: entity
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "23657eb3935efc0dbc400af97abfe6e9aa4c98d3cc6aac876d7a0ed1195b3b92"
sources:
  - raw/2026-04-22-250925140v2pdf.md
quality_score: 60
concepts:
  - agent-evaluation-benchmarks
related:
  - "[[ReasoningBank]]"
  - "[[SWE-Bench-Verified]]"
tier: warm
tags: [benchmark, evaluation, agent-testing, web-navigation]
---

# WebArena

## Overview

WebArena is a benchmark for evaluating agent performance on web browsing and navigation tasks. Used as a primary evaluation environment in the ReasoningBank research.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Benchmark/Evaluation Environment |
| Created | 2025-09 |
| Creator | Google Research |
| URL | https://arxiv.org/abs/2509.25140 |
| Status | Active |
## ReasoningBank Evaluation

WebArena was used to evaluate ReasoningBank's improvements over baseline approaches:
- **Baseline (Vanilla ReAct)**: Memory-free agent
- **Synapse**: Trajectory memory approach
- **Agent Workflow Memory**: Workflow memory (successful only)
- **ReasoningBank**: Novel approach with failure learning
- **ReasoningBank + MaTTS**: With memory-aware test-time scaling

**Results**: 8.3% success rate improvement on WebArena (ReasoningBank vs. memory-free)

## Related Entities

- **[[ReasoningBank]]** — Framework evaluated on WebArena
- **[[SWE-Bench-Verified]]** — Complementary software engineering benchmark
