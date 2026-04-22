---
title: "Memory Supersession Chains"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "d91b38ada9d4efe004c00599e1912104a61ce1104675de55ba02a3cfa6ad1e70"
sources:
  - raw/2026-04-19-6372438pdf.md
  - raw/2026-04-20-agents-that-remember-introducing-agent-memory.md
quality_score: 84
concepts:
  - memory-supersession-chains
related:
  - "[[Agent Memory Ingestion Pipeline]]"
  - "[[Agents that remember: introducing Agent Memory]]"
tier: hot
tags: [agent-memory, supersession, versioning, provenance, auditability]
---

# Memory Supersession Chains

## Overview

Memory Supersession Chains are a versioning mechanism in Agent Memory, where new memories with the same key replace older ones, maintaining a forward pointer for version history. This ensures that facts and instructions remain current while preserving provenance.

## How It Works

When a new memory (fact or instruction) is ingested with a normalized topic key matching an existing memory, the system does not delete the old memory outright. Instead, it marks the old memory as superseded, creating a forward pointer to the new memory. This forms a chain of versions, allowing retrieval systems to trace the evolution of a particular fact or instruction over time.

Supersession chains are critical for maintaining institutional knowledge in dynamic environments. For example, if a project changes its package manager from npm to pnpm, the supersession chain records both states, with the latest memory representing the current truth. This mechanism also supports auditability and provenance tracking, as each memory retains its insertion date, source transcript, and prior versions.

In storage, superseded memories are excluded from the vector index to keep retrieval lean, but remain accessible via full-text search. When new memories are upserted, vectors for old versions are deleted in parallel, ensuring efficient storage and retrieval.

## Key Properties

- **Version Chain with Forward Pointer:** Each superseded memory points to its successor, forming a chain of historical versions.
- **Keyed Memory Classification:** Facts and instructions are keyed for versioning; events and tasks are not superseded.
- **Efficient Vector Index Management:** Superseded memories are removed from the vector index, reducing retrieval noise.
- **Provenance and Auditability:** Each memory retains source information and insertion date for traceability.

## Limitations

Supersession chains require careful key normalization; accidental key mismatches can fragment version history. Only facts and instructions are versioned; events and tasks are not, which may limit auditability for certain memory types. Overly aggressive supersession can obscure nuanced changes if not managed properly.

## Example

If a memory records 'user prefers npm', and later 'user prefers pnpm', the latter supersedes the former. The chain allows retrieval of both states, with the latest memory representing the current preference.

## Visual

No explicit diagram, but the version chain mechanism is described in text.

## Relationship to Other Concepts

- **[[Agent Memory Ingestion Pipeline]]** — Supersession chains are created during classification and storage in the ingestion pipeline.

## Practical Applications

Used for tracking evolving facts and instructions in coding agents, team-shared memory profiles, and audit trails for operational decisions. Supports durable knowledge management and provenance in agentic workflows.

## Sources

- [[Agents that remember: introducing Agent Memory]] — primary source for this concept
- [[6372438.pdf]] — additional source
