---
title: "Context Window"
type: concept
created: 2026-04-07
last_verified: 2026-04-07
source_hash: "a4e125acd956ed0ccf70ba66d6510f746deb20fa870597168af46311ee8dd133"
sources:
  - raw/2026-04-07-test-tweet.md
quality_score: 0
concepts:
  - context-window
related:
  - "[[Transformer Architecture]]"
  - "[[Karpathy LLM OS Tweet]]"
tier: hot
tags: [context-window, llm, memory]
---

# Context Window

## Overview

The context window refers to the amount of information (tokens) an LLM can process at once, analogous to RAM in traditional computers.

## How It Works

The LLM's context window determines how much data it can 'remember' and reason over during inference. Larger context windows enable more complex tasks and richer interactions, but are limited by model architecture and hardware.

## Key Properties

- **Token Limit:** Defines the maximum number of tokens the LLM can handle.
- **RAM Analogy:** Acts as the LLM's working memory during computation.

## Relationship to Other Concepts

- **[[Transformer Architecture]]** — Context window size is determined by transformer model design.

## Practical Applications

Critical for tasks requiring long-term memory, document analysis, and multi-turn conversations.

## Sources

- [[Karpathy LLM OS Tweet]] — primary source for this concept
