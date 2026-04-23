---
title: "KV Cache and Paged Attention in Large Language Models"
type: concept
created: 2026-04-13
last_verified: 2026-04-13
source_hash: "b40c474ba92950c304e974ce61881ccd715b0bf0d3118793b32a838d0ca55c36"
sources:
  - raw/2026-04-13-amitshekhariitbhullm-internals-learn-llm-internals-step-by-s.md
quality_score: 79
concepts:
  - kv-cache-and-paged-attention-in-large-language-models
related:
  - "[[Attention Mechanism in Large Language Models]]"
  - "[[amitshekhariitbhu/llm-internals]]"
  - "[[microsoft/memento]]"
tier: hot
tags: [kv-cache, paged-attention, llm, inference-optimization]
---

# KV Cache and Paged Attention in Large Language Models

## Overview

KV Cache and Paged Attention are inference optimization techniques used in LLMs to accelerate text generation and improve memory efficiency. KV Cache stores Key and Value matrices from previous steps, while Paged Attention manages memory allocation to serve multiple users efficiently.

## How It Works

During autoregressive text generation, LLMs generate one token at a time, requiring repeated computation of attention for each new token. The Key (K) and Value (V) matrices for previous tokens remain unchanged, but recomputing them for every step is wasteful. KV Cache addresses this by storing K and V matrices for all past tokens, allowing the model to reuse them and only compute Q for the new token. This significantly reduces computation, especially for long sequences.

The process is as follows:
1. **Initial Generation**: For the first token, compute Q, K, and V.
2. **Caching**: Store K and V for each token in a cache.
3. **Subsequent Steps**: For each new token, compute Q, retrieve K and V from the cache, and perform attention using the cached values.
4. **Speedup**: By avoiding recomputation, inference becomes much faster, with a trade-off in increased memory usage.

Paged Attention builds on KV Cache by addressing its memory inefficiency. Traditional KV Cache allocates fixed memory blocks per request, leading to wasted space when serving many users with varying sequence lengths. Paged Attention borrows from operating system memory management, dividing memory into pages and allocating them dynamically. This allows memory sharing across requests, reducing waste and enabling LLMs to serve more users simultaneously.

Paged Attention works by:
- Dividing cache memory into pages.
- Allocating pages as needed for each user's sequence.
- Sharing unused pages across requests.

This approach optimizes memory usage, making large-scale inference more practical. Both KV Cache and Paged Attention are crucial for deploying LLMs in real-world applications, where speed and scalability are paramount.

## Key Properties

- **Inference Speedup:** KV Cache reduces repeated computation, accelerating token generation.
- **Memory Efficiency:** Paged Attention minimizes memory waste, enabling efficient multi-user serving.
- **Trade-Offs:** KV Cache increases memory usage; Paged Attention balances speed and memory.

## Limitations

KV Cache consumes significant memory, especially for long sequences and many users. Paged Attention mitigates this but introduces complexity in memory management. Both techniques are limited by hardware constraints and may require careful tuning for optimal performance.

## Example

In a chatbot serving thousands of users, KV Cache stores K and V for each user's conversation. Paged Attention allocates memory pages dynamically, ensuring efficient resource usage and fast response times.

## Relationship to Other Concepts

- **[[Attention Mechanism in Large Language Models]]** — KV Cache and Paged Attention optimize the computation of attention during inference.

## Practical Applications

These techniques are used in production LLMs for real-time text generation, chatbots, and large-scale inference systems, improving latency and scalability.

## Sources

- [[amitshekhariitbhu/llm-internals]] — primary source for this concept
- [[microsoft/memento]] — KV cache compaction via block masking
