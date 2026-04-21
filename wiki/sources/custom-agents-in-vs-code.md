---
title: "Custom Agents in VS Code"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "0b4ca1a6668a37f0034808e00b1b05c0b3c1e2f03f82902ed4971e8256ec3179"
sources:
  - raw/2026-04-07-custom-agents-in-vs-code.md
quality_score: 100
concepts:
  - custom-agents-in-vs-code
  - agent-handoffs-in-vs-code
  - custom-agent-file-structure
related:
  - "[[Agent Handoffs in VS Code]]"
  - "[[Custom Agent File Structure]]"
  - "[[Visual Studio Code]]"
tier: hot
knowledge_state: executed
tags: [vs-code, customization, ai, security, agent, workflow]
---

# Custom Agents in VS Code

## Summary

This article details how to create, configure, and manage custom AI agents in Visual Studio Code, enabling tailored personas for distinct development roles and tasks. It covers agent file structure, handoff workflows, agent orchestration, file locations, and sharing strategies, emphasizing persistent, role-specific customization and workflow automation. Security considerations and integration with VS Code and Claude Code formats are also discussed.

## Key Points

- Custom agents allow persistent, role-specific AI personas with tool and instruction restrictions.
- Handoffs orchestrate guided workflows between agents, supporting sequential task transitions.
- Custom agent files use a structured Markdown format with YAML frontmatter for configuration.

## Concepts Extracted

- **Custom Agents in VS Code** — Custom agents in VS Code are configurable AI personas tailored for specific development roles and tasks. They allow users to define persistent agent behaviors, tool restrictions, and instructions, enabling seamless switching between specialized workflows and consistent task execution.
- **[[Agent Handoffs in VS Code]]** — Agent handoffs in VS Code enable guided, sequential workflows by transitioning context and prompts between specialized agents. This mechanism supports multi-step processes, ensuring continuity and developer control at each stage.
- **[[Custom Agent File Structure]]** — The custom agent file structure in VS Code defines how agents are configured and implemented using Markdown files with YAML frontmatter. This structure enables precise control over agent behavior, tool access, model selection, and workflow orchestration.

## Entities Mentioned

- **[[Visual Studio Code]]** — Visual Studio Code (VS Code) is a widely used, extensible code editor developed by Microsoft. It supports a rich ecosystem of extensions, including AI-powered agents, and provides robust customization for development workflows.

## Notable Quotes

> "Use custom agents when you need a persistent persona with specific tool restrictions, model preferences, or handoffs between roles." — VS Code Documentation
> "Custom agents consist of a set of instructions and tools that are applied when you switch to that agent." — VS Code Documentation

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-07-custom-agents-in-vs-code.md` |
| Type | guide |
| Author | Unknown |
| Date | 2026-04-15 |
| URL | https://code.visualstudio.com/docs/copilot/customization/custom-agents |
