---
title: "Model-Context-Protocol (MCP) Server for Chrome DevTools"
type: concept
created: 2026-04-13
last_verified: 2026-04-13
source_hash: "c4e8332bb539477ec966d1695a93bae4bf06a12c0a260303fe393c7f68646500"
sources:
  - raw/2026-04-13-httpsgithubcomchromedevtoolschrome-devtools-mcp.md
quality_score: 76
concepts:
  - model-context-protocol-mcp-server-for-chrome-devtools
related:
  - "[[AXI Design Principles for Agent-Ergonomic CLI Tools]]"
  - "[[ChromeDevTools/chrome-devtools-mcp]]"
tier: hot
tags: [browser-automation, chrome-devtools, agentic-workflows, debugging, performance-analysis, mcp, puppeteer, cli, agent-integration]
---

# Model-Context-Protocol (MCP) Server for Chrome DevTools

## Overview

The Model-Context-Protocol (MCP) server for Chrome DevTools is a middleware that allows coding agents to remotely control, inspect, and automate a Chrome browser instance. It exposes Chrome DevTools functionality via a standardized protocol, enabling reliable automation, advanced debugging, and performance analysis for agentic workflows.

## How It Works

The MCP server acts as a bridge between coding agents (such as Gemini, Claude, Copilot, Cursor) and a running Chrome browser, exposing the Chrome DevTools API through a standardized protocol. Agents connect to the MCP server via a configuration specifying the command and arguments (typically using `npx chrome-devtools-mcp@latest`).

Upon connection, the MCP server launches or connects to a Chrome instance, optionally in headless mode, and exposes a suite of tools for browser automation, inspection, and debugging. These tools are accessible via agent prompts or CLI commands, and include input automation (click, drag, fill), navigation (new_page, navigate_page), emulation (emulate, resize_page), performance tracing (performance_start_trace, performance_analyze_insight), network inspection (list_network_requests, get_network_request), and debugging (evaluate_script, take_screenshot, lighthouse_audit).

The server supports both local and remote browser instances, configurable via flags such as `--browser-url` or `--ws-endpoint`. It can connect to browsers running on desktop, in CI environments, or even on Android devices (via port forwarding and WebSocket endpoints). The server is designed to be agent-agnostic, supporting integration with a wide range of agent platforms and IDEs through standardized configuration snippets.

For automation, the MCP server leverages Puppeteer to drive browser actions and Chrome DevTools for deep inspection and performance analysis. It records traces, extracts actionable insights, and returns structured summaries optimized for token efficiency. Heavy assets (screenshots, traces) are referenced via file paths or URIs, rather than streamed, to minimize token usage and maximize interoperability.

The server also supports usage statistics collection (opt-out via flags or environment variables), update checks, and progressive complexity in tool arguments. It is robust against errors, providing actionable, context-rich error messages for agents to self-heal or guide human intervention. The CLI interface enables direct terminal interaction, with automatic daemon management and persistent browser state across commands.

## Key Properties

- **Agent-Agnostic API:** Uses the MCP standard, enabling interoperability with multiple coding agents and IDEs without lock-in.
- **Comprehensive Toolset:** Exposes tools for input automation, navigation, emulation, performance, network, and debugging, mapped to Chrome DevTools capabilities.
- **Token-Optimized Summaries:** Returns concise, semantic summaries for agent consumption, referencing heavy assets via file paths or URIs.
- **Self-Healing Errors:** Provides actionable error messages with context and potential fixes to support agent and human collaboration.
- **Progressive Complexity:** Tools are simple by default but offer advanced arguments for power users and agents requiring fine-grained control.
- **Persistent Browser State:** CLI and agent workflows reuse background browser instances, preserving state such as open pages and cookies.

## Limitations

Officially supports only Google Chrome and Chrome for Testing. Other Chromium-based browsers may work but are not guaranteed. Exposes browser content to MCP clients, so sensitive information should not be shared. Usage statistics are collected by default unless opted out. Some advanced features (e.g., debugging Chrome on Android) are experimental and may require manual setup.

## Example

To configure an agent (e.g., Claude Code) to use Chrome DevTools MCP:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

To take a screenshot via CLI:

```sh
chrome-devtools take_screenshot --filePath screenshot.png
```

## Visual

No diagrams or charts are present in the source, but the README and tool reference enumerate the available tools and their categories in structured lists.

## Relationship to Other Concepts

- **Agent eXperience Interface (AXI)** — Both are agent-ergonomic interfaces for tool integration; AXI is a design pattern, MCP is a protocol implementation.
- **[[AXI Design Principles for Agent-Ergonomic CLI Tools]]** — Chrome DevTools MCP follows similar principles for agent-ergonomic design, such as composable tools and human-agent collaboration.

## Practical Applications

Used by coding agents to automate browser tasks, debug web applications, analyze performance, and inspect network activity. Enables agent-driven workflows in IDEs, CI/CD pipelines, and agentic coding platforms. Supports use cases such as automated testing, performance audits, browser-based data collection, and agent-assisted debugging.

## Sources

- [[ChromeDevTools/chrome-devtools-mcp]] — primary source for this concept
