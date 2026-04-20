---
title: "Agent Memory Retrieval Pipeline"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "6d3926b294fd189631a5b0192148c2460f4f4d037b2814c551620137e4a5fae8"
sources:
  - raw/2026-04-20-agents-that-remember-introducing-agent-memory.md
quality_score: 100
concepts:
  - agent-memory-retrieval-pipeline
related:
  - "[[Hybrid Retrieval in Agent Memory Systems]]"
  - "[[MemPalace Memory System]]"
  - "[[Agents that remember: introducing Agent Memory]]"
tier: hot
tags: [retrieval-pipeline, hybrid-retrieval, reciprocal-rank-fusion, agent-memory]
---

# Agent Memory Retrieval Pipeline

## Overview

The retrieval pipeline in Agent Memory enables agents to recall relevant memories efficiently by fusing results from multiple retrieval channels. It combines query analysis, embedding, and reciprocal rank fusion to synthesize natural-language answers to agent queries.

## How It Works

When an agent issues a recall query, the pipeline begins with concurrent query analysis and embedding. The query analyzer generates ranked topic keys, full-text search terms (with synonyms), and a HyDE (Hypothetical Document Embedding) — a declarative statement phrased as if it were the answer. Both the raw query and HyDE are embedded for downstream retrieval.

Five retrieval channels run in parallel:
1. Full-text search with Porter stemming for keyword precision.
2. Exact fact-key lookup for direct topic matches.
3. Raw message search for verbatim details missed by extraction.
4. Direct vector search for semantic similarity.
5. HyDE vector search for answer-like similarity, useful for abstract or multi-hop queries.

Results from all channels are merged using Reciprocal Rank Fusion (RRF), where each result is weighted by its rank within the channel. Fact-key matches receive the highest weight, followed by full-text, HyDE, direct vector, and raw message matches. Recency breaks ties, favoring newer results.

The top candidates are passed to the synthesis model (Nemotron 3), which generates a natural-language answer. Temporal queries are handled deterministically via regex and arithmetic, with results injected into the synthesis prompt, avoiding unreliable LLM date math.

## Key Properties

- **Multi-Channel Retrieval:** Parallel channels (full-text, fact-key, raw message, direct vector, HyDE vector) ensure robust recall.
- **Reciprocal Rank Fusion:** Weighted merging of results from all channels, prioritizing strongest signals and recency.
- **HyDE Embedding:** Hypothetical Document Embedding bridges question-answer vocabulary gaps for abstract queries.
- **Deterministic Temporal Computation:** Regex and arithmetic handle date math reliably, avoiding LLM errors.
- **Natural-Language Synthesis:** Top results are synthesized into answers by a large model (Nemotron 3).

## Limitations

Retrieval quality depends on the accuracy of topic keys, embeddings, and channel weighting. HyDE may miss nuanced answers if hypothetical phrasing diverges from stored memory. RRF weighting can bias toward certain channels, potentially missing relevant results. Synthesis depends on model quality and may introduce stochasticity.

## Example

Agent issues recall: 'What package manager does the user prefer?'
- Query analyzer ranks 'package manager' topic, generates full-text terms and HyDE embedding.
- Retrieval channels find 'pnpm' in fact-key, full-text, and vector search.
- RRF merges results, prioritizing fact-key match.
- Synthesis model returns: 'The user prefers pnpm over npm.'

## Visual

No explicit diagram for retrieval pipeline, but the stylized robot in a modular box (third image) suggests the multi-channel, compartmentalized retrieval process.

## Relationship to Other Concepts

- **[[Hybrid Retrieval in Agent Memory Systems]]** — Agent Memory's retrieval pipeline is a practical implementation of hybrid retrieval.
- **[[MemPalace Memory System]]** — Both systems use retrieval pipelines for agent recall.

## Practical Applications

Used for agent recall during task execution, code review feedback retrieval, chat bot question answering, and durable knowledge access across teams and sessions.

## Sources

- [[Agents that remember: introducing Agent Memory]] — primary source for this concept
