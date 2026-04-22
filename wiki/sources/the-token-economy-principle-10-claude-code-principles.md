---
title: "The Token Economy Principle | 10 Claude Code Principles"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "915cc659ae6d5fa84f05a134f6e919e43f7907eedbdf24ee04aca81684538af7"
sources:
  - raw/2026-04-08-the-token-economy-principle-10-claude-code-principles.md
quality_score: 83
concepts:
  - the-token-economy-principle
related:
  - "[[The Token Economy Principle]]"
  - "[[DeepMind]]"
  - "[[Forge]]"
  - "[[jig]]"
tier: hot
knowledge_state: executed
tags: [llm-workflows, token-economy, cost-optimization, multi-agent-systems, context-management]
---

# The Token Economy Principle | 10 Claude Code Principles

## Summary

This article articulates the Token Economy Principle, emphasizing the need to treat tokens, latency, and dollars as first-class engineering constraints in multi-agent AI workflows. Drawing on DeepMind's 2025 research, it demonstrates that adding more agents often results in superlinear cost increases and diminishing or even negative returns in output, and provides actionable guidelines for optimizing agentic workflows. The principle is grounded in empirical data, advocating for measured escalation, adaptive team composition, and strict context management to maximize efficiency and minimize waste.

## Key Points

- Token costs scale superlinearly with agent team size, while output plateaus and can degrade beyond 4 agents.
- DeepMind's research shows most tasks are best handled by a single well-prompted agent; multi-agent setups only benefit decomposable tasks.
- The Token Economy Principle prescribes measurement, optimization, and hard caps before scaling agent teams.

## Concepts Extracted

- **[[The Token Economy Principle]]** — The Token Economy Principle is a foundational guideline for designing and scaling agentic AI workflows, asserting that tokens, latency, and dollars must be treated as primary engineering constraints. It mandates measurement before scaling, optimization before adding agents, and the establishment of hard caps to enforce efficiency. This principle is rooted in empirical research showing that indiscriminate scaling of agent teams leads to superlinear cost increases and often degrades output quality.

## Entities Mentioned

- **[[DeepMind]]** — DeepMind is a leading AI research organization whose 2025 multi-agent scaling research forms the empirical foundation for the Token Economy Principle. Their studies reveal the economic and performance trade-offs in scaling agent teams, showing that coordination overhead grows superlinearly and that most tasks are best handled by a single agent.
- **[[Forge]]** — Forge is an open-source tool that encodes the Token Economy Principle directly into its team assembly and planning logic. It enforces hard caps, applies the 45% threshold, and starts escalation at Level 0, only moving to larger teams when task decomposition and measured data justify the cost.
- **[[jig]]** — jig is an open-source tool (github.com/jdforsythe/jig) that manages project-level configuration files to declare which tools activate per session. This ensures reproducible, minimal context loading, keeping the context window lean and focused on the current task.

## Notable Quotes

> "Treat tokens, latency, and dollars as first-class engineering constraints — measure before scaling, optimize before adding agents, and set hard caps that force efficiency." — Fact Sheet
> "If a single well-prompted agent achieves greater than 45% of optimal performance on a task, adding more agents yields diminishing returns." — DeepMind 2025 research
> "Tokens are not labor. They are attention. And attention does not scale linearly." — Section 1

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-08-the-token-economy-principle-10-claude-code-principles.md` |
| Type | article |
| Author | jdforsythe |
| Date | Unknown |
| URL | https://jdforsythe.github.io/10-principles/principles/token-economy/ |
