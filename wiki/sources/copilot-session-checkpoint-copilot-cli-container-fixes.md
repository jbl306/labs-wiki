---
title: "Copilot Session Checkpoint: Copilot CLI container deployment fixes"
type: source
created: '2026-04-22'
last_verified: '2026-04-22'
source_hash: "b294f67bfd6f7f277718c37fe164f5e5ec5b8a5c4db7beb1d1f8c1d439be29dd"
sources:
  - raw/2026-04-22-copilot-session-copilot-cli-container-deployment-fixes-3fd4b3d0.md
concepts:
  - copilot-cli-backend-wiki-ingestion
  - writable-home-cache-bootstrapping-containerized-cli-tools
related:
  - "[[Copilot CLI]]"
  - "[[GitHub Models API]]"
  - "[[Dockerfile.auto-ingest]]"
  - "[[scripts/auto_ingest.py]]"
  - "[[Homelab]]"
tags: [copilot-session, checkpoint, durable-knowledge, labs-wiki, auto-ingest, copilot-cli, docker, homelab]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 78
checkpoint_class: project-progress
retention_mode: compress
---

# Copilot Session Checkpoint: Copilot CLI container deployment fixes

## Summary

This checkpoint records the migration of Labs-Wiki's `wiki-auto-ingest` container from a [[GitHub Models API]] compile path to a [[Copilot CLI]]-driven backend. It captures two operational fixes that made the backend viable in Docker: installing the real `copilot` binary instead of relying on the `gh copilot` launcher alone, and giving the container a writable HOME/cache path so the CLI's runtime extraction could succeed under uid 1000.

## Key Points

- **Backend switch**: the ingest pipeline is now intended to use `gh copilot -p` as the default LLM compile path rather than direct GitHub Models HTTP calls.
- **Launcher trap**: `gh copilot` was present in the container, but the command still failed because the launcher expects the actual `copilot` binary on `PATH`.
- **Concrete fix**: `Dockerfile.auto-ingest` was updated to install Node 22 and `npm install -g @github/copilot`, which placed the `copilot` executable at `/usr/bin/copilot`.
- **Noninteractive container constraint**: auto-download behavior that might work on a developer machine is unreliable inside the ingest container, so the CLI binary must be baked into the image.
- **Permission failure**: once the binary existed, the next blocker was `EACCES: permission denied, mkdir '/.cache'`, caused by the container running with `HOME=/`.
- **HOME/cache remedy**: the container now sets `HOME=/tmp/copilot-home` and pre-creates `/tmp/copilot-home/.cache` so the Copilot CLI can unpack its runtime state.
- **Runtime assumption exposed**: the checkpoint notes that Copilot CLI behaves like a single-executable app that still needs writable per-user cache space even when the main binary is installed globally.
- **Validation signal**: a smoke test returned `PONG`, showing the containerized Copilot path worked end to end after the image and filesystem changes.
- **Cost observability**: the CLI output footer reports request class and runtime, making premium-request consumption visible during ingest validation.
- **Source-type gap**: HTML validation was in flight, but explicit PDF and image raws were still missing from the corpus, leaving multimodal backend coverage incomplete.

## Key Concepts

- [[Copilot CLI Backend for Wiki Ingestion]]
- [[Writable HOME and Cache Bootstrapping for Containerized CLI Tools]]
- [[Source-Aware Model Routing in Wiki Ingestion Pipelines]]

## Related Entities

- **[[Copilot CLI]]** — The command-line model interface now used as the compile backend inside the ingest container.
- **[[GitHub Models API]]** — The prior backend that this checkpoint implicitly contrasts against on authentication, cost reporting, and runtime assumptions.
- **[[Dockerfile.auto-ingest]]** — The build artifact that absorbed the binary-install and writable-HOME fixes.
- **[[scripts/auto_ingest.py]]** — The pipeline entrypoint that dispatches the ingest workflow and now depends on the new backend behavior.
- **[[Homelab]]** — The deployment environment where the rebuilt `wiki-auto-ingest` container was validated.
