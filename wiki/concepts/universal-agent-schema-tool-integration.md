---
title: "Universal Agent Schema and Tool Integration"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "26f254b5e6c65170bfc0d1bbf80f2de1aafe3266407d54a0e3243b0e1600d156"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-creating-claude-and-labs-wiki-repos-cccb14d5.md
quality_score: 0
concepts:
  - universal-agent-schema-tool-integration
related:
  - "[[Natural Language-Driven Agent Creation]]"
  - "[[Agent-Ergonomic Tool Design Principles]]"
  - "[[Copilot Session Checkpoint: Creating Claude and Labs-Wiki Repos]]"
tier: hot
tags: [agent-schema, tool-integration, copilot-cli, vscode, opencode]
---

# Universal Agent Schema and Tool Integration

## Overview

A universal agent schema defines a common configuration format (e.g., AGENTS.md) to enable seamless integration of AI agents and skills across multiple tools and platforms such as VS Code, Copilot CLI, and OpenCode. This promotes portability, consistency, and ease of maintenance.

## How It Works

The universal agent schema acts as a single source of truth describing agents, skills, hooks, and their configurations in a standardized format. In the labs-wiki implementation:

- **AGENTS.md** serves as the universal schema file read by all supported tools.
- **Skills** are defined using a YAML frontmatter standard (agentskills.io) for portability.
- **Tool-specific config paths** are mapped to canonical locations:
  - VS Code Copilot uses `.github/copilot-instructions.md`, `.github/skills/*/SKILL.md`, and `.github/hooks/*.json`.
  - Copilot CLI shares the `.github/` structure plus the root `AGENTS.md`.
  - OpenCode uses `AGENTS.md`, `.opencode/skills/*/SKILL.md`, and `opencode.json` for multi-agent model configuration.
- Canonical skill definitions reside in `.github/skills/` and are symlinked into `.opencode/skills/` for consistency.

This design allows developers to maintain one set of skill and agent definitions that work across multiple environments without duplication or divergence. It supports multi-agent workflows, model configuration, and hook-driven automation.

The schema also facilitates incremental updates and validation, enabling smooth integration of new agents or skills and automated tooling support.

## Key Properties

- **Universal Schema File:** AGENTS.md is the single configuration file shared across tools.
- **Skill Definition Standard:** Uses agentskills.io YAML frontmatter for skill portability.
- **Tool-Specific Config Paths:** Maps canonical skill locations to tool-specific directories and files.
- **Multi-Agent Model Config:** Supports multi-agent setups via opencode.json and hooks.

## Limitations

Requires strict adherence to schema standards and careful synchronization of symlinks and config files. Tooling must support the universal schema format for full interoperability. Initial setup complexity may be higher due to multiple config layers.

## Example

A skill called 'code-review' is defined in `.github/skills/code-review/SKILL.md` with YAML frontmatter describing triggers and capabilities. This skill is symlinked into `.opencode/skills/code-review/SKILL.md`. The AGENTS.md file references this skill and defines which agents use it. VS Code Copilot, Copilot CLI, and OpenCode all read AGENTS.md and the skill definitions to activate the skill in their respective environments.

## Relationship to Other Concepts

- **[[Natural Language-Driven Agent Creation]]** — Universal schema enables consistent agent creation workflows across tools.
- **[[Agent-Ergonomic Tool Design Principles]]** — Schema design supports ergonomic integration of agents in developer tools.

## Practical Applications

Facilitates development and deployment of AI agents and skills across multiple platforms without duplication. Enables consistent user experience and easier maintenance in multi-tool environments like VS Code and CLI.

## Sources

- [[Copilot Session Checkpoint: Creating Claude and Labs-Wiki Repos]] — primary source for this concept
