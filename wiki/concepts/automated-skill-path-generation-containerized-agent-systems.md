---
title: "Automated Skill Path Generation for Containerized Agent Systems"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "358108ea4d82e3accc5cb671afd3dec27dfb9c5dae571d0970c1b790078c615e"
sources:
  - raw/2026-04-20-copilot-session-integrating-agent-skill-routing-3f817cb6.md
quality_score: 59
concepts:
  - automated-skill-path-generation-containerized-agent-systems
related:
  - "[[Automated AI Skill Stack Installation]]"
  - "[[Universal Agent Schema and Tool Integration]]"
  - "[[Copilot Session Checkpoint: Integrating Agent Skill Routing]]"
tier: hot
tags: [skill-path, automation, container, agent-system, integration, config]
---

# Automated Skill Path Generation for Containerized Agent Systems

## Overview

Automated skill path generation is a mechanism for dynamically discovering, rewriting, and syncing skill paths across host and container environments in agent-system projects. It ensures accurate skill discovery, prevents path leaks, and supports robust integration in containerized setups like OpenCode and Giniecode.

## How It Works

Skill path generation begins with a script (e.g., update_opencode_skills_paths.py) that scans the shared workspace directory for skill files (SKILL.md) and generates path lists for different targets: host, opencode, giniecode, or all. The script uses a ConfigTarget abstraction to rewrite paths appropriately, ensuring that container configs reference the correct absolute paths (e.g., /home/opencode/projects/external-powers/Agent-Skills-for-Context-Engineering/skills/).

The script is designed to handle collection roots that contain both a root SKILL.md and nested skills/*/SKILL.md. It skips the collection root and exposes only the nested skills, preventing accidental inclusion of incomplete or aggregate skill paths. It also excludes ephemeral directories like .worktrees and worktrees from discovery, avoiding leaks of temporary paths into tracked configs.

Path rewriting is robust against container quirks. The script supports --homelab-root and HOMELAB_ROOT overrides, allowing safe execution in worktree environments. It regenerates configs (opencode.json, giniecode.json) with accurate container prefixes, ensuring that agent systems in different environments discover the correct skill paths. Workspace files (projects.code-workspace) are updated to reference absolute paths, and plugin locations are fixed to avoid stale or incorrect references.

The process is iterative, with review loops to catch issues like collection-root leaks, .worktrees leaks, stale plugin paths, and incomplete skill coverage. Configs are regenerated after each fix, and final reviews ensure that all paths are correct, no leaks remain, and documentation is accurate. The mechanism supports large-scale skill packs (e.g., 226 paths in each tracked config) and is resilient to baseline quirks (workspace file resolution, container path mapping).

Documentation is updated to reflect sync commands, generator script usage, and container path conventions. The mechanism is essential for robust skill integration in containerized agent-system projects, enabling seamless discovery and invocation across host and container environments.

## Key Properties

- **Dynamic Skill Discovery:** The script scans workspace directories for SKILL.md files and generates path lists for different targets.
- **Robust Path Rewriting:** Paths are rewritten for container safety, skipping collection roots and excluding ephemeral directories.
- **Config Regeneration:** Container configs (opencode.json, giniecode.json) are regenerated with accurate prefixes and no leaks.
- **Iterative Review and Fixes:** Review loops catch and fix issues like path leaks, stale references, and incomplete coverage.
- **Documentation Sync:** Workspace files and docs are updated to reflect accurate skill locations and generator usage.

## Limitations

The script must be carefully maintained to avoid accidental inclusion of ephemeral or collection-root paths. Workspace file resolution can be quirky when opened from worktree paths. Large skill packs require robust review to ensure coverage and prevent leaks.

## Example

Example generator usage:

python3 update_opencode_skills_paths.py --target opencode --homelab-root /home/jbl/projects/homelab

This command scans the workspace, rewrites paths for the opencode container, and regenerates config/opencode/opencode.json with correct skill paths.

## Visual

No diagrams or charts are included in the source.

## Relationship to Other Concepts

- **[[Automated AI Skill Stack Installation]]** — Both automate skill discovery and integration, but this concept focuses on path generation for containerized environments.
- **[[Universal Agent Schema and Tool Integration]]** — Both support robust integration across agent systems, but this concept details path generation and container config management.

## Practical Applications

This mechanism is used in containerized agent-system projects (OpenCode, Giniecode) to ensure accurate skill discovery and invocation. It supports large-scale skill packs, robust integration, and seamless operation across host and container environments.

## Sources

- [[Copilot Session Checkpoint: Integrating Agent Skill Routing]] — primary source for this concept
