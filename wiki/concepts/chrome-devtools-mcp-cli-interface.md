---
title: "Chrome DevTools MCP CLI Interface"
type: concept
created: 2026-04-13
last_verified: 2026-04-13
source_hash: "c4e8332bb539477ec966d1695a93bae4bf06a12c0a260303fe393c7f68646500"
sources:
  - raw/2026-04-13-httpsgithubcomchromedevtoolschrome-devtools-mcp.md
quality_score: 100
concepts:
  - chrome-devtools-mcp-cli-interface
related:
  - "[[Agent-Ergonomic Tool Design Principles]]"
  - "[[Chrome DevTools MCP GitHub Repository]]"
tier: hot
tags: [cli, browser-automation, chrome-devtools, agentic-tools, debugging, performance-analysis]
---

# Chrome DevTools MCP CLI Interface

## Overview

The Chrome DevTools MCP CLI is an experimental command-line interface that allows direct interaction with the Chrome browser via the MCP server. It enables automation, debugging, and inspection tasks from the terminal, supporting both human and agent-generated scripts.

## How It Works

The CLI is installed globally via npm (`npm i chrome-devtools-mcp@latest -g`) and exposes the `chrome-devtools` command. It acts as a client to a background MCP daemon, which manages the Chrome browser instance using Unix sockets (Linux/Mac) or named pipes (Windows).

When a tool command is issued (e.g., `list_pages`), the CLI automatically starts the MCP server and browser in the background if they aren't already running. The background instance is persistent, so subsequent commands reuse the same browser state (open pages, cookies, etc.), enabling stateful workflows.

Manual control is available via `start`, `stop`, and `status` commands. The `start` command forwards arguments (such as `--headless`, `--userDataDir`) to the MCP server, allowing customization of the browser environment. Headless and isolated modes are enabled by default unless overridden.

The CLI supports all tools available in the MCP tool reference, with required arguments passed positionally and optional arguments as flags. Output is human-readable by default but can be formatted as raw JSON for programmatic consumption. Example commands include navigating to a URL, taking screenshots, clicking elements, filling forms, and running Lighthouse audits.

Troubleshooting is facilitated by the `stop` command to reset the daemon and the `DEBUG` environment variable for verbose logs. CLI command generation is handled by scripts, with some commands excluded for usability reasons.

## Key Properties

- **Automatic Daemon Management:** CLI automatically starts and manages the MCP server and browser instance, enabling seamless interaction.
- **Persistent Browser State:** Background browser instance preserves state across commands, supporting complex workflows.
- **Comprehensive Tool Access:** All MCP tools are accessible via CLI, supporting automation, debugging, and inspection.
- **Flexible Output Formats:** Supports human-readable summaries and raw JSON output for programmatic use.
- **Manual Control:** Explicit start, stop, and status commands allow fine-grained management of the daemon.

## Limitations

Experimental; some arguments and commands are not supported or excluded for usability. Headless and isolated modes are defaults, which may not suit all workflows. Requires global npm installation. Troubleshooting may require manual intervention if the daemon hangs.

## Example

Install and check status:

```sh
npm i chrome-devtools-mcp@latest -g
chrome-devtools status
```

Navigate to a URL:

```sh
chrome-devtools navigate_page "https://google.com"
```

Take a screenshot:

```sh
chrome-devtools take_screenshot --filePath screenshot.png
```

Output as JSON:

```sh
chrome-devtools list_pages --output-format=json
```

## Visual

No diagrams, but the docs/cli.md file contains code snippets showing CLI usage and tool invocation.

## Relationship to Other Concepts

- **[[Agent-Ergonomic Tool Design Principles]]** — The CLI interface is designed according to agent-ergonomic principles for composability and usability.

## Practical Applications

Used for direct browser automation, debugging, and inspection from the terminal. Supports agent-generated scripts and manual workflows for testing, performance analysis, and web automation.

## Sources

- [[Chrome DevTools MCP GitHub Repository]] — primary source for this concept
