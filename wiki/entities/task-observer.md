---
title: "Task Observer"
type: entity
created: 2026-04-27
last_verified: 2026-04-27
source_hash: "255939f5ac74cb5fa7ae0a104d5fcf5288dca4618889290a4930b3448a966440"
sources:
  - raw/2026-04-27-copilot-session-task-observer-repo-rollout-6fb8d221.md
concepts: [dual-layer-skill-activation]
related:
  - "[[Copilot CLI]]"
  - "[[OpenCode]]"
  - "[[Labs-Wiki]]"
  - "[[Homelab]]"
  - "[[update_opencode_skills_paths.py]]"
tier: hot
tags: [task-observer, meta-skill, agent-skills, copilot-cli, opencode, vscode, workspace-management]
---

# Task Observer

## Overview

Task Observer is a workspace-specific meta-skill created to make task-oriented AI sessions behave consistently across multiple tool surfaces instead of relying on whichever skill a model happens to infer from description matching. In this rollout, it was installed as a canonical workspace skill and then propagated into five repositories so VS Code, [[Copilot CLI]], and [[OpenCode]] could all discover and invoke the same operational pattern.

The skill matters because it converts a loosely documented habit into explicit infrastructure. Rather than treating skill use as optional, the rollout encoded a deterministic rule: invoke `task-observer` at session start, consult `skill-observations/log.md` for `OPEN` observations when skills load, and proactively update instructions or skills when safe. That turns the meta-skill into a coordination layer for workflow hygiene, not just another prompt wrapper.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | 2026-04-27 |
| Creator | Adapted locally from rebelytics' "One Skill to Rule Them All" pattern |
| URL | N/A |
| Status | Active |

## Design

The rollout used a two-tier layout. The authoritative copy lives at `/home/jbl/projects/.github/skills/task-observer/`, where the workspace keeps the canonical `SKILL.md` and `LICENSE.txt`. Each project then received its own self-contained `.github/skills/task-observer/` directory so the skill could travel with the repository instead of depending on the untracked workspace root.

The second half of the design lives in instruction surfaces rather than skill files. Root and repo-local `AGENTS.md`, `.github/copilot-instructions.md`, and `.vscode/settings.json` files were updated so the skill is not merely present on disk but is explicitly routed into task-oriented sessions. This is the critical distinction between a discoverable skill and an actually enforced workflow.

## Rollout Model

The deployment covered `debrid-downloader-web`, `galloping-bot`, `homelab`, `labs-wiki`, and `nba-ml-engine`. Four repos exposed the skill to OpenCode by using `.opencode/skills -> ../.github/skills`, while `nba-ml-engine` used explicit mirrored files under `.opencode/skills/task-observer/`.

After adding those surfaces, the rollout refreshed OpenCode skill discovery with [[update_opencode_skills_paths.py]], updating both `~/.config/opencode/config.json` and `homelab/config/opencode/opencode.json`. This made the same meta-skill visible across host and containerized OpenCode environments.

## Operational Impact

The most important correction in the session was a portability fix. The first implementation used symlinks that pointed outside each repo to `/home/jbl/projects/.github/skills/task-observer/...`, which would have failed for anyone cloning the repositories elsewhere. Replacing those symlinks with committed in-repo copies turned the rollout from a local convenience into a portable repository feature.

The rollout also survived real verification pressure. Existing repo checks were rerun, temporary pytest environments were created where local Python environments were missing, and an unrelated stale-date failure in `nba-ml-engine` was repaired before the final pushes. By the end of the session, all five repos had their task-observer changes committed and pushed to `main`.

## Related Work

- **[[OpenCode]]** — One of the tool surfaces that needed explicit skill discovery and path refresh.
- **[[Copilot CLI]]** — Another target surface for enforced session-start invocation.
- **[[Labs-Wiki]]** — One of the repositories updated with repo-local task-observer wiring.
- **[[Homelab]]** — Hosted the container-side OpenCode config refreshed during the rollout.
