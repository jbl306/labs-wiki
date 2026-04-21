---
title: "The Hardening Principle | 10 Claude Code Principles"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "72fa1070a2f27b8e6cbf8d572afb6676f9c39333ee58819acb6b2287c2606f8b"
sources:
  - raw/2026-04-08-the-hardening-principle-10-claude-code-principles.md
quality_score: 100
concepts:
  - the-hardening-principle
related:
  - "[[The Hardening Principle]]"
tier: hot
knowledge_state: executed
tags: [workflow-design, reliability, llm-engineering, automation, agentic-workflows]
---

# The Hardening Principle | 10 Claude Code Principles

## Summary

This article introduces the Hardening Principle, a foundational guideline for designing reliable agentic workflows with LLMs like Claude. It argues that deterministic steps in a workflow should be implemented as hardened code, while LLMs should be reserved for tasks requiring fuzzy reasoning. The author illustrates this with a war story of a meeting transcription pipeline, detailing the pitfalls of relying on LLMs for mechanical execution and offering tactical steps for applying the principle.

## Key Points

- LLMs are excellent for fuzzy reasoning but unreliable for deterministic, mechanical tasks.
- Hardening involves replacing LLM-powered deterministic steps with robust code, improving workflow reliability.
- Silent failures in agentic pipelines are costly; hardened tools fail loudly and predictably.

## Concepts Extracted

- **[[The Hardening Principle]]** — The Hardening Principle is a foundational engineering discipline for agentic workflows involving large language models (LLMs). It asserts that any step in a workflow requiring identical behavior across runs should be implemented as deterministic code, relegating LLMs to tasks demanding fuzzy reasoning. This separation improves reliability, reduces silent failures, and enables genuine trust in automated pipelines.

## Entities Mentioned

No entities mentioned.

## Notable Quotes

> "Every fuzzy LLM step that must behave identically every time must eventually be replaced by a deterministic tool built with Claude’s help." — Fact Sheet
> "The mistake is using a probabilistic system for deterministic work. And the cost of that mistake is not just unreliability — it is the invisible tax of never fully trusting your own tools." — Section 2: The Principle
> "Silent failures are the most expensive failures — hardened tools fail loudly or succeed completely." — Fact Sheet

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-08-the-hardening-principle-10-claude-code-principles.md` |
| Type | article |
| Author | Unknown |
| Date | Unknown |
| URL | https://jdforsythe.github.io/10-principles/principles/hardening/ |
