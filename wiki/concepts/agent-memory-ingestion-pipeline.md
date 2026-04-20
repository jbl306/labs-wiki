---
title: "Agent Memory Ingestion Pipeline"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "6d3926b294fd189631a5b0192148c2460f4f4d037b2814c551620137e4a5fae8"
sources:
  - raw/2026-04-20-agents-that-remember-introducing-agent-memory.md
quality_score: 100
concepts:
  - agent-memory-ingestion-pipeline
related:
  - "[[MemPalace Architecture and Migration]]"
  - "[[Hybrid Retrieval in Agent Memory Systems]]"
  - "[[Agents that remember: introducing Agent Memory]]"
tier: hot
tags: [ingestion-pipeline, memory-extraction, verification, classification, agent-memory]
---

# Agent Memory Ingestion Pipeline

## Overview

The ingestion pipeline in Agent Memory is responsible for extracting, verifying, classifying, and storing memories from agent conversations. It ensures that relevant information is persistently captured, deduplicated, and structured for efficient retrieval.

## How It Works

When a conversation is ingested, the pipeline begins with deterministic ID generation: each message receives a SHA-256 hash of session ID, role, and content, truncated to 128 bits. This guarantees idempotency, so repeated ingestion of the same conversation results in identical memory IDs.

Extraction runs in two parallel passes. The full pass chunks messages at roughly 10K characters with two-message overlap, processing up to four chunks concurrently. Each chunk is labeled with roles, absolute dates, and line indices for provenance. The detail pass runs alongside for longer conversations, using overlapping windows to extract concrete values (names, prices, version numbers, entity attributes) that broad extraction may miss. The results from both passes are merged for completeness.

Verification follows, with eight checks: entity identity, object identity, location context, temporal accuracy, organizational context, completeness, relational context, and factual support. Each extracted memory is either passed, corrected, or dropped based on these checks.

Classification assigns each memory to one of four types: facts (atomic, stable knowledge), events (time-specific occurrences), instructions (procedures, workflows), and tasks (ephemeral work-in-progress). Facts and instructions are keyed and superseded if a new memory with the same key is ingested, forming version chains. Tasks are excluded from vector indexing but remain searchable via full-text.

Storage uses INSERT OR IGNORE to skip duplicates. After the response, background vectorization prepends 3-5 search queries generated during classification to the memory content, bridging declarative and interrogative forms for embedding. Superseded vectors are deleted in parallel with new upserts.

## Key Properties

- **Idempotent Storage:** Deterministic content-addressed IDs ensure repeated ingestion does not create duplicates.
- **Parallel Extraction Passes:** Full and detail passes run concurrently for broad and concrete value extraction.
- **Eight-Point Verification:** Comprehensive checks ensure extracted memories are accurate and contextually valid.
- **Version Chains and Supersession:** Keyed facts and instructions are superseded, maintaining a forward-linked history.
- **Background Vectorization:** Embeddings are generated asynchronously, combining search queries and memory content.

## Limitations

Extraction quality depends on the accuracy of chunking and detail passes; errors can propagate. Verification may drop or misclassify relevant memories if checks are too strict or misapplied. Tasks are not vector-indexed, reducing semantic recall. Supersession relies on normalized topic keys, which may not capture nuanced changes.

## Example

A conversation about project setup is ingested:
- Full pass extracts 'user prefers pnpm', 'dark mode by default', 'React + TypeScript setup'.
- Detail pass identifies 'pnpm' as package manager, 'dark mode' as theme.
- Verification checks that 'pnpm' is user preference, not assistant suggestion.
- Classification keys 'package manager' and 'theme', superseding older memories if present.
- Storage inserts new memories, skips duplicates, and triggers background embedding.

## Visual

The second image shows a stylized robot agent in a box, surrounded by modular structures, representing the compartmentalized, multi-stage pipeline for memory extraction and storage.

## Relationship to Other Concepts

- **[[MemPalace Architecture and Migration]]** — Both systems use structured ingestion and deduplication for persistent agent memory.
- **[[Hybrid Retrieval in Agent Memory Systems]]** — Ingestion prepares memories for multi-channel retrieval.

## Practical Applications

Used for bulk ingestion during context compaction, explicit memory storage by agents, and maintaining durable knowledge across sessions. Enables shared team memory, code review feedback persistence, and chat bot contextual recall.

## Sources

- [[Agents that remember: introducing Agent Memory]] — primary source for this concept
