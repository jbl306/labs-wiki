---
title: "Selective Compression via Reinforcement Learning"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "e977787aa3bf4258d848bcffeb1d351a97dd2ac862ebcbcb87b914ba073277ad"
sources:
  - raw/2026-04-22-250901092v2pdf.md
quality_score: 69
concepts:
  - selective-compression-via-reinforcement-learning
related:
  - "[[REFRAG: Rethinking RAG Based Decoding]]"
tier: hot
tags: [reinforcement-learning, compression, RAG, LLM, attention]
---

# Selective Compression via Reinforcement Learning

## Overview

Selective compression in REFRAG uses a reinforcement learning (RL) policy to dynamically decide which context chunks should be expanded in full token form and which can be safely compressed into embeddings. This approach preserves answer quality while maximizing efficiency.

## How It Works

The RL policy is trained to optimize chunk expansion decisions based on next-paragraph prediction perplexity, which serves as a negative reward. During training, the policy network receives chunk embeddings and masking information, and sequentially selects chunks for expansion or compression. The encoder and decoder are fine-tuned to handle mixed inputs, maintaining the autoregressive property of the decoder.

Heuristic baselines include random selection and perplexity-based selection (compressing chunks with low perplexity or high perplexity), but RL-based selection consistently outperforms these. The RL policy learns to expand chunks that are most informative for answer prediction, as measured by perplexity, while compressing less relevant chunks.

Ablation studies show that RL-based selective compression maintains low perplexity across datasets (Arxiv, Book, PG19, ProofPile) even at high compression rates. The effective compression rate decreases as more chunks are expanded, but answer quality remains high due to targeted expansion.

This mechanism is crucial for balancing the trade-off between efficiency (speedup, memory reduction) and quality (accuracy, perplexity). It allows REFRAG to operate flexibly in agentic and multi-turn applications, where context relevance varies dynamically.

## Key Properties

- **RL Policy Optimization:** Uses next-paragraph prediction perplexity as reward to guide chunk expansion decisions.
- **Flexible Compression Placement:** Supports arbitrary chunk expansion, preserving decoder autoregression.
- **Empirical Performance:** RL-based selection achieves lowest perplexity among all selection strategies.

## Limitations

RL policy training adds complexity and requires careful reward shaping. If the policy fails to identify critical chunks, answer quality may suffer. The approach assumes chunk-level relevance can be captured by embeddings and perplexity, which may not always hold in highly entangled contexts.

## Example

In a summarization task, the RL policy expands chunks containing summary-relevant information (as indicated by high perplexity), compressing background chunks. This yields a concise, accurate summary with minimal latency.

## Visual

Figure 3 shows log-perplexity curves for RL, random, and perplexity-based selection across datasets and compression rates. RL consistently achieves lowest perplexity.

## Relationship to Other Concepts

- **Reinforcement Learning** — RL is used to optimize chunk expansion decisions in REFRAG.
- **Prompt Compression** — Selective compression extends prompt compression with RL-driven chunk selection.

## Practical Applications

Selective compression enables efficient, high-quality decoding in RAG, multi-turn conversations, and document summarization. It is especially beneficial in agentic workflows where context importance varies dynamically.

## Sources

- [[REFRAG: Rethinking RAG Based Decoding]] — primary source for this concept
