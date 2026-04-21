---
title: "Context Poisoning in LLM Workflows"
type: concept
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "f746baf27768533a8c0ad9df802594ecb61e45933c725a7cf5ef4e92306fadc3"
sources:
  - raw/2026-04-08-the-context-hygiene-principle-10-claude-code-principles.md
quality_score: 100
concepts:
  - context-poisoning-llm-workflows
related:
  - "[[The Context Hygiene Principle]]"
  - "[[Agent Documentation Hygiene And Migration]]"
  - "[[The Context Hygiene Principle | 10 Claude Code Principles]]"
tier: hot
tags: [context-management, attention-mechanism, llm, documentation-hygiene]
---

# Context Poisoning in LLM Workflows

## Overview

Context poisoning occurs when outdated, irrelevant, or misleading information remains in the model's context window, actively degrading performance. Unlike context bloat, which passively dilutes attention, poisoned context misdirects the model toward obsolete or incorrect patterns.

## How It Works

Context poisoning is a critical failure mode in LLM workflows. When instructions, conventions, or examples in context are no longer current or accurate, the model treats them as authoritative. This can cause the model to re-address resolved issues, follow outdated patterns, or ignore newer, correct instructions.

The mechanism is rooted in the self-attention architecture: every token competes for attention weight, and the model cannot distinguish between current and stale information. If an outdated instruction is weighted strongly, it can override multiple correct ones. This is especially problematic in files like CLAUDE.md or project rules, where old conventions may persist unnoticed.

Context poisoning is worse than context bloat. While bloat dilutes attention passively, poisoning actively misdirects it. The impact can be severe—one stale instruction can cause cascading failures, as illustrated by the example of an outdated line about `Array<T>` causing days of ESLint violations.

Prevention requires regular audits and maintenance of context files. Treating context files like code—reviewing, pruning, and updating them—ensures only current, relevant information is present. Aggressive clearing and externalization of state also help, as each session starts fresh and reads only what is needed.

## Key Properties

- **Active Misdirection:** Poisoned context actively misleads the model, causing it to follow outdated or incorrect instructions.
- **Attention Weight Competition:** Stale tokens compete with current tokens for attention, and may override correct instructions if weighted strongly.
- **Cascading Failure Risk:** One stale instruction can cause widespread errors, requiring extensive debugging and correction.

## Limitations

Requires regular audits and maintenance. If context files are not reviewed, stale instructions can persist and cause failures. The model cannot distinguish between current and outdated information.

## Example

A markdown file contains an outdated instruction about `Array<T>`. The model follows this instruction, causing days of ESLint violations before the issue is traced back to the stale context.

## Visual

No specific diagram, but the article describes the impact of stale context causing cascading failures and misdirection.

## Relationship to Other Concepts

- **[[The Context Hygiene Principle]]** — Context hygiene prevents context poisoning by enforcing regular audits and aggressive clearing.
- **[[Agent Documentation Hygiene And Migration]]** — Documentation hygiene ensures externalized state is current, preventing context poisoning.

## Practical Applications

Regular audits of context files (e.g., CLAUDE.md, project rules) are necessary in agentic workflows and prompt engineering. Developers should treat context files like code, reviewing and pruning them to prevent poisoning.

## Sources

- [[The Context Hygiene Principle | 10 Claude Code Principles]] — primary source for this concept
