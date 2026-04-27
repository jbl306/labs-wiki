---
title: "Layered Agentic Architecture in Claude Code"
type: concept
created: 2026-04-18
last_verified: 2026-04-27
source_hash: "sha256:52403a5a6e85eaaaea18a62242944f072dddb53022a49811b1954716bb1f6b68"
sources:
  - raw/2026-04-18-260414228v1pdf.md
  - raw/2026-04-27-260414228v1pdf.md
quality_score: 59
concepts:
  - layered-agentic-architecture-claude-code
related:
  - "[[Agentic Context Engineering (ACE)]]"
  - "[[Agentic Loop Architecture in Claude Code]]"
  - "[[Agent-Ergonomic Tool Design Principles]]"
  - "[[Dive Into Claude Code: The Design Space of Today’s and Future AI Agent Systems]]"
tier: hot
tags: [agentic-architecture, safety, context-management, extensibility, session-persistence]
---

# Layered Agentic Architecture in Claude Code

## Overview

Claude Code employs a layered agentic architecture that decomposes the system into distinct functional subsystems, each addressing recurring design questions in agentic coding tools. This structure enables robust safety, extensibility, context management, and delegation, supporting both autonomous operation and human oversight.

## How It Works

The architecture of Claude Code is organized into seven high-level components: user, interfaces, agent loop, permission system, tools, state & persistence, and execution environment. All user entry points (CLI, SDK, IDE, browser) converge on a shared agent loop, which orchestrates the iterative cycle of model invocation, tool dispatch, and result collection.

**Agent Loop:** The core of the system is a simple `while-true` cycle. On each turn, the agent assembles context, calls the Claude model, receives responses (including tool-use requests), routes those requests through the permission system, and dispatches approved actions to tools. The agent loop is responsible for maintaining state, managing session identity, and supporting resume, fork, and rewind operations.

**Permission System:** Safety is enforced through a deny-first permission system with seven modes and an ML-based classifier. Permission rules, PreToolUse hooks, auto-mode classifier, and optional shell sandboxing operate in parallel, ensuring defense in depth. Unrecognized actions are escalated to the user, not allowed silently. This separation between reasoning (model) and enforcement (harness) prevents adversarial model behavior from bypassing safety controls.

**Context Management:** The context window is the binding resource constraint. A five-layer compaction pipeline manages context pressure: budget reduction (for tool outputs), snip (temporal depth), microcompact (cache overhead), context collapse (long histories), and auto-compact (semantic compression). Each layer operates at different cost-benefit tradeoffs, running earlier, cheaper layers before costlier ones. Lazy loading of instructions, deferred tool schemas, and summary-only subagent returns further optimize context usage.

**Extensibility:** Four extension mechanisms—MCP servers, plugins, skills, and hooks—allow composable extensibility at different context costs. This enables the system to fit user-specific contexts and evolve over time. Transparent file-based configuration and memory (CLAUDE.md hierarchy, auto memory) provide user-visible, version-controllable files instead of opaque databases.

**Subagent Delegation and Orchestration:** Subagents can be delegated tasks based on criteria, operating in isolation when required. Sidechain transcripts and isolation architecture ensure reliability and safety, preventing subagents from inheriting parent context and permissions unless explicitly allowed.

**Session Persistence:** Append-only durable state records conversation transcripts, supporting auditability, session resumption, forking, and recovery. Graceful recovery mechanisms reserve human attention for unrecoverable situations, silently recovering from errors when possible.

This layered decomposition contrasts with monolithic mechanisms, favoring graduated layering for auditability, operational harness over explicit planning graphs, and values-based judgment over rigid rules. The bulk of the codebase is operational infrastructure, with only a thin layer dedicated to AI decision logic.

## Key Properties

- **Layered Subsystem Decomposition:** System is divided into surface, core, safety/action, state, and backend layers, each with distinct responsibilities.
- **Deny-First Safety Posture:** Permission system defaults to denying actions, escalating to human review, and applies multiple safety layers in parallel.
- **Five-Layer Context Compaction Pipeline:** Context management uses graduated strategies to optimize resource usage and maintain reliability.
- **Composable Extensibility:** Supports MCP, plugins, skills, and hooks for flexible extension at varying context costs.
- **Append-Only Durable State:** Session transcripts are stored in an append-only log, enabling auditability and recovery.

## Limitations

The architecture does not impose explicit planning graphs on the model’s reasoning, lacks a single unified extension mechanism, and does not restore all session-scoped trust-related state across resume. Long-term human capability preservation is not explicitly embedded as a design driver, raising concerns about skill atrophy and codebase coherence.

## Example

When a user submits 'Fix the failing test in auth.test.ts', the agent loop assembles context, calls the model, checks tool-use requests via the permission system, applies context compaction, delegates subagent tasks if needed, and records the session transcript for auditability and recovery.

## Visual

Figure 1 (from the paper) illustrates the high-level system structure: seven functional components connected by a main data flow, with all entry surfaces converging on the agent loop. Figure 2 shows the runtime turn flow, detailing end-to-end execution of a single agentic turn, including context assembly, model call, permission gate, tool dispatch, and compaction.

## Relationship to Other Concepts

- **[[Agentic Context Engineering (ACE)]]** — Both focus on context management and agent loop design for self-improving language models.
- **[[Agent-Ergonomic Tool Design Principles]]** — Shares emphasis on safety, extensibility, and user-centric design in agentic systems.

## Practical Applications

Used in AI-assisted coding tools that autonomously plan, execute shell commands, edit files, and iterate on outputs. Applicable to IDE-integrated assistants, CLI tools, and agent SDKs requiring robust safety, extensibility, and context management.

## Sources

- [[Dive Into Claude Code: The Design Space of Today’s and Future AI Agent Systems]] — primary source for this concept
