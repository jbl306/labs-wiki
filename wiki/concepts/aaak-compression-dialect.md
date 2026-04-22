---
title: "AAAK Compression Dialect"
type: concept
created: 2026-04-11
last_verified: 2026-04-11
source_hash: "101bef9011616b455e60e17998c3f1b308c5cab895c27a19c5a6f4d028ffcfb8"
sources:
  - raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md
quality_score: 76
concepts:
  - aaak-compression-dialect
related:
  - "[[Palace Memory Architecture]]"
  - "[[milla-jovovich/mempalace]]"
tier: hot
tags: [compression, tokenization, llm, context-management]
---

# AAAK Compression Dialect

## Overview

AAAK is an experimental, lossy abbreviation system designed to compress repeated entities and relationships in AI memory into fewer tokens. It is readable by any LLM without a decoder and aims to optimize context loading for large-scale, repeated data.

## How It Works

AAAK (pronounced 'triple-A-K') is a custom dialect for compressing memory content in MemPalace. Unlike traditional compression algorithms, AAAK uses regex-based abbreviation, entity codes, structural markers, and sentence truncation to reduce token count, especially in scenarios with many repeated entities (e.g., a team mentioned hundreds of times across sessions).

The system works by replacing full entity names with short codes, marking relationships with standardized separators, and truncating sentences to preserve only the most salient facts. For example, 'Kai debugged the OAuth token refresh' might be encoded as 'K:debug:OAuth-refresh'. This approach is lossy—meaning information is discarded for brevity—and not reversible, so AAAK is not suitable for archival storage but is useful for context injection where token limits are strict.

AAAK is not the default storage mode; MemPalace stores raw verbatim text in ChromaDB for maximum fidelity. AAAK is used as a compression layer for loading critical facts into an LLM's context window (e.g., during wake-up commands), enabling the injection of ~170 tokens of essential information versus millions of tokens for full transcripts.

Benchmark results show that AAAK mode regresses recall on LongMemEval (84.2% R@5 vs 96.6% for raw mode), indicating a trade-off between token density and retrieval fidelity. AAAK overhead (codes, separators) can exceed savings for small-scale data, so its benefits are realized only at scale with repeated entities.

The dialect is readable by any LLM (Claude, GPT, Gemini, Llama, Mistral), requiring no external decoder. Ongoing development includes integrating AAAK into closets for greater compression and refining the dialect spec with real tokenizer counts and better break points.

## Key Properties

- **Lossy Compression:** Uses abbreviation, entity codes, and sentence truncation to reduce token count, sacrificing some fidelity.
- **LLM-Readable:** Produces compressed text readable by any LLM without a decoder or special parsing.
- **Scalable Token Savings:** Effective at scale for repeated entities; overhead can outweigh savings for small data.
- **Context Injection:** Used for loading critical facts into LLM context windows, not for persistent storage.

## Limitations

AAAK is lossy and not reversible; it does not save tokens at small scales and regresses recall on benchmarks compared to raw mode. The dialect is experimental and subject to change. Not suitable for archival or legal record-keeping.

## Example

Injecting team and project facts into a local LLM's context: 'K:debug:OAuth-refresh; P:approve:Clerk; D:migrate:auth' instead of full sentences. This enables the model to recall key decisions within token limits.

## Visual

No specific diagram for AAAK, but README notes that AAAK-encoded closets will be added in future updates, increasing info density in the palace structure.

## Relationship to Other Concepts

- **[[Palace Memory Architecture]]** — AAAK is a compression layer for context loading within the palace structure.

## Practical Applications

Used to inject critical facts into LLM prompts for wake-up commands or context loading, enabling efficient recall without exceeding token limits. Useful for local models (Llama, Mistral) and offline workflows.

## Sources

- [[milla-jovovich/mempalace]] — primary source for this concept
