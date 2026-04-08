---
title: "10 Claude Code Principles | What the Research Actually Says"
type: source
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "a5ed6720a8e499fec504f09a5c3ce60d6067385dc5b5038864e2b0f8372284f3"
sources:
  - raw/2026-04-08-10-claude-code-principles-what-the-research-actually-says-10.md
quality_score: 0
concepts:
  - the-hardening-principle
  - the-context-hygiene-principle
  - the-disposable-blueprint-principle
  - the-token-economy-principle
related:
  - "[[The Hardening Principle]]"
  - "[[The Context Hygiene Principle]]"
  - "[[The Disposable Blueprint Principle]]"
  - "[[The Token Economy Principle]]"
  - "[[Forge]]"
  - "[[jig]]"
tier: hot
tags: [prompt-engineering, agentic-workflows, planning, llm, production, automation, cost]
---

# 10 Claude Code Principles | What the Research Actually Says

## Summary

This article introduces ten evidence-based principles for building reliable, production-grade agentic coding workflows with LLMs, challenging much of the popular advice in the AI coding community. Drawing on peer-reviewed research from leading institutions, the series presents actionable guidelines for prompt engineering, agent orchestration, documentation, and workflow automation. Each principle is grounded in empirical findings and is designed to address common failure modes and inefficiencies in LLM-powered development.

## Key Points

- Most mainstream AI coding advice is empirically incorrect and can lead to fragile, inefficient workflows.
- The ten principles are distilled from peer-reviewed research and focus on reliability, context management, documentation, planning, review, observability, governance, and automation.
- The series advocates for a scientific, evidence-based approach to agentic workflow design, moving away from intuition-driven ('vibes-based') practices.

## Concepts Extracted

- **[[The Hardening Principle]]** — The Hardening Principle asserts that every non-deterministic LLM step in a workflow that must behave identically each time should eventually be replaced by a deterministic tool. LLMs excel at prototyping and handling ambiguity, but their probabilistic nature makes them unreliable for production-critical steps.
- **[[The Context Hygiene Principle]]** — The Context Hygiene Principle emphasizes that context window space in LLMs is a scarce and valuable resource. Proper management of prompt context—especially the placement and freshness of critical information—directly impacts model accuracy and output quality.
- **[[The Disposable Blueprint Principle]]** — The Disposable Blueprint Principle advocates for always externalizing plans as versioned artifacts before implementation and being willing to discard and revise them as needed. Structured planning artifacts reduce errors and enable reproducible, auditable workflows.
- **[[The Token Economy Principle]]** — The Token Economy Principle treats tokens as a finite, costly resource and advocates for efficient agent team design. Empirical research shows that adding more agents quickly leads to diminishing returns and runaway costs.

## Entities Mentioned

- **[[Forge]]** — Forge is an open-source Claude Code plugin designed to assemble science-backed specialist agent teams for production-grade workflows. It encodes the ten Claude Code Principles into actionable automation.
- **[[jig]]** — jig is an open-source session profile manager that loads only the tools each project needs, supporting context hygiene and workflow specialization. It is designed to enforce the Claude Code Principles in daily development.

## Notable Quotes

> "Most AI coding advice is wrong. Not 'slightly suboptimal' wrong — measurably, scientifically, provably wrong." — JD Forsythe
> "The Hardening Principle says: use the LLM to prototype, then harden the deterministic parts into real tools." — JD Forsythe
> "Context is your scarcest resource. Treat it like memory in an embedded system, not disk space on a server." — JD Forsythe

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-08-10-claude-code-principles-what-the-research-actually-says-10.md` |
| Type | guide |
| Author | JD Forsythe |
| Date | Unknown |
| URL | https://jdforsythe.github.io/10-principles/overview/ |
