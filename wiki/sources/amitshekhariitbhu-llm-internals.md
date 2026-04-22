---
title: amitshekhariitbhu/llm-internals
type: source
created: '2026-04-21'
last_verified: '2026-04-22'
source_hash: bd7533347210f3de1fc3aa28a3b1cfbf5e71b1322fd169946ce1b5d7759ffe78
sources:
- raw/2026-04-13-amitshekhariitbhullm-internals-learn-llm-internals-step-by-s.md
source_url: https://github.com/amitshekhariitbhu/llm-internals
tags:
- attention-is-all-you-need
- attention-mechanism
- github
- large-language-models
- learn-llm
- llm
- llm-internals
- none
tier: warm
knowledge_state: ingested
ingest_method: manual-deepen-github-2026-04-22
quality_score: 90
concepts:
- attention-mechanism-in-large-language-models
- byte-pair-encoding-bpe-in-large-language-models
- backpropagation-learning-mechanism
- self-attention-mechanism
- multi-head-attention
- flash-attention-in-large-language-models
- kv-cache-and-paged-attention-in-large-language-models
---

# amitshekhariitbhu/llm-internals

## What it is

A curated learning index, maintained by Amit Shekhar (founder of Outcome School), that walks through LLM internals step by step from tokenization through attention to inference optimization. The repo itself is mostly a README of links — each entry points to a blog post on `outcomeschool.com` or a YouTube video covering one mechanism (BPE, scaled dot-product attention, causal masking, backpropagation, cross-entropy loss, the full Transformer architecture, etc.) with worked numeric examples.

## Why it matters

Useful as a reference index for ourselves and any agents we point at "explain this LLM concept" tasks. Many of the topics already have local concept pages (attention, BPE, backprop) that this repo could be used to refresh or expand. Not a tool to deploy — a learning resource to mine when authoring new wiki concept pages.

## Curriculum / Topics covered

**Tokenization and BPE** — Explains why raw text must be split into subword units before an LLM can process it. Walks through Byte Pair Encoding (BPE): the iterative merge algorithm that builds a vocabulary from byte pairs, how it handles rare words, and why it's the default tokenizer for GPT, LLaMA, and most modern LLMs. Includes step-by-step merge examples.
> See [[byte-pair-encoding-bpe-in-large-language-models]].

**Math behind Attention (Q, K, V)** — Introduces Query, Key, Value matrices and the scaled dot-product attention formula: `softmax((Q × K^T) / √dₖ) × V`. Provides a worked numeric example: given two input word vectors, computes attention scores, applies softmax, and calculates the weighted output. Clarifies what each component (Q, K, V) represents.
> See [[attention-mechanism-in-large-language-models]] and [[self-attention-mechanism]].

**√dₖ Scaling factor** — Explains why dot products between Q and K grow with embedding dimension `dₖ` (variance scales linearly with `dₖ`). Derives the variance formula step-by-step, shows how large dot products push softmax into saturation (near-zero gradients), and proves why dividing by `√dₖ` stabilizes training. Includes numeric comparisons: attention scores before and after scaling.

**Causal Masking** — Covers how autoregressive LLMs prevent tokens from attending to future positions. Shows the causal mask matrix (upper triangular `-inf` entries), demonstrates how it zeroes out future attention weights after softmax, and provides an implementation walkthrough. Explains the difference between masked and unmasked attention outputs.

**Backpropagation math** — Deep dive into the chain rule, forward pass (layer-by-layer activation computation), loss calculation, and backward pass (gradient propagation from loss to weights). Includes a step-by-step numeric example: computing gradients for a two-layer network with ReLU activation, then updating weights via gradient descent. Concludes with a Python implementation.

**Cross-Entropy Loss** — Explains the loss function used to train LLMs and classifiers. Covers binary vs. categorical cross-entropy, the role of negative log-likelihood, and why minimizing cross-entropy maximizes the probability of the correct class. Walks through a step-by-step numeric example (model outputs logits → softmax → cross-entropy), derives the gradient formula, and shows how it propagates through backprop. Connects to language modeling: predicting the next token.

**Transformer Architecture Decoded** — Component-by-component breakdown of the original Transformer (encoder-decoder) and its three modern variants: encoder-only (BERT), decoder-only (GPT), encoder-decoder (T5/BART). Explains why each piece exists: tokenization + embeddings, positional encoding, multi-head attention, feed-forward networks, residual connections, layer normalization. Traces data flow through the full architecture. Answers "why is the Transformer so powerful?" (parallelizable, scalable, context-aware).
> See [[multi-head-attention]].

**Feed-Forward Networks in LLMs** — Explains the position-wise FFN that follows every attention layer in a Transformer: a two-layer MLP with expand-then-contract structure (typically `4 × d_model` intermediate size). Covers the ReLU activation, what the FFN actually learns (feature transformations beyond attention), and how much of the model's parameters live in FFNs (typically 2/3 of total). Introduces Mixture of Experts (MoE) as an FFN variant.

**KV Cache in LLMs** — Explains how autoregressive generation recomputes attention for all prior tokens at every step, why this is wasteful, and how caching Key and Value matrices eliminates redundant computation. Shows why Query isn't cached (it's only used once per token). Includes speed/memory trade-off analysis: KV cache grows linearly with sequence length and can consume gigabytes for long contexts.
> See [[kv-cache-and-paged-attention-in-large-language-models]].

**Paged Attention** — Introduces vLLM's paging technique: splits KV cache into fixed-size blocks (pages) instead of pre-allocating contiguous memory per request. Explains the memory waste problem (over-allocation for unknown sequence lengths) and how Paged Attention solves it by allocating pages on demand. Covers memory sharing across requests (prefix caching for shared prompts). Inspired by OS virtual memory.
> See [[kv-cache-and-paged-attention-in-large-language-models]].

**Flash Attention** — Explains why standard attention is memory-bound (reads/writes large NxN score matrices to HBM), how GPU memory hierarchy works (fast SRAM vs. slow HBM), and Flash Attention's tiling + online softmax trick. Covers tiling (splits Q/K/V into blocks, computes attention in SRAM), online softmax (incremental softmax computation without storing the full score matrix), and recomputation in the backward pass (trades recomputation for memory). Mentions Flash Attention 2 (better parallelism) and Flash Attention 3 (asynchronous pipelining). Shows why it's 2–4× faster with zero approximation error.
> See [[flash-attention-in-large-language-models]].

**Mixture of Experts (MoE)** — Explains how MoE replaces dense FFNs with sparse expert selection: each token is routed to the top-k experts (typically k=2) out of N total experts. Covers the router network (learned gating function), sparse activation (only k experts compute per token, saving FLOPs), load balancing (auxiliary loss to prevent expert collapse), and why MoE scales efficiently (more parameters, same compute per token). Used in Mixtral, GPT-4 (rumored), and other large models.

**Harness Engineering in AI** — Explains the harness concept: the execution environment that wraps an AI model or agent to provide inputs, capture outputs, enforce constraints, and measure performance. Covers harness components (data loaders, prompt templates, output parsers, evaluation metrics), use cases (agent task execution, benchmark evaluation), and best practices (deterministic replay, versioning, isolation).

## How it works

**Repository structure**: The repo is a single README acting as a structured table of contents. Each topic is an `## Heading` with:
- A 2–3 sentence summary of what the topic covers
- A bulleted outline of subtopics (e.g., "What is BPE?", "How BPE Works: Step by Step")
- A link to the corresponding outcomeschool.com blog post or YouTube video

**Learning path**: Topics are ordered bottom-up: tokenization → attention math → Transformer architecture → inference optimizations (KV cache, Paged Attention, Flash Attention, MoE). The intro video ("AI Engineering Explained: LLM, RAG, MCP, Agent, Fine-Tuning, Quantization") provides high-level context before diving into internals.

**Content format**: Most topics are blog posts (outcomeschool.com) with step-by-step math walkthroughs and numeric examples. A few have companion YouTube videos. The repo itself contains no code — it's a curated index pointing to external resources.

**License**: Apache 2.0 (Outcome School), so content can be referenced and adapted with attribution.

## API / interface surface

**No programmatic API** — This is a learning resource, not a deployable tool. The "interface" is the README structure:
- 14 topic headings, each with:
  - Summary paragraph
  - Bulleted subtopic outline
  - Link to external content (outcomeschool.com or YouTube)
- External links:
  - Blog posts: `https://outcomeschool.com/blog/<topic-slug>`
  - YouTube videos: `https://www.youtube.com/watch?v=<video-id>`
- Maintained by: [Amit Shekhar](https://x.com/amitiitbhu), founder of Outcome School
- Last commit: April 2026 (actively updated)

## Setup

No setup required — read the README and follow the links.

```bash
# Clone to browse locally
git clone https://github.com/amitshekhariitbhu/llm-internals.git
cd llm-internals
cat README.md
```

## Integration notes

Source material for upgrading or backfilling our existing concept pages on attention, BPE, backprop, cross-entropy, and the Transformer. When adding a new ML primer concept page (especially in nba-ml-engine context for ML newcomers reading the codebase), this is a known-good external reference to cite.

## Caveats / Gotchas

- **Off-repo content**: All substantive content lives on outcomeschool.com or YouTube. The repository itself is just a README index. Long-term link rot is the primary risk — if Outcome School's domain goes down, the links break.
- **No source code**: Repo `Language: None` because there are no implementation files, only Markdown. This is a *learning* resource, not a code artifact. Examples in the blog posts are pseudocode or illustrative; no runnable scripts provided.
- **License unspecified in README excerpt**: The README footer says "Apache License, Version 2.0 (Outcome School)", but verify the upstream LICENSE file before redistributing any of the blog content itself.
- **Ongoing updates**: Maintained by a single author (Amit Shekhar). Last update April 2026 with Cross-Entropy Loss added. New topics are added as blog posts are published, so the curriculum is still growing.
- **No interactive exercises**: Unlike notebook-based tutorials (e.g., fast.ai, Hugging Face courses), this resource is read-only. You watch/read, then implement yourself. No Colab notebooks or problem sets.
- **Focus on fundamentals, not implementation**: Explains *how* mechanisms work (math, concepts), not *how to code them*. For hands-on implementation, pair with Hugging Face `transformers` docs or Karpathy's nanoGPT.
- **No benchmarks**: Blog posts don't include performance numbers (e.g., Flash Attention speedup on specific hardware). They explain *why* optimizations work, not empirical results.

## Repo metadata

| Field | Value |
|---|---|
| Stars | 605 |
| Primary language | (none — Markdown only) |
| Topics | attention-is-all-you-need, attention-mechanism, large-language-models, learn-llm, llm, llm-internals |
| License | (see upstream) |

## Related concepts

- [[attention-mechanism-in-large-language-models]]
- [[self-attention-mechanism]]
- [[multi-head-attention]]
- [[byte-pair-encoding-bpe-in-large-language-models]]
- [[backpropagation-learning-mechanism]]
- [[kv-cache-and-paged-attention-in-large-language-models]]
- [[flash-attention-in-large-language-models]]
- [[tokenization-and-representation-in-vla-models]]
- [[u-shaped-attention-curve-transformer-models]]

## Source

- Raw dump: `raw/2026-04-13-amitshekhariitbhullm-internals-learn-llm-internals-step-by-s.md`
- Upstream: https://github.com/amitshekhariitbhu/llm-internals
