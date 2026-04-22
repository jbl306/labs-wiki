---
title: "Clean Worktree-Based Development for Wiki Curation Pipelines"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "4f6f78933f56d8ae7e529c0883a3bea68f61cc64465402d8aa421afc538919d5"
sources:
  - raw/2026-04-20-copilot-session-second-curation-reports-23bcd48f.md
quality_score: 46
concepts:
  - clean-worktree-based-development-wiki-curation-pipelines
related:
  - "[[Phased Implementation Planning and Progress Tracking for LLM Wikis]]"
  - "[[Copilot Session Checkpoint: Second Curation Reports]]"
tier: hot
tags: [git, worktree, development-workflow, wiki-curation, branch-management]
---

# Clean Worktree-Based Development for Wiki Curation Pipelines

## Overview

Clean worktree-based development is a workflow strategy for managing complex, multi-branch changes in large wiki or code repositories. By using isolated git worktrees for each feature or report update, developers can avoid conflicts with untracked or generated files in the main checkout, ensure reproducibility, and streamline branch management and code review.

## How It Works

In repositories with heavy automation or content generation (such as auto-ingested wikis), the main branch checkout can quickly become 'dirty'—filled with untracked, generated, or intermediate files. Editing or merging directly in this environment risks accidental inclusion of unwanted changes, merge conflicts, or even data loss.

The clean worktree-based approach creates a separate, clean working directory (worktree) for each feature, bugfix, or report update. Each worktree is checked out at a specific branch or commit, ensuring that only the intended changes are present. Developers can make, test, and review changes in isolation, then commit and push them without polluting the main branch or affecting ongoing auto-ingest processes.

This workflow is especially useful when multiple branches are active, or when certain files (such as generated wiki pages) should not be tracked in version control. It also enables parallel development: for example, one worktree can be used for audit follow-ups, another for curation report updates, and a third for bugfixes in the curation scripts.

Branch and worktree cleanup is handled explicitly. After merging a feature branch, the corresponding worktree is removed and the branch deleted locally and remotely. If a worktree contains uncommitted or unrelated changes, force removal can be used with explicit user approval, ensuring that only clean, intentional edits are merged.

This approach also supports targeted bugfixing and validation. For instance, a bug in the checkpoint curation script can be fixed and tested in a clean worktree against a live wiki tree, without risk of interfering with the main checkout. Once validated, the fix is merged back to main, and the worktree is cleaned up.

## Key Properties

- **Isolation of Changes:** Each worktree contains only the changes relevant to a specific feature or report, preventing accidental inclusion of unrelated files.
- **Parallel Development:** Multiple worktrees can be active at once, allowing different branches or features to be developed and tested independently.
- **Safe Integration:** Merges and PRs are created from clean worktrees, reducing the risk of merge conflicts or inclusion of generated files.

## Limitations

Requires discipline in worktree and branch management; manual cleanup is sometimes necessary, especially when local branch deletion fails due to active checkouts. Generated files in the main checkout must be carefully excluded from tracked changes. Force removal of worktrees can lead to loss of uncommitted work if not handled carefully.

## Example

A developer needs to update the curation report with new editorial scoring options but finds the main checkout full of generated files. They create a new worktree on branch `feature/report-update`, make the changes, commit and push the branch, and then merge it via PR. Afterward, they remove the worktree and delete the branch, ensuring the main branch remains clean.

## Visual

No explicit diagrams, but the session narrative describes the use of multiple worktrees (e.g., `.worktrees/audit-followups`, `.worktrees/second-curation`, `.worktrees/report-update`) and their lifecycle from creation to cleanup.

## Relationship to Other Concepts

- **[[Phased Implementation Planning and Progress Tracking for LLM Wikis]]** — Worktree-based development supports phased, parallel progress.

## Practical Applications

Essential for teams managing large, auto-ingested wikis or codebases with many generated files. Enables safe, parallel development and robust code review practices in projects like labs-wiki, where content and code are tightly coupled but must be managed separately.

## Sources

- [[Copilot Session Checkpoint: Second Curation Reports]] — primary source for this concept
