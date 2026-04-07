---
title: "Multi-Head Attention"
type: concept
created: 2026-04-07
last_verified: 2026-04-07
source_hash: "526c9c18bb793ad371844f633b6ee7b5a9c81a887586b409bfcc05845b0dc1bb"
sources:
  - raw/2026-04-07-transformer-architecture-note.md
quality_score: 0
concepts:
  - multi-head-attention
related:
  - "[[Self-Attention Mechanism]]"
  - "[[Transformer Architecture Note]]"
tier: hot
tags: [multi-head-attention, transformer, deep-learning]
---

# Multi-Head Attention

## Overview

A mechanism in the Transformer architecture that allows the model to focus on different representation subspaces simultaneously.

## How It Works

Multi-head attention splits the input embeddings into multiple smaller subspaces, applies self-attention independently to each, and then concatenates the results. This enables the model to capture diverse relationships within the data.

## Key Properties

- **Subspace Representation:** Focuses on different aspects of the input data.
- **Parallel Processing:** Processes multiple attention heads simultaneously.

## Relationship to Other Concepts

- **[[Self-Attention Mechanism]]** — Builds on self-attention to enhance representation.

## Practical Applications

Improves performance in tasks requiring nuanced understanding of input data, such as language modeling and image recognition.

## Sources

- [[Transformer Architecture Note]] — primary source for this concept
