---
title: "Agent-Ergonomic Tool Design Principles"
type: concept
created: 2026-04-13
last_verified: 2026-04-13
source_hash: "c4e8332bb539477ec966d1695a93bae4bf06a12c0a260303fe393c7f68646500"
sources:
  - raw/2026-04-13-httpsgithubcomchromedevtoolschrome-devtools-mcp.md
quality_score: 76
concepts:
  - agent-ergonomic-tool-design-principles
related:
  - "[[AXI Design Principles for Agent-Ergonomic CLI Tools]]"
  - "[[ChromeDevTools/chrome-devtools-mcp]]"
tier: hot
tags: [agent-ergonomics, design-principles, token-efficiency, composability, error-handling, interoperability]
---

# Agent-Ergonomic Tool Design Principles

## Overview

Agent-ergonomic tool design principles are guidelines for building tools that are easily usable by coding agents and humans. They emphasize interoperability, composability, token efficiency, actionable errors, and progressive complexity, ensuring tools are robust, flexible, and optimized for agent workflows.

## How It Works

The principles outlined for Chrome DevTools MCP serve as a blueprint for designing agentic tools that maximize usability and reliability. The first principle, Agent-Agnostic API, mandates the use of standards like MCP, avoiding lock-in to a single LLM or agent platform. This ensures broad compatibility and future-proofing.

Token-Optimized design focuses on returning concise, semantic summaries rather than verbose data dumps. For example, reporting 'LCP was 3.2s' instead of streaming tens of thousands of lines of JSON. Heavy assets (screenshots, traces, videos) are referenced by file paths or URIs, not streamed, to minimize token usage and facilitate efficient retrieval.

Small, Deterministic Blocks encourage the creation of composable, granular tools (such as Click, Screenshot) rather than monolithic, opaque actions. This allows agents to build complex workflows from simple primitives, improving reliability and interpretability.

Self-Healing Errors require tools to return actionable error messages that include context and potential fixes. This supports both agent self-repair and human intervention, reducing workflow interruptions and improving debugging efficiency.

Human-Agent Collaboration is achieved by ensuring outputs are readable by both machines (structured data) and humans (summaries). This dual-format approach enables seamless handoffs and collaborative troubleshooting.

Progressive Complexity means tools are simple by default, offering high-level actions for common tasks, but exposing advanced arguments for power users and agents needing fine-grained control. This balances accessibility and power.

Reference Over Value dictates that heavy assets should be referenced, not streamed, unless the client supports direct handling (e.g., built-in image display). This principle prevents unnecessary token consumption and supports scalable workflows.

## Key Properties

- **Interoperability:** Tools are designed to work across multiple agents and platforms via standardized APIs.
- **Token Efficiency:** Outputs are optimized for minimal token usage, referencing heavy assets instead of streaming them.
- **Composability:** Tools are granular and deterministic, enabling agents to build complex workflows from simple actions.
- **Actionable Error Handling:** Errors include context and potential fixes, supporting self-healing and collaborative debugging.
- **Dual-Format Output:** Outputs are structured for machine parsing and summarized for human readability.
- **Progressive Complexity:** Tools offer simple defaults with advanced options for power users.

## Limitations

Requires careful implementation to avoid over-complication or excessive abstraction. Some principles (e.g., reference over value) may not be applicable in all agent environments. Token optimization can conflict with detailed reporting needs. Not all agent platforms support advanced arguments or asset referencing.

## Example

A tool that analyzes performance returns:

- Summary: 'LCP was 3.2s'
- Asset reference: '/tmp/trace-123.json'

A click tool:

```json
{
  "tool": "click",
  "uid": "element-uid-123"
}
```

If an error occurs:

```json
{
  "error": "Element not found",
  "context": "UID: element-uid-123",
  "potential_fix": "Check if the element exists in the latest snapshot."
}
```

## Visual

No diagrams are present, but the design principles are listed in bullet points in the docs/design-principles.md file.

## Relationship to Other Concepts

- **[[AXI Design Principles for Agent-Ergonomic CLI Tools]]** — Both sets of principles guide agentic tool design for ergonomic, reliable, and composable interfaces.

## Practical Applications

Used in the design of agentic tools for browser automation, debugging, and performance analysis. Guides developers building agent plugins, MCP servers, and CLI interfaces to maximize usability and reliability for both agents and humans.

## Sources

- [[ChromeDevTools/chrome-devtools-mcp]] — primary source for this concept
