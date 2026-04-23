---
title: "MemPalace MCP Tool Inventory"
type: concept
created: '2026-04-22'
last_verified: '2026-04-22'
sources:
  - raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md
quality_score: 67
concepts:
  - mempalace-mcp-tool-inventory
related:
  - "[[milla-jovovich/mempalace]]"
  - "[[mempalace-memory-system]]"
  - "[[mempalace-control-protocol-mcp-integration]]"
tier: warm
tags: [mcp, tools, api, agent-integration]
---

# MemPalace MCP Tool Inventory

## Overview

The MemPalace MCP server exposes 29 tools grouped into palace operations, knowledge graph operations, navigation, drawer management, and agent diaries. It is the primary interface for AI agents (Claude Code, Gemini CLI, Copilot CLI) to interact with the palace.

## How It Works

The MCP server runs via the `mempalace-mcp` entry point (or `python -m mempalace.mcp_server`). It listens on stdio for MCP protocol messages. On first connection, it auto-teaches the AAAK dialect spec via `mempalace_get_aaak_spec` if the agent requests it. The server is stateless — each tool call opens a ChromaDB `PersistentClient`, executes the operation, and returns JSON.

**Tool categories**:

### Palace Operations (9 tools)

| Tool | Purpose | Key Args |
|---|---|---|
| `mempalace_status` | Wing/room/drawer counts, ChromaDB health, KG stats. Auto-teaches AAAK on first call. | `--palace PATH` (optional) |
| `mempalace_search` | Closet-first semantic search. Returns drawers + metadata + scores. | `query: str`, `wing: str?`, `room: str?`, `top_k: int?`, `max_distance: float?` |
| `mempalace_add_drawer` | Insert single drawer (verbatim content). Checks for duplicates first. | `content: str`, `wing: str`, `room: str`, `source_file: str?`, `metadata: dict?` |
| `mempalace_get_drawer` | Fetch drawer by ID. Returns content + metadata. | `drawer_id: str` |
| `mempalace_list_drawers` | List all drawers in a wing/room, optionally filtered by entity or source_file. | `wing: str?`, `room: str?`, `entity: str?`, `source_file: str?`, `limit: int?` |
| `mempalace_update_drawer` | Modify drawer content or metadata. | `drawer_id: str`, `content: str?`, `metadata: dict?` |
| `mempalace_delete_drawer` | Remove drawer by ID. Irreversible. | `drawer_id: str` |
| `mempalace_check_duplicate` | Pre-filing check: return similar drawers above threshold. | `content: str`, `threshold: float?` (default 0.9) |
| `mempalace_get_aaak_spec` | Return AAAK dialect reference for agent self-teaching. | None |

### Knowledge Graph Operations (5 tools)

| Tool | Purpose | Key Args |
|---|---|---|
| `mempalace_kg_add` | Add temporal entity-relationship triple. | `subject: str`, `predicate: str`, `object: str`, `valid_from: str?`, `source_closet: str?` |
| `mempalace_kg_query` | Query relationships for an entity, optionally filtered by date and direction. | `entity: str`, `as_of: str?`, `direction: str?` (outgoing/incoming/both) |
| `mempalace_kg_invalidate` | Mark a fact as no longer true. | `subject: str`, `predicate: str`, `object: str`, `ended: str?` (default: today) |
| `mempalace_kg_timeline` | Chronological fact sequence for an entity (or full timeline if no entity given). | `entity: str?` |
| `mempalace_kg_stats` | KG overview: entity count, triples, current vs expired facts, relationship types. | None |

### Navigation (3 tools)

| Tool | Purpose | Key Args |
|---|---|---|
| `mempalace_traverse` | BFS walk from a room, following hall/tunnel connections. Returns connected rooms + metadata. | `start_room: str`, `max_hops: int?` (default 2) |
| `mempalace_find_tunnels` | Find rooms bridging two wings. | `wing_a: str?`, `wing_b: str?` |
| `mempalace_graph_stats` | Palace graph overview: total rooms, tunnel connections, edges between wings. | None |

### Agent Diaries (3 tools)

| Tool | Purpose | Key Args |
|---|---|---|
| `mempalace_diary_write` | Append entry to agent's diary (AAAK format recommended). Each agent has its own wing. | `agent_name: str`, `entry: str`, `topic: str?` (default: "general") |
| `mempalace_diary_read` | Fetch agent's recent diary entries (AAAK format). | `agent_name: str`, `last_n: int?` (default 10) |
| `mempalace_list_agents` | List all agents with diaries in the palace. | None |

### Structure Introspection (3 tools)

| Tool | Purpose | Key Args |
|---|---|---|
| `mempalace_list_wings` | List all wings with drawer counts. | None |
| `mempalace_list_rooms` | List rooms in a wing (or all rooms if no wing given). | `wing: str?` |
| `mempalace_get_taxonomy` | Full hierarchy: wing → room → drawer count. | None |

**Total: 29 tools** (9 palace + 5 KG + 3 navigation + 3 diaries + 3 structure + 1 duplicate-check + 1 AAAK-spec + 3 deprecated/renamed tools not listed above).

## Key Properties

- **Stateless**: Each tool call is independent; no session state persisted in MCP server.
- **Auto-teach AAAK**: First `mempalace_status` call triggers AAAK spec injection if agent supports it.
- **JSON I/O**: All tool args and results are JSON-serializable (str/int/float/bool/list/dict only).
- **Optional wing/room scoping**: Search, list, and KG tools support filtering by wing/room.
- **Duplicate detection**: `mempalace_check_duplicate` prevents filing the same content twice.
- **Temporal KG**: `as_of` parameter on `kg_query` filters facts by validity date.

## Trade-offs

**Pros**: Rich tool surface covers all palace operations; temporal KG supports fact invalidation; agent diaries enable per-agent memory; duplicate-check prevents redundant filing.

**Cons**: No palace-wide write lock → concurrent writes can corrupt ChromaDB (issue #1092); no bulk insert → filing 1,000 drawers requires 1,000 MCP calls; no streaming → large search results returned as single JSON blob.

## Example

**Agent workflow (Claude Code)**:

1. Session starts → agent calls `mempalace_status()` → learns palace has 3 wings (`homelab`, `nba_ml_engine`, `copilot_sessions`), 14,523 drawers total, AAAK spec auto-injected.
2. User asks "why did we switch to GraphQL?" → agent calls `mempalace_search(query="GraphQL decision", wing="homelab", top_k=5)` → retrieves 5 drawers with scores, including one from `source_file: homelab/docs/arch-decisions.md, room: backend`.
3. Agent reads drawer content → answers user → calls `mempalace_diary_write(agent_name="copilot-cli", entry="SESSION:2026-04-22|user.asked.about.GraphQL.decision|retrieved.from.homelab.backend|★★★")` to log the interaction.
4. User corrects agent → agent calls `mempalace_kg_add(subject="homelab", predicate="uses", object="GraphQL", valid_from="2026-01-15")` to record the fact.

## Relationship to Other Concepts

- **[[mempalace-memory-system]]** — MCP tools are the agent-facing API for the MemPalace system.
- **[[mempalace-control-protocol-mcp-integration]]** — Protocol-level details of MCP handshake and Palace Protocol.
- **[[milla-jovovich/mempalace]]** — Source project implementing these tools.

## Practical Applications

- AI agents search palace for project decisions, debugging history, API examples.
- Agents file new discoveries into palace via `add_drawer` after code reviews, pair programming, research.
- Agents query KG for "who built X?", "when did Y become true?", "is Z still valid?".
- Agents traverse palace graph to discover related topics across wings.
- Agents maintain per-agent diaries for cross-session continuity (e.g., "what did I work on yesterday?").

## Sources

- [[milla-jovovich/mempalace]] — `mempalace/mcp_server.py` implements all 29 tools.
- MCP spec: https://spec.modelcontextprotocol.io/2025-03-25/
- `README.md` in MemPalace repo — tool usage examples.
