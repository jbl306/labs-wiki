---
title: "Copilot Session Checkpoint: Dashboard Accuracy Fixes"
type: text
captured: 2026-04-25T01:05:19.018133Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, mempalace, agents, dashboard]
checkpoint_class: durable-workflow
checkpoint_class_rule: "body:ci"
retention_mode: retain
status: success
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Dashboard Accuracy Fixes
**Session ID:** `39cb6a8f-14d7-43a7-bad1-98ec00e06033`
**Checkpoint file:** `/home/jbl/.copilot/session-state/39cb6a8f-14d7-43a7-bad1-98ec00e06033/checkpoints/001-dashboard-accuracy-fixes.md`
**Checkpoint timestamp:** 2026-04-25T00:58:58.398118Z
**Exported:** 2026-04-25T01:05:19.018133Z
**Checkpoint class:** `durable-workflow` (rule: `body:ci`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user first asked to evaluate `nba-dashboard.jbl-lab.com`, identify accuracy issues in “Today's Most Confident Predictions,” Props, and Production Model R² by Stat, then write and push a report. After the report was pushed, the user asked to implement the proposed fixes, evaluate the dashboard again, create a new report under `nba-ml-engine/reports`, and push it. The work is currently mid-implementation in an isolated git worktree; code changes build, focused tests pass, but lint has baseline and one touched-file issue remaining.
</overview>

<history>
1. The user asked to evaluate the NBA ML dashboard and write/push a report.
   - Loaded NBA project memory from MemPalace and relevant skills (`stealth-browser`, `writing-plans`, later `data-analyst`, `ml-engineer`, `writing-clearly-and-concisely`).
   - Tried to start stealth browser, but it failed because no Chrome binary was installed in the environment.
   - Pivoted to direct live HTTP/API inspection with `curl` against `https://nba-dashboard.jbl-lab.com`.
   - Inspected dashboard BFF and frontend code in `dashboard-ui/server/src/index.ts`, `DashboardPage.tsx`, `PropsPage.tsx`, `ModelsPage.tsx`, and API types.
   - Found:
     - `/api/dashboard` returned 8 models, 354 confident props, 10 featured predictions.
     - `/api/props` returned `props: []`, `stats: []`, `sources: []` for the same featured date.
     - `/api/models` returned nested metrics under `metrics.test_r2`, but `ModelsPage.tsx` expected top-level `test_r2`, `val_r2`, `stat_name`.
     - High confidence tier in `/api/props/history` hit only 48.86%, worse than Medium (52.95%) and Low (50.71%).
     - Model health and calibration were degraded: ECE 0.3661/0.4055, 21 drifted features, stale game logs.
   - Created `nba-ml-engine/reports/2026-04-24-dashboard-accuracy-audit.md`.
   - Committed and pushed report to `main` as commit `47a351b docs: add dashboard accuracy audit`.
   - Left pre-existing dirty file `.github/skills/nba-ml-pipeline/SKILL.md` untouched.
   - Recorded findings in MemPalace and diary.

2. The user asked to “implement the plan then evaluate again and push new report to github.”
   - Loaded `executing-plans`, `test-driven-development`, `frontend-developer`, `using-git-worktrees`, `subagent-driven-development`, and `homelab-deploy`.
   - Created implementation todos in SQL:
     - `fix-models-contract`
     - `unify-prop-picks`
     - `add-accuracy-warnings`
     - `validate-and-deploy`
     - `write-followup-report`
   - Created isolated worktree:
     - Path: `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-fixes`
     - Branch: `feature/dashboard-accuracy-fixes`
     - Base commit: `47a351b`
   - Ran `npm ci --quiet` in `dashboard-ui`.
   - Tried baseline `npm run typecheck`; failed because no `typecheck` script exists.
   - Ran baseline `npm run build`; it passed.
   - Added failing contract tests first, per TDD, in `dashboard-ui/server/src/dashboardContracts.test.ts`; initial run failed because `dashboardContracts.js` did not exist.
   - Implemented `dashboard-ui/server/src/dashboardContracts.ts`.
   - Re-ran focused tests; they passed.
   - Wired new contract/helpers into BFF and frontend.
   - Ran focused contract tests plus `npm run build`; both passed.
   - Ran `npm run lint`; it failed with several baseline errors and one touched-file error in `DashboardPage.tsx`.
</history>

<work_done>
Files created:
- `/home/jbl/projects/nba-ml-engine/reports/2026-04-24-dashboard-accuracy-audit.md`
  - First audit report; committed and pushed to `main` in commit `47a351b`.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-fixes/dashboard-ui/server/src/dashboardContracts.test.ts`
  - New Node test file for BFF/frontend contract logic.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-fixes/dashboard-ui/server/src/dashboardContracts.ts`
  - New shared helper module for model normalization, prop edge normalization, prop payload construction, confidence tiering, and type definitions.

Files modified in worktree:
- `dashboard-ui/server/src/index.ts`
  - Imports new contract helpers.
  - Removed local `EdgePolicy` interface and local `getConfidenceTier`.
  - Added shared prop-pick helpers:
    - `normalizeSqlPropRow`
    - `dedupePropPicks`
    - `summarizeEdgeByStat`
    - `queryBffFallbackPropPicks`
    - `getPropPicksForSlate`
    - `getAccuracyWarnings`
  - `/api/dashboard` now uses shared `getPropPicksForSlate()` instead of duplicated SQL for top picks/edge summary, and includes:
    - `prop_data_source`
    - `prop_empty_reason`
    - `accuracy_warnings`
  - `/api/props` now uses the same prop-pick source and `buildPropsPayload()`, surfaces `data_source` and `empty_reason`, and returns 502 on top-level route failure instead of silent empty success.
  - `/api/models` now returns `normalizeModelRecords(json)` so metrics are flattened.
  - `/api/rankings` confident props now use shared `getPropPicksForSlate()` and include source metadata.
- `dashboard-ui/src/lib/api.ts`
  - Extended API types to include normalized model metrics, model raw `metrics`, prop `edge_abs`, dashboard `accuracy_warnings`, and prop `data_source`/`empty_reason`.
- `dashboard-ui/src/pages/DashboardPage.tsx`
  - Renamed confidence language to “Model Signal.”
  - Added accuracy warning panel.
  - Shows SQL fallback badge when `prop_data_source === 'bff_sql_fallback'`.
  - Empty state uses `prop_empty_reason`.
- `dashboard-ui/src/pages/props/TodayTab.tsx`
  - Shows prop source and `empty_reason`.
  - Renamed “Confidence” column/copy to “Model Signal.”
- `dashboard-ui/src/pages/RankingsPage.tsx`
  - Renamed “Confident Props” UI to “Prop Signals.”
  - Adjusted chart labels/copy to “Model Signal.”
- `dashboard-ui/src/pages/ModelsPage.tsx`
  - Filters chart rows only when both `test_r2` and `val_r2` are null.
  - Allows string/nullable model versions.

Completed verification:
- `npx tsx --test server/src/dashboardContracts.test.ts` passed: 4 tests.
- `npm run build` passed after implementation.
- Baseline `npm run build` also passed before implementation.

Current issue:
- `npm run lint` failed. Many failures are pre-existing baseline issues in untouched files:
  - `FeatureDriftPanel.tsx`: `no-explicit-any`
  - `ModelHealthPanel.tsx`: `no-explicit-any`
  - `NavBar.tsx`: `react-hooks/set-state-in-effect`
  - `DataTable.tsx`: warning about incompatible library
  - `theme.tsx`: `react-refresh/only-export-components`
  - `PlayerPage.tsx`: conditional hook
  - `SeasonsPage.tsx`: memoization preservation errors
  - `server/src/index.ts`: pre-existing `getCurrentNbaSeason` unused and `no-constant-binary-expression` around line ~1180
- One touched-file lint issue is new or in touched area:
  - `src/pages/DashboardPage.tsx` line ~244: unnecessary escape character `\'`. Fix by replacing `"Today\\'s Games"`/escaped apostrophe with a normal apostrophe string or `Today&apos;s` as appropriate.

SQL todo statuses at compaction:
- `fix-models-contract`: done
- `unify-prop-picks`: done
- `add-accuracy-warnings`: done
- `validate-and-deploy`: in_progress
- `write-followup-report`: pending
- older audit todos: done
</work_done>

<technical_details>
- Environment:
  - Current root `/home/jbl/projects`, repo root `/home/jbl/projects/nba-ml-engine`.
  - Original checkout is dirty with unrelated `.github/skills/nba-ml-pipeline/SKILL.md`; do not touch/revert it.
  - Worktree path: `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-fixes`.
  - Worktree branch: `feature/dashboard-accuracy-fixes`.
- Dashboard stack:
  - React dashboard in `dashboard-ui/`.
  - Express/BFF in `dashboard-ui/server/src/index.ts`.
  - FastAPI backend in `src/api/server.py`.
  - Deployment likely via homelab `compose/compose.nba-ml.yml`; `NBA_ML_ENGINE_PATH` in homelab `.env.example` defaults to `../../nba-ml-engine`.
- Build/test commands:
  - No `npm run typecheck`.
  - Use:
    - `cd dashboard-ui && npx tsx --test server/src/dashboardContracts.test.ts`
    - `cd dashboard-ui && npm run build`
    - `cd dashboard-ui && npm run lint` (currently fails due baseline + one touched issue)
- Important live audit observations:
  - `/api/dashboard`: 8 models, 354 confident props, 10 best predictions.
  - Top predictions were implausible assist unders like Derrick White AST 4.5 predicted 0.00, confidence 99.97%.
  - `/api/props`: empty before fixes despite same date and joined dates.
  - `/api/models`: returned 58 models, 8 production models, but `stat_name`, `test_r2`, etc. were not top-level.
  - `/api/props/history`: High confidence hit rate was 48.86%, Medium 52.95%, Low 50.71%.
  - `/api/evaluation/calibration`: ECE 0.3661.
  - `/api/evaluation/model-health`: degraded, ECE 0.4055, 21 drifted features.
  - `/api/health/data`: game logs latest 2026-04-12, predictions 2026-04-24, prop lines 2026-04-26.
- Key implementation decision:
  - Instead of leaving duplicate prop-pick SQL in Overview/Rankings and FastAPI-only Props, centralize BFF access through `getPropPicksForSlate()`.
  - `getPropPicksForSlate()` tries canonical FastAPI `/prop-edges?game_date=...&min_edge=0&include_excluded=false`, normalizes rows, and falls back to BFF SQL if FastAPI fails.
  - BFF SQL fallback remains labeled as `bff_sql_fallback`, so the UI can warn users.
  - Dashboard uses the shared prop pick result for:
    - count
    - best predictions
    - edge summary
  - Props Today and Rankings also use the same shared result.
- Contract helper behavior:
  - `normalizeModelRecord(raw)` flattens `metrics.val_r2`, `metrics.test_r2`, `metrics.val_mae`, etc. onto top-level fields.
  - Derives `stat_name` from `model_name` suffix, e.g. `EnsembleModel_fg3m` -> `fg3m`.
  - Derives `model_family`, e.g. `EnsembleModel_fg3m` -> `EnsembleModel`.
  - `normalizeFastApiPropEdge(raw, resolvedDate)` maps FastAPI fields (`stat`, `predicted`, `edge`, `confidence`) to UI fields (`stat_name`, `predicted_value`, `edge_pct`, `confidence_score`, `edge_abs`, `call`, `direction`, `odds`).
  - `buildPropsPayload()` adds `data_source` and `empty_reason`.
- Lint gotchas:
  - Lint is not currently clean on baseline; do not fix broad unrelated lint issues unless necessary.
  - Need to fix touched-file lint issue in `DashboardPage.tsx` before continuing.
  - There are server lint errors in touched `index.ts`, but at least two were pre-existing:
    - `getCurrentNbaSeason` unused existed before.
    - `no-constant-binary-expression` likely pre-existing around `/api/seasons`.
    - `settledMap` prefer-const was introduced/touched in `/api/props`; change `let settledMap` to `const settledMap`.
- Deployment:
  - Homelab-deploy skill was loaded because the user wants live evaluation after implementation.
  - Need read homelab refs if proceeding with deployment; at least `homelab/compose/docker-compose.yml` and `homelab/.env.example` were already read.
  - No deployment has been done yet.
- No browser evaluation:
  - Stealth browser failed earlier due no Chrome binary:
    - `FileNotFoundError: could not find a valid chrome browser binary`.
  - Continue using direct endpoint checks unless Chrome becomes available.
</technical_details>

<important_files>
- `/home/jbl/projects/nba-ml-engine/reports/2026-04-24-dashboard-accuracy-audit.md`
  - First pushed report and implementation plan basis.
  - Contains P0/P1 fixes, live evidence, acceptance checks.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-fixes/dashboard-ui/server/src/dashboardContracts.ts`
  - New central contract helper module.
  - Defines `EdgePolicy`, `NormalizedModelRecord`, `NormalizedPropRecord`, `PropsPayload`.
  - Implements `normalizeModelRecord(s)`, `normalizeFastApiPropEdge`, `buildPropsPayload`, `getConfidenceTier`, `numberOrNull`.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-fixes/dashboard-ui/server/src/dashboardContracts.test.ts`
  - New TDD contract tests.
  - Tests model metric flattening, prop edge normalization, prop payload metadata, confidence tier boundaries.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-fixes/dashboard-ui/server/src/index.ts`
  - Main BFF.
  - Major changes around:
    - imports at top,
    - helper section after `getFeaturedPropSlate()`,
    - `/api/dashboard`,
    - `/api/props`,
    - `/api/models`,
    - `/api/rankings`.
  - Needs lint fixes: `let settledMap` -> `const`; consider not touching unrelated baseline errors unless required.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-fixes/dashboard-ui/src/lib/api.ts`
  - Frontend API type contract.
  - Updated for normalized model fields, prop metadata, dashboard warnings.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-fixes/dashboard-ui/src/pages/DashboardPage.tsx`
  - UI changes for “Model Signal,” accuracy warnings, fallback badge, empty reason.
  - Has current lint error around escaped apostrophe line ~244.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-fixes/dashboard-ui/src/pages/props/TodayTab.tsx`
  - Props Today UI now shows `data_source`, `empty_reason`, and “Model Signal” copy.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-fixes/dashboard-ui/src/pages/RankingsPage.tsx`
  - Confident Props renamed to Prop Signals; shared source metadata returned by BFF.
- `/home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-fixes/dashboard-ui/src/pages/ModelsPage.tsx`
  - Uses normalized top-level model fields.
  - Chart should now render valid production bars when live `/api/models` is normalized.
- `/home/jbl/projects/homelab/compose/docker-compose.yml`
  - Homelab stack include list; includes `compose.nba-ml.yml`.
- `/home/jbl/projects/homelab/.env.example`
  - Shows `NBA_ML_ENGINE_PATH=../../nba-ml-engine` and NBA ML env vars.
</important_files>

<next_steps>
Immediate next steps:
1. Fix touched-file lint issues:
   - In `DashboardPage.tsx`, remove unnecessary escaped apostrophe near line ~244.
   - In `dashboard-ui/server/src/index.ts`, change `let settledMap` to `const settledMap`.
2. Re-run:
   - `cd /home/jbl/projects/nba-ml-engine/.worktrees/dashboard-accuracy-fixes/dashboard-ui && npx tsx --test server/src/dashboardContracts.test.ts`
   - `npm run build`
   - Optionally `npm run lint`; expect baseline failures to remain. Note which failures are pre-existing versus touched.
3. Inspect diff carefully:
   - `git status --short`
   - `git diff --check`
   - `git diff --stat`
4. Deploy or stage for live evaluation:
   - Need determine deployment method. Likely sync/merge worktree changes back or push branch, then deploy homelab `nba-ml` stack using existing scripts.
   - Since user asked to evaluate again live, deployment is needed before live endpoint re-check unless testing against local BFF connected to production DB is available.
5. Re-evaluate endpoints after deployment:
   - `/api/dashboard`
   - `/api/props`
   - `/api/models`
   - `/api/rankings`
   - `/api/evaluation/model-health`
   - `/api/health/data`
   - Check:
     - Props no longer empty when dashboard shows prop signals.
     - `/api/models` has top-level `stat_name`, `test_r2`/`val_r2` for production models.
     - Dashboard exposes `accuracy_warnings`.
     - `prop_data_source` is visible and honest.
6. Write follow-up report under `reports/`, likely e.g. `reports/2026-04-24-dashboard-accuracy-fixes-reevaluation.md`.
7. Commit with required trailer:
   - `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`
8. Push to GitHub.
9. Record MemPalace findings/diary at end.

Open blockers/questions:
- Need decide exact deployment path and whether to merge branch to `main` before deploying. The original main checkout is dirty with unrelated `.github/skills/nba-ml-pipeline/SKILL.md`; avoid touching it.
- Lint baseline is dirty; do not claim lint passes unless it actually does. It currently does not.
- Live evaluation cannot use stealth browser unless Chrome is installed; use endpoint contracts via `curl`.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
