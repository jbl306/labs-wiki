---
title: "REFRAG: Rethinking RAG Based Decoding"
type: source
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "e977787aa3bf4258d848bcffeb1d351a97dd2ac862ebcbcb87b914ba073277ad"
sources:
  - raw/2026-04-22-250901092v2pdf.md
quality_score: 82
concepts:
  - refrag-decoding-framework
  - selective-compression-via-reinforcement-learning
  - continual-pre-training-reconstruction-curriculum-learning
related:
  - "[[REFRAG Decoding Framework]]"
  - "[[Selective Compression via Reinforcement Learning]]"
  - "[[Continual Pre-Training with Reconstruction and Curriculum Learning]]"
  - "[[REFRAG]]"
tier: hot
tags: [latency, compression, RAG, memory, LLM, reinforcement-learning, attention]
---

# REFRAG: Rethinking RAG Based Decoding

## Summary

REFRAG introduces a novel decoding framework for retrieval-augmented generation (RAG) in large language models, leveraging chunk-level compression and selective expansion to drastically reduce latency and memory usage. By exploiting the block-diagonal sparsity in RAG attention patterns, REFRAG achieves significant acceleration in inference, especially time-to-first-token (TTFT), without sacrificing accuracy or perplexity. The approach is validated across multiple long-context tasks and datasets, outperforming previous state-of-the-art methods.

## Key Points

- REFRAG compresses retrieved context into chunk embeddings, reducing input length and attention computation.
- Selective expansion via RL policy preserves critical context chunks, balancing efficiency and answer quality.
- Empirical results show up to 30x TTFT acceleration and extended context windows with no loss in perplexity.

## Concepts Extracted

- **[[REFRAG Decoding Framework]]** — REFRAG is a decoding framework for retrieval-augmented generation (RAG) in large language models, designed to minimize inference latency and memory usage by compressing context into chunk embeddings and selectively expanding relevant chunks. It exploits the block-diagonal sparsity in attention patterns typical of RAG contexts, enabling substantial speedups without loss of accuracy.
- **[[Selective Compression via Reinforcement Learning]]** — Selective compression in REFRAG uses a reinforcement learning (RL) policy to dynamically decide which context chunks should be expanded in full token form and which can be safely compressed into embeddings. This approach preserves answer quality while maximizing efficiency.
- **[[Continual Pre-Training with Reconstruction and Curriculum Learning]]** — REFRAG aligns its encoder and decoder using continual pre-training (CPT) augmented by a reconstruction task and curriculum learning. This ensures chunk embeddings are informative and compatible with the decoder, enabling effective compression and expansion.

## Entities Mentioned

- **[[REFRAG]]** — REFRAG is a decoding framework for retrieval-augmented generation in large language models, designed to compress context into chunk embeddings and selectively expand relevant chunks for efficient inference. It achieves substantial speedup in latency and throughput, validated across multiple datasets and tasks.

## Notable Quotes

> "By exploiting this attention sparsity structure, we demonstrate a 30.85× time-to-first-token acceleration (3.75× improvement to previous work) without loss in perplexity." — Abstract
> "REFRAG significantly reduces latency, TTFT, and memory usage during decoding, all without requiring modifications to the LLM architecture or introducing new decoder parameters." — Section 1.1 Our Contributions

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-22-250901092v2pdf.md` |
| Type | paper |
| Author | Xiaoqiang Lin, Aritra Ghosh, Bryan Kian Hsiang Low, Anshumali Shrivastava, Vijai Mohan |
| Date | October 12, 2025 |
| URL | https://arxiv.org/pdf/2509.01092 |
