---
title: "Custom Agent File Structure"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "f15329dffe4f35b2509a04e3f7c3e97f8a038943740f52a8d082de1b4c3bd472"
sources:
  - raw/2026-04-07-custom-agents-in-vs-code.md
quality_score: 0
concepts:
  - custom-agent-file-structure
related:
  - "[[Custom Agents in VS Code]]"
  - "[[Agent Skills]]"
  - "[[Custom Agents in VS Code]]"
tier: hot
tags: [agent, vs-code, file-format, yaml, markdown]
---

# Custom Agent File Structure

## Overview

Custom agent files in VS Code are Markdown documents (.agent.md) with a YAML frontmatter header and a Markdown body. The frontmatter defines agent configuration, while the body provides instructions and guidelines for the agent's behavior.

## How It Works

The custom agent file structure consists of two main parts:

**1. YAML Frontmatter Header:**
- Placed at the top of the .agent.md file, enclosed by triple dashes (`---`).
- Fields include:
  - `description`: Brief summary for chat input.
  - `name`: Agent name.
  - `argument-hint`: Optional guidance for user input.
  - `tools`: List of allowed tools (array or comma-separated string).
  - `agents`: Subagents permitted for orchestration.
  - `model`: Preferred AI model(s).
  - `handoffs`: Workflow transitions with button labels, prompts, and model selection.
  - `hooks`: Commands triggered by agent actions (e.g., post-edit formatting).
  - `target`: Target environment (e.g., vscode, github-copilot).
  - `user-invocable` and `disable-model-invocation`: Control agent visibility and invocation as subagent.
- Supports both VS Code and Claude-specific formats for cross-platform agent reuse.

**2. Markdown Body:**
- Contains detailed instructions, guidelines, and references for the agent.
- Instructions are prepended to user prompts when the agent is active.
- Supports Markdown links to other files and tool references (e.g., `#tool:web/fetch`).

**Example File:**
```yaml
---
description: Generate an implementation plan for new features or refactoring existing code.
name: Planner
tools: ['web/fetch', 'search/codebase', 'search/usages']
model: ['Claude Opus 4.5', 'GPT-5.2']
handoffs:
  - label: Implement Plan
    agent: agent
    prompt: Implement the plan outlined above.
    send: false
---
# Planning instructions
You are in planning mode. Your task is to generate an implementation plan for a new feature or for refactoring existing code. Don't make any code edits, just generate a plan. The plan consists of a Markdown document that describes the implementation plan, including the following sections:
* Overview
* Requirements
* Implementation Steps
* Testing
```

**Edge Cases and Trade-Offs:**
- Tool availability is checked at runtime; unavailable tools are ignored.
- Agents can be hidden from dropdowns or restricted from subagent invocation for granular control.
- Security-sensitive agents should be reviewed for tool and instruction compliance before sharing.

**Complexity:**
- The YAML frontmatter provides flexible, composable agent definitions, supporting both simple and complex use cases.

## Key Properties

- **YAML Frontmatter Configuration:** Defines agent metadata, tool access, model preferences, handoffs, hooks, and visibility.
- **Markdown Body Instructions:** Provides detailed guidelines and instructions for agent behavior, prepended to user prompts.
- **Cross-Platform Format Support:** Supports both VS Code and Claude agent formats for compatibility and reuse.

## Limitations

Misconfigured frontmatter or instructions can lead to privilege escalation, workflow dead-ends, or ineffective agent behavior. Tool availability is checked at runtime; unavailable tools are ignored. Agents require maintenance as project requirements evolve.

## Example

Example Custom Agent File:

```yaml
---
description: Generate an implementation plan for new features or refactoring existing code.
name: Planner
tools: ['web/fetch', 'search/codebase', 'search/usages']
model: ['Claude Opus 4.5', 'GPT-5.2']
handoffs:
  - label: Implement Plan
    agent: agent
    prompt: Implement the plan outlined above.
    send: false
---
# Planning instructions
You are in planning mode. Your task is to generate an implementation plan for a new feature or for refactoring existing code. Don't make any code edits, just generate a plan. The plan consists of a Markdown document that describes the implementation plan, including the following sections:
* Overview
* Requirements
* Implementation Steps
* Testing
```

## Visual

No specific diagram, but the second image shows the Chat Customizations editor with options to generate new agents and manage agent files.

## Relationship to Other Concepts

- **[[Custom Agents in VS Code]]** — The file structure is the foundation for defining custom agents.
- **[[Agent Skills]]** — Skills can be referenced or used within custom agent instructions.

## Practical Applications

Custom agent files are used to define specialized AI personas for planning, implementation, review, and other development tasks. Teams can share agent files to enforce consistent practices, restrict tool access, and automate workflow steps. The file structure supports modular, repeatable workflows and facilitates collaboration.

## Sources

- [[Custom Agents in VS Code]] — primary source for this concept
