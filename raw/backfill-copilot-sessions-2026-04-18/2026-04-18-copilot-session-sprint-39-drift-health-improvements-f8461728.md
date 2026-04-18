---
title: "Copilot Session Checkpoint: Sprint 39 drift health improvements"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard]
status: pending
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint 39 drift health improvements
**Session ID:** `8d466128-8017-482d-b021-0fffe970d5eb`
**Checkpoint file:** `/home/jbl/.copilot/session-state/8d466128-8017-482d-b021-0fffe970d5eb/checkpoints/008-sprint-39-drift-health-improve.md`
**Checkpoint timestamp:** 2026-03-30T22:17:55.634592Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user is running sprint-based development on the NBA ML Engine project on a homelab server (beelink-gti13). This session segment covered: completing Sprint 38 documentation updates, diagnosing and fixing server resource issues (training OOM, cadvisor crash loop, Ofelia cron bugs), resuming a failed ML training pipeline, and beginning Sprint 39 implementation (drift & health monitoring improvements). The approach follows the execute-sprint-from-report skill workflow with autonomous diagnosis, fix, deploy, and verify cycles.
</overview>

<history>
1. **Documentation update completion** (carried over from previous segment)
   - Sprint 38 code was already committed; documentation audit identified gaps in 4 files
   - Launched 3 parallel general-purpose agents to update README.md, docs/02-data-layer.md, docs/05-training-pipeline.md, docs/06-applications.md, docs/07-deployment.md
   - All agents completed successfully: +195/-61 lines across 5 files
   - Committed as `d571399` and pushed to GitHub

2. **User asked: "check on nba-ml-api training, is it stuck?"**
   - Diagnosed: Today's daily pipeline completed OK (5h48m), but yesterday's weekly retrain was OOM-killed (exit 137 after 38m at 10GB limit)
   - Found 3 additional issues: health check JSONB error (already fixed by Sprint 38 rebuild), post-retrain-analysis cron broken (`&&` not supported by Ofelia), Odds API 401 errors (fallback source)

3. **User asked to fix training OOM and cron issues**
   - Increased API container memory 10G→14G in `compose.nba-ml.yml` (system has 31GB, 23GB available)
   - Wrapped post-retrain-analysis Ofelia command in `/bin/bash -c '...'` for shell chain support
   - Deployed both fixes, verified scheduler registered corrected commands
   - Committed to homelab repo and pushed

4. **User reported CPU/memory overload on server**
   - Diagnosed: cadvisor at 26% CPU constant (monitoring 40+ containers), MLflow spawning too many workers (6 processes swapped), 3GB swap from OOM event
   - Fixed cadvisor: added `--housekeeping_interval=30s`, `--docker_only=true`, disabled unused metric collectors
   - Fixed MLflow: added `--workers 2`, reduced memory limit 2G→1.5G
   - Increased prometheus cadvisor scrape interval 15s→30s
   - Results: cadvisor 26%→<1% CPU, 195MB→26MB memory, swap 3GB→1.9GB, load 2.62→0.92
   - Committed and pushed homelab changes

5. **cadvisor crash-looping after fix**
   - Root cause: `accelerator` is not a valid `disable_metrics` value in cadvisor v0.55.1
   - Fixed with only valid metric names: `advtcp,cpu_topology,cpuset,hugetlb,memory_numa,percpu,perf_event,process,referenced_memory,resctrl,sched,tcp,udp`
   - Redeployed, verified healthy at 5.75% CPU, 25.8MB memory
   - Also confirmed 8-hour training timeout is adequate (pipeline has 4 steps, worst case ~5.5h)

6. **User asked to resume ML training from where it died**
   - Launched `docker exec -d` with `python main.py train --full-pipeline`
   - First exec didn't capture output; launched second with log redirect to `/tmp/training.log`
   - Discovered both were running simultaneously (double memory usage: 10GB)
   - Killed duplicate process (PID 32 inside container), memory dropped 10GB→5GB
   - Training progressed through all 4 steps successfully in 478 minutes
   - All 9 stat models + classifiers + calibrators trained, ntfy notification sent

7. **User invoked execute-sprint-from-report for Sprint 39: high + medium next steps**
   - Read Sprint 38 report, extracted next steps
   - Ran explore agent to audit codebase for all 6 Sprint 39 planning questions
   - Created branch `feature/sprint-39-drift-health-improvements`
   - Created progress tracker, set up SQL todos with dependencies
   - **Started implementing temporal drift filter in dispatcher.py**
   - Edit applied to dispatcher.py — filtering temporal features from drift alerts
   - Was about to implement dashboard components (DriftTrendsPanel, health comparison) when compaction triggered
</history>

<work_done>
## Completed:
- ✅ Sprint 38 documentation update (5 files, committed d571399, pushed)
- ✅ Training OOM fix (API memory 10G→14G)
- ✅ Ofelia cron fix (bash -c wrapper for && chains)
- ✅ Server resource optimization (cadvisor, MLflow, prometheus)
- ✅ cadvisor crash loop fix (valid disable_metrics values)
- ✅ Full ML retrain completed (478 min, all models + classifiers + calibrators)
- ✅ Lessons documented in tasks/lessons.md (Ofelia shell operators, OOM limits)

## Sprint 39 In Progress:
- ✅ Branch created: `feature/sprint-39-drift-health-improvements`
- ✅ Progress tracker: `tasks/PROGRESS-sprint39-drift-health-0330.md`
- ✅ SQL todos set up (6 items with dependencies)
- ✅ `temporal-drift-filter` — dispatcher.py edited (TEMPORAL_DRIFT_FEATURES set added, actionable_drifted filtering, temporal_drifted in details)
- 🔄 `investigate-opp-drift` — marked in_progress but not yet analyzed
- ⬜ `drift-trends-panel` — DriftTrendsPanel.tsx not yet created (API endpoint + types already exist)
- ⬜ `health-comparison` — not yet started
- ⬜ `deploy-verify` — blocked on above
- ⬜ `sprint-report` — blocked on deploy

## Current Git State:
- Branch: `feature/sprint-39-drift-health-improvements`
- 1 unstaged edit: `src/notifications/dispatcher.py`
- 1 new file: `tasks/PROGRESS-sprint39-drift-health-0330.md`
</work_done>

<technical_details>
### Temporal Drift Filtering (Sprint 39 core change)
- Features `month`, `season_phase`, `season_game_number`, `game_hour`, `day_of_week` always show high PSI because 90-day reference vs 7-day inference windows span different calendar periods
- Fix: `TEMPORAL_DRIFT_FEATURES` set in dispatcher.py filters these from `drift_count` and alert messages
- PSI snapshots still stored for ALL features (including temporal) for trend tracking
- `details["temporal_drifted"]` added to health snapshot for dashboard display

### opp_vs_pos_reb_avg Investigation Findings (from explore agent)
- Feature created in `src/features/builder.py:569-620` via `_add_opp_vs_position_features()`
- Uses expanding rolling average with 1-day shift, min 3 periods
- Groups by `(opponent_team, position, season, game_date)`
- PSI=0.26 (just above 0.2 threshold) — needs further analysis to determine if actionable

### Training Pipeline Details
- Full pipeline: 4 steps (minutes → 9 stat models → classifiers → calibrators)
- Duration: 478 minutes with 14GB memory limit
- Peak memory: ~10GB during Optuna tuning + feature matrix construction
- Post-retrain ECE: 0.3492, hit rate: 51.7%, drift count: 7 (pre-temporal-filter)
- Calibrator reduced ECE from 0.3492 → 0.0000 (isotonic regression on 13,123 samples)
- Classifiers had modest AUC (stl=0.574, blk=0.500, fg3m=0.503, reb=0.550)

### cadvisor Valid disable_metrics Values (v0.55.1)
- Valid: `advtcp,app,cpu,cpuLoad,cpu_topology,cpuset,disk,diskIO,hugetlb,memory,memory_numa,network,oom_event,percpu,perf_event,pressure,process,referenced_memory,resctrl,sched,tcp,udp`
- `accelerator` is NOT valid despite appearing in older docs
- Default disabled: `advtcp,cpu_topology,cpuset,hugetlb,memory_numa,process,referenced_memory,resctrl,sched,tcp,udp`

### Ofelia Cron Limitation
- `job-exec` commands pass args directly to `docker exec`, not through shell
- `&&`, `||`, pipes, redirects all fail silently or cause argument parsing errors
- Fix: wrap in `/bin/bash -c '...'`

### Docker exec -d Behavior
- `docker exec -d` output does NOT appear in `docker logs` — it's fully detached
- Must redirect output inside the container: `/bin/bash -c 'cmd > /tmp/log 2>&1'`
- PYTHONUNBUFFERED=1 required for real-time output

### Server Resources (beelink-gti13)
- 31GB RAM, 20 CPUs, 8GB swap
- API container: 14GB limit (was 10G, OOM at 38min)
- MLflow: 1.5GB limit, 2 workers (was 2G, default workers)
- cadvisor: 256MB limit, 0.25 CPU, docker_only mode
- ~40 containers total across all services

### Dashboard Architecture (for Sprint 39 UI work)
- HealthPage.tsx renders: Header → Table Health → Pipeline Calendar → ModelHealthPanel → FeatureDriftPanel
- FeatureDriftPanel: horizontal bar chart, top 15 features, color-coded PSI severity
- ModelHealthPanel: status card + ECE/hit rate trend line charts
- DriftTrendsPanel: NOT YET CREATED — API endpoint `/evaluation/drift-trends` returns `{features: [{name, max_psi}], snapshots: [{checked_at, feature_name, psi_value, drift_status}]}`
- API types + fetch function already exist in `dashboard-ui/src/lib/api.ts` (DriftTrendsData type, driftTrends function)
- BFF proxy already exists in `dashboard-ui/server/src/index.ts`
</technical_details>

<important_files>
- `src/notifications/dispatcher.py`
   - Core of Sprint 39 work — health check orchestration, drift alert generation, PSI snapshot storage
   - EDITED: Added TEMPORAL_DRIFT_FEATURES set (line ~241), filtering temporal features from drift_count and alerts, adding temporal_drifted to details
   - Key sections: check_model_health() function (lines ~200-315), PSI snapshot insert (lines ~258-282), health snapshot insert (lines ~286-306)

- `src/api/server.py`
   - FastAPI endpoints — may need health comparison endpoint added
   - model-health endpoint: lines 1292-1343 (reads latest snapshot from DB)
   - model-health/history: lines 1346-1377 (time series)
   - drift-trends: lines 1380-1424 (top-N drifted features with PSI trends)

- `dashboard-ui/src/pages/HealthPage.tsx`
   - Health page layout — needs DriftTrendsPanel added after FeatureDriftPanel (line ~99)
   - Current components: Table Health, Pipeline Calendar, ModelHealthPanel, FeatureDriftPanel

- `dashboard-ui/src/components/charts/FeatureDriftPanel.tsx`
   - Existing PSI bar chart — for reference when building DriftTrendsPanel
   - Lines 42-142: horizontal bar chart, top 15, color-coded severity

- `dashboard-ui/src/components/charts/ModelHealthPanel.tsx`
   - May need health comparison section added (before/after retrain metrics)

- `dashboard-ui/src/lib/api.ts`
   - Already has DriftTrendsData type + driftTrends() fetch function (line ~34, types lines ~527-542)
   - Will need HealthComparisonData type if adding comparison endpoint

- `~/projects/homelab/compose/compose.nba-ml.yml`
   - Deployment config — recently modified: API memory 14G, MLflow workers 2 + 1.5G, post-retrain cron fixed
   - All changes committed and pushed to homelab repo

- `~/projects/homelab/compose/compose.monitoring.yml`
   - cadvisor config — fixed disable_metrics, added docker_only + housekeeping_interval flags
   - Committed and pushed

- `src/features/builder.py`
   - Feature engineering — `_add_opp_vs_position_features()` at lines 569-620 creates opp_vs_pos_reb_avg
   - Relevant for investigating drift (Sprint 39 H2)

- `tasks/PROGRESS-sprint39-drift-health-0330.md`
   - Sprint 39 progress tracker — NEW, lists implementation/validation/deployment checklists

- `docs/reports/sprint38-s34-next-steps.md`
   - Source report for Sprint 39 next steps
</important_files>

<next_steps>
## Active Sprint: Sprint 39 — Drift & Health Improvements
Branch: `feature/sprint-39-drift-health-improvements`

### Remaining Todos (from SQL):
1. **temporal-drift-filter** (in_progress) — dispatcher.py edit is DONE but needs testing
2. **investigate-opp-drift** (in_progress) — Need to analyze opp_vs_pos_reb_avg PSI=0.26: run feature drift analysis, compare distributions, determine if actionable or expected seasonal variation
3. **drift-trends-panel** (pending, depends on temporal-drift-filter) — Create `dashboard-ui/src/components/charts/DriftTrendsPanel.tsx` with multi-line Recharts chart showing PSI over time per feature. API types and BFF proxy already exist.
4. **health-comparison** (pending) — Add before/after retrain comparison to ModelHealthPanel or new component. Query model_health_snapshots for latest two snapshots, show ECE/hit rate/drift deltas.
5. **deploy-verify** (pending, depends on 1-4) — Build + deploy nba-ml-api and nba-ml-dashboard, run health-check, verify endpoints + dashboard
6. **sprint-report** (pending, depends on 5) — Write docs/reports/sprint39-drift-health.md

### Immediate Next Actions:
1. Finish backend: add `/evaluation/model-health/comparison` endpoint to server.py
2. Create DriftTrendsPanel.tsx component (line chart with Recharts)
3. Add health comparison section to ModelHealthPanel or new component
4. Add DriftTrendsPanel to HealthPage.tsx
5. Run pytest + tsc --noEmit to validate
6. Deploy both containers, run health-check, verify live
7. Write sprint report, commit, merge to main, push

### Key Context for Implementation:
- The DriftTrendsPanel API is ready (`/evaluation/drift-trends`), types exist in api.ts, BFF proxy exists
- For health comparison, query `model_health_snapshots ORDER BY checked_at DESC LIMIT 2` to get before/after
- The temporal drift filter edit in dispatcher.py changes `drift_count` to only count non-temporal features, which will change the model-health API response (status may flip from "degraded" to "healthy" if only temporal features are drifted)
- Server mode deployment: `docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache <service> && ... up -d`
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
