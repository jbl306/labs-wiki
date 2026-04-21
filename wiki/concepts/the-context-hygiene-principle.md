---
title: "The Context Hygiene Principle"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "a5ed6720a8e499fec504f09a5c3ce60d6067385dc5b5038864e2b0f8372284f3"
sources:
  - raw/2026-04-19-6372438pdf.md
  - raw/2026-04-08-the-context-hygiene-principle-10-claude-code-principles.md
  - raw/2026-04-08-10-claude-code-principles-what-the-research-actually-says-10.md
quality_score: 100
concepts:
  - the-context-hygiene-principle
related:
  - "[[Positional Encoding]]"
  - "[[10 Claude Code Principles | What the Research Actually Says]]"
tier: hot
tags: [llm, prompt-engineering, context, accuracy]
---

# The Context Hygiene Principle

## Overview

The Context Hygiene Principle emphasizes that context window space in LLMs is a scarce and valuable resource. Proper management of prompt context—especially the placement and freshness of critical information—directly impacts model accuracy and output quality.

## How It Works

LLMs process input as a sequence of tokens within a fixed-size context window. Each token consumes part of the model's finite attention budget, and not all tokens are treated equally due to architectural biases (e.g., the 'Lost in the Middle' effect).

Research (Liu et al., 2024; Wu et al., 2025) demonstrates that when essential information is placed in the middle of a long context, model accuracy drops by over 30%. This is attributed to the transformer architecture's positional encoding and attention mechanisms, which prioritize tokens at the beginning and end of the context window.

Context hygiene involves:
- Placing critical instructions or data at the start or end of the prompt.
- Minimizing irrelevant or outdated content to reduce competition for attention.
- Treating context as a precious, limited resource (like RAM in embedded systems), not as cheap, infinite storage.

Unfocused or bloated context can actively degrade output quality, leading to hallucinations, missed requirements, or inconsistent behavior. The principle advocates for regular audits of prompt structure, aggressive pruning of stale or redundant information, and automated freshness checks for documentation included in context.

Edge cases include tasks that require large amounts of background knowledge, where context compression or retrieval-augmented generation may be necessary. The principle also warns against the temptation to 'just add more instructions,' as this can backfire by diluting the model's focus.

## Key Properties

- **Accuracy Sensitivity:** Model output quality is highly sensitive to the position and relevance of information in the prompt context.
- **Finite Attention Budget:** Every token in the context window competes for limited model attention, making efficient context management critical.
- **Context Entropy:** Stale or irrelevant context acts as noise, reducing the effectiveness of the prompt.

## Limitations

The principle may be challenging to apply in workflows with large, dynamic knowledge bases. Automated context management tools may be required for complex applications. Over-pruning can remove useful background information if not done carefully.

## Example

A code generation prompt places the project’s coding standards at the top, followed by the current task description, ensuring that the model always sees the most important information first.

## Relationship to Other Concepts

- **[[Positional Encoding]]** — Explains the architectural basis for the 'Lost in the Middle' effect in transformer models.

## Practical Applications

Essential for prompt engineering, agentic workflow design, and any application where LLMs must process complex or evolving instructions.

## Sources

- [[10 Claude Code Principles | What the Research Actually Says]] — primary source for this concept
- The Context Hygiene Principle — additional source
- [[6372438.pdf]] — additional source
