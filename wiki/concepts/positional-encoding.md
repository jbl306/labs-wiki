---
title: "Positional Encoding"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "526c9c18bb793ad371844f633b6ee7b5a9c81a887586b409bfcc05845b0dc1bb"
sources:
  - raw/2026-04-07-transformer-architecture-note.md
quality_score: 0
concepts:
  - positional-encoding
related:
  - "[[Transformer Architecture]]"
  - "[[Transformer Architecture Note]]"
tier: hot
tags: [positional-encoding, transformer, sequence-modeling]
---

# Positional Encoding

## Overview

Positional encoding is a technique used in Transformer models to inject information about the order of sequence elements, compensating for the lack of recurrence or convolution. It enables the model to distinguish between different positions in the input sequence.

## How It Works

Since the Transformer processes all tokens in a sequence simultaneously and does not have a built-in notion of order, positional encodings are added to the input embeddings to provide sequence information. The original Transformer paper uses sinusoidal positional encodings, where each dimension of the encoding corresponds to a sinusoid of a different frequency:

\[
PE_{(pos, 2i)} = \sin(pos / 10000^{2i/d_{model}})
\]
\[
PE_{(pos, 2i+1)} = \cos(pos / 10000^{2i/d_{model}})
\]

where \(pos\) is the position and \(i\) is the dimension. These encodings are added to the input embeddings before being fed into the model. The sinusoidal design allows the model to learn to attend by relative positions, as any fixed offset between positions can be represented as a linear function of the encodings.

Alternatively, learned positional embeddings can be used, where each position has a trainable vector. This approach allows the model to adapt the positional information during training but may not generalize to longer sequences than seen during training.

Positional encodings are essential for any task where the order of elements matters, such as language modeling or translation. Without them, the model would treat the input as a bag of tokens, ignoring sequence structure.

The choice between sinusoidal and learned positional encodings involves trade-offs between generalization and flexibility. Sinusoidal encodings generalize to unseen sequence lengths, while learned embeddings can better fit the training data but may not extrapolate.

## Key Properties

- **Order Information:** Encodes the position of each token, enabling the model to capture sequence structure.
- **Sinusoidal or Learned:** Can be fixed (sinusoidal) or learned during training.
- **Addition to Embeddings:** Positional encodings are added to token embeddings before input to the model.

## Limitations

Sinusoidal encodings may not capture complex positional relationships as well as learned embeddings. Learned embeddings may not generalize to longer sequences than those seen during training. Both approaches add parameters and computation.

## Example

For a 10-token sequence, each token embedding is augmented with a positional encoding vector (using sin/cos functions or learned vectors) before being processed by the Transformer.

## Relationship to Other Concepts

- **[[Transformer Architecture]]** — Positional encoding is required for Transformers to process sequences meaningfully.

## Practical Applications

Used in all Transformer-based models for NLP, speech, and other sequential data. Critical for tasks where the order of elements affects meaning, such as translation or summarization.

## Sources

- [[Transformer Architecture Note]] — primary source for this concept
