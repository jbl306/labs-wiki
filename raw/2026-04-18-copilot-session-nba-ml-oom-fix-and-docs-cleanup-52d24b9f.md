---
title: "Copilot Session Checkpoint: NBA ML OOM fix and docs cleanup"
type: text
captured: 2026-04-18T01:37:38.386572Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki, nba-ml-engine, mempalace, agents]
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** NBA ML OOM fix and docs cleanup
**Session ID:** `2e3d0a8c-0302-474f-a269-e28a5a23b123`
**Checkpoint file:** `/home/jbl/.copilot/session-state/2e3d0a8c-0302-474f-a269-e28a5a23b123/checkpoints/002-nba-ml-oom-fix-and-docs-cleanu.md`
**Checkpoint timestamp:** 2026-04-13T13:18:45.595975Z
**Exported:** 2026-04-18T01:37:38.386572Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user reported NBA ML containers dying from OOM, then asked to add MemPalace instructions to AGENTS.md, remove all OpenMemory references from the homelab repo, change a mempalace cron from weekly to daily, and remove stale agent persona files from the labs-wiki repo. I diagnosed the OOM, bumped memory limits, re-ran the pipeline, updated documentation across both repos, and cleaned up deprecated references.
</overview>

<history>
1. User reported NBA ML containers died OOM
   - Inspected all 5 NBA ML containers — all running but showed recent restarts
   - Found `nba-ml-db` (postgres) was OOM-killed at 768M cgroup limit during daily pipeline's bulk INSERT INTO game_logs at 07:00 UTC
   - Found `nba-ml-scheduler` (ofelia) also OOM-killed at 64M limit seconds later
   - Kernel dmesg confirmed: `constraint=CONSTRAINT_MEMCG` for both processes
   - Pipeline-daily job never completed — killed mid-execution
   - Also discovered yesterday's `weekly-retrain` failed due to MLflow DNS resolution error (separate issue)
   - Bumped `nba-ml-db` from 768M → 2G and `nba-ml-scheduler` from 64M → 256M in compose file
   - Validated compose config, recreated both containers with new limits
   - Re-ran `docker exec nba-ml-api python main.py pipeline` — ingestion completed successfully (26,651 game logs, 390 tracking stats, etc.)
   - Training step started (Optuna tuning) — running for hours in background
   - DB at 567-624MB during training — safely under new 2G limit
   - Committed (22d1f3a) and pushed to GitHub

2. User asked about Odds API quota issue — said it should be in mempalace
   - Pushed the OOM fix commit first
   - Verified pipeline still running (6.6GB API container, DB healthy)
   - Searched mempalace: found documented known issue — Odds API key exhausted monthly quota, SportsGameOdds provides fallback
   - Confirmed this matches what we saw in pipeline logs (401 from Odds API, SGO fallback working)

3. User asked why mempalace wasn't automatically searched at session start
   - Explained two gaps: (1) no instruction to search mempalace at session start, only OpenMemory instructions existed; (2) the 401 was a secondary finding during diagnostics, not the primary issue
   - Proposed three triggers: session-start search, error-encounter cross-reference, post-resolution storage
   - User approved adding to AGENTS.md

4. User asked to add MemPalace instructions and remove all OpenMemory references
   - Added compact MemPalace section to AGENTS.md (lines 154-165) with three triggers
   - Removed `memory` from available stacks list in AGENTS.md
   - Removed OpenMemory from README.md: service tables (2 rows), architecture diagram
   - Removed OpenMemory section from docs/05-service-guide.md (86 lines)
   - Removed OpenMemory row from docs/08-cloudflare-tunnel.md
   - Removed memory-ui DNS rewrite from config/adguard/dns-rewrites.json
   - Left docs/12-mempalace-setup.md untouched (documents migration history)
   - Committed (5097a99) and pushed

5. User asked to change mempalace-remine.sh cron from weekly to daily
   - Found crontab entry: `0 3 * * 0` (Sunday 3am)
   - Changed to `0 3 * * *` (daily 3am)
   - Updated comment from "weekly Sunday 3am" to "daily 3am"

6. User asked about duplicate agents directories in labs-wiki (root `agents/` vs `.github/agents/`)
   - Initially misunderstood — thought they meant homelab repo. User clarified: labs-wiki repo
   - Found root `agents/` has 5 old persona-style MDs (researcher, compiler, curator, knowledge-curator, auditor)
   - Found `.github/agents/` has 7 Copilot-format agent specs with YAML frontmatter
   - Root `agents/` not loaded by any code — only referenced in docs. `.github/agents/` is the active set (validated by setup.sh)
   - User approved removal

7. Removed stale labs-wiki agents/ directory
   - `git rm -r agents/` — removed 5 files (245 lines)
   - Updated AGENTS.md: replaced persona table with `.github/agents/` agent table (7 agents)
   - Updated .github/copilot-instructions.md: directory map and scoped instructions table
   - Updated README.md: removed `agents/` from architecture tree
   - Staged all changes (8 files, +12/-261 lines) — NOT YET COMMITTED
</history>

<work_done>
Files updated (homelab repo — committed and pushed):
- `compose/compose.nba-ml.yml`: nba-ml-db 768M→2G, nba-ml-scheduler 64M→256M (commit 22d1f3a)
- `AGENTS.md`: Added MemPalace section, removed `memory` from stacks (commit 5097a99)
- `README.md`: Removed OpenMemory UI, MCP, Qdrant rows + architecture diagram reference (commit 5097a99)
- `docs/05-service-guide.md`: Removed entire OpenMemory section (86 lines) (commit 5097a99)
- `docs/08-cloudflare-tunnel.md`: Removed OpenMemory MCP row (commit 5097a99)
- `config/adguard/dns-rewrites.json`: Removed memory-ui.jbl-lab.com entry (commit 5097a99)

System changes:
- Crontab: mempalace-remine.sh changed from weekly (`0 3 * * 0`) to daily (`0 3 * * *`)
- Containers recreated: nba-ml-db and nba-ml-scheduler with new memory limits
- Pipeline re-run triggered — ingestion complete, training in progress (long-running, hours)

Files updated (labs-wiki repo — STAGED, NOT COMMITTED):
- `agents/` directory: 5 files deleted via git rm
- `AGENTS.md`: Agent Personas section rewritten to reference `.github/agents/`
- `.github/copilot-instructions.md`: Directory map updated, removed `agents/**/*.md` scoped instruction
- `README.md`: Removed `agents/` from architecture tree

Unstaged changes in homelab repo (not ours):
- `compose/compose.monitoring.yml` and `config/prometheus/prometheus.yml` have pre-existing uncommitted changes

Work completed:
- [x] Diagnosed and fixed NBA ML OOM (memory limits bumped)
- [x] Re-ran daily pipeline (ingestion done, training running)
- [x] Added MemPalace instructions to AGENTS.md
- [x] Removed all OpenMemory references from homelab repo
- [x] Changed mempalace-remine.sh cron to daily
- [x] Removed stale labs-wiki agents/ directory
- [ ] Labs-wiki changes staged but NOT committed/pushed
</work_done>

<technical_details>
- **NBA ML OOM root cause**: Daily pipeline at 07:00 UTC does bulk INSERT INTO game_logs. Postgres worker process hit 768M cgroup limit → kernel OOM killed it (signal 9). Ofelia scheduler at 64M also OOM'd from buffering job stdout/stderr. Both auto-recovered (postgres WAL replay, ofelia re-registered jobs), but pipeline never completed.
- **nba-ml-scheduler (ofelia)**: Uses `job-exec` labels to docker exec commands into other containers (mainly nba-ml-api). The 64M limit is for ofelia itself, not the jobs — but it buffers all job output which can spike memory.
- **Odds API**: Key `eb4a4ca82b5709fde429d542cb9bfcc0` has exhausted monthly quota (500 free tier). All requests return 401. Both prop_lines and game_lines have SportsGameOdds fallback. Known issue documented in mempalace.
- **Weekly retrain failure**: Yesterday's `weekly-retrain` job failed — MLflow DNS resolution error (`nba-ml-mlflow` not resolving). This is a separate issue from OOM, not yet investigated.
- **System swap**: Fully exhausted at 8GB/8GB — compounds OOM issues. Not addressed.
- **MemPalace vs OpenMemory**: OpenMemory (Docker-based: Qdrant + MCP + UI) was replaced by MemPalace (local MCP, no containers). Migration documented in docs/12-mempalace-setup.md. The compose.memory.yml is archived (`.archived` extension).
- **labs-wiki agents**: Root `agents/` had freeform persona definitions. `.github/agents/` has Copilot-format specs with YAML frontmatter (name, description, tools, model). Only `.github/agents/` is validated by setup.sh and used by Copilot.
- **Pipeline training**: Running inside nba-ml-api container (14G limit, 4 CPUs). Uses Optuna hyperparameter tuning. Pipeline mode expected ~4.4 hours. Shell session `pipeline-run` may still be active.
- **NBA API flakiness**: BoxScorePlayerTrackV3 endpoint consistently times out. Pipeline has built-in fallback: after 3 consecutive failures, switches to curl_cffi browser fallback which succeeded (390 rows).
</technical_details>

<important_files>
- `compose/compose.nba-ml.yml` (homelab)
   - Defines all 5 NBA ML services with resource limits
   - Changed nba-ml-db memory 768M→2G (line 31), nba-ml-scheduler 64M→256M (line 165)
   - Committed and pushed

- `AGENTS.md` (homelab)
   - Central agent instructions file for the homelab repo
   - Added MemPalace section at end (lines ~154-165): session-start search, error cross-ref, post-resolution storage
   - Removed `memory` from available stacks (line 21)
   - Committed and pushed

- `README.md` (homelab)
   - Service inventory and architecture diagram
   - Removed 3 OpenMemory rows from service tables, removed `[memory]` from architecture
   - Committed and pushed

- `AGENTS.md` (labs-wiki)
   - Agent Personas section (lines ~279-293) rewritten from old 5-persona table pointing to `agents/` → new 7-agent table pointing to `.github/agents/`
   - STAGED, not committed

- `.github/copilot-instructions.md` (labs-wiki)
   - Directory map updated (line 12): `agents/` → `.github/agents/`
   - Removed `agents/**/*.md` scoped instruction row (was line 50)
   - STAGED, not committed

- `README.md` (labs-wiki)
   - Architecture tree: removed `agents/` line
   - STAGED, not committed

- `config/adguard/dns-rewrites.json` (homelab)
   - Removed memory-ui.jbl-lab.com DNS rewrite entry
   - Committed and pushed
</important_files>

<next_steps>
Remaining work:
- **Labs-wiki commit**: Changes are staged but NOT committed or pushed. Need to commit and push the agents/ removal + doc updates.
- **Pipeline monitoring**: Training pipeline is running in background (shell `pipeline-run`). Should complete in a few hours. No action needed unless it fails.
- **MLflow DNS issue**: Yesterday's weekly-retrain failed due to MLflow DNS resolution. Not investigated yet — may recur next Sunday.
- **Swap exhaustion**: System swap at 8GB/8GB — not addressed, could cause future OOM cascades.

Immediate next action:
- Commit and push the labs-wiki changes (staged: 8 files, +12/-261)
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
