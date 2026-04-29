---
name: task-observer
description: >
  Observe every task-oriented session, capture corrections and skill gaps, and
  drive proactive skill maintenance. Use at the start of any multi-step task,
  agentic workflow, or deliverable-producing session. Also trigger on "One Skill
  to Rule Them All" and "task observer". IMPORTANT: invoke this skill before
  other skill or tool work in any task session.
license: CC-BY-4.0
metadata:
  author: Eoghan Henn
  adapted_by: Joshua Lee
  upstream: https://github.com/rebelytics/one-skill-to-rule-them-all
  category: workspace-orchestration
  tags: [meta-skill, observation, skill-maintenance, task-observer]
---

# Task Observer

**Created by [Eoghan Henn](https://rebelytics.com). Adapted for this workspace's VS Code, Copilot CLI, and OpenCode surfaces.**

Task Observer is the cross-cutting meta-skill that watches how other skills
perform, captures reusable improvements, and pushes the skill library to evolve
from real work instead of ad-hoc rewrites.

**Licence:** This adapted skill preserves the upstream
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
licence. Credit the upstream author when reusing or adapting it further.

**Feedback & Support:** Methodology feedback belongs upstream at
<https://github.com/rebelytics/one-skill-to-rule-them-all>. Workspace-specific
integration issues belong in this workspace's instruction or skill files.

## Core Contract

1. Invoke this skill at the **start of every task-oriented session** before any
   other skill or tool work.
2. Keep observation active through planning, implementation, validation, review,
   user feedback, and post-task discussion.
3. Do not replace domain or process skills. Observe them, strengthen them, and
   surface improvements.

## Workspace Integration

- **Canonical skill surface:** `.github/skills/task-observer/`
- **OpenCode mirror:** `.opencode/skills/task-observer/`
- **Activation instructions:** `AGENTS.md` and `.github/copilot-instructions.md`
- **OpenCode refresh command after skill-directory changes:**
  `python3 /home/jbl/projects/update_opencode_skills_paths.py`

For this workspace, reliability comes from a **dual-layer setup**:

1. This skill's own description-level trigger
2. Explicit project instructions that require invoking `task-observer` before
   task work starts

Do not rely on description matching alone.

## Observation Store

Use `[workspace folder]/skill-observations/` for persistent findings:

- `log.md` — active and resolved observations
- `principles.md` — cross-cutting rules that should influence all skills
- `archive/` — optional closed review snapshots

Create the directory and files on first use if they do not exist.

### Minimum Log Entry Shape

Use compact YAML blocks so future sessions can scan them quickly:

```yaml
- id: obs-2026-04-27-001
  status: OPEN
  type: improve-existing-skill
  skill: homelab-deploy
  summary: "Deployment skill missed the Homepage + Uptime Kuma registration rule."
  evidence:
    - "User asked for a new service and follow-up edits were needed in config/homepage and monitoring."
  suggested_update: "Add a mandatory post-deploy registration checklist."
  source: "session"
```

Statuses:

- `OPEN` — observation not yet integrated
- `APPLIED` — guidance already used in live work, file update still optional
- `RESOLVED` — skill/instruction updated and observation no longer pending

## What to Watch For

### Improve an Existing Skill

Log an observation when you see:

- User corrections that reveal a missing or weak rule
- Repeated manual cleanup after a skill was used
- A better workflow emerging during real execution
- A rule that needs stronger enforcement, not just clearer wording
- A useful pattern that should be promoted from incidental to explicit
- A stale or tool-specific instruction that needs updating

### Create a New Skill Candidate

Log a new-skill observation when work reveals:

- A repeatable multi-step workflow with clear inputs and outputs
- A recurring task family no current skill covers
- A project-specific process the user keeps re-explaining

### Simplify an Existing Skill

Log simplification opportunities too:

- Dead sections that never influence work
- One-off rules that added noise but did not recur
- Repeatedly skipped steps
- Overly tool-specific wording that no longer matches the environment

## Immediate-Application Rule

When **any** skill loads:

1. Check `skill-observations/log.md` for `OPEN` entries tagged to that skill.
2. Apply those observations to the current work immediately, even if the skill
   file itself has not been updated yet.
3. Mark the observation `APPLIED` if it materially influenced the session.

Also scan `principles.md` for global rules that should affect the skill being
used now.

## Proactive-Update Rule

When this session produces a **safe, concrete, low-risk** improvement to a
skill or instruction file:

1. Update the affected skill or instruction in the same session.
2. Keep `.github/skills/` as the canonical Copilot/Copilot CLI surface.
3. Keep `.opencode/skills/` in sync for OpenCode.
4. Refresh OpenCode path config with
   `python3 /home/jbl/projects/update_opencode_skills_paths.py`.

If the improvement is real but not safe to apply immediately, leave an `OPEN`
observation with enough detail for the next maintenance pass.

## Skill-Maintenance Heuristics

- Prefer generalized, reusable rules over session-specific anecdotes.
- Prefer simplification when a rule did not earn its keep.
- Never add secrets, credentials, or private customer details to observations.
- Keep project-local details in project skills or local instructions, not in
  generic open-source skills.
- When the same issue affects multiple skills, record it in `principles.md`
  instead of duplicating the note everywhere.

## Session-Close Checklist

Before the session ends:

1. Surface any new `OPEN` observations created during the task.
2. Note which observations were applied live.
3. Update affected skills or instructions when the change is ready now.
4. Leave only real follow-ups open.

## Anti-Patterns

- Treating this skill as optional background noise
- Waiting for a weekly sweep when the current session already proves the fix
- Logging observations without ever applying them
- Growing skills endlessly without pruning stale rules
- Relying on one skill to load this skill instead of direct config instructions
