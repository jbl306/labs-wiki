---
title: "Copilot Session Checkpoint: Sprint Accuracy Planning"
type: text
captured: 2026-05-31T23:07:45.741410Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, nba-ml-engine, mempalace, agents, dashboard]
checkpoint_class: project-progress
checkpoint_class_rule: "body:sprint 62"
retention_mode: compress
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint Accuracy Planning
**Session ID:** `29085277-dd99-479d-9108-a1b945876488`
**Checkpoint file:** `/home/jbl/.copilot/session-state/29085277-dd99-479d-9108-a1b945876488/checkpoints/001-sprint-accuracy-planning.md`
**Checkpoint timestamp:** 2026-05-31T22:43:51.377414Z
**Exported:** 2026-05-31T23:07:45.741410Z
**Checkpoint class:** `project-progress` (rule: `body:sprint 62`)
**Retention mode:** `compress`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user first requested a review of `nba-ml-engine` across DB accuracy, props accuracy, and dashboard accuracy, with gaps converted into the next sprint. After that sprint backlog was created, the user asked to implement all P0 and P1 items. The current approach is to implement a shared canonical settled-prop population first, then rewire edge generation, calibration/model-health, matviews, dashboard contracts, and tests around it.
</overview>

<history>
1. User asked: “review nba-ml-engine repo, db accuracy, props accuracy, dashboard accuracy. identify gaps and improvements and put in next sprint”
   - Loaded `task-observer`, NBA skills (`sprint-orchestrator`, `data-quality`, `dashboard`, `backtest-lab`, `model-calibration`), MemPalace context, repo rules, and recent reports.
   - Dispatched three parallel researcher agents: DB/data accuracy, props/model accuracy, dashboard/BFF accuracy.
   - Ran live read-only Postgres queries via `docker exec -i nba-ml-db ... psql` because local `config.DATABASE_URL` password failed for user `nba_ml`.
   - Added a new sprint section to `nba-ml-engine/tasks/todo.md`: **2026-05-31: Sprint 62 - Accuracy Trust Hardening**.
   - Stored the audit findings in MemPalace and wrote a diary entry.

2. User then asked: “implement p0 and p1”
   - Loaded `task-observer` again, then NBA/domain skills and brainstorming/context.
   - Created a session plan at `/home/jbl/.copilot/session-state/29085277-dd99-479d-9108-a1b945876488/plan.md`.
   - Reset session SQL todos into implementation workstreams:
     - `canonical-helper`
     - `snapshot-identity`
     - `prop-edge-gates`
     - `calibration-health`
     - `canonical-matviews`
     - `dashboard-contracts`
     - `validation-tests`
   - Began mapping the edit surface and reading target modules.
   - No code changes for P0/P1 implementation had been applied yet before compaction.
</history>

<work_done>
Files modified:
- `/home/jbl/projects/nba-ml-engine/tasks/todo.md`
  - Added Sprint 62 backlog with audit baseline, P0 plan, P1 plan, P2 plan, and validation gates.

Files created/updated outside repo:
- `/home/jbl/.copilot/session-state/29085277-dd99-479d-9108-a1b945876488/plan.md`
  - Contains the implementation plan for Sprint 62 P0/P1.

Completed:
- Reviewed repo and live DB state.
- Identified major accuracy gaps.
- Added next sprint backlog.
- Started implementation planning.

In progress:
- Implementing Sprint 62 P0/P1.
- Most recent action before compaction: reading target modules:
  - `src/applications/prop_finder.py`
  - `src/applications/edge_policy.py`
  - `src/data/prop_lines.py`
  - `src/data/prop_history.py`
  - `src/db/models.py`
  - `config.py`

Untested:
- No P0/P1 implementation changes yet, so no tests/builds have been run for implementation.
</work_done>

<technical_details>
Live DB audit evidence from `nba-ml-db`:
- `game_logs` latest: `2026-05-30`
- `predictions` latest: `2026-05-31`
- `prop_lines` and `prop_line_snapshots` latest: `2026-06-03`
- Latest joined prop+prediction slate: `2026-05-26`
- `prop_line_snapshots`: `24,421` rows and `24,421` coarse identities, implying repeated captures are not preserving multi-point history.
- Last 30 days:
  - `6,080` settled snapshots
  - `2,238` canonical joined bets
  - `4,360` broad matview calls
- Calibration join fan-out: `3.80x`
- Latest model health: `degraded`, ECE `0.026`, hit rate `60.2%`, PTS alert `42.4%` over `92` seven-day predictions.
- Example latest slate line mismatches:
  - Victor Wembanyama REB `3.5` vs `12.5`
  - Josh Hart REB `2.5` vs `7.5`
  - Jalen Brunson AST `2.5` vs `6.5`
  - Josh Hart STL `0.5` vs `1.5`

Important implementation direction:
- Build one canonical settled-bet helper/CTE first.
- Canonical identity should use immutable snapshot data, not mutable `prop_lines`: `player_id + game_date + stat_name + source/bookmaker + line + fetched_at/snapshot_id`.
- Calibration, model-health, backtest-like endpoints, Props History, and matviews should consume this canonical population.
- Avoid hiding data problems in dashboard fallbacks.
- Heavy aggregation belongs in materialized views, not BFF request-time logic.
- Prefer NULL over invented defaults.
- Do not mutate production DB unless a migration is explicitly needed; use read-only validation for live DB checks.

Tool/env quirks:
- App default local DB connection failed: password authentication failed for `nba_ml` at localhost:5432.
- Querying through Docker container worked: `docker exec -i nba-ml-db sh -lc 'psql ...'`.
</technical_details>

<important_files>
- `/home/jbl/projects/nba-ml-engine/tasks/todo.md`
  - Main sprint tracker.
  - Modified to add **Sprint 62 - Accuracy Trust Hardening**.
  - New section is at the top of the file.

- `/home/jbl/.copilot/session-state/29085277-dd99-479d-9108-a1b945876488/plan.md`
  - Session-only implementation plan.
  - Lists shared boundary, workstreams, and risk controls.

- `/home/jbl/projects/nba-ml-engine/src/applications/prop_finder.py`
  - Central for prop edge generation.
  - Needs vig/EV gate, absolute edge threshold enforcement, probability/EV metadata, Kelly/P&L standardization.

- `/home/jbl/projects/nba-ml-engine/src/applications/edge_policy.py`
  - Existing policy surface likely relevant for edge gates/thresholds.

- `/home/jbl/projects/nba-ml-engine/src/data/prop_lines.py`
  - Prop line ingestion/normalization.
  - Needs suspicious provider-line validation/quarantine.

- `/home/jbl/projects/nba-ml-engine/src/data/prop_history.py`
  - Snapshot capture and settlement logic.
  - Needs immutable point-in-time snapshot identity.

- `/home/jbl/projects/nba-ml-engine/src/db/models.py`
  - SQLAlchemy models for `PropLine`, `PropLineSnapshot`, predictions, model health, etc.
  - Key for constraints/indexes if snapshot identity requires schema/model changes.

- `/home/jbl/projects/nba-ml-engine/scripts/optimize_db.py`
  - Defines/refreshes matviews such as `mv_daily_hit_rates`, `mv_backtest_summary`, `mv_clv_daily`, `mv_dashboard_metrics`, `mv_prop_lines_primary`.
  - Needs canonical population/freshness updates.

- `/home/jbl/projects/nba-ml-engine/src/api/server.py`
  - FastAPI endpoints for calibration, model health, dashboard/backtest-style data.
  - Needs rewiring to canonical population/source metadata.

- `/home/jbl/projects/nba-ml-engine/dashboard-ui/server/src/index.ts`
  - Dashboard BFF.
  - Needs non-silent failures, metadata propagation, freshness/CLV/edge unit contract hardening.

- `/home/jbl/projects/nba-ml-engine/dashboard-ui/server/src/dashboardContracts.ts`
  - Dashboard response contract definitions.
  - Likely needs new metadata fields and unit/source labels.
</important_files>

<next_steps>
Continue implementing P0/P1 in this order:

1. Read enough of the target modules to understand current helper patterns and tests.
2. Mark `canonical-helper` in progress in session SQL todos.
3. Add a canonical settled-prop population helper/CTE module.
4. Make `prop_line_snapshots` immutable by changing snapshot upsert identity and adding regression tests.
5. Add provider-line validation/quarantine and prop edge gates in `prop_finder.py`/policy code.
6. Rewire calibration/model-health to canonical settled population.
7. Rebuild matview SQL in `scripts/optimize_db.py` around canonical population and freshness.
8. Harden dashboard/BFF contracts and UI metadata/error handling.
9. Add focused tests and run relevant backend pytest plus dashboard build/tests.
10. Run read-only SQL validation gates against `nba-ml-db`.
11. Update `tasks/todo.md` Review section and MemPalace diary when complete.

Current session SQL todos already exist with dependencies; query them with:
`SELECT * FROM todos ORDER BY id;`
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
