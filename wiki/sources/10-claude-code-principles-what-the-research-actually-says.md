---
title: "10 Claude Code Principles | What the Research Actually Says"
type: source
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "1eed11d2ed454dc89a84d3d3df97738ae3f994a8212ad37e8a16f53652bfb692"
sources:
  - raw/2026-04-08-10-claude-code-principles-what-the-research-actually-says-10.md
quality_score: 86
concepts:
  - the-hardening-principle
  - the-context-hygiene-principle
  - the-living-documentation-principle
  - the-token-economy-principle
related:
  - "[[The Hardening Principle]]"
  - "[[The Context Hygiene Principle]]"
  - "[[The Living Documentation Principle]]"
  - "[[The Token Economy Principle]]"
  - "[[Claude]]"
  - "[[Forge]]"
  - "[[jig]]"
tier: hot
knowledge_state: executed
tags: [best-practices, llm, automation, production, agentic-workflow]
---

# 10 Claude Code Principles | What the Research Actually Says

## Summary

This article introduces 10 evidence-based principles for building production-grade agentic workflows with AI coding tools, challenging much of the prevailing advice in the field. Drawing on peer-reviewed research from leading organizations, it outlines a progression from prototyping with LLMs to hardening workflows, optimizing context, documentation, review, and cost, and finally automating best practices through tooling. The series is structured as a narrative arc, with each principle building on the last to guide developers from intuition-driven to scientifically grounded, reliable AI systems.

## Key Points

- Most common AI coding advice is not just suboptimal but often scientifically disproven.
- The 10 principles are grounded in published research and real-world production experience, not anecdotal best practices.
- Principles cover LLM hardening, context hygiene, living documentation, planning artifacts, institutional memory, specialist review, observability, human review gates, token economy, and tool automation.

## Concepts Extracted

- **[[The Hardening Principle]]** — The Hardening Principle asserts that every probabilistic or 'fuzzy' step in an LLM-driven workflow that must behave identically every time should ultimately be replaced by a deterministic tool. While LLMs excel at prototyping and intent interpretation, their inherent variability makes them unsuitable for production-critical, repeatable tasks.
- **[[The Context Hygiene Principle]]** — The Context Hygiene Principle emphasizes that context—the prompt and supporting information provided to an LLM—is a scarce and valuable resource. Mismanagement of context, such as burying critical information in the middle of long prompts, leads to significant drops in model accuracy due to architectural limitations like the 'Lost in the Middle' effect.
- **[[The Living Documentation Principle]]** — The Living Documentation Principle posits that documentation is not just for humans—it's a critical part of the context LLMs use to generate code and make decisions. Stale or incorrect documentation acts as poisoned context, leading to persistent errors and degraded model performance.
- **[[The Token Economy Principle]]** — The Token Economy Principle recognizes that tokens—the units of computation for LLMs—are a direct cost, both financially and in terms of system efficiency. Scaling up agent teams or prompt complexity without evidence of improved output leads to runaway costs and diminishing returns.

## Entities Mentioned

- **[[Claude]]** — Claude is a large language model (LLM) developed for advanced AI-assisted coding and agentic workflows. It excels at prototyping, intent interpretation, and handling ambiguous or creative tasks, but its probabilistic nature makes it less suitable for deterministic, production-critical steps.
- **[[Forge]]** — Forge is an open-source Claude Code plugin designed to assemble science-backed specialist agent teams for AI workflows. Every design decision in Forge is grounded in published research on effective agentic workflow construction.
- **[[jig]]** — jig is an open-source session profile manager that loads only the tools each project needs for Claude Code workflows. It is designed to enforce context hygiene and minimize unnecessary resource usage.

## Notable Quotes

> "Every fuzzy LLM step that must behave identically every time must eventually be replaced by a deterministic tool." — The Hardening Principle
> "Context is your scarcest resource. Treat it like memory in an embedded system, not disk space on a server." — The Context Hygiene Principle
> "Knowledge without automation decays. Encode your principles into tools that enforce them automatically." — The Toolkit Principle

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-08-10-claude-code-principles-what-the-research-actually-says-10.md` |
| Type | article |
| Author | jdforsythe |
| Date | Unknown |
| URL | https://jdforsythe.github.io/10-principles/overview/ |
