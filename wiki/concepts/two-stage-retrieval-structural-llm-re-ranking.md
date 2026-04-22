---
title: "Two-Stage Retrieval with Structural LLM Re-Ranking"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "b72ef6058f17587232e6e8667c2c3535ffda06dfd613d577b6084da33cfb1c29"
sources:
  - raw/2026-04-20-proxy-pointer-rag-structure-meets-scale-at-100-accuracy-with.md
quality_score: 56
concepts:
  - two-stage-retrieval-structural-llm-re-ranking
related:
  - "[[Hybrid Retrieval in Agent Memory Systems]]"
  - "[[Proxy-Pointer RAG: Structure Meets Scale at 100% Accuracy with Smarter Retrieval]]"
tier: hot
tags: [retrieval, LLM, semantic search, structural ranking, multi-hop reasoning]
---

# Two-Stage Retrieval with Structural LLM Re-Ranking

## Overview

Proxy-Pointer RAG employs a two-stage retrieval pipeline: semantic recall via vector search, followed by structural LLM re-ranking. This ensures that retrieved sections are not only semantically relevant but also structurally appropriate for the query.

## How It Works

The retrieval pipeline begins with semantic recall: FAISS returns the top 200 chunks by embedding similarity. These chunks are deduplicated by (doc_id, node_id) to yield 50 unique candidate nodes. This broad recall ensures that all potentially relevant sections are considered.

The second stage is structural re-ranking. The hierarchical breadcrumb paths of these candidates are sent to a Gemini LLM, which ranks them by structural relevance to the query. For example, a query about 'AMD's cash flow' will prioritize 'AMD > Financial Statements > Cash Flows' over paragraphs that merely mention cash flow. The LLM returns the top 5 nodes, which are then used to load the full, unbroken sections for the synthesizer.

This approach outperforms embedding-only retrieval, especially for complex queries requiring multi-hop reasoning or cross-statement reconciliation. It also provides robustness against adversarial queries and ensures that answers are grounded in the correct structural context.

Benchmarking demonstrated that k=5 (retrieving 5 sections) provides full coverage for complex queries, while k=3 is adequate for most single-section queries but may miss secondary context for reconciliation tasks.

## Key Properties

- **Semantic Recall:** FAISS retrieves top 200 chunks by embedding similarity, ensuring broad coverage.
- **Structural Re-Ranking:** LLM ranks candidates by hierarchical breadcrumb relevance, returning top 5 nodes.
- **Context Coverage:** k=5 ensures coverage for multi-hop and reconciliation queries; k=3 is faster but may miss secondary context.

## Limitations

Structural re-ranking depends on the quality of breadcrumb paths and LLM ranking. At lower k, complex queries may suffer from insufficient coverage. Requires documents to have structural headings for optimal performance.

## Example

For the query 'Did provisions for credit losses increase faster than total revenue?' in AMEX's 10-K, the pipeline retrieves both provisions and revenue sections, enabling accurate comparison.

## Visual

Retrieval pipeline diagram shows semantic recall, structural deduplication, LLM re-ranking, section loading, and synthesis stages.

## Relationship to Other Concepts

- **[[Hybrid Retrieval in Agent Memory Systems]]** — Both use multi-stage retrieval to combine semantic and structural cues.

## Practical Applications

Used in financial analysis, legal review, technical documentation search, and any domain requiring precise, multi-section retrieval. Enables robust, explainable answers in enterprise settings.

## Sources

- [[Proxy-Pointer RAG: Structure Meets Scale at 100% Accuracy with Smarter Retrieval]] — primary source for this concept
