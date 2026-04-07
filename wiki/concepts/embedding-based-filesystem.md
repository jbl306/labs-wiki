---
title: "Embedding-Based Filesystem"
type: concept
created: 2026-04-07
last_verified: 2026-04-07
source_hash: "a4e125acd956ed0ccf70ba66d6510f746deb20fa870597168af46311ee8dd133"
sources:
  - raw/2026-04-07-test-tweet.md
quality_score: 0
concepts:
  - embedding-based-filesystem
related:
  - "[[Context Window]]"
  - "[[Karpathy LLM OS Tweet]]"
tier: hot
tags: [embedding, filesystem, llm, semantic-search]
---

# Embedding-Based Filesystem

## Overview

A filesystem that stores not only traditional data but also embeddings, allowing LLMs to efficiently retrieve and reason over stored information.

## How It Works

Embeddings are vector representations of data, enabling semantic search and retrieval. The LLM interacts with this filesystem to access relevant information, using embeddings to match queries with stored content. This enhances the LLM's ability to recall and utilize context beyond its immediate window.

## Key Properties

- **Semantic Retrieval:** Embeddings allow for context-aware, semantic search of files.
- **Integration with LLM:** Filesystem is designed to be accessed and utilized by the LLM.

## Relationship to Other Concepts

- **[[Context Window]]** — Embeddings supplement the LLM's limited context window.

## Practical Applications

Used in AI-powered knowledge management, search systems, and intelligent assistants.

## Sources

- [[Karpathy LLM OS Tweet]] — primary source for this concept
