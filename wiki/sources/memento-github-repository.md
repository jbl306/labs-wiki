---
title: "Memento GitHub Repository"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "e7275fa833e5a7d37c42ebe57ee2b1da6ef9871243ade9a1891b01c5cd7da154"
sources:
  - raw/2026-04-21-httpsgithubcommicrosoftmemento.md
quality_score: 63
concepts:
  - memento-blockwise-summarization-for-llms
related:
  - "[[Memento Blockwise Summarization for LLMs]]"
  - "[[Memento]]"
  - "[[OpenMementos Dataset]]"
  - "[[Microsoft]]"
tier: hot
knowledge_state: executed
tags: [summarization, llm, memory, kv-cache, block-masking, context-management]
---

# Memento GitHub Repository

## Summary

The Memento repository by Microsoft introduces a method for extending the effective output length of large language models by splitting chain-of-thought reasoning into blocks and summaries, enabling more reasoning within a fixed context window. It provides a data pipeline for converting raw chain-of-thought traces into the Memento format and a vLLM overlay for efficient inference using KV cache block masking. The repository includes documentation, example scripts, and a connection to the OpenMementos dataset for supervised fine-tuning.

## Key Points

- Memento splits chain-of-thought reasoning into blocks and generates summaries after each block.
- After each summary, block content is evicted from the KV cache, allowing the model to continue with a shorter context.
- The repository includes a data pipeline for formatting training data and a vLLM overlay for efficient inference with block masking.

## Concepts Extracted

- **[[Memento Blockwise Summarization for LLMs]]** — Memento blockwise summarization is a technique designed to extend the effective output length of large language models (LLMs) by segmenting chain-of-thought reasoning into discrete blocks, each followed by a summary. This approach allows the model to operate within a fixed context window by evicting earlier block content from the KV cache after summarization, enabling continued reasoning without exceeding context limitations.

## Entities Mentioned

- **[[Memento]]** — Memento is a method and software package developed by Microsoft for extending the output length of large language models by segmenting chain-of-thought reasoning into blocks and summaries. It includes a data pipeline for formatting training data and a vLLM overlay for efficient inference using block masking and KV cache compaction.
- **[[OpenMementos Dataset]]** — The OpenMementos Dataset is a collection of chain-of-thought traces formatted for Memento blockwise summarization, designed for supervised fine-tuning of large language models. It is hosted on Hugging Face and referenced in the Memento repository.
- **[[Microsoft]]** — Microsoft is a global technology company and the creator of the Memento repository and OpenMementos dataset. It is responsible for developing tools and research in large language models and context management.

## Notable Quotes

> "Memento extends the effective output length of large language models by splitting chain-of-thought reasoning into blocks and summaries (memento). After each reasoning block, the model generates a short summary, then the block content is evicted from the KV cache." — README

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-21-httpsgithubcommicrosoftmemento.md` |
| Type | repo |
| Author | Unknown |
| Date | Unknown |
| URL | https://github.com/microsoft/memento |
