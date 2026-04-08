---
title: "Custom Agents in VS Code"
type: source
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "f15329dffe4f35b2509a04e3f7c3e97f8a038943740f52a8d082de1b4c3bd472"
sources:
  - raw/2026-04-07-custom-agents-in-vs-code.md
quality_score: 0
concepts:
  - custom-agents-in-vs-code
  - agent-handoffs-in-vs-code
  - custom-agent-file-structure
related:
  - "[[Custom Agents in VS Code]]"
  - "[[Agent Handoffs in VS Code]]"
  - "[[Custom Agent File Structure]]"
  - "[[Visual Studio Code]]"
  - "[[GitHub Copilot]]"
tier: hot
tags: [vs-code, ai, security, customization, workflow, agent]
---

# Custom Agents in VS Code

## Summary

This guide details how to create, configure, and manage custom AI agents in Visual Studio Code, enabling tailored personas for specific development roles and tasks. It covers agent file structure, tool restrictions, handoffs for workflow orchestration, sharing agents across teams, and security considerations. Examples and UI screenshots illustrate practical usage and customization.

## Key Points

- Custom agents allow AI to adopt specialized personas with specific tools and instructions.
- Agents can orchestrate workflows via handoffs, enabling guided transitions between roles.
- Custom agents are defined in .agent.md files and can be shared at workspace, user, or organization levels.

## Concepts Extracted

- **[[Custom Agents in VS Code]]** — Custom agents in Visual Studio Code are configurable AI personas tailored to specific development roles and tasks. They allow users to define distinct behaviors, tool access, and instructions for each agent, enabling consistent and specialized AI responses for workflows such as planning, implementation, and code review.
- **[[Agent Handoffs in VS Code]]** — Agent handoffs in VS Code enable guided, sequential workflows by transitioning users between specialized custom agents. Each handoff passes relevant context and prompts, supporting multi-step processes such as planning, implementation, and review.
- **[[Custom Agent File Structure]]** — Custom agent files in VS Code are Markdown documents (.agent.md) with a YAML frontmatter header and a Markdown body. The frontmatter defines agent configuration, while the body provides instructions and guidelines for the agent's behavior.

## Entities Mentioned

- **[[Visual Studio Code]]** — Visual Studio Code (VS Code) is a free, open-source code editor developed by Microsoft. It supports a wide range of programming languages, extensions, and AI-powered features, including custom agents for tailored development workflows.
- **[[GitHub Copilot]]** — GitHub Copilot is an AI-powered code completion tool developed by GitHub and OpenAI. It integrates with VS Code to provide intelligent code suggestions, and supports custom agents for specialized workflows.

## Notable Quotes

> "Custom agents enable you to configure the AI to adopt different personas tailored to specific development roles and tasks." — VS Code Documentation
> "Use custom agents when you need a persistent persona with specific tool restrictions, model preferences, or handoffs between roles." — VS Code Documentation

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-07-custom-agents-in-vs-code.md` |
| Type | guide |
| Author | Unknown |
| Date | 2024-04-01 |
| URL | https://code.visualstudio.com/docs/copilot/customization/custom-agents |
