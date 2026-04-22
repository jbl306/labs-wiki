---
title: "write_synth.py"
type: entity
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "cb1641cfd3a617f69e5849c8b18e45f913175c5a97adb89f01ebd767b34bd251"
sources:
  - raw/2026-04-22-copilot-session-self-synthesizing-r4-checkpoint-clusters-fc158a39.md
quality_score: 55
concepts:
  - write-synth-py
related:
  - "[[Self-Synthesizing Checkpoint Cluster Synthesis]]"
  - "[[Copilot Session Checkpoint: Self-synthesizing R4 checkpoint clusters]]"
  - "[[backfill_checkpoint_cluster_synthesis.py]]"
  - "[[auto_ingest.py]]"
tier: hot
tags: [synthesis-script, wiki-tool, checkpoint-cluster]
---

# write_synth.py

## Overview

write_synth.py is a custom Python script prepared to generate synthesis pages for checkpoint clusters in the labs-wiki. It holds manually authored synthesis dicts for each cluster and invokes existing helpers to create, validate, and deploy synthesis pages, bypassing external LLM API calls.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | 2026 |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

This script is the main deliverable for the self-synthesizing checkpoint cluster synthesis workflow, enabling manual synthesis page creation and integration with the wiki without incurring external API costs.

## Associated Concepts

- **[[Self-Synthesizing Checkpoint Cluster Synthesis]]** — write_synth.py implements the synthesis workflow for checkpoint clusters.

## Related Entities

- **[[backfill_checkpoint_cluster_synthesis.py]]** — Provides helper functions reused by write_synth.py.
- **[[auto_ingest.py]]** — Source of synthesis page generation and postprocessing helpers.

## Sources

- [[Copilot Session Checkpoint: Self-synthesizing R4 checkpoint clusters]] — where this entity was mentioned
