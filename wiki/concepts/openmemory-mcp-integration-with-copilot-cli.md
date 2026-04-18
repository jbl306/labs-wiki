---
title: "OpenMemory MCP Integration with Copilot CLI"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "94a3f24d84af863c5b7181b6b3955f897bb5554330e966d2f452d23543e6b2f4"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-homelab-monitoring-and-knightcrawler-fixes-a62133b0.md
quality_score: 100
concepts:
  - openmemory-mcp-integration-with-copilot-cli
related:
  - "[[Copilot CLI]]"
  - "[[Durable Copilot Session Checkpoint Promotion]]"
  - "[[Copilot Session Checkpoint: Homelab Monitoring and KnightCrawler Fixes]]"
tier: hot
tags: [openmemory, mcp, copilot-cli, memory-integration, persistence]
---

# OpenMemory MCP Integration with Copilot CLI

## Overview

OpenMemory MCP is a memory service providing persistent memory storage and retrieval capabilities via a Model Context Protocol (MCP) server. Integrating OpenMemory MCP with the Copilot CLI enables automated memory management for session data, facilitating recall and knowledge persistence across interactions.

## How It Works

OpenMemory MCP runs as a server exposing an SSE (Server-Sent Events) endpoint that clients like Copilot CLI can connect to for memory operations. The integration involves configuring a JSON file (`~/.copilot/mcp-config.json`) specifying the SSE URL, client name, user, and enabled tools such as `add_memories`, `search_memory`, `list_memories`, and `delete_all_memories`. 

Once configured, the Copilot CLI must be restarted to activate the connection. After activation, the CLI can automatically add memory entries from session findings, search existing memories, list them, or delete them as needed. This enables a persistent knowledge base that grows with user interactions and supports context-aware assistance.

In this session, the user added memory entries covering the KnightCrawler permission bug fix, coverage statistics, cron infrastructure details, and Grafana dashboard information. This structured memory storage supports durable knowledge retention and retrieval for future sessions.

## Key Properties

- **SSE Endpoint:** OpenMemory MCP exposes an SSE endpoint for real-time memory operations.
- **Tools Enabled:** Supports add, search, list, and delete memory operations.
- **Configuration File:** JSON config file specifies endpoint, client, user, and tools.
- **Requires Restart:** Copilot CLI restart is necessary to activate MCP integration.

## Limitations

OpenMemory MCP must be running and reachable for integration to work. Initial state may have zero memories if not connected. Memory operations depend on correct configuration and network accessibility. Without restart, changes do not take effect. The system assumes structured memory entries for effective retrieval.

## Example

Example MCP config file:
```json
{
  "type": "sse",
  "url": "http://localhost:8765/mcp/copilot/sse/jbl",
  "client": "copilot",
  "user": "jbl",
  "tools": ["add_memories", "search_memory", "list_memories", "delete_all_memories"]
}
```
After saving, restart Copilot CLI to enable integration.

## Relationship to Other Concepts

- **[[Copilot CLI]]** — Client tool integrating with OpenMemory MCP
- **[[Durable Copilot Session Checkpoint Promotion]]** — Concept related to persistent session knowledge storage

## Practical Applications

Enables persistent, structured memory for AI-assisted CLI tools, improving context retention and reducing repeated user input. Useful for complex workflows requiring knowledge accumulation and recall. Supports automated documentation and knowledge base growth in agentic environments.

## Sources

- [[Copilot Session Checkpoint: Homelab Monitoring and KnightCrawler Fixes]] — primary source for this concept
