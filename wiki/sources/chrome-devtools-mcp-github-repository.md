---
title: "Chrome DevTools MCP GitHub Repository"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "d08068fb45e100d60f932162eb36a897a7cc3ce1d57ed489379266aea9366d7d"
sources:
  - raw/2026-04-13-httpsgithubcomchromedevtoolschrome-devtools-mcp.md
quality_score: 80
concepts:
  - model-context-protocol-mcp-server-for-chrome-devtools
  - chrome-devtools-mcp-cli-interface
  - design-principles-agentic-browser-automation-tools
related:
  - "[[Model-Context-Protocol (MCP) Server for Chrome DevTools]]"
  - "[[Chrome DevTools MCP CLI Interface]]"
  - "[[Chrome DevTools MCP]]"
tier: hot
knowledge_state: executed
tags: [agentic-integration, chrome-devtools, browser-automation, tooling, mcp]
---

# Chrome DevTools MCP GitHub Repository

## Summary

The Chrome DevTools MCP project provides a Model-Context-Protocol (MCP) server that enables AI coding agents to control and inspect a live Chrome browser for automation, debugging, and performance analysis. It offers a rich set of tools for browser automation, integrates with a wide range of agentic platforms, and emphasizes agent-agnostic design and token-efficient communication. The repository includes a CLI, extensive configuration options, and support for advanced use cases such as Android debugging and plugin-based skill extension.

## Key Points

- Implements an MCP server for Chrome DevTools, allowing agents like Claude, Gemini, Copilot, and Cursor to automate and debug browsers.
- Features a comprehensive CLI, plugin system, and support for both local and remote Chrome instances (including Android).
- Emphasizes agent-agnostic, token-optimized, and composable tool design, with privacy controls and opt-out mechanisms for telemetry.

## Concepts Extracted

- **[[Model-Context-Protocol (MCP) Server for Chrome DevTools]]** — The Model-Context-Protocol (MCP) Server for Chrome DevTools is a middleware layer that allows AI coding agents to programmatically control, inspect, and automate a live Chrome browser. It exposes a standardized API for browser automation, debugging, and performance analysis, making advanced browser tooling accessible to agentic workflows.
- **[[Chrome DevTools MCP CLI Interface]]** — The Chrome DevTools MCP CLI is an experimental command-line interface that allows users and agents to interact with the browser via the MCP server directly from the terminal. It streamlines debugging, automation, and script generation by providing persistent, scriptable access to browser tools.
- **Design Principles for Agentic Browser Automation Tools** — The design principles underlying Chrome DevTools MCP emphasize agent-agnosticism, composability, token efficiency, and robust error handling. These guidelines ensure that browser automation tools are interoperable, efficient, and usable by both humans and AI agents.

## Entities Mentioned

- **[[Chrome DevTools MCP]]** — Chrome DevTools MCP is an open-source Model-Context-Protocol server that enables AI coding agents to automate, inspect, and debug Chrome browsers. It exposes a rich set of composable tools for browser automation, performance analysis, and debugging, and is designed to be agent-agnostic and token-efficient.

## Notable Quotes

> "Chrome DevTools for Agents (`chrome-devtools-mcp`) lets your coding agent (such as Gemini, Claude, Cursor or Copilot) control and inspect a live Chrome browser." — README
> "Use standards like MCP. Don't lock in to one LLM. Interoperability is key." — docs/design-principles.md
> "Return semantic summaries. 'LCP was 3.2s' is better than 50k lines of JSON. Files are the right location for large amounts of data." — docs/design-principles.md

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-13-httpsgithubcomchromedevtoolschrome-devtools-mcp.md` |
| Type | repo |
| Author | Unknown |
| Date | Unknown |
| URL | https://github.com/ChromeDevTools/chrome-devtools-mcp |
