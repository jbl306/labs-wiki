---
title: TerminalBench
type: entity
created: 2026-04-23
last_verified: 2026-04-23
source_hash: "1ca1c01606b2b234d278cd0aefc974bff993603f4c4596baf0be8b058331d26e"
sources:
  - raw/2026-04-23-260419572v1pdf.md
concepts:
  - terminal-observation-compression
  - agentic-ai-evaluation-software-engineering
related:
  - "[[TACO]]"
  - "[[Qwen3-Coder-480B-A35B]]"
tier: hot
tags: [benchmark, terminal-agents, evaluation, software-engineering, command-line]
quality_score: 79
---

# TerminalBench

## Overview

TerminalBench is a benchmark family for evaluating agents on hard, realistic command-line tasks. In the TACO paper it serves as the main proving ground for whether terminal-output compression improves long-horizon reasoning rather than merely reducing prompt size.

The benchmark matters because terminal-centric software tasks produce exactly the kind of noisy, stateful, tool-heavy feedback that simple context-trimming strategies struggle with. That makes it a natural fit for studying whether agents can separate meaningful execution signals from irrelevant shell noise.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Benchmark |
| Created | 2026 |
| Creator | Mike A. Merrill, Alexander G. Shaw, Nicholas Carlini, Boxuan Li, Harsh Raj, Ivan Bercovich, Lin Shi, Jeong Yeon Shin, Thomas Walshe, E. Kelly Buchanan, et al. |
| URL | https://arxiv.org/abs/2601.11868 |
| Status | Active |

## Role in TACO Evaluation

The TACO paper evaluates both TerminalBench 1.0 and 2.0 and reports consistent improvements after inserting compression into the terminal-agent loop. The benchmark is important here not just as a leaderboard source, but as a stress test for observation management: logs, compiler output, package-manager chatter, and binary-analysis traces can all become prompt pollution if they are preserved verbatim across many steps.

The paper also uses pass@k experiments on TerminalBench 2.0 to show that compression improves more than single-run accuracy. With TACO enabled, pass@k rises across all reported models and `k` values in the study, suggesting that cleaner context improves both individual attempts and the diversity of viable trajectories.

## Agent Scaffolds and Models

For TerminalBench-style evaluations in the paper, the authors use the Terminus-2 scaffold as the main host agent and test across multiple backbones, including [[Qwen3-Coder-480B-A35B]], DeepSeek-V3.2, MiniMax-2.5, and smaller Qwen3 models. This makes the benchmark a useful lens on model-agnostic agent behavior rather than on one specific prompt stack.

## Why It Matters

TerminalBench is a good example of the broader problem described in [[Agentic AI Evaluation for Software Engineering]]: success rates alone are not enough when agents interact with complex environments over many steps. Because the benchmark exposes long CLI traces, it helps reveal whether an approach improves genuine reasoning quality or merely changes prompt economics.

In the TACO paper, TerminalBench becomes evidence that context compression can be treated as a first-class systems problem. Better filtering of observations does not just save tokens; it changes what information survives long enough to influence future decisions.

## Sources

- [[A Self-Evolving Framework for Efficient Terminal Agents via Observational Context Compression]] — where TerminalBench is used as the paper's primary evaluation setting
