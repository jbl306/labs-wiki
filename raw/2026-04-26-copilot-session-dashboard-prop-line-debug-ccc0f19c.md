---
title: "Copilot Session Checkpoint: Dashboard Prop Line Debug"
type: text
captured: 2026-04-26T00:50:19.293694Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, mempalace, dashboard]
checkpoint_class: durable-debugging
checkpoint_class_rule: "body:root-cause"
retention_mode: retain
status: success
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Dashboard Prop Line Debug
**Session ID:** `39cb6a8f-14d7-43a7-bad1-98ec00e06033`
**Checkpoint file:** `/home/jbl/.copilot/session-state/39cb6a8f-14d7-43a7-bad1-98ec00e06033/checkpoints/010-dashboard-prop-line-debug.md`
**Checkpoint timestamp:** 2026-04-26T00:42:30.447262Z
**Exported:** 2026-04-26T00:50:19.293694Z
**Checkpoint class:** `durable-debugging` (rule: `body:root-cause`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user’s larger goal was to improve NBA ML dashboard/model accuracy, implement all audit recommendations, deploy them, and then investigate why Josh Hart’s steals prop still shows a suspicious `SGO_DK 0.5` line despite direct-source ingestion priority. The implementation/deployment sprint is complete and pushed to `main`; the current active thread is a root-cause investigation of live Josh Hart prop-line source selection across dashboard, FastAPI, DB, and direct sportsbook ingestion.
</overview>

<history>
1. The user first asked to evaluate `nba-dashboard.jbl-lab.com`, identify dashboard/model accuracy issues, write reports, implement fixes, validate, deploy, and later finish all recommendations from the audit report.
   - Created and pushed `reports/2026-04-25-dashboard-model-training-audit.md` on `main`.
   - Worked on branch/worktree `feature/audit-recommendations` at `/home/jbl/projects/nba-ml-engine/.worktrees/audit-recommendations`.
   - Implemented audit recommendations in slices with review gates:
     - Dashboard/API population correctness.
     - Confidence provenance contract.
     - Production/research training split metadata.
     - Feature-leakage fixes.
     - Predicted-minutes and ensemble contract hardening.
     - Drift threshold alignment.
   - Wrote final report `reports/2026-04-25-audit-recommendations-implementation-status.md`.
   - Merged branch to `main`, pushed, deployed homelab `nba-ml` stack, applied pending Alembic migrations, refreshed materialized views, and cleaned all non-main branches.

2. During deployment, materialized-view refresh initially failed.
   - `scripts/optimize_db.py` attempted to create `mv_prop_lines_primary`, but the live DB lacked `prop_lines.bookmaker`.
   - Root cause: pending Alembic migrations had not been applied.
   - `alembic` inside `nba-ml-api` initially failed with `ModuleNotFoundError: No module named 'config'` unless run with `PYTHONPATH=/app`.
   - Applied migrations through `f4a1c7d9e2b0`.
   - Recreated/refreshed `mv_daily_hit_rates`, `mv_backtest_summary`, and then refreshed all materialized views cleanly.
   - Verified local and LAN endpoints.

3. The user corrected the earlier validation framing: “add a lesson that its reachable on lan with http. then continue validating.”
   - Added lesson to `tasks/lessons.md`:
     - Public HTTPS, LAN HTTP, and local/container health are separate validation layers.
     - If LAN HTTP works, public HTTPS failure should be treated as routing/edge until proven otherwise.
   - Updated session `plan.md`.
   - Validated:
     - `http://192.168.1.238:8000/health` OK.
     - `http://192.168.1.238:8501` HTTP 200.
     - `http://192.168.1.238:8501/api/backtest?days=30` OK.
     - Authenticated LAN FastAPI checks to `/models`, `/prop-hit-rate`, and `/evaluation/backtest/canonical?days=30` OK with `X-API-Key`.
   - Committed and pushed lesson as `880a66c docs: add LAN HTTP validation lesson`.

4. The user then asked why Josh Hart’s steals prop line still points at `0.5`, `SGO_DK` on the props dashboard if direct-source ingestion is prioritized.
   - Loaded systematic debugging.
   - Queried MemPalace and prior session context.
   - Important recalled prior findings:
     - FanDuel direct API had Josh Hart steals standard O/U at `1.5`.
     - DraftKings direct investigation found:
       - DK standard `Steals O/U` had Josh Hart at `0.5 -226/+168`.
       - DK `Steals Milestones` had Josh Hart `2+ +198`.
       - User visually saw DraftKings UI “2+” and considered dashboard `0.5` inaccurate.
     - SportsGameOdds raw payload had SGO_DK `0.5` for Josh Hart steals and SGO_FD `1.5`; SGO_DK looked contaminated/cross-market in an earlier report.
   - Began tracing live data:
     - Found Josh Hart player id `1879`.
     - Live dashboard `/api/props` returned two Josh Hart `stl` rows:
       - `SGO_DK`, line `0.5`, predicted `1.34`, call `Over`, confidence source `ci_platt+classifier_blend+posthoc_isotonic`.
       - `SGO_FD`, line `1.5`, predicted `1.34`, call `Under`, same confidence source.
     - Live FastAPI `/prop-edges?min_edge=0&limit=1000` also returned two Josh Hart rows:
       - `SGO_DK`, line `0.5`, over odds `-226`, under odds `168`.
       - `SGO_FD`, line `1.5`, over odds `178`, under odds `-245`.
     - First DB query failed because it selected nonexistent `created_at`/`updated_at` from `prop_lines`; need rerun without those columns.
   - Current investigation was interrupted before final root cause answer/fix.
</history>

<work_done>
Completed code/report/deploy work:
- Implemented and pushed audit recommendation branch to `main`.
- Current `main` is at `880a66c`.
- Final audit implementation report:
  - `reports/2026-04-25-audit-recommendations-implementation-status.md`
- Added LAN HTTP validation lesson:
  - `tasks/lessons.md`
  - Commit: `880a66c docs: add LAN HTTP validation lesson`
- Deployment completed:
  - `nba-ml-api`, `nba-ml-dashboard`, `nba-ml-db`, `nba-ml-mlflow`, `nba-ml-scheduler` running.
  - Alembic current/head applied through `f4a1c7d9e2b0`.
  - Materialized views refreshed successfully.
- Branch cleanup completed:
  - Only local branch `main`.
  - Only remote branches `origin/main`, `origin/HEAD -> origin/main`.
- Remaining dirty file:
  - `.github/skills/nba-ml-pipeline/SKILL.md`
  - Pre-existing unrelated change; do not touch/revert unless user asks.

Validation completed:
- Python suite on merged main: `469 passed, 9 skipped, 2 warnings`.
- Dashboard contract tests: `19 passed`.
- Dashboard build: passed with existing chunk warning.
- Local API health OK.
- Public dashboard `https://nba-dashboard.jbl-lab.com`: HTTP 200.
- Public API HTTPS `https://nba-ml.jbl-lab.com/health`: not reachable from this environment.
- LAN HTTP works:
  - `http://192.168.1.238:8000/health`: OK.
  - `http://192.168.1.238:8501`: HTTP 200.
  - Dashboard BFF and authenticated FastAPI routes return data.

Current active work:
- Debugging Josh Hart steals line still showing `SGO_DK 0.5`.
- Live dashboard/API confirmed it still appears.
- Need complete DB/source trace and then propose or implement fix.
</work_done>

<technical_details>
Audit implementation decisions:
- `/prop-hit-rate` now uses canonical settled `prop_line_snapshots + predictions`, with population metadata.
- Broad diagnostics are separated/labeled and should not pretend all-time broad rows are windowed settled data.
- `confidence_source` is exposed through FastAPI/BFF/frontend contracts; heuristic confidence tiers are capped below `High`.
- `TRAINING_MODE=production|research`:
  - Production: rolling chronological validation.
  - Research: fixed historical split.
- Registry snapshots now include training/validation/test windows, but existing production models show `null` until next retrain.
- Feature leakage fixes:
  - `_load_game_logs()` joins `Player.team`.
  - Season-level advanced/team/hustle/BBRef features use prior-season mapping.
  - Advanced same-season fallback removed.
- Predicted minutes:
  - `build_features(..., predicted_minutes_mode='inference'|'training'|'disabled')`.
  - Minutes model training uses disabled mode.
  - Stat training uses historical player-minutes prior.
  - Inference uses production minutes model with explicit fallback metadata.
- Ensemble:
  - Default serving/training metrics contract is performance-weighted average.
  - Legacy ridge mode preserved.
  - Date-aware folds use `X_train.attrs["game_dates"]`.
  - Warmup rows without OOF predictions are excluded from ensemble meta-training/metrics.
- Drift threshold:
  - `DRIFT_PSI_EXCLUSION_THRESHOLD` default aligned to `0.25`.

Deployment quirks:
- Run Alembic inside container with:
  - `docker exec -w /app -e PYTHONPATH=/app nba-ml-api alembic ...`
- `prop_lines.bookmaker`, `market_scope`, `market_class`, `provider_market_id` were added by migration `e2f6a8b4c901`.
- `mv_prop_lines_primary` was rebuilt by migration `f4a1c7d9e2b0`.
- `scripts/optimize_db.py` `CREATE MATERIALIZED VIEW IF NOT EXISTS` will not alter existing materialized view definitions; if view DDL changes, drop/recreate changed views or use migration.
- Direct FastAPI endpoints require `X-API-Key`, while dashboard BFF routes work unauthenticated because the dashboard talks to API internally.

Direct sportsbook / Josh Hart context:
- Source priority:
  - `DK_WEB`, `FD_WEB`: rank `0`.
  - `DK`, `FD`: rank `10`.
  - `SGO_DK`, `SGO_FD`: rank `20`.
  - Unknown: rank `100`.
- Bookmaker grouping:
  - `DK_WEB`, `DK`, `SGO_DK` → `draftkings`.
  - `FD_WEB`, `FD`, `SGO_FD` → `fanduel`.
- `mv_prop_lines_primary` selects one row per `(player_id, game_date, stat_name, source_bookmaker)`, ordered by source rank then closeness to prediction.
- Dashboard BFF `/api/props` reads from `mv_prop_lines_primary` in `dashboard-ui/server/src/index.ts`.
- FastAPI prop edge path uses source-priority helper in `src/applications/prop_finder.py`.
- Important distinction:
  - DK standard `Steals O/U` appears to be `0.5`.
  - DK milestone “2+” is a different market and should be captured in generic `sportsbook_markets`, not `prop_lines`.
  - User expects dashboard props page not to show the misleading `SGO_DK 0.5` row if direct source priority exists.
- Possible root causes still to confirm:
  1. Direct DK/FD ingestion did not run after deploy, so only SGO rows exist in `prop_lines`.
  2. Direct DK/FD fetch failed due Akamai/endpoint/config, so SGO fallback remained.
  3. DK direct may classify the standard O/U as `DK_WEB 0.5`; if absent, dashboard shows `SGO_DK 0.5`.
  4. FanDuel direct `FD_WEB 1.5` may be missing from live `prop_lines`, so source priority cannot shadow `SGO_FD`.
  5. Even if SGO_DK `0.5` is technically DraftKings standard O/U, the dashboard may need UX/market-class changes to distinguish standard O/U vs milestone “2+” and/or suppress SGO rows when direct book data is missing/untrusted.

Recent failed DB query:
- Query selected `created_at` and `updated_at` from `prop_lines`; live table does not have these columns.
- Rerun DB query without those columns.
</technical_details>

<important_files>
- `src/data/prop_lines.py`
  - Core prop ingestion and source-priority helpers.
  - Key sections:
    - `_SOURCE_BOOKMAKER_MAP`, `_SOURCE_PRIORITY` around lines ~65-86.
    - `_bookmaker_for_source`, `_source_priority_rank`, `_filter_current_prop_rows_by_source_priority`, `_delete_shadowed_current_prop_lines` around lines ~209-260.
    - Direct sportsbook fetch/integration near later sections; need inspect around `_fetch_direct_sportsbook_rows`, `fetch_prop_lines`.
  - Determines whether `DK_WEB`/`FD_WEB` rows shadow `SGO_*`.

- `src/data/sportsbooks/fanduel_web.py`
  - FanDuel direct adapter.
  - Prior research confirmed FD standard O/U Josh Hart steals at `1.5`.
  - Need check whether live fetch ran and inserted `FD_WEB`.

- `src/data/sportsbooks/draftkings_web.py`
  - DraftKings direct adapter.
  - Prior research showed DK standard steals O/U `0.5` and separate milestone `2+`.
  - Need check if live fetch works/configured and whether it inserts `DK_WEB`.

- `src/applications/prop_finder.py`
  - FastAPI prop-edge logic.
  - Imports `_bookmaker_for_source`, `_source_priority_rank`.
  - Has priority selection; live FastAPI still returns SGO_DK/SGO_FD because direct rows likely absent or not used.

- `dashboard-ui/server/src/index.ts`
  - BFF `/api/props` reads `mv_prop_lines_primary`.
  - Query around lines ~435-485 selects from `mv_prop_lines_primary`.
  - Current live dashboard shows Josh Hart `SGO_DK 0.5` and `SGO_FD 1.5`.

- `scripts/optimize_db.py`
  - Materialized-view definitions.
  - `mv_prop_lines_primary` source-priority DDL around lines ~320-368.
  - Requires existing `prop_lines.bookmaker` etc. after migrations.

- `alembic/versions/e2f6a8b4c901_add_sportsbook_market_tables.py`
  - Adds `bookmaker`, `market_scope`, `market_class`, `provider_market_id` to `prop_lines` and `prop_line_snapshots`.
  - Adds generic sportsbook market tables.

- `alembic/versions/f4a1c7d9e2b0_rebuild_prop_lines_primary_priority.py`
  - Rebuilds `mv_prop_lines_primary` with source priority and `(player_id, game_date, stat_name, bookmaker)` unique index.

- `tests/test_prop_lines_source_priority.py`
  - Tests source-priority filtering and shadowed-row cleanup.
  - Contains examples where `DK_WEB` shadows `SGO_DK`.

- `tests/test_direct_sportsbook_adapters.py`
  - Parser tests for FD/DK direct standard/milestone/game markets.

- `reports/2026-04-25-prop-line-integrity-audit.md`
  - Earlier report documenting Josh Hart line issue and raw SGO contamination.
  - Important for explaining the original problem.

- `reports/2026-04-25-direct-sportsbook-props-plan.md`
  - Direct sportsbook plan, including FD/DK discovery and source priority.

- `tasks/lessons.md`
  - Newly added LAN HTTP validation lesson at top.
  - Also includes old lessons about deployment/builds/Alembic.

- `/home/jbl/.copilot/session-state/39cb6a8f-14d7-43a7-bad1-98ec00e06033/plan.md`
  - Updated to note completion, deployment, and LAN HTTP validation.
</important_files>

<next_steps>
Immediate next steps for Josh Hart investigation:
1. Rerun live DB query without nonexistent `created_at`/`updated_at` columns:
   - `prop_lines` for player_id `1879`, stat `stl`, game_date current/today.
   - `mv_prop_lines_primary`.
   - `prop_line_snapshots`.
   - `sportsbook_markets` / snapshots for Josh Hart steals and milestone markets.
2. Check ingestion config in live container:
   - `DIRECT_SPORTSBOOK_ENABLED` or equivalent flags.
   - `PROP_SOURCES`.
   - `DRAFTKINGS_*` and `FANDUEL_*` env/config.
   - direct max requests/delay.
3. Check recent `nba-ml-api` logs around prop ingest:
   - Look for `DK_WEB`, `FD_WEB`, direct fetch warnings, Akamai/403, FD event discovery, SGO fallback.
4. Run a bounded dry/smoke direct sportsbook fetch if safe:
   - Avoid broad/rate-heavy ingestion.
   - Prefer using existing adapter functions with current date/Josh Hart/Knicks-Hawks if possible.
   - Confirm whether FD direct can currently produce Josh Hart `FD_WEB 1.5`.
   - Confirm whether DK direct currently produces `DK_WEB 0.5` standard O/U and a generic milestone `2+`.
5. Determine root cause:
   - If no direct rows exist: likely direct ingestion didn’t run or failed; fix scheduler/command/config or trigger props ingest.
   - If direct rows exist but dashboard still shows SGO: fix source priority/materialized view/FastAPI query.
   - If DK direct standard is `0.5`: explain that dashboard is showing standard O/U market; user-visible “2+” is milestone market. Then decide whether props page should prefer milestone/current UI lines or show market type labels.
   - If SGO rows are stale or contaminated: quarantine/suppress SGO_DK for suspicious inconsistent line data when direct book data is absent or when SGO market metadata indicates yes/no contamination.
6. After root cause, implement fix with TDD if code change is needed, validate, deploy, and update report/lesson if warranted.

Useful commands:
- Authenticated LAN FastAPI:
  - `set -a && source /home/jbl/projects/homelab/.env && set +a`
  - `curl -H "X-API-Key: $NBA_ML_API_KEY" http://192.168.1.238:8000/...`
- Alembic in container:
  - `docker exec -w /app -e PYTHONPATH=/app nba-ml-api alembic current`
- DB query in container:
  - `docker exec -i -w /app nba-ml-api python - <<'PY' ... PY`
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
