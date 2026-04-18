---
title: "Copilot Session Checkpoint: Sprint 52 planning started"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, mempalace, agents, dashboard]
status: pending
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint 52 planning started
**Session ID:** `31d93251-dac7-4543-89a4-bd567847c867`
**Checkpoint file:** `/home/jbl/.copilot/session-state/31d93251-dac7-4543-89a4-bd567847c867/checkpoints/005-sprint-52-planning-started.md`
**Checkpoint timestamp:** 2026-04-12T18:11:11.265426Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user is executing Sprint 52 for the NBA ML Engine project, implementing next steps from Sprints 50 and 51. Sprint 52 covers 5 items: PTS model SHAP analysis, scale-aware edge metrics, rankings position filter + fallback query, mv_prop_lines_primary matview, and matview refresh timestamps on health endpoint. Earlier in this session, Sprint 51 (dashboard agent + 5 materialized views) was completed and merged as PR #35, then an MLflow crash was debugged and fixed (alembic version table collision). We're on the server (beelink-gti13), operating directly on the homelab.
</overview>

<history>
1. Earlier session work (already merged, from prior compaction summaries):
   - Sprint 50 merged as PR #32 (PTS edge threshold, SGO timezone, BFF alt-line fix)
   - PR #33: Sprint skill optimization (65% reduction)
   - PR #34: copilot-instructions.md optimization (MemPalace, 39% reduction)

2. Sprint 51: Dashboard agent + materialized views (completed this session)
   - Created `agents/dashboard.md`, updated `AGENTS.md`
   - Added 5 new matviews in `scripts/optimize_db.py` (mv_daily_hit_rates, mv_backtest_summary, mv_player_rankings, mv_clv_daily, mv_dashboard_metrics)
   - Added unique indexes for CONCURRENTLY support
   - Created alembic migration `a1b2c3d4e5f6`
   - Rewired BFF endpoints (backtest, rankings, dashboard trending/hit-rate/accuracy)
   - Rewired FastAPI endpoints (prop-hit-rate, CLV with fallback)
   - 26 new tests, 282 total passing
   - Deployed to homelab, verified matviews populated
   - Merged as PR #35

3. MLflow crash debugging and fix
   - MLflow was crash-looping: "Detected out-of-date database schema (found version a1b2c3d4e5f6, but expected 1b5f0d9ad7c1)"
   - Root cause: Our alembic migration wrote to the shared `alembic_version` table that MLflow also uses
   - Fix: Restored MLflow's version, added `version_table = nba_ml_alembic_version` to alembic.ini, created custom table stamped with our revision
   - Committed directly to main and pushed

4. User requested Sprint 52: implement next steps from Sprint 50 and 51
   - Invoked execute-sprint-from-report skill
   - User confirmed all 5 items for Sprint 52
   - Created branch `feature/sprint-52-pts-edge-matview`
   - Ran data quality gate: 126 timezone mismatches (known historical SGO issue, not blocking), 0 zero prop lines, freshness OK
   - Launched background explore agent to audit codebase for all 5 work areas
   - Started examining config.py edge thresholds, SHAP usage, DISTINCT ON patterns
   - Compaction occurred during planning phase
</history>

<work_done>
Files created/modified this session (already merged to main):
- `agents/dashboard.md`: New dashboard agent
- `AGENTS.md`: Added dashboard agent to routing, ownership, quality gates
- `scripts/optimize_db.py`: 5 new matview definitions, MV_UNIQUE_INDEXES, CONCURRENTLY refresh
- `alembic/versions/a1b2c3d4e5f6_add_dashboard_matviews.py`: Migration for 5 matviews
- `dashboard-ui/server/src/index.ts`: BFF endpoints rewired to matviews (backtest, rankings, dashboard)
- `src/api/server.py`: FastAPI prop-hit-rate and CLV rewired to matviews with fallback + db.rollback()
- `tests/test_sprint51.py`: 26 tests
- `docs/reports/sprint51-results.md`: Sprint report
- `tasks/lessons.md`: 3 new lessons (matview rollback, docker env, alembic collision)
- `alembic.ini`: Added `version_table = nba_ml_alembic_version`

Current git state:
- On branch `feature/sprint-52-pts-edge-matview` (just created, no commits yet)
- Main is at `48a891a` (includes alembic.ini fix)
- All containers running: nba-ml-api, nba-ml-dashboard, nba-ml-db (healthy), nba-ml-scheduler, nba-ml-mlflow
- 282 tests passing

Sprint 52 SQL todos not yet created (was in planning phase).
</work_done>

<technical_details>
**Matview Architecture (8 total):**
- 3 original: mv_season_summary, mv_player_leaderboard, mv_injury_latest
- 5 new (Sprint 51): mv_daily_hit_rates (105 rows), mv_backtest_summary (31), mv_player_rankings (405), mv_clv_daily (72), mv_dashboard_metrics (12)
- All have unique indexes for REFRESH MATERIALIZED VIEW CONCURRENTLY
- Pipeline refreshes in main.py Step 7 after QA — no new cron needed
- refresh_materialized_views() tries CONCURRENTLY first, falls back to blocking (first populate)

**Critical: Alembic Version Table**
- `alembic.ini` now uses `version_table = nba_ml_alembic_version` (custom table)
- MLflow owns the default `alembic_version` table (current version: `1b5f0d9ad7c1`)
- NEVER touch `alembic_version` directly — it belongs to MLflow
- Our custom table `nba_ml_alembic_version` has revision `a1b2c3d4e5f6`

**Matview fallback pattern:**
- When matview query fails in FastAPI, MUST call `db.rollback()` before fallback ORM queries
- SQLAlchemy session stays in InFailedSqlTransaction state otherwise

**Deployment:**
- Server mode: hostname `beelink-gti13`, operate directly
- MUST source homelab .env before docker compose: `cd ~/projects/homelab && set -a && source .env && set +a`
- Alembic migrations: docker cp into nba-ml-api container, then run via Python
- NBA_ML_ENGINE_PATH must be absolute: `/home/jbl/projects/nba-ml-engine`

**Edge Configuration (current state for Sprint 52):**
- MIN_EDGE_THRESHOLD = 0.005 (0.5%)
- STAT_EDGE_THRESHOLDS in config.py:198-208 — percentage-based per stat
- Edge is computed as `(pred - line) / line` (percentage-based)
- Sprint 50 finding: PTS needs 0.5% edge (was too restrictive at higher values)
- USE_OPTIMIZED_THRESHOLDS = true, OPTIMIZED_EDGE_THRESHOLDS populated at runtime

**SHAP:**
- Already in feature_selector.py: `_get_shap_importances()` uses TreeExplainer
- Falls back to GBT importance if SHAP unavailable
- Subsamples for speed

**DISTINCT ON patterns in BFF (3 locations):**
- Line ~398: overview/props query
- Line ~668: settlement/hit-rate query 
- Line ~1632: rankings confidence props query
- All use pattern: DISTINCT ON (player_id, stat_name, source) with ABS(predicted - line) ASC tiebreaker

**Rankings matview:**
- mv_player_rankings includes position column (from players table)
- Currently BFF reads from matview with no position filter
- Days param hardcoded to 30 in matview — needs fallback for non-default

**Data quality:**
- 126 historical SGO timezone mismatches (known, not blocking)
- 0 zero prop lines
- Off-season: minimal fresh prop data
</technical_details>

<important_files>
- `config.py`
   - Edge thresholds (STAT_EDGE_THRESHOLDS line 198-208), MIN_EDGE_THRESHOLD (line 190)
   - Sprint 52 will add scale-aware absolute-point edge metric here
   - Also has STAT_LINE_FLOORS, EXCLUDED_PROP_STATS

- `src/training/feature_selector.py`
   - SHAP-based feature importance (_get_shap_importances line 29)
   - Sprint 52 PTS SHAP analysis will use/extend this

- `src/inference/predictor.py`
   - Edge computation logic — currently percentage-based
   - Sprint 52 scale-aware edge metric changes here

- `scripts/optimize_db.py`
   - All matview definitions (MATERIALIZED_VIEWS dict line 32+)
   - MV_UNIQUE_INDEXES (line 273), MV_INDEXES (line 284)
   - create/refresh functions (lines 307, 332)
   - Sprint 52 adds mv_prop_lines_primary matview

- `dashboard-ui/server/src/index.ts`
   - BFF layer (~2000+ lines), 26+ endpoints
   - Rankings endpoint (line ~1545) — needs position filter + days fallback
   - DISTINCT ON patterns at lines ~398, ~668, ~1632 — candidates for mv_prop_lines_primary
   - Already uses mv_backtest_summary, mv_player_rankings, mv_dashboard_metrics, mv_daily_hit_rates

- `src/api/server.py`
   - FastAPI endpoints, health endpoint
   - Sprint 52 adds matview refresh timestamp to /health
   - prop-hit-rate (line ~591) and CLV (line ~742) already use matviews

- `alembic.ini`
   - Uses `version_table = nba_ml_alembic_version` (CRITICAL: don't use default)

- `src/features/builder.py`
   - Feature engineering — Sprint 52 may add PTS-specific features

- `AGENTS.md`
   - Agent routing table, file ownership, quality gates
   - 7 agents: nba-ml-pipeline, model-calibration, feature-lab, data-quality, backtest-lab, sprint-orchestrator, dashboard
</important_files>

<next_steps>
**Sprint 52 — 5 items to implement:**

1. **PTS Model SHAP Analysis** (feature-lab agent domain)
   - Run SHAP on PTS predictions, identify top features driving 7.46 MAE
   - Consider PTS-specific feature engineering (pace, scoring streaks, rest days)
   - May need to add a SHAP analysis script or extend existing feature_selector.py

2. **Scale-Aware Edge Metric** (model-calibration agent domain)
   - Current edge is percentage: `(pred - line) / line`
   - For PTS (line ~25), 1% edge = 0.25 points — too noisy
   - Implement absolute-point edge option with per-stat thresholds
   - E.g., PTS needs ≥0.5pt edge, AST needs ≥0.3pt
   - Changes in: config.py, src/inference/predictor.py, possibly BFF edge filter

3. **Rankings Position Filter + Non-30-Day Fallback** (dashboard agent domain)
   - mv_player_rankings has position column — add WHERE clause in BFF
   - For `?days=` values other than 30, fall back to original aggregation query
   - Changes in: dashboard-ui/server/src/index.ts

4. **mv_prop_lines_primary Matview** (dashboard agent domain)
   - New matview for DISTINCT ON (player_id, game_date, stat_name) dedup
   - Replace 3 BFF DISTINCT ON patterns (lines ~398, ~668, ~1632)
   - Add to scripts/optimize_db.py, create alembic migration
   - Add unique index for CONCURRENTLY

5. **Matview Refresh Timestamp on Health** (nba-ml-pipeline agent domain)
   - Track when each matview was last refreshed
   - Add to /health endpoint response in src/api/server.py
   - Could use pg_stat_user_tables.last_analyze or a custom tracking table

**Immediate actions when resuming:**
- A background explore agent (`audit-sprint52`) was running — check if complete and read results
- Create SQL todos for the 5 items
- Create progress tracker at `tasks/PROGRESS-sprint52-pts-edge-matview-0412.md`
- Plan implementation order (items 3-5 are independent and parallelizable; items 1-2 are sequential)
- Write failing tests first for each item
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
