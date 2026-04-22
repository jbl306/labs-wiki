---
title: "Agent Documentation Hygiene And Migration"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "61d2a663201be1287914b264819f16b9d6d4bbee33865442f2be9300278c25db"
sources:
  - raw/2026-04-18-copilot-session-nba-ml-oom-fix-and-docs-cleanup-52d24b9f.md
quality_score: 76
concepts:
  - agent-documentation-hygiene-and-migration
related:
  - "[[Agent-Ergonomic Tool Design Principles]]"
  - "[[Copilot Session Checkpoint: NBA ML OOM Fix And Docs Cleanup]]"
tier: hot
tags: [documentation, agent, migration, repo-hygiene, copilot]
---

# Agent Documentation Hygiene And Migration

## Overview

Agent documentation hygiene and migration refers to the systematic process of updating, consolidating, and removing deprecated agent-related files and references in code repositories. This ensures that only active, validated agent specifications are documented and used, reducing confusion and technical debt.

## How It Works

Documentation hygiene begins with identifying outdated or unused agent files and references. In this session, two repositories were involved: homelab and labs-wiki. The homelab repo's AGENTS.md was updated to add MemPalace instructions and remove references to deprecated OpenMemory stacks. In the labs-wiki repo, a root `agents/` directory contained five old persona-style Markdown files, while `.github/agents/` held seven Copilot-format agent specs with YAML frontmatter.

The process involved:
- Removing the root `agents/` directory and its files, which were no longer loaded by any code and only referenced in documentation.
- Updating AGENTS.md to reference the active `.github/agents/` directory and its validated Copilot-format agent specs.
- Revising `.github/copilot-instructions.md` to update the directory map and remove scoped instructions for the old `agents/**/*.md` files.
- Updating README.md to remove references to the deprecated `agents/` directory from the architecture tree.

These changes were staged but not yet committed or pushed, highlighting the importance of finalizing documentation updates. The hygiene process also included removing OpenMemory references from service tables, architecture diagrams, and DNS rewrite configs in the homelab repo, reflecting a migration from OpenMemory (Docker-based) to MemPalace (local MCP, no containers).

Migration documentation was preserved in `docs/12-mempalace-setup.md`, ensuring historical context for the transition. The process emphasizes the need for clear, up-to-date documentation that accurately reflects the current system architecture and agent workflow, reducing confusion for users and maintainers.

## Key Properties

- **Documentation Consistency:** Ensures all references, tables, and architecture diagrams reflect the current set of active agents and memory stacks.
- **Migration Tracking:** Preserves historical migration documentation to maintain context for architectural changes.
- **Technical Debt Reduction:** Removes stale files and references, preventing confusion and reducing maintenance overhead.

## Limitations

Requires careful coordination to avoid accidental deletion of active files. Staged changes must be committed and pushed to take effect. Migration documentation must be preserved to avoid loss of historical context.

## Example

```bash
git rm -r agents/
# Removes 5 persona-style MD files from labs-wiki
```
AGENTS.md updated:
- Old persona table replaced with `.github/agents/` agent table (7 agents)
README.md updated:
- Removed `agents/` from architecture tree
.github/copilot-instructions.md updated:
- Directory map points to `.github/agents/`

## Visual

Null (no diagrams or charts in the source).

## Relationship to Other Concepts

- **[[Agent-Ergonomic Tool Design Principles]]** — Both focus on clarity and usability for agent workflows.

## Practical Applications

Applied in code repositories to maintain accurate agent documentation, ensure only validated agent specs are used, and facilitate migration between memory architectures (e.g., OpenMemory to MemPalace). Essential for collaborative ML and agentic projects.

## Sources

- [[Copilot Session Checkpoint: NBA ML OOM Fix And Docs Cleanup]] — primary source for this concept
