---
title: "Copilot Session Checkpoint: Pilot Worktree Baseline"
type: source
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "58f7e891b3f357ec9e293d8dfe365b373ec7a7fbe3eba4e22a93947cc4d024c4"
sources:
  - raw/2026-04-20-copilot-session-pilot-worktree-baseline-10f2a2a8.md
quality_score: 81
concepts:
  - worktree-based-baseline-verification-durable-workflow-pilots
related:
  - "[[Worktree-Based Baseline Verification for Durable Workflow Pilots]]"
  - "[[scripts/auto_ingest.py]]"
tier: hot
checkpoint_class: durable-workflow
retention_mode: retain
tags: [agents, worktree, copilot-session, durable-knowledge, artifact-control, pilot, labs-wiki, baseline-verification, repo-rules, graph, durable-workflow, fileback, checkpoint]
knowledge_state: validated
---

# Copilot Session Checkpoint: Pilot Worktree Baseline

## Summary

This checkpoint documents the transition from planning to execution for the 'URL raw preservation pilot' in the labs-wiki project. The pilot aims to preserve fetched URL/article content directly into raw files, using a quota-safe 3-page approach with validation gates. The session details the creation of a clean worktree, baseline verification, and the technical and procedural constraints that must be addressed before implementation begins.

## Key Points

- Shift from planning/spec work to execution of the URL raw preservation pilot.
- Creation of a dedicated worktree and branch for isolated implementation.
- Baseline verification completed; implementation code changes pending.
- Strict repo rules currently forbid modifying raw files except for status, requiring rule and doc updates.
- Pilot targets three specific raw files, all verified as baseline stubs.

## Concepts Extracted

- **[[Worktree-Based Baseline Verification for Durable Workflow Pilots]]** — Worktree-based baseline verification is a process used to ensure a clean, isolated environment for implementing and validating workflow pilots, such as the URL raw preservation pilot in labs-wiki. This approach leverages git worktrees and branches to avoid accidental commits of unrelated changes, enabling precise control over pilot execution and artifact management. It is especially critical when repo rules enforce strict immutability or deterministic artifact generation.

## Entities Mentioned

- **labs-wiki** — labs-wiki is a knowledge wiki project designed for agentic context engineering, durable session checkpoints, and compile-once ingestion workflows. It enforces strict artifact and workflow rules, including immutability of raw files except for status updates, and supports pilot-driven development through isolated worktrees and branches.
- **[[scripts/auto_ingest.py]]** — scripts/auto_ingest.py is the central ingestion script in labs-wiki, responsible for fetching URL content, processing raw sources, and updating wiki artifacts. It currently supports live-fetching content from various sources but does not persist fetched content back into raw files.

## Notable Quotes

> "Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion." — None
> "Implementation should follow the core spec and current codebase behavior, not blindly the roughest plan fragments." — None

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-20-copilot-session-pilot-worktree-baseline-10f2a2a8.md` |
| Type | note |
| Author | Unknown |
| Date | 2026-04-20 |
| URL | N/A |
