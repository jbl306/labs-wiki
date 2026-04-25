---
title: "Copilot Session Checkpoint: Backtest Completion Props Investigation"
type: text
captured: 2026-04-25T15:41:11.027006Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, mempalace, graph, agents, dashboard]
checkpoint_class: project-progress
checkpoint_class_rule: "body:deployed"
retention_mode: compress
status: success
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Backtest Completion Props Investigation
**Session ID:** `39cb6a8f-14d7-43a7-bad1-98ec00e06033`
**Checkpoint file:** `/home/jbl/.copilot/session-state/39cb6a8f-14d7-43a7-bad1-98ec00e06033/checkpoints/005-backtest-completion-props-inve.md`
**Checkpoint timestamp:** 2026-04-25T15:33:35.018463Z
**Exported:** 2026-04-25T15:41:11.027006Z
**Checkpoint class:** `project-progress` (rule: `body:deployed`)
**Retention mode:** `compress`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user first wanted the NBA ML dashboard Backtesting page improved for accuracy/trust, then deployed and reported. That work was completed: canonical settled props now drive headline Backtest metrics, broad backtest metrics are secondary diagnostics, the page was validated live, deployed to the homelab, reported under `reports/`, and pushed to GitHub `main`.

The user then reported a new high-priority props data-integrity issue: DraftKings UI shows Josh Hart steals at `2+` for tonight, while the dashboard shows `0.5` for `SGO_DK`. The current active work is investigating whether SGO/DK/FD lines in the API and production DB are polluted by alternate/game-prop lines or stale/incorrect source mapping, then writing a report under `nba-ml-engine/reports` on how to fix it.
</overview>

<history>
1. The user asked to improve the Backtest page on the dashboard for accuracy and features.
   - Used brainstorming, planning, subagent-driven development, TDD, code review, and verification workflows.
   - Established the product decision: headline Backtest metrics must use settled canonical prop rows, not broad `predictions x game_logs x prop_lines`; broad backtest remains a clearly labeled secondary diagnostic.
   - Created and committed:
     - `docs/superpowers/specs/2026-04-25-backtest-accuracy-page-design.md`
     - `docs/superpowers/plans/2026-04-25-backtest-accuracy-page.md`
   - Implemented backend canonical aggregation, FastAPI endpoint, BFF contract/proxy, frontend API types, and React Backtest page.
   - Ran per-task spec and code-quality reviews and fixed review issues before proceeding.

2. Task 5 BFF proxy hardening resumed after compaction.
   - Fixed `days` query validation for `/api/backtest`: parse/clamp/default to `1..365`, use validated numeric value in cache key and FastAPI upstream path.
   - Fixed semantic sorting for broad diagnostic `by_edge_size`: `0-5%`, `5-15%`, `15-30%`, `30%+`, unknowns last lexicographically.
   - Preserved `by_edge_abs` support because live/current optimized matview includes it.
   - Commit: `827b790 fix: harden backtest proxy parameters`.
   - Passed spec and quality review.

3. Task 6 React API types.
   - Replaced old broad-only `BacktestData`/`BacktestDetail` in `dashboard-ui/src/lib/api.ts` with canonical backtest + broad diagnostic types.
   - Preserved server-approved nullable fields: `CanonicalBacktestDetail.player_id`, `confidence_tier`, and `odds`.
   - Initial commit: `731655e feat: update backtest API types`.
   - Quality review flagged permissive `[key: string]: unknown` in `BacktestBreakdown`; removed it.
   - Fix commit: `0983a67 fix: tighten backtest type safety`.
   - Final typecheck became clean.

4. Task 7 React Backtest page rebuild.
   - Rebuilt `dashboard-ui/src/pages/BacktestPage.tsx` around canonical settled-prop data.
   - Added:
     - Canonical summary cards: settled bets, hit rate vs breakeven, flat ROI, Kelly ROI, peak drawdown.
     - Accuracy notes with population counts, source labels, warning badges.
     - Canonical P&L curve with flat and Kelly series.
     - Reliability charts by stat, signal tier, edge bucket, direction, source.
     - Settled bet details table with CSV export.
     - Broad Model Diagnostic section below canonical content only.
   - Initial commit: `2d3fb35 feat: rebuild backtest page around canonical results`.
   - Quality review found:
     - Broad diagnostic should not render healthy cards/charts when `broad.status !== 'ok'`.
     - Empty canonical results should still show warnings.
     - Timestamp/drawdown/key cleanup.
   - Fix commit: `7ffe24d fix: handle backtest diagnostic edge states`.
   - Passed final re-review.

5. Task 8 validation and deployment.
   - Initial validation command missed server TypeScript compilation because `dashboard-ui/package.json` has no `test:server` or `typecheck:server` scripts.
   - Docker build caught server TS error:
     - `dashboard-ui/server/src/index.ts` `loadBroadBacktestDiagnostic()` returned `by_stat` rows without required `hit_rate`.
   - Fixed by adding `hit_rate` to broad diagnostic `byStat` rows.
   - Commit: `e2fc1a4 fix: address backtest validation issues`.
   - Added `npx tsc -p server/tsconfig.json` to practical validation coverage.

6. Live validation exposed canonical-vs-history mismatch.
   - After initial deploy, `/api/backtest` returned:
     - canonical_total `8394`
     - history_total `4197`
   - Investigation found the canonical FastAPI endpoint ranked one line per `player_id/game_date/stat_name/source`, while Props History deduped to one line per `player/date/stat`.
   - Root cause: `src/api/server.py` `ROW_NUMBER()` partition included `snap.source`, doubling or multiplying canonical population across sportsbooks.
   - Fixed canonical endpoint to partition by `snap.player_id, snap.game_date, snap.stat_name` only.
   - Updated regression test to assert source-agnostic canonical grain.
   - Commits:
     - `696de7b fix: align canonical backtest grain`
     - `1dd4c94 test: harden canonical backtest grain check`
   - Live validation after redeploy and dashboard cache restart:
     - Backtest canonical_total `4197`
     - Props History total `4197`
     - Backtest hit_rate `0.5282`
     - Props History hit_rate `0.5282`
     - Backtest flat_pnl `237`
     - Props History flat_pnl `237`
     - broad diagnostic still `11400`.

7. Final Backtest report and push.
   - Created `reports/2026-04-25-backtest-accuracy-page-status.md`.
   - Report documents implementation, validation commands, deployment, live comparison, and remaining notes.
   - Commit: `4140810 docs: report backtest accuracy page status`.
   - Pushed to GitHub `main`: `92cdb88..4140810`.

8. The user then reported a new props line-integrity issue:
   - User said: “for props, josh hart steals line is at 2+ for tonight on draftkings ui. the dashboard says 0.5 for sgo_dk source. this is a huge inaccuracy that I'm worried about across the board for predictions and bet ingestion. validate the api against the actual lines for dk/fd and whats in the db. create a report on how to fix.”
   - Invoked `systematic-debugging`, `stealth-browser`, and `data-analyst`.
   - Queried MemPalace and found prior critical context:
     - SGO has previously mixed standard O/U props with alternate/game-prop lines.
     - Prior issue examples included one-sided stl/blk “3+” props, missing under odds, and SGO extraction using source/stat keys incorrectly.
   - Fetched live `/api/props`.
   - Confirmed API currently returns `340` props for `2026-04-25`, source `fastapi_prop_edges`, sources `['SGO_DK', 'SGO_FD']`, stats `['ast', 'blk', 'fg3m', 'pts', 'reb', 'stl']`.
   - Confirmed live API row for Josh Hart:
     - `player_name`: Josh Hart
     - `stat_name`: `stl`
     - `source`: `SGO_DK`
     - `line`: `0.5`
     - `predicted`: `1.34`
     - `call`: `Over`
     - `odds`: `-226`
     - `game_date`: `2026-04-25`
   - Also API row for Josh Hart `SGO_FD stl`:
     - `line`: `1.5`
     - `predicted`: `1.34`
     - `call`: `Under`
     - `odds`: `-270`
   - Queried production DB for Josh Hart:
     - `players.id = 1879`, `name = Josh Hart`, `team = NYK`.
   - Confirmed production DB has tables:
     - `prop_lines`
     - `prop_line_snapshots`
   - Investigation was still in progress at compaction; no report for the Josh Hart/DK/FD line issue has been written yet.
</history>

<work_done>
Files created:
- `docs/superpowers/specs/2026-04-25-backtest-accuracy-page-design.md`
  - Approved Backtest page design spec.
- `docs/superpowers/plans/2026-04-25-backtest-accuracy-page.md`
  - Implementation plan for canonical backtest backend/BFF/UI/deploy/report.
- `tests/test_canonical_backtest.py`
  - Canonical aggregation tests, endpoint registration test, canonical SQL grain regression.
- `src/evaluation/canonical_backtest.py`
  - Pure canonical settled-prop aggregation service.
- `reports/2026-04-25-backtest-accuracy-page-status.md`
  - Final deployed status report for Backtest accuracy page.

Files modified:
- `.gitignore`
  - Added `.superpowers/`.
- `src/api/server.py`
  - Added `/evaluation/backtest/canonical`.
  - Fixed broad count to `SUM(total_calls)`.
  - Fixed canonical endpoint SQL and player join.
  - Final important fix: canonical `ROW_NUMBER()` partition is now `player_id, game_date, stat_name`, not per `source`.
- `dashboard-ui/server/src/dashboardContracts.ts`
  - Added canonical backtest payload, broad diagnostic types, normalization helpers, explicit unavailable payload.
- `dashboard-ui/server/src/dashboardContracts.test.ts`
  - Added BFF contract tests for canonical normalization and unavailable payload behavior.
- `dashboard-ui/server/src/index.ts`
  - `/api/backtest` now proxies FastAPI canonical data and attaches broad diagnostic.
  - Validates/clamps `days`.
  - Sorts broad edge buckets semantically.
  - Adds `hit_rate` to broad `by_stat` rows for server TS contract.
  - Canonical fetch failure returns HTTP 502 with unavailable payload; broad diagnostic failure remains non-fatal.
- `dashboard-ui/src/lib/api.ts`
  - Replaced old `BacktestData` with canonical + broad diagnostic type shape.
- `dashboard-ui/src/pages/BacktestPage.tsx`
  - Rebuilt page around canonical metrics and labeled broad diagnostic.
  - Handles loading/error/unavailable/empty states.
  - Shows accuracy notes and warnings.
  - Broad diagnostic cards/charts render only when `broad.status === 'ok'`.
- `reports/2026-04-25-backtest-accuracy-page-status.md`
  - Final report committed and pushed.

Validation completed for Backtest work:
- `.venv/bin/python -m pytest tests/test_canonical_backtest.py::test_canonical_backtest_endpoint_ranks_one_line_per_player_date_stat -q`
- `.venv/bin/python -m pytest tests/test_canonical_backtest.py tests/test_backtester.py tests/test_dashboard_accuracy_followups.py -q` → `24 passed`
- `.venv/bin/python -m py_compile src/evaluation/canonical_backtest.py src/api/server.py`
- `cd dashboard-ui && npx tsc -p server/tsconfig.json`
- `cd dashboard-ui && npx tsx --test server/src/dashboardContracts.test.ts` → `14 passed`
- `cd dashboard-ui && npm run build`
- changed-file ESLint for server contracts/index, API types, and Backtest page.
- Homelab deploy:
  - `docker compose --env-file .env -f compose/compose.nba-ml.yml up -d --build nba-ml-api nba-ml-dashboard`
- Live validation:
  - `/api/backtest`
  - `/api/props/history`
  - `/backtest` `HTTP/2 200`

Current git state at Backtest completion:
- Worktree: `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final`
- Branch: `feature/dashboard-accuracy-final`
- `origin/main` points to `4140810`.
- Final pushed commit: `4140810 docs: report backtest accuracy page status`.

Current active work:
- Investigating Josh Hart/DK/FD props line mismatch.
- No code changes or report have been created yet for the new props line-integrity investigation.
</work_done>

<technical_details>
Backtest architecture and decisions:
- Headline Backtest metrics must use settled canonical prop rows.
- Broad `mv_backtest_summary` metrics are useful but must remain secondary diagnostics.
- Canonical settled grain must match Props History:
  - one line per `player/date/stat`
  - not per sportsbook source
- The canonical endpoint still preserves the selected row’s `source`, but source breakdown now represents the chosen canonical source, not all sportsbook rows.
- Broad diagnostic remains `11,400` calls and intentionally differs from canonical `4,197`.
- Props History ROI is reported as percentages (`5.6`, `-5.9`), while Backtest canonical ROI values are decimal rates (`0.0565`, `-0.0572`). Report explicitly notes this unit mismatch.
- Kelly P&L differs slightly between canonical Backtest and Props History after reconciliation (`-22.49` vs `-23.07`) because canonical service computes Kelly under the new endpoint contract.

Validation/deploy quirks:
- `dashboard-ui/package.json` does not define `test:server` or `typecheck:server`.
- Use direct equivalents:
  - `cd dashboard-ui && npx tsx --test server/src/dashboardContracts.test.ts`
  - `cd dashboard-ui && npx tsc -p server/tsconfig.json`
- Docker dashboard build runs both frontend build and server TypeScript compile:
  - Dockerfile step: `RUN npx tsc -p server/tsconfig.json`
  - Local validation must include this or Docker may catch contract errors later.
- Python tests must use repo-local venv:
  - `.venv/bin/python -m pytest ...`
  - `pytest` is not on global PATH in this shell.
- Homelab deploy must run from `/home/jbl/projects/homelab` and load `.env`:
  ```bash
  cd /home/jbl/projects/homelab
  set -a && . ./.env && set +a
  NBA_ML_ENGINE_PATH=/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final \
    docker compose --env-file .env -f compose/compose.nba-ml.yml up -d --build nba-ml-api nba-ml-dashboard
  ```
- Dashboard BFF has an in-memory cache, including `backtest:30`. After redeploying API-only changes, restart `nba-ml-dashboard` or wait for cache expiry before live validation.

Relevant prior memory for current Josh Hart/props issue:
- Prior SGO alt-line problem:
  - SportsGameOdds DraftKings returns alternate/game-prop lines alongside standard O/U props.
  - Examples in prior sessions: `blk 2.5` with `+800 over` and no under odds, stl/blk one-sided game props.
  - Prior fixes included rejecting lines missing either `over_odds` or `under_odds`.
  - Prior context says `_extract_sportsgameodds_prop_rows()` and `fetch_prop_lines()` in `src/data/prop_lines.py` are central.
  - Prior issue: SGO extractor used `setdefault()` keyed by `(player_id, date, source, stat_name)`, whichever line came first won, and DK alts could come first.
  - Another prior fix used “primary_props” CTE selecting closest line to model prediction; but this may now be unsafe because it can prefer a stale/incorrect line near the prediction rather than the actual sportsbook market.
- Current live API evidence:
  - Josh Hart `SGO_DK stl` shows `line: 0.5`, `odds: -226`, `predicted: 1.34`, `call: Over`.
  - User says DraftKings UI shows `2+` for tonight.
  - Josh Hart `SGO_FD stl` shows `line: 1.5`, `odds: -270`, `predicted: 1.34`, `call: Under`.
  - This could indicate:
    - dashboard is using standard O/U `0.5` while user is viewing a DK “2+ steals” game prop/alternate market;
    - or SGO_DK is stale/incorrect relative to DK UI;
    - or source mapping/market extraction is mixing alternate and standard markets;
    - or “2+” should be represented as line `1.5`, not `2.0`, and the dashboard’s `0.5` is genuinely wrong.
- Need to validate against:
  - actual DK UI line
  - actual FD UI line
  - SGO API raw payload if possible
  - `prop_lines`
  - `prop_line_snapshots`
  - `/api/props` output
  - prediction join logic
- It is important not to jump to a fix; use systematic debugging first.

Current DB access pattern:
- Can query production DB via:
  ```bash
  cd /home/jbl/projects/homelab
  docker exec nba-ml-db psql -U nba_ml -d nba_ml -c "<SQL>"
  ```
- Confirmed Josh Hart:
  - `id = 1879`
  - `team = NYK`
- Confirmed prop tables:
  - `prop_lines`
  - `prop_line_snapshots`

Current API fetch used:
```bash
curl -fsSL -A 'Mozilla/5.0' 'https://nba-dashboard.jbl-lab.com/api/props' > /tmp/props-current.json
```
Then inspected Josh Hart and stl rows via Python.

Potential next report path:
- Use a new report under `reports/`, likely:
  - `reports/2026-04-25-prop-line-integrity-audit.md`
  - or similar.
</technical_details>

<important_files>
- `src/data/prop_lines.py`
  - Central ingestion/extraction logic for The Odds API and SportsGameOdds prop lines.
  - Prior sessions heavily modified this file for SGO extraction, missing-odds filters, selected bookmakers, and alt-line handling.
  - Must inspect `_extract_sportsgameodds_prop_rows()`, `_selected_sportsgameodds_bookmakers()`, `_SPORTSGAMEODDS_BOOKMAKER_MAP`, and `fetch_prop_lines()`.
- `src/api/server.py`
  - FastAPI serves `/prop-edges` and `/evaluation/backtest/canonical`.
  - For current investigation, inspect prop-edge endpoint and any SQL/selection logic that reads `prop_lines` or snapshots.
  - Recently changed canonical backtest partition around lines ~1035.
- `dashboard-ui/server/src/index.ts`
  - BFF `/api/props` and `/api/props/history`.
  - It proxies FastAPI `/prop-edges` for current props and may have fallback SQL.
  - Props History uses `PREDICTION_BLEND_CTE` and dedupe logic around lines ~827–1170.
- `dashboard-ui/src/pages/props/TodayTab.tsx`
  - Likely renders current props rows and source/line values. Not yet inspected for Josh Hart issue.
- `dashboard-ui/src/lib/api.ts`
  - Frontend API types; useful to understand displayed prop shape.
- `tasks/lessons.md`
  - Contains durable lessons including prior prop-line and API-performance issues.
  - Important entries:
    - API endpoints must not trigger live inference.
    - Dashboard overview props must use latest joined prop slate, not wall-clock today.
    - SGO alt-line / one-sided prop lessons are in MemPalace/session summaries, may need new lesson after final investigation.
- `reports/2026-04-25-backtest-accuracy-page-status.md`
  - Final report for completed Backtest work.
- `docs/superpowers/plans/2026-04-25-backtest-accuracy-page.md`
  - Completed implementation plan for Backtest; less relevant now except as historical context.
- `tests/test_canonical_backtest.py`
  - Contains regression for canonical backtest grain; completed.
</important_files>

<next_steps>
Immediate active task: investigate and report on Josh Hart / DK / FD prop-line integrity.

Recommended next steps:
1. Update session `plan.md` to reflect the new current task, since reminder requested it.
   - Problem: Josh Hart steals line mismatch and cross-board prop-line integrity risk.
   - Approach: API → DB → raw source → sportsbook UI validation → report fixes.
2. Create SQL todos for this new investigation/report.
3. Continue systematic debugging:
   - Query `prop_lines` and `prop_line_snapshots` for Josh Hart (`player_id=1879`), `game_date='2026-04-25'`, `stat_name in ('stl','blk','ast','reb','fg3m','pts')`, all sources, fetched/snapshot timestamps, odds, line, market identifiers if available.
   - Query all `stl` lines for `SGO_DK`/`SGO_FD` on `2026-04-25` to detect distribution anomalies (`0.5`, `1.5`, `2.5`, missing odds, weird odds).
   - Compare `prop_lines` vs `prop_line_snapshots`.
   - Inspect `src/data/prop_lines.py` to identify raw source fields stored/dropped and whether SGO market type/period/alternate line markers are available but not stored.
   - Check FastAPI `/prop-edges` behavior for Josh Hart, including whether it reads `prop_lines`, `prop_line_snapshots`, or “primary” selection logic.
4. Validate external/current sportsbook lines:
   - Use stealth-browser for DraftKings and FanDuel UI if accessible.
   - If direct UI blocks/geofences, try public sportsbook pages/search and capture screenshots or page text.
   - Consider querying raw SportsGameOdds API from inside `nba-ml-api` container if API key is available via env; do not print secrets.
   - Compare SGO raw DK/FD entries for Josh Hart steals against DB and dashboard.
5. Produce report under `nba-ml-engine/reports`, likely:
   - `reports/2026-04-25-prop-line-integrity-audit.md`
   - Include:
     - user-reported mismatch
     - live dashboard/API evidence
     - DB evidence
     - DK/FD UI or raw provider evidence
     - scope/risk analysis across all current props
     - root cause hypothesis with confidence
     - concrete fix plan
     - validation plan before deployment
6. Do not implement the fix unless the user asks; current request is to validate and create a report on how to fix.
7. At end, save important finding to MemPalace and diary.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
