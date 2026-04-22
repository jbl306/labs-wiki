---
title: "Recurring checkpoint patterns: Agent Skill Routing Architecture, Worktree-Based Subagent-Driven Development, Automated Skill Path Generation for Containerized Agent Systems"
type: synthesis
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "synthesis-generated"
sources:
  - raw/2026-04-20-copilot-session-integrating-agent-skill-routing-3f817cb6.md
  - raw/2026-04-20-copilot-session-pilot-worktree-baseline-10f2a2a8.md
  - raw/2026-04-20-copilot-session-url-followup-pass-b53bba3e.md
concepts:
  - worktree-based-baseline-verification-for-durable-workflow-pilots
  - worktree-based-subagent-driven-development
  - agent-skill-routing-architecture
  - automated-skill-path-generation-for-containerized-agent-systems
related:
  - "[[Copilot Session Checkpoint: Pilot Worktree Baseline]]"
  - "[[Automated Skill Path Generation for Containerized Agent Systems]]"
  - "[[Worktree-Based Subagent-Driven Development]]"
  - "[[Worktree-Based Baseline Verification for Durable Workflow Pilots]]"
  - "[[Agent Skill Routing Architecture]]"
  - "[[Copilot Session Checkpoint: URL Followup Pass]]"
  - "[[Copilot Session Checkpoint: Integrating Agent Skill Routing]]"
tier: hot
checkpoint_cluster_community: 14
checkpoint_cluster_checkpoint_count: 3
checkpoint_cluster_signature: bae1fea89061419a
tags: [agents, checkpoint, checkpoint-synthesis, copilot-session, durable-knowledge, fileback, graph, labs-wiki, mempalace]
quality_score: 75
---

# Recurring checkpoint patterns: Agent Skill Routing Architecture, Worktree-Based Subagent-Driven Development, Automated Skill Path Generation for Containerized Agent Systems

## Question

What recurring decisions, fixes, and durable patterns appear across the 3 session checkpoints in this cluster, especially around Agent Skill Routing Architecture, Worktree-Based Subagent-Driven Development, Automated Skill Path Generation for Containerized Agent Systems?

## Summary

Across 3 agent-system integration checkpoints the recurring decisions converge on a **share-once-route-locally** architecture: skill content lives in a single workspace directory, repo-local routing surfaces (AGENTS.md, copilot-instructions.md) point at it, an automated path generator rewrites paths for host vs container, and all of it happens inside isolated git worktrees so the integration can be reviewed and rolled back without touching main. The shared discipline is treating *baseline verification* as a precondition—not a side effect—of every integration step.

## Comparison

| Dimension | [[Agent Skill Routing Architecture]] | [[Worktree-Based Subagent-Driven Development]] | [[Automated Skill Path Generation for Containerized Agent Systems]] | [[Worktree-Based Baseline Verification for Durable Workflow Pilots]] |
|-----------|---------------------||---------------------||---------------------||---------------------|
| Architectural slot | Layer 0: where skills live (canonical /home/jbl/projects/external-powers/.../skills/) and how repos point at them. | Layer 1: the workflow used to ship a routing change without contaminating main. | Layer 2: the script (update_opencode_skills_paths.py) that rewrites paths per ConfigTarget (host/opencode/giniecode/all). | Layer 3: pre-implementation validation (gitignore, scripts compile, raw stubs untouched, repo rules consistent) inside the worktree. |
| Failure surface guarded against | Skill duplication across repos that drifts out of sync. | Half-finished integrations contaminating main and blocking other work. | Collection-root and `.worktrees` paths leaking into tracked configs; container vs host path mismatches. | Pilots that ship but rely on baseline behavior nobody validated. |
| Concrete artifact produced | Routing block in AGENTS.md listing 14 context-engineering skills + path. | Per-repo `.worktrees/context-engineering-skills` on branch `feat/context-engineering-skills`; .gitignore updated; SQL todo trail. | Regenerated opencode.json, giniecode.json, projects.code-workspace with 226 skill paths each, container-prefix-corrected. | Compile + help-output check on auto_ingest.py; confirmation that pilot raw files are untouched stubs; explicit acceptance log of any deferred baseline issues. |
| Review loop | Quality and spec reviews per task; findings sent back for fix until approved. | Each subagent task closed by a spec/quality review before next task starts. | Iterative review for collection-root leaks, .worktrees leaks, stale plugin paths, coverage gaps. | Plan-review subagent compares plan vs spec vs current code; finds undefined imports / artifact mismatches before implementation. |

## Analysis

These three checkpoints describe a single end-to-end pattern for shipping cross-repo agent-system changes safely: **share content centrally, route locally, generate paths automatically, verify baseline first, and do all of it in a worktree**.

The routing architecture is deliberately layered. Skill content sits exactly once in `external-powers/Agent-Skills-for-Context-Engineering/skills/`; every consuming repo gets a *trigger surface* (AGENTS.md table, copilot-instructions.md heading) that points at it. This means an upgrade to a skill happens in one place, but each repo gets to decide which skills it routes to. The architectural separation between content and routing is what makes the pattern tractable across labs-wiki, homelab, and nba-ml-engine simultaneously.

The path-generation script is what makes this work in containers. OpenCode and Giniecode mount the workspace at different absolute paths (`/home/opencode/...`, etc.); the script's `ConfigTarget` abstraction lets one source tree generate the right paths for each target. The recurring leaks the script has to defend against—collection roots that contain both a `SKILL.md` and `skills/*/SKILL.md`, `.worktrees` directories, stale plugin paths—are all consequences of the share-once-route-locally architecture: any tracked config that captures the wrong absolute path will mis-route the agent.

Worktree-based development is the workflow that contains the blast radius. Each repo gets `.worktrees/context-engineering-skills` on a `feat/` branch; gitignore is updated so worktree directories never enter history; subagents work in those worktrees without touching main. When something goes sideways (the Layer 3 baseline verification entry exists precisely because something *did* go sideways with the url-raw-preservation pilot), the worktree confines the damage and the SQL todo trail preserves the rollback context.

Baseline verification is the meta-discipline. Before any code is edited, the pilot validates: gitignore covers `.worktrees`, key scripts compile and run `--help`, raw stubs are untouched, `AGENTS.md`/`raw-sources.instructions.md` rules are consistent with the planned change. Plan-review subagents compare the plan doc against the actual code (because plan docs drift). The principle is that the pilot can't be trusted unless the baseline is proven.

## Key Insights

1. **Share-once-route-locally is the architectural primitive that lets one skill upgrade propagate to all consuming repos without copy-paste drift, because the trigger surface (AGENTS.md table) and the content (SKILL.md) are deliberately decoupled.** — supported by [[Agent Skill Routing Architecture]], [[Automated Skill Path Generation for Containerized Agent Systems]]
2. **The path-generation script's defenses against collection-root and `.worktrees` leaks aren't lint—they're load-bearing. A leaked path silently mis-routes every agent that reads the config until someone notices, which can be days.** — supported by [[Automated Skill Path Generation for Containerized Agent Systems]]
3. **Worktrees + plan-review subagents create a cheap rollback boundary: the plan can drift from code, but the worktree confines drift consequences and the review loop catches it before it merges.** — supported by [[Worktree-Based Subagent-Driven Development]], [[Worktree-Based Baseline Verification for Durable Workflow Pilots]]
4. **Baseline verification as a *first* step (not a smoke test at the end) is what made these integrations reproducible—every later step assumes the baseline already passes, which means failures land in the new code, not in unvalidated existing state.** — supported by [[Worktree-Based Baseline Verification for Durable Workflow Pilots]]

## Open Questions

- Should the central skill workspace be promoted to a git repo so changes are versioned and reverteable, given that share-once means a bad commit reaches every consumer simultaneously?
- What's the right detection for stale plugin paths across all tracked configs—a CI lint, a periodic regen-and-diff, or making the generator a pre-commit hook?
- When a worktree pilot is rolled back, what guarantees that the SQL todo trail and acceptance log are preserved (rather than discarded with the worktree)?

## Sources

- [[Copilot Session Checkpoint: Integrating Agent Skill Routing]]
- [[Copilot Session Checkpoint: Pilot Worktree Baseline]]
- [[Copilot Session Checkpoint: URL Followup Pass]]
