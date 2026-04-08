---
title: "The Specialized Review Principle | 10 Claude Code Principles"
type: source
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "e07e5051691c4755e2f30694f3fc063b4f6c821a142667606bf4f3c54ed9a4a1"
sources:
  - raw/2026-04-08-the-specialized-review-principle-10-claude-code-principles.md
quality_score: 0
concepts:
  - the-specialized-review-principle
related:
  - "[[The Specialized Review Principle]]"
  - "[[Forge]]"
  - "[[PRISM Persona Science]]"
  - "[[MAST Failure Taxonomy]]"
tier: hot
tags: [prompt-engineering, software-quality, multi-agent-systems, llm, code-review, specialization]
---

# The Specialized Review Principle | 10 Claude Code Principles

## Summary

This article presents the Specialized Review Principle, arguing that code review by a single generalist AI agent trends toward shallow, median-quality feedback, while a panel of specialist agents—each focused on a specific domain with targeted vocabulary—delivers deeper, more effective coverage. It draws on research about vocabulary routing in LLMs, persona length effects, and the dangers of self-evaluation, providing a tactical guide for implementing specialist review panels and highlighting common pitfalls. The principle is situated within the broader context of the 10 Claude Code Principles.

## Key Points

- Generalist AI code reviewers provide shallow, median-quality feedback due to fragmented attention and lack of domain-specific vocabulary.
- Specialist review panels, with agents focused on distinct domains and equipped with precise vocabulary and anti-pattern lists, dramatically improve issue detection rates.
- Research shows that prompt vocabulary routes LLMs to expert knowledge clusters, persona length affects accuracy, and separating code generation from evaluation is crucial.

## Concepts Extracted

- **[[The Specialized Review Principle]]** — The Specialized Review Principle asserts that code review should be performed by a panel of specialist agents, each focused on a single domain (e.g., security, performance, accessibility), rather than by a single generalist. This approach leverages domain-specific vocabulary and anti-patterns to activate expert knowledge clusters in LLMs, resulting in deeper, more accurate, and actionable feedback.

## Entities Mentioned

- **[[Forge]]** — Forge is an open-source system that automates the assembly of specialist agent teams for code review, using vocabulary routing, persona science, and failure taxonomies to optimize review quality.
- **[[PRISM Persona Science]]** — PRISM is a research framework that investigates how persona length and definition affect LLM accuracy and instruction-following, showing that shorter, domain-specific personas yield better results.
- **[[MAST Failure Taxonomy]]** — The MAST Failure Taxonomy is a classification system for common failure modes in multi-agent workflows, such as 'rubber-stamp reviews' where agents approve code without substantive analysis.

## Notable Quotes

> "Code review is too important for a single generalist — orchestrate a panel of specialist agents that each apply domain-specific vocabulary and deliver prioritized, multi-angle feedback." — JD Forsythe
> "Expert vocabulary is the primary lever for output quality — the words in your prompt determine which knowledge the model accesses." — JD Forsythe

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-08-the-specialized-review-principle-10-claude-code-principles.md` |
| Type | article |
| Author | JD Forsythe |
| Date | Unknown |
| URL | https://jdforsythe.github.io/10-principles/principles/specialized-review/ |
