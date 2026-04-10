---
title: "The Token Economy Principle | 10 Claude Code Principles"
type: source
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "f6933d2a95acf0b4917f8621a07e5686d09e25f2c5e930389f1d70533135e80c"
sources:
  - raw/2026-04-08-the-token-economy-principle-10-claude-code-principles.md
quality_score: 100
concepts:
  - the-token-economy-principle
related:
  - "[[The Token Economy Principle]]"
  - "[[DeepMind]]"
  - "[[Forge]]"
  - "[[jig]]"
tier: hot
tags: [cost-optimization, token-economy, engineering-principles, ai-workflows, multi-agent]
---

# The Token Economy Principle | 10 Claude Code Principles

## Summary

This article presents the Token Economy Principle, a research-backed guideline for managing token usage, cost, and efficiency in multi-agent AI workflows. Drawing on DeepMind's 2025 multi-agent scaling research, it demonstrates that adding more agents often leads to superlinear cost increases and diminishing or even negative returns in output. The principle advocates for treating tokens, latency, and dollars as first-class engineering constraints, starting with single-agent baselines, and escalating team size only when measured data justifies it.

## Key Points

- Token costs scale superlinearly with team size, while output plateaus and can degrade beyond 4 agents.
- Most tasks are best handled by a single well-prompted agent with appropriate tools; multi-agent setups should be justified by measurement.
- Coordination overhead and context loading costs are major sources of inefficiency, and adaptive team composition outperforms static teams.

## Concepts Extracted

- **[[The Token Economy Principle]]** — The Token Economy Principle is a foundational guideline for AI engineering that treats tokens, latency, and dollars as first-class constraints in the design and operation of multi-agent workflows. It asserts that every workflow should begin with measurement, prioritize optimization, and only scale agent teams when justified by empirical data. This principle is critical for controlling costs, maximizing output efficiency, and avoiding the common pitfall of over-provisioned, underperforming agent teams.

## Entities Mentioned

- **[[DeepMind]]** — DeepMind is an AI research organization whose 2025 multi-agent scaling research underpins the Token Economy Principle. Their studies provide empirical data on how cost and output scale with agent team size in AI workflows.
- **[[Forge]]** — Forge is a tool that encodes the Token Economy Principle into workflow automation, ensuring that agent team size and token budgets are justified by measured data. It enforces the cascade escalation model and hard constraints on agent usage.
- **[[jig]]** — jig is a configuration tool that manages context loading in AI workflows, ensuring that only the necessary tools and skills are loaded per task. This minimizes token spend on unused context and enforces reproducibility.

## Notable Quotes

> "Treat tokens, latency, and dollars as first-class engineering constraints — measure before scaling, optimize before adding agents, and set hard caps that force efficiency." — JD Forsythe
> "The instinct to throw more agents at a problem feels right — more workers, more output. But tokens are not labor. They are attention. And attention does not scale linearly." — JD Forsythe

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-08-the-token-economy-principle-10-claude-code-principles.md` |
| Type | article |
| Author | JD Forsythe |
| Date | Unknown |
| URL | https://jdforsythe.github.io/10-principles/principles/token-economy/ |
