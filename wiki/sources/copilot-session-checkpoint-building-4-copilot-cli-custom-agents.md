---
title: "Copilot Session Checkpoint: Building 4 Copilot CLI Custom Agents"
type: source
created: 2026-04-12
last_verified: 2026-04-21
source_hash: "3a38e39284cc0602ec33af8d22ef0dfb3c2a3a21b23b03f06716e3221ca8b49e"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-building-4-copilot-cli-custom-agents-4d3f83bc.md
quality_score: 100
concepts:
  - custom-copilot-cli-agents
  - autoagent-framework-research-integration-planning
  - agent-feedback-loop-mechanism
related:
  - "[[Custom Copilot CLI Agents]]"
  - "[[AutoAgent Framework Research and Integration Planning]]"
  - "[[Agent Feedback Loop Mechanism]]"
  - "[[AutoAgent]]"
  - "[[Copilot CLI]]"
  - "[[MemPalace]]"
  - "[[Homelab]]"
  - "[[NBA-ML Engine]]"
tier: hot
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki, nba-ml-engine, mempalace, agents, dashboard, multi-repo, automation, custom-agents, autoagent, agent-feedback, copilot-cli]
checkpoint_class: durable-architecture
retention_mode: retain
knowledge_state: validated
---

# Copilot Session Checkpoint: Building 4 Copilot CLI Custom Agents

## Summary

The user is executing a multi-repo project spanning labs-wiki, homelab, and nba-ml-engine repositories. This session focused on two major tasks: (1) deep researching AutoAgent (HKUDS) framework and creating an integration plan for the homelab, and (2) building 4 custom Copilot CLI agents tailored to the user's projects with integrated feedback loops. The session builds on extensive prior work including MemPalace installation, OpenMemory migration, wiki auto-ingest pipeline, and knowledge curation infrastructure.

## Key Points

- AutoAgent deep research (3 explore agents + web fetching)
- AutoAgent integration plan written and pushed
- Custom agent creation guide added to plan
- Homelab Ops Agent built
- DevOps Deploy Agent built
- NBA-ML Pipeline Agent built

## Execution Snapshot

**Files created this session:**
- `labs-wiki/plans/autoagent-integration.md` — AutoAgent research + integration plan (committed: a719db9, updated: 35a7ae5)
- `homelab/agents/homelab-ops.md` — Homelab infrastructure ops agent (NOT COMMITTED)
- `homelab/agents/devops-deploy.md` — DevOps deployment agent (NOT COMMITTED)
- `nba-ml-engine/agents/nba-ml-pipeline.md` — NBA-ML pipeline agent (NOT COMMITTED)
- `labs-wiki/agents/knowledge-curator.md` — Knowledge curator agent (NOT COMMITTED)
- `labs-wiki/tasks/lessons.md` — Feedback loop lesson template (NOT COMMITTED)
- `labs-wiki/plans/agent-build-report.md` — Build status report (NOT COMMITTED)

**Files modified this session:**
- `homelab/AGENTS.md` — Added Custom Agent Personas section with table and feedback loop format (NOT COMMITTED)
- `nba-ml-engine/.github/copilot-instructions.md` — Added Custom Agents section with agent table (NOT COMMITTED)
- `labs-wiki/AGENTS.md` — Added knowledge-curator to agent personas table (NOT COMMITTED)

**Work completed:**
- [x] AutoAgent deep research (3 explore agents + web fetching)
- [x] AutoAgent integration plan written and pushed
- [x] Custom agent creation guide added to plan
- [x] Homelab Ops Agent built
- [x] DevOps Deploy Agent built
- [x] NBA-ML Pipeline Agent built
- [x] Knowledge Curator Agent built
- [x] Feedback loop mechanism (lessons.md templates, agent rules)
- [x] Integration points updated (AGENTS.md in all repos)
- [x] Validation (44 file refs, 29 commands — 4/4 PASS)
- [x] Status report created
- [ ] **Commits and pushes for agent build work (3 repos) NOT DONE YET**

SQL todo status: 6/7 done, 1 in_progress (status-report — report created but not committed)

## Technical Details

- **Architecture**: MetaChain engine + LiteLLM (v1.55.0) + Docker sandbox + BrowserEnv (Playwright)
- **No MCP support**: Zero references to Model Context Protocol anywhere in codebase
- **No GitHub Models API support**: GITHUB_AI_TOKEN is for git operations only, not model inference
- **Pre-built Docker images**: `tjbtech1/metachain:amd64_latest` / `arm64` — no Dockerfile in repo
- **~60 Python dependencies**: Including playwright, docling, faster-whisper, sentence-transformers, chromadb
- **CLI commands**: `auto main` (full), `auto deep-research` (lightweight), `auto agent`, `auto workflow`
- **REST API**: FastAPI at `/agents/{name}/run`, `/tools/{name}`, `/agents`
- **Decision**: Score 2.5/5, recommend Option B+C hybrid (deep research sidecar + cherry-pick patterns) ### Agent Architecture Patterns
- **labs-wiki**: Rich agent persona system — 4 personas (researcher, compiler, curator, auditor) + 7 skills in `.github/agents/`
- **homelab**: AGENTS.md with validation commands, deploy workflow, superpowers integration
- **nba-ml-engine**: Sprint-driven with `.opencode/skills/execute-sprint-from-report/` (11-step orchestration)
- All repos use `tasks/lessons.md` for feedback loop entries ### Homelab Server Reference
- Host: beelink-gti13 / 192.168.1.238, Ubuntu 24.04 LTS
- 13 Docker Compose stacks in `compose/compose.<stack>.yml`
- Main orchestrator: `compose/docker-compose.yml`
- Deploy: `scripts/ops/deploy.sh [stack]`
- Monitoring: Prometheus + Grafana + cAdvisor + node-exporter
- MemPalace: native pipx install, ~11,157 drawers, weekly cron re-mine ### NBA-ML Engine Reference
- 9-cat fantasy stats prediction (pts, reb, ast, stl, blk, tov, fg_pct, ft_pct, fg3m)
- TimescaleDB on port 5433, MLflow on port 5000
- Click CLI with 10+ commands (init, ingest, train, predict, backtest, evaluate, serve, etc.)
- Notifications via Apprise (ntfy, email, Telegram, Slack)
- Known issue: UniqueViolation on `uq_prop_line_snapshot` during duplicate ingest ### MemPalace Context
- Palace: ~11,157 drawers across 10 wings
- Wings: copilot_sessions (3,776), nba_ml_engine (3,918), labs_wiki (2,231), homelab (1,013), labs_wiki_knowledge (158), openmemory_archive (49), agent wings (12)
- ChromaDB PersistentClient at `~/.mempalace/palace/`
- Wiki injection: `scripts/wiki_to_mempalace.py` uses mempalace's pipx venv Python
- Cron: `0 3 * * 0` runs `homelab/scripts/mempalace-remine.sh` (5 steps)

## Important Files

- `labs-wiki/plans/autoagent-integration.md`
- Comprehensive AutoAgent research + integration plan + custom agent creation guide
- Committed in a719db9 and 35a7ae5 (both pushed)
- Key sections: architecture diagram (~line 30), comparison matrix (~line 175), decision matrix (~line 310), custom agents guide (~line 370)

- `homelab/agents/homelab-ops.md`
- NEW — Homelab infrastructure ops agent (NOT COMMITTED)
- Service map table (13 stacks), 10 operating rules, 3 diagnostic playbooks
- 87 lines

- `homelab/agents/devops-deploy.md`
- NEW — DevOps deployment agent (NOT COMMITTED)
- 8 deployment scripts, 10 operating rules, 8-step deployment workflow, server reference
- 80 lines

- `nba-ml-engine/agents/nba-ml-pipeline.md`
- NEW — NBA-ML pipeline operations agent (NOT COMMITTED)
- 10 CLI commands, config reference table, 10 operating rules, 3 diagnostic playbooks
- 102 lines

- `labs-wiki/agents/knowledge-curator.md`
- NEW — Knowledge curator agent (NOT COMMITTED)
- 4 maintenance workflows, quality score rubric, 10 operating rules, MemPalace bridge
- 95 lines

- `labs-wiki/plans/agent-build-report.md`
- NEW — Status report with validation results (NOT COMMITTED)
- 4/4 agents PASS, 44 file refs checked, 29 commands verified

- `homelab/AGENTS.md`
- MODIFIED — Added Custom Agent Personas section at end (NOT COMMITTED)

- `nba-ml-engine/.github/copilot-instructions.md`
- MODIFIED — Added Custom Agents section near top (NOT COMMITTED)

- `labs-wiki/AGENTS.md`
- MODIFIED — Added knowledge-curator row to personas table at line 291 (NOT COMMITTED)

- `labs-wiki/tasks/lessons.md`
- NEW — Feedback loop template (NOT COMMITTED)

## Next Steps

**Immediate (in progress):**
- **Commit and push all 3 repos** — This is the critical remaining step. All files are created and validated but NOT committed:
1. `cd ~/projects/labs-wiki && git add agents/knowledge-curator.md tasks/lessons.md plans/agent-build-report.md AGENTS.md && git commit && git push`
2. `cd ~/projects/homelab && git add agents/ AGENTS.md && git commit && git push`
3. `cd ~/projects/nba-ml-engine && git add agents/ .github/copilot-instructions.md && git commit && git push`
- Update SQL todo: mark `status-report` as done after commits

**After commits:**
- Test each agent by invoking them in real Copilot CLI sessions
- Generate initial lessons.md entries from real usage
- Consider adding agents to `opencode.json` in each repo for OpenCode compatibility
- Set up quarterly agent review cadence
- After 30 days: evaluate agent usage and retire unused ones

## Related Wiki Pages

- [[Custom Copilot CLI Agents]]
- [[AutoAgent Framework Research and Integration Planning]]
- [[Agent Feedback Loop Mechanism]]
- [[AutoAgent]]
- [[Copilot CLI]]
- [[MemPalace]]
- [[Homelab]]
- [[NBA-ML Engine]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-building-4-copilot-cli-custom-agents-4d3f83bc.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-04-12 |
| URL | N/A |
