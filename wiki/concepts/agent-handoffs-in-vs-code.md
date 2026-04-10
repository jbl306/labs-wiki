---
title: "Agent Handoffs in VS Code"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "f15329dffe4f35b2509a04e3f7c3e97f8a038943740f52a8d082de1b4c3bd472"
sources:
  - raw/2026-04-07-custom-agents-in-vs-code.md
quality_score: 100
concepts:
  - agent-handoffs-in-vs-code
related:
  - "[[Custom Agents in VS Code]]"
tier: hot
tags: [workflow, ai, vs-code, handoff, automation]
---

# Agent Handoffs in VS Code

## Overview

Agent handoffs in VS Code enable guided, sequential workflows by transitioning users between specialized custom agents. Each handoff passes relevant context and prompts, supporting multi-step processes such as planning, implementation, and review.

## How It Works

Handoffs are defined in the YAML frontmatter of a custom agent file under the `handoffs` property. Each handoff specifies the target agent, button label, prompt text, and optional flags (such as auto-submit and model selection). When a chat response completes, handoff buttons appear, allowing users to seamlessly transition to the next agent with context and a pre-filled prompt.

**Handoff Definition:**
```yaml
handoffs:
  - label: Start Implementation
    agent: implementation
    prompt: Now implement the plan outlined above.
    send: false
    model: GPT-5.2 (copilot)
```

**Mechanism:**
- After an agent completes its task, handoff buttons are displayed.
- Selecting a handoff button switches to the target agent and pre-fills the prompt.
- If `send: true`, the prompt is automatically submitted, starting the next workflow step.
- The handoff can specify a model to use for the next step, ensuring task-appropriate AI behavior.

**Workflow Examples:**
- Planning → Implementation: Generate a plan, then hand off to an implementation agent to start coding.
- Implementation → Review: Complete implementation, then switch to a code review agent for quality and security checks.
- Write Failing Tests → Write Passing Tests: Generate failing tests, then hand off to implement code changes that make tests pass.

**Edge Cases and Trade-Offs:**
- Handoffs require careful configuration to ensure context is preserved and prompts are appropriate for the next agent.
- Misconfigured handoffs can lead to workflow dead-ends or loss of context.
- Handoffs support both manual and automated transitions, giving developers control over each step.

**Complexity:**
- Handoffs add modularity and composability to agent workflows, enabling repeatable, guided processes.
- They require coordination between agent definitions to ensure smooth transitions and task coverage.

## Key Properties

- **Guided Workflow Transitions:** Handoffs enable step-by-step workflows, transitioning users between agents with relevant context and prompts.
- **Context Preservation:** Handoffs pass context and pre-filled prompts to the next agent, ensuring continuity and task focus.
- **Flexible Model Selection:** Each handoff can specify a preferred AI model for the next step, supporting task-specific optimization.

## Limitations

Handoffs depend on correct agent configuration and context management. Misconfigured handoffs can break workflow continuity or lead to inappropriate prompts. Automated handoffs (`send: true`) may bypass user review, which is risky for sensitive tasks. Context loss or tool mismatch between agents can reduce effectiveness.

## Example

Example Handoff in YAML Frontmatter:

```yaml
handoffs:
  - label: Implement Plan
    agent: implementation
    prompt: Implement the plan outlined above.
    send: false
```

After generating a plan, the user sees an 'Implement Plan' button. Clicking it switches to the implementation agent with the prompt pre-filled.

## Visual

No specific diagram for handoffs, but the second image shows the Chat Customizations editor where agents can be created and managed, supporting handoff configuration.

## Relationship to Other Concepts

- **[[Custom Agents in VS Code]]** — Handoffs are a feature within custom agents, enabling workflow orchestration.
- **Subagents** — Subagents can be invoked as part of handoff workflows for specialized tasks.

## Practical Applications

Handoffs are used to orchestrate multi-step development workflows, such as planning → implementation → review, ensuring each step is handled by a specialized agent. They support modular, repeatable processes and facilitate collaboration by guiding developers through task sequences with context preservation.

## Sources

- [[Custom Agents in VS Code]] — primary source for this concept
