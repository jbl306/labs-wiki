---
title: "Agent-Tool-Memory Loop"
type: concept
created: '2026-04-22'
last_verified: '2026-04-22'
sources:
  - raw/2026-04-12-httpsgithubcomhkudsautoagent.md
quality_score: 85
concepts:
  - agent-tool-memory-loop
related:
  - "[[HKUDS/AutoAgent]]"
  - "[[AutoAgent Framework Research]]"
  - "[[Natural Language Driven Agent Building]]"
tier: warm
tags: [agent-loop, tool-calling, memory, iterative-refinement, agent-architecture]
---

# Agent-Tool-Memory Loop

## Overview

The agent-tool-memory loop is a fundamental architectural pattern for autonomous agents: receive task → plan → call tool → store result in memory → iterate. The agent maintains a memory of prior actions and observations, uses tools to interact with the environment, and iteratively refines its plan based on feedback. This pattern is generic enough to underpin many agent frameworks (AutoAgent, ReAct, Reflexion, etc.) and is the core execution model for agents that must act, observe, and adapt.

## How It Works

The loop proceeds in discrete steps:

1. **Receive task** — The agent is given a high-level goal (e.g., "Research quantum computing and write a report").

2. **Plan** — The agent generates a plan: a sequence of actions (tool calls) to achieve the goal. This may be a single-step plan ("call search tool") or a multi-step plan ("search → read → summarize → write").

3. **Call tool** — The agent executes the next action in the plan by invoking a tool (e.g., `search("quantum computing")`, `read_file("report.md")`, `write_file("summary.txt", ...)`). Tools are the agent's interface to the environment (file system, web, databases, etc.).

4. **Observe result** — The tool returns a result (e.g., search results, file contents, success/failure status). The agent observes this result and updates its understanding of the environment.

5. **Store in memory** — The agent stores the action and result in a memory structure (e.g., a conversation history, a working memory buffer, or a structured knowledge base). This memory is used to:
   - Track what has been done (avoid redundant tool calls)
   - Inform future planning (e.g., "I already searched for X, so I should refine the query")
   - Provide context for the next iteration (e.g., "The last file read contained Y")

6. **Iterate** — The agent decides whether to:
   - **Continue** — Re-plan based on the new memory state and execute the next action
   - **Stop** — The goal is achieved, or the agent detects a failure/loop

This loop repeats until the agent reaches a stopping condition (goal satisfied, max iterations, detected failure, etc.).

**Key design choices:**

- **Memory structure** — The memory can be:
  - A flat list of `(action, result)` pairs (simple, used in ReAct)
  - A structured knowledge graph (e.g., AutoAgent's self-modifying agent scaffold)
  - A hierarchical working memory (e.g., short-term + long-term buffers)

- **Planning strategy** — The agent can:
  - **Reactive** — Generate one action at a time based on the current memory state (ReAct pattern)
  - **Proactive** — Generate a full multi-step plan upfront, then execute it step-by-step (AutoAgent's workflow editor)
  - **Hybrid** — Generate a coarse plan, then refine it at each step based on observations

- **Tool failure handling** — If a tool call fails (e.g., file not found, API error), the agent must:
  - **Retry** — Try the same tool again (with modified arguments)
  - **Re-plan** — Generate a new plan that avoids the failed tool
  - **Escalate** — Ask the user for help or halt

- **Loop termination** — The agent must detect:
  - **Success** — The goal is achieved (e.g., report written, task completed)
  - **Failure** — The agent is stuck (e.g., tool call fails repeatedly, no valid actions remain)
  - **Loop** — The agent is repeating the same actions indefinitely (e.g., calling the same tool with the same arguments)

**AutoAgent's variant:**

In AutoAgent, the loop is wrapped in a self-modifying envelope: the agent can generate new tools (by writing Python code), add them to its tool library, and call them in subsequent iterations. This enables "tool bootstrapping" where simple tools are composed into more complex ones:

```
Task → Plan → [No tool exists for this sub-task]
            → Generate tool code → Test tool → Add to library
            → Re-plan with new tool → Call new tool → Observe → Store
```

This extends the basic loop with a **meta-loop** where the tool set itself evolves during execution.

## Key Properties

- **Iterative refinement** — The agent improves its plan at each step based on new observations.
- **Memory-grounded** — All planning and tool calls are informed by the accumulated memory of prior actions.
- **Tool-mediated** — The agent interacts with the environment exclusively through tools; no direct access to files, APIs, etc.
- **Failure-aware** — The agent must handle tool failures and avoid infinite loops.

## Trade-offs

**Benefits:**
- **Flexibility** — The agent can adapt its plan based on runtime observations (e.g., if a search returns no results, try a different query).
- **Composability** — Complex tasks are decomposed into sequences of simple tool calls.
- **Transparency** — The memory trace (action log) makes the agent's reasoning inspectable and debuggable.

**Drawbacks:**
- **Inefficiency** — Reactive agents may call tools redundantly or explore dead-ends before converging on a solution.
- **Memory overhead** — Storing the full action history can consume significant token budget (for LLM-based agents) or RAM (for stateful agents).
- **Loop detection is hard** — Detecting whether the agent is stuck requires heuristics (e.g., "same action called 3 times in a row") that may mis-classify valid retries as loops.

## Example

**Task:** "Research quantum computing and write a summary."

**Loop iterations:**

1. **Plan:** Call `search("quantum computing")`
2. **Tool:** `search("quantum computing")` → returns 10 results
3. **Memory:** Store "searched for quantum computing, got 10 results"
4. **Plan:** Call `read_url(results[0])`
5. **Tool:** `read_url(...)` → returns article text
6. **Memory:** Store "read article from URL X, content: ..."
7. **Plan:** Call `summarize(article_text)`
8. **Tool:** `summarize(...)` → returns summary
9. **Memory:** Store "summarized article, result: ..."
10. **Plan:** Call `write_file("summary.md", summary)`
11. **Tool:** `write_file(...)` → success
12. **Memory:** Store "wrote summary to summary.md"
13. **Stop:** Goal achieved

**Pseudocode:**

```python
memory = []
plan = generate_plan(task)

for step in plan:
    tool_result = call_tool(step.tool, step.args)
    memory.append((step.tool, step.args, tool_result))
    
    if is_goal_achieved(memory):
        break
    
    if is_loop_detected(memory):
        re_plan(task, memory)
    
    if is_tool_failure(tool_result):
        handle_failure(step, tool_result, memory)
    
    plan = refine_plan(plan, memory)
```

## Relationship to Other Concepts

- **[[AutoAgent Framework Research]]** — AutoAgent implements this loop with a self-modifying tool library.
- **[[HKUDS/AutoAgent]]** — The upstream project that uses this pattern for zero-code agent creation.
- **[[Natural Language Driven Agent Building]]** — The agent-tool-memory loop is the runtime execution model for agents created via natural language descriptions.

## Practical Applications

The agent-tool-memory loop is used for:
- **Research agents** — Agents that search, read, and synthesize information (e.g., AutoAgent's Deep Research mode).
- **File manipulation** — Agents that read, write, and transform files (e.g., code generation, data processing).
- **API orchestration** — Agents that call multiple APIs in sequence to achieve a goal (e.g., booking a flight: search → select → book → confirm).
- **Code generation** — Agents that generate code, test it, observe failures, and iterate (e.g., AutoAgent's self-play customization).
- **Interactive debugging** — Agents that inspect program state, hypothesize bugs, and test fixes iteratively.

Specific examples:
- **AutoAgent Deep Research** — Searches web, reads articles, synthesizes results, writes reports.
- **GitHub Copilot CLI** — Plans shell commands, executes them, observes output, refines plan.
- **ReAct agents** — Reason about what to do, act via tool calls, observe results, repeat.

## Sources

- [[HKUDS/AutoAgent]] — implements the agent-tool-memory loop with self-modifying tools
