---
title: Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering
type: entity
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "5173b70a6725e131573c351830b6c4874521518221c53b9cb004f836568ed255"
sources:
  - raw/2026-04-22-260401437v1pdf.md
concepts: [agentic-ai-evaluation-software-engineering, thought-action-result-tar-trajectories]
related:
  - "[[Thought-Action-Result (TAR) Trajectories]]"
  - "[[Agentic AI Evaluation for Software Engineering]]"
  - "[[Anthropic’s 'Building Effective Agents' Guide]]"
  - "[[SWE-Bench-Verified]]"
tier: hot
tags: [arxiv, position-paper, agentic-ai, software-engineering, evaluation, reproducibility, explainability]
---

# Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering

## Overview

Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering is a 2026 position paper arguing that software-engineering research on autonomous agents needs a stronger evaluation discipline. Its central claim is that current papers often report outcomes without enough artifact-level evidence to explain why an agent performed well or to let other researchers recreate the evaluation faithfully.

The paper matters because it shifts attention away from raw leaderboard deltas and toward evaluation design itself. By analyzing 18 recent papers from major SE venues, the authors identify recurring weaknesses in transparency and propose a concrete remedy: publish Thought-Action-Result (TAR) trajectories and LLM interaction artifacts so future work can inspect reasoning, tool use, environmental feedback, and failure patterns instead of only final outcomes.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Position Paper |
| Created | 2026-04-01 |
| Creator | Jingyue Li and André Storhaug |
| URL | https://arxiv.org/abs/2604.01437 |
| Status | Active |

## Problem Framing

The paper starts from two linked problems. First, the LLMs behind agentic systems are frequently treated as black boxes, so it becomes difficult to justify why one approach is better than another beyond headline metrics. Second, evaluation sections often omit practical details about setup, intermediate traces, or analysis criteria, which makes reproduction fragile or impossible.

In software engineering this matters more than it does for short-form generation tasks because agents operate over long horizons, interact with tools and repositories, and can fail for many reasons that never appear in an aggregate success rate. The paper therefore argues that evaluation should preserve process evidence, not just terminal scores.

## Proposed Guidance

The strongest recommendation is to release **[[Thought-Action-Result (TAR) Trajectories]]** together with LLM interaction data, or summarized versions when full release is impractical. In the paper's framing, these artifacts provide the missing bridge between:

- outcome metrics,
- agent behavior during execution,
- and post-hoc explanation of strengths and weaknesses.

This recommendation is part of a broader methodology for **[[Agentic AI Evaluation for Software Engineering]]** that emphasizes reproducibility, explainability, and usefulness for downstream comparative analysis.

## Evidence Base and Venue Context

The paper's recommendations are grounded in a review of 18 Agentic AI for SE papers published or accepted at ICSE 2025, ICSE 2026, FSE 2025, ASE 2025, and ISSTA 2025. It was accepted to the 2nd International Workshop on Responsible Software Engineering (ResponsibleSE 2026), co-located with FSE, which reinforces its focus on responsible research practice rather than on launching a new benchmark.

## Practical Impact

For researchers, the paper provides a concrete standard for what an evaluation package should contain if the goal is durable scientific comparison rather than one-off demonstration. For practitioners, it clarifies why richer traces are necessary when evaluating coding agents, review agents, or repository-manipulation agents: without them, failures remain opaque and successes are hard to trust.

The paper also complements more deployment-oriented guidance such as **[[Anthropic’s 'Building Effective Agents' Guide]]**. That guide explains how to build agentic systems effectively; this paper explains how to evaluate them in a way that other teams can inspect, reproduce, and learn from.
