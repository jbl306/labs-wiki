---
title: "REFRAG Decoding Framework"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "e977787aa3bf4258d848bcffeb1d351a97dd2ac862ebcbcb87b914ba073277ad"
sources:
  - raw/2026-04-22-250901092v2pdf.md
quality_score: 100
concepts:
  - refrag-decoding-framework
related:
  - "[[REFRAG: Rethinking RAG Based Decoding]]"
tier: hot
tags: [RAG, LLM, compression, latency, memory, reinforcement-learning, attention]
---

# REFRAG Decoding Framework

## Overview

REFRAG is a decoding framework for retrieval-augmented generation (RAG) in large language models, designed to minimize inference latency and memory usage by compressing context into chunk embeddings and selectively expanding relevant chunks. It exploits the block-diagonal sparsity in attention patterns typical of RAG contexts, enabling substantial speedups without loss of accuracy.

## How It Works

REFRAG operates by chunking the context input (typically retrieved passages in RAG) and processing each chunk with a lightweight encoder to produce chunk embeddings. These embeddings are then projected to match the decoder's token embedding space and fed directly into the decoder, alongside token embeddings for the query/question. This reduces the input length to the decoder by a factor of k (the chunk size), and attention computation now scales quadratically with the number of chunks, rather than the number of tokens.

A key innovation is the 'compress anywhere' capability: REFRAG allows arbitrary chunks to be compressed, preserving the autoregressive nature of the decoder. To optimize which chunks are compressed versus expanded, a lightweight reinforcement learning (RL) policy is trained, using next-paragraph prediction perplexity as a negative reward. This policy decides, for each chunk, whether to feed the full token sequence or the compressed embedding, thus balancing efficiency and answer quality.

The encoder and decoder are aligned through continual pre-training (CPT) using next-paragraph prediction tasks, followed by supervised fine-tuning for downstream applications. A reconstruction task is used during CPT, where the encoder learns to compress k tokens with minimal information loss, and the projection layer maps these embeddings into the decoder's token space. Curriculum learning is employed to gradually increase task difficulty, starting with single chunk reconstruction and progressing to multiple chunks.

Empirical and theoretical analyses show that REFRAG achieves up to k× acceleration in TTFT and throughput for short contexts, and up to k²× for longer contexts. With k=16, REFRAG achieves 16.53× TTFT acceleration with cache and 8.59× without cache, outperforming previous methods like CEPE. At k=32, TTFT acceleration reaches 32.99× compared to LLaMA, with comparable perplexity.

Selective compression is further refined by the RL policy, which expands important chunks based on perplexity heuristics. Ablation studies demonstrate that RL-based selection consistently outperforms random or perplexity-based heuristics, maintaining low perplexity even at high compression rates.

## Key Properties

- **Compression Rate:** Chunk size k determines the compression rate; higher k yields greater speedup but increases information loss risk.
- **Attention Sparsity Exploitation:** Block-diagonal attention patterns in RAG contexts allow quadratic reduction in attention computation.
- **Time-to-First-Token (TTFT) Acceleration:** Achieves up to 30x TTFT speedup compared to standard LLM decoding, with empirical validation.
- **Memory Usage Reduction:** Significantly lowers KV cache requirements by reducing input sequence length.
- **Selective Chunk Expansion:** RL policy expands only critical chunks, balancing efficiency and answer quality.

## Limitations

REFRAG relies on the quality of chunk embeddings and the RL policy for selective expansion; poor alignment between encoder and decoder may degrade performance. High compression rates risk losing critical information if the RL policy fails to identify important chunks. The approach assumes block-diagonal attention sparsity, which may not hold in all RAG scenarios. Requires additional pre-training and fine-tuning steps for encoder-decoder alignment.

## Example

Suppose a RAG system retrieves 2048 tokens of context for a query. REFRAG chunks this into 128 chunks of 16 tokens each. Each chunk is encoded into a single embedding, projected, and fed to the decoder. The RL policy decides to expand 10% of chunks (those most relevant to the query) in full token form, while compressing the rest. This reduces the decoder input from 2048 tokens to ~138 embeddings, yielding a 16x speedup in TTFT and throughput, with negligible loss in answer quality.

## Visual

Figure 1 shows the REFRAG architecture: context is chunked, encoded, and projected; chunk embeddings and query token embeddings are fed to a decoder-only foundation model. RL policy selectively expands chunks. Figure 2 presents TTFT, TTIT, and throughput acceleration curves versus input tokens, demonstrating REFRAG's speedup over CEPE and LLaMA. Figure 3 compares log-perplexity across compression rates and selection policies, showing RL-based selection outperforms others.

## Relationship to Other Concepts

- **Retrieval-Augmented Generation (RAG)** — REFRAG is specifically designed to optimize RAG decoding.
- **Compressive Transformer** — Both exploit attention sparsity and compression for efficiency.
- **Prompt Compression** — REFRAG extends prompt compression with chunk-level embeddings and selective expansion.

## Practical Applications

REFRAG is suited for web-scale search, document summarization, multi-turn conversational agents, and any LLM application requiring efficient handling of long contexts. It is particularly valuable in production RAG systems where latency and throughput are critical, such as real-time QA, chatbots, and agentic workflows. Its ability to extend context windows enables richer knowledge integration without performance penalties.

## Sources

- [[REFRAG: Rethinking RAG Based Decoding]] — primary source for this concept
