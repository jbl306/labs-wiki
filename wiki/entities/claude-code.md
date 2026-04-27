---
title: "Claude Code"
type: entity
created: 2026-04-10
last_verified: 2026-04-27
source_hash: "sha256:52403a5a6e85eaaaea18a62242944f072dddb53022a49811b1954716bb1f6b68"
sources:
  - raw/2026-04-10-httpsgithubcommidudevautoskills.md
  - raw/2026-04-18-260414228v1pdf.md
  - raw/2026-04-27-260414228v1pdf.md
quality_score: 76
concepts:
  - agentic-loop-architecture-claude-code
  - layered-agentic-architecture-claude-code
  - context-management-compaction-pipeline-claude-code
related:
  - "[[Anthropic]]"
  - "[[OpenClaw]]"
  - "[[Claude Code Skill Summarization]]"
  - "[[Agentic Loop Architecture in Claude Code]]"
  - "[[Layered Agentic Architecture in Claude Code]]"
  - "[[Context Management and Compaction Pipeline in Claude Code]]"
  - "[[Comparative Agent System Architecture: Claude Code vs. OpenClaw]]"
  - "[[Claude Code vs OpenClaw: Architecture Choices Shaped by Deployment Context]]"
tier: hot
tags: [claude-code, agentic-system, coding-agent, safety, context-management, subagents]
---

# Claude Code

## Overview

Claude Code is Anthropic’s agentic coding system for tasks that require more than next-token code completion. In the paper’s framing, it is a production harness that lets a model inspect files, run shell commands, call tools and external services, and keep iterating until a task is resolved.

What makes Claude Code notable in this source is not just the core model loop, but the amount of infrastructure around it: layered permissions, context compaction, extensibility surfaces, subagent isolation, and append-oriented session persistence. The paper treats it as a representative answer to the broader question of how modern coding agents should balance autonomy, safety, reliability, and adaptability.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | 2026 |
| Creator | Anthropic |
| URL | https://code.claude.com/docs/en/how-claude-code-works |
| Status | Active |

## Architecture

The paper decomposes Claude Code into seven functional components: user, interfaces, agent loop, permission system, tools, state and persistence, and execution environment. It then expands that into five subsystem layers—surface, core, safety/action, state, and backend—to show that most of the system’s complexity lives outside the model call itself.

At runtime, the core execution path is the shared `queryLoop()` async generator. Interactive CLI, headless CLI, SDK, and IDE-adjacent surfaces all converge on that loop, which assembles context, calls the model, dispatches tool requests, gathers results, and repeats until the response is text-only.

## Safety and Control Model

Claude Code uses a deny-first posture with human escalation. Permission rules, permission modes, hook interception, an auto-mode ML classifier, shell sandboxing, and non-restoration of session-scoped permissions on resume create a defense-in-depth stack rather than relying on a single boundary.

The paper explicitly contrasts this with alternative safety choices such as container-first isolation or git-rollback-as-safety. That makes Claude Code a useful entity in the wiki not just as a tool, but as a concrete reference architecture for agent harness design.

## Extensibility, Context, and Persistence

The system exposes four extension mechanisms: MCP, plugins, skills, and hooks. It also treats context as the critical bottleneck, using a five-stage compaction pipeline and several supporting tactics such as lazy instruction loading, deferred tool schemas, and summary-only subagent returns.

Persistence is mostly append-oriented JSONL session storage, with sidechain transcripts for subagents and support for resume, fork, and rewind. Together, those choices make Claude Code relevant to our workspace as a high-signal example of how to build agent tooling that remains inspectable under long-horizon use.

## Related Work

- **[[OpenClaw]]** — Contrasting gateway-style agent system used in the paper’s comparative analysis.
- **[[Anthropic]]** — Creator of Claude Code and source of much of the cited safe-agent guidance.
- **[[Claude Code Skill Summarization]]** — Existing wiki concept about downstream tooling built around Claude Code workflows.

## Sources

- [[Dive Into Claude Code: The Design Space of Today’s and Future AI Agent Systems]] — primary architectural source
- [[midudev/autoskills]] — secondary mention through workflow tooling around Claude Code
