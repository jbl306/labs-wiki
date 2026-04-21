---
title: "Progressive Disclosure Context Loading"
type: concept
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "f746baf27768533a8c0ad9df802594ecb61e45933c725a7cf5ef4e92306fadc3"
sources:
  - raw/2026-04-08-the-context-hygiene-principle-10-claude-code-principles.md
quality_score: 100
concepts:
  - progressive-disclosure-context-loading
related:
  - "[[The Context Hygiene Principle]]"
  - "[[The Context Hygiene Principle | 10 Claude Code Principles]]"
tier: hot
tags: [context-management, progressive-disclosure, agentic-workflows, prompt-engineering]
---

# Progressive Disclosure Context Loading

## Overview

Progressive disclosure is a context management strategy for LLMs that loads the right context at the right time, using a layered stack. It minimizes attention dilution and maximizes task focus by ensuring only relevant information is present in the model's context window.

## How It Works

Progressive disclosure divides context loading into four layers, each with a specific scope and token budget:

- Layer 1 (always loaded, ~200-500 tokens): This layer contains role identity and domain vocabulary. It is the minimum viable context, always present to route the model to the correct region of its knowledge.
- Layer 2 (task-triggered, ~500-2,000 tokens): This layer includes standard operating procedures (SOPs) and checklists relevant to the current task. It is loaded when the task type is identified, ensuring the model has the necessary procedural knowledge.
- Layer 3 (on-demand, 2,000+ tokens): This layer holds full documentation, detailed examples, and reference material. It is loaded only when specifically needed, preventing unnecessary dilution of attention.
- Layer 4 (compressed): This layer contains summaries of large inputs, such as structured summaries of lengthy documents. It preserves key facts without incurring the quadratic attention cost of loading the full text.

The funnel diagram in the article illustrates how token cost increases with each layer, from narrow permanent context at the top to broad ephemeral compressed context at the bottom. The key insight is that the model does not need to hold everything in context simultaneously; it needs to hold the right things at the right time.

Progressive disclosure is implemented by externalizing plans, artifacts, and reference material to files, and loading them only as needed. This ensures high signal-to-noise ratio and prevents context rot. It also enables aggressive clearing between units of work, as state is preserved externally and can be reloaded cleanly.

The strategy is particularly effective in agentic workflows, where multiple tools, plugins, and MCP servers may be available. By loading only the handful needed for the current task, attention budget is preserved and performance remains high.

## Key Properties

- **Layered Context Stack:** Four layers—permanent, task-triggered, on-demand, compressed—ensure only relevant context is loaded at any time.
- **Token Cost Management:** Token cost increases with each layer; progressive disclosure minimizes unnecessary token spend.
- **Externalized State:** Plans, artifacts, and reference material are saved to files and loaded as needed, enabling aggressive clearing and focused sessions.

## Limitations

Requires disciplined workflow and file management. If externalized state is not maintained or updated, stale information can poison context. Overloading layers can defeat the purpose, leading to attention dilution.

## Example

A developer uses a four-layer stack: always-loaded CLAUDE.md for identity, task-triggered SOPs for current feature, on-demand full documentation for edge cases, and compressed summaries for referencing large documents. Only relevant layers are loaded per task, maintaining high model performance.

## Visual

A funnel diagram shows four layers of context loading, from narrow permanent context at the top (Layer 1) to wide ephemeral compressed context at the bottom (Layer 4), illustrating how token cost increases with each layer.

## Relationship to Other Concepts

- **[[The Context Hygiene Principle]]** — Progressive disclosure is a tactical implementation of the Context Hygiene Principle, ensuring focused context.

## Practical Applications

Progressive disclosure is used in agentic coding workflows, prompt engineering, and multi-tool environments. It enables aggressive clearing, focused sessions, and high-quality outputs by ensuring only relevant context is loaded.

## Sources

- [[The Context Hygiene Principle | 10 Claude Code Principles]] — primary source for this concept
