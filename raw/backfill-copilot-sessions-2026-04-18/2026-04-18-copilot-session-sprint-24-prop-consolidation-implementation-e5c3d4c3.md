---
title: "Copilot Session Checkpoint: Sprint 24 prop consolidation implementation"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, agents, dashboard]
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint 24 prop consolidation implementation
**Session ID:** `c1de5ddc-0296-4d1b-ab46-50fab29eb8f1`
**Checkpoint file:** `/home/jbl/.copilot/session-state/c1de5ddc-0296-4d1b-ab46-50fab29eb8f1/checkpoints/006-sprint-24-prop-consolidation-i.md`
**Checkpoint timestamp:** 2026-03-26T21:31:23.021492Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user invoked the `execute-sprint-from-report` skill to implement Sprint 24 based on Sprint 23's immediate and high-priority next steps: (1) fix SGO_FD stat misclassification, (2) consolidate BFF prop query path to use FastAPI, (3) add holdout-based model selection, and (4) add prop hit-rate tracking. We're on branch `feature/sprint-24-prop-consolidation-and-hit-rates` on the homelab server (beelink-gti13) in server mode. Sprint 23 (PR #25) was completed and merged earlier this session.
</overview>

<history>
1. Earlier session work completed Sprint 22 (post-retrain optimization, PR #24) and Sprint 23 (props dashboard fixes — confidence formula, edge cap, stat filtering, PR #25).

2. User invoked `/execute-sprint-from-report` to implement Sprint 23's immediate and high-priority next steps as Sprint 24:
   - Read AGENTS.md (not found), tasks/lessons.md, Sprint 23 report
   - Confirmed server mode (hostname beelink-gti13), clean main branch
   - Created branch `feature/sprint-24-prop-consolidation-and-hit-rates`
   - Set up SQL todos with 7 tasks and dependencies

3. **SGO_FD stat misclassification investigation and fix** (DONE):
   - Queried DB: SGO sources have ZERO fg3m entries but pts avg_line=9.5 (vs DK/FD pts avg=14.3)
   - Root cause: `_normalize_sportsgameodds_stat_id()` strips case but doesn't insert word boundaries — `threePointers` → `threepointers` (not in map) → skipped entirely
   - Players like Cameron Johnson showing pts line=2.5 are clearly three-pointer lines from the SGO API sending `statID="points"` for what should be fg3m
   - Fixed: Added 13 new stat ID mappings to `_SPORTSGAMEODDS_STAT_MAP` covering camelCase variants, numeric prefixes, and other API formats
   - Added diagnostic logging for unmapped stat IDs via `_sgo_unmapped_stats` set
   - Added 2 new tests: `test_camelcase_three_pointer_stat_ids_map_to_fg3m` and `test_extract_sportsgameodds_three_pointers_camelcase`

4. **Holdout-based model selection** (DONE):
   - Added `MODEL_SELECTION_METRIC` config option in config.py (default "val_mse", alternative "test_mse")
   - Modified `_register_best_model()` in trainer.py to use configurable metric key
   - Falls back to val_mse if test_mse unavailable, preserves degradation guardrail

5. **Consolidate BFF prop query path** (DONE but hit deployment issue):
   - Extended `PropEdge` pydantic model in server.py with 10 new fields (team, CI bounds, odds, opponent, is_home, game_date, game_time)
   - Updated `find_edges()` in prop_finder.py to return all new fields (team from Player query, opponent/is_home/game_time from PropLine)
   - Replaced BFF `/api/props` direct Postgres query with `fetch()` to FastAPI `/prop-edges`
   - Removed unused BFF constants (`VALID_PROP_STATS`, `MIN_LINE_SQL`)
   - Added NaN-safe int conversion (`_safe_int`) for odds fields in server.py

6. **Prop hit-rate tracking endpoint** (DONE):
   - Added `PropHitRateStat` and `PropHitRateResponse` pydantic models
   - Added `GET /prop-hit-rate?days=30` endpoint that settles outstanding snapshots, computes per-stat model-direction hit rates by joining PropLineSnapshot with Prediction
   - Added BFF proxy route `GET /api/prop-hit-rate`

7. **Testing** (PASSED):
   - 165/165 Python tests pass (was 163, +2 new SGO tests)
   - TypeScript compiles clean

8. **Deployment** (IN PROGRESS — hit issues):
   - Built nba-ml-api and nba-ml-dashboard containers successfully
   - Deployed both containers
   - API health check: OK
   - Props API returned EMPTY — first error was Pydantic `ValidationError` for `under_odds` receiving NaN (fixed with `_safe_int`)
   - **Then discovered performance issue**: FastAPI `/prop-edges` does live inference via `Predictor.predict_player()` which is very slow. The old BFF used stored predictions from the `predictions` table.
   - **Refactored `find_edges()`** to use stored predictions by default (blended via AVG like the old BFF CTE), falling back to live inference only when no stored predictions exist
   - **Was mid-edit** when compaction occurred — the `find_edges()` function header and stored-predictions logic has been written, but the rest of the function (the edges loop starting at `for prop_row, player_name, player_team in props:`) was already correct from the previous edit. Need to verify the full function is coherent and redeploy.
</history>

<work_done>
### Files modified:

- `src/data/prop_lines.py`: Added 13 camelCase/variant stat ID mappings to `_SPORTSGAMEODDS_STAT_MAP`, added `_sgo_unmapped_stats` diagnostic logging
- `tests/test_prop_lines_sportsgameodds.py`: Added 2 new tests for camelCase stat ID mapping
- `config.py`: Added `MODEL_SELECTION_METRIC` env-var config option (line ~158)
- `src/training/trainer.py`: Refactored `_register_best_model()` to use configurable metric key with fallback
- `src/applications/prop_finder.py`: Major refactor of `find_edges()` — uses stored predictions from DB by default (blended via AVG), added team/opponent/is_home/game_date/game_time to output, updated query to `session.query(PropLine, Player.name, Player.team)`
- `src/api/server.py`: Extended `PropEdge` with 10 new fields, added `_safe_int()` NaN handler, added `/prop-hit-rate` endpoint with `PropHitRateStat`/`PropHitRateResponse` models, added `timedelta` import
- `dashboard-ui/server/src/index.ts`: Replaced `/api/props` direct SQL with FastAPI proxy fetch, removed `VALID_PROP_STATS`/`MIN_LINE_SQL` constants, added `/api/prop-hit-rate` proxy route

### SQL Todos Status:
- `sgo-stat-fix`: ✅ done
- `consolidate-props`: ✅ done
- `holdout-selection`: ✅ done
- `prop-hit-rate`: ✅ done
- `test-validate`: ✅ done (165/165 pass)
- `deploy-verify`: 🔄 in_progress (first deploy failed, fixes applied, needs rebuild+redeploy)
- `write-report`: ⏳ pending

### Current state:
- Code changes are complete and tests pass locally
- Containers were built and deployed but props returned empty due to: (1) NaN in odds → fixed, (2) live inference too slow → fixed by switching to stored predictions
- **Needs rebuild and redeploy** after the `_safe_int` fix and `find_edges()` stored-predictions refactor
- Sprint report not yet written
- Git: uncommitted changes on branch `feature/sprint-24-prop-consolidation-and-hit-rates`
</work_done>

<technical_details>
### SGO Stat Misclassification Root Cause
- The `_normalize_sportsgameodds_stat_id()` function lowercases and replaces non-alphanumeric chars with underscores
- `threePointers` → `threepointers` (no underscore between words) → not in the map → **skipped entirely**
- SGO sources had ZERO fg3m entries in the DB — all three-pointer props were being silently dropped
- Low "pts" lines (2.5, 3.5) are genuine API-side misclassification where `statID="points"` is sent for three-pointer markets
- Fix: added `threepointers`, `threepointersmade`, `madethrees`, `fg3m`, `3pm`, etc. to the map

### BFF → FastAPI Consolidation
- The BFF previously queried Postgres directly with `PREDICTION_BLEND_CTE` (averages all models' predictions)
- FastAPI's `find_edges()` used live inference via `Predictor.predict_player()` — single production model per stat, ~60+ seconds for all players
- **Critical fix**: Refactored `find_edges()` to query stored predictions from the `predictions` table using `AVG()` grouping (matching the BFF's CTE approach), only falling back to live inference when no stored predictions exist
- Pydantic `PropEdge` model now has 20 fields (was 10) to match what the frontend needs

### NaN Handling
- `PropLine.over_odds` and `under_odds` are nullable Integer columns
- When loaded into a pandas DataFrame, NULL integers become `float('nan')`
- Pydantic rejects `nan` for `int | None` fields — need explicit NaN → None conversion via `_safe_int()`

### Model Selection
- `_register_best_model()` now reads `config.MODEL_SELECTION_METRIC` ("val_mse" or "test_mse")
- Falls back: test_mse → val_mse → train_mse → inf
- Degradation guardrail also uses the configured metric for comparison

### Prop Hit-Rate
- Infrastructure already existed: `PropLineSnapshot` table with `settle_prop_line_snapshots()` that joins with `game_logs` to determine OVER/UNDER/PUSH outcomes
- New endpoint joins settled snapshots with predictions to compute model-direction hit rates
- A "hit" = the model's predicted direction (OVER/UNDER based on edge sign) matched the actual outcome

### Homelab Deployment
- Server: beelink-gti13, containers: nba-ml-api (port 8000), nba-ml-dashboard (port 8501/3080)
- Build: `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache <service>`
- Deploy: `docker compose --env-file .env -f compose/compose.nba-ml.yml up -d <service>`
- Python tests: `.venv/bin/python -m pytest tests/ -q --ignore=tests/test_notifications.py`
- TypeScript: `source /home/jbl/.nvm/nvm.sh && cd dashboard-ui && npx tsc --noEmit -p server/tsconfig.json`
- API healthcheck: `curl -s http://localhost:8000/health`
- 15 tests in test_notifications.py fail due to missing `apprise` module — pre-existing, unrelated
</technical_details>

<important_files>
- `src/applications/prop_finder.py`
  - Core prop edge finder — major refactor in Sprint 24
  - Changed to use stored predictions (AVG blend) instead of live inference
  - Added team, opponent, is_home, game_date, game_time to output dict
  - Updated query to `session.query(PropLine, Player.name, Player.team)`
  - Confidence formula uses normal CDF logistic approximation (Sprint 23 fix preserved)
  - Edge capped at ±100%

- `src/api/server.py`
  - FastAPI endpoints
  - `PropEdge` model extended with 10 new fields (lines ~154-173)
  - Added `_safe_int()` helper for NaN handling (line ~485)
  - Added `/prop-hit-rate` endpoint (line ~510+)
  - Added `timedelta` import

- `dashboard-ui/server/src/index.ts`
  - BFF Express server
  - `/api/props` now proxies to FastAPI instead of direct SQL (line ~474+)
  - Removed `VALID_PROP_STATS` and `MIN_LINE_SQL` constants
  - Added `/api/prop-hit-rate` proxy route (line ~601+)
  - `PREDICTION_BLEND_CTE`, `PROP_CONFIDENCE_SQL`, `PROP_EDGE_SQL` still used by dashboard overview queries

- `src/data/prop_lines.py`
  - SGO prop scraper — fixed stat ID mapping
  - `_SPORTSGAMEODDS_STAT_MAP` expanded from 14 to 27 entries (line ~53-81)
  - Added `_sgo_unmapped_stats` diagnostic logging in `_extract_sportsgameodds_prop_rows()`

- `config.py`
  - Added `MODEL_SELECTION_METRIC` (line ~158)

- `src/training/trainer.py`
  - `_register_best_model()` refactored for configurable metric (line ~652+)

- `tests/test_prop_lines_sportsgameodds.py`
  - Added 2 new tests for camelCase stat mapping

- `docs/reports/sprint23-props-dashboard-fixes.md`
  - Source report — Sprint 23 next steps define Sprint 24 scope
</important_files>

<next_steps>
### Immediate (was actively working on):
1. **Verify `find_edges()` coherence** — The function was partially rewritten. Need to confirm the stored-predictions refactor integrates cleanly with the existing edges loop (the `for prop_row, player_name, player_team in props:` section). The key change is that `predictions_cache` now stores `{"predicted": float, "low": float, "high": float}` dicts (matching the old Predictor output format).

2. **Rebuild and redeploy** — Both API and dashboard containers need rebuild after the `_safe_int` fix and `find_edges()` stored-predictions refactor:
   ```
   cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache nba-ml-api nba-ml-dashboard && docker compose --env-file .env -f compose/compose.nba-ml.yml up -d nba-ml-api nba-ml-dashboard
   ```

3. **Verify live props** — `curl -s http://localhost:8501/api/props | python3 -c "..."` — confirm props return with proper confidence/edge values, no empty results.

4. **Verify hit-rate endpoint** — `curl -s http://localhost:8501/api/prop-hit-rate | python3 -m json.tool`

5. **Write Sprint 24 report** — `docs/reports/sprint24-prop-consolidation-and-hit-rates.md`

6. **Commit, push, PR, merge** — Standard git workflow:
   ```
   git add -A && git commit -m "..." && git push -u origin feature/sprint-24-prop-consolidation-and-hit-rates
   gh pr create ... && gh pr merge --squash --delete-branch
   ```

### Carry-forward next steps (low priority, for Sprint 25+):
- Investigate blk over-coverage (86.8% vs 80% target)
- Evaluate rolling windows [5,15] vs [5,20]
- Monitor weekly post-retrain-analysis job
- Investigate remaining SGO API-side misclassification (pts line sent as "points" for three-pointers)
- Consider adding hit-rate data to the dashboard UI

### SQL todos remaining:
- `deploy-verify`: in_progress
- `write-report`: pending

### Git state:
- Branch: `feature/sprint-24-prop-consolidation-and-hit-rates` (checked out)
- Base: main at commit after Sprint 23 merge (PR #25)
- Working tree: multiple modified files, uncommitted
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
