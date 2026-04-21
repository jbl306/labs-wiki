---
title: "Memento: Extending LLM Output Length via Blockwise Summarization and KV Cache Compaction"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "7b344980e889d401d340d2539bd18583a585c26640fe19f36c596d887e647ba2"
sources:
  - raw/2026-04-21-httpsgithubcommicrosoftmemento.md
quality_score: 100
concepts:
  - memento-blockwise-summarization-for-llms
related:
  - "[[Memento Blockwise Summarization for LLMs]]"
  - "[[Memento]]"
  - "[[OpenMementos Dataset]]"
  - "[[Microsoft]]"
tier: hot
tags: [context-window, llm, memory, kv-cache, summarization, block-masking]
---

# Memento: Extending LLM Output Length via Blockwise Summarization and KV Cache Compaction

## Summary

The Memento repository by Microsoft introduces a method for extending the effective output length of large language models (LLMs) by splitting chain-of-thought reasoning into blocks and generating summaries (mementos) after each block. These summaries allow the model to evict block content from the KV cache, enabling continued reasoning within a fixed context window. The repository provides a data pipeline for converting traces into the Memento format and a vLLM overlay for efficient inference with block masking.

## Key Points

- Memento enables longer LLM outputs by blockwise summarization and KV cache compaction.
- Special tokens define reasoning blocks and summaries, allowing for selective eviction of context.
- The repository includes tools for data preparation and a modified vLLM server supporting block masking.

## Concepts Extracted

- **[[Memento Blockwise Summarization for LLMs]]** — Memento is a technique for extending the effective output length of large language models by dividing chain-of-thought reasoning into discrete blocks, each followed by a summary (memento). After each block, the model generates a concise summary, evicts the block's content from the KV cache, and continues reasoning from the summary, thus enabling more computation within a fixed context window.

## Entities Mentioned

- **[[Memento]]** — Memento is an open-source framework developed by Microsoft for extending the effective output length of large language models. It achieves this by segmenting chain-of-thought reasoning into blocks and generating summaries (mementos) after each block, which allows for selective eviction of context from the model's KV cache. The repository includes a data pipeline for formatting training data and a vLLM overlay for inference with block masking.
- **vLLM Overlay for Memento** — The vLLM overlay provided in the Memento repository is a customized extension of the vLLM inference engine, adding support for block masking and KV cache compaction. This overlay enables efficient inference with the Memento protocol, allowing the model to serve API-compatible endpoints while managing context via blockwise eviction.
- **[[OpenMementos Dataset]]** — The OpenMementos Dataset is a collection of chain-of-thought traces formatted in the Memento block+summary style, designed for supervised fine-tuning of LLMs to learn the Memento protocol. It is hosted on HuggingFace and referenced in the Memento repository.
- **[[Microsoft]]** — Microsoft is a global technology company and the creator of the Memento framework for extending LLM output length. The company is active in AI research and open-source software development.

## Notable Quotes

> "Memento extends the effective output length of large language models by splitting chain-of-thought reasoning into blocks and summaries (memento). After each reasoning block, the model generates a short summary, then the block content is evicted from the KV cache." — README

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-21-httpsgithubcommicrosoftmemento.md` |
| Type | repo |
| Author | Microsoft |
| Date | Unknown |
| URL | https://github.com/microsoft/memento |
