---
title: "MemPalace Memory System"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "b467128355ad46633de12b9a2a90526c0641bff2b8a228c3bbd2cb733e3ad37b"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-researching-mempalace-for-comparison-doc-50987160.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-installing-mempalace-beginning-migration-f4a540d2.md
quality_score: 100
concepts:
  - mempalace-memory-system
related:
  - "[[OpenMemory]]"
  - "[[MCP (MemPalace Control Protocol)]]"
  - "[[Labs-Wiki]]"
  - "[[Copilot Session Checkpoint: Installing MemPalace, Beginning Migration]]"
tier: hot
tags: [ai-memory, mempalace, chroma-db, pipx, local-storage]
---

# MemPalace Memory System

## Overview

MemPalace is a native, pip-installable AI memory system designed for local filesystem access without requiring Docker or external API keys. It serves as a conversational memory layer that integrates with knowledge compilation systems like labs-wiki, enabling efficient memory management and retrieval in AI workflows.

## How It Works

MemPalace operates by organizing knowledge into a 'palace' structure stored locally, using ChromaDB as its persistent vector storage backend. The system is initialized by scanning a project directory to detect entities and create configuration files such as mempalace.yaml and entities.json. The 'mine' command ingests files from the project directory into the palace, distributing content into 'drawers' within 'rooms' that represent logical groupings of information.

The palace data resides in the user's home directory under ~/.mempalace/palace/, with configuration and identity files stored in ~/.mempalace/config.json and ~/.mempalace/identity.txt respectively. The identity file represents the L0 memory layer and contains a small tokenized context (~100 tokens) that is always loaded to provide foundational context.

MemPalace includes an MCP (MemPalace Control Protocol) server accessible via stdio transport, exposing 19 tools for interaction and management. This design avoids the need for Docker containers or external embedding API keys, simplifying deployment and enhancing security.

The system uses a ChromaDB embedding model (all-MiniLM-L6-v2, 384 dimensions) that is automatically downloaded on first use. This embedding model enables semantic search and retrieval within the palace. MemPalace's architecture supports multiple 'rooms' and 'drawers', allowing fine-grained organization and scalable memory management.

The migration from OpenMemory involves creating an 'openmemory-archive' wing within MemPalace to house legacy memories, ensuring continuity and data preservation. The system's native install approach leverages pipx to create isolated virtual environments, complying with Python environment management policies such as PEP 668 on Ubuntu 24.04.

## Key Properties

- **Installation:** Installed via pipx to create isolated virtual environments, avoiding conflicts with system Python and adhering to PEP 668.
- **Storage Backend:** Uses ChromaDB for persistent vector storage of embedded memory content.
- **Configuration Files:** Includes mempalace.yaml (room and drawer structure), entities.json (detected entities), config.json (palace path and collection name), and identity.txt (L0 memory context).
- **MCP Server:** Exposes 19 tools over stdio transport for memory management and integration.
- **Embedding Model:** Uses all-MiniLM-L6-v2 embedding model (384 dimensions) auto-downloaded on first use.

## Limitations

MemPalace currently requires local filesystem access and is designed for native installation; it does not support Docker-based deployment. The system depends on ChromaDB embeddings, which may limit embedding model flexibility. Sensitive data migration requires careful handling, especially credentials stored in memories. The MCP server uses stdio transport, which may limit remote or networked access scenarios.

## Example

Example MemPalace usage commands:

```bash
pipx install mempalace
mempalace init ~/projects/homelab --yes
mempalace mine ~/projects/homelab
mempalace mcp
```

This sequence installs MemPalace, initializes the palace structure for the homelab project, mines files into the palace, and launches the MCP server for interaction.

## Relationship to Other Concepts

- **[[OpenMemory]]** — MemPalace is the native replacement for the Docker-based OpenMemory system.
- **[[MCP (MemPalace Control Protocol)]]** — MemPalace exposes memory management tools via MCP server.
- **[[Labs-Wiki]]** — MemPalace integrates with labs-wiki for knowledge compilation and conversational memory bridging.

## Practical Applications

MemPalace is used to manage AI agent conversational memory locally, enabling persistent, semantic memory storage without reliance on cloud APIs or Docker. It supports migration from legacy memory systems like OpenMemory and facilitates integration with knowledge bases such as labs-wiki. This makes it suitable for homelab environments, research projects, and AI workflows requiring robust local memory management.

## Sources

- [[Copilot Session Checkpoint: Installing MemPalace, Beginning Migration]] — primary source for this concept
- [[Copilot Session Checkpoint: Researching MemPalace for Comparison Doc]] — additional source
