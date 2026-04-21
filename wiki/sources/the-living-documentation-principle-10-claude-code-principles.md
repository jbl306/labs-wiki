---
title: "The Living Documentation Principle | 10 Claude Code Principles"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "4aaa5cfef62e43e7595210d4bd1e5525656038e25d284f6e446d0e30f6166e9a"
sources:
  - raw/2026-04-08-the-living-documentation-principle-10-claude-code-principles.md
quality_score: 100
concepts:
  - the-living-documentation-principle
related:
  - "[[The Living Documentation Principle]]"
  - "[[Architecture Decision Record (ADR)]]"
  - "[[CLAUDE.md]]"
tier: hot
knowledge_state: executed
tags: [conventions, agentic-workflows, automation, documentation, CI, machine-readable]
---

# The Living Documentation Principle | 10 Claude Code Principles

## Summary

This article articulates the Living Documentation Principle for agentic coding workflows, emphasizing that documentation must be structured, machine-readable, and actively maintained through automation. It details how AI agents treat documentation as operational instructions, making stale or ambiguous docs a vector for systematic errors, and prescribes engineering solutions like CI-driven freshness checks and canonical code examples to ensure reliability.

## Key Points

- Agents treat documentation as literal operational instructions, not just reference material.
- Stale or ambiguous documentation can cause systematic, repeatable errors that mimic model failures.
- Structured, machine-readable documentation with automated freshness checks is essential for reliable agent behavior.

## Concepts Extracted

- **[[The Living Documentation Principle]]** — The Living Documentation Principle asserts that documentation in agentic coding environments must be structured, machine-readable, and continuously maintained through automation. This principle is critical because AI agents interpret documentation as literal operational instructions, making stale or ambiguous docs a source of systematic errors. The approach reframes documentation maintenance as an engineering challenge, solved by structure and CI, rather than a discipline problem.

## Entities Mentioned

- **[[Architecture Decision Record (ADR)]]** — Architecture Decision Records (ADRs) are structured documents that capture the rationale, context, and outcomes behind significant technical decisions in a project. Each ADR records not only what was decided, but why, what alternatives were considered, and who approved the change, providing authoritative guidance for both humans and agents encountering legacy patterns.
- **[[CLAUDE.md]]** — CLAUDE.md is a convention file automatically read by Claude Code agents at the start of every session, containing structured, machine-readable operational instructions. It houses the most critical coding standards, naming conventions, import patterns, and testing requirements, formatted for both human and agent consumption.

## Notable Quotes

> "Documentation must be structured, machine-readable, and automatically checked for freshness — because agents follow stale docs as faithfully as current ones." — Fact Sheet
> "Documentation entropy — the natural tendency of docs to drift out of sync with reality — is not a minor inconvenience in agentic workflows. It is a vector for systematic, repeatable errors that look like model failures but are entirely self-inflicted." — Section 2
> "You do not solve it by telling people to update their docs. You solve it with structure, automation, and CI." — Section 2

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-08-the-living-documentation-principle-10-claude-code-principles.md` |
| Type | article |
| Author | Unknown |
| Date | Unknown |
| URL | https://jdforsythe.github.io/10-principles/principles/living-documentation/ |
