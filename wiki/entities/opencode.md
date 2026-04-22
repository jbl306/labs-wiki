---
title: "OpenCode"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "8f16e4e60e551cdd3f674035b1b2a27a6be65980aad74f267605217db5acbc98"
sources:
  - raw/2026-04-18-copilot-session-knightcrawler-done-routing-traced-7bbbddcd.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-reworking-docs-for-copilot-opencode-4710bc64.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-resource-optimization-opencode-bash-fix-c00d8543.md
quality_score: 80
concepts:
  - opencode
related:
  - "[[OpenCode Bash Shell Configuration and posix_spawn ENOENT Fix]]"
  - "[[Copilot Session Checkpoint: Resource Optimization, Opencode Bash Fix]]"
  - "[[KnightCrawler]]"
  - "[[Caddy]]"
tier: hot
tags: [docker, shell, code-execution, container]
---

# OpenCode

## Overview

OpenCode is a code execution and tooling containerized environment used in the homelab for running shell commands and code snippets. It requires precise shell configuration to function correctly, specifically setting the shell path to /usr/bin/bash. The session addressed a critical posix_spawn ENOENT error caused by mismatched working directory paths between host and container, resolved by creating a symlink inside the container. OpenCode's configuration files are managed via mounted JSON configs and environment variables.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | midudev |
| URL | https://github.com/midudev/autoskills |
| Status | Active |
## Relevance

Fixing OpenCode's shell environment and path issues was necessary to restore reliable code execution capabilities in containerized workflows.

## Associated Concepts

- **[[OpenCode Bash Shell Configuration and posix_spawn ENOENT Fix]]** — Directly related to shell and path fixes

## Related Entities

- **[[KnightCrawler]]** — co-mentioned in source (Tool)
- **[[Caddy]]** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Resource Optimization, Opencode Bash Fix]] — where this entity was mentioned
- [[Copilot Session Checkpoint: Reworking Docs for Copilot/OpenCode]] — additional source
- [[Copilot Session Checkpoint: Knightcrawler done, routing traced]] — additional source
