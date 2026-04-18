---
title: "OpenMemory"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "61d2a663201be1287914b264819f16b9d6d4bbee33865442f2be9300278c25db"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-reworking-docs-for-copilot-opencode-4710bc64.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-researching-mempalace-for-comparison-doc-50987160.md
  - raw/2026-04-18-copilot-session-nba-ml-oom-fix-and-docs-cleanup-52d24b9f.md
quality_score: 100
concepts:
  - openmemory
related:
  - "[[Agent Documentation Hygiene And Migration]]"
  - "[[Copilot Session Checkpoint: NBA ML OOM Fix And Docs Cleanup]]"
  - "[[MemPalace]]"
  - "[[NBA-ML Model Registry]]"
tier: hot
tags: [memory, deprecated, docker, qdrant, mcp]
---

# OpenMemory

## Overview

OpenMemory was a Docker-based memory stack comprising Qdrant, MCP, and a UI, previously used in the homelab and labs-wiki repos. It has been deprecated and replaced by MemPalace, with all references removed from documentation and service tables.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Deprecated |

## Relevance

OpenMemory's deprecation reflects a migration to more streamlined, local memory protocols (MemPalace). Its removal from documentation and architecture diagrams reduces technical debt and confusion.

## Associated Concepts

- **[[Agent Documentation Hygiene And Migration]]** — OpenMemory references were systematically removed during documentation hygiene and migration.

## Related Entities

- **[[MemPalace]]** — Replacement for OpenMemory in agent workflows.
- **[[NBA-ML Model Registry]]** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: NBA ML OOM Fix And Docs Cleanup]] — where this entity was mentioned
- [[Copilot Session Checkpoint: Researching MemPalace for Comparison Doc]] — additional source
- [[Copilot Session Checkpoint: Reworking Docs for Copilot/OpenCode]] — additional source
