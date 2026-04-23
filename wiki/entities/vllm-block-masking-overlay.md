---
title: "vLLM Block Masking Overlay"
type: entity
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "83e4097d6c8d747e6aa2a78c7a183c40ba512003561361620dedae2faeaa34e2"
sources:
  - raw/2026-04-21-httpsgithubcommicrosoftmemento.md
concepts:
  - block-masking-for-llm-kv-cache-compaction
  - memento-blockwise-summarization-for-llms
related:
  - "[[microsoft/memento]]"
  - "[[Memento]]"
  - "[[Microsoft]]"
  - "[[KV Cache and Paged Attention in Large Language Models]]"
tier: hot
tags: [vllm, llm, inference, kv-cache, block-masking, microsoft]
quality_score: 82
---

# vLLM Block Masking Overlay

## Overview

The vLLM Block Masking Overlay is the inference-side runtime shipped inside `microsoft/memento`. Instead of being a separate standalone server, it is a patch set over stock vLLM 0.13.x that teaches the scheduler and KV cache manager how to recognize Memento block and summary delimiters during generation.

Its role is to turn the Memento format from a training convention into a systems optimization. Once a Memento-formatted model emits `<|summary_end|>`, the overlay can evict the completed reasoning block from the KV cache and continue generation from the shorter summary state, effectively stretching reasoning length within the same context budget.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Microsoft |
| URL | N/A |
| Status | Active |

## Core Mechanism

The overlay monitors generation token by token and tracks the lifecycle of blocks and summaries. When compaction is enabled, it treats the summary as the durable memory artifact and the preceding reasoning block as disposable cache content.

The runtime behavior is controlled through `BlockMaskingConfig`, including whether to preserve delimiters, how many recent blocks to keep, whether compaction should wait until `<|summary_end|>`, and whether the final block should be retained for answer generation. This makes the overlay the operational bridge between [[Memento Blockwise Summarization for LLMs]] and real serving infrastructure.

## Installation and Operations

The repo documents the overlay as a pure-Python patch over stock `vllm==0.13.0`, applied with `bash install_overlay.sh`. The installer copies modified Python files on top of the installed vLLM package, restores two critical `.so`-interface files from the stock wheel, and verifies that the patched runtime imports cleanly.

Because the overlay is version-coupled to vLLM 0.13.x and requires prefix caching to remain disabled, it is best viewed as a research-serving environment rather than a transparent production extension.

## Related Pages

- **[[Memento]]** — The parent framework that relies on this overlay at inference time.
- **[[microsoft/memento]]** — Source repository containing the overlay files and setup instructions.
- **[[KV Cache and Paged Attention in Large Language Models]]** — Broader inference-memory context for what the overlay modifies.

## Sources

- [[microsoft/memento]] — primary source for the overlay
