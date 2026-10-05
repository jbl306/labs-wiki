---
title: "Generative Procedural Graph Guidance"
type: concept
created: 2026-09-11
last_verified: 2026-09-11
source_hash: "1bc0b4741bb3665f648aa66b33b3b2f3374352f53cc3586680de2f75509d6983"
sources:
  - raw/2026-09-11-260909153v1pdf.md
quality_score: 90
concepts:
  - procedural-graph-guidance
  - local-retrieval
  - situational-guidance
related:
  - "[[Procedural Graphs]]"
  - "[[Memory Operations in Foundation Agents]]"
  - "[[Agentic Memory in Autonomous Agents]]"
  - "[[Self-Evolution of Procedural Graphs]]"
tier: hot
tags: [procedural-graphs, guidance, retrieval, llm-agents, tool-use]
---

# Generative Procedural Graph Guidance

## Overview

Generative Procedural Graph Guidance is the inference-time mechanism that turns a Procedural Graph and the agent’s current progress into a short, situation-aware recommendation. It combines exact localization of the latest procedure, extraction of a connected graph neighborhood, and language-model generation of guidance. The recommendation is appended to the solver prompt as a soft prior: it identifies the next strategic step and pitfalls without replacing the solver’s reasoning.

## How It Works

At decision step `t`, the framework keeps a query `q` and an interleaved action–observation trajectory. It matches the most recent procedure to a graph node, `u_t = Match(a_(t-1), V)`. If matching succeeds, it extracts the directed neighborhood reached within `h` hops; otherwise it supplies the complete graph as a fallback. The reported default is `h = 2`, paired with a recent trajectory window of `w = 3` steps.

A guidance model `Ψ` receives the selected graph context, query, and recent trajectory and generates `g_t`. It interprets each nearby edge’s condition, guidance, and pitfalls in topological context, so it can preserve prerequisites and downstream consequences that independent top-k retrieval might omit. The solver then samples or selects its next action from the query, full trajectory, and generated guidance.

```
locate latest procedure
        ↓
extract connected neighborhood (up to 2 hops)
        ↓
generate situational guidance from conditions, guidance, and pitfalls
        ↓
solver chooses the next action
```

The connected context matters when an action depends on an earlier check. For example, retrieving a transition for `submit` alone could omit the preceding `check_answer`; retrieving the local neighborhood exposes both the verification step and the permissible next action.

## Key Properties

- **Topology-aware retrieval:** Neighboring transitions preserve procedural dependencies instead of treating rules as unrelated snippets.
- **State-conditioned advice:** The guidance model combines graph attributes with the live query and recent trajectory.
- **Graceful fallback:** A failed exact match does not stop execution; the framework can use the full graph.
- **Soft control:** The solver remains responsible for the final action, retaining flexibility for observations not represented in the graph.
- **Configurable horizon:** The neighborhood depth and trajectory window can be adjusted for the task.

## Trade-offs and Limitations

Local generative guidance costs an additional model call and can increase total token use even when it shortens the solver trajectory. Full-graph context is particularly expensive and can distract the solver. Exact matching is brittle when action names or procedure descriptions differ from graph node IDs, while overly shallow neighborhoods can omit necessary prerequisites. The method also depends on the guidance model correctly verbalizing graph attributes; it is not a formal action validator.

In the Gemini 3.5 Flash ablation, subgraph generative guidance achieved 89.31 MultiChallenge accuracy, 63.99 GDPval rubric score, and 81.53 ALFWorld success, compared with 80.27, 54.80, and 72.58 for the no-graph baseline. It used fewer tokens than full-graph generative guidance, but localized guidance still used 33.4% more tokens on GDPval and 55.4% more on ALFWorld than the no-graph baseline.

## Concrete Example

Suppose an agent is managing liquidity. After `check_cash_in_bank`, the two-hop neighborhood can expose `cash_flow_forecast_calculation` followed by `save_note` and `check_market_data`. Guidance can tell the solver to project runway, preserve the result for the next cycle, and inspect market conditions before choosing between fundraising and month advancement. The graph supplies ordering and pitfalls; the solver still decides the request amount from the observed state.

## Relationship to Other Concepts

- **[[Procedural Graphs]]** — Provides the graph representation and edge-attribute schema consumed by this mechanism.
- **[[Memory Operations in Foundation Agents]]** — Local retrieval and context injection are specialized memory-loading operations.
- **[[Agentic Memory in Autonomous Agents]]** — Guidance makes stored procedural knowledge part of the agent’s behavior loop.
- **[[Self-Evolution of Procedural Graphs]]** — Changes the graph that guidance retrieves between evaluation rounds.

## Practical Applications

This mechanism is appropriate for agents that must preserve action dependencies while handling open-ended reasoning: function calling, embodied interaction, long-horizon planning, customer-service policies, and multi-turn instruction following. Local neighborhoods are especially useful when the full procedure library is too large or contains unrelated branches.

## Sources

- [[Procedural Graphs: Self-Evolving Execution Structures for LLM Agents]] — Specifies the locate–extract–generate pipeline and reports the local-versus-full graph ablation.