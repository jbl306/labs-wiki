---
title: "Writable HOME and Cache Bootstrapping for Containerized CLI Tools"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "b294f67bfd6f7f277718c37fe164f5e5ec5b8a5c4db7beb1d1f8c1d439be29dd"
sources:
  - raw/2026-04-22-copilot-session-copilot-cli-container-deployment-fixes-3fd4b3d0.md
related:
  - "[[Docker]]"
  - "[[Copilot CLI]]"
  - "[[Copilot CLI Backend for Wiki Ingestion]]"
  - "[[Auto-Ingest Pipeline for LLM-Powered Knowledge Wiki]]"
  - "[[Dockerfile.auto-ingest]]"
tier: hot
tags: [docker, containers, permissions, cache, cli, runtime]
---

# Writable HOME and Cache Bootstrapping for Containerized CLI Tools

## Overview

Writable HOME and cache bootstrapping is the practice of explicitly provisioning a user-writable home directory and cache path inside a container before running developer-oriented CLI tools. It matters because many modern CLIs appear to be single binaries but still unpack assets, write state, or initialize runtime files under `$HOME`, which can fail immediately in minimal container environments.

## How It Works

The problem starts with a mismatch between tool assumptions and container defaults. Many command-line tools are built first for interactive developer machines, where a normal user account, writable home directory, and standard cache layout are taken for granted. Containers often remove those guarantees: processes may run as a numeric uid with no named user, application directories may be read-only, and `HOME` may be unset or point somewhere like `/` that is not writable for the active uid.

The checkpoint demonstrates this with Copilot CLI. After the ingest image gained the correct binary, the next startup failure was `EACCES: permission denied, mkdir '/.cache'`. That error tells a precise story. The tool did not fail because of missing tokens or prompt logic; it failed because it tried to initialize user cache state under a location derived from `HOME`, and in the container that resolved to a root-level path the runtime user could not create.

The fix is to make the writable contract explicit in the image itself. Instead of hoping the runtime environment supplies a safe home directory, the Dockerfile sets `HOME=/tmp/copilot-home`, creates `/tmp/copilot-home/.cache`, and ensures the path is writable before the process ever starts. `/tmp` is a strong choice in constrained images because it is the one path most operators already expect to be writable, even when application code and mounted repositories are read-only.

This pattern is especially important for packaged or bundled CLIs that behave like a single executable application. Even when the binary lives in `/usr/bin`, the tool may still extract supporting assets, caches, or transient runtime files on first launch. The checkpoint explicitly notes that Copilot CLI behaves this way. In other words, "binary installed" is only half of bootstrapping; the other half is giving the binary a writable place to become fully operational.

There is also a reliability benefit to doing this at build time rather than reacting to failures at runtime. If the directory is created and environment variables are set in the Dockerfile, every rebuilt image carries the same invariant into deployment. That is far more reproducible than asking the entrypoint script to repair permissions on the fly or depending on host-specific volume ownership. For unattended services such as `wiki-auto-ingest`, reproducibility matters more than clever recovery logic because the system has no human nearby to answer prompts or fix directories interactively.

The pattern generalizes beyond Copilot CLI. Any containerized tool that uses package managers, embedded runtimes, browser bundles, model caches, or credential helpers may need the same treatment. The concrete details differ, but the operational checklist stays stable: identify where the tool writes state, point `HOME` or equivalent environment variables at a writable location, pre-create expected subdirectories, and make those assumptions visible in the image rather than hiding them in tribal knowledge.

The deeper lesson is that filesystem design is part of application design in containerized automation. A pipeline may be logically correct and still fail if it assumes laptop-style user directories. Writable HOME bootstrapping turns those assumptions into explicit infrastructure, which is why it often appears as the decisive fix in otherwise mysterious "works on host, fails in container" incidents.

## Key Properties

- **Explicit user-state contract**: Makes the tool's expected writable paths visible in the image.
- **Build-time reproducibility**: Encodes the fix in Docker rather than depending on ad hoc runtime repair.
- **Minimal writable surface**: Uses a narrow path such as `/tmp/copilot-home` instead of broad write access across the filesystem.
- **Compatibility with numeric UIDs**: Works even when the container runs as uid 1000 without a full user account setup.
- **Reusable operational pattern**: Applies to many CLIs beyond Copilot CLI.

## Limitations

This pattern does not solve every permission problem. Mounted volumes may still have incompatible ownership, and some tools also need writable config or credential directories outside `.cache`. Using permissive modes such as `777` can be operationally convenient but should be weighed against the container's threat model. Finally, a writable HOME fixes startup assumptions, not missing binaries or invalid authentication.

## Examples

```dockerfile
ENV HOME=/tmp/copilot-home
RUN mkdir -p /tmp/copilot-home/.cache \
    && chmod 777 /tmp/copilot-home /tmp/copilot-home/.cache
```

That snippet is the minimal pattern: define a safe home, create the expected cache directory, and do it before the container starts the service that depends on it.

## Practical Applications

Use this pattern when packaging AI CLIs, browser automation tools, bundlers, or any other developer-facing binary into unattended containers. It is particularly valuable in homelab sidecars, cron-driven jobs, and file-watcher services where failures must be prevented by image design rather than corrected manually after deployment.

## Related Concepts

- **[[Copilot CLI Backend for Wiki Ingestion]]**: A concrete ingest backend whose viability depended on this bootstrapping pattern.
- **[[Auto-Ingest Pipeline for LLM-Powered Knowledge Wiki]]**: The larger service architecture that exposed the HOME/cache assumption.
- **[[Docker]]**: The containerization substrate where writable-path assumptions must be made explicit.
