---
title: "Systematic Cleanup of Obsolete Cron Workflows"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "3e65ff8540004a023938bd503813baf3709bfc64d1dbcc49c436263dccdc458c"
sources:
  - raw/2026-04-22-copilot-session-graph-incident-and-cleanup-14e5153b.md
quality_score: 46
concepts:
  - systematic-cleanup-obsolete-cron-workflows
related:
  - "[[Free-Tier-Constrained Backfill Runner Design]]"
  - "[[Copilot Session Checkpoint: Graph Incident and Cleanup]]"
tier: hot
tags: [cleanup, cron, ops, homelab, deployment, documentation]
---

# Systematic Cleanup of Obsolete Cron Workflows

## Overview

Systematic cleanup is a methodical process for identifying, retiring, and removing obsolete cron jobs, scripts, and associated documentation from a codebase and deployment environment. This ensures that legacy workflows do not persist, reducing operational noise and preventing failures due to missing dependencies.

## How It Works

The cleanup process begins with a comprehensive search for all references to the obsolete workflow across code, scripts, environment files, and documentation. In the documented session, the developer searched for terms like `tmp_free_tier_url_backfill`, `labs-wiki-backfill`, and `LABS_WIKI_BACKFILL_PATH` in both `homelab` and `labs-wiki` repositories.

Once all artifacts are identified, the developer creates an isolated worktree (e.g., `/home/jbl/projects/homelab/.worktrees/remove-free-tier-backfill`) to apply targeted diffs. This includes deleting obsolete scripts (such as `homelab/scripts/ops/labs-wiki-backfill.sh`), removing environment variables from `.env.example`, and updating setup scripts to stop provisioning unnecessary directories. Documentation is also updated to remove references to the retired workflow, including inventory entries, service guides, maintenance commands, and log/cron/status sections.

After code and documentation cleanup, live deployment state is validated. Subagents are launched to inspect host cron tables, systemd timers, and script existence. In this session, the subagent found a live user crontab entry and an obsolete host script, both of which were removed. The log showed the job was failing due to a missing runner, confirming the need for cleanup.

Final validation involves running deployment configuration checks (e.g., `docker compose ... config`) to ensure that the removal does not introduce new failures. Any quirks, such as placeholder IPs in `.env.example`, are addressed for validation purposes. The developer reconciles tracked cleanup diffs with the root checkout, ensuring that all changes are merged and temporary worktrees are discarded.

## Key Properties

- **Comprehensive Artifact Search:** All references to the obsolete workflow are identified across code, scripts, environment files, and documentation.
- **Isolated Cleanup Worktree:** Cleanup is performed in a dedicated worktree to avoid contaminating the main codebase and facilitate targeted diffs.
- **Live Deployment Validation:** Host cron tables, scripts, and logs are inspected and cleaned to ensure the workflow is fully retired.
- **Documentation Consistency:** All documentation is updated to remove references to the retired workflow, preventing confusion for future maintainers.
- **Configuration Validation:** Deployment configuration checks are run to ensure that cleanup does not break the build or introduce new errors.

## Limitations

Systematic cleanup relies on thorough artifact search; missed references can lead to lingering operational issues. Live deployment validation may require elevated permissions or access to host cron tables, which can be a blocker in some environments. Documentation updates must be carefully reviewed to avoid accidental removal of relevant information.

## Example

The developer deleted `homelab/scripts/ops/labs-wiki-backfill.sh`, removed `LABS_WIKI_BACKFILL_PATH` from `.env.example`, and updated documentation files. A subagent removed the live user cron entry and obsolete host script from `beelink-gti13`, ensuring that the free-tier backfill workflow was fully retired.

## Visual

No diagrams or charts are included in the source.

## Relationship to Other Concepts

- **[[Free-Tier-Constrained Backfill Runner Design]]** — Both concepts address backfill workflows, but systematic cleanup focuses on retiring obsolete runners.

## Practical Applications

This method is critical for maintaining operational hygiene in homelab environments, containerized deployments, and multi-agent systems. It prevents failures caused by missing scripts, reduces noise from obsolete cron jobs, and ensures that documentation accurately reflects the current state of the system.

## Sources

- [[Copilot Session Checkpoint: Graph Incident and Cleanup]] — primary source for this concept
