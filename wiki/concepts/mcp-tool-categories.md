---
title: "MCP Tool Categories"
type: concept
created: '2026-04-22'
last_verified: '2026-04-22'
sources:
  - raw/2026-04-13-httpsgithubcomchromedevtoolschrome-devtools-mcp.md
quality_score: 85
concepts:
  - mcp-tool-categories
related:
  - "[[ChromeDevTools/chrome-devtools-mcp]]"
  - "[[Model-Context-Protocol (MCP) Server for Chrome DevTools]]"
tier: warm
tags: [mcp, tool-design, browser-automation, agent-ergonomics]
---

# MCP Tool Categories

## Overview

MCP tool categories are a design pattern for organizing Model Context Protocol server tools into semantic groupings that reflect both domain boundaries and user intent. In the chrome-devtools-mcp implementation, 34 tools are grouped into 7 categories: Input automation, Navigation automation, Emulation, Performance, Network, Debugging, Extensions, and Memory. This categorical structure provides agents with a mental model of the tool surface and enables mode-based tool subsetting (e.g., `--slim` mode drops Performance/Memory/Extensions).

## How It Works

MCP servers expose tools as a flat list to agents, but the categorical structure serves three purposes:

1. **Documentation organization** — Tool reference docs group tools by category, making it easier for humans (and agents reading docs) to discover related capabilities. For example, all network-inspection tools (`list_network_requests`, `get_network_request`) are grouped under "Network."

2. **Mode-based subsetting** — The server can selectively expose tools based on categories. The `--slim` flag drops Performance/Memory/Extensions categories, reducing the tool surface from 34 to ~15 tools. This lowers MCP handshake overhead and LLM token cost for basic browser workflows.

3. **Semantic boundaries** — Categories reflect functional domains that align with how developers think about browser automation: "I want to navigate" → Navigation tools; "I want to debug network issues" → Network + Debugging tools; "I want to measure performance" → Performance tools.

The categorical structure is implemented as:
- A structured README section listing tools by category (e.g., "**Input automation (9 tools)**")
- CLI mode filtering logic that conditionally loads tool handlers based on category flags
- Tool reference documentation (markdown) that groups tool descriptions by category

Categories in chrome-devtools-mcp:
- **Input automation** (9 tools) — `click`, `drag`, `fill`, `fill_form`, `handle_dialog`, `hover`, `press_key`, `type_text`, `upload_file`
- **Navigation automation** (6 tools) — `close_page`, `list_pages`, `navigate_page`, `new_page`, `select_page`, `wait_for`
- **Emulation** (2 tools) — `emulate`, `resize_page`
- **Performance** (3 tools) — `performance_analyze_insight`, `performance_start_trace`, `performance_stop_trace`
- **Network** (2 tools) — `get_network_request`, `list_network_requests`
- **Debugging** (6 tools) — `evaluate_script`, `get_console_message`, `lighthouse_audit`, `list_console_messages`, `take_screenshot`, `take_snapshot`
- **Extensions** (5 tools) — `install_extension`, `list_extensions`, `reload_extension`, `trigger_extension_action`, `uninstall_extension`
- **Memory** (1 tool) — `take_memory_snapshot`

## Key Properties

- **Orthogonal categories** — Each tool belongs to exactly one category; categories do not overlap (e.g., `take_screenshot` is Debugging, not Navigation).
- **Mode-based subsetting** — Categories enable selective tool exposure (slim mode drops 3 of 7 categories).
- **Agent-ergonomic** — Categories provide a semantic map that agents can reason about when planning tool sequences.
- **Documented structure** — Categories are explicit in the README and tool reference, not just internal implementation details.

## Trade-offs

**Benefits:**
- Reduces cognitive load for humans and agents discovering tools
- Enables mode-based optimization (slim vs full)
- Provides a natural clustering for documentation and tool discovery

**Drawbacks:**
- Adds complexity to tool registration (each tool must be tagged with a category)
- Categories must remain stable across versions to avoid breaking mode filters
- Forcing a single category per tool may feel arbitrary for tools that span domains (e.g., `evaluate_script` could be Debugging or Input automation)

## Example

A minimal navigation workflow using only Navigation tools:

```python
agent.call_mcp_tool("chrome-devtools", "new_page")
agent.call_mcp_tool("chrome-devtools", "navigate_page", url="https://example.com")
agent.call_mcp_tool("chrome-devtools", "wait_for", selector="h1")
```

A full debugging workflow using Navigation + Network + Debugging:

```python
agent.call_mcp_tool("chrome-devtools", "navigate_page", url="https://example.com")
agent.call_mcp_tool("chrome-devtools", "list_network_requests")  # Network
agent.call_mcp_tool("chrome-devtools", "list_console_messages")  # Debugging
agent.call_mcp_tool("chrome-devtools", "take_screenshot")        # Debugging
```

Slim mode excludes Performance/Memory/Extensions categories, so agents using `--slim` cannot call:
- `performance_start_trace`, `performance_stop_trace`, `performance_analyze_insight`
- `take_memory_snapshot`
- `install_extension`, `list_extensions`, `reload_extension`, `trigger_extension_action`, `uninstall_extension`

## Relationship to Other Concepts

- **[[Model-Context-Protocol (MCP) Server for Chrome DevTools]]** — The MCP server implementation that uses these categories.
- **[[ChromeDevTools/chrome-devtools-mcp]]** — The upstream project that defines these categories.

## Practical Applications

MCP tool categories are useful for:
- **Agent planning** — Agents can reason about which category of tools to use for a given task ("I need to measure performance" → Performance category).
- **Cost optimization** — Slim mode reduces token cost by ~50% for basic workflows.
- **Documentation** — Categories provide a natural structure for tool reference docs, making it easier for humans to find relevant tools.
- **Tool discovery** — Agents reading the README can quickly identify all tools in a category without scanning the full 34-tool list.

## Sources

- [[ChromeDevTools/chrome-devtools-mcp]] — defines the 7-category structure for 34 MCP tools
