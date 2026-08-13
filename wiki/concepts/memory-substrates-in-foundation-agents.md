---
title: "Memory Substrates in Foundation Agents"
type: concept
created: 2026-08-13
last_verified: 2026-08-13
source_hash: "5188041197543db7e1169697b2686a797ee4a04261e2f29180683d75ce3ff09b"
sources:
  - raw/2026-08-13-260206052v4pdf.md
quality_score: 88
concepts:
  - memory-substrates
  - external-memory
  - internal-memory
  - foundation-agents
related:
  - "[[Agent Memory Frameworks]]"
  - "[[Explicit Memory in LLM Systems]]"
  - "[[Implicit Memory in LLMs]]"
  - "[[Memory Operations in Foundation Agents]]"
tier: hot
tags: [agent-memory, memory-substrates, foundation-agents, retrieval, long-context]
---

# Memory Substrates in Foundation Agents

## Overview

A memory substrate is the storage form in which a foundation agent retains knowledge, interaction history, or runtime state. The survey separates substrates into **external memory**, stored outside model parameters or state and accessed through explicit retrieval and updates, and **internal memory**, stored in parameters or inference-time states. This distinction exposes the main engineering trade-off between scalable, refreshable storage and low-latency model-local state.

## How It Works

External memory separates computation from knowledge. The agent writes information to and reads it from a store that may be represented as:

- **Vector indexes:** memory items and queries are embedded into a shared space, then approximate-nearest-neighbor search returns semantically similar items.
- **Text records:** human-readable summaries, semantic facts, and chronological episodic logs are edited and selectively copied into the active context.
- **Structural stores:** relational tables, graphs, or trees expose symbolic queries, traversals, joins, and multi-level abstractions.
- **Hierarchical stores:** multiple specialized modules hold categories such as core user facts, episodic events, semantic knowledge, procedures, resources, or protected knowledge, with a manager routing requests to the appropriate store.

Internal memory is kept within the model architecture:

- **Weights** encode information through pre-training, post-training, continual learning, model editing, or distillation.
- **Latent states** carry intermediate hidden representations across steps or segments; they usually support runtime continuity rather than durable cross-session persistence.
- **KV caches** retain attention keys and values from previous tokens to accelerate autoregressive decoding, trading memory footprint and implementation complexity for lower repeated-computation cost.

The substrate is only useful when paired with operations that make its contents accessible and maintainable. External stores require indexing and retrieval; internal stores require parameter or state-management methods. The survey therefore treats substrate choice as one axis of a larger memory design, alongside cognitive role and memory subject.

## Key Properties

- **Persistence:** External memory can survive sessions; latent states and KV caches are typically runtime-scoped, while weights persist until changed.
- **Update flexibility:** External entries can be inserted, updated, or deleted directly; weight memory generally requires costly parameter-level intervention.
- **Latency:** Internal memory is accessed through the model’s forward computation or GPU-resident state, while external access depends on index, corpus size, and ranking.
- **Scalability:** External stores can grow independently of model architecture, but incur storage, indexing, and retrieval costs.
- **Precision and noise:** External retrieval can return irrelevant context when ranking is weak; internal memory avoids a separate retrieval step but can suffer interference or overwrite during updates.
- **Context overhead:** Textual external memory may add prompt tokens, whereas latent and parametric approaches can reduce explicit context transfer at the cost of model or runtime resources.

## Trade-offs and Limitations

External memory is easier to refresh, audit, replace, and share across sessions, but it adds retrieval latency and can become noisy as the corpus grows. It also needs summarization, selective retention, deduplication, and pruning to control storage and context costs. Internal memory offers fast access and can avoid a retrieval boundary, but parameter updates may cause interference or forgetting, latent state consumes runtime resources, and KV caches are transient.

No single substrate covers every horizon and workload. A long-running coding agent may use a working-context or KV-cache layer for the current task, episodic text or vector records for past runs, and semantic or procedural stores for reusable knowledge. The survey’s taxonomy supports composing these layers instead of treating internal and external memory as mutually exclusive alternatives.

## Concrete Example

A research agent can use the following layered design:

1. Keep current tool outputs and active reasoning in working context and runtime state.
2. Store completed search episodes as timestamped text records with metadata.
3. Index stable findings in a vector or graph store for semantic retrieval.
4. Consolidate recurring search procedures into a procedural skill record.
5. Periodically prune low-value or obsolete episodes while preserving provenance for retained knowledge.

A query can then retrieve a small set of relevant episodes and semantic facts without replaying the full interaction history.

## Relationship to Other Concepts

- **[[Explicit Memory in LLM Systems]]** — Covers the external-memory side of this taxonomy, including text, vector, and graph representations.
- **[[Implicit Memory in LLMs]]** — Covers knowledge internalized in model parameters and activation dynamics.
- **[[Memory Operations in Foundation Agents]]** — Describes the lifecycle operations required to make a substrate adaptive.
- **[[Agent Memory Frameworks]]** — Places substrate choice within broader persistent and self-evolving agent-memory designs.

## Sources

- [[A Survey of Agent Memory in the Second Half: Towards Self-Evolving and Long-Horizon Agents]] — Defines the internal/external substrate taxonomy and its trade-offs.
