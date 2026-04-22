---
title: "Worktree-Based Subagent-Driven Development"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "358108ea4d82e3accc5cb671afd3dec27dfb9c5dae571d0970c1b790078c615e"
sources:
  - raw/2026-04-20-copilot-session-integrating-agent-skill-routing-3f817cb6.md
quality_score: 79
concepts:
  - worktree-based-subagent-driven-development
related:
  - "[[Phased Implementation Planning and Progress Tracking for LLM Wikis]]"
  - "[[Agent Documentation Hygiene And Migration]]"
  - "[[Copilot Session Checkpoint: Integrating Agent Skill Routing]]"
tier: hot
tags: [worktree, subagent, development-workflow, integration, review, git]
---

# Worktree-Based Subagent-Driven Development

## Overview

Worktree-based subagent-driven development is a workflow pattern that leverages git worktrees and subagent task execution to isolate feature branches, enable parallel development, and ensure safe integration of complex changes across multiple repositories. This approach is particularly suited for agent-system projects requiring modular skill integration and iterative review.

## How It Works

The workflow begins by setting up isolated git worktrees for each repository involved in the integration. Worktrees are directories linked to specific branches, allowing developers to work on multiple features in parallel without interfering with the main branch. In this integration, worktrees were created for homelab, nba-ml-engine, and labs-wiki, each on the branch 'feat/context-engineering-skills'. Gitignore files were updated to prevent worktree directories from being tracked, ensuring clean repo histories.

Subagent-driven development refers to delegating implementation tasks to specialized subagents (automated or human), who execute discrete steps in the integration plan. Each task—such as importing upstream skills, wiring shared workspace discovery, syncing OpenCode configs, and updating repo-local routing—is assigned to a subagent. After completion, the work is reviewed for spec compliance and quality, with findings sent back for fixes as needed.

This pattern enables modular, incremental progress. For example, Task 1 (import upstream skills) was completed and reviewed before Task 2 (shared workspace wiring) began. Each task is tracked and documented, with commits made in the relevant worktree branches. Baseline checks (linting, test runs) are performed in each worktree to ensure integration does not break existing functionality. Known issues (such as pre-existing test failures in nba-ml-engine) are explicitly accepted or deferred based on user input.

The workflow supports safe experimentation and rollback. Because worktrees are isolated, developers can test changes, run validation scripts, and iterate on fixes without risking the stability of the main branch. Once tasks are approved, changes can be merged into the main branch. This is especially important in agent-system projects, where skill integration can affect multiple tool surfaces and workflows.

Documentation is created and updated throughout the process, including design specs, implementation plans, and validation reports. Each worktree contains the relevant files, and progress is tracked via SQL todos and session checkpoints. The workflow is robust against baseline quirks (missing .env files, container path resolution issues) and allows for explicit user acceptance of unresolved issues.

## Key Properties

- **Isolated Feature Branches:** Worktrees allow development on isolated branches, preventing interference with the main branch and enabling parallel progress.
- **Subagent Task Execution:** Tasks are delegated to subagents, who execute, review, and iterate on discrete steps in the integration plan.
- **Iterative Review and Fix Loops:** Each task undergoes spec and quality reviews, with findings sent back for fixes until approved.
- **Baseline Validation:** Linting and test runs are performed in each worktree to ensure integration does not break existing functionality.
- **Explicit Acceptance of Unresolved Issues:** Known baseline quirks or failures can be accepted or deferred based on user input, maintaining focus on integration scope.

## Limitations

Worktree directories must be carefully managed and ignored in git to prevent repo pollution. The workflow relies on disciplined task tracking and review; missed steps or poor documentation can lead to integration errors. Baseline validation is only as robust as the existing test coverage; unresolved issues may persist if not explicitly addressed.

## Example

Worktree setup example:

- homelab/.worktrees/context-engineering-skills (branch: feat/context-engineering-skills)
- nba-ml-engine/.worktrees/context-engineering-skills (branch: feat/context-engineering-skills)
- labs-wiki/.worktrees/context-engineering-skills (branch: feat/context-engineering-skills)

Gitignore updates:
- homelab/.gitignore: added .worktrees/
- nba-ml-engine/.gitignore: added .worktrees/

Task execution:
- Task 1: Import upstream skills
- Task 2: Wire shared workspace
- Task 3: Sync OpenCode configs
- Task 4: Update homelab routing

Each task is completed, reviewed, and documented in the relevant worktree branch.

## Visual

No diagrams or charts are included in the source.

## Relationship to Other Concepts

- **[[Phased Implementation Planning and Progress Tracking for LLM Wikis]]** — Both involve structured, incremental workflows for complex project integration.
- **[[Agent Documentation Hygiene And Migration]]** — Worktree-based development supports documentation hygiene by isolating changes and tracking progress.

## Practical Applications

This workflow is ideal for large-scale agent-system projects, collaborative AI development, and modular skill integration. It enables safe experimentation, parallel progress, and robust review processes, reducing risk and improving integration quality.

## Sources

- [[Copilot Session Checkpoint: Integrating Agent Skill Routing]] — primary source for this concept
