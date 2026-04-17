---
title: "Chrome DevTools MCP GitHub Repository"
type: source
created: 2026-04-13
last_verified: 2026-04-13
source_hash: "c4e8332bb539477ec966d1695a93bae4bf06a12c0a260303fe393c7f68646500"
sources:
  - raw/2026-04-13-httpsgithubcomchromedevtoolschrome-devtools-mcp.md
quality_score: 100
concepts:
  - model-context-protocol-mcp-server-for-chrome-devtools
  - agent-ergonomic-tool-design-principles
  - chrome-devtools-mcp-cli-interface
related:
  - "[[Model-Context-Protocol (MCP) Server for Chrome DevTools]]"
  - "[[Agent-Ergonomic Tool Design Principles]]"
  - "[[Chrome DevTools MCP CLI Interface]]"
  - "[[Chrome DevTools MCP]]"
  - "[[puppeteer]]"
  - "[[Chrome DevTools]]"
tier: hot
tags: [chrome-devtools, agentic-tools, cli, debugging, browser-automation, mcp, design-principles, performance-analysis, puppeteer]
---

# Chrome DevTools MCP GitHub Repository

## Summary

Chrome DevTools MCP is a server and plugin that enables coding agents (such as Gemini, Claude, Cursor, Copilot) to control and inspect a live Chrome browser via the Model-Context-Protocol (MCP). It provides deep integration with Chrome DevTools for automation, debugging, and performance analysis, supporting a wide range of agentic and CLI workflows. The repository includes detailed configuration instructions for many agent platforms, a robust tool reference, and design principles for agent-ergonomic interfaces.

## Key Points

- Provides an MCP server for agentic control of Chrome DevTools, enabling browser automation, debugging, and performance analysis.
- Supports integration with numerous coding agent platforms and IDEs, including Gemini, Claude Code, Copilot, Cursor, JetBrains, and more.
- Features a comprehensive toolset for input automation, navigation, emulation, performance, network, and debugging tasks, with agent-agnostic and token-optimized design principles.

## Concepts Extracted

- **[[Model-Context-Protocol (MCP) Server for Chrome DevTools]]** — The Model-Context-Protocol (MCP) server for Chrome DevTools is a middleware that allows coding agents to remotely control, inspect, and automate a Chrome browser instance. It exposes Chrome DevTools functionality via a standardized protocol, enabling reliable automation, advanced debugging, and performance analysis for agentic workflows.
- **[[Agent-Ergonomic Tool Design Principles]]** — Agent-ergonomic tool design principles are guidelines for building tools that are easily usable by coding agents and humans. They emphasize interoperability, composability, token efficiency, actionable errors, and progressive complexity, ensuring tools are robust, flexible, and optimized for agent workflows.
- **[[Chrome DevTools MCP CLI Interface]]** — The Chrome DevTools MCP CLI is an experimental command-line interface that allows direct interaction with the Chrome browser via the MCP server. It enables automation, debugging, and inspection tasks from the terminal, supporting both human and agent-generated scripts.

## Entities Mentioned

- **[[Chrome DevTools MCP]]** — Chrome DevTools MCP is a server and plugin that enables coding agents to control and inspect a live Chrome browser using the Model-Context-Protocol (MCP). It exposes Chrome DevTools functionality for automation, debugging, and performance analysis, supporting integration with a wide variety of agent platforms and IDEs.
- **[[puppeteer]]** — Puppeteer is a Node.js library that provides a high-level API to control Chrome or Chromium over the DevTools Protocol. It is used by Chrome DevTools MCP for reliable browser automation, enabling actions such as navigation, input simulation, and screenshot capture.
- **[[Chrome DevTools]]** — Chrome DevTools is a suite of developer tools built into the Chrome browser for debugging, inspecting, and analyzing web applications. Chrome DevTools MCP exposes its API to coding agents via the MCP protocol, enabling deep inspection and performance analysis.

## Notable Quotes

> "chrome-devtools-mcp lets your coding agent (such as Gemini, Claude, Cursor or Copilot) control and inspect a live Chrome browser." — README
> "Use standards like MCP. Don't lock in to one LLM. Interoperability is key." — Design Principles
> "Return semantic summaries. 'LCP was 3.2s' is better than 50k lines of JSON." — Design Principles

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-13-httpsgithubcomchromedevtoolschrome-devtools-mcp.md` |
| Type | repo |
| Author | Unknown |
| Date | Unknown |
| URL | https://github.com/ChromeDevTools/chrome-devtools-mcp |
