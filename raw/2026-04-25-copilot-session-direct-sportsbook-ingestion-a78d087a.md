---
title: "Copilot Session Checkpoint: Direct Sportsbook Ingestion"
type: text
captured: 2026-04-25T17:32:10.672714Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, nba-ml-engine, mempalace, agents, dashboard]
checkpoint_class: durable-workflow
checkpoint_class_rule: "body:workflow"
retention_mode: retain
status: success
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Direct Sportsbook Ingestion
**Session ID:** `39cb6a8f-14d7-43a7-bad1-98ec00e06033`
**Checkpoint file:** `/home/jbl/.copilot/session-state/39cb6a8f-14d7-43a7-bad1-98ec00e06033/checkpoints/007-direct-sportsbook-ingestion.md`
**Checkpoint timestamp:** 2026-04-25T17:30:06.843676Z
**Exported:** 2026-04-25T17:32:10.672714Z
**Checkpoint class:** `durable-workflow` (rule: `body:workflow`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user wanted NBA ML prop-line ingestion hardened after a DraftKings/FanDuel line-accuracy investigation, with source priority implemented, direct sportsbook feeds added, game/milestone props captured separately, and historical DB rows updated safely without burning API quota. The approach was TDD-first: preserve `prop_lines` for model-ready standard player O/U rows, add generic sportsbook market tables for milestones/game props, rank sources (`DK_WEB`/`FD_WEB` > `DK`/`FD` > `SGO_*`), validate with tests, then commit/push/merge.
</overview>

<history>
1. Earlier context before this segment: the user asked to validate a Josh Hart steals mismatch and discover direct DK/FD sources.
   - A report found `SGO_DK stl=0.5 -226/+168` matched DK’s standard `Steals O/U`, while the user-observed `2+` was a separate DraftKings milestone ladder market.
   - FanDuel direct `sbapi` worked and showed Josh Hart standard steals O/U at `1.5 +178/-245`.
   - DraftKings old `/api/v5/eventgroups` endpoints were blocked by Akamai; FlareSolverr did not help.
   - Browser-backed DraftKings discovered working `sportscontent/controldata/standalone/leagueSubcategory/v1/markets` endpoints.
   - Created and pushed `reports/2026-04-25-direct-sportsbook-props-plan.md` on `feature/dashboard-accuracy-final`.

2. The user then asked: “implement source priority list from plan for ingestion. i want to expand to capture game props too, not just player props. then see if we can update historical data that we have in db but be careful with api rate limits. complete in a branch and merge when done.”
   - Loaded MemPalace/project context, repo plan, lessons, and relevant code.
   - Invoked workflow/data skills: `executing-plans`, `using-git-worktrees`, `test-driven-development`, `writing-plans`, `data-engineer`, `subagent-driven-development`, and later `finishing-a-development-branch`.
   - Created implementation branch `feature/direct-sportsbook-ingestion` from the existing clean worktree at `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final`.
   - Updated session plan at `/home/jbl/.copilot/session-state/39cb6a8f-14d7-43a7-bad1-98ec00e06033/plan.md` with the direct sportsbook ingestion plan and mirrored todos into SQL.

3. Implementation phase: source priority.
   - Added tests in `tests/test_prop_lines_source_priority.py`.
   - Implemented `_SOURCE_BOOKMAKER_MAP`, `_SOURCE_PRIORITY`, `_filter_current_prop_rows_by_source_priority`, `_delete_shadowed_current_prop_lines`, and `_normalize_prop_rows_for_insert` in `src/data/prop_lines.py`.
   - Behavior: `DK_WEB`/`FD_WEB` shadow lower-priority same-book rows for the same `player_id/game_date/stat_name`, while preserving separate books and unknown vendor rows.

4. Implementation phase: schema expansion.
   - Added ORM metadata columns to `PropLine` and `PropLineSnapshot`: `bookmaker`, `market_scope`, `market_class`, `provider_market_id`.
   - Added `SportsbookMarket` and `SportsbookMarketSnapshot` ORM models for generic non-model-ready markets.
   - Added Alembic migration `e2f6a8b4c901_add_sportsbook_market_tables.py`.
   - Tests in `tests/test_sportsbook_market_schema.py` passed.

5. Implementation phase: direct sportsbook adapters.
   - Added package `src/data/sportsbooks/` with `common.py`, `fanduel_web.py`, and `draftkings_web.py`.
   - Added parser tests in `tests/test_direct_sportsbook_adapters.py`.
   - FanDuel parser accepts standard MOVING_HANDICAP O/U markets like `Josh Hart - Steals`.
   - DraftKings parser accepts standard `Steals O/U` rows into `prop_lines` and captures milestone/game markets into generic sportsbook market rows.
   - Added game-scope parser coverage for DK game spread markets.
   - Default DK subcategories set to `4511,13508,16485` to include NBA main/game props, steals O/U, and steals milestones.

6. Implementation phase: wiring direct adapters into ingestion.
   - Added direct fetch wrapper `_fetch_direct_sportsbook_rows()` in `src/data/prop_lines.py`.
   - `fetch_prop_lines()` now:
     - settles snapshots,
     - fetches direct sportsbook rows first,
     - fetches Odds API rows,
     - fetches SportsGameOdds rows,
     - writes generic market rows/snapshots,
     - normalizes prop rows,
     - applies validation/floor/extreme/one-sided filters,
     - applies source-priority filtering,
     - deletes shadowed current rows,
     - upserts current prop rows and prop snapshots.
   - Provider failures log warnings and do not abort fallback providers.

7. Implementation phase: safe historical update.
   - Added `src/data/prop_market_backfill.py`.
   - Added CLI command `python main.py backfill-prop-market-metadata [--apply]`.
   - Default/dry-run performs local DB classification only; no external API calls.
   - Initial implementation loaded all rows with `.all()`; code review flagged this as memory-risk.
   - Fixed by using grouped counts and bulk updates per `source` instead of loading entire tables.
   - Tests in `tests/test_prop_market_backfill.py` passed.

8. Implementation phase: dashboard/API source priority.
   - Updated `scripts/optimize_db.py` `mv_prop_lines_primary` definition to:
     - filter `(market_scope = 'player' OR NULL)`,
     - filter `(market_class = 'standard_ou' OR NULL)`,
     - derive `source_bookmaker`,
     - rank source priority before closest-to-prediction,
     - select one row per `player_id/game_date/stat_name/bookmaker`.
   - Added Alembic migration `f4a1c7d9e2b0_rebuild_prop_lines_primary_priority.py`.
   - Updated unique index for `mv_prop_lines_primary` to `(player_id, game_date, stat_name, bookmaker)`.
   - Updated `src/applications/prop_finder.py` to filter standard player O/U rows and apply the same per-book source-priority selection for FastAPI prop edges.
   - Added tests in `tests/test_sprint52.py`.

9. Review and validation.
   - Ran focused baseline tests and then full suite.
   - Full suite initially failed:
     - `/health` returned 500 when DB unavailable because model-count query was uncaught. Fixed `src/api/server.py` to return `models_loaded=0` if DB count fails.
     - `test_ingest_game_logs_transforms_and_upserts` expected 2 rows but current code ingests Regular Season + Playoffs by default. Fixed test fixture to pass `season_types=["Regular Season"]`.
   - Full suite then passed: `427 passed, 9 skipped, 14 deselected, 1 warning`.
   - Code-review agent found:
     - High: unbounded `.all()` in backfill. Fixed with grouped bulk updates.
     - Medium: FanDuel state host injection risk and DK OData filter injection via env vars. Fixed config validation.
   - Added `tests/test_direct_sportsbook_config.py` for:
     - FD state whitelist.
     - DK numeric-only subcategory IDs.
   - Full suite passed again: `427 passed, 9 skipped, 14 deselected, 1 warning`.

10. Commit/push/merge status at compaction.
   - Committed implementation on `feature/direct-sportsbook-ingestion`:
     - Commit `3551914 feat: add direct sportsbook ingestion priority`
     - Includes required trailer: `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`
   - Pushed feature branch to origin:
     - `origin/feature/direct-sportsbook-ingestion`
   - Attempted to merge to `main`, but the main worktree `/home/jbl/projects/nba-ml-engine` was dirty:
     - `M .github/skills/nba-ml-pipeline/SKILL.md`
   - Because that file was unrelated/user-owned, merge to `main` had **not yet happened** when compaction was requested.
</history>

<work_done>
Files created:
- `alembic/versions/e2f6a8b4c901_add_sportsbook_market_tables.py`
  - Adds metadata columns to `prop_lines` and `prop_line_snapshots`.
  - Creates `sportsbook_markets` and `sportsbook_market_snapshots`.
- `alembic/versions/f4a1c7d9e2b0_rebuild_prop_lines_primary_priority.py`
  - Rebuilds `mv_prop_lines_primary` with market-class filtering and source priority.
- `src/data/prop_market_backfill.py`
  - DB-only metadata classifier/backfill for existing prop rows.
  - Uses grouped counts/bulk updates, not unbounded row loading.
- `src/data/sportsbooks/__init__.py`
- `src/data/sportsbooks/common.py`
- `src/data/sportsbooks/fanduel_web.py`
- `src/data/sportsbooks/draftkings_web.py`
  - Direct sportsbook adapter/parsing/fetching package.
- `tests/test_direct_sportsbook_adapters.py`
- `tests/test_direct_sportsbook_config.py`
- `tests/test_prop_lines_source_priority.py`
- `tests/test_prop_market_backfill.py`
- `tests/test_sportsbook_market_schema.py`

Files modified:
- `config.py`
  - Added direct sportsbook config:
    - `DIRECT_SPORTSBOOKS_ENABLED`
    - `DIRECT_SPORTSBOOK_STATES`
    - `DIRECT_SPORTSBOOK_REQUEST_DELAY`
    - `DIRECT_SPORTSBOOK_MAX_REQUESTS`
    - `FANDUEL_WEB_APP_KEY`
    - `DRAFTKINGS_SITE_CODE`
    - `DRAFTKINGS_PROP_SUBCATEGORIES`
    - `HISTORICAL_PROP_BACKFILL_MAX_REQUESTS`
  - Added `_parse_direct_sportsbook_states()` with FD state whitelist.
  - Added `_parse_draftkings_subcategories()` numeric-only validation.
- `main.py`
  - Added `backfill-prop-market-metadata` CLI command.
- `scripts/optimize_db.py`
  - Updated `mv_prop_lines_primary` SQL and unique index to use bookmaker/source priority.
- `src/api/server.py`
  - Hardened `/health` to return OK even if DB model-count query fails.
- `src/applications/prop_finder.py`
  - Filters to standard player O/U rows and applies source-priority grouping before edge generation.
- `src/data/prop_lines.py`
  - Added source priority helpers.
  - Added prop row normalization.
  - Added generic sportsbook market upsert helpers.
  - Added direct sportsbook row fetch wrapper.
  - Wired generic market storage and direct source rows into `fetch_prop_lines`.
- `src/db/models.py`
  - Added prop metadata columns and generic sportsbook market models.
- `tests/test_ingest_integration.py`
  - Made game-log ingest test explicit about `season_types=["Regular Season"]`.
- `tests/test_sprint52.py`
  - Added assertions for `mv_prop_lines_primary` market-class filters/source priority.

Current state:
- Branch: `feature/direct-sportsbook-ingestion`
- Commit: `3551914 feat: add direct sportsbook ingestion priority`
- Pushed: yes, to `origin/feature/direct-sportsbook-ingestion`
- Tests: full Python non-integration suite passed: `427 passed, 9 skipped, 14 deselected, 1 warning`
- Alembic heads: one head, `f4a1c7d9e2b0`
- Merge to `main`: pending because main worktree is dirty with unrelated `M .github/skills/nba-ml-pipeline/SKILL.md`.

SQL todo status before compaction:
- All implementation todos were marked done except `direct-ingest-validation`, which was still `in_progress` because merge to main/push main had not completed.
</work_done>

<technical_details>
- Source priority implemented:
  - `DK_WEB` and `FD_WEB`: rank `0`
  - `DK` and `FD`: rank `10`
  - `SGO_DK` and `SGO_FD`: rank `20`
  - unknown sources: rank `100`, isolated under synthetic bookmaker key `source:<source>`.
- Bookmaker mapping:
  - `DK_WEB`, `DK`, `SGO_DK` → `draftkings`
  - `FD_WEB`, `FD`, `SGO_FD` → `fanduel`
- `prop_lines` remains for model-ready standard player O/U rows only.
  - Milestones, ladders, game props, spreads, totals, moneylines, and other non-standard markets go to generic `sportsbook_markets`/`sportsbook_market_snapshots`.
- DraftKings standard O/U vs milestone distinction:
  - DK standard `Steals O/U`: subcategory `13508`; Josh Hart `0.5 -226/+168`.
  - DK `Steals Milestones`: subcategory `16485`; Josh Hart `2+ +198`.
  - DK main/game props subcategory included by default: `4511`.
- FanDuel direct API:
  - Uses `sbapi.{state}.sportsbook.fanduel.com`.
  - Default app key `_ak`: `FhMFpcPWXMeyZxOx`.
  - State codes are whitelisted in config to prevent hostname injection.
- DraftKings direct API:
  - Uses `sportsbook-nash.draftkings.com/sites/{DRAFTKINGS_SITE_CODE}/api/sportscontent/controldata/standalone/leagueSubcategory/v1/markets`.
  - `DRAFTKINGS_PROP_SUBCATEGORIES` must be numeric-only to avoid OData filter injection.
- Direct fetch request controls:
  - `DIRECT_SPORTSBOOK_MAX_REQUESTS` default `20`.
  - `DIRECT_SPORTSBOOK_REQUEST_DELAY` default `0.5`.
  - Direct sportsbook fetch failures log warnings and fallback providers still run.
- Historical data update:
  - `backfill-prop-market-metadata` is local DB-only.
  - Dry-run default: `python main.py backfill-prop-market-metadata`
  - Apply mode: `python main.py backfill-prop-market-metadata --apply`
  - It classifies existing prop rows/snapshots as `bookmaker`, `market_scope='player'`, `market_class='standard_ou'`.
  - It does **not** call external APIs, respecting rate-limit concerns.
- `prop_line_snapshots` semantics:
  - Current snapshot upsert still conflicts on `(player_id, game_date, stat_name, source)`, meaning it does not preserve every fetch timestamp as immutable line movement history for props. Generic sportsbook snapshots use `provider_source/external_market_id/selection_label/fetched_at`.
- Materialized view priority:
  - `mv_prop_lines_primary` now selects one row per bookmaker/player/date/stat and ranks source before closest-to-prediction.
  - Unique index changed to `(player_id, game_date, stat_name, bookmaker)`.
- FastAPI prop edges:
  - Previously read all `prop_lines`, bypassing materialized-view priority.
  - Now filters `market_scope`/`market_class` and applies `_prioritize_prop_query_results()`.
- Full suite warning:
  - One sklearn warning in `tests/test_sprint59.py::test_shap_values_linear_runs_on_ridge_wrapper`; not introduced by this work.
- Main worktree blocker:
  - `/home/jbl/projects/nba-ml-engine` is on `main` with unrelated dirty file `.github/skills/nba-ml-pipeline/SKILL.md`.
  - Do not overwrite/revert it without user permission.
</technical_details>

<important_files>
- `src/data/prop_lines.py`
  - Core prop ingestion.
  - New source priority helpers and direct adapter wiring.
  - Generic market upsert helpers.
  - Key sections:
    - source maps near top (`_SOURCE_BOOKMAKER_MAP`, `_SOURCE_PRIORITY`)
    - `_filter_current_prop_rows_by_source_priority`
    - `_delete_shadowed_current_prop_lines`
    - `_normalize_prop_rows_for_insert`
    - `_fetch_direct_sportsbook_rows`
    - `fetch_prop_lines()`
- `src/data/sportsbooks/draftkings_web.py`
  - Parses/fetches DK direct web markets.
  - Standard O/U rows become `DK_WEB` prop rows.
  - Milestones/game markets become generic sportsbook market rows.
  - Uses numeric validated subcategory IDs from config.
- `src/data/sportsbooks/fanduel_web.py`
  - Parses/fetches FD direct `sbapi` event-page markets.
  - Standard MOVING_HANDICAP player O/U rows become `FD_WEB` prop rows.
  - Uses whitelisted state hosts from config.
- `src/data/sportsbooks/common.py`
  - Shared coercion, stat parsing, name resolution, and game-context helpers.
- `src/db/models.py`
  - Added `PropLine`/`PropLineSnapshot` metadata columns.
  - Added `SportsbookMarket` and `SportsbookMarketSnapshot`.
- `alembic/versions/e2f6a8b4c901_add_sportsbook_market_tables.py`
  - Migration for metadata columns and generic sportsbook market tables.
- `alembic/versions/f4a1c7d9e2b0_rebuild_prop_lines_primary_priority.py`
  - Migration rebuilding `mv_prop_lines_primary` with standard O/U filtering/source priority.
- `scripts/optimize_db.py`
  - Runtime materialized-view definition for `mv_prop_lines_primary`.
  - Must stay aligned with Alembic migration SQL.
- `src/applications/prop_finder.py`
  - FastAPI prop-edge path now enforces standard-market filtering and source-priority selection.
- `src/data/prop_market_backfill.py`
  - Safe local DB-only historical metadata classifier.
- `main.py`
  - New CLI command `backfill-prop-market-metadata`.
- `config.py`
  - Direct sportsbook config and validation helpers.
- `tests/test_direct_sportsbook_adapters.py`
  - Parser tests for FD standard O/U, DK standard O/U, DK milestone, and DK game-scope market.
- `tests/test_direct_sportsbook_config.py`
  - Regression tests for FD state whitelist and DK numeric-only subcategory validation.
- `tests/test_prop_lines_source_priority.py`
  - Source-priority and shadowed-row cleanup tests.
- `tests/test_prop_market_backfill.py`
  - Dry-run/apply tests for local historical classification.
- `tests/test_sportsbook_market_schema.py`
  - ORM/table creation tests for new schema.
- `/home/jbl/.copilot/session-state/39cb6a8f-14d7-43a7-bad1-98ec00e06033/plan.md`
  - Updated implementation plan and current intended workflow.
</important_files>

<next_steps>
Pending work:
1. Complete merge to `main` and push `main`.
   - Feature branch is committed and pushed.
   - Main worktree is dirty with unrelated `.github/skills/nba-ml-pipeline/SKILL.md`.
   - Need to avoid overwriting that user/unrelated change.
   - Options:
     - Ask user what to do with the dirty file before merging.
     - Or merge from a clean worktree if safe, but remember `main` is already checked out in `/home/jbl/projects/nba-ml-engine`, so Git may block main updates in another worktree.
2. After successful merge/push, mark SQL todo `direct-ingest-validation` done.
3. Consider deleting the feature branch/worktree only after merge is complete and user does not need it.

Recommended immediate continuation:
- Inspect main dirty file:
  - `cd /home/jbl/projects/nba-ml-engine && git --no-pager diff -- .github/skills/nba-ml-pipeline/SKILL.md`
- Ask user whether to keep/stash/commit that unrelated change before merging, unless it is clearly safe to leave untouched and merge can proceed without conflict.
- If user approves stashing or commits it separately:
  - `cd /home/jbl/projects/nba-ml-engine`
  - `git fetch origin`
  - `git merge --ff-only feature/direct-sportsbook-ingestion` if possible, otherwise normal merge.
  - Run relevant tests on merged `main` if feasible.
  - `git push origin main`
- Save final durable findings to MemPalace after merge:
  - Direct ingestion architecture.
  - Source priority.
  - Generic market separation.
  - Backfill safety.
  - Commit SHA `3551914`.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
