---
title: "REFRAG"
type: entity
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "e977787aa3bf4258d848bcffeb1d351a97dd2ac862ebcbcb87b914ba073277ad"
sources:
  - raw/2026-04-22-250901092v2pdf.md
quality_score: 66
concepts:
  - refrag
related:
  - "[[REFRAG Decoding Framework]]"
  - "[[Selective Compression via Reinforcement Learning]]"
  - "[[Continual Pre-Training with Reconstruction and Curriculum Learning]]"
  - "[[REFRAG: Rethinking RAG Based Decoding]]"
tier: hot
tags: [RAG, LLM, compression, latency, memory, reinforcement-learning]
---

# REFRAG

## Overview

REFRAG is a decoding framework for retrieval-augmented generation in large language models, designed to compress context into chunk embeddings and selectively expand relevant chunks for efficient inference. It achieves substantial speedup in latency and throughput, validated across multiple datasets and tasks.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Framework |
| Created | 2025 |
| Creator | Xiaoqiang Lin, Aritra Ghosh, Bryan Kian Hsiang Low, Anshumali Shrivastava, Vijai Mohan |
| URL | https://github.com/facebookresearch/refrag |
| Status | Active |

## Relevance

REFRAG addresses the fundamental trade-off in RAG systems between knowledge enrichment and system efficiency, enabling practical deployment of long-context LLMs in high-throughput, low-latency applications. Its selective compression and RL-driven expansion mechanisms outperform previous state-of-the-art methods.

## Associated Concepts

- **[[REFRAG Decoding Framework]]** — Core mechanism for efficient RAG decoding.
- **[[Selective Compression via Reinforcement Learning]]** — Optimizes chunk expansion for answer quality.
- **[[Continual Pre-Training with Reconstruction and Curriculum Learning]]** — Ensures encoder-decoder alignment for chunk embeddings.

## Related Entities

- **CEPE** — Previous SOTA baseline for memory-efficient long-context decoding.
- **LLaMA** — Decoder-only foundation model used in REFRAG experiments.
- **Roberta** — Lightweight encoder model used for chunk embedding.

## Sources

- [[REFRAG: Rethinking RAG Based Decoding]] — where this entity was mentioned
