---
title: "Migration from OpenMemory to MemPalace"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "b467128355ad46633de12b9a2a90526c0641bff2b8a228c3bbd2cb733e3ad37b"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-installing-mempalace-beginning-migration-f4a540d2.md
quality_score: 100
concepts:
  - migration-from-openmemory-to-mempalace
related:
  - "[[MemPalace Memory System]]"
  - "[[OpenMemory]]"
  - "[[MCP (MemPalace Control Protocol)]]"
  - "[[Labs-Wiki]]"
  - "[[Copilot Session Checkpoint: Installing MemPalace, Beginning Migration]]"
tier: hot
tags: [migration, openmemory, mempalace, homelab, ai-memory]
---

# Migration from OpenMemory to MemPalace

## Overview

The migration process involves transitioning AI memory data and infrastructure from OpenMemory, a Docker-based memory system, to MemPalace, a native pip-installed memory system. This migration is critical for improving system maintainability, security, and integration with newer tools like labs-wiki.

## How It Works

The migration begins with a comprehensive evaluation and planning phase, documented in mempalace-evaluation.md and mempalace-migration.md, which outline a 7-phase migration plan with progress tracking and decision tables.

Key steps include:

1. Inventorying existing OpenMemory data by listing all 55 memories via the MCP list_memories tool, categorizing them by domain (e.g., NBA-ML, KnightCrawler, Wiki).
2. Installing MemPalace natively using pipx, initializing the palace structure for the homelab project, and mining existing project files into MemPalace's palace storage.
3. Creating configuration and identity files for MemPalace to establish the memory context and system paths.
4. Planning and implementing MCP configuration changes to replace OpenMemory's MCP server (SSE transport) with MemPalace's MCP server (stdio transport).
5. Developing a migration script to export memories from OpenMemory and import them into a dedicated 'openmemory-archive' wing within MemPalace, ensuring sensitive data like Grafana admin credentials are carefully handled.
6. Updating homelab infrastructure files to remove OpenMemory Docker services and replace backup and deployment scripts with MemPalace-compatible versions.
7. Validating the migration by testing MemPalace search and MCP functionality, ensuring the bridge to labs-wiki is operational, and performing full system tests.

The migration emphasizes a one-way bridge from MemPalace to labs-wiki to maintain conversational memory insights as raw sources in the knowledge base. The approach also includes removing OpenMemory-related configuration files and Docker compose includes to fully retire the old system.

## Key Properties

- **Phased Migration Plan:** Seven phases including planning, installation, configuration, migration, bridging, infrastructure update, and validation.
- **Memory Inventory:** 55 OpenMemory memories categorized and listed for migration.
- **Infrastructure Changes:** Removal of OpenMemory Docker services and configuration, replacement with MemPalace native install.
- **Bridge Implementation:** One-way bridge from MemPalace to labs-wiki for conversational memory integration.

## Limitations

Migration requires careful handling of sensitive data stored in memories, such as credentials. OpenMemory containers must be stopped and data verified accessible before migration. The migration script and bridge are custom implementations requiring maintenance. The transition from SSE to stdio MCP transport may affect integration with existing tools. Some configuration files and scripts require manual updates, which may introduce errors if not carefully managed.

## Example

Migration todo tracker snippet (SQL style):

```sql
-- Migration steps with progress
[x] plan-homelab
[~] install-mempalace
[ ] configure-mcp
[ ] migrate-memories
[ ] bridge-labswiki
[ ] homelab-config
[ ] homelab-docs
[ ] remove-openmemory
[ ] validate-test
[ ] next-steps-doc
```

This tracker guides the migration workflow from planning to final validation.

## Relationship to Other Concepts

- **[[MemPalace Memory System]]** — Target system for migration.
- **[[OpenMemory]]** — Source system being migrated from.
- **[[MCP (MemPalace Control Protocol)]]** — Protocol used for memory management in both systems, with different transports.
- **[[Labs-Wiki]]** — Destination for conversational memory insights after migration.

## Practical Applications

This migration process is applicable for organizations or individuals maintaining AI memory systems who want to transition from containerized, Docker-based solutions to lightweight, native installations for better performance, security, and integration. It supports continuity of AI memory data and enables leveraging newer memory architectures and tooling.

## Sources

- [[Copilot Session Checkpoint: Installing MemPalace, Beginning Migration]] — primary source for this concept
