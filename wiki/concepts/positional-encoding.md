---
title: "Positional Encoding"
type: concept
created: 2026-04-07
last_verified: 2026-04-07
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
tags: [positional-encoding, transformer, nlp]
---

# Positional Encoding

## Overview

A technique used in the Transformer architecture to provide sequence order information to the model, which lacks inherent sequential structure.

## How It Works

Positional encoding adds a unique vector to each input token based on its position in the sequence. These vectors are often derived using sinusoidal functions, ensuring that each position has a unique representation.

## Key Properties

- **Sequence Order:** Encodes the position of each token in the sequence.
- **Sinusoidal Functions:** Commonly used to generate positional encodings.

## Relationship to Other Concepts

- **[[Transformer Architecture]]** — Essential for handling sequence data in Transformers.

## Practical Applications

Used in tasks where sequence order is critical, such as language translation and speech recognition.

## Sources

- [[Transformer Architecture Note]] — primary source for this concept
