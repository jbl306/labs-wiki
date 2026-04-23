---
title: "Dockerfile.auto-ingest"
type: entity
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "b294f67bfd6f7f277718c37fe164f5e5ec5b8a5c4db7beb1d1f8c1d439be29dd"
sources:
  - raw/2026-04-22-copilot-session-copilot-cli-container-deployment-fixes-3fd4b3d0.md
concepts: [copilot-cli-backend-wiki-ingestion, writable-home-cache-bootstrapping-containerized-cli-tools]
related:
  - "[[Copilot CLI]]"
  - "[[scripts/auto_ingest.py]]"
  - "[[Docker]]"
  - "[[Homelab]]"
tier: hot
tags: [docker, auto-ingest, copilot-cli, container, build-config]
quality_score: 50
---

# Dockerfile.auto-ingest

## Overview

`Dockerfile.auto-ingest` is the container build specification for the Labs-Wiki `wiki-auto-ingest` service. It matters because the ingest pipeline's real behavior is constrained less by prompt logic than by what the image actually contains: runtime binaries, writable directories, environment defaults, and ownership assumptions.

In this checkpoint, the file becomes the decisive operational surface for a backend migration. The pipeline had already been updated to invoke Copilot CLI, but the container still failed until the Dockerfile explicitly installed `@github/copilot`, set a writable `HOME`, and provisioned cache directories that the CLI expects during startup.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Build Configuration |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Role in the Ingest Stack

The file defines the execution environment for `wiki-auto-ingest`, the sidecar that watches `raw/` and runs the compile step. That makes it the boundary between abstract pipeline design and deployable reality: if the Dockerfile omits a dependency or assumes the wrong filesystem layout, even a correct prompt and script will still fail in production.

This checkpoint shows that dynamic behavior in `scripts/auto_ingest.py` depended on static image guarantees. `gh copilot -p` looked available because GitHub CLI was installed, but the image still lacked the `copilot` executable that the launcher delegates to. The Dockerfile fix made the backend executable in the literal sense, not just the logical sense.

## Copilot CLI Bootstrapping

The most important change was adding Node 22 plus a global `npm install -g @github/copilot`. That moved the image from "GitHub CLI present" to "Copilot CLI actually runnable." In a laptop workflow, a user might rely on one-time install flows or home-directory downloads; in a containerized watcher, the binary must be present without any interactive setup path.

By baking the CLI into the image, `Dockerfile.auto-ingest` turns backend selection into a reproducible deployment property. Rebuilding the image is now the mechanism that carries the backend into production, which is exactly what the checkpoint's deploy-and-smoke-test loop verified.

## Writable HOME and Cache Fix

The second change is more subtle but equally important: setting `HOME=/tmp/copilot-home` and pre-creating a writable `.cache` directory. The checkpoint documents an `EACCES` failure on `mkdir '/.cache'`, which happened because the container ran as uid 1000 while `HOME` effectively resolved to `/`.

That error reveals a common container pitfall: globally installed CLIs may still need per-user writable state for startup, extraction, or caching. In this case the Copilot CLI's packaged runtime needed somewhere to unpack itself. The Dockerfile fix converts a fragile implicit dependency into an explicit filesystem contract.

## Operational Impact

After these changes, the checkpoint records a successful `PONG` smoke test from inside the rebuilt container and notes that the auto-ingest service resumed processing pending raws. That makes `Dockerfile.auto-ingest` more than build metadata; it is the durable artifact that encoded the deployment fix and restored the ingestion system's ability to compile sources through Copilot CLI.

For future operators, the file is also the place to reason about backend portability, writable paths, and dependency drift. If the ingest stack changes model backends again, this Dockerfile will likely be the first artifact that must change to make the transition real.
