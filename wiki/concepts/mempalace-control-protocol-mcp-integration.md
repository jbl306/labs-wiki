---
title: "MemPalace Control Protocol (MCP) Integration"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "b467128355ad46633de12b9a2a90526c0641bff2b8a228c3bbd2cb733e3ad37b"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-installing-mempalace-beginning-migration-f4a540d2.md
quality_score: 0
concepts:
  - mempalace-control-protocol-mcp-integration
related:
  - "[[MemPalace Memory System]]"
  - "[[OpenMemory]]"
  - "[[Copilot CLI]]"
  - "[[Copilot Session Checkpoint: Installing MemPalace, Beginning Migration]]"
tier: hot
tags: [mcp, mempalace, openmemory, ai-agent-integration, protocol]
---

# MemPalace Control Protocol (MCP) Integration

## Overview

MCP is a control protocol used by MemPalace to expose memory management tools and enable integration with other systems. It replaces the OpenMemory MCP server and uses stdio transport for local communication, facilitating seamless interaction with AI agents and tooling.

## How It Works

MCP servers expose a set of tools accessible via defined transports. OpenMemory used an SSE (Server-Sent Events) transport over HTTP at port 8765, while MemPalace uses a stdio transport by running the `mempalace mcp` command locally.

The MCP server provides 19 tools that allow listing memories, querying, managing drawers and rooms, and other memory operations. This protocol enables AI agents and orchestration tools like Copilot CLI to interact programmatically with the memory system.

Configuration for MCP servers is maintained in a JSON file (`~/.copilot/mcp-config.json`) listing servers by name, type, and connection details. Migration involves replacing the OpenMemory MCP server entry with MemPalace's stdio server entry, updating commands and arguments accordingly.

This design choice avoids network dependencies and API key management, enhancing security and simplifying local development. The stdio transport is well-suited for local agent workflows and scripting environments.

Integration with labs-wiki and other AI tools is facilitated by MCP, enabling memory bridging and conversational context sharing.

## Key Properties

- **Transport Types:** Supports SSE (OpenMemory) and stdio (MemPalace) transports.
- **Toolset:** 19 memory management tools exposed via MCP.
- **Configuration:** JSON config file listing MCP servers with type, URL or command, and arguments.
- **Security:** Local stdio transport reduces attack surface compared to networked SSE.

## Limitations

The stdio transport limits MCP server access to local processes, restricting remote or distributed use cases. Transitioning from SSE to stdio requires updating client tooling and scripts. The MCP toolset is fixed at 19 tools, which may limit extensibility without protocol updates.

## Example

Example MCP config snippet replacing OpenMemory with MemPalace:

```json
{
  "mcpServers": {
    "mempalace": {
      "type": "stdio",
      "command": "mempalace",
      "args": ["mcp"]
    },
    "labs-wiki": {
      "type": "stdio",
      "command": "python3",
      "args": ["/home/jbl/projects/labs-wiki/scripts/wiki_mcp_server.py"]
    }
  }
}
```

This config enables local stdio-based MCP communication with MemPalace.

## Relationship to Other Concepts

- **[[MemPalace Memory System]]** — MCP is the control protocol for MemPalace.
- **[[OpenMemory]]** — Previous MCP server used SSE transport.
- **[[Copilot CLI]]** — Uses MCP servers for AI agent integration.

## Practical Applications

MCP integration enables AI agents and orchestration tools to manage memory systems programmatically, supporting workflows such as memory listing, querying, and migration. The stdio transport simplifies local development and improves security by avoiding network exposure. This protocol is essential for integrating MemPalace into AI agent ecosystems and bridging with knowledge bases like labs-wiki.

## Sources

- [[Copilot Session Checkpoint: Installing MemPalace, Beginning Migration]] — primary source for this concept
