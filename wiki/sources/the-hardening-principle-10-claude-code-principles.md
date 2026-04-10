---
title: "The Hardening Principle | 10 Claude Code Principles"
type: source
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "07173adf0a23d99d4e19b0760bfd78b6d34d9e6d29a64415b4303d0245e32fa4"
sources:
  - raw/2026-04-08-the-hardening-principle-10-claude-code-principles.md
quality_score: 100
concepts:
  - the-hardening-principle
related:
  - "[[The Hardening Principle]]"
  - "[[Claude]]"
  - "[[ffmpeg]]"
  - "[[Whisper]]"
  - "[[Obsidian]]"
tier: hot
tags: [workflow, llm, engineering, reliability, determinism, automation]
---

# The Hardening Principle | 10 Claude Code Principles

## Summary

This article introduces the Hardening Principle, a foundational engineering discipline for building reliable AI-powered workflows. It argues that any step in an LLM-powered pipeline that must behave identically every time should be replaced by deterministic code, relegating the LLM to tasks requiring fuzzy reasoning and orchestration. The piece provides a detailed war story, scientific rationale, tactical implementation steps, common pitfalls, and measurable impacts of applying this principle.

## Key Points

- LLMs are inherently probabilistic and unreliable for deterministic tasks.
- Production workflows require separating fuzzy (LLM) and mechanical (code) steps.
- Hardening mechanical steps into deterministic tools dramatically improves reliability and trust.

## Concepts Extracted

- **[[The Hardening Principle]]** — The Hardening Principle is an engineering discipline for AI-powered workflows: every step in an LLM-driven pipeline that must behave identically each time should be replaced by deterministic code, with the LLM relegated to fuzzy reasoning and orchestration. This principle addresses the reliability gap between probabilistic LLM outputs and the strict requirements of production systems.

## Entities Mentioned

- **[[Claude]]** — Claude is a large language model (LLM) developed by Anthropic, used for tasks such as summarization, classification, and orchestration in agentic workflows.
- **[[ffmpeg]]** — ffmpeg is a deterministic command-line tool for audio and video processing, used for tasks such as converting audio recordings to different formats.
- **[[Whisper]]** — Whisper is an automatic speech recognition (ASR) system, used to transcribe audio recordings into text.
- **[[Obsidian]]** — Obsidian is a note-taking and knowledge management tool, often used to store structured notes, wikilinks, and project documentation.

## Notable Quotes

> "Every fuzzy LLM step that must behave identically every time must eventually be replaced by a deterministic tool." — J.D. Forsythe
> "LLMs excel at fuzzy reasoning... Production workflows, on the other hand, require steps that behave identically every time." — J.D. Forsythe
> "The reliability gap between these two paradigms is not marginal. It is categorical." — J.D. Forsythe

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-08-the-hardening-principle-10-claude-code-principles.md` |
| Type | article |
| Author | J.D. Forsythe |
| Date | Unknown |
| URL | https://jdforsythe.github.io/10-principles/principles/hardening/ |
