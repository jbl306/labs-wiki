---
title: "Copilot Session Checkpoint: Task-Observer Repo Rollout"
type: source
created: '2026-04-27'
last_verified: '2026-04-27'
source_hash: "255939f5ac74cb5fa7ae0a104d5fcf5288dca4618889290a4930b3448a966440"
sources:
  - raw/2026-04-27-copilot-session-task-observer-repo-rollout-6fb8d221.md
concepts:
  - dual-layer-skill-activation
related:
  - "[[Task Observer]]"
  - "[[Dual-Layer Skill Activation]]"
  - "[[Agent Skill Routing Architecture]]"
  - "[[Automated Skill Path Generation for Containerized Agent Systems]]"
  - "[[Copilot CLI]]"
  - "[[OpenCode]]"
  - "[[MemPalace]]"
  - "[[update_opencode_skills_paths.py]]"
checkpoint_class: durable-architecture
retention_mode: retain
tags: [copilot-session, checkpoint, task-observer, meta-skill, skill-integration, opencode, copilot-cli, labs-wiki]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 69
---

# Copilot Session Checkpoint: Task-Observer Repo Rollout

## Summary

This checkpoint captures the rollout of a canonical `task-observer` meta-skill across the shared workspace and five project repositories, with consistent wiring for VS Code, [[Copilot CLI]], and [[OpenCode]]. The durable knowledge is not just that the skill was installed, but that reliable activation required both discoverable skill files and explicit instruction-layer rules, plus a later portability fix that replaced out-of-repo symlinks with committed in-repo copies.

## Key Points

- **Upstream pattern adoption:** The rollout started by studying `rebelytics/one-skill-to-rule-them-all` and extracting the key rule that skill installation alone is insufficient; each tool surface also needs explicit instructions that force invocation.
- **Canonical workspace skill:** A shared `task-observer` skill was created at `/home/jbl/projects/.github/skills/task-observer/` as the authoritative local adaptation for the workspace.
- **Project-local deployment:** Matching `.github/skills/task-observer/` surfaces were added inside `debrid-downloader-web`, `galloping-bot`, `homelab`, `labs-wiki`, and `nba-ml-engine` so the pattern would survive cloning and GitHub pushes.
- **Instruction-layer enforcement:** Root and repo-local `AGENTS.md` plus `.github/copilot-instructions.md` files were updated to invoke `task-observer` at session start and to apply `OPEN` entries from `skill-observations/log.md` whenever relevant skills load.
- **OpenCode integration model:** `debrid-downloader-web`, `galloping-bot`, `homelab`, and `labs-wiki` used `.opencode/skills -> ../.github/skills`, while `nba-ml-engine` used an explicit mirrored `.opencode/skills/task-observer/` directory.
- **Config refresh:** `python3 /home/jbl/projects/update_opencode_skills_paths.py` regenerated host and homelab OpenCode skill-path config so the new skill became discoverable in both environments.
- **Portability correction:** Initial project-local symlinks pointed outside repo roots to `/home/jbl/projects/.github/skills/task-observer/...`; these were replaced with real copied files before commit so downstream clones would not break.
- **Verification and repair:** Existing repo validation was rerun after the rollout; environment-only pytest gaps were handled with temporary virtualenvs, and a stale-date test in `nba-ml-engine` was fixed by switching to `date.today() - timedelta(days=1)`.
- **Deployment result:** Changes were committed and pushed directly to `main` for all five repos, with confirmed commits for `debrid-downloader-web` (`7c5a530`), `galloping-bot` (`929641e`), `homelab` (`7a7f1fd`), `labs-wiki` (`c189caa`), and `nba-ml-engine` (`05bf273`).

## Key Concepts

- [[Dual-Layer Skill Activation]]
- [[Agent Skill Routing Architecture]]
- [[Automated Skill Path Generation for Containerized Agent Systems]]
- [[Universal Agent Schema (AGENTS.md) for AI Tool Integration]]

## Related Entities

- **[[Task Observer]]** — Workspace meta-skill adapted from the upstream meta-skill pattern and rolled out across five repositories.
- **[[Copilot CLI]]** — One of the primary agent surfaces that now explicitly routes task-oriented sessions through the new meta-skill.
- **[[OpenCode]]** — Needed both repo-local skill visibility and refreshed config paths for the rollout to work consistently.
- **[[MemPalace]]** — Used during the session for prior-context lookup and result recording around the rollout work.
- **[[update_opencode_skills_paths.py]]** — The path-generation script used to refresh OpenCode skill discovery after adding the new surfaces.
