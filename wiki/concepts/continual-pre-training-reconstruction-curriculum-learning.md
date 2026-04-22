---
title: "Continual Pre-Training with Reconstruction and Curriculum Learning"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "e977787aa3bf4258d848bcffeb1d351a97dd2ac862ebcbcb87b914ba073277ad"
sources:
  - raw/2026-04-22-250901092v2pdf.md
quality_score: 53
concepts:
  - continual-pre-training-reconstruction-curriculum-learning
related:
  - "[[REFRAG: Rethinking RAG Based Decoding]]"
tier: hot
tags: [pre-training, curriculum-learning, compression, LLM, RAG]
---

# Continual Pre-Training with Reconstruction and Curriculum Learning

## Overview

REFRAG aligns its encoder and decoder using continual pre-training (CPT) augmented by a reconstruction task and curriculum learning. This ensures chunk embeddings are informative and compatible with the decoder, enabling effective compression and expansion.

## How It Works

CPT involves next-paragraph prediction tasks, where the encoder processes context tokens and the decoder predicts subsequent tokens. The reconstruction task freezes the decoder and trains the encoder and projection layer to reconstruct original tokens from chunk embeddings. This encourages the encoder to compress k tokens with minimal information loss and the projection layer to map embeddings into the decoder's token space.

Curriculum learning gradually increases task difficulty: training starts with single chunk reconstruction and progresses to multiple chunks, adjusting the data mixture over time. This approach addresses the exponential growth in token combinations as chunk size increases (V^k, where V is vocabulary size), and the challenge of reconstructing s=k×L tokens from L chunk embeddings.

Ablation studies confirm that CPT with reconstruction and curriculum learning is essential for achieving low perplexity and effective encoder-decoder alignment. Once aligned, supervised fine-tuning adapts the model to downstream tasks (RAG, multi-turn conversation).

## Key Properties

- **Encoder-Decoder Alignment:** Ensures chunk embeddings are compatible with decoder token space.
- **Reconstruction Task:** Trains encoder and projection layer to reconstruct original tokens from embeddings.
- **Curriculum Learning:** Gradually increases task difficulty, enabling robust skill acquisition.

## Limitations

CPT and curriculum learning require additional training resources and careful scheduling. Poor alignment may result in degraded compression quality. The approach is sensitive to chunk size and data mixture.

## Example

Training begins with the encoder reconstructing a single chunk of 16 tokens; as training progresses, the model reconstructs multiple chunks, adapting to increasingly complex compression scenarios.

## Visual

Figure 6 (not shown here) visualizes the data mixture evolution during curriculum learning; Table 8 details scheduling.

## Relationship to Other Concepts

- **Continual Pre-Training** — REFRAG uses CPT for encoder-decoder alignment.
- **Curriculum Learning** — Curriculum learning is applied to gradually increase task complexity.

## Practical Applications

CPT with reconstruction and curriculum learning is critical for deploying REFRAG in production RAG systems, ensuring chunk embeddings are informative and compatible with downstream decoders.

## Sources

- [[REFRAG: Rethinking RAG Based Decoding]] — primary source for this concept
