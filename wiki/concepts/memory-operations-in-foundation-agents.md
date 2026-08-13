---
title: "Memory Operations in Foundation Agents"
type: concept
created: 2026-08-13
last_verified: 2026-08-13
source_hash: "5188041197543db7e1169697b2686a797ee4a04261e2f29180683d75ce3ff09b"
sources:
  - raw/2026-08-13-260206052v4pdf.md
quality_score: 89
concepts:
  - memory-operations
  - retrieval
  - memory-consolidation
  - multi-agent-memory
related:
  - "[[Agent Memory Frameworks]]"
  - "[[Memory Substrates in Foundation Agents]]"
  - "[[Agent Memory Retrieval Pipeline]]"
  - "[[Memory Supersession Chains]]"
  - "[[Agentic Memory in Autonomous Agents]]"
tier: hot
tags: [agent-memory, memory-operations, consolidation, multi-agent-systems, self-evolution]
---

# Memory Operations in Foundation Agents

## Overview

Memory operations are the actions that construct, access, revise, compress, and retire an agent’s stored experience. The survey treats memory as an active subsystem rather than a static repository: a single-agent loop retrieves relevant experience, acts, evaluates outcomes, and updates memory, while multi-agent systems add routing, permission, isolation, and consistency concerns.

## How It Works

The survey identifies five core single-agent operation families:

1. **Storage and indexing:** Write memories with representations and metadata such as embeddings, timestamps, task identifiers, entities, or tool usage. Indexes may be vector-based, lexical, relational, graph-based, or hierarchical.
2. **Loading and retrieval:** Turn the current task or state into a query, retrieve candidate memories, then rank, filter, and inject a task-relevant subset into the active context. Retrieval can include structured expansion or specialized memory views.
3. **Update and refresh:** Revise stored facts, preferences, episodes, or skills as new information arrives. Update policies must handle changing state and can include consolidation of repeated experience into reusable knowledge.
4. **Compression and summarization:** Reduce token, storage, or retrieval cost by summarizing interaction histories, folding completed reasoning, or distilling trajectories into semantic knowledge and procedural skills.
5. **Forgetting and retention:** Decide what to preserve, evict, prune, or discard under bounded memory budgets. Selective retention is necessary because longer histories and larger stores can increase noise and cost.

These operations form a continual adaptation loop:

```
retrieve relevant memory
        ↓
plan and act
        ↓
evaluate success or failure
        ↓
update, consolidate, compress, or forget
        ↺
```

In multi-agent settings, operation policy also determines where memory is stored and who can access it. The survey distinguishes private-only, shared-workspace, hybrid, and orchestrated architectures. It also groups routing as orchestrator-based, agent-initiated, or memory-driven. Isolation and conflict handling are necessary because shared writes can duplicate, leak, or contradict information.

## Key Properties

- **Closed-loop adaptation:** Memory changes in response to execution outcomes, allowing experience to influence later decisions.
- **Selective context:** Retrieval and compression limit the active context to information relevant to the current task.
- **Consolidation:** Episodic experiences can be abstracted into semantic facts or procedural skills for reuse.
- **Governance:** Routing and permission policies control private, shared, and role-specific memory views.
- **Bounded growth:** Forgetting, pruning, deduplication, and retention policies keep memory costs manageable.
- **Evaluability:** Memory quality can be measured separately from final task success through retrieval, integrity, hallucination, and grounding metrics.

## Trade-offs and Limitations

Aggressive compression can remove rationale or temporal detail; weak compression leaves the system with noisy, expensive context. Retrieval can miss important memories or surface irrelevant ones. Shared workspaces improve reuse but increase conflict and privacy risks, while private stores reduce interference but duplicate information and limit collaboration. Central orchestration provides control but can become a bottleneck; local or memory-driven routing is more flexible but depends on filtering and ranking quality.

The survey also warns that end-task success alone may conceal memory failures. A system can complete short tasks while mishandling preference drift, provenance, contradiction resolution, false memories, or persistent state. Evaluation therefore needs both outcome metrics and memory-sensitive measures.

## Concrete Example

For a long-running coding agent:

1. Index each completed task with repository, issue, tools, outcome, and timestamp metadata.
2. Retrieve prior failures and successful procedures when a similar issue appears.
3. Evaluate the new attempt and record whether the retrieved lesson helped.
4. Summarize repeated patterns into a reusable debugging procedure.
5. Retain the procedure and high-value evidence, while pruning redundant traces.
6. In a multi-agent workflow, expose repository-wide lessons through a shared store but keep user-specific or credential-related records private.

This design uses memory operations to turn raw trajectories into controlled, reusable experience rather than repeatedly replaying the entire history.

## Relationship to Other Concepts

- **[[Memory Substrates in Foundation Agents]]** — Operations act on the internal and external substrates chosen for a system.
- **[[Agent Memory Retrieval Pipeline]]** — An implementation example of multi-channel loading and retrieval.
- **[[Memory Supersession Chains]]** — A concrete pattern for preserving historical versions while updating facts.
- **[[Agentic Memory in Autonomous Agents]]** — Frames memory operations as part of an agent’s planning and behavior loop.
- **[[Agent Memory Frameworks]]** — Covers the broader evolution from storage toward self-evolving memory systems.

## Sources

- [[A Survey of Agent Memory in the Second Half: Towards Self-Evolving and Long-Horizon Agents]] — Defines the core operations, multi-agent architectures, routing, and evaluation implications.
