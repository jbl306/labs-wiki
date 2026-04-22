---
title: "The Context Hygiene Principle"
type: source
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "4e0be7f4370f91ef752fb421adafe9e295a097a9f83ca034d9e875ec44e0bba9"
sources:
  - raw/2026-04-08-the-context-hygiene-principle-10-claude-code-principles.md
quality_score: 76
concepts:
  - the-context-hygiene-principle
related:
  - "[[Claude]]"
  - "[[jig]]"
tier: hot
tags: [prompt-engineering, transformer, attention-mechanism, llm, context-management]
---

# The Context Hygiene Principle

## Summary

This article, part of the '10 Claude Code Principles,' introduces the Context Hygiene Principle for working with large language models (LLMs) like Claude. It explains why context is a scarce resource, how the transformer architecture's self-attention mechanism creates quadratic competition among tokens, and provides actionable strategies to maintain high-quality, efficient sessions. The principle is grounded in recent research on attention allocation and context window utilization, offering practical steps for developers to avoid context rot, poisoning, and performance degradation.

## Key Points

- Context in LLMs is a finite, highly competitive resource due to the quadratic scaling of self-attention.
- The U-shaped attention curve means position within context is critical—front-load constraints, back-load instructions.
- Aggressive context clearing, externalizing state, and minimal knowledge structures dramatically improve performance and reduce token spend.

## Concepts Extracted

- **The Context Hygiene Principle** — The Context Hygiene Principle is a disciplined approach to managing context in large language model (LLM) interactions. It asserts that context is a finite, highly competitive resource, and that maintaining focused, relevant, and minimal context is essential for optimal model performance. The principle is rooted in the transformer architecture's self-attention mechanism, which causes every token to compete with every other token, leading to quadratic scaling of attention relationships and potential performance degradation as context grows.

## Entities Mentioned

- **[[Claude]]** — Claude is a large language model (LLM) developed by Anthropic, designed for conversational AI, code generation, and other advanced language tasks. It is notable for its long context window and focus on safety and interpretability.
- **[[jig]]** — jig is a tool for managing plugin, MCP server, skill, and hook loading in Claude sessions. It enables selective activation of tools per session based on project configuration files.

## Notable Quotes

> "Context is your scarcest resource. Treat it like memory in an embedded system, not disk space on a server." — J.D. Forsythe
> "Every token you add to context actively competes with every other token for the model’s attention. This is not a metaphor. It is a mathematical consequence of the transformer architecture." — J.D. Forsythe
> "Stale context is worse than no context — it actively misdirects the model." — J.D. Forsythe

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-08-the-context-hygiene-principle-10-claude-code-principles.md` |
| Type | article |
| Author | J.D. Forsythe |
| Date | Unknown |
| URL | https://jdforsythe.github.io/10-principles/principles/context-hygiene/ |
