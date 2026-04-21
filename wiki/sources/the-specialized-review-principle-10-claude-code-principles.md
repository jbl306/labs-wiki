---
title: "The Specialized Review Principle | 10 Claude Code Principles"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "d86b1fd9d8d3cb655ece683aef07db27e7b1bc3868b3201d915af52094f217e2"
sources:
  - raw/2026-04-08-the-specialized-review-principle-10-claude-code-principles.md
quality_score: 100
concepts:
  - the-specialized-review-principle
related:
  - "[[The Specialized Review Principle]]"
  - "[[Forge]]"
  - "[[PRISM Persona Science]]"
  - "[[MAST Failure Taxonomy]]"
tier: hot
knowledge_state: executed
tags: [specialization, agentic-workflows, security, accessibility, llm, code-review, prompt-engineering, performance]
---

# The Specialized Review Principle | 10 Claude Code Principles

## Summary

This article introduces the Specialized Review Principle, arguing that code review should be handled by a panel of domain-specific specialist agents rather than a single generalist. It explains the scientific rationale behind specialization, details tactical implementation steps, and contrasts the effectiveness of specialist panels with generalist reviewers. The piece draws on research about vocabulary routing in LLMs, persona science, and evaluation biases, and provides practical guidance for assembling and automating specialist review panels.

## Key Points

- Generalist code review agents tend to provide shallow, median-quality coverage across domains.
- Specialist agents, defined by precise domain vocabulary and brief identities, deliver deep, expert-level feedback.
- Research shows that prompt vocabulary and persona length critically affect LLM output quality and domain activation.

## Concepts Extracted

- **[[The Specialized Review Principle]]** — The Specialized Review Principle asserts that code review should be conducted by a panel of domain-specific specialist agents, each equipped with precise vocabulary and brief identities, rather than a single generalist agent. This approach leverages the strengths of large language models (LLMs) by activating deep, expert-level knowledge clusters through targeted prompts, resulting in higher-quality, actionable feedback across security, performance, accessibility, and domain logic.

## Entities Mentioned

- **[[Forge]]** — Forge is an open-source system designed to automate the assembly of specialist agent teams for code review and other multi-domain tasks. It leverages vocabulary routing, persona science, DeepMind scaling laws, and the MAST failure taxonomy to build panels of domain-specific agents from a goal description. Forge includes a library of 11 domain agents and 3 team templates, enabling rapid deployment of specialist reviewers with precise vocabulary and anti-pattern lists.
- **[[PRISM Persona Science]]** — PRISM Persona Science is a research framework that investigates the impact of persona length and definition on LLM accuracy and instruction-following. It demonstrates that shorter identities (under 50 tokens) cause less degradation in accuracy, while longer personas (100+ tokens) degrade performance on knowledge tasks. PRISM also documents the alignment-accuracy tradeoff, showing that stronger persona definitions improve instruction-following but can reduce factual accuracy.
- **[[MAST Failure Taxonomy]]** — The MAST Failure Taxonomy is a classification system for common failure modes in multi-agent systems, including LLM-based workflows. It documents patterns such as 'rubber-stamp reviews' (FM-3.1), where agents approve code without substantive analysis, leading to false confidence and missed critical issues. The taxonomy provides structural fixes for these failures, such as requiring evidence-backed justification for every review.

## Notable Quotes

> "Code review is too important for a single generalist — orchestrate a panel of specialist agents that each apply domain-specific vocabulary and deliver prioritized, multi-angle feedback." — Fact Sheet
> "Expert vocabulary is the primary lever for output quality — the words in your prompt determine which knowledge the model accesses." — Fact Sheet
> "The agent that wrote the code must not be the agent that reviews it." — Fact Sheet

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-08-the-specialized-review-principle-10-claude-code-principles.md` |
| Type | article |
| Author | jdforsythe |
| Date | Unknown |
| URL | https://jdforsythe.github.io/10-principles/principles/specialized-review/ |
