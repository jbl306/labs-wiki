---
title: "Memento Blockwise Summarization for LLMs"
type: concept
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "7b344980e889d401d340d2539bd18583a585c26640fe19f36c596d887e647ba2"
sources:
  - raw/2026-04-13-260406231v1pdf.md
  - raw/2026-04-21-httpsgithubcommicrosoftmemento.md
quality_score: 84
concepts:
  - memento-blockwise-summarization-for-llms
related:
  - "[[KV Cache and Paged Attention in Large Language Models]]"
  - "[[microsoft/memento]]"
tier: hot
tags: [llm, memory, summarization, context-window, kv-cache, chain-of-thought]
---

# Memento Blockwise Summarization for LLMs

## Overview

Memento is a technique for extending the effective output length of large language models by dividing chain-of-thought reasoning into discrete blocks, each followed by a summary (memento). After each block, the model generates a concise summary, evicts the block's content from the KV cache, and continues reasoning from the summary, thus enabling more computation within a fixed context window.

## How It Works

The Memento approach addresses the inherent limitation of transformer-based LLMs: their fixed context window, which restricts the amount of information the model can attend to during generation. In long-form reasoning tasks, especially those requiring multi-step chain-of-thought (CoT) processing, this limitation can truncate relevant context, leading to degraded performance or incomplete answers.

Memento introduces a structured protocol for managing context by splitting the reasoning process into blocks. Each block is a contiguous segment of reasoning, demarcated by special tokens (`<|block_start|>` and `<|block_end|>`). After completing a block, the model generates a summary, also bounded by special tokens (`<|summary_start|>` and `<|summary_end|>`). This summary acts as a 'memento'—a compressed representation of the block's essential information.

Once the summary is generated, the content of the preceding block is evicted from the model's KV (key-value) cache. The KV cache is the internal memory structure transformers use to store intermediate activations for attention computation. By evicting the block, the model reduces the cache's memory footprint, freeing up space for subsequent reasoning steps. The model then continues generation from the summary, which is now part of the active context, allowing it to reason further without exceeding the context window.

This process can be repeated multiple times, effectively enabling the model to 'think longer' by retaining only the distilled essence of previous reasoning, rather than the full token sequence. The trade-off is that the model must learn to produce high-fidelity summaries that preserve all information necessary for continued reasoning. This is supported by supervised fine-tuning (SFT) on traces formatted in the Memento style.

The Memento protocol is implemented via a data pipeline that converts raw CoT traces into the block+summary format for training. At inference time, a customized vLLM server with block masking support manages the KV cache, ensuring that only the summary and relevant context remain after each block. This is configured via a block masking configuration, which controls how many blocks to keep, when to compact the cache, and other operational parameters.

The intuition behind Memento is similar to human note-taking: after completing a segment of work, one writes a summary and then refers only to the summary for subsequent steps, reducing cognitive load. This enables more complex or lengthy tasks to be handled within bounded memory resources.

## Key Properties

- **Context Window Efficiency:** By evicting block content after summarization, Memento allows more reasoning steps within a fixed context window, effectively increasing the model's usable output length.
- **Special Token Protocol:** Uses explicit tokens to mark the start/end of reasoning blocks and summaries, enabling precise segmentation and cache management.
- **KV Cache Compaction:** Actively removes block content from the transformer KV cache after summarization, reducing memory usage and preventing context overflow.
- **Supervised Fine-Tuning Support:** Provides a data pipeline to convert chain-of-thought traces into the Memento format for SFT, teaching the model to summarize and continue reasoning effectively.
- **vLLM Overlay Integration:** Implements block masking and cache compaction in a modified vLLM server, enabling efficient inference with the Memento protocol.

## Limitations

The effectiveness of Memento depends on the model's ability to generate high-quality summaries that preserve all necessary information for continued reasoning. If important details are omitted or misrepresented in the summary, downstream reasoning may fail or produce incorrect results. There is also a risk that repeated summarization may accumulate errors or lose nuance. The approach requires explicit formatting and fine-tuning, and may not generalize to all tasks or models without adaptation.

## Example

Suppose an LLM is tasked with solving a multi-step math problem. The model generates a reasoning block:

```text
<|block_start|> Let's analyze the problem: ... <|block_end|>
<|summary_start|> The problem reduces to finding X given Y. <|summary_end|>
```

After generating the summary, the block is evicted from the KV cache, and the model continues reasoning from the summary, allowing it to handle more steps without exceeding the context limit.

## Visual

In the Memento blogpost animation (from the repository's blogpost/figures), a side-by-side visualization shows the generation process: on the left, reasoning blocks and summaries are displayed, with masked segments faded out after eviction; on the right, a chart tracks the KV cache usage over time, comparing Memento's compacted cache to vanilla (unmasked) cache growth.

## Relationship to Other Concepts

- **[[KV Cache and Paged Attention in Large Language Models]]** — Memento builds on the idea of KV cache management, introducing blockwise eviction and compaction.
- **Chain-of-Thought Reasoning** — Memento explicitly segments and summarizes CoT traces to extend reasoning length.

## Practical Applications

Memento is particularly useful in scenarios requiring long-form reasoning, such as mathematical proofs, code generation, scientific analysis, and multi-step planning, where the context window of standard LLMs would otherwise be exceeded. It enables deployment of LLMs for tasks that demand extended memory without resorting to much larger models or external memory systems.

## Sources

- [[microsoft/memento]] — primary source for this concept
- [[Hope: A Memory Architecture for Continual Learning with Long Contexts]] — additional source
