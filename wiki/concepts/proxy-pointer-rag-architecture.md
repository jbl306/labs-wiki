---
title: "Proxy-Pointer RAG Architecture"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "b72ef6058f17587232e6e8667c2c3535ffda06dfd613d577b6084da33cfb1c29"
sources:
  - raw/2026-04-20-proxy-pointer-rag-structure-meets-scale-at-100-accuracy-with.md
quality_score: 75
concepts:
  - proxy-pointer-rag-architecture
related:
  - "[[Hybrid Retrieval in Agent Memory Systems]]"
  - "[[Hallucinations in Legal Retrieval-Augmented Generation (RAG) Systems]]"
  - "[[Proxy-Pointer RAG: Structure Meets Scale at 100% Accuracy with Smarter Retrieval]]"
tier: hot
tags: [RAG, document retrieval, structured data, vector search, LLM, auditability, open source]
---

# Proxy-Pointer RAG Architecture

## Overview

Proxy-Pointer RAG is a retrieval-augmented generation architecture that embeds document structure directly into vector indices, enabling highly accurate and scalable retrieval for structured documents. It overcomes the limitations of standard vector RAG and expensive 'Vectorless RAG' approaches by using lightweight structural cues and a two-stage retrieval pipeline.

## How It Works

Proxy-Pointer RAG fundamentally changes how retrieval-augmented generation systems handle structured documents. Instead of splitting documents into contextless chunks, it parses Markdown headings into a hierarchical skeleton tree using pure Python (no LLM calls, no dependencies), creating a lightweight JSON representation of the document's structure. Each chunk is then prepended with its full structural breadcrumb path (e.g., 'AMD > Financial Statements > Cash Flows'), ensuring that the embedding model encodes not just the content but also its location within the document.

The indexing pipeline consists of several zero-cost engineering techniques:
- **Skeleton Tree Generation:** Parses headings to build a hierarchical tree, allowing boundary propagation and parent-child capping.
- **Breadcrumb Injection:** Prepends the structural path to each chunk before embedding, so every chunk knows its context.
- **Structure-Guided Chunking:** Splits text within section boundaries, never across them, preserving semantic integrity.
- **Noise Filtering:** Uses an LLM (gemini-flash-lite) to identify and exclude semantically equivalent noise sections (e.g., TOC, glossary, acknowledgments) across six categories, outperforming regex-based approaches.
- **Pointer-Based Context:** When retrieving, chunks act as pointers to load the full, unbroken section for the synthesizer LLM.

The retrieval pipeline operates in two stages:
1. **Semantic Recall:** FAISS returns the top 200 chunks by embedding similarity, deduplicated to 50 unique candidate nodes.
2. **Structural Re-Ranking:** The hierarchical breadcrumb paths of these candidates are sent to a Gemini LLM, which re-ranks them by structural relevance (not just embedding similarity) and returns the top 5. This ensures that queries about specific sections (e.g., 'cash flow') prioritize the correct structural context.

At query time, the synthesizer LLM receives complete sections (not fragments), along with structural breadcrumbs, enabling precise, grounded answers. The architecture is open-source, runs on commodity hardware (no GPU required), and is compatible with budget-friendly models like gemini-flash-lite and gemini-embedding-001 (1536 dims for vector storage efficiency).

Benchmarking on four Fortune 500 10-K filings (AMD, AMEX, Boeing, PepsiCo) with 66 questions across two benchmarks (FinanceBench and a custom comprehensive stress test) demonstrated 100% accuracy at k=5 and 93.9% at k=3. Failures at k=3 were due to insufficient context coverage for complex, cross-statement queries, not retrieval errors.

The architecture is transparent and auditable: every answer includes structural traces, breadcrumbs, and exact line ranges, enabling analysts to verify responses directly against source documents. Proxy-Pointer unifies vector and structure-aware retrieval, eliminating the need for separate pipelines and expensive LLM tree navigation.

## Key Properties

- **Structural Embedding:** Chunks are embedded with their full structural breadcrumb path, allowing the embedding model to encode both content and location.
- **Zero-Cost Skeleton Tree:** Pure Python tree builder parses headings into a hierarchical structure in milliseconds, with no external dependencies or LLM calls.
- **LLM-Powered Noise Filtering:** Gemini-flash-lite identifies semantically equivalent noise nodes across six categories, outperforming regex-based filters.
- **Two-Stage Retrieval:** Semantic recall via FAISS (top 200 chunks), followed by structural LLM re-ranking (top 50 → top 5 nodes).
- **Transparent Audit Trail:** Every answer includes structural breadcrumbs and line ranges, enabling direct verification against source documents.
- **Benchmark Accuracy:** 100% accuracy on 66 questions at k=5; 93.9% at k=3; failures at k=3 due to context window limitations, not retrieval errors.

## Limitations

Proxy-Pointer's accuracy depends on the presence of structural headings in documents. For unstructured documents, it degrades gracefully to standard chunking but loses structural advantages. At lower k (e.g., k=3), complex queries requiring cross-referencing multiple sections may suffer from insufficient context coverage. Arithmetic errors in synthesis are possible if the LLM is too small or context is constrained.

## Example

For the query 'Calculate the reinvestment rate defined as Capex divided by (Operating Cash Flow minus Dividends)' in PepsiCo's 10-K, Proxy-Pointer retrieves the relevant cash flow statement sections, computes the ratio (5,207 / (10,811 − 6,172) = 1.1224), and returns a grounded answer with structural breadcrumbs.

## Visual

The article includes two pipeline diagrams: one for indexing (showing skeleton tree, noise filter, chunking, embedding, FAISS index) and one for retrieval (showing query embedding, FAISS search, structural dedup, LLM re-ranker, section loading, synthesis). There are also two illustrative images: one depicting a digital cube structure with embedded data flowing to a neural processor, and another showing fragmented documents transforming into a structured tree, symbolizing structured retrieval.

## Relationship to Other Concepts

- **[[Hybrid Retrieval in Agent Memory Systems]]** — Proxy-Pointer extends hybrid retrieval by combining semantic and structural cues for improved accuracy.
- **[[Hallucinations in Legal Retrieval-Augmented Generation (RAG) Systems]]** — Proxy-Pointer mitigates hallucinations by grounding answers in structural context and breadcrumbs.

## Practical Applications

Proxy-Pointer RAG is ideal for enterprise retrieval tasks involving structured documents: financial filings, legal contracts, technical manuals, policy reports, and compliance documents. It enables precise, auditable answers in high-stakes contexts (e.g., financial analysis, regulatory compliance) and is deployable on commodity hardware with open-source tooling.

## Sources

- [[Proxy-Pointer RAG: Structure Meets Scale at 100% Accuracy with Smarter Retrieval]] — primary source for this concept
