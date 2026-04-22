---
title: "Recursive Language Models"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "f5ae69a723513d24cbcbb84186eb866bf58307e8fe5c8f38ae2f92a7d7095538"
sources:
  - raw/2026-04-10-251224601v2pdf.md
quality_score: 77
concepts:
  - recursive-language-models
related:
  - "[[RLM-Qwen3-8B]]"
  - "[[Qwen3-Coder-480B-A35B]]"
tier: hot
knowledge_state: executed
tags: [agentic-architecture, long-context, language-models, scaling, recursion]
---

# Recursive Language Models

## Summary

This paper introduces Recursive Language Models (RLMs), a paradigm for scaling large language models (LLMs) to process arbitrarily long prompts by treating the prompt as an external environment and enabling programmatic, recursive self-invocation. RLMs outperform vanilla LLMs and common long-context scaffolds in both quality and cost across diverse tasks, and the authors demonstrate the first natively recursive language model via post-training. Extensive experiments show that RLMs maintain strong performance even as input lengths greatly exceed traditional context windows.

## Key Points

- RLMs allow LLMs to process prompts far beyond their native context window by recursively decomposing and invoking themselves over prompt slices.
- RLMs outperform vanilla LLMs and other agent scaffolds on long-context tasks, maintaining quality and comparable cost.
- The first natively recursive model, RLM-Qwen3-8B, is post-trained and achieves substantial performance gains over its base model.

## Concepts Extracted

- **Recursive Language Models** — Recursive Language Models (RLMs) are an inference-time paradigm for large language models (LLMs) that enables processing of arbitrarily long prompts by treating the prompt as an external environment and allowing the LLM to recursively invoke itself over programmatic slices of the prompt. This approach overcomes the limitations of fixed context windows and enables dense, expressive access to prompt content.

## Entities Mentioned

- **[[RLM-Qwen3-8B]]** — RLM-Qwen3-8B is the first natively recursive language model, created by post-training Qwen3-8B on filtered trajectories from Qwen3-Coder-480B-A35B. It is designed to operate as a Recursive Language Model, enabling programmatic recursion and manipulation of prompt content for long-context tasks.
- **[[Qwen3-Coder-480B-A35B]]** — Qwen3-Coder-480B-A35B is a frontier open language model used as a baseline and for generating training trajectories for RLM-Qwen3-8B. It is evaluated across diverse long-context tasks and serves as a foundation for recursive inference experiments.

## Notable Quotes

> "RLMs can successfully process inputs up to two orders of magnitude beyond model context windows and, even for shorter prompts, dramatically outperform the quality of vanilla frontier LLMs and common long-context scaffolds." — Alex L. Zhang et al.
> "The key insight is that arbitrarily long user prompts should not be fed into the neural network directly but should instead be treated as part of the environment that the LLM is tasked to symbolically and recursively interact with." — Alex L. Zhang et al.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-10-251224601v2pdf.md` |
| Type | paper |
| Author | Alex L. Zhang, Tim Kraska, Omar Khattab |
| Date | null |
| URL | https://arxiv.org/pdf/2512.24601 |
