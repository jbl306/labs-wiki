---
title: "scripts/replay_kg_facts.py"
type: entity
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "e1abec72ac6d1d4aced535dcadb22b76009a9cea5bca69c6840036ee63725044"
sources:
  - raw/2026-04-22-copilot-session-wiki-ingest-pipeline-4-fix-implementation-6262ab1b.md
concepts: [jsonl-sidecar-kg-fact-replay-containerized-ingest, source-aware-model-routing-wiki-ingestion-pipelines]
related:
  - "[[MemPalace]]"
  - "[[scripts/auto_ingest.py]]"
  - "[[Labs-Wiki]]"
tier: hot
tags: [python, automation, mempalace, knowledge-graph, labs-wiki]
quality_score: 56
---

# scripts/replay_kg_facts.py

## Overview

`scripts/replay_kg_facts.py` is the host-side replay worker introduced to bridge Labs-Wiki's ingest container and the local [[MemPalace]] knowledge graph. Its job is simple but critical: read pending JSONL facts written by the ingest pipeline and persist them through `KnowledgeGraph.add_triple` in an environment that actually has MemPalace installed.

The script matters because it converts a container limitation into a recoverable workflow instead of a hard failure. The checkpoint states that the auto-ingest container cannot reach MemPalace MCP tools and does not have the package installed, so direct writes from the compile step would fail. By moving graph persistence into this dedicated worker, the ingest pipeline can still finish page generation while the host periodically drains deferred facts.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | 2026-04-22 |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Pipeline Role

The script sits downstream of [[scripts/auto_ingest.py]]. During ingestion, the pipeline now appends fact objects to `wiki/.kg-pending.jsonl` whenever an entity page yields explicit knowledge-graph facts. `scripts/replay_kg_facts.py` then runs from the MemPalace pipx interpreter on the host and consumes that queue. This separation lets the container stay lightweight while still keeping graph enrichment eventually consistent with newly created wiki pages.

The source notes that the cron schedule runs every 15 minutes and logs to `/home/jbl/logs/kg-replay.log`. That makes the worker part of the operational fabric of Labs-Wiki rather than an ad hoc repair tool. It is expected to wake up, drain pending facts, and remove the sidecar file once every line has been replayed successfully.

## Implementation Details

The script imports `mempalace.knowledge_graph.KnowledgeGraph` and uses the confirmed `add_triple(subject, predicate, obj, valid_from, valid_to, confidence, source_closet, source_file)` interface. In practice, that means the replay worker can preserve provenance from the wiki layer into the graph layer: every triple can point back to the entity markdown file that justified it and optionally carry a `valid_from` date when the source provides one.

This makes the worker more than a queue consumer. It is also the schema boundary between wiki facts and MemPalace's temporal triple model. If the JSONL sidecar is well-formed, the worker can translate wiki-derived assertions into graph state without involving the ingest model again.

## Operational Constraints

The checkpoint is explicit that the script must be run via `/home/jbl/.local/share/pipx/venvs/mempalace/bin/python`, not the container's interpreter. That constraint follows directly from where MemPalace is installed and where the SQLite knowledge-graph database lives. The script therefore depends on host-level filesystem access and the user's existing MemPalace environment rather than repo-local Python dependencies alone.

It also inherits the usual replay-worker tradeoffs: malformed JSON lines, duplicate deliveries, or downstream graph errors need to be handled by replay logic rather than by the original ingest. The benefit is that those failures are visible and retryable instead of being hidden inside the model compile step.

## Impact

`scripts/replay_kg_facts.py` enables Labs-Wiki to keep markdown compilation and graph synchronization loosely coupled. That makes the overall system more resilient: wiki pages still land even when MemPalace is unavailable, and graph writes can be retried independently. In a homelab setting, that is often the difference between a pipeline that works only during ideal conditions and one that survives real operational drift.
