---
title: "Agent and Skill Surface Optimization for Multi-Tool AI Project Compatibility"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "8d4ffe804f00fc1786f05b552df93998c7e6bf7f3b353158464961c4edb4f8a3"
sources:
  - raw/2026-04-20-copilot-session-scheduler-dns-agents-cleanup-2222559c.md
quality_score: 100
concepts:
  - agent-skill-surface-optimization-multi-tool-ai-project-compatibility
related:
  - "[[Custom Copilot CLI Agents]]"
  - "[[Custom Agents in VS Code]]"
  - "[[Copilot Session Checkpoint: Scheduler DNS Agents Cleanup]]"
tier: hot
tags: [agent, skill, ai-tools, surface-optimization, compatibility]
---

# Agent and Skill Surface Optimization for Multi-Tool AI Project Compatibility

## Overview

Agent and skill surface optimization is the process of structuring and exposing project-specific skills and agents for seamless integration with AI tools like VS Code, GitHub Copilot, Copilot CLI, and OpenCode. This enables consistent, discoverable workflows and robust compatibility across development environments.

## How It Works

Modern AI projects often require their specialist agents and skills to be accessible from multiple surfaces: IDEs (VS Code), code assistants (GitHub Copilot), CLI tools (Copilot CLI), and prompt-driven platforms (OpenCode). Surface optimization involves:

1. **Canonical Skill Layer Definition:** Establish `.github/skills/` as the canonical directory for project skills, with each skill encapsulated in its own `SKILL.md` wrapper. This provides a discoverable, standardized entry point for AI tools.

2. **Mirrored Skill Layers:** Mirror the canonical skill set to `.opencode/skills/` for OpenCode compatibility, ensuring parity and preventing drift between tool surfaces.

3. **Prompt Compatibility Shims:** Retain legacy prompt files (e.g., `.github/prompts/execute-sprint-from-report.prompt.md`) as compatibility shims that point to the canonical skill definition, avoiding duplication and ensuring backward compatibility.

4. **Specialist Skill Wrappers:** Create skill wrappers for key project workflows (e.g., `sprint-orchestrator`, `nba-ml-pipeline`, `model-calibration`, `feature-lab`, `data-quality`, `backtest-lab`, `dashboard`). These wrappers expose deep specialist docs and workflows to AI tools, enabling targeted orchestration.

5. **IDE Configuration:** Add project-local `.vscode/settings.json` and `.vscode/extensions.json` to configure Python interpreter, enable pytest, and exclude cache directories, supporting robust development and testing.

6. **Code Review and Drift Correction:** Run automated or subagent code reviews to detect and fix issues like corrupted skill files, broken symlinks, and content drift between mirrored skill layers. Synchronize content to maintain consistency.

7. **Documentation and Surface Mapping:** Update routing/index docs (e.g., `AGENTS.md`) to include a 'Project Skill' column and an 'AI Surface Map' section, clarifying the role of each skill and its compatibility across tool surfaces.

This structured approach ensures that project agents and skills are discoverable, consistent, and robustly integrated across all supported AI toolchains, enabling seamless workflow orchestration and reducing friction for developers.

## Key Properties

- **Canonical Skill Directory:** Defines `.github/skills/` as the authoritative skill layer for project workflows.
- **Mirrored Skill Layers:** Ensures `.opencode/skills/` mirrors the canonical skills for OpenCode compatibility.
- **Specialist Skill Wrappers:** Encapsulates specialist workflows in skill wrappers for targeted orchestration.
- **IDE and Tool Surface Mapping:** Documents and configures skill compatibility across VS Code, Copilot, CLI, and OpenCode.

## Limitations

Requires ongoing maintenance to prevent drift between mirrored skill layers. Corrupted skill files or broken symlinks can cause tool failures. Compatibility shims may become outdated if canonical skills evolve. Surface mapping must be kept up-to-date as new tools or workflows are added.

## Example

```markdown
# .github/skills/model-calibration/SKILL.md
## Skill: Model Calibration
- Exposes calibration workflow for NBA ML models
- Compatible with Copilot, CLI, OpenCode
- See AGENTS.md for surface mapping
```

## Relationship to Other Concepts

- **[[Custom Copilot CLI Agents]]** — Surface optimization enables robust Copilot CLI agent integration.
- **[[Custom Agents in VS Code]]** — Skill wrappers support agent discoverability in VS Code.

## Practical Applications

Used in AI projects requiring seamless integration with multiple development tools. Enables robust orchestration of specialist workflows (e.g., sprint execution, calibration, backtesting) from IDEs, code assistants, and prompt-driven platforms. Reduces friction and increases productivity for developers working across toolchains.

## Sources

- [[Copilot Session Checkpoint: Scheduler DNS Agents Cleanup]] — primary source for this concept
