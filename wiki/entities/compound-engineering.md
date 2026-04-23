---
title: Compound Engineering
type: entity
created: '2026-04-23'
last_verified: '2026-04-23'
source_hash: 47dca59f5e85d3b968b39b0119e3e03fe82d3bc935cfa91eaa1b03d60cf1aeeb
sources:
  - raw/2026-04-23-httpsgithubcomeveryinccompound-engineering-plugin.md
concepts:
  - compound-engineering-workflow
  - cross-platform-agent-plugin-conversion
related:
  - "[[Claude Code]]"
  - "[[Copilot CLI]]"
  - "[[GitHub Copilot]]"
  - "[[OpenCode]]"
tier: hot
tags:
  - ai-agents
  - code-review
  - knowledge-management
  - plugin
  - workflow-automation
---

# Compound Engineering

## Overview

Compound Engineering is EveryInc's workflow system and plugin suite for AI-assisted software development. It packages the idea that engineering leverage comes primarily from better planning, sharper review, and durable learning capture, then turns that idea into installable agent tooling for platforms such as Claude Code, Copilot CLI, Codex, OpenCode, Pi, Gemini CLI, and Kiro.

In practice, the project is both a methodology and a distribution artifact. The methodology is the repeating loop of ideation, brainstorming, planning, execution or debugging, specialist review, and post-hoc compounding of lessons. The artifact is the GitHub repository and Bun CLI that ship the corresponding skills, agents, manifests, converters, and cleanup logic needed to run that loop across different agent runtimes.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Workflow framework & plugin suite |
| Created | 2025-10-09 |
| Creator | EveryInc (plugin package authored by Kieran Klaassen) |
| URL | https://github.com/EveryInc/compound-engineering-plugin |
| Status | Active |

## Core Workflow

The source README states the central thesis plainly: each unit of engineering work should make subsequent units easier rather than harder. Compound Engineering operationalizes that with a standard chain: optional ideation, interactive brainstorming, explicit planning, guided execution, specialist review, and deliberate knowledge capture. The root README even frames the method as an 80/20 split where planning and review produce most of the leverage.

That makes Compound Engineering more than a bag of prompts. The repo encodes named entry points for each phase (`/ce-brainstorm`, `/ce-plan`, `/ce-work`, `/ce-debug`, `/ce-code-review`, `/ce-compound`) and treats the documents produced in those phases as durable assets rather than disposable chat byproducts.

## Distribution Model

Compound Engineering is distributed as a Claude-compatible marketplace/plugin repo plus a Bun CLI named `compound-plugin`. Native plugin install is documented for Claude Code, Copilot CLI, Cursor, Droid, and Qwen Code. Converter-backed or hybrid flows cover Codex, OpenCode, Pi, Gemini CLI, and Kiro.

Internally, the repository parses Claude plugin manifests and Markdown-defined components, converts them to target-specific bundles, then writes them to stable host-specific locations. That portability is one of the project's strongest practical qualities: the same workflow system can travel across multiple agent environments without re-authoring the skills from scratch.

## Review and Knowledge Capture

Compound Engineering's most distinctive operational surface is its review layer. The plugin README lists specialist reviewer agents for security, performance, correctness, testing, data migrations, API contracts, project standards, and adversarial failure probing, aligning the project closely with [[The Specialized Review Principle]] even though the repo presents that idea as tooling rather than theory.

The second distinctive surface is its memory discipline. `/ce-compound` and `/ce-compound-refresh` exist specifically so teams do not keep relearning the same lesson in isolated sessions. In that sense, Compound Engineering is as much about institutional memory as it is about code generation.

## Related Entities

- **[[Claude Code]]** — the native plugin format and one of the primary host runtimes.
- **[[Copilot CLI]]** — a documented native install target for the plugin.
- **[[GitHub Copilot]]** — the broader ecosystem that includes the plugin-compatible Copilot surfaces.
- **[[OpenCode]]** — one of the converter-backed target runtimes written by the Bun CLI.

## Sources

- [[EveryInc/compound-engineering-plugin]] — repository source and primary technical reference
