---
title: "A Survey of Agent Memory in the Second Half: Towards Self-Evolving and Long-Horizon Agents"
type: source
created: 2026-08-13
last_verified: 2026-08-13
source_hash: "5188041197543db7e1169697b2686a797ee4a04261e2f29180683d75ce3ff09b"
sources:
  - raw/2026-08-13-260206052v4pdf.md
quality_score: 90
concepts:
  - agent-memory-frameworks
  - memory-substrates-in-foundation-agents
  - memory-operations-in-foundation-agents
related:
  - "[[Agent Memory Frameworks]]"
  - "[[Agentic Memory in Autonomous Agents]]"
  - "[[Explicit Memory in LLM Systems]]"
  - "[[Implicit Memory in LLMs]]"
  - "[[Implicit vs. Explicit vs. Agentic Memory in LLM Systems]]"
tier: hot
tags: [agent-memory, foundation-agents, long-horizon-agents, self-evolution, survey]
---

# A Survey of Agent Memory in the Second Half: Towards Self-Evolving and Long-Horizon Agents

## Summary

This survey presents foundation-agent memory as a systems capability for long-horizon, dynamic, and user-dependent tasks. It organizes the literature along three orthogonal dimensions—memory substrates, cognitive mechanisms, and memory subjects—and then analyzes memory operations, multi-agent coordination, learning policies, scaling, evaluation, applications, and open research directions.

The paper argues that memory is increasingly the substrate through which agents self-evolve: short-term memory selects and abstracts experiences during execution, while episodic, semantic, and procedural memory consolidate them into reusable knowledge and skills. It reports a systematic review of 218 key articles published between 2023 Q1 and 2025 Q4.

## Key Points

- Foundation-agent memory is classified by **memory substrate** (internal or external), **cognitive mechanism** (sensory, working, episodic, semantic, or procedural), and **memory subject** (user-centric or agent-centric).
- External substrates include vector indexes, text records, structural stores, and hierarchical stores; internal substrates include weights, latent states, and transformer KV caches.
- A single-agent memory system is described through storage/indexing, loading/retrieval, update/refresh, compression/summarization, and forgetting/retention operations.
- Multi-agent memory introduces private-only, shared-workspace, hybrid, and orchestrated architectures, plus orchestrator-based, agent-initiated, and memory-driven routing.
- The survey groups memory evaluation into accuracy-based, similarity-based, and LLM-as-a-judge metrics, and distinguishes user-centric from agent-centric benchmarks.
- Open directions include continual learning and self-evolving agents, collaborative human-agent memory, efficient memory infrastructure, trustworthy lifelong personalization, multimodal and embodied memory, and more realistic longitudinal evaluation.

## Concepts Extracted

- **[[Agent Memory Frameworks]]** — A broad framework for persistent memory that lets agents retrieve, consolidate, and reuse experience for continual improvement.
- **[[Memory Substrates in Foundation Agents]]** — The internal and external storage forms used to represent agent memory, with explicit trade-offs in latency, persistence, update flexibility, scalability, and precision.
- **[[Memory Operations in Foundation Agents]]** — The storage, retrieval, update, compression, forgetting, routing, and conflict-management operations that turn a memory store into an adaptive control subsystem.

## Entities Mentioned

- **AgentMemoryWorld/Awesome-Agent-Memory** — A roadmap resource shown in the survey’s timeline of foundation-agent memory frameworks.
- **Foundation agent** — The survey’s term for an autonomous or semi-autonomous system driven by a foundation model and augmented with perception, reasoning, planning, tool use, and memory management.

## Notable Quotes

> "Memory, with hundreds of papers released in 2025, therefore emerges as the critical solution to fill the utility gap."

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-08-13-260206052v4pdf.md` |
| Type | research survey / paper |
| Author | Wei-Chieh Huang et al. |
| Date | Not stated in the fetched content |
| URL | https://arxiv.org/pdf/2602.06052v4 |
