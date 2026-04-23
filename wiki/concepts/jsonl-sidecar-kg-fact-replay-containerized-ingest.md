---
title: "JSONL Sidecar Knowledge-Graph Fact Replay for Containerized Ingest Pipelines"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "e1abec72ac6d1d4aced535dcadb22b76009a9cea5bca69c6840036ee63725044"
sources:
  - raw/2026-04-22-copilot-session-wiki-ingest-pipeline-4-fix-implementation-6262ab1b.md
related:
  - "[[Post-Ingest Quality Fixes in Auto-Ingest Pipelines]]"
  - "[[Source-Aware Model Routing in Wiki Ingestion Pipelines]]"
  - "[[Auto-Ingest Pipeline for LLM-Powered Knowledge Wiki]]"
tier: hot
tags: [knowledge-graph, jsonl, auto-ingest, mempalace, pipeline]
quality_score: 65
---

# JSONL Sidecar Knowledge-Graph Fact Replay for Containerized Ingest Pipelines

## Overview

JSONL sidecar knowledge-graph replay is a deferred-write pattern for ingestion systems that can extract structured facts inside one runtime but are not allowed to write those facts to the target graph directly. In Labs-Wiki, the pattern bridges a gap between the `wiki-auto-ingest` container and [[MemPalace]]: the container can identify facts during page generation, but the actual knowledge-graph writer lives outside the container and must replay them later.

## How It Works

The core idea is to split **fact extraction** from **fact persistence**. The ingest worker still performs the cognitively hard part: reading a source, deciding which entities matter, and expressing explicit triples such as `created_by`, `uses`, or `evaluated_on`. What changes is where the write happens. Instead of calling a graph API inline, the worker serializes each fact as one JSON object per line and appends it to `wiki/.kg-pending.jsonl`. That file becomes a durable handoff queue between two trust domains: the unprivileged compile container and the host environment that can actually reach the graph.

JSONL is a particularly strong fit for this boundary because the unit of work is naturally record-shaped and append-only. Each line can stand on its own:

```json
{"subject":"ReasoningBank","predicate":"created_by","object":"Google Research","source_closet":"wiki/entities/reasoningbank.md","valid_from":"2026-04-21"}
```

That means the producer never has to reopen and rewrite a large array, worry about commas, or coordinate a complex transactional format. If one ingest emits three facts and the next emits two more, the shared file can simply grow by five lines. Host-side consumers can then read, validate, and replay line by line. In the checkpoint, that append-only contract matters because the prompt explicitly instructs the model-driven ingest to append with `>>` semantics rather than overwrite the queue.

The replay side is intentionally decoupled from the container. The new [[scripts/replay_kg_facts.py]] worker runs on the host via the MemPalace pipx interpreter and imports `mempalace.knowledge_graph.KnowledgeGraph` directly. It reads pending JSON objects, calls `add_triple(subject, predicate, obj, valid_from, valid_to, confidence, source_closet, source_file)`, and deletes the queue only when every line has been drained successfully. This matters operationally: if the host crashes mid-run or one line is malformed, the queue can remain on disk and be retried later instead of silently losing extracted knowledge.

The checkpoint also adds a dual-strategy replay hook inside `scripts/auto_ingest.py`. The success path first rebuilds the wiki index, then attempts replay through one of two direct channels: HTTP if `MEMPALACE_API_URL` is configured, or direct Python replay if the `mempalace` package is importable. If neither path is available, the code does **not** drop the facts. It logs that the lines are being left for host-side replay and exits cleanly. That behavior is the heart of the pattern: the compile pipeline remains successful even when the graph writer is unavailable, because graph persistence is now a deferred concern rather than a hard synchronous dependency.

Why does this work well in containerized systems? Because it respects deployment asymmetry. The container image is intentionally thin and isolated. It may not include MemPalace, may not have MCP access, and may not be trusted with the user's local graph database. The host, by contrast, already owns the persistent MemPalace installation and the SQLite graph. The sidecar queue turns that mismatch from a blocker into a protocol. Rather than pretending both environments are identical, the system defines a small data contract that each can satisfy independently.

There is also an architectural benefit for observability and auditability. Pending facts are visible as ordinary text in `wiki/.kg-pending.jsonl`, which makes failure inspection easier than debugging hidden subprocess state. Operators can `tail` the file, dry-run the replay worker, or manually inspect whether the model emitted the expected `subject`, `predicate`, and `object` keys. In a knowledge pipeline, this is valuable because graph writes are often harder to validate than markdown page generation. The queue acts as both buffer and evidence trail.

Finally, the pattern embodies a broader principle: **side effects that cross privilege boundaries should be replayable**. The compile step should still produce durable wiki pages even if downstream graph synchronization is delayed. By shifting KG writes into a replayable queue, the pipeline avoids coupling page creation, graph availability, and container permissions into one brittle success condition.

## Key Properties

- **Append-only work queue**: Each fact is one JSON object per line, so concurrent or sequential ingests can add work without rewriting prior state.
- **Privilege separation**: The container extracts facts; the host-side worker performs privileged graph writes through MemPalace.
- **Replayability**: Failed or deferred graph writes remain visible on disk and can be retried by cron or manual execution.
- **Schema visibility**: Required fields like `subject`, `predicate`, `object`, `source_closet`, and optional `valid_from` are inspectable without specialized tooling.
- **Non-blocking ingest success**: Page generation can complete even when graph access is unavailable.

## Limitations

This pattern does not provide exactly-once delivery by itself. If a replay worker partially succeeds and then crashes before trimming consumed lines, duplicate writes may need to be tolerated or deduplicated downstream. It also depends on the producer honoring append semantics; if a tool overwrites the JSONL file instead of appending, pending work can be lost. Finally, the queue only captures facts that are explicitly extracted from the source, so it does not solve ontology design, predicate normalization, or semantic validation on its own.

## Examples

A minimal producer/consumer split looks like this:

```python
# producer inside the ingest container
with open("wiki/.kg-pending.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(fact) + "\n")

# consumer on the host
for line in pending_file.read_text().splitlines():
    fact = json.loads(line)
    kg.add_triple(
        fact["subject"],
        fact["predicate"],
        fact["object"],
        valid_from=fact.get("valid_from"),
        source_closet=fact.get("source_closet"),
    )
```

In Labs-Wiki, the producer is the Copilot-driven ingest workflow, while the consumer is [[scripts/replay_kg_facts.py]] running from the MemPalace environment.

## Practical Applications

Use this pattern when a pipeline can extract structured facts in one environment but only a second environment has the credentials, libraries, or filesystem access needed to persist them. It is especially useful for homelab automations, restricted build containers, MCP-isolated services, and any workflow where wiki generation should remain available even when downstream graph synchronization is temporarily offline.

## Related Concepts

- **[[Post-Ingest Quality Fixes in Auto-Ingest Pipelines]]**: Both patterns harden the success path after model output, but sidecar replay handles cross-system side effects rather than page cleanup.
- **[[Source-Aware Model Routing in Wiki Ingestion Pipelines]]**: Routing determines how a source is compiled; sidecar replay determines how extracted facts leave the compile environment.
- **[[Auto-Ingest Pipeline for LLM-Powered Knowledge Wiki]]**: Provides the watcher-driven ingest architecture that this deferred-write pattern plugs into.

## Sources

- [[Copilot Session Checkpoint: Wiki Ingest Pipeline 4-Fix Implementation]] — introduces the JSONL sidecar contract, host replay worker, and replay fallback logic.
