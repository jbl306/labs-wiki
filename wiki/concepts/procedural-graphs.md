---
title: "Procedural Graphs"
type: concept
created: 2026-09-11
last_verified: 2026-09-11
source_hash: "1bc0b4741bb3665f648aa66b33b3b2f3374352f53cc3586680de2f75509d6983"
sources:
  - raw/2026-09-11-260909153v1pdf.md
quality_score: 91
concepts:
  - procedural-knowledge
  - graph-structured-planning
  - llm-agents
related:
  - "[[Agent Memory Frameworks]]"
  - "[[Agentic Memory in Autonomous Agents]]"
  - "[[Generative Procedural Graph Guidance]]"
  - "[[Self-Evolution of Procedural Graphs]]"
  - "[[Self-Managing Workflow Generation]]"
tier: hot
tags: [procedural-knowledge, llm-agents, graph-planning, tool-use, agent-memory]
---

# Procedural Graphs

## Overview

A Procedural Graph (PG) is an explicit, directed, and editable representation of what an LLM agent should do next. It externalizes procedural knowledge from model weights into nodes for tools, reasoning steps, skills, or task states, and attributed edges for the admissible transitions between them. The structure answers a procedural “what-to-do” question while leaving the solver free to reason about the task.

## How It Works

The formal graph is `G = (V, R, E, Φ)`, where `V` is the node set, `R` is the transition-relation vocabulary, `E` contains directed triplets `(u, r, v)`, and `Φ` maps edges to named attributes. In the paper’s implementation, those attributes are `condition`, `guidance`, and `pitfalls`. An edge therefore records both that `v` may follow `u` and the operational context for taking that transition.

Nodes can represent a tool call such as `cash_flow_forecast_calculation`, a reasoning step, or a status such as the beginning of a month. Relations include `LEADS_TO`, `TRIGGERS`, `PROVIDES_INPUT_FOR`, and `CONVERGES_TO`. A graph may begin as a hand-designed expert prior or as a minimal `Start → End` skeleton and can later be changed by adding or deleting nodes, edges, and edge attributes.

During execution, the graph is frozen. The framework identifies the node corresponding to the agent’s latest procedure, retrieves a connected neighborhood, and asks a guidance model to verbalize the relevant transitions. The solver receives this guidance alongside the query and trajectory, so PG functions as a soft structural prior rather than a hard finite-state controller.

```
Start → check_cash → forecast_runway → check_market → decide_capital
```

This separation is important: the graph constrains the space of plausible next actions and exposes dependencies, but the solver still chooses the concrete action and can adapt its reasoning to observations.

## Key Properties

- **Explicit procedural structure:** Admissible transitions are inspectable instead of being reconstructed from a flat history.
- **Attributed transitions:** Conditions, guidance, and pitfalls carry context that a bare adjacency list would lose.
- **External editability:** The graph can be revised without retraining the base model.
- **Local retrieval:** Execution can use the neighborhood around the active node rather than injecting every task procedure at every step.
- **Flexible integration:** Generated advice steers the solver but does not dictate its full chain of thought or action choice.

## Trade-offs and Limitations

PG adds graph-maintenance and inference complexity. A graph can encode the wrong procedure, and a soft guidance message can still be ignored or misinterpreted by the solver. Exact action-to-node matching may fail; the framework then falls back to the full graph, which increases context cost. Guidance calls add tokens and latency, and the paper’s results are benchmark- and model-specific rather than evidence that one graph topology transfers universally.

The representation also does not automatically guarantee semantic correctness. Structural validation checks endpoints, reachability, and configured cycle policy, but the refiner prompt is responsible for keeping action nodes compatible with the available tool catalog. Human priors can be harmful: in the MultiChallenge construction study, an unsuitable expert graph initially reduced performance before iterative evolution repaired it.

## Concrete Example

In EnterpriseArena, a useful procedure is to inspect cash, forecast runway, save notes, inspect market conditions, and only then decide whether to request financing or advance the month. The graph’s transitions make the dependency visible. Because funding arrives one to six months after a request, the procedure encourages early fundraising; because only one request may be pending, its guidance can warn the agent not to submit a second request while waiting.

## Relationship to Other Concepts

- **[[Agentic Memory in Autonomous Agents]]** — PG is a procedural-memory substrate that feeds ongoing action selection.
- **[[Agent Memory Frameworks]]** — Places PG alongside episodic, semantic, and other external memory designs.
- **[[Generative Procedural Graph Guidance]]** — Describes how a frozen graph is localized and verbalized at inference time.
- **[[Self-Evolution of Procedural Graphs]]** — Describes how execution feedback changes the graph offline.
- **[[Self-Managing Workflow Generation]]** — A related workflow-construction approach; PG makes transitions and their conditions explicit at execution time.

## Practical Applications

PG is suited to tool-using agents with ordering constraints, long-horizon state, or recurring failure modes: financial planning, customer-service tool use, embodied tasks, multi-turn instruction following, research workflows, and coding operations. It is most useful when a team needs procedures that can be inspected, revised, and evaluated independently of model weights.

## Sources

- [[Procedural Graphs: Self-Evolving Execution Structures for LLM Agents]] — Defines the representation, inference-time guidance, benchmarks, and self-evolution loop.