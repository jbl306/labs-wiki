---
title: "auto_ingest.py"
type: entity
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "cb1641cfd3a617f69e5849c8b18e45f913175c5a97adb89f01ebd767b34bd251"
sources:
  - raw/2026-04-22-copilot-session-mobile-node-viewer-and-richer-github-ingestion-8b1dee20.md
  - raw/2026-04-22-copilot-session-self-synthesizing-r4-checkpoint-clusters-fc158a39.md
quality_score: 63
concepts:
  - auto-ingest-py
related:
  - "[[Self-Synthesizing Checkpoint Cluster Synthesis]]"
  - "[[Copilot Session Checkpoint: Self-synthesizing R4 checkpoint clusters]]"
  - "[[write_synth.py]]"
  - "[[backfill_checkpoint_cluster_synthesis.py]]"
tier: hot
tags: [synthesis-helper, wiki-integration, auto-ingest]
---

# auto_ingest.py

## Overview

auto_ingest.py is a core script in labs-wiki responsible for synthesis page generation, postprocessing, logging, and index rebuilding. It defines the synthesis dict contract and provides helpers for integration of new pages.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | 2026 |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

This script is central to the synthesis workflow, ensuring that manually authored synthesis dicts are formatted, validated, and deployed according to wiki standards.

## Associated Concepts

- **[[Self-Synthesizing Checkpoint Cluster Synthesis]]** — Defines synthesis dict contract and provides page generation helpers.

## Related Entities

- **[[write_synth.py]]** — Invokes helpers from auto_ingest.py for synthesis page creation.
- **[[backfill_checkpoint_cluster_synthesis.py]]** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Self-synthesizing R4 checkpoint clusters]] — where this entity was mentioned
- [[Copilot Session Checkpoint: Mobile Node Viewer And Richer GitHub Ingestion]] — additional source
