---
title: "Agent Skill Routing Architecture"
type: concept
created: 2026-04-20
last_verified: 2026-04-22
source_hash: "358108ea4d82e3accc5cb671afd3dec27dfb9c5dae571d0970c1b790078c615e"
sources:
  - raw/2026-04-20-copilot-session-integrating-agent-skill-routing-3f817cb6.md
quality_score: 74
concepts:
  - agent-skill-routing-architecture
related:
  - "[[Agent Skill Integration for Time-Series Forecasting]]"
  - "[[Agent and Skill Surface Optimization for Multi-Tool AI Project Compatibility]]"
  - "[[Custom Copilot CLI Agents]]"
  - "[[Copilot Session Checkpoint: Integrating Agent Skill Routing]]"
  - "[[midudev/autoskills]]"
  - "[[Automated AI Skill Stack Installation]]"
tier: hot
tags: [agent-routing, skill-integration, architecture, context-engineering, automation, workspace-management]
---

# Agent Skill Routing Architecture

## Overview

Agent skill routing architecture refers to the systematic design and implementation of mechanisms that ensure agent skills are discoverable, invokable, and contextually routed across multiple agent systems and tool surfaces. This architecture centralizes skill content while maintaining lightweight, project-local triggers, enabling seamless integration and automatic invocation in environments like VS Code, Copilot CLI, and OpenCode.

## How It Works

The agent skill routing architecture is built on the principle of centralizing skill content in a shared workspace layer, while maintaining repo-local routing surfaces that enable automatic skill invocation for agent-system work. The process begins with importing the full skill pack (in this case, 'Agent-Skills-for-Context-Engineering') into a canonical directory, such as `/home/jbl/projects/external-powers/Agent-Skills-for-Context-Engineering`. This ensures that all agent systems reference a single, authoritative source for skills, reducing duplication and simplifying updates.

To trigger skills contextually within individual projects, lightweight routing surfaces are established. These include files like `AGENTS.md`, `.github/copilot-instructions.md`, and selected agent-definition files in each project. The routing surfaces contain explicit references (paths, tables, headings) to the shared skill content, ensuring that agent instructions, Copilot CLI commands, and VS Code settings automatically invoke the relevant skills. This design allows for both centralized management and decentralized activation, as each project can tailor its routing logic without duplicating skill content.

The architecture also leverages automated path generation scripts, such as `update_opencode_skills_paths.py`, which rewrite skill paths for different targets (host, opencode, giniecode, all) and ensure container safety. The script is designed to avoid common pitfalls: it skips collection roots that contain both a root `SKILL.md` and nested `skills/*/SKILL.md`, and excludes ephemeral directories like `.worktrees` from discovery. This prevents accidental inclusion of incomplete or temporary skill paths in tracked configs, maintaining integrity across environments.

Worktree-based development is used to isolate feature branches and edits, enabling safe, parallel development across multiple repositories (homelab, nba-ml-engine, labs-wiki). Each repo has its own `.worktrees/context-engineering-skills` branch, allowing for targeted integration and testing without affecting the main branch until changes are merged. Gitignore conventions are updated to prevent worktree directories from polluting the repo history.

Quality and spec reviews are integral to the architecture. Each task (import, workspace wiring, path generation, local routing) undergoes iterative review loops, with findings (such as incomplete skill coverage or stale paths) sent back for fixes. This ensures routing blocks are synchronized, skill coverage is complete, and all references are accurate. The architecture is robust against baseline quirks (missing .env files, pre-existing test failures) and allows for explicit user acceptance of unresolved issues when outside the integration scope.

## Key Properties

- **Centralized Skill Content:** All skills are imported into a shared workspace directory, referenced by all agent systems, reducing duplication and simplifying updates.
- **Repo-Local Routing Surfaces:** Each project maintains lightweight trigger files (AGENTS.md, copilot instructions) that route agent-system work to the centralized skills.
- **Automated Path Generation:** Scripts like update_opencode_skills_paths.py rewrite skill paths for container safety, skip collection roots, and exclude ephemeral directories.
- **Worktree-Based Development:** Feature branches are isolated in worktrees, allowing parallel, safe edits across multiple repositories.
- **Iterative Quality and Spec Reviews:** Each integration task is reviewed for spec compliance and quality, with findings sent back for fixes until approved.

## Limitations

The shared workspace layer is not a git repo, so edits persist on disk but cannot be committed or versioned unless the root is later converted to a repo. Path generation scripts must be carefully maintained to avoid accidental inclusion of ephemeral or collection-root paths. Baseline quirks (missing .env, pre-existing test failures) can affect testing but are explicitly accepted when outside the integration scope.

## Example

Example routing block in AGENTS.md:

### Context-Engineering Skills
Path: /home/jbl/projects/external-powers/Agent-Skills-for-Context-Engineering/skills/
| Skills to Invoke |
|------------------|
| context-fundamentals |
| context-degradation |
| context-compression |
| context-optimization |
| latent-briefing |
| multi-agent-patterns |
| memory-systems |
| tool-design |
| filesystem-context |
| hosted-agents |
| evaluation |
| advanced-evaluation |
| project-development |
| bdi-mental-states |

This block ensures that agent-system work in the project automatically triggers the relevant skills from the centralized directory.

## Visual

No diagrams or charts are included in the source.

## Relationship to Other Concepts

- **[[Agent Skill Integration for Time-Series Forecasting]]** — Both involve integrating agent skills into project workflows, but this concept generalizes the routing architecture across all agent systems.
- **[[Agent and Skill Surface Optimization for Multi-Tool AI Project Compatibility]]** — Both focus on optimizing skill surfaces for compatibility, but this concept details the routing and trigger mechanisms.
- **[[Custom Copilot CLI Agents]]** — Custom agents rely on routing architecture for skill invocation; this concept explains the underlying routing design.

## Practical Applications

This architecture is used in multi-agent environments where skills need to be discoverable and invokable across VS Code, Copilot CLI, OpenCode, and containerized hosts. It enables centralized skill management, automatic invocation for agent-system work, and robust integration in collaborative projects. It is especially valuable in large-scale AI projects, homelab setups, and environments requiring modular, extensible agent tooling.

## Sources

- [[Copilot Session Checkpoint: Integrating Agent Skill Routing]] — primary source for this concept
