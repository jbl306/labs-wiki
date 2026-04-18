---
title: "Copilot CLI and OpenCode Integration with MemPalace"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "d7c9bdfd6b0d2d033db7f2aacc5997a2b254a782eeeec861b84c54e43fa5c867"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-reworking-docs-for-copilot-opencode-4710bc64.md
quality_score: 100
concepts:
  - copilot-cli-opencode-integration-with-mempalace
related:
  - "[[Durable Copilot Session Checkpoint]]"
  - "[[Agent Skill Integration for Time-Series Forecasting]]"
  - "[[Copilot Session Checkpoint: Reworking Docs for Copilot/OpenCode]]"
tier: hot
tags: [copilot-cli, opencode, mempalace, mcp, ai-coding-tools, integration]
---

# Copilot CLI and OpenCode Integration with MemPalace

## Overview

Copilot CLI and OpenCode are AI coding tools integrated with the MemPalace AI memory system via MCP. This integration replaces previous references to Claude Code, reflecting the actual tools in use. The integration involves configuring MCP client settings, updating auto-save hooks, and managing agent wings to enable seamless AI-assisted coding workflows.

## How It Works

Both Copilot CLI and OpenCode use the MemPalace MCP server as their AI memory backend. The MCP configuration files specify stdio transport and the Python binary managed by pipx to run the MemPalace MCP server. This setup allows these tools to query, add, and manage knowledge in the palace, enabling features like conversation mining and auto-save hooks.

Auto-save hooks are configured to capture session artifacts from directories such as ~/.copilot/session-state/ and ~/.opencode/sessions, mining these into the palace for persistent storage and retrieval. Agent wings are updated to include copilot_cli and opencode wings, which represent specialized agent contexts or capabilities linked to these tools.

Documentation and integration plans have been reworked to replace all mentions of Claude Code with Copilot CLI and OpenCode, ensuring clarity and accuracy in the AI coding toolchain. MCP config examples in documentation now show both Copilot CLI and OpenCode formats, facilitating easier adoption and maintenance.

This integration supports advanced AI workflows by enabling persistent memory, knowledge graph queries, and seamless interaction between AI coding agents and the underlying knowledge base. It also supports future roadmap items like building wiki-to-palace injection scripts and setting up periodic re-mining cron jobs.

## Key Properties

- **MCP Configuration:** Uses JSON-RPC stdio transport with pipx-managed Python binary for MemPalace MCP server.
- **Auto-Save Hooks:** Capture session artifacts from Copilot CLI and OpenCode session directories for mining.
- **Agent Wings:** Includes copilot_cli and opencode wings representing specialized agent contexts.
- **Documentation Update:** Replaces Claude Code references with Copilot CLI and OpenCode in all actionable docs.

## Limitations

Integration depends on correct MCP configuration and pipx environment management, which can be complex for new users. Auto-save hooks require careful setup to ensure all relevant session artifacts are captured without duplication or omission. The current migration and integration are in progress with some changes uncommitted, indicating potential instability or incomplete documentation.

## Example

Example MCP config snippet for Copilot CLI (~/.copilot/mcp-config.json):

```json
{
  "transport": "stdio",
  "python_binary": "/home/jbl/.local/share/pipx/venvs/mempalace/bin/python"
}
```

Auto-save hook example for mining Copilot CLI session state:

```bash
mempalace mine ~/.copilot/session-state/
```

Agent wings configuration snippet:

```json
{
  "agent_wings": ["copilot_cli", "opencode"]
}
```

## Relationship to Other Concepts

- **[[Durable Copilot Session Checkpoint]]** — Copilot CLI session artifacts are mined into MemPalace for durable checkpointing.
- **[[Agent Skill Integration for Time-Series Forecasting]]** — Similar pattern of agent wings and skill integration applies.

## Practical Applications

This integration enables AI-assisted coding workflows with persistent memory and knowledge management, improving developer productivity and session continuity. It supports advanced features like conversation mining, auto-save hooks, and knowledge graph queries, making AI coding tools more robust and context-aware. The reworked documentation ensures teams can adopt and maintain this integration effectively.

## Sources

- [[Copilot Session Checkpoint: Reworking Docs for Copilot/OpenCode]] — primary source for this concept
