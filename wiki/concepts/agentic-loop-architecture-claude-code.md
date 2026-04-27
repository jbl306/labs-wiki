---
title: "Agentic Loop Architecture in Claude Code"
type: concept
created: 2026-04-27
last_verified: 2026-04-27
source_hash: "sha256:52403a5a6e85eaaaea18a62242944f072dddb53022a49811b1954716bb1f6b68"
sources:
  - raw/2026-04-27-260414228v1pdf.md
quality_score: 84
related:
  - "[[Layered Agentic Architecture in Claude Code]]"
  - "[[Context Management and Compaction Pipeline in Claude Code]]"
  - "[[Parallel Subagent Stream Implementation]]"
  - "[[Worktree-Based Subagent-Driven Development]]"
tier: hot
tags: [claude-code, agentic-loop, tool-orchestration, streaming-execution, coding-agents]
---

# Agentic Loop Architecture in Claude Code

## Overview

The agentic loop in Claude Code is the shared execution cycle that turns a model response into a long-horizon coding workflow. Instead of embedding a planner graph, workflow DSL, or explicit task machine into the product, the system uses a relatively small reactive loop and pushes most of the sophistication into the surrounding harness: permissions, tool dispatch, context shaping, persistence, and recovery.

This concept matters because it shows a concrete answer to a recurring agent-design question: should a production coding agent be organized around elaborate scaffolding, or around a compact control loop surrounded by deterministic infrastructure? The paper argues that Claude Code chooses the latter, and that choice shapes nearly every other subsystem.

## How It Works

At the center of the system is `queryLoop()`, an async generator that is shared across the interactive CLI, headless CLI, SDK, and IDE-adjacent surfaces. The loop is not just a convenience wrapper; it is the execution engine that normalizes otherwise different entry points into the same runtime semantics. A user request enters through one of those surfaces, but once the message is handed to the loop the rest of the lifecycle is uniform: assemble context, call the model, inspect tool requests, run tools, collect results, and continue until the response contains no further tool use.

The paper describes the loop as a fixed-sequence pipeline. First, settings are resolved and immutable configuration is unpacked. Then a mutable state object is initialized to hold the conversation messages, tool context, compaction bookkeeping, and recovery counters that will persist across iterations. Before the model is called, the loop reconstructs the conversation slice after the most recent compact boundary, ensuring that already-compacted history stays represented by summaries instead of by the full original transcript. This preserves continuity without replaying the entire session verbatim.

Once the message set is assembled, five pre-model context shapers run in sequence. These are not incidental helpers; they are an essential part of the loop contract because Claude Code treats context pressure as the binding systems constraint. The shapers are **budget reduction**, **snip**, **microcompact**, **context collapse**, and **auto-compact**. They progress from cheaper, narrower interventions to broader and more expensive summarization. By the time the model is finally called, the loop has already transformed the raw working set into the smallest version that can still support coherent reasoning.

The model call itself is performed as a streaming operation. The loop yields typed events while the response is arriving, which lets the UI render progress in real time while preserving a single logical execution path. If the model emits `tool_use` blocks, those blocks do not execute directly. They flow outward into the surrounding harness, where permission checks and tool orchestration take over. This separation is the security-critical property of the design: the model can propose actions, but it cannot bypass the harness that validates and executes them.

Tool execution is also integrated into the loop in a deliberately structured way. Claude Code uses a primary streaming path that can begin executing tools while the response is still being received, reducing latency for multi-tool turns. At the same time, it classifies tools as concurrent-safe or exclusive. Read-only operations can run in parallel, but state-mutating operations such as shell commands are serialized. The executor maintains ordered output even when execution is concurrent so the model sees results in the same order that it requested them. This is a subtle but important systems property: concurrency is exploited for throughput, but the conversational protocol remains deterministic.

The loop also coordinates failure and recovery. The paper highlights mechanisms such as sibling abort controllers for streaming tool execution, progress-available signals for result collection, compact boundaries for reconstructing history, and a family of continue points that overwrite state in whole-object assignments rather than accumulating ad hoc mutations. These choices reduce the number of places where partial state can become inconsistent. In practical terms, the loop is designed less like a chatbot turn handler and more like a resilient transaction manager for model-mediated work.

Another crucial feature is what the loop does **not** do. It does not impose an explicit planning graph on the model. It does not perform tree search over alternative action sequences. It does not hardcode a single planner-executor state machine. Instead, it keeps a ReAct-style iterative pattern: the model reasons, requests tools, receives grounded results, and continues. The paper contrasts this with graph-routed systems such as LangGraph and search-heavy alternatives such as tree-search agents. Claude Code trades some completeness and search breadth for implementation simplicity, lower orchestration overhead, and a tighter fit with streaming human-facing tooling.

Finally, the loop connects to subagent execution without ceasing to be the main primitive. Subagents are not a second architecture; they are spawned back through the same tool factory and re-enter the same query-loop pattern with isolated context. Their full transcripts stay in sidechain storage, and only summaries return to the parent. That means the main loop remains the universal computational unit even when work is delegated.

## Key Properties

- **Shared engine across surfaces:** Interactive CLI, headless mode, SDK, and other front ends all converge on the same core loop.
- **Harness-model separation:** The model proposes tool calls, but the harness enforces permissions, sandboxing, and execution.
- **Streaming by default:** Responses and tool execution can stream incrementally instead of waiting for an entire turn to finish.
- **Concurrent reads, serialized writes:** Safe reads can overlap, while shell-like or stateful actions are kept ordered.
- **Context-aware by construction:** The loop always runs after compaction shapers, so context management is part of control flow rather than an optional addon.

## Limitations

The reactive loop does not search over multiple full trajectories before committing to one, so it can miss better branches that a more exploratory planner might find. It also depends heavily on the quality of the surrounding harness; a simple loop without strong context management, permissions, and recovery would be brittle. Finally, because the model still owns high-level reasoning, the system inherits model-level issues such as poor strategic choices or premature task completion claims.

## Examples

When the user asks Claude Code to fix a failing test, the loop can be thought of like this:

```python
state = initialize_state(user_request)
while True:
    messages = assemble_messages_after_compact_boundary(state)
    messages = apply_context_shapers(messages)
    response = call_model(messages, tools=available_tools)
    if not response.tool_uses:
        break
    approved = permission_gate(response.tool_uses)
    results = run_tools_streaming(approved)
    state = merge_results_back_into_state(state, results)
```

The important detail is that each step in that pseudocode maps to real surrounding infrastructure rather than to free-form model behavior.

## Practical Applications

This concept is useful when designing coding agents, ops agents, or long-running research assistants that need to stay responsive without becoming opaque. A compact shared loop plus strong harnessing is especially attractive when you want streaming UX, tool interoperability, human interrupts, resumable sessions, and deterministic safety boundaries. It is also directly relevant to this workspace because it explains why Claude Code-like systems can feel simple on the surface while still requiring deep investment in context hygiene, permission models, and transcript durability.

## Related Concepts

- **[[Layered Agentic Architecture in Claude Code]]** — Shows how the loop sits inside a larger five-layer subsystem structure.
- **[[Context Management and Compaction Pipeline in Claude Code]]** — Details the pre-model shaping stages the loop depends on every turn.
- **[[Parallel Subagent Stream Implementation]]** — Related to the loop’s concurrent execution and ordered result handling.
- **[[Worktree-Based Subagent-Driven Development]]** — Related example of isolated delegated work within agentic coding systems.

## Sources

- [[Dive Into Claude Code: The Design Space of Today’s and Future AI Agent Systems]] — primary source for the control-flow, dispatch, and compaction details
