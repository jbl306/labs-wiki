---
title: "Recursive Language Models"
type: source
created: 2026-04-10
last_verified: 2026-04-10
source_hash: "5f2847d1dbcf35bd34acfecc570026a5d5e0b7bde6f961fa89402aa86610f961"
sources:
  - raw/2026-04-10-251224601v2pdf.md
quality_score: 100
concepts:
  - recursive-language-models
related:
  - "[[RLM-Qwen3-8B]]"
  - "[[GPT-5]]"
  - "[[Qwen3-Coder-480B-A35B]]"
tier: hot
tags: [prompt-engineering, long-context, recursion, scaffolding, inference, language-models]
---

# Recursive Language Models

## Summary

This paper introduces Recursive Language Models (RLMs), a novel inference-time paradigm for scaling large language models (LLMs) to process arbitrarily long prompts. RLMs treat the prompt as an external environment, enabling programmatic decomposition and recursive self-invocation, thus overcoming context window limitations. The authors demonstrate that RLMs outperform vanilla LLMs and common long-context scaffolds across diverse tasks, maintaining comparable costs and showing strong performance even at the 10M+ token scale.

## Key Points

- RLMs enable LLMs to process inputs far beyond their native context window by treating prompts as external variables and using recursive calls.
- RLMs outperform base LLMs and common long-context scaffolds on tasks requiring dense access to prompt content, with significant gains in information-dense tasks.
- The REPL environment and symbolic recursion are essential for RLMs' expressiveness and scalability, allowing selective and programmatic context management.

## Concepts Extracted

- **Recursive Language Models** — Recursive Language Models (RLMs) are an inference-time scaffold for large language models (LLMs) that enable them to process arbitrarily long prompts by treating the prompt as an external environment. This paradigm allows the LLM to programmatically examine, decompose, and recursively invoke itself over portions of the input, overcoming the limitations of fixed context windows and enabling dense access to prompt content.

## Entities Mentioned

- **[[RLM-Qwen3-8B]]** — RLM-Qwen3-8B is the first natively recursive language model, created by fine-tuning Qwen3-8B to operate as a Recursive Language Model (RLM) with recursive sub-calls. It demonstrates substantial performance improvements on long-context tasks, approaching the quality of vanilla GPT-5 in several benchmarks.
- **[[GPT-5]]** — GPT-5 is a frontier large language model used as a base model and as a recursive sub-call agent in the evaluation of RLMs. It serves as a benchmark for comparing RLM performance and context scaling.
- **[[Qwen3-Coder-480B-A35B]]** — Qwen3-Coder-480B-A35B is a frontier open language model evaluated as both a base model and within the RLM scaffold. It is used in experiments on long-context tasks and information-dense benchmarks.

## Notable Quotes

> "We propose Recursive Language Models (RLMs), a general inference paradigm that treats long prompts as part of an external environment and allows the LLM to programmatically examine, decompose, and recursively call itself over snippets of the prompt." — Alex L. Zhang et al.
> "RLMs can successfully process inputs up to two orders of magnitude beyond model context windows and, even for shorter prompts, dramatically outperform the quality of vanilla frontier LLMs and common long-context scaffolds." — Alex L. Zhang et al.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-10-251224601v2pdf.md` |
| Type | paper |
| Author | Alex L. Zhang, Tim Kraska, Omar Khattab |
| Date | 2026-01-28 |
| URL | https://arxiv.org/pdf/2512.24601 |
