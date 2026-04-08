---
title: "The Living Documentation Principle | 10 Claude Code Principles"
type: source
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "5f635969f0ddd587b6295138d202654a9ab042a49563b6eeaa3f303248112b44"
sources:
  - raw/2026-04-08-the-living-documentation-principle-10-claude-code-principles.md
quality_score: 0
concepts:
  - the-living-documentation-principle
related:
  - "[[The Living Documentation Principle]]"
  - "[[Claude]]"
  - "[[Architecture Decision Record (ADR)]]"
tier: hot
tags: [continuous-integration, llm-pattern-matching, agentic-workflows, documentation]
---

# The Living Documentation Principle | 10 Claude Code Principles

## Summary

This article introduces the Living Documentation Principle, emphasizing the necessity of structured, machine-readable, and continuously verified documentation in environments where AI agents consume codebase instructions. It details the risks of stale documentation, the science behind LLM pattern-matching, and provides tactical steps for implementing robust, agent-friendly documentation practices. The principle reframes documentation maintenance as an engineering problem, advocating for automation and structure to prevent systematic agent errors.

## Key Points

- Stale documentation can cause systematic, hard-to-detect errors in agentic workflows.
- LLMs pattern-match against examples and structure more reliably than they follow abstract rules.
- Automated freshness checks and structured, machine-readable formats are essential for reliable agent behavior.

## Concepts Extracted

- **[[The Living Documentation Principle]]** — The Living Documentation Principle asserts that documentation must be structured, machine-readable, and automatically checked for freshness, especially in codebases where AI agents use documentation as operational instructions. This principle reframes documentation as active context for both humans and agents, emphasizing that stale or ambiguous docs can directly cause systematic errors in agentic workflows.

## Entities Mentioned

- **[[Claude]]** — Claude is a large language model developed by Anthropic, designed to assist with a variety of tasks including code generation, documentation parsing, and agentic workflows. It is specifically tuned to pay attention to structured documentation formats.
- **[[Architecture Decision Record (ADR)]]** — An Architecture Decision Record (ADR) is a structured document that captures significant architectural decisions, their rationale, alternatives considered, and the context in which they were made.

## Notable Quotes

> "Documentation is context. Stale documentation is poisoned context." — J.D. Forsythe
> "The Living Documentation Principle treats this as an engineering problem, not a discipline problem. You do not solve it by telling people to update their docs. You solve it with structure, automation, and CI." — J.D. Forsythe
> "LLMs are fundamentally pattern-matching engines. They were trained on sequence prediction — given this input, predict the most likely next token." — J.D. Forsythe

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-08-the-living-documentation-principle-10-claude-code-principles.md` |
| Type | article |
| Author | J.D. Forsythe |
| Date | Unknown |
| URL | https://jdforsythe.github.io/10-principles/principles/living-documentation/ |
