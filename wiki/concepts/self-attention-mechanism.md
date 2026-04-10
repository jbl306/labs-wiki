---
title: "Self-Attention Mechanism"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "526c9c18bb793ad371844f633b6ee7b5a9c81a887586b409bfcc05845b0dc1bb"
sources:
  - raw/2026-04-07-transformer-architecture-note.md
quality_score: 100
concepts:
  - self-attention-mechanism
related:
  - "[[Transformer Architecture]]"
  - "[[Transformer Architecture Note]]"
tier: hot
tags: [self-attention, transformer, deep-learning]
---

# Self-Attention Mechanism

## Overview

Self-attention is a mechanism that allows each element of a sequence to attend to all other elements, enabling the model to capture dependencies regardless of their distance. It is the foundational building block of the Transformer architecture.

## How It Works

In self-attention, each input token is projected into three vectors: query (Q), key (K), and value (V), using learned linear transformations. The attention score between two tokens is computed as the dot product of their query and key vectors, scaled by the square root of the dimension of the key vectors (\( \sqrt{d_k} \)) to prevent large values from destabilizing the softmax function:

\[
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
\]

This produces a weighted sum of the value vectors, where the weights reflect the relevance of each token to the current token. By computing these scores for all pairs of tokens, the model can aggregate information from the entire sequence at each position.

The self-attention mechanism is highly parallelizable, as all attention scores can be computed simultaneously using matrix operations. This enables efficient training and inference, especially on modern hardware like GPUs and TPUs. The mechanism is also flexible, as it can model both local and global dependencies without regard to their position in the sequence.

Self-attention is used in both the encoder and decoder of the Transformer. In the decoder, a masked version is used to prevent attending to future tokens during training, preserving causality for sequence generation tasks.

The main intuition behind self-attention is that it allows the model to dynamically focus on relevant parts of the input for each position, rather than relying on fixed-size windows or sequential processing. This adaptability is a key factor in the success of Transformer-based models.

## Key Properties

- **Global Context:** Each token can attend to all others, capturing long-range dependencies efficiently.
- **Parallel Computation:** All attention scores are computed simultaneously, enabling fast training.
- **Scalability:** Easily extended to long sequences, though with quadratic complexity in sequence length.

## Limitations

The main limitation is the quadratic time and space complexity with respect to sequence length, making it challenging to scale to very long sequences. Additionally, self-attention does not encode any prior knowledge about sequence structure, relying entirely on learned parameters and positional encodings.

## Example

Given a sequence [A, B, C], self-attention computes attention scores between all pairs: (A,B), (A,C), (B,C), etc. For each position, the output is a weighted sum of all value vectors, with weights determined by the similarity of queries and keys.

## Relationship to Other Concepts

- **[[Transformer Architecture]]** — Self-attention is the core operation in each Transformer layer.

## Practical Applications

Self-attention is used in language models, translation systems, and any task where capturing relationships between sequence elements is important. It has also been adapted for images, graphs, and other data modalities.

## Sources

- [[Transformer Architecture Note]] — primary source for this concept
