---
title: "Procedural Graphs: Self-Evolving Execution Structures for LLM Agents"
type: source
created: 2026-09-11
last_verified: 2026-09-11
source_hash: "1bc0b4741bb3665f648aa66b33b3b2f3374352f53cc3586680de2f75509d6983"
sources:
  - raw/2026-09-11-260909153v1pdf.md
quality_score: 92
concepts:
  - procedural-graphs
  - generative-procedural-graph-guidance
  - self-evolution-of-procedural-graphs
related:
  - "[[Agent Memory Frameworks]]"
  - "[[Memory Operations in Foundation Agents]]"
  - "[[Self-Managing Workflow Generation]]"
tier: hot
tags: [llm-agents, procedural-knowledge, graph-planning, agent-memory, self-evolution]
---

# Procedural Graphs: Self-Evolving Execution Structures for LLM Agents

## Summary

This paper introduces the Procedural Graph (PG), an explicit directed graph that represents procedural knowledge as connected transitions between tool actions, reasoning steps, and task states. At inference time, a guidance model retrieves the active node’s local neighborhood and translates edge attributes into situational advice; offline, an LLM refiner proposes graph edits from successful and failed trajectories, with validation gating and rejection memory controlling which edits persist.

In the main comparison across six benchmarks and four language models, PG ranks first or joint first in 21 of 24 model–benchmark settings. EnterpriseArena is evaluated separately. The paper also reports that localized generative guidance is more effective and cheaper than exposing the full graph, while iterative self-evolution can build useful graphs from a minimal skeleton and repair a flawed expert prior.

## Key Points

- A PG is a directed, attributed graph whose nodes abstract tools, skills, reasoning steps, or task statuses; edges encode admissible procedural transitions.
- Edge attributes provide a condition, actionable guidance, and pitfalls, allowing the same graph structure to express when and how a transition should be taken.
- Online guidance follows a locate–extract–generate pipeline: match the latest action to a node, retrieve a connected neighborhood, and generate step-level guidance for the solver.
- Offline self-evolution contrasts scored trajectories, adds missing nodes or edges, prunes failure-inducing structure, and revises attributes.
- Candidate graphs are accepted only when structurally valid and no worse on held-out validation; rejected candidates are retained as negative evidence.
- In a long-horizon financial simulator, PG improves survival for three of four evaluated solvers and encourages anticipatory fundraising before capital-delivery delays become dangerous.
- The main cost is additional guidance computation and tokens; localized retrieval reduces this overhead relative to full-graph guidance but still costs more than an unguided baseline in some tasks.

## Concepts Extracted

- **[[Procedural Graphs]]** — An explicit, editable graph for representing and retrieving what an LLM agent should do next.
- **[[Generative Procedural Graph Guidance]]** — Localized graph retrieval translated into soft, situation-aware instructions during execution.
- **[[Self-Evolution of Procedural Graphs]]** — A validation-gated feedback loop that mutates graph topology and edge attributes from execution traces.

## Entities Mentioned

- Yuxing Lu — first author; the paper lists Google, Georgia Institute of Technology, and Peking University affiliations.
- EnterpriseArena — long-horizon financial decision-making simulator used to evaluate survival under delayed funding and macroeconomic crises.
- Claude Sonnet 4.6, Gemini 3.1 Pro, Gemini 3.5 Flash, and Grok 4.1 Fast — language models used as solvers, guidance models, and refiners.

## Notable Quotes

> "A Procedural Graph organizes procedural knowledge into (procedure, relation, procedure) triplets." — abstract

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-09-11-260909153v1pdf.md` |
| Type | research paper |
| Author | Yuxing Lu, Yicheng Chen, Shanchan Wu, and Sercan Ö. Arık |
| Date | Not stated in fetched content |
| URL | https://arxiv.org/pdf/2609.09153 |