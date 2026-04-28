---
title: "The AI Hippocampus: How Far are We From Human Memory?"
type: source
created: '2026-04-28'
last_verified: '2026-04-28'
source_hash: "5c076b0d6707c2a164db74d06089b8cef513bc2e88042923d3246c2fe75b7203"
sources:
  - raw/2026-04-28-260109113v1pdf.md
concepts:
  - implicit-memory-llms
  - explicit-memory-llm-systems
  - agentic-memory-autonomous-agents
related:
  - "[[Agent Memory Frameworks]]"
  - "[[Implicit Memory in LLMs]]"
  - "[[Explicit Memory in LLM Systems]]"
  - "[[Agentic Memory in Autonomous Agents]]"
  - "[[Implicit vs Explicit vs Agentic Memory in LLM Systems]]"
  - "[[Agent Memory]]"
  - "[[OpenMemory]]"
  - "[[ReasoningBank]]"
  - "[[Agent Workflow Memory]]"
source_url: https://arxiv.org/abs/2601.09113
tags: [arxiv, llm-memory, multimodal-llms, survey, agentic-memory, continual-learning]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 65
---

# The AI Hippocampus: How Far are We From Human Memory?

## Summary

This survey frames memory as a core capability for moving large language models and multimodal LLMs from static next-token predictors toward interactive systems that can adapt, personalize, and operate over longer time horizons. It organizes the space into three major paradigms—[[Implicit Memory in LLMs]], [[Explicit Memory in LLM Systems]], and [[Agentic Memory in Autonomous Agents]]—and closes by highlighting multimodal extensions, benchmark needs, and unresolved challenges around capacity, alignment, factual consistency, and interoperability.

## Key Points

- The paper argues that memory is no longer a peripheral add-on for LLMs; it is a foundational mechanism for reasoning quality, adaptability, and contextual fidelity in long-running systems.
- Its core taxonomy has three buckets: **implicit memory** stored in model parameters, **explicit memory** stored in external retrievable systems, and **agentic memory** embedded in persistent autonomous-agent workflows.
- **Implicit memory** covers what pre-trained transformers retain internally, including memorized facts, associative retrieval patterns, and latent support for contextual reasoning.
- **Explicit memory** covers external, queryable stores such as text corpora, dense vector indexes, and graph-structured knowledge representations that can be updated without retraining the base model.
- **Agentic memory** is presented as temporally extended memory for autonomous agents, supporting long-horizon planning, self-consistency, and collaborative multi-agent behavior.
- The survey explicitly extends the discussion beyond text-only models into multimodal settings where memory has to preserve coherence across vision, language, audio, and action.
- The paper emphasizes that memory design is not just a storage problem; it is also an architectural and systems problem involving retrieval quality, update pathways, provenance, and interface boundaries between model and memory.
- Open research challenges named in the abstract include **memory capacity**, **alignment**, **factual consistency**, and **cross-system interoperability**, which together define much of the practical frontier for production memory systems.
- The paper was posted to arXiv as **2601.09113v1** on **2026-01-14**, has DOI **10.48550/arXiv.2601.09113**, and lists **Transactions on Machine Learning Research (11/2025)** as a journal reference.

## Key Concepts

- [[Agent Memory Frameworks]]
- [[Implicit Memory in LLMs]]
- [[Explicit Memory in LLM Systems]]
- [[Agentic Memory in Autonomous Agents]]
- [[Implicit vs Explicit vs Agentic Memory in LLM Systems]]

## Related Entities

- **[[Agent Memory]]** — Cloudflare's managed memory service is a concrete example of explicit external memory coupled to agent workflows.
- **[[OpenMemory]]** — An open, tool-oriented memory layer relevant as an implementation example of externalized memory infrastructure.
- **[[ReasoningBank]]** — A research framework that exemplifies agentic memory by learning structured reasoning lessons from agent trajectories.
- **[[Agent Workflow Memory]]** — Prior art for workflow-centric agent memory that is useful for contrasting narrower agent-memory designs with the survey's broader taxonomy.
