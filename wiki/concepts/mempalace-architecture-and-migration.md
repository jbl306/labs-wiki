---
title: "MemPalace Architecture and Migration"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "d7c9bdfd6b0d2d033db7f2aacc5997a2b254a782eeeec861b84c54e43fa5c867"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-reworking-docs-for-copilot-opencode-4710bc64.md
quality_score: 100
concepts:
  - mempalace-architecture-and-migration
related:
  - "[[OpenMemory MCP Integration with Copilot CLI]]"
  - "[[Agent Documentation Hygiene And Migration]]"
  - "[[Copilot Session Checkpoint: Reworking Docs for Copilot/OpenCode]]"
tier: hot
tags: [mempalace, ai-memory, migration, mcp, copilot-cli, opencode]
---

# MemPalace Architecture and Migration

## Overview

MemPalace is a native Python-based AI memory system that replaces the Docker-based OpenMemory. It uses ChromaDB for persistent vector storage and communicates via a JSON-RPC protocol over stdio. Migrating to MemPalace involves initializing a palace, mining project data into it, and updating MCP configurations for AI agents.

## How It Works

MemPalace stores knowledge in a 'palace' directory, which is a persistent vector database powered by ChromaDB embedding model all-MiniLM-L6-v2. The palace data resides at ~/.mempalace/palace/. Configuration and identity files are stored at ~/.mempalace/config.json and ~/.mempalace/identity.txt respectively. The MCP (MemPalace Control Protocol) server is launched using the command `python -m mempalace.mcp_server`, which exposes 19 tools such as status, search, drawer management, knowledge graph queries, and agent diaries. Communication with MCP is via JSON-RPC over stdio, which allows integration with AI agents like Copilot CLI and OpenCode.

Migration from OpenMemory to MemPalace involves several steps: first, the user initializes MemPalace in the project directory using `mempalace init <dir> --yes`, which creates mempalace.yaml and entities.json files that should be gitignored. Then, `mempalace mine <dir>` ingests data into the palace. The migration script uses JSON-RPC calls to transfer memories from OpenMemory to MemPalace, placing them into an `openmemory_archive` wing with multiple rooms. During migration, some memories are skipped for security reasons (e.g., credentials), and duplicates or low-value memories may be excluded.

The MCP configuration files for Copilot CLI and OpenCode are updated to point to the MemPalace MCP server using stdio transport and the pipx-managed Python virtual environment. This ensures seamless integration of AI coding tools with the new memory backend. The migration also requires infrastructure updates in homelab, such as removing OpenMemory containers and references, updating Docker compose files, deployment scripts, and backup rotation to reflect MemPalace usage.

Key gotchas include the need to use pipx for Python package management on Ubuntu 24.04 due to PEP 668 restrictions, the absence of a `mempalace mcp` subcommand (requiring the use of `python -m mempalace.mcp_server`), and the archival (not deletion) of old compose.memory.yml files for reference. Grafana dashboards referencing OpenMemory containers remain but show empty panels until cleaned up.

## Key Properties

- **Storage:** Uses ChromaDB vector database with all-MiniLM-L6-v2 embedding model (384 dimensions).
- **Communication Protocol:** JSON-RPC over stdio transport for MCP server tools.
- **MCP Tools:** 19 tools including status, search, drawer management, knowledge graph queries, and agent diaries.
- **Migration Coverage:** Migrated 49 of 55 OpenMemory memories; some skipped for security or duplication.
- **Python Environment:** Managed via pipx virtual environment; direct pip install not recommended on Ubuntu 24.04.

## Limitations

The MCP server lacks a dedicated subcommand (`mempalace mcp`), requiring manual invocation via Python module. Migration may skip sensitive or duplicate memories, potentially causing incomplete data transfer. Grafana dashboards and other monitoring tools need manual cleanup post-migration to remove stale references. The system depends on external Python environment management which can complicate deployment if not handled properly.

## Example

Migration script pseudocode for transferring OpenMemory drawers to MemPalace via JSON-RPC:

```python
initialize_mcp()
for drawer in openmemory_drawers:
    if drawer.is_sensitive():
        continue
    mcp.call('tools/add_drawer', drawer.data)
```

MCP server start command:

```bash
python -m mempalace.mcp_server
```

MCP config snippet for Copilot CLI (~/.copilot/mcp-config.json):

```json
{
  "transport": "stdio",
  "python_binary": "/home/jbl/.local/share/pipx/venvs/mempalace/bin/python"
}
```

## Relationship to Other Concepts

- **[[OpenMemory MCP Integration with Copilot CLI]]** — MemPalace replaces OpenMemory as the AI memory backend integrated via MCP.
- **[[Agent Documentation Hygiene And Migration]]** — Migration involves updating documentation references and configurations.

## Practical Applications

MemPalace serves as a persistent, scalable AI memory system for multi-agent workflows, enabling advanced knowledge graph queries, drawer management, and integration with AI coding tools like Copilot CLI and OpenCode. Its migration from OpenMemory allows for a more native Python environment, improved tooling, and better integration with existing infrastructure. This is critical for maintaining durable session checkpoints, enabling conversation mining, and supporting auto-save hooks in AI agent workflows.

## Sources

- [[Copilot Session Checkpoint: Reworking Docs for Copilot/OpenCode]] — primary source for this concept
