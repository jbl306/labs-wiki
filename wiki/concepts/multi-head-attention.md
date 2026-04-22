---
title: "Multi-Head Attention"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "526c9c18bb793ad371844f633b6ee7b5a9c81a887586b409bfcc05845b0dc1bb"
sources:
  - raw/2026-04-07-transformer-architecture-note.md
quality_score: 79
concepts:
  - multi-head-attention
related:
  - "[[Self-Attention Mechanism]]"
  - "[[Transformer Architecture]]"
  - "[[Transformer Architecture Note]]"
tier: hot
tags: [multi-head-attention, self-attention, transformer]
---

# Multi-Head Attention

## Overview

Multi-head attention is an extension of the self-attention mechanism that allows the model to attend to information from multiple representation subspaces simultaneously. It enhances the model's ability to capture diverse relationships within the data.

## How It Works

In multi-head attention, the input is linearly projected into multiple sets of queries, keys, and values (one set for each head). Each head performs self-attention independently, learning to focus on different aspects of the sequence. The outputs of all heads are then concatenated and projected through a final linear layer to produce the final output.

Formally, for each head \(i\):

\[
\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)
\]

where \(W_i^Q, W_i^K, W_i^V\) are learned projection matrices for head \(i\). The outputs of all heads are concatenated and passed through another learned projection:

\[
\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_h)W^O
\]

This design allows each head to learn different types of relationships and patterns, such as syntactic dependencies, semantic roles, or positional relationships. By combining multiple heads, the model can capture richer and more nuanced representations than a single attention mechanism could.

Multi-head attention is used in both the encoder and decoder layers of the Transformer. It is a key factor in the model's expressiveness and performance, as it enables the aggregation of information from multiple perspectives at each layer.

The number of heads is a hyperparameter, typically set to 8 or 16 in practice. Increasing the number of heads can improve performance up to a point, but also increases computational cost.

## Key Properties

- **Diversity of Representations:** Each head can learn to focus on different relationships, improving the model's expressiveness.
- **Parallel Processing:** All heads operate independently and in parallel, maintaining efficiency.
- **Final Aggregation:** Outputs from all heads are concatenated and linearly transformed to produce the final output.

## Limitations

Multi-head attention increases the number of parameters and computational cost. If the number of heads is too large relative to the model size, each head may have too little capacity to learn meaningful patterns. There is also redundancy among heads in some cases.

## Example

For a 4-head attention layer, the input is projected into 4 sets of queries, keys, and values. Each head computes self-attention separately, and the results are concatenated and projected to form the output.

## Relationship to Other Concepts

- **[[Self-Attention Mechanism]]** — Multi-head attention is a parallelized, multi-representation extension of self-attention.
- **[[Transformer Architecture]]** — Multi-head attention is a core component of each Transformer layer.

## Practical Applications

Multi-head attention is used in all Transformer-based models for NLP, vision, and other domains. It is critical for tasks requiring the modeling of complex, multi-faceted relationships in data.

## Sources

- [[Transformer Architecture Note]] — primary source for this concept
