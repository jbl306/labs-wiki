---
title: "Copilot Session Checkpoint: Backtest Accuracy Contracts"
type: text
captured: 2026-04-25T15:10:21.567953Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, mempalace, graph, agents, dashboard]
checkpoint_class: durable-architecture
checkpoint_class_rule: "body:architecture"
retention_mode: retain
status: success
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Backtest Accuracy Contracts
**Session ID:** `39cb6a8f-14d7-43a7-bad1-98ec00e06033`
**Checkpoint file:** `/home/jbl/.copilot/session-state/39cb6a8f-14d7-43a7-bad1-98ec00e06033/checkpoints/004-backtest-accuracy-contracts.md`
**Checkpoint timestamp:** 2026-04-25T14:38:15.370969Z
**Exported:** 2026-04-25T15:10:21.567953Z
**Checkpoint class:** `durable-architecture` (rule: `body:architecture`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user asked to improve the NBA ML dashboard Backtesting page at `nba-dashboard.jbl-lab.com` for accuracy and features, with accuracy/trust as the primary focus. The approved approach is to make settled canonical prop performance the headline backtest population, keep the existing broad `predictions × game_logs × prop_lines` backtest as a labeled secondary diagnostic, and implement the work with TDD, subagent-driven task execution, review gates, validation, deployment, a new report, and push to GitHub.
</overview>

<history>
1. The prior compacted session ended after dashboard accuracy hardening was implemented, deployed, reported, and pushed.
   - Final commit from prior work: `92cdb88 fix: finish dashboard accuracy hardening` pushed to `main`.
   - Final report: `reports/2026-04-25-dashboard-accuracy-final-status.md`.
   - Key live state: `/api/props` had 340 canonical props, calibration ECE was fixed to served signal (`0.0215`), registry health was clean, and remaining degraded model-health was legitimate model-quality drift/hit-rate risk.

2. The user then asked: “now improve the backtest page on the dashboard in terms of accuracy and features.”
   - Used the required brainstorming skill before implementation.
   - Queried MemPalace and session history for NBA ML dashboard/backtest context.
   - Inspected existing backtest page/API:
     - `dashboard-ui/src/pages/BacktestPage.tsx` was thin: summary cards, broad cumulative P&L, hit rate by stat, hit rate by edge size.
     - `dashboard-ui/server/src/index.ts` `/api/backtest` read `mv_backtest_summary`, returned old broad-only shape, and returned empty success data on errors.
     - Existing lessons warned that History-vs-Backtest differences are population differences and must show source/counts.
   - Live checks showed:
     - `/api/backtest`: 11,400 broad calls, 53.45% hit rate, +786 pseudo-units.
     - `/api/props/history`: 4,197 settled canonical bets, 52.82% hit rate, +237 flat units, Kelly ROI -5.9%.
     - This mismatch became the main accuracy issue.

3. Brainstorming/design process:
   - Offered visual companion; user accepted.
   - Asked the user to choose primary target:
     - User chose **Accuracy/trust first: reconcile backtest vs settled props, show data source, coverage, caveats, and prevent misleading metrics**.
   - Asked whether headline metrics should use broad backtest or settled/canonical props:
     - User chose **Use settled/canonical props for headline metrics, keep broad backtest as secondary diagnostic**.
   - Offered approaches:
     - User chose **B. Canonical backtest API**.
   - Presented and got approval for:
     - Architecture/data contract.
     - Feature set.
     - Data flow, error handling, and validation.
   - Created a visual wireframe via visual companion showing:
     - Canonical summary cards first.
     - Accuracy notes.
     - Canonical P&L/stat reliability sections.
     - Broad Model Diagnostic below.
     - User approved the layout.

4. Design spec and implementation plan:
   - Invoked writing-clearly-and-concisely for prose.
   - Wrote and committed design spec:
     - `docs/superpowers/specs/2026-04-25-backtest-accuracy-page-design.md`
     - Commit: `35f59b2 docs: design backtest accuracy page`
   - Added `.superpowers/` to `.gitignore` because visual companion artifacts were untracked.
   - User approved the spec.
   - Invoked writing-plans.
   - Wrote detailed implementation plan:
     - `docs/superpowers/plans/2026-04-25-backtest-accuracy-page.md`
     - Commit: `d0a614c docs: plan backtest accuracy page`
   - User chose **Subagent-Driven** execution.
   - Invoked subagent-driven-development.

5. Task 1: Canonical backtest contract tests.
   - Implementer added `tests/test_canonical_backtest.py`.
   - Initial commit: `a424261b test: define canonical backtest contract`.
   - Spec review passed, but quality review found ambiguities:
     - Flat P&L formula underdetermined.
     - Signal tier thresholds undefined.
     - Detail direction/call under-tested.
     - Edge bucket assertion vague/wrong.
     - Composite/excluded-stat semantics ambiguous.
     - `generated_at` handling unclear.
   - Fix commit: `604166c test: clarify canonical backtest contract`.
     - Clarified +1/-1 flat P&L semantics.
     - Clarified tier thresholds: High >= 0.8, Medium >= 0.6, Low otherwise.
     - Added detail assertions for over/under.
     - Added exact edge bucket count expectations.
     - Clarified composite stats are flagged, not dropped.
     - Added default `generated_at` assertion.
     - Updated plan snippet to match.
   - Final quality review found one bad comment and timestamp comment need:
     - Fix commit: `5e8e4d6 test: fix backtest contract comments`.
   - Task 1 final review approved.

6. Task 2: Canonical backtest aggregation service.
   - Implemented `src/evaluation/canonical_backtest.py`.
   - Commit: `4b9b356 feat: add canonical backtest aggregation`.
   - Exports:
     - `BacktestWarning`
     - `compute_american_breakeven`
     - `compute_kelly_fraction`
     - `build_backtest_response_from_rows`
   - Tests passed: all canonical tests.
   - Compile passed.
   - Spec and quality reviews approved.

7. Task 3: FastAPI canonical endpoint.
   - Added route test to `tests/test_canonical_backtest.py`.
   - Added `/evaluation/backtest/canonical` in `src/api/server.py`.
   - Initial commit: `b4ebc84 feat: expose canonical backtest endpoint`.
   - Spec review found critical SQL bug:
     - CTE/window referenced `snap.line` in a grouped scope incorrectly.
     - Also broad count used `COUNT(*)` instead of `SUM(total_calls)`.
   - Fix commit: `32c87a4 fix: correct canonical backtest endpoint query`.
     - Rewrote SQL with `prediction_blend` CTE and `ranked_snaps` CTE.
     - Fixed player join to `players p ON p.id = rs.player_id`.
     - Added confidence-score CASE defaulting to `0.5`.
     - Fixed broad count to `COALESCE(SUM(total_calls), 0)`.
   - Quality review found high-severity multi-source dedupe:
     - `ROW_NUMBER()` partition omitted `snap.source`, silently dropping sportsbook/source rows and distorting `by_source`.
   - Fix commit: `669dd4e fix: preserve backtest source splits`.
     - Partition now includes `snap.source`.
     - Added regression test that asserts source is in the partition.
   - Final Task 3 quality review approved.

8. Task 4: BFF backtest contract helpers.
   - Added types/helpers in `dashboard-ui/server/src/dashboardContracts.ts`.
   - Added tests in `dashboard-ui/server/src/dashboardContracts.test.ts`.
   - Initial commit: `635e648 feat: add backtest dashboard contract`.
   - Spec review passed.
   - Quality review found contract ergonomics issues:
     - `normalizeCanonicalBacktest` null semantics were confusing.
     - `CanonicalBacktestDetail` over-constrained fields that may be nullable.
     - `buildBacktestUnavailablePayload` generated runtime timestamp without injectable value.
   - Fix commit: `4a4da6d fix: tighten backtest contract helpers`.
     - `normalizeCanonicalBacktest(canonical, broadDiagnostic?)` distinguishes omitted vs explicit `null`.
     - `player_id`, `confidence_tier`, and `odds` are nullable in detail type.
     - `buildBacktestUnavailablePayload(reason, generatedAt?)` accepts fixed timestamp.
     - Added tests for all behaviors.
   - Final Task 4 review approved.

9. Task 5: BFF `/api/backtest` canonical proxy plus broad diagnostic.
   - Implemented route changes in `dashboard-ui/server/src/index.ts`.
   - Initial commit: `406dfab feat: proxy canonical backtest data`.
   - Added:
     - `fetchFastApiJson<T>()` using existing `apiFetch()`.
     - `loadBroadBacktestDiagnostic()`.
     - Replaced `/api/backtest` to fetch FastAPI canonical data and attach broad diagnostic.
   - Spec review found real bug:
     - Canonical FastAPI failure returned unavailable payload with HTTP 200, not HTTP 502.
     - `npm run test:server` script is absent; direct `npx tsx --test server/src/dashboardContracts.test.ts` is the available server test command.
   - Fix commit: `c2e753c fix: return 502 for canonical backtest failures`.
     - Changed route to use `Promise.all`.
     - Canonical fetch rejection now reaches route catch and returns HTTP 502 with unavailable payload.
     - Broad diagnostic failure remains non-fatal and returns `null`.
   - Spec re-review approved.
   - Quality review then found three real issues:
     - **Current active issue:** `days` query is unvalidated, causing cache-key pollution/upstream errors.
     - `by_edge_size` sorting is lexicographic, producing wrong order (`0-5%`, `15-30%`, `30%+`, `5-15%`).
     - `byEdgeAbs` may be dead/empty depending on production matview schema; reviewer claimed migration has only `daily`, `by_stat`, `by_edge`, though earlier project files showed `scripts/optimize_db.py` includes `by_edge_abs`. This requires verification before fixing/removing.
   - This is where work paused for compaction.
</history>

<work_done>
Files created:
- `docs/superpowers/specs/2026-04-25-backtest-accuracy-page-design.md`
  - Approved design spec for accuracy-first Backtesting page.
  - Commit: `35f59b2`.
- `docs/superpowers/plans/2026-04-25-backtest-accuracy-page.md`
  - Detailed implementation plan with TDD tasks.
  - Commit: `d0a614c`.
- `tests/test_canonical_backtest.py`
  - Canonical backtest contract tests and endpoint regression tests.
  - Commits: `a424261b`, `604166c`, `5e8e4d6`, plus later endpoint/source tests.
- `src/evaluation/canonical_backtest.py`
  - Pure canonical settled-prop aggregation service.
  - Commit: `4b9b356`.

Files modified:
- `.gitignore`
  - Added `.superpowers/`.
  - Commit: `35f59b2`.
- `/home/jbl/.copilot/session-state/39cb6a8f-14d7-43a7-bad1-98ec00e06033/plan.md`
  - Updated from final dashboard hardening to backtest accuracy page work.
- `src/api/server.py`
  - Added `/evaluation/backtest/canonical`.
  - Fixed SQL CTE shape, broad count, players join, confidence score CASE, and source-preserving ranking.
  - Commits: `b4ebc84`, `32c87a4`, `669dd4e`.
- `dashboard-ui/server/src/dashboardContracts.ts`
  - Added backtest contract types/helpers.
  - Refined null semantics, nullable detail fields, and deterministic unavailable timestamps.
  - Commits: `635e648`, `4a4da6d`.
- `dashboard-ui/server/src/dashboardContracts.test.ts`
  - Added tests for BFF contract helpers.
  - Commits: `635e648`, `4a4da6d`.
- `dashboard-ui/server/src/index.ts`
  - Replaced old `/api/backtest` broad-only route with canonical FastAPI proxy plus broad diagnostic helper.
  - Fixed canonical failure to return HTTP 502.
  - Commits: `406dfab`, `c2e753c`.

Current task state:
- Task 1 accepted.
- Task 2 accepted.
- Task 3 accepted.
- Task 4 accepted.
- Task 5 is **not yet accepted**; quality review found issues needing a focused fix.
- SQL todos:
  - `backtest-task-1` done.
  - `backtest-task-2` done.
  - `backtest-task-3` done.
  - `backtest-task-4` done.
  - `backtest-task-5` in progress.
  - `backtest-task-6` through `backtest-task-10` pending.
- Branch/worktree:
  - Worktree: `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final`
  - Branch: `feature/dashboard-accuracy-final`
  - Ahead of `origin/main` by multiple commits from spec/plan/tasks.
- No final deployment or report for backtest page has happened yet.
- Do not push yet; implementation is incomplete.
</work_done>

<technical_details>
- The core accuracy decision: the Backtesting page must no longer use broad `predictions × game_logs × prop_lines` as the headline performance claim. Headline metrics should use settled canonical props, matching Props History population.
- Broad diagnostic remains valuable but must be labeled as a wider model diagnostic that is not directly comparable to Props History.
- Live pre-work evidence:
  - `/api/backtest`: `total_bets` 11,400, hit rate 0.5345, pseudo P&L +786, date range 2026-03-16 to 2026-04-24.
  - `/api/props/history`: total bets 4,197, hit rate 0.5282, flat P&L +237, Kelly ROI -5.9%, date range approximately 2026-03-26 to 2026-04-24.
- Existing lesson:
  - “Hit rate discrepancy between pages is population difference, not a bug”: History requires settled snapshots; Backtest was broader. Display data source and population count beside rates.
- Canonical flat P&L semantics:
  - +1 unit per hit, -1 per miss; ignores odds.
- Kelly semantics in canonical service:
  - Capped half-Kelly, cap 0.25.
- Confidence tier thresholds:
  - High >= 0.8.
  - Medium >= 0.6.
  - Low otherwise.
- Edge bucket thresholds:
  - `0-5%`, `5-15%`, `15-30%`, `30%+`.
- Composite stats:
  - For this pass, synthetic/composite stats such as `pra` are flagged in `population.excluded_stats` and warnings, but **not dropped** from headline metrics/details unless a future product decision says to remove them.
- Canonical FastAPI endpoint:
  - Path: `/evaluation/backtest/canonical`
  - Params: `days: int = Query(default=30, ge=1, le=365)`, `db=Depends(get_db)`.
  - Reads stored data only; no inference.
  - Broad diagnostic count uses:
    - `SELECT COALESCE(SUM(total_calls), 0) FROM mv_backtest_summary WHERE qtype = 'daily'`
    - Failure is non-fatal with rollback/debug/use 0.
  - Main query uses:
    - `prediction_blend` CTE: average predictions by `player_id`, `game_date`, `stat_name`.
    - `ranked_snaps` CTE: joins snapshots to prediction blend and ranks by smallest `ABS(pb.predicted_value - snap.line)`.
    - Critical: partition includes `snap.source`: `PARTITION BY snap.player_id, snap.game_date, snap.stat_name, snap.source`
    - Final join uses `players p ON p.id = rs.player_id`.
  - Confidence score SQL:
    - Defaults to 0.5 if missing prediction or missing/zero CI.
    - Otherwise logistic approximation using `1/(1+EXP(-1.7 * ABS(predicted-line) / sigma))`.
- BFF `/api/backtest`:
  - Uses existing `apiFetch()` circuit breaker for FastAPI.
  - `fetchFastApiJson<T>()` wraps `apiFetch()` and throws on non-OK.
  - `loadBroadBacktestDiagnostic()` reads `mv_backtest_summary`.
  - Current issue: the route still needs quality fixes for days validation and edge sorting.
  - Canonical fetch failure must return HTTP 502 with `buildBacktestUnavailablePayload(reason)`.
  - Broad diagnostic failure must be non-fatal and use `null`.
- There is no `npm run test:server` script in `dashboard-ui/package.json`.
  - Existing working server test command: `cd dashboard-ui && npx tsx --test server/src/dashboardContracts.test.ts`.
  - `npm run build` passed for BFF/frontend bundle in several tasks.
  - `npx eslint server/src/index.ts` passed after Task 5.
- Homelab deployment gotcha from prior work:
  - Always deploy from `/home/jbl/projects/homelab`.
  - Must load `.env` and use `--env-file .env`:
    ```bash
    cd /home/jbl/projects/homelab
    set -a && . ./.env && set +a
    NBA_ML_ENGINE_PATH=/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final \
      docker compose --env-file .env -f compose/compose.nba-ml.yml up -d --build nba-ml-api
    ```
  - Same pattern for `nba-ml-dashboard`.
- Potential `by_edge_abs` ambiguity:
  - Quality reviewer claimed `mv_backtest_summary` migration only has `daily`, `by_stat`, `by_edge`, making `by_edge_abs` dead.
  - Earlier in this session we inspected `scripts/optimize_db.py` and saw `by_edge_abs` present there. `alembic/versions/a1b2c3d4e5f6_add_dashboard_matviews.py` may be older and lacks it.
  - Before removing `by_edge_abs`, verify current live/optimized schema expectations. Prior live `/api/backtest` before this work returned `by_edge_abs_len: 5`, so production likely has it. Safer fix may be to leave `by_edge_abs` support, not remove it, and only fix sort/validation.
</technical_details>

<important_files>
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/docs/superpowers/specs/2026-04-25-backtest-accuracy-page-design.md`
  - Approved design spec.
  - Defines goals: canonical settled props headline, broad diagnostic secondary, explicit population warnings, no silent failures.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/docs/superpowers/plans/2026-04-25-backtest-accuracy-page.md`
  - Detailed task-by-task implementation plan.
  - Contains expected contracts and validation steps.
  - Some snippets may have drifted slightly due implementation/review fixes.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/tests/test_canonical_backtest.py`
  - Canonical backend contract and endpoint tests.
  - Important tests include:
    - Breakeven odds math.
    - Kelly cap.
    - Settled headline metrics.
    - Grouping by stat/tier/direction/source/edge.
    - Composite warning semantics.
    - Empty response warning.
    - Default `generated_at`.
    - Route registration.
    - Source-preserving SQL partition.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/src/evaluation/canonical_backtest.py`
  - Pure canonical aggregation service.
  - No DB/HTTP/inference.
  - Builds canonical response from row-like objects.
  - Approved by reviews.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/src/api/server.py`
  - FastAPI server.
  - Added `/evaluation/backtest/canonical` around the evaluation endpoints before calibration.
  - Important to preserve:
    - `prediction_blend` + `ranked_snaps`.
    - `PARTITION BY snap.player_id, snap.game_date, snap.stat_name, snap.source`.
    - `players p ON p.id = rs.player_id`.
    - `COALESCE(SUM(total_calls), 0)` for broad count.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/dashboard-ui/server/src/dashboardContracts.ts`
  - BFF contract layer.
  - Added:
    - `BacktestStatus`
    - `BacktestWarningSeverity`
    - `BacktestWarning`
    - `CanonicalBacktestSummary`
    - `BacktestPopulation`
    - `BacktestBreakdown`
    - `CanonicalBacktestDetail`
    - `BroadBacktestDiagnostic`
    - `CanonicalBacktestPayload`
    - `normalizeCanonicalBacktest`
    - `buildBacktestUnavailablePayload`
  - Final quality-approved state includes explicit null semantics and deterministic timestamp optional param.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/dashboard-ui/server/src/dashboardContracts.test.ts`
  - BFF contract tests.
  - 14 tests passed after Task 4 fixes.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/dashboard-ui/server/src/index.ts`
  - Current active work file for Task 5.
  - Added `fetchFastApiJson`, `loadBroadBacktestDiagnostic`, and replaced `/api/backtest`.
  - Needs fixes from latest quality review:
    - Validate/clamp `days`.
    - Sort `by_edge_size` semantically.
    - Investigate/handle `by_edge_abs` claim carefully.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/dashboard-ui/src/lib/api.ts`
  - Still old React API type for `BacktestData`; Task 6 will update it.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-final/dashboard-ui/src/pages/BacktestPage.tsx`
  - Still old broad-only UI; Task 7 will rebuild it.
- `/home/jbl/projects/nba-ml-engine/tasks/lessons.md`
  - Contains relevant prior lessons:
    - SQL CASE branches join with spaces, not commas.
    - Materialized-view definition changes require DROP + CREATE.
    - History vs Backtest hit-rate discrepancy is population difference.
    - Composite stat predictions compound error and produce -EV portfolios.
</important_files>

<next_steps>
Immediate next step:
1. Fix Task 5 quality issues in `dashboard-ui/server/src/index.ts` with a focused subagent:
   - Validate/clamp `days`:
     ```ts
     const days = Math.min(Math.max(Number(req.query.days ?? 30) || 30, 1), 365)
     ```
     Use string only when encoding path/cache if needed:
     ```ts
     const daysParam = String(days)
     ```
     Cache key: `backtest:${days}`.
   - Sort `by_edge_size` semantically:
     ```ts
     const EDGE_BUCKET_ORDER = ['0-5%', '5-15%', '15-30%', '30%+']
     .sort((a, b) => EDGE_BUCKET_ORDER.indexOf(a.bucket) - EDGE_BUCKET_ORDER.indexOf(b.bucket))
     ```
   - Investigate `by_edge_abs` before changing:
     - Do not blindly remove it; prior live endpoint returned `by_edge_abs` data and `scripts/optimize_db.py` includes it.
     - Either leave it as optional support and add a comment that older migrations may not include it, or verify current production schema later during validation.
   - Validate:
     - `cd dashboard-ui && npx tsx --test server/src/dashboardContracts.test.ts`
     - `cd dashboard-ui && npm run build`
     - `cd dashboard-ui && npx eslint server/src/index.ts`
   - Commit message suggestion:
     - `fix: harden backtest proxy parameters`
     - Include Co-authored-by trailer.

2. Re-run Task 5 quality review after the fix.
   - If approved, mark `backtest-task-5` done and start Task 6.

Remaining planned tasks:
- Task 6: Update `dashboard-ui/src/lib/api.ts` React `BacktestData` types to canonical + broad diagnostic shape.
- Task 7: Rebuild `dashboard-ui/src/pages/BacktestPage.tsx`:
  - Canonical summary cards.
  - Accuracy notes/warnings.
  - Canonical P&L curve.
  - Reliability charts by stat, signal tier, edge bucket, direction, source.
  - Details table.
  - Broad Model Diagnostic section.
- Task 8: Targeted validation:
  - Python canonical/backend tests.
  - Compile checks.
  - BFF tests/build/lint.
  - Dashboard build.
- Task 9: Deploy `nba-ml-api` and `nba-ml-dashboard` using homelab compose with `.env` loaded.
- Task 10: Live validation and report:
  - Compare `/api/backtest` against `/api/props/history`.
  - Check broad diagnostic still appears separately.
  - Write `reports/2026-04-25-backtest-accuracy-page-status.md`.
  - Commit and push to GitHub.

Current response/action should likely continue from Task 5 quality failure by dispatching a fix subagent, not by answering final completion.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
