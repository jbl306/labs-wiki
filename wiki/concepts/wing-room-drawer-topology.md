---
title: "Wing-Room-Drawer Topology"
type: concept
created: '2026-04-22'
last_verified: '2026-04-22'
sources:
  - raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md
quality_score: 67
concepts:
  - wing-room-drawer-topology
related:
  - "[[milla-jovovich/mempalace]]"
  - "[[palace-memory-architecture]]"
  - "[[closet-index-layer]]"
tier: warm
tags: [memory-architecture, indexing, semantic-organization]
---

# Wing-Room-Drawer Topology

## Overview

The wing-room-drawer topology is MemPalace's hierarchical naming and scoping system for organizing AI memory. Wings partition by person/project, rooms group by topic/time, halls connect related rooms semantically, closets index topics → drawers, drawers hold verbatim content, and tunnels link rooms across wings.

## How It Works

**Wings** are the top-level partitions, representing major domains such as people, projects, or organizations. Examples: `homelab`, `nba_ml_engine`, `copilot_sessions`, `copilot_cli`, `labs_wiki`, `ops`. Queries can be scoped to a wing to prevent cross-project contamination (e.g., `mempalace search "auth bug" --wing homelab` won't surface results from `nba_ml_engine`). Each wing is stored as a metadata filter in ChromaDB.

**Rooms** are topic or time-based groupings within a wing. For project-mined wings, rooms are auto-detected from folder structure using 70+ keyword patterns in `room_detector_local.py` (e.g., `backend`, `frontend`, `auth`, `CI-pipeline`, `billing`). For conversation-mined wings, rooms are day-based by default (e.g., `2026-04-22`) but can be topic-based if content analysis is enabled. Room detection scans the first 5,000 characters of each file. Rooms are mutable — users can override auto-detected names via config.

**Halls** are semantic corridors that connect related rooms within a wing. They are standardized memory types: `hall_facts`, `hall_events`, `hall_discoveries`, `hall_preferences`, `hall_advice`, plus thematic halls like `emotions`, `technical`, `family`, `memory`, `identity`, `consciousness`, `creative`. Halls enable graph-based navigation via `palace_graph.py`. A drawer's hall is determined by content classification during mining (e.g., code goes to `technical`, personal reflections go to `emotions`). Halls support BFS traversal: `mempalace_traverse(start_room="auth-migration", max_hops=2)` walks connected rooms via their shared halls.

**Closets** are the index layer — compact pointers to verbatim drawers. Each closet stores topic-entity-drawer mappings in the format: `topic description|entity1;entity2|→drawer_id_1,drawer_id_2` or `"verbatim quote"|entity1|→drawer_id_3`. Closets are capped at 1,500 characters, with a max of 12 topics, 3 quotes, and 5 entities per source file. Search queries hit closets first (fast scan of small docs), parse the drawer pointers, then hydrate the full verbatim content from the referenced drawers. Closets are stored in the `mempalace_closets` ChromaDB collection and are rebuilt on every mine (no stale topics). See [[closet-index-layer]] for full details.

**Drawers** hold the verbatim content chunks — never summarized, never paraphrased. For project files, drawers are ~800 characters each, chunked by paragraph. For conversations, drawers are exchange-pairs (user message + assistant response). Each drawer is identified by `MD5(content + source_file + chunk_index)` for idempotent writes. Drawers are stored in the `mempalace_drawers` ChromaDB collection with `hnsw:space=cosine` distance (critical — L2 default breaks similarity scoring). Metadata includes wing, room, hall, source_file, chunk_index, entities, and timestamps.

**Tunnels** are explicit cross-wing links for rooms that appear in multiple projects. For example, if `auth-migration` is a room in both the `homelab` wing and the `copilot_sessions` wing (because you discussed it in both contexts), a tunnel connects them. Tunnels enable queries like "show me everything about auth-migration across all wings" via `mempalace_find_tunnels(wing_a="homelab", wing_b="copilot_sessions")`. Tunnels are stored as edges in the palace graph (`palace_graph.py`) and are auto-detected during mining based on room name similarity across wings.

The topology is not static — it evolves as new content is mined. Adding a new project creates a new wing. Adding files to an existing project may create new rooms or populate existing ones. Re-mining a file purges its old closets and drawers, then rebuilds them with fresh content.

## Key Properties

- **Hierarchical scoping**: Wings → Rooms → Drawers enables filtering at each level without post-processing.
- **Auto-detection**: Rooms and halls are inferred from folder paths (70+ patterns) and content analysis.
- **Verbatim storage**: Drawers never summarize — they store the exact original text.
- **Idempotent writes**: Drawer IDs are deterministic (MD5), so re-mining the same content produces the same IDs.
- **Cross-wing linking**: Tunnels connect rooms with the same name across different wings.
- **Index-then-hydrate**: Closets enable fast topic lookup before fetching full verbatim drawers.

## Trade-offs

**Pros**: Scoped retrieval improves precision; hierarchical structure mirrors human project organization; verbatim storage preserves full context; tunnels enable cross-project discovery.

**Cons**: Requires accurate room detection (can misclassify if folder names are ambiguous); closet extraction limited to first 5,000 chars per file; topology complexity increases with scale; manual wing/room overrides require config editing.

## Example

A developer works on three projects: `homelab`, `nba_ml_engine`, `labs_wiki`. Each is a wing. Within `homelab`, rooms include `auth`, `networking`, `docker-compose`. Within `nba_ml_engine`, rooms include `data-pipeline`, `modeling`, `backtest`. The `auth` room in `homelab` contains 47 drawers from files in `homelab/auth/`. A search for "JWT refresh logic" scoped to `wing=homelab, room=auth` hits closets → parses pointers → fetches those exact drawers. A tunnel links `auth` in `homelab` to `auth-notes` in `copilot_sessions` (where the developer discussed it with the AI).

## Relationship to Other Concepts

- **[[palace-memory-architecture]]** — Broader architectural overview; this page focuses on the naming/scoping taxonomy.
- **[[closet-index-layer]]** — Closets are part of the topology; they sit between rooms and drawers.
- **[[milla-jovovich/mempalace]]** — Source project implementing this topology.

## Practical Applications

- Scoped searches prevent cross-project contamination (e.g., "auth bug" in one project won't surface irrelevant results from another).
- Cross-wing queries via tunnels retrieve related context across projects (e.g., "show me all auth decisions").
- Hierarchical structure mirrors developer mental models (project → subsystem → file → chunk).
- Verbatim drawers enable precise quote retrieval for documentation, debugging, and decision rationale.

## Sources

- [[milla-jovovich/mempalace]] — implements the wing-room-drawer topology as described here.
- `docs/CLOSETS.md` in the MemPalace repo — closet layer details.
- `mempalace/palace.py`, `mempalace/searcher.py`, `mempalace/palace_graph.py` — implementation modules.
