---
title: "OpenClaw"
type: entity
created: 2026-04-18
last_verified: 2026-04-27
source_hash: "sha256:52403a5a6e85eaaaea18a62242944f072dddb53022a49811b1954716bb1f6b68"
sources:
  - raw/2026-04-18-260414228v1pdf.md
  - raw/2026-04-27-260414228v1pdf.md
quality_score: 68
concepts:
  - comparative-agent-system-architecture-claude-code-vs-openclaw
related:
  - "[[Claude Code]]"
  - "[[Anthropic]]"
  - "[[Comparative Agent System Architecture: Claude Code vs. OpenClaw]]"
  - "[[Claude Code vs OpenClaw: Architecture Choices Shaped by Deployment Context]]"
  - "[[Dive Into Claude Code: The Design Space of Today’s and Future AI Agent Systems]]"
tier: hot
tags: [openclaw, gateway-agent, agentic-system, multi-agent-orchestration, architecture, safety]
---

# OpenClaw

## Overview

OpenClaw appears in this source as the main comparison point for Claude Code. The paper describes it as an independent open-source AI agent system built as a multi-channel personal assistant gateway rather than as a single CLI-centered coding harness.

That difference in deployment setting matters because the paper uses OpenClaw to show how the same recurring questions—where safety lives, how tools are registered, how context is managed, and how multiple agents are coordinated—can produce materially different system designs.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Role in the Paper

OpenClaw is used as a gateway-oriented contrast case. Where Claude Code centralizes execution around a shared query loop and per-action permissioning, OpenClaw is described as embedding agent runtime inside a gateway control plane with perimeter-level access control and gateway-wide capability registration.

The comparison spans six dimensions: system scope, trust model, runtime and tool orchestration, extension architecture, memory/context management, and multi-agent routing. That makes OpenClaw valuable in the wiki less as a fully specified standalone product record and more as a reference point for architectural trade-offs in agent systems.

## Distinctive Properties

- **Perimeter-level access control** instead of Claude Code’s layered per-action permission checks.
- **Gateway-wide capability registration** instead of Claude Code’s local tool-pool assembly plus MCP/skills/hooks mix.
- **Embedded runtime within a gateway** rather than a single shared CLI/SDK loop.
- **Multi-channel, multi-agent orchestration** as a first-class deployment assumption.

## Related Work

- **[[Claude Code]]** — The paper’s primary system, used as the direct comparison point.
- **[[Comparative Agent System Architecture: Claude Code vs. OpenClaw]]** — Existing concept page distilling the six-dimension contrast.

## Sources

- [[Dive Into Claude Code: The Design Space of Today’s and Future AI Agent Systems]] — primary mention and comparison source
