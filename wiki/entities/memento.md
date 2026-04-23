---
title: "Memento"
type: entity
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "83e4097d6c8d747e6aa2a78c7a183c40ba512003561361620dedae2faeaa34e2"
sources:
  - raw/2026-04-21-httpsgithubcommicrosoftmemento.md
concepts:
  - memento-blockwise-summarization-for-llms
  - block-masking-for-llm-kv-cache-compaction
  - reasoning-trace-segmentation-and-iterative-summarization
related:
  - "[[microsoft/memento]]"
  - "[[Microsoft]]"
  - "[[OpenMementos Dataset]]"
  - "[[vLLM Block Masking Overlay]]"
  - "[[KV Cache and Paged Attention in Large Language Models]]"
tier: hot
tags: [llm, framework, long-context, kv-cache, summarization, microsoft]
quality_score: 85
---

# Memento

## Overview

Memento is an open-source framework from Microsoft for extending the effective output length of large language models without increasing the underlying context window. It structures chain-of-thought reasoning into explicit blocks and summaries, then uses those summaries as the durable state that survives after old reasoning blocks are evicted from the KV cache.

What makes Memento notable is that it is not just a prompting trick. The repo combines a training-data pipeline for producing block-and-summary supervision with a patched vLLM runtime that performs cache compaction during inference, which makes the framework a coordinated training-plus-serving design rather than a single algorithmic tweak.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Framework |
| Created | 2026 |
| Creator | Microsoft |
| URL | https://github.com/microsoft/memento |
| Status | Active |

## Core Concept

Memento addresses a core transformer limitation: every generated token normally remains part of the active context unless the model reaches the context limit. Memento changes that by asking the model to periodically write a compact summary of its reasoning and then treating that summary as the state that later steps attend to.

The mechanism depends on two supporting ideas. First, the model has to learn the Memento format itself, which is captured in [[Memento Blockwise Summarization for LLMs]] and supported by [[Reasoning Trace Segmentation and Iterative Summarization]]. Second, the server has to understand those delimiters and compact the KV cache accordingly, which is the job of [[vLLM Block Masking Overlay]] and the broader idea in [[Block Masking for LLM KV Cache Compaction]].

## Training and Inference Stack

The `data/` pipeline converts raw chain-of-thought traces into supervised examples with sentence boundaries, scored transitions, dynamic-programming blocks, and judge-refined summaries. The `vllm/` overlay then patches stock vLLM 0.13.x so a served Memento checkpoint can watch for `<|summary_end|>` and evict the completed block from the KV cache.

Together, those two halves let Memento replace "keep every old token forever" with "keep summaries plus whatever recent high-resolution context is still needed." That trade-off is what makes the framework interesting for long-form reasoning workloads such as code generation, scientific explanation, and multi-step analysis.

## Related Entities

- **[[Microsoft]]** — The organization publishing the framework and repository.
- **[[OpenMementos Dataset]]** — Training data source for teaching models the Memento block+summary protocol.
- **[[vLLM Block Masking Overlay]]** — Runtime implementation that makes summary-based cache compaction possible.

## Sources

- [[microsoft/memento]] — primary repository and technical source
