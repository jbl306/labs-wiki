---
title: "The Context Hygiene Principle | 10 Claude Code Principles"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "f746baf27768533a8c0ad9df802594ecb61e45933c725a7cf5ef4e92306fadc3"
sources:
  - raw/2026-04-08-the-context-hygiene-principle-10-claude-code-principles.md
quality_score: 86
concepts:
  - the-context-hygiene-principle
  - u-shaped-attention-curve-transformer-models
  - progressive-disclosure-context-loading
  - context-poisoning-llm-workflows
related:
  - "[[The Context Hygiene Principle]]"
  - "[[U-Shaped Attention Curve in Transformer Models]]"
  - "[[Progressive Disclosure Context Loading]]"
  - "[[Context Poisoning in LLM Workflows]]"
  - "[[jig]]"
tier: hot
knowledge_state: executed
tags: [attention-mechanism, context-hygiene, llm, prompt-engineering, agentic-workflows]
---

# The Context Hygiene Principle | 10 Claude Code Principles

## Summary

This article introduces and details the Context Hygiene Principle for working with large language models, especially Claude. It explains the scientific basis for context management, emphasizing that context is a scarce resource and that indiscriminate accumulation of tokens leads to performance degradation. The article provides actionable strategies for maintaining optimal context, including aggressive clearing, externalizing state, and structuring prompts to leverage the U-shaped attention curve.

## Key Points

- Context is a finite and highly competitive resource in transformer-based LLMs.
- The U-shaped attention curve means critical information should be front-loaded or back-loaded, never buried in the middle.
- Optimal context utilization is 15-40% of the window; more context leads to attention dilution and performance drop.
- Aggressive clearing and externalizing state to files maintains high signal-to-noise ratio and prevents context rot.
- Stale or poisoned context actively misleads the model, requiring regular audits and maintenance.

## Concepts Extracted

- **[[The Context Hygiene Principle]]** — The Context Hygiene Principle is a foundational guideline for working with large language models (LLMs) such as Claude. It asserts that context is a scarce and competitive resource, and that maximizing model performance requires aggressive clearing of conversations, externalizing state to files, and loading only the minimal, relevant context for the current task. This principle is grounded in the structural properties of transformer architectures and the empirical findings on attention distribution.
- **[[U-Shaped Attention Curve in Transformer Models]]** — The U-shaped attention curve describes how transformer-based LLMs distribute attention across context positions. Tokens at the start and end of the context receive high attention weight, while those in the middle suffer a significant drop. This curve is a structural consequence of causal masking and Rotary Position Embedding (RoPE), and has direct implications for prompt and context design.
- **[[Progressive Disclosure Context Loading]]** — Progressive disclosure is a context management strategy for LLMs that loads the right context at the right time, using a layered stack. It minimizes attention dilution and maximizes task focus by ensuring only relevant information is present in the model's context window.
- **[[Context Poisoning in LLM Workflows]]** — Context poisoning occurs when outdated, irrelevant, or misleading information remains in the model's context window, actively degrading performance. Unlike context bloat, which passively dilutes attention, poisoned context misdirects the model toward obsolete or incorrect patterns.

## Entities Mentioned

- **[[jig]]** — jig is a tool designed to manage plugin, MCP server, skill, and hook loading in Claude sessions. It uses project-checked-in configuration files to selectively enable and disable tools per session, ensuring only relevant resources are loaded for the current task. This approach preserves attention budget and prevents unnecessary dilution from unused tools.

## Notable Quotes

> "Context is your scarcest resource. Clear conversations aggressively, externalize every plan and artifact to focused files, and use minimal knowledge structures so the agent stays sharp and token-efficient." — jdforsythe
> "Every token you add that is not directly relevant to the current task is actively degrading performance on the tokens that are." — jdforsythe
> "The U-shaped attention curve is not optional. Middle content receives measurably less attention — 30%+ less, per Liu et al. Critical instructions in the middle may as well be whispered in a noisy room." — jdforsythe

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-08-the-context-hygiene-principle-10-claude-code-principles.md` |
| Type | article |
| Author | jdforsythe |
| Date | Unknown |
| URL | https://jdforsythe.github.io/10-principles/principles/context-hygiene/ |
