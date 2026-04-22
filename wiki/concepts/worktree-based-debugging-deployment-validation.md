---
title: "Worktree-Based Debugging and Deployment Validation"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "3e65ff8540004a023938bd503813baf3709bfc64d1dbcc49c436263dccdc458c"
sources:
  - raw/2026-04-22-copilot-session-graph-incident-and-cleanup-14e5153b.md
quality_score: 100
concepts:
  - worktree-based-debugging-deployment-validation
related:
  - "[[Durable Copilot Session Checkpoint Promotion]]"
  - "[[Clean Worktree-Based Development for Wiki Curation Pipelines]]"
  - "[[Copilot Session Checkpoint: Graph Incident and Cleanup]]"
tier: hot
tags: [debugging, deployment, worktree, ops, tdd, homelab, wiki]
---

# Worktree-Based Debugging and Deployment Validation

## Overview

Worktree-based debugging is a disciplined approach to isolating code and deployment issues by creating clean, branch-specific worktrees for targeted investigation. This method enables developers to separate local code bugs from runtime or deployment drift, validate live server state, and ensure fixes are applied only where necessary.

## How It Works

Worktree-based debugging leverages Git's worktree functionality to create isolated environments for code and deployment troubleshooting. When a problem arises—such as a blank graph UI or a failing cron job—the developer creates a new worktree from the relevant branch (e.g., `origin/main`) to avoid contaminating the root checkout with unrelated changes. This worktree is used to inspect, reproduce, and debug the issue in isolation.

For UI rendering failures, the process begins with tracing the data path from the current main state, inspecting key files (`app.js`, `index.html`, `styles.css`, etc.), and confirming the existence and integrity of data artifacts (like `graph.json`). A local debug harness, such as a temporary HTTP server or jsdom-based runtime, is constructed to validate whether the UI logic is functioning as expected. This harness can simulate draw calls and verify schema compatibility, ensuring that the renderer is not the source of the problem.

If the local renderer is proven healthy, attention shifts to the deployment environment. Subagents (automated scripts or ops tools) are launched to inspect live server state, including mount paths, container wiring, and runtime artifacts. In the documented incident, the root cause was a server mount to a deleted worktree path, resulting in an empty `/app/wiki` and a graph rebuilt with zero nodes and edges. The fix involved fast-forwarding the server-side checkout, redeploying containers, and triggering an internal graph rebuild.

Worktree-based debugging also facilitates systematic cleanup. When retiring obsolete workflows (like a free-tier backfill cron job), the developer creates a dedicated worktree for the cleanup, searches for all references across code, docs, and environment files, and applies targeted diffs. This ensures that only relevant changes are tracked and merged, while temporary artifacts are discarded.

This approach is complemented by test-driven development (TDD) and runtime validation. Before implementing fixes, regression tests are written to reproduce the failure, and local harnesses are used to validate the fix. Only after successful validation are changes committed and merged, maintaining a clean and reliable deployment pipeline.

## Key Properties

- **Isolation of Debugging Environment:** Worktrees allow developers to isolate debugging sessions from the main codebase, preventing contamination and enabling focused investigation.
- **Separation of Code and Deployment Issues:** By validating both local code and live server state, developers can distinguish between code bugs and operational drift.
- **Facilitation of Systematic Cleanup:** Worktrees support targeted removal of obsolete scripts, cron jobs, and documentation, ensuring that only relevant changes are tracked.
- **Support for Test-Driven Development:** Regression tests can be written and validated within isolated worktrees before fixes are implemented, promoting reliability.
- **Deployment Validation:** Live server state is inspected and validated, ensuring that fixes are effective and persistent in production environments.

## Limitations

Worktree-based debugging requires careful management of multiple environments, which can lead to confusion if not documented. It does not address issues arising from complex container orchestration or external dependencies unless those are explicitly included in the worktree setup. Additionally, runtime drift may persist if deployment scripts do not consistently rebuild containers from updated worktrees.

## Example

In this session, the developer created a worktree at `/home/jbl/projects/labs-wiki/.worktrees/graph-ui-render-fix` to debug a blank graph UI. After confirming the renderer was healthy locally, a homelab-ops subagent was used to inspect the live server, revealing a mount to a deleted worktree path. The fix involved fast-forwarding the server checkout, redeploying containers, and rebuilding the graph, restoring node and edge counts.

## Visual

No diagrams or charts are included in the source.

## Relationship to Other Concepts

- **[[Durable Copilot Session Checkpoint Promotion]]** — Both concepts use isolated worktrees and disciplined session tracking for reliable debugging and deployment.
- **[[Clean Worktree-Based Development for Wiki Curation Pipelines]]** — Worktree-based debugging is a foundational practice for clean development and curation pipelines.

## Practical Applications

This approach is essential for debugging complex deployments where code and runtime artifacts may diverge, such as containerized wiki systems, homelab orchestration, and multi-agent workflows. It is especially valuable for retiring obsolete infrastructure, validating UI fixes, and ensuring that production environments reflect intended changes.

## Sources

- [[Copilot Session Checkpoint: Graph Incident and Cleanup]] — primary source for this concept
