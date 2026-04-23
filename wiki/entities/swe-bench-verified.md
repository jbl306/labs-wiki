---
title: SWE-Bench-Verified
type: entity
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "23657eb3935efc0dbc400af97abfe6e9aa4c98d3cc6aac876d7a0ed1195b3b92"
sources:
  - raw/2026-04-22-250925140v2pdf.md
quality_score: 68
concepts:
  - agent-evaluation-benchmarks
related:
  - "[[ReasoningBank]]"
  - "[[WebArena]]"
tier: warm
tags: [benchmark, evaluation, agent-testing, software-engineering]
---

# SWE-Bench-Verified

## Overview

SWE-Bench-Verified is a benchmark for evaluating agent performance on software engineering tasks, specifically code manipulation and repository understanding. Used as a primary evaluation environment in the ReasoningBank research.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Benchmark/Evaluation Environment |
| Created | 2025-09 |
| Creator | Google Research |
| URL | https://arxiv.org/abs/2509.25140 |
| Status | Active |
## ReasoningBank Evaluation

SWE-Bench-Verified was used to evaluate ReasoningBank's effectiveness on software engineering tasks:
- **Success Rate Improvement**: 4.6% over memory-free baseline
- **Efficiency Gain**: ~3 fewer task execution steps per task compared to baseline
- **MaTTS Addition**: Further 3% success rate boost when combined with memory-aware test-time scaling

## Related Entities

- **[[ReasoningBank]]** — Framework evaluated on SWE-Bench-Verified
- **[[WebArena]]** — Complementary web browsing benchmark
