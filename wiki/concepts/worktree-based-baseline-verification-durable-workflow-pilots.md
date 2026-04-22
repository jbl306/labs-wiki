---
title: "Worktree-Based Baseline Verification for Durable Workflow Pilots"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "58f7e891b3f357ec9e293d8dfe365b373ec7a7fbe3eba4e22a93947cc4d024c4"
sources:
  - raw/2026-04-20-copilot-session-pilot-worktree-baseline-10f2a2a8.md
quality_score: 59
concepts:
  - worktree-based-baseline-verification-durable-workflow-pilots
related:
  - "[[Worktree-Based Subagent-Driven Development]]"
  - "[[Durable Copilot Session Checkpoint Promotion]]"
  - "[[Copilot Session Checkpoint: Pilot Worktree Baseline]]"
tier: hot
tags: [worktree, baseline-verification, durable-workflow, pilot, artifact-control, repo-rules]
---

# Worktree-Based Baseline Verification for Durable Workflow Pilots

## Overview

Worktree-based baseline verification is a process used to ensure a clean, isolated environment for implementing and validating workflow pilots, such as the URL raw preservation pilot in labs-wiki. This approach leverages git worktrees and branches to avoid accidental commits of unrelated changes, enabling precise control over pilot execution and artifact management. It is especially critical when repo rules enforce strict immutability or deterministic artifact generation.

## How It Works

The worktree-based baseline verification process begins by creating a dedicated git worktree and feature branch, ensuring that the pilot implementation is isolated from the main development branch and any unrelated changes. This isolation is crucial for workflows where deterministic artifact generation and strict adherence to repo rules are required, such as the labs-wiki URL raw preservation pilot.

The steps include:
1. **Worktree Creation:** A new worktree is created (e.g., `/home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot`) based on the latest main branch commit. This ensures the pilot starts from a known, clean state.
2. **Baseline Verification:** Before any code changes, the environment is validated:
   - `.worktrees` directory is confirmed as git-ignored to prevent accidental commits.
   - Key scripts (`scripts/auto_ingest.py`) are compiled and run for help output to verify baseline functionality.
   - Pilot target raw files are inspected to ensure they are untouched stubs (containing only frontmatter and URL body, no fetched-content blocks).
3. **Artifact Management:** Only relevant planning and spec artifacts are committed to main, avoiding unrelated dirty/generated wiki content. This prevents accidental inclusion of drift or non-pilot changes.
4. **SQL Todo Tracking:** Implementation progress is tracked via SQL todos, marking steps such as worktree creation, implementation start, and blocking conditions (e.g., no revised raw articles yet).

This process is tightly coupled with repo rules and operational constraints. For example, `AGENTS.md` and `.github/instructions/raw-sources.instructions.md` currently forbid modifying raw files except for status. Any implementation that persists fetched-content blocks must update these rules and documentation in tandem with code changes.

Baseline verification also includes reviewing the implementation plan against the approved spec and current codebase, using plan-review subagents to identify issues such as undefined imports, broken snippets, and artifact mismatches. The plan file is treated as guidance, not executable truth, and implementation decisions are made based on observed code behavior and spec requirements.

The worktree-based approach enables quota-safe pilot execution, ensuring that only the intended three raw files are processed and that manual notes and artifact structure are preserved. It also facilitates validation gates, such as Docker build checks and deterministic artifact generation, before proceeding to core implementation.

Edge cases addressed include:
- Avoiding accidental commits of unrelated changes.
- Ensuring manual notes outside fetched-content blocks are preserved.
- Handling repo rule conflicts and updating documentation as needed.
- Verifying that baseline scripts and dependencies are functional before code edits.

Trade-offs include the overhead of maintaining isolated worktrees and branches, but this is justified by the need for deterministic, reproducible pilot workflows and strict artifact control.

## Key Properties

- **Isolation:** Ensures pilot implementation is separated from unrelated changes via dedicated worktree and branch.
- **Baseline Verification:** Validates that scripts, dependencies, and pilot target files are in their intended pre-implementation state.
- **Artifact Control:** Prevents accidental commits of dirty/generated wiki content; only relevant planning/spec artifacts are pushed.
- **Quota-Safe Execution:** Limits pilot to three specific raw files, avoiding broad backfill or destructive refresh logic.

## Limitations

Requires manual setup and maintenance of worktrees and branches. Repo rule conflicts must be resolved before implementation. Overhead may be significant for small pilots but is necessary for deterministic artifact workflows. Baseline verification does not guarantee correctness of future code changes; it only ensures starting state.

## Example

```bash
# Create worktree for pilot
cd /home/jbl/projects/labs-wiki
git worktree add .worktrees/url-raw-preservation-pilot feature/url-raw-preservation-pilot

# Verify baseline
cd .worktrees/url-raw-preservation-pilot
python3 -m py_compile scripts/auto_ingest.py
python3 scripts/auto_ingest.py --help
# Inspect pilot raw files for baseline stub state
cat raw/2026-04-20-agents-that-remember-introducing-agent-memory.md
```

## Relationship to Other Concepts

- **[[Worktree-Based Subagent-Driven Development]]** — Worktree-based baseline verification is a prerequisite for subagent-driven development, enabling isolated execution and validation.
- **[[Durable Copilot Session Checkpoint Promotion]]** — Baseline verification is part of the durable checkpoint promotion process, ensuring only validated artifacts are promoted.

## Practical Applications

Used for pilot workflows where deterministic artifact generation and strict repo rule adherence are required, such as URL raw preservation pilots, durable session checkpoint promotion, and quota-safe targeted backfill in knowledge wikis.

## Sources

- [[Copilot Session Checkpoint: Pilot Worktree Baseline]] — primary source for this concept
