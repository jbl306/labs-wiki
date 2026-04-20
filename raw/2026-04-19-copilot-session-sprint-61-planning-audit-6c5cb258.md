---
title: "Copilot Session Checkpoint: Sprint 61 planning + audit"
type: text
captured: 2026-04-19T22:53:41.892067Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine]
checkpoint_class: project-progress
checkpoint_class_rule: "title:sprint 61"
retention_mode: compress
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint 61 planning + audit
**Session ID:** `af2982d2-180f-4871-ab07-ba61d03faf7d`
**Checkpoint file:** `/home/jbl/.copilot/session-state/af2982d2-180f-4871-ab07-ba61d03faf7d/checkpoints/006-sprint-61-planning-audit.md`
**Checkpoint timestamp:** 2026-04-19T22:45:37.945858Z
**Exported:** 2026-04-19T22:53:41.892067Z
**Checkpoint class:** `project-progress` (rule: `title:sprint 61`)
**Retention mode:** `compress`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
Sprint 61 on the NBA ML Engine. Sprint 60 (PR #44) was already merged; the user asked to "merge sprint 60 branch to main and implement sprint 61." Goal: lift predictions across stat categories, but most Sprint 60 next-steps are blocked (no retrain yet — next is 2026-04-24, Odds API budget exhausted till May). Strategy: focus on items that don't require a retrain — STL edge-threshold audit, PTS-specific feature interactions (code-only, takes effect at next retrain), `pickle_load` audit across all base-model classes, optional Tier C SHAP polish.
</overview>

<history>
1. User asked: merge sprint 60 + implement sprint 61. Loaded skill.
   - Verified state: sprint 60 already merged (PR #44, commit `75c50ab` on main).
   - Found dirty worktree: `src/api/server.py`, `src/training/status.py`, `tests/test_training_status.py` — unrelated WIP. Stashed as "WIP training-status before sprint 61".
   - Ran DQ gate: 138 historical tz_mismatch (known prior issue), 0 zero_lines, 4168 predictions today. Clean.
   - Audited remaining `pickle.load`/`pickle.dump` sites: ~15 across `src/models/` (lightgbm, catboost, xgboost, ridge, random_forest, minutes, over_under) + `src/evaluation/calibration.py` (3 dump+load pairs).
   - Audited `config.py` thresholds for STL: edge 0.005, abs 0.3, max_abs 2.0 (already permissive).
   - Conversation compacted before plan was written.
</history>

<work_done>
Files modified this session: **none** (only stash performed).
Files stashed: src/api/server.py, src/training/status.py, tests/test_training_status.py (WIP, NOT sprint 61 scope).

Work completed:
- [x] Skill loaded
- [x] Verified main has Sprint 60 merged
- [x] Stashed unrelated WIP
- [x] DQ gate (clean except known historical 138 tz rows)
- [x] Audit: pickle sites enumerated, STL thresholds inspected
- [ ] Sprint 61 branch
- [ ] Plan + tracker
- [ ] SQL todos seeded
- [ ] Implementation
- [ ] Tests, deploy, report, lessons, PR
</work_done>

<technical_details>
- **Environment**: server (`beelink-gti13`). Sprint 60 PR #44 merged. Latest main = `75c50ab`.
- **Blocked Sprint 61 items**: A.1 backtest (no retrain till 2026-04-24), A.2 model re-selection (needs retrain), B.4 Odds API expansion (budget exhausted till May), B.5 PRA/DD/TD ingestion (depends on B.4).
- **Actionable Sprint 61 items**:
  - **D.8 — pickle_load audit**: refactor every `pickle.load(f)` site in `src/models/` and `src/evaluation/calibration.py` to use the `src.models._io.pickle_load` helper. ~10 base-model sites + 3 calibration sites. Requires only a tiny edit per file plus removing the now-unused `import pickle` lines where possible.
  - **D.9 — PTS feature interactions**: add `usage × pace_factor`, `home × usage`, `rest × usage` (and possibly `usage × opportunity_boost`). Lives in `src/features/builder.py:_add_context_features` (~line 482-505) but `gadv_usg_pct` isn't available there — must add as new function called after `_add_game_advanced_rolling` like Sprint 60's `_add_teammate_out_usage_share` did. **CRITICAL**: do not repeat the Sprint 60 ordering trap.
  - **A.3 — STL edge-threshold audit**: STL hit 64.6% on 478 bets last 60d. Suggests filters too tight, leaving prediction volume on table. Investigate whether lowering `STAT_EDGE_ABSOLUTE['stl']` from 0.3 → 0.2 (its prior value) increases bet count without crashing hit rate. Pure config + backtest.
  - **C.6 — SHAP timing budget**: only matters if nightly ensemble SHAP runs.
  - **C.7 — meta-ridge weight surfacing**: surface meta-ridge weight in `scripts/shap_analysis.py:_shap_values_ensemble`.

- **Sprint 60 lessons to avoid repeating**:
  - Feature-builder ordering: any new feature using `gadv_usg_pct` must run after `_add_game_advanced_rolling` (line 90 in build_features).
  - Don't add stats to CLASSIFIER_STATS without checking `prop_lines` has rows for that stat.

- **Quirks**:
  - `predictions` table has NO `confidence_score` column — only `confidence_low/high`. Calibration audit must use derived signals.
  - `pickle_load` helper from Sprint 60 is at `src/models/_io.py:25` (or thereabouts after sprint 60 edit).
  - `prop_lines` has no id column (composite key).
  - Deploy: `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache <svc>`.

- **Open questions**:
  - Does the user want the off-cycle retrain to materialize Sprint 60+61 features now, or wait for 2026-04-24? Default: wait.
  - Should STL audit just be a report finding, or should config be edited this sprint? Default: edit if backtest supports it.
</technical_details>

<important_files>
- `docs/reports/sprint60-results.md`
   - Sprint 61 source — defines all next-step items (Tier A.1-3, B.4-5, C.6-7, D.8-9).

- `src/features/builder.py`
   - Workstream for D.9 PTS interactions. Lines 90 (where `gadv_usg_pct` becomes available) and 686+ (where `_add_teammate_out_usage_share` template lives).

- `src/models/_io.py`
   - Already exposes `pickle_load` (Sprint 60). Source for D.8 refactor.

- Files to edit for D.8 (pickle_load audit):
   - `src/models/lightgbm_model.py:137`
   - `src/models/catboost_model.py:97`
   - `src/models/xgboost_model.py:154`
   - `src/models/ridge_model.py:88`
   - `src/models/random_forest_model.py:84`
   - `src/models/minutes_model.py:153`
   - `src/models/over_under_model.py:180`
   - `src/evaluation/calibration.py:289, 445, 661` (load sites)

- `config.py:189-231`
   - STL thresholds for A.3 audit. Edit `STAT_EDGE_ABSOLUTE['stl']` and `STAT_EDGE_THRESHOLDS['stl']` if backtest supports.

- `scripts/shap_analysis.py`
   - Tier C.7 meta-ridge weight surfacing in `_shap_values_ensemble`.

- `~/projects/homelab/compose/compose.nba-ml.yml`
   - Deploy target if any cron change needed (likely none for Sprint 61).

- Files NOT yet created:
   - Sprint 61 branch `feature/sprint-61-pickle-audit-pts-interactions`
   - `tasks/PROGRESS-sprint61-pts-interactions-0419.md`
   - `tests/test_sprint61.py`
   - `docs/reports/sprint61-results.md`

- Stashed (DO NOT TOUCH this sprint):
   - WIP `src/api/server.py`, `src/training/status.py`, `tests/test_training_status.py` — different feature, recover with `git stash pop` later.
</important_files>

<next_steps>
Immediate:
1. Create branch `feature/sprint-61-pickle-audit-pts-interactions`.
2. Seed plan.md + SQL todos: s61-pickle-load-audit, s61-pts-interactions, s61-stl-threshold-audit, s61-meta-ridge-shap, s61-tests, s61-deploy, s61-report, s61-lessons, s61-pr.
3. **D.8 pickle_load audit** — TDD: test that `pickle.load(f)` doesn't appear at module scope in any base model file (similar to Sprint 60 ensemble check). Then replace each load site with `pickle_load(path)` call, drop top-level `import pickle` where unused.
4. **D.9 PTS interactions** — Add new function `_add_usage_interactions(df)` called after `_add_game_advanced_rolling` (and `_add_teammate_out_usage_share`). Adds `usage_x_pace_factor`, `home_x_usage`, `rest_x_usage`, `usage_x_opportunity_boost`. Tests for column presence + finite + arithmetic.
5. **A.3 STL audit** — Run a SQL backtest at threshold 0.2 vs 0.3 abs; if 0.2 keeps hit rate >55% with materially more volume, edit config.
6. **C.7 meta-ridge SHAP** (optional, time permitting).
7. Tests, deploy api (no retrain), Ofelia unchanged, report, lessons, PR + merge.
8. Restore stashed WIP after sprint closes (`git stash pop`).

Blockers: A.1/A.2 deferred to Sprint 62 post-retrain; B.4/B.5 deferred to May.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
