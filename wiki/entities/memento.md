---
title: "Memento"
type: entity
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "7b344980e889d401d340d2539bd18583a585c26640fe19f36c596d887e647ba2"
sources:
  - raw/2026-04-21-httpsgithubcommicrosoftmemento.md
quality_score: 68
concepts:
  - memento
related:
  - "[[Memento Blockwise Summarization for LLMs]]"
  - "[[microsoft/memento]]"
  - "[[Microsoft]]"
  - "[[OpenMementos Dataset]]"
tier: hot
tags: [llm, tool, memory, summarization]
---

# Memento

## Overview

Memento is an open-source framework developed by Microsoft for extending the effective output length of large language models. It achieves this by segmenting chain-of-thought reasoning into blocks and generating summaries (mementos) after each block, which allows for selective eviction of context from the model's KV cache. The repository includes a data pipeline for formatting training data and a vLLM overlay for inference with block masking.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Microsoft |
| URL | https://github.com/microsoft/memento |
| Status | Active |

## Relevance

Memento addresses a key limitation of transformer-based LLMs—their fixed context window—by enabling longer, more complex reasoning without increasing model size. Its approach is relevant for research and applications requiring extended context, such as advanced question answering, code generation, and scientific analysis.

## Associated Concepts

- **[[Memento Blockwise Summarization for LLMs]]** — Implements the blockwise summarization and KV cache compaction protocol.

## Related Entities

- **[[Microsoft]]** — Creator
- **vLLM Overlay for Memento** — co-mentioned in source (Tool)
- **[[OpenMementos Dataset]]** — co-mentioned in source (Dataset)

## Sources

- [[microsoft/memento]] — where this entity was mentioned
