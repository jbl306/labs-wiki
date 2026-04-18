---
title: "Custom Agents in VS Code"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "f15329dffe4f35b2509a04e3f7c3e97f8a038943740f52a8d082de1b4c3bd472"
sources:
  - raw/2026-04-07-custom-agents-in-vs-code.md
quality_score: 75
concepts:
  - custom-agents-in-vs-code
related:
  []
  []
tier: hot
tags: [ai, vs-code, agent, workflow, security, customization]
---

# Custom Agents in VS Code

## Overview

Custom agents in Visual Studio Code are configurable AI personas tailored to specific development roles and tasks. They allow users to define distinct behaviors, tool access, and instructions for each agent, enabling consistent and specialized AI responses for workflows such as planning, implementation, and code review.

## How It Works

Custom agents are implemented as Markdown files (.agent.md) with YAML frontmatter specifying metadata and configuration. The frontmatter includes fields such as description, name, tools, agents (for subagent orchestration), model preferences, and handoffs. The body of the file contains detailed instructions and guidelines for the agent's behavior.

**Agent File Structure:**
- The header (YAML frontmatter) defines agent properties:
  - `description`: Brief summary shown in chat input.
  - `name`: Agent name (defaults to filename if omitted).
  - `tools`: List of allowed tools (e.g., 'search/codebase', 'edit').
  - `agents`: Subagents permitted for orchestration.
  - `model`: AI model(s) to use, prioritized if an array.
  - `handoffs`: Workflow transitions to other agents, with button labels and prompts.
  - `hooks`: Commands triggered by agent actions (e.g., post-edit formatting).
- The body provides Markdown-formatted instructions, which are prepended to user prompts when the agent is active.

**Agent Creation and Management:**
- Agents can be created via the Chat Customizations editor or using the `/create-agent` command in chat.
- Agents are stored in workspace (.github/agents), user profile (~/.copilot/agents), or organization-level folders.
- The UI allows users to show/hide agents in dropdowns, customize tool priority, and share agents across teams.

**Tool Restrictions and Security:**
- Each agent can restrict tool access, enforcing the principle of least privilege for sensitive workflows (e.g., read-only tools for planning).
- Tool list priority ensures prompt file tools override agent tools if both are specified.

**Handoffs and Workflow Orchestration:**
- Handoffs enable guided transitions between agents, supporting multi-step workflows (e.g., planning → implementation → review).
- Handoff buttons appear after chat responses, pre-filling prompts and optionally auto-submitting them.

**Subagents and Hooks:**
- Agents can invoke subagents for specialized tasks, with restrictions controlled via the `agents` property.
- Hooks allow automation of actions (e.g., running a formatter after edits) scoped to the agent.

**Claude Format Compatibility:**
- VS Code supports Claude-specific agent formats for cross-platform agent reuse.

**Example:**
A planning agent might restrict tools to 'web/fetch' and 'search/codebase', use the 'Claude Opus 4.5' model, and provide instructions to generate an implementation plan without making code edits. Handoffs can transition to an implementation agent with a pre-filled prompt.

**Edge Cases and Trade-Offs:**
- Tool availability is checked at runtime; unavailable tools are ignored.
- Agents can be hidden from dropdowns or restricted from subagent invocation for granular control.
- Security-sensitive agents should be reviewed for tool and instruction compliance before sharing.

**Complexity:**
- Agent orchestration enables modular, reusable workflows but requires careful configuration to avoid privilege escalation or workflow dead-ends.
- The YAML frontmatter provides flexible, composable agent definitions, supporting both simple and complex use cases.

## Key Properties

- **Configurable Tool Access:** Agents can restrict which tools are available, enforcing least privilege and task-specific capabilities.
- **Persistent Persona:** Agents retain instructions, tool restrictions, and model preferences for consistent, repeatable behavior.
- **Workflow Orchestration via Handoffs:** Agents can guide users through multi-step workflows with handoff buttons, pre-filled prompts, and context transitions.
- **Flexible File Locations:** Agents can be defined at workspace, user, or organization level, supporting sharing and reuse.

## Limitations

Custom agents rely on tool availability; unavailable tools are ignored, which may limit functionality. Misconfigured tool lists or instructions can lead to privilege escalation or workflow dead-ends. Security-sensitive workflows require careful review of tool access and instructions before sharing. Agents are only as effective as their instructions and tool configuration, and may require maintenance as project requirements evolve.

## Example

Example Planning Agent File:

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
* Overview: A brief description of the feature or refactoring task.
* Requirements: A list of requirements for the feature or refactoring task.
* Implementation Steps: A detailed list of steps to implement the feature or refactoring task.
* Testing: A list of tests that need to be implemented to verify the feature or refactoring task.
```

## Visual

The first image shows the VS Code documentation header for custom agents. The second image displays the Chat Customizations editor, with the 'Agents' tab selected and options to generate a new agent for workspace or user. Built-in agents (Ask, Explore, Plan) are listed, and a button allows creation of new custom agents.

## Relationship to Other Concepts

- **Prompt Files** — Prompt files provide one-off instructions and tool lists, but lack persistent personas and workflow orchestration.
- **Agent Skills** — Agent skills are portable, reusable capabilities (scripts/resources) that can be used by custom agents.

## Practical Applications

Custom agents are used for specialized development workflows such as security review, planning, implementation, and code review. Teams can share agents to enforce consistent practices, restrict tool access for sensitive tasks, and automate post-edit actions (e.g., formatting). Agents enable modular, repeatable workflows and facilitate collaboration by providing persistent AI personas tailored to organizational roles.

## Sources

- Custom Agents in VS Code — primary source for this concept
