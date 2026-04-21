---
title: "Copilot Session Checkpoint: NBA-ML Agents and Homelab Fixes"
type: source
created: 2026-04-12
last_verified: 2026-04-21
source_hash: "5d62c5ec9d154108bd891ed92b71cf061018b412b20cfcfc2b686c64b646c9e9"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-nba-ml-agents-and-homelab-fixes-646cf99a.md
quality_score: 100
concepts:
  - nba-ml-specialized-prediction-agents
  - sprint-workflow-integration-for-ai-agents
  - adguard-memory-oom-diagnosis-and-fix
related:
  - "[[NBA-ML Specialized Prediction Agents]]"
  - "[[Sprint Workflow Integration for AI Agents]]"
  - "[[AdGuard Memory Out-Of-Memory (OOM) Diagnosis and Fix]]"
  - "[[Copilot CLI]]"
  - "[[AdGuard]]"
  - "[[KnightCrawler]]"
  - "[[Homelab]]"
  - "[[Labs-Wiki]]"
tier: hot
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki, nba-ml-engine, mempalace, agents, automation, docker, nba-ml, ai-agents, mlops]
checkpoint_class: durable-debugging
retention_mode: retain
knowledge_state: validated
---

# Copilot Session Checkpoint: NBA-ML Agents and Homelab Fixes

## Summary

The user is executing a multi-repo project spanning labs-wiki, homelab, and nba-ml-engine repositories. This session focused on: (1) building 4 specialized Copilot CLI agents for nba-ml-engine to improve prediction hit rates, (2) writing a sprint report integrating those agents into the existing sprint workflow, (3) diagnosing and fixing an AdGuard OOM crash on the homelab server, and (4) beginning diagnosis of a KnightCrawler issue where Peaky Blinders S06E04 wasn't returning streaming results. The session builds on extensive prior work including 4 custom agents built in the previous session, MemPalace installation, and wiki auto-ingest infrastructure.

## Key Points

- 4 nba-ml prediction agents built, validated (34 file refs, 9 CLI commands), committed and pushed
- Sprint 48 report written with agent-sprint integration mapping and 5 gap findings
- AdGuard OOM diagnosed (filter update spike) and fixed (512M limit)
- AdGuard redeployed and verified (DNS resolving)
- The user asked what other agents could be added to nba-ml-engine to improve prediction accuracy
- Created SQL todos with 6 items and dependency chain

## Execution Snapshot

**Files created:**
- `nba-ml-engine/agents/model-calibration.md` — ECE reduction, Platt/isotonic scaling, edge thresholds (committed: a4fb36a)
- `nba-ml-engine/agents/feature-lab.md` — Feature engineering experiments, ablation studies (committed: a4fb36a)
- `nba-ml-engine/agents/data-quality.md` — Data validation, timezone fixes, prop line integrity (committed: a4fb36a)
- `nba-ml-engine/agents/backtest-lab.md` — Performance regression testing, A/B experiments (committed: a4fb36a)
- `nba-ml-engine/docs/reports/sprint48-agent-driven-improvement.md` — Sprint report with agent integration (committed: 67e7763)
- `labs-wiki/plans/nba-ml-agent-expansion.md` — Agent expansion plan with gap analysis (committed: ebbbaa2)

**Files modified:**
- `nba-ml-engine/.github/copilot-instructions.md` — Added 4 agents to agent table (5 total) (committed: a4fb36a)
- `homelab/compose/compose.infra.yml` — AdGuard memory 256M → 512M (committed: 8c35ee7)

**Work completed:**
- [x] 4 nba-ml prediction agents built, validated (34 file refs, 9 CLI commands), committed and pushed
- [x] Sprint 48 report written with agent-sprint integration mapping and 5 gap findings
- [x] AdGuard OOM diagnosed (filter update spike) and fixed (512M limit)
- [x] AdGuard redeployed and verified (DNS resolving)
- [ ] KnightCrawler diagnosis — IN PROGRESS (containers healthy, DB connection established, query pending)

## Technical Details

- 16,741 LOC Python, 9-cat fantasy basketball prediction (pts, reb, ast, stl, blk, tov, fg_pct, ft_pct, fg3m)
- Models: XGBoost (primary), LightGBM, RF, Ridge, LSTM, Stacking Ensemble
- ~326 features (lags, rolling, EWMA, trend, context, opponent, injury, advanced stats)
- Current hit rate: 53.2% overall; STL 66.4%, BLK 55.4%, FG3M 54.2% (profitable); PTS 49.9%, REB 51.2% (underwater)
- ECE: 0.36 (target <0.20) — calibration is #1 bottleneck
- Vig breakeven at -110 odds = 52.4%
- Sprint 47 identified 8 critical bugs; items 1-7 deployed, 8-14 remain
- Now has 5 agents: nba-ml-pipeline (ops), model-calibration, feature-lab, data-quality, backtest-lab ### Sprint Workflow (execute-sprint-from-report)
- 10-step workflow: scope → audit → plan → implement → validate → deploy → verify → report → review → sync
- Integrates superpowers skills (TDD, subagent-driven dev, parallel agents, verification, debugging)
- Detects server vs remote mode for deployment
- Creates progress tracker in tasks/
- 5 gaps identified for agent integration (routing, data gate, backtest gate, monitoring, feedback) ### KnightCrawler Infrastructure
- 6 containers: addon (port 7000), producer, consumer, postgres, redis, lavinmq
- DB: postgres user `postgres`, database `knightcrawler`
- Two critical cron jobs: kc-populate-files.sh (15min), kc-scrape-recent.sh (6h)
- kc-populate-files.sh maps DMM torrents to files table via 4-pass SQL
- Previous issue: populate-files.sh missing +x permission (fixed April 5)
- Peaky Blinders IMDB IDs: tt2442560 (series), tt13968894 (possible season/episode) ### AdGuard
- Container in compose.infra.yml, restart: unless-stopped
- Memory increased 256M → 512M after OOM kill during filter refresh
- 3 filter lists totaling 600K+ rules; largest filter hit 421K rules (9.7MB)
- Binds to both SERVER_IP and TAILSCALE_IP on port 53 ### Server Environment
- Running directly on beelink-gti13 (hostname confirmed), no SSH needed
- SSH key auth to beelink-gti13 is NOT configured from this session (Permission denied on both hostname and IP)
- 31GB RAM, swap nearly full (7.9/8.0GB), disk 150G/914G used
- Compose commands: `docker compose --env-file .env -f compose/docker-compose.yml -f compose/compose.<stack>.yml up -d <service>`

## Important Files

- `nba-ml-engine/agents/model-calibration.md`
- Calibration specialist agent — ECE reduction, per-stat isotonic/Platt scaling, edge thresholds
- Created this session, committed a4fb36a
- Key sections: operating rules (10 rules), diagnostic playbooks (ECE spike, inverse edge-accuracy)

- `nba-ml-engine/agents/data-quality.md`
- Data validation agent — timezone fixes, prop line integrity, silent failure elimination
- Created this session, committed a4fb36a
- Key sections: known bugs table (6 Sprint 47 bugs), validation queries, diagnostic playbooks

- `nba-ml-engine/agents/feature-lab.md`
- Feature engineering agent — experiment workflow, ablation studies, gap analysis table
- Created this session, committed a4fb36a
- Key sections: feature gap analysis (6 missing categories), experiment workflow (8-step protocol)

- `nba-ml-engine/agents/backtest-lab.md`
- Regression testing agent — 10-point pre-deploy protocol, A/B testing, drawdown monitoring
- Created this session, committed a4fb36a
- Key sections: pre-deployment checklist, edge bucket analysis table, metrics reference

- `nba-ml-engine/docs/reports/sprint48-agent-driven-improvement.md`
- Sprint report mapping agents into sprint workflow, 4 phases, 5 gaps identified
- Created this session, committed 67e7763
- Key sections: agent-sprint integration table, gap analysis (5 gaps), success criteria table

- `nba-ml-engine/.opencode/skills/execute-sprint-from-report/SKILL.md`
- Sprint execution skill — 10-step workflow with superpowers integration
- Not modified, but central to understanding agent integration
- Key: steps map, deploy rules, superpowers skill table

- `homelab/compose/compose.infra.yml`
- AdGuard + uptime-kuma + other infra services
- Modified: AdGuard memory 256M → 512M (line ~21)
- Committed 8c35ee7

- `labs-wiki/plans/nba-ml-agent-expansion.md`
- Agent expansion plan with impact projections (+4-7% HR)
- Created this session, committed ebbbaa2
- Key sections: gap analysis, agent interaction map, priority order

## Next Steps

**Immediate (in progress):**
- **KnightCrawler diagnosis for Peaky Blinders S06E04** — containers are all healthy, DB connection established (user: postgres, db: knightcrawler). Need to:
1. Query torrents table for Peaky Blinders (IMDB: tt2442560) — check if torrents exist
2. Query files table for S06E04 specifically — check if file mappings exist
3. Check addon logs for the specific request that failed
4. Check if kc-populate-files.sh cron is running and mapping torrents → files correctly
5. The "torrent being downloaded" message suggests torrents exist but files table mapping may be missing (same issue as the April 5 fix)

**DB query format that works:**
```bash
docker exec knightcrawler-postgres psql -U postgres -d knightcrawler -c "QUERY"
```

**After KnightCrawler fix:**
- Consider building automated health-check scripts from agent playbooks for Ofelia
- Sprint 48 execution (data-quality → model-calibration → backtest-lab → feature-lab phases)
- Update sprint skill SKILL.md with agent routing table (Gap 1 from sprint report)

## Related Wiki Pages

- [[NBA-ML Specialized Prediction Agents]]
- [[Sprint Workflow Integration for AI Agents]]
- [[AdGuard Memory Out-Of-Memory (OOM) Diagnosis and Fix]]
- [[Copilot CLI]]
- [[AdGuard]]
- [[KnightCrawler]]
- [[Homelab]]
- [[Labs-Wiki]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-nba-ml-agents-and-homelab-fixes-646cf99a.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-04-12 |
| URL | N/A |
