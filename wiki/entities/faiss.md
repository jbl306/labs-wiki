---
title: "FAISS"
type: entity
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "b72ef6058f17587232e6e8667c2c3535ffda06dfd613d577b6084da33cfb1c29"
sources:
  - raw/2026-04-20-proxy-pointer-rag-structure-meets-scale-at-100-accuracy-with.md
quality_score: 100
concepts:
  - faiss
related:
  - "[[Two-Stage Retrieval with Structural LLM Re-Ranking]]"
  - "[[Proxy-Pointer RAG: Structure Meets Scale at 100% Accuracy with Smarter Retrieval]]"
  - "[[Proxy-Pointer]]"
  - "[[Gemini-flash-lite]]"
  - "[[LlamaParse]]"
tier: hot
tags: [vector search, semantic retrieval, tool, scalability]
---

# FAISS

## Overview

FAISS is a vector search library used for semantic recall in the Proxy-Pointer pipeline. It retrieves the top 200 chunks by embedding similarity, providing broad coverage for subsequent structural re-ranking.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

FAISS enables efficient, scalable semantic search in Proxy-Pointer, forming the first stage of the two-stage retrieval pipeline.

## Associated Concepts

- **[[Two-Stage Retrieval with Structural LLM Re-Ranking]]** — FAISS provides semantic recall for structural re-ranking.

## Related Entities

- **[[Proxy-Pointer]]** — FAISS is used for semantic recall in Proxy-Pointer.
- **[[Gemini-flash-lite]]** — co-mentioned in source (Model)
- **[[LlamaParse]]** — co-mentioned in source (Tool)

## Sources

- [[Proxy-Pointer RAG: Structure Meets Scale at 100% Accuracy with Smarter Retrieval]] — where this entity was mentioned
