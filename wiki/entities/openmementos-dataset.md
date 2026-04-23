---
title: "OpenMementos Dataset"
type: entity
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "83e4097d6c8d747e6aa2a78c7a183c40ba512003561361620dedae2faeaa34e2"
sources:
  - raw/2026-04-21-httpsgithubcommicrosoftmemento.md
concepts:
  - memento-blockwise-summarization-for-llms
  - reasoning-trace-segmentation-and-iterative-summarization
related:
  - "[[microsoft/memento]]"
  - "[[Memento]]"
  - "[[Microsoft]]"
  - "[[vLLM Block Masking Overlay]]"
tier: hot
tags: [dataset, llm, chain-of-thought, summarization, training-data]
quality_score: 71
---

# OpenMementos Dataset

## Overview

OpenMementos Dataset is the training-data counterpart to the Memento framework. It is referenced from the repo as the Hugging Face dataset containing chain-of-thought traces formatted in the Memento block-and-summary style so models can be supervised to emit the same protocol at inference time.

Its importance is not just that it stores examples, but that it stores examples in the exact structure the runtime expects: segmented reasoning blocks followed by compressed summaries. That makes it the bridge between raw reasoning traces and a model that can later support cache compaction safely.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Dataset |
| Created | Unknown |
| Creator | Microsoft |
| URL | https://huggingface.co/datasets/microsoft/OpenMementos |
| Status | Active |

## Role in Memento

The repo's `data/` pipeline explains how traces are transformed before they can become Memento-style supervision. Raw reasoning is split into structure-aware units, candidate boundaries are scored, blocks are chosen with dynamic programming, and each block is summarized with iterative judge-guided refinement.

OpenMementos represents the outcome of that preparation process: training data that teaches a model to preserve reasoning state in summaries rather than relying on the full original token history. In practice, that is what enables the inference side of [[Memento]] and the [[vLLM Block Masking Overlay]] to replace old block content with summaries instead of breaking the model's reasoning chain.

## Related Concepts

- **[[Memento Blockwise Summarization for LLMs]]** — The dataset teaches this output protocol.
- **[[Reasoning Trace Segmentation and Iterative Summarization]]** — The data-generation process used to create block-and-summary training traces.

## Related Entities

- **[[Memento]]** — Parent framework that consumes the dataset during model training.
- **[[Microsoft]]** — Publisher of both the repo and the Hugging Face dataset.
- **[[vLLM Block Masking Overlay]]** — Inference-side system that benefits from models trained on this format.

## Sources

- [[microsoft/memento]] — primary source describing the dataset's role
