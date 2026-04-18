---
title: "OpenCode Bash Shell Configuration and posix_spawn ENOENT Fix"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "8f16e4e60e551cdd3f674035b1b2a27a6be65980aad74f267605217db5acbc98"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-resource-optimization-opencode-bash-fix-c00d8543.md
quality_score: 100
concepts:
  - opencode-bash-shell-configuration-posix-spawn-enoent-fix
related:
  - "[[Agent-Ergonomic Tool Design Principles]]"
  - "[[Copilot Session Checkpoint: Resource Optimization, Opencode Bash Fix]]"
tier: hot
tags: [opencode, docker, bash, posix_spawn, containerization]
---

# OpenCode Bash Shell Configuration and posix_spawn ENOENT Fix

## Overview

OpenCode containers experienced errors running bash shell commands due to misconfigured shell paths and working directory mismatches. This concept covers the mechanism of shell resolution in OpenCode, the cause of posix_spawn ENOENT errors related to non-existent working directories, and the fixes applied including environment variable setting and symlink creation to resolve path discrepancies between host and container.

## How It Works

OpenCode determines the shell executable to use by first checking the environment variable `SHELL`. If unset or set to a blacklisted shell (like fish or nu), it falls back to locating bash via `which('bash')`, which typically resolves to `/bin/sh` on Linux.

Setting `ENV SHELL=/usr/bin/bash` in the Dockerfile ensures OpenCode uses the correct bash binary path, avoiding fallback to incompatible shells.

The posix_spawn ENOENT error occurs not because the shell binary is missing, but because the working directory (`cwd`) specified for the spawned process does not exist inside the container. In this case, the OpenCode SQLite database stored project paths referencing the host's `/home/jbl/projects/...` directory, but inside the container, projects are mounted at `/home/opencode/projects/...`. When `child_process.spawn()` tries to set `cwd` to a non-existent path, it fails with a misleading error showing the shell path.

The fix was to create a symbolic link inside the container: `/home/jbl → /home/opencode`. This makes the host paths valid inside the container, allowing the spawn call to succeed.

Additionally, the opencode server ignores `server.hostname` and `server.port` settings in the config file, requiring CLI flags `--hostname` and `--port` to be passed explicitly at startup.

## Key Properties

- **Shell Resolution:** Uses `process.env.SHELL` if set and acceptable; fallback uses `which('bash')`.
- **posix_spawn ENOENT Cause:** Occurs when the working directory for the spawned process does not exist, not when the shell binary is missing.
- **Fixes:** Set `ENV SHELL=/usr/bin/bash` in Dockerfiles; create symlink `/home/jbl → /home/opencode` inside container.
- **Config Precedence:** Remote → Global → Custom → Project → Inline; but server hostname/port must be set via CLI flags.

## Limitations

This fix assumes the host and container directory structures can be aligned via symlinks. If paths diverge significantly, additional path remapping or configuration may be necessary. Also, reliance on CLI flags for hostname/port may cause confusion or deployment errors if not documented.

## Example

Dockerfile snippet:
```
ENV SHELL=/usr/bin/bash
RUN ln -s /home/opencode /home/jbl
```

Compose service snippet:
```
env:
  - SHELL=/usr/bin/bash
command: serve --hostname 0.0.0.0 --port 4096
```

This setup ensures bash is used and that working directory paths in the DB are valid inside the container.

## Relationship to Other Concepts

- **[[Agent-Ergonomic Tool Design Principles]]** — Relates to reliable CLI tool configuration and environment setup

## Practical Applications

This concept is critical for containerized development environments and CI/CD pipelines where host and container file paths differ. Correct shell configuration and path alignment prevent runtime errors and improve developer experience when running shell commands inside containers.

## Sources

- [[Copilot Session Checkpoint: Resource Optimization, Opencode Bash Fix]] — primary source for this concept
