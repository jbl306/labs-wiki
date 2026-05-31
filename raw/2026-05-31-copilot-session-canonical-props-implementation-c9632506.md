---
title: "Copilot Session Checkpoint: Canonical Props Implementation"
type: text
captured: 2026-05-31T23:07:45.741410Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, nba-ml-engine, mempalace, graph, agents, dashboard]
checkpoint_class: project-progress
checkpoint_class_rule: "body:sprint 62"
retention_mode: compress
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Canonical Props Implementation
**Session ID:** `29085277-dd99-479d-9108-a1b945876488`
**Checkpoint file:** `/home/jbl/.copilot/session-state/29085277-dd99-479d-9108-a1b945876488/checkpoints/002-canonical-props-implementation.md`
**Checkpoint timestamp:** 2026-05-31T22:49:12.509375Z
**Exported:** 2026-05-31T23:07:45.741410Z
**Checkpoint class:** `project-progress` (rule: `body:sprint 62`)
**Retention mode:** `compress`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user asked to review `nba-ml-engine` DB accuracy, props accuracy, and dashboard accuracy, convert gaps into a next sprint, then implement all Sprint 62 P0/P1 items. The implementation strategy is to make immutable `prop_line_snapshots` and a shared canonical settled-prop population the source of truth, then rewire prop edges, calibration/model-health, materialized views, dashboard contracts, and validation around that canonical population. Work is mid-implementation and not yet tested.
</overview>

<history>
1. User asked: “review nba-ml-engine repo, db accuracy, props accuracy, dashboard accuracy. identify gaps and improvements and put in next sprint”
   - Loaded task/process/domain skills: `task-observer`, `sprint-orchestrator`, `data-quality`, `dashboard`, `backtest-lab`, `model-calibration`.
   - Queried MemPalace and repo context.
   - Dispatched parallel research agents for DB/data accuracy, props/model accuracy, and dashboard/BFF accuracy.
   - Ran read-only live Postgres checks via Docker because local app DB credentials failed.
   - Added **Sprint 62 - Accuracy Trust Hardening** to `nba-ml-engine/tasks/todo.md`.

2. User asked: “implement p0 and p1”
   - Created implementation plan at `/home/jbl/.copilot/session-state/29085277-dd99-479d-9108-a1b945876488/plan.md`.
   - Created session SQL todos:
     - `canonical-helper`
     - `snapshot-identity`
     - `prop-edge-gates`
     - `calibration-health`
     - `canonical-matviews`
     - `dashboard-contracts`
     - `validation-tests`
   - Began implementation with the shared canonical settled-prop helper, immutable snapshot identity, suspicious-line quarantine, prop edge gates, calibration rewiring, and matview rewiring.
   - Most recent work before compaction: editing backend SQL/materialized-view logic in `scripts/optimize_db.py`.

3. User then requested a detailed compaction summary.
   - Current response is the handoff summary for continuing the partially implemented Sprint 62 P0/P1 work.
</history>

<work_done>
Files modified:
- `/home/jbl/projects/nba-ml-engine/tasks/todo.md`
  - Added Sprint 62 backlog with audit baseline, P0/P1/P2 plans, and validation gates.
- `/home/jbl/.copilot/session-state/29085277-dd99-479d-9108-a1b945876488/plan.md`
  - Contains Sprint 62 P0/P1 implementation plan.
- `/home/jbl/projects/nba-ml-engine/config.py`
  - Added prop gate/line validation settings:
    - `PROP_EDGE_VIG_MARGIN`
    - `PROP_LINE_BOOK_GAP_TOLERANCE`
    - `PROP_KELLY_FRACTION`
    - `PROP_KELLY_MAX_FRACTION`
- `/home/jbl/projects/nba-ml-engine/src/evaluation/canonical_props.py`
  - New helper module.
  - Defines `CANONICAL_SETTLED_PROPS_CTE`, `canonical_settled_props_query`, `fetch_canonical_settled_props`, `fetch_canonical_population_count`, and `fetch_canonical_calibration_rows`.
  - Canonical identity selects one settled snapshot per `player_id/game_date/stat_name` from immutable `prop_line_snapshots`, with source priority and no mutable `prop_lines` join.
- `/home/jbl/projects/nba-ml-engine/src/evaluation/canonical_backtest.py`
  - Kelly defaults now use config constants.
  - Flat P&L now respects American odds profit instead of always `+1/-1`.
- `/home/jbl/projects/nba-ml-engine/src/data/prop_lines.py`
  - Added `_quarantine_suspicious_provider_lines`.
  - Added rejection for unsupported stats, nonpositive lines, missing side odds, non-player/non-standard markets, missing game context, and paired DK/FD line gaps.
  - Changed `_build_snapshot_upsert_statement` to `on_conflict_do_nothing` using point-in-time identity including `fetched_at`.
- `/home/jbl/projects/nba-ml-engine/src/db/models.py`
  - Removed old coarse `uq_prop_line_snapshot` unique constraint from `PropLineSnapshot`.
  - Existing point-in-time unique constraint remains the intended model identity.
- `/home/jbl/projects/nba-ml-engine/alembic/versions/cc62a1b0d531_make_prop_snapshots_point_in_time.py`
  - New migration to drop old `uq_prop_line_snapshot` and create `uq_prop_line_snapshots_point` on `player_id/game_date/source/stat_name/fetched_at`.
- `/home/jbl/projects/nba-ml-engine/src/applications/prop_finder.py`
  - Added suspicious paired-book line gap filtering.
  - Added American odds helpers, implied probability, decimal odds, EV calculation.
  - Added absolute edge threshold gate and vig/EV gate.
  - Added edge metadata: `model_probability`, `implied_probability`, `ev`, `vig_gate_passed`, `absolute_edge_threshold`, `edge_threshold`.
- `/home/jbl/projects/nba-ml-engine/src/api/server.py`
  - `PropEdge` model and edge conversion now expose new edge metadata.
  - Backtest endpoint now uses `fetch_canonical_settled_props`.
  - Calibration/model-health/fitting endpoints partially rewired to `fetch_canonical_calibration_rows`.
  - `/api/evaluation/prop-confidence` SQL partially rewired to `canonical_settled_props_query`.
- `/home/jbl/projects/nba-ml-engine/src/notifications/dispatcher.py`
  - Model-health style notification queries partially rewired to `canonical_settled_props_query`.
  - Added `timedelta` import.
- `/home/jbl/projects/nba-ml-engine/scripts/optimize_db.py`
  - Began rewiring `mv_daily_hit_rates`, `mv_backtest_summary`, and `mv_clv_daily` away from mutable `prop_lines`/`game_logs` joins and toward settled snapshots.
  - This file needs careful review for SQL syntax/column consistency before testing.

Current state:
- Implementation is incomplete and untested.
- No lint/test/build has been run after these edits.
- Session SQL todo `canonical-helper` was marked `in_progress`; other todo statuses should be queried before continuing.
</work_done>

<technical_details>
Live DB audit evidence from earlier review:
- `game_logs` latest: `2026-05-30`
- `predictions` latest: `2026-05-31`
- `prop_lines` and `prop_line_snapshots` latest: `2026-06-03`
- Latest joined prop+prediction slate: `2026-05-26`
- `prop_line_snapshots`: `24,421` rows and `24,421` coarse identities, meaning repeated captures were not preserving multi-point history under old identity.
- Last 30 days:
  - `6,080` settled snapshots
  - `2,238` canonical joined bets
  - `4,360` broad matview calls
- Calibration join fan-out: `3.80x`
- Latest model health: degraded, ECE `0.026`, hit rate `60.2%`, PTS alert `42.4%` over `92` seven-day predictions.
- Example suspicious latest slate line mismatches:
  - Victor Wembanyama REB `3.5` vs `12.5`
  - Josh Hart REB `2.5` vs `7.5`
  - Jalen Brunson AST `2.5` vs `6.5`
  - Josh Hart STL `0.5` vs `1.5`

Key implementation decisions:
- Canonical settled population must use immutable `prop_line_snapshots`, not mutable `prop_lines`.
- Snapshot identity should include `fetched_at`; old coarse uniqueness by `player_id/game_date/stat_name/source` destroys point-in-time history.
- Downstream calibration, model health, backtest-ish endpoints, matviews, and dashboard should consume the same canonical population to avoid fan-out and denominator drift.
- Suspicious provider lines should be filtered/quarantined at ingestion/scoring, not hidden by dashboard fallbacks.
- Prefer `NULL`/explicit metadata over invented defaults.
- Heavy aggregation belongs in materialized views or shared SQL helpers, not dashboard request-time ad hoc joins.
- No production DB mutation should occur unless explicitly applying a migration; live DB checks should remain read-only.

Environment/tool quirks:
- Local app `DATABASE_URL` failed auth for user `nba_ml` at `localhost:5432`.
- Live DB querying worked via Docker:
  - `docker exec -i nba-ml-db sh -lc 'psql ...'`
- Repo root for current work is `/home/jbl/projects/nba-ml-engine`.
- Top-level `/home/jbl/projects` is not a git repo.
- User memory: when committing/pushing, stage only task-authored files by explicit path, never `git add -A`.

Unresolved/needs verification:
- Confirm Alembic heads/branching: new migration uses `down_revision = "f4a1c7d9e2b0"`, but migration graph may have multiple heads.
- Confirm `PropLineSnapshot` model now matches DB constraints after migration.
- Confirm SQL in `scripts/optimize_db.py` compiles; edits were midstream.
- Confirm API endpoint rewires have correct row indexing and imports.
- Confirm `prop_finder` confidence-as-probability assumption is acceptable or refine probability source.
</technical_details>

<important_files>
- `/home/jbl/projects/nba-ml-engine/tasks/todo.md`
  - Sprint tracker.
  - Contains newly added **Sprint 62 - Accuracy Trust Hardening** section near top.
  - Update this with review/results after implementation and validation.

- `/home/jbl/.copilot/session-state/29085277-dd99-479d-9108-a1b945876488/plan.md`
  - Current implementation plan:
    - shared canonical settled-prop boundary
    - data contract
    - prop scoring
    - calibration/model-health
    - matviews/dashboard
    - validation.

- `/home/jbl/projects/nba-ml-engine/src/evaluation/canonical_props.py`
  - New central SQL helper.
  - Continue using this instead of duplicating settled-population SQL.
  - Important symbols: `CANONICAL_SETTLED_PROPS_CTE`, `canonical_settled_props_query`, fetch helpers.

- `/home/jbl/projects/nba-ml-engine/src/data/prop_lines.py`
  - Ingestion and snapshot upsert logic.
  - Changed snapshot upsert to point-in-time `do_nothing`.
  - Added suspicious-line quarantine logic.
  - Needs tests for snapshot immutability and quarantine behavior.

- `/home/jbl/projects/nba-ml-engine/src/db/models.py`
  - SQLAlchemy model for `PropLineSnapshot`.
  - Old coarse unique constraint removed.
  - Verify constraints against migration.

- `/home/jbl/projects/nba-ml-engine/alembic/versions/cc62a1b0d531_make_prop_snapshots_point_in_time.py`
  - New migration for snapshot identity.
  - Needs migration graph validation.

- `/home/jbl/projects/nba-ml-engine/src/applications/prop_finder.py`
  - Prop edge generation.
  - Added vig/EV/absolute edge/suspicious-line gates and metadata.
  - Needs focused tests.

- `/home/jbl/projects/nba-ml-engine/src/api/server.py`
  - FastAPI endpoints for prop edges, backtest, calibration, model health.
  - Partially rewired to canonical helper.
  - Needs syntax/type/test verification.

- `/home/jbl/projects/nba-ml-engine/src/notifications/dispatcher.py`
  - Model-health and notification checks.
  - Partially rewired to canonical helper.
  - Needs syntax/test verification.

- `/home/jbl/projects/nba-ml-engine/scripts/optimize_db.py`
  - Materialized views:
    - `mv_daily_hit_rates`
    - `mv_backtest_summary`
    - `mv_clv_daily`
    - likely still need `mv_dashboard_metrics` review.
  - Currently most likely to have incomplete/invalid SQL after mid-edit.

- `/home/jbl/projects/nba-ml-engine/dashboard-ui/server/src/index.ts`
  - Dashboard BFF.
  - Viewed but not yet meaningfully modified during this segment.
  - Still needs dashboard contract hardening: non-silent failures, freshness/CLV/edge unit metadata.

- `/home/jbl/projects/nba-ml-engine/dashboard-ui/server/src/dashboardContracts.ts`
  - Dashboard response contract definitions.
  - Viewed but not yet modified.
  - Likely needs fields for metadata/source/unit clarity.

- `/home/jbl/projects/nba-ml-engine/tests/test_prop_history.py`
  - Existing snapshot tests.
  - Add immutable snapshot identity regression here or a focused new test.

- `/home/jbl/projects/nba-ml-engine/tests/test_canonical_backtest.py`
  - Existing canonical backtest tests.
  - Update expected flat P&L/Kelly behavior if failures arise.

- `/home/jbl/projects/nba-ml-engine/tests/test_prop_lines_source_priority.py`
  - Relevant for provider/source selection and new quarantine behavior.

- `/home/jbl/projects/nba-ml-engine/tests/test_prop_lines_sportsgameodds.py`
  - Relevant ingestion tests for SGO/DK/FD lines.
</important_files>

<next_steps>
Continue Sprint 62 P0/P1 implementation:

1. Query session SQL todos:
   - `SELECT id, title, status, description FROM todos ORDER BY id;`
2. Review the current diff before editing further:
   - `rtk git --no-pager diff -- config.py src/evaluation/canonical_props.py src/data/prop_lines.py src/db/models.py src/applications/prop_finder.py src/api/server.py src/notifications/dispatcher.py scripts/optimize_db.py`
3. Finish/fix backend rewires:
   - Validate imports and row indexing in `src/api/server.py`.
   - Validate canonical SQL shape in `src/evaluation/canonical_props.py`.
   - Finish `scripts/optimize_db.py` canonical matview rewires, especially `mv_dashboard_metrics` and any CLV column-name compatibility.
   - Check `src/notifications/dispatcher.py` for repeated imports and SQL correctness.
4. Add/adjust tests:
   - Snapshot identity regression: same player/date/source/stat with different `fetched_at` should preserve distinct snapshots; same exact `fetched_at` should no-op.
   - Suspicious-line quarantine/gate tests.
   - Prop edge vig/EV/absolute threshold metadata tests.
   - Calibration/backtest canonical denominator tests if feasible.
5. Dashboard/BFF P1 work still pending:
   - Add edge unit/source metadata to contracts/responses.
   - Avoid silent success-shaped fallbacks where the API/dashboard should expose stale/missing data.
   - Clarify CLV as proxy/source-labeled if real closing-line data is not available.
6. Run validation:
   - Backend: focused pytest first, then broader relevant pytest.
   - Syntax: compile affected Python modules if pytest scope is slow.
   - Dashboard: run existing dashboard build/tests if package scripts exist.
   - Live DB read-only SQL gates via `docker exec -i nba-ml-db ... psql`, no mutation.
7. Update `tasks/todo.md` review/results section and session SQL todo statuses.
8. Store final durable findings in MemPalace and write a `copilot-cli` diary entry.
9. Only call `task_complete` after implementation is complete and verified.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
