---
title: "Agent Memory Frameworks"
type: concept
created: 2026-04-22
last_verified: 2026-08-13
source_hash: "15e0d38d97945d4e58427c03622de24ec2191b5d77cc532159579b7444219a6d"
sources:
  - raw/2026-04-22-reasoningbank-enabling-agents-to-learn-from-experience.md
  - raw/2026-04-22-250925140v2pdf.md
  - raw/2026-08-13-260206052v4pdf.md
quality_score: 88
concepts:
  - agent-memory-frameworks
  - memory-substrates-in-foundation-agents
  - memory-operations-in-foundation-agents
  - experience-driven-learning
  - self-evolving-agents
related:
  - "[[ReasoningBank]]"
  - "[[Agent Memory]]"
  - "[[Agentic Memory in Autonomous Agents]]"
  - "[[Memory Substrates in Foundation Agents]]"
  - "[[Memory Operations in Foundation Agents]]"
  - "[[Memory-Aware Test-Time Scaling]]"
tier: established
tags: [agent-memory, learning, frameworks, llm-agents, self-evolution, long-horizon]
---

# Agent Memory Frameworks

## Overview

Agent memory frameworks enable persistent agents to store, retrieve, evaluate, and reuse past experience so performance can improve across tasks and sessions. The survey literature broadens this idea beyond a single retrieval mechanism: a framework can be understood by its storage substrate, cognitive role, supported subject, operational lifecycle, and learning policy.

## Key Concept

As LLM agents move from batch-mode inference to persistent, long-running roles, they encounter continuous task streams. Without effective memory mechanisms, agents repeat strategic errors, discard useful experience, and fail to develop reusable strategies. A mature framework therefore treats memory as part of the agent’s adaptation loop:

1. capture interaction state and outcomes,
2. retrieve relevant prior experience,
3. assess success, failure, or utility,
4. distill experience into reusable knowledge or skills,
5. consolidate, revise, or forget memory under resource constraints.

The new survey organizes this design space along three orthogonal perspectives:

- **Memory substrate:** internal weights, latent states, and KV caches versus external vector indexes, text records, structural stores, and hierarchical stores.
- **Cognitive mechanism:** sensory and working memory gate current perception and reasoning; episodic, semantic, and procedural memory preserve and consolidate experience.
- **Memory subject:** user-centric memory supports personalization, while agent-centric memory supports the agent’s own experience, policies, and long-horizon behavior.

## Historical Approaches

### Trajectory Memory (Synapse)

- **Approach:** Store exhaustive records of actions taken.
- **Limitation:** Records detailed actions rather than distilling higher-level patterns.
- **Result:** Verbose, low-level memories that transfer less well.

### Workflow Memory (Agent Workflow Memory)

- **Approach:** Summarize workflows from successful task attempts.
- **Limitation:** Can overlook learning from failures, which are important signals for lesson distillation.
- **Result:** Incomplete learning signal and weaker preventative strategies.

### Reasoning-Based Memory (ReasoningBank)

- **Approach:** Distill generalizable reasoning strategies from successful and failed experiences.
- **Structure:** Structured memory items with titles, descriptions, and reasoning steps.
- **Innovation:** Active failure analysis for counterfactual learning.
- **Result:** Higher-level, more transferable strategies and emergent strategic maturity.

## Memory Operations and Learning Policies

The framework’s memory operations include storage/indexing, loading/retrieval, update/refresh, compression/summarization, and forgetting/retention. In multi-agent systems, these extend to memory architecture, routing, isolation, and conflict management.

Learning policies can be prompt-driven, parameterized through fine-tuning, or optimized with reinforcement learning. Prompt-driven policies may be static or dynamically revised. Parameterized policies internalize or stabilize memory behavior in model parameters. Reinforcement-learning approaches can make step-level memory decisions, represent trajectories, and coordinate cross-episode or multi-agent memory. The common direction is to make memory management itself increasingly adaptive rather than relying only on fixed heuristics.

## Emerging Properties

As agent memory systems mature, they enable:

- **Emergent strategic maturity:** Simple procedural rules can evolve into compositional structures with preventative logic.
- **Continuous self-evolution:** Agents can improve through experience without full retraining.
- **Failure-driven learning:** Mistakes become structured preventative lessons.
- **Long-horizon continuity:** Episodic, semantic, and procedural memory preserve state across tasks and sessions.
- **Resource-aware adaptation:** Compression, selective retention, and learned memory policies balance utility against latency, storage, and context costs.

## Evaluation and Limits

The survey groups memory evaluation into accuracy-based metrics, similarity-based metrics, and LLM-as-a-judge metrics. Useful measures include answer accuracy and F1, retrieval Recall@K/MAP/NDCG@K, success or goal-completion rate, memory integrity, false-memory rate, semantic similarity, faithfulness, and preference following. User-centric benchmarks focus on conversational consistency and personalization; agent-centric benchmarks focus on task execution, tool use, and long-horizon behavior.

Frameworks remain vulnerable to retrieval noise, stale or contradictory memories, false memory insertion, privacy and access-control failures, uncontrolled drift, and the cost of maintaining growing stores. A successful framework must therefore make provenance, retention, conflict handling, and evaluation explicit.

## Practical Applications

Agent memory frameworks are useful in coding agents, research assistants, browser agents, workflow automation, personalized assistants, and embodied or multimodal systems. The appropriate design depends on the task’s time horizon, rate of change, need for auditability, modality, and tolerance for latency. A practical system can combine internal runtime state with external episodic records and consolidated semantic or procedural memory.

## Relationship to Other Concepts

- **[[Memory Substrates in Foundation Agents]]** — Explains where framework memory is represented and the trade-offs among substrates.
- **[[Memory Operations in Foundation Agents]]** — Details the lifecycle and coordination operations that make memory adaptive.
- **[[Agentic Memory in Autonomous Agents]]** — Describes the temporal and behavioral role of memory in autonomous systems.
- **[[Memory-Aware Test-Time Scaling]]** — Shows how richer exploration and memory can reinforce each other.
- **[[ReasoningBank]]** — Exemplifies failure-aware reasoning-memory distillation.

## Sources

- [[A Survey of Agent Memory in the Second Half: Towards Self-Evolving and Long-Horizon Agents]] — Provides the unified taxonomy, operation model, learning-policy overview, evaluation categories, and open challenges.
- [[ReasoningBank: Enabling agents to learn from experience]] — Grounds the failure-aware reasoning-memory framework and experience-driven improvement.
- [[ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory]] — Grounds the interaction between memory quality and test-time exploration scaling.
