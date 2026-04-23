---
title: "Hybrid v4 Retrieval"
type: concept
created: '2026-04-22'
last_verified: '2026-04-22'
sources:
  - raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md
quality_score: 64
concepts:
  - hybrid-v4-retrieval
related:
  - "[[milla-jovovich/mempalace]]"
  - "[[hybrid-retrieval-agent-memory-systems]]"
tier: warm
tags: [retrieval, search, ranking, benchmarking]
---

# Hybrid v4 Retrieval

## Overview

Hybrid v4 is MemPalace's multi-signal retrieval pipeline that layers keyword boosting, temporal-proximity boosting, and preference-pattern extraction on top of raw semantic search. It achieves 98.4% R@5 on a held-out 450-question LongMemEval split without an LLM in the retrieval path.

## How It Works

Hybrid v4 is an opt-in enhancement over raw semantic search (which already scores 96.6% R@5 on the full 500-question LongMemEval set). The pipeline has three stages:

1. **Semantic baseline**: Query embeddings are computed with a local sentence-transformer model (~300 MB, no API key). ChromaDB retrieves the top-N candidates (typically N=20-50) by cosine similarity against drawer embeddings. This is the same as raw mode.

2. **Keyword boosting (BM25-like)**: For each candidate, term frequency and inverse document frequency are computed. Candidates containing exact query terms (case-insensitive) receive a boosting score. This addresses cases where semantic similarity is high but the exact keyword is missing (e.g., query "PostgreSQL" matching a drawer about "database setup" that mentions "Postgres" once).

3. **Temporal-proximity boosting**: Recent drawers are favored. Recency is computed from the drawer's `created_at` or `last_modified` timestamp. A decay function applies: drawers from the last 7 days get full boost, drawers older than 90 days get minimal boost. This addresses the problem where older, less relevant drawers rank high due to high semantic similarity but low temporal relevance.

4. **Preference-pattern extraction**: User likes/dislikes are mined from past exchanges (e.g., "I prefer X over Y", "never use Z"). These patterns are stored in the knowledge graph with `predicate: prefers` / `dislikes`. During retrieval, if a candidate drawer matches a known preference pattern (e.g., mentions a library the user dislikes), it is downranked or filtered out. This is optional and requires at least 10 mined preference statements to activate.

5. **Fusion scoring**: The three boosting signals are combined via weighted sum: `final_score = semantic_score + λ1 * keyword_score + λ2 * temporal_score + λ3 * preference_score`. Weights (λ1, λ2, λ3) were tuned on a 50-question dev split from LongMemEval (held constant, seed=42). The remaining 450 questions were never seen during tuning and constitute the held-out test set.

6. **Reranking**: The fused scores rerank the top-N candidates. The top-K (typically K=5-10) are returned to the user.

**Held-out evaluation**: On the 450-question held-out split, hybrid v4 achieves **98.4% R@5** (recall at top-5) without any LLM in the loop. This is the honest, generalizable figure. The full 500-question set (including the 50 dev questions) scores slightly higher (98.6%), but that includes questions used for tuning, so it's not a fair comparison.

**Optional LLM rerank**: An additional stage can promote the best candidate from the top-20 using an LLM reader (Claude Haiku, Claude Sonnet, minimax-m2.7 via Ollama Cloud). This pushes R@5 to ≥99% on the full 500-question set. However, the 99.4% → 100% step involved inspecting specific wrong answers, which `benchmarks/BENCHMARKS.md` flags as "teaching to the test". The LLM rerank is not included in the headline 98.4% figure because it requires an API key and is model-dependent.

## Key Properties

- **Deterministic tuning**: Weights tuned on 50 dev questions, held out 450 for eval (seed=42 for reproducibility).
- **No LLM in retrieval**: Hybrid v4 achieves 98.4% R@5 with zero LLM calls; all boosting is rule-based.
- **Complementary signals**: Keyword catches exact matches, temporal catches recency, preference catches user biases.
- **Opt-in**: Hybrid v4 is not the default; raw semantic search (96.6% R@5) is the out-of-box experience.
- **Reproducible**: `python benchmarks/longmemeval_bench.py <data.json> --mode hybrid_v4 --held-out` reproduces the 98.4% figure.

## Trade-offs

**Pros**: Significant recall improvement (98.4% vs 96.6%) with no LLM cost; interpretable boosting signals; generalizes to held-out data.

**Cons**: Requires tuning on a dev set; preference-pattern extraction needs at least 10 mined preference statements; temporal boosting assumes recent = relevant (not always true for evergreen documentation); keyword boosting may over-favor exact matches at the expense of semantic similarity.

## Example

**Query**: "Why did we choose PostgreSQL over MySQL?"

**Raw semantic search (96.6% R@5)**: Retrieves top-5 candidates, including drawer D1 (score 0.92, mentions "database decision, Postgres chosen for JSONB support") and drawer D2 (score 0.91, mentions "MySQL considered but rejected").

**Hybrid v4 (98.4% R@5)**: D1 gets keyword boost (+0.05 for exact "PostgreSQL" match) and temporal boost (+0.03 for being from last week). D2 gets keyword boost (+0.04 for "MySQL") but no temporal boost (from 6 months ago). Final scores: D1 = 1.00, D2 = 0.95. D1 ranks #1, D2 ranks #2. User retrieves the exact rationale in the top result.

## Relationship to Other Concepts

- **[[hybrid-retrieval-agent-memory-systems]]** — Broader treatment of hybrid retrieval across systems; hybrid v4 is MemPalace's specific implementation.
- **[[milla-jovovich/mempalace]]** — Project implementing hybrid v4.

## Practical Applications

- Improves recall for queries requiring exact keyword matches (e.g., library names, API endpoints).
- Prioritizes recent decisions/discussions over stale ones (e.g., "what's the current approach?" favors last week's conversation, not last year's).
- Filters out or downranks suggestions that conflict with user's stated preferences (e.g., "never use ORM X" prevents ORM X recommendations).

## Sources

- [[milla-jovovich/mempalace]] — `benchmarks/longmemeval_bench.py` reproduces the 98.4% R@5 held-out result.
- `benchmarks/BENCHMARKS.md` — methodology, tuning details, and "teaching to the test" disclaimer for the 100% figure.
