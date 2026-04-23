---
title: "Homelab Infrastructure Patterns for AI Memory Migration"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "d7c9bdfd6b0d2d033db7f2aacc5997a2b254a782eeeec861b84c54e43fa5c867"
sources:
  - raw/2026-04-07-jbl306homelab.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-reworking-docs-for-copilot-opencode-4710bc64.md
quality_score: 79
concepts:
  - homelab-infrastructure-patterns-for-ai-memory-migration
related:
  - "[[MemPalace Architecture and Migration]]"
  - "[[Agent Documentation Hygiene And Migration]]"
  - "[[Copilot Session Checkpoint: Reworking Docs for Copilot/OpenCode]]"
tier: hot
tags: [homelab, infrastructure, deployment, docker, migration, backup]
---

# Homelab Infrastructure Patterns for AI Memory Migration

## Overview

The homelab infrastructure supports the migration from OpenMemory to MemPalace through structured compose files, configuration directories, deployment scripts, and backup rotation policies. This pattern ensures reliable deployment, configuration management, and data retention for AI memory services.

## How It Works

The homelab repository organizes Docker compose files in a `compose/` directory, with a main `compose/docker-compose.yml` that includes service-specific compose files. Configuration files reside in `config/<service>/` directories, and persistent data is stored in `data/<service>/`. Deployment is managed via shell scripts like `deploy.sh`, which define a STACKS array to control service startup order. During migration, the memory stack is removed from the deployment order to reflect the deprecation of OpenMemory.

Backup scripts implement rotation policies with a 30-day retention period to ensure data durability. Validation commands such as `docker compose -f compose/docker-compose.yml --env-file .env config > /dev/null` are used to verify configuration correctness before deployment.

Migration steps include removing OpenMemory containers and configuration files from git, archiving old compose files (e.g., renaming compose.memory.yml to .archived), and updating environment files to remove OpenMemory sections. The MemPalace MCP configuration replaces OpenMemory MCP in the homelab config, and bridge scripts like `mempalace-bridge.sh` facilitate one-way data synchronization from MemPalace to labs-wiki raw sources.

This infrastructure pattern supports clean, maintainable, and reproducible deployments of AI memory backends and their integration with AI agent workflows.

## Key Properties

- **Compose File Organization:** Service-specific compose files in `compose/`, included by main `compose/docker-compose.yml`.
- **Configuration Management:** Service configs in `config/<service>/`, data in `data/<service>/`.
- **Deployment Scripts:** Shell scripts manage deployment order and stack composition.
- **Backup Rotation:** 30-day retention policy for backups.
- **Validation:** Docker compose config validation before deployment.

## Limitations

The migration requires manual cleanup of stale Grafana dashboard panels referencing deprecated OpenMemory containers. Archiving old compose files instead of deleting them may cause confusion if not properly documented. The dependency on shell scripts and environment files requires careful version control and documentation to avoid configuration drift.

## Example

Example deployment script snippet removing memory stack:

```bash
STACKS=(base db web api)
# memory removed
```

Example docker compose validation command:

```bash
docker compose -f compose/docker-compose.yml --env-file .env config > /dev/null
```

Backup script rotation example:

```bash
# rotate backups older than 30 days
find backups/ -type f -mtime +30 -delete
```

## Relationship to Other Concepts

- **[[MemPalace Architecture and Migration]]** — Infrastructure supports deployment and migration of MemPalace.
- **[[Agent Documentation Hygiene And Migration]]** — Infrastructure changes reflect documentation updates and migration hygiene.

## Practical Applications

This infrastructure pattern ensures reliable deployment and management of AI memory services in a homelab environment. It facilitates smooth migration from legacy systems like OpenMemory to modern solutions like MemPalace, supporting continuous integration and delivery of AI agent workflows with persistent memory backends.

## Sources

- [[Copilot Session Checkpoint: Reworking Docs for Copilot/OpenCode]] — primary source for this concept
- [[jbl306/homelab]] — additional source
