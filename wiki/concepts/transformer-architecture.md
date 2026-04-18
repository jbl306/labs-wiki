---
title: "Transformer Architecture"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "526c9c18bb793ad371844f633b6ee7b5a9c81a887586b409bfcc05845b0dc1bb"
sources:
  - raw/2026-04-07-transformer-architecture-note.md
quality_score: 100
concepts:
  - transformer-architecture
related:
  - "[[Self-Attention Mechanism]]"
  - "[[Multi-Head Attention]]"
  - "[[Positional Encoding]]"
  - "[[Attention Mechanism in Large Language Models]]"
  - "[[Flash Attention in Large Language Models]]"
  - "[[KV Cache and Paged Attention in Large Language Models]]"
  - "[[Transformer Architecture Note]]"
tier: hot
tags: [transformer, deep-learning, self-attention, nlp]
---

# Transformer Architecture

## Overview

The Transformer architecture is a deep learning model introduced to handle sequence transduction tasks without relying on recurrence. Its main innovation is the self-attention mechanism, which enables parallel processing of sequence elements and efficient modeling of long-range dependencies.

## How It Works

The Transformer architecture is built on the principle of self-attention, which allows each position in the input sequence to attend to all other positions, capturing dependencies regardless of their distance. Unlike recurrent neural networks (RNNs) or long short-term memory networks (LSTMs), which process sequences sequentially, the Transformer processes all tokens in parallel, leading to significant speedups in training and inference.

A Transformer model is composed of an encoder and a decoder, each consisting of multiple identical layers. Each encoder layer contains two main sub-layers: a multi-head self-attention mechanism and a position-wise fully connected feed-forward network. Layer normalization and residual connections are applied around each sub-layer to stabilize training and facilitate gradient flow.

The self-attention mechanism computes a weighted sum of all input representations for each position, where the weights are determined by the similarity between query and key vectors. These vectors are derived from the input embeddings via learned linear transformations. The multi-head attention mechanism extends this by projecting the input into multiple subspaces (heads), performing self-attention in each, and concatenating the results. This enables the model to capture diverse types of relationships and patterns in the data.

Since the architecture lacks any inherent notion of sequence order, positional encodings are added to the input embeddings. These encodings inject information about the position of each token, allowing the model to distinguish between different sequence arrangements. The original paper uses sinusoidal positional encodings, but learned positional embeddings are also common.

The decoder layers are similar but include an additional encoder-decoder attention sub-layer, enabling the decoder to attend to the encoder's output. Masking is applied in the decoder's self-attention to prevent positions from attending to subsequent positions, preserving the autoregressive property needed for sequence generation.

The Transformer architecture's parallelism and ability to model long-range dependencies have made it the foundation for state-of-the-art models in natural language processing, such as BERT, GPT, and many others.

## Key Properties

- **Self-Attention Mechanism:** Allows each token to attend to all others in the sequence, capturing global dependencies efficiently.
- **Multi-Head Attention:** Enables the model to jointly attend to information from different representation subspaces at different positions.
- **Positional Encoding:** Injects information about the order of tokens, compensating for the lack of recurrence or convolution.
- **Parallelization:** Processes all tokens in a sequence simultaneously, leading to faster training and inference compared to RNNs.

## Limitations

Transformers require substantial computational resources, especially for long sequences, due to the quadratic complexity of self-attention with respect to sequence length. They also lack an inherent inductive bias for sequential data, relying entirely on positional encodings. For very long sequences, memory and efficiency can become bottlenecks.

## Example

Suppose we have an input sequence: ["The", "cat", "sat"]. Each word is embedded into a vector, positional encodings are added, and the self-attention mechanism computes attention scores between all pairs (e.g., 'The' attends to 'cat' and 'sat'). Multi-head attention allows the model to capture different aspects of the relationships. The output is then passed through feed-forward layers and stacked for deeper representations.

## Visual

No diagram or image is included in the source.

## Relationship to Other Concepts

- **[[Self-Attention Mechanism]]** — Core component of the Transformer architecture.
- **[[Multi-Head Attention]]** — Enhances the representational power of self-attention in Transformers.
- **[[Positional Encoding]]** — Essential for providing sequence order information in Transformers.

## Practical Applications

Transformers are widely used in machine translation, text summarization, question answering, language modeling, and many other NLP tasks. Their parallelism and scalability have also enabled applications in computer vision, protein folding, and more.

## Sources

- [[Transformer Architecture Note]] — primary source for this concept
