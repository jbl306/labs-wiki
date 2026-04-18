---
title: "Copilot Session Checkpoint: Sprint 56 no-retrain fixes planning"
type: text
captured: 2026-04-18T01:36:58.581806Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, dashboard]
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint 56 no-retrain fixes planning
**Session ID:** `af2982d2-180f-4871-ab07-ba61d03faf7d`
**Checkpoint file:** `/home/jbl/.copilot/session-state/af2982d2-180f-4871-ab07-ba61d03faf7d/checkpoints/001-sprint-56-no-retrain-fixes-pla.md`
**Checkpoint timestamp:** 2026-04-16T21:20:27.316130Z
**Exported:** 2026-04-18T01:36:58.581806Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
User asked for a comprehensive ML engine + dashboard review, focusing on increasing prediction hit rates across stat categories. A review report was created and merged (branch now deleted, only `main`). Current task is Sprint 56: implement no-retrain items from `docs/reports/comprehensive-ml-review_0416.md`, document that the Odds API monthly limit is exhausted, and defer retrain-requiring items to "next steps" in a sprint results report.
</overview>

<history>
1. User asked to review sprint reports under `docs/reports/`, do an independent review focused on raising hit rate, create a report, and push to GitHub.
   - Read `sprint55-results.md`, `comprehensive-ml-review_0413.md`, `sprint54-pipeline-resilience.md`.
   - Queried live production state: containers, `mv_daily_hit_rates`, `model_registry`, `feature_importance_snapshots`, `prop_line_snapshots`, `predictions`, scheduler logs.
   - Found 7 new issues (§N1-N7) beyond the April 13 review, including missing `minutes_model.pkl`, missing ensemble pkls for PTS/AST/FG3M from today's 2026-04-16 retrain, `fg_pct`/`ft_pct` still in production despite R1, feature importance Kendall τ instability across all stats, 21 drifted features, Odds API still 401, PRA composite dragging portfolio, 7h36m daily pipeline runtime.
   - Wrote `docs/reports/comprehensive-ml-review_0416.md` with Phase 0/1/2/3 prioritized plan.
   - Pushed to branch `review/comprehensive-2026-04-16` on GitHub.

2. User said the PR was merged (only `main` exists now), Odds API monthly limit is exhausted (document it), and asked to implement the no-retrain items from the 04-16 report, deferring the rest to next steps. Invoked the `execute-sprint-from-report` skill.
   - Synced main, created `feature/sprint-56-no-retrain-fixes` branch.
   - Created progress tracker `tasks/PROGRESS-sprint56-no-retrain-fixes-0416.md`.
   - Inserted 6 todos into the session SQL DB.
   - Identified Phase 0 tasks: P0-1 disable PRA, P0-2 minutes model + artifact↔registry validation, P0-3 retire fg_pct/ft_pct, P0-4 document Odds API quota exhaustion, P0-5 trainer artifact gate.
   - Audited code locations: PRA composite at `src/inference/predictor.py:472-497`, exclusion policy at `src/applications/edge_policy.py`, startup hook at `src/api/server.py:95-123` lifespan, minutes training save at `src/training/trainer.py:394-395`, `_register_minutes_model` at `:412-430`, best-model registration at `:985-998`, predictor fallback at `src/inference/predictor.py:124-218`.
   - Confirmed `/opt/homelab/data/nba-ml/models/minutes/` directory is empty on host (no pkl anywhere) — so restoring minutes requires a minutes-only retrain (deferred to next steps).
   - Found dashboard fallback edge policy with `fg_pct`/`ft_pct` at `dashboard-ui/server/src/index.ts:28-43`.
   - Compaction triggered before implementation was started.
</history>

<work_done>
Files created:
- `docs/reports/comprehensive-ml-review_0416.md` (merged to main via prior branch)
- `tasks/PROGRESS-sprint56-no-retrain-fixes-0416.md` (sprint tracker)

Branch state:
- On `feature/sprint-56-no-retrain-fixes`, clean working tree (no code edits yet).
- Only tracker + SQL todos exist.

Work completed:
- [x] Comprehensive review report written, pushed, merged
- [x] Sprint 56 branch + tracker created
- [x] Audit of all affected code paths done
- [ ] P0-1 Disable PRA betting (code edits pending)
- [ ] P0-2 Artifact↔registry validator + demote stale MinutesModel_minutes to is_production=false
- [ ] P0-3 Retire fg_pct/ft_pct in production + remove from STAT_EDGE_* maps + dashboard fallback
- [ ] P0-4 Document Odds API monthly quota exhausted in results report
- [ ] P0-5 Post-training artifact validation gate in `trainer.py::register_best_model`
- [ ] Tests, pytest, deploy, verify, results report, lessons, PR
</work_done>

<technical_details>
- **Environment:** hostname `beelink-gti13` — server mode, operate directly. Env vars at `~/projects/homelab/.env`, `HOMELAB_BASE=/opt/homelab`, DB on `nba-ml-db` container port 5433 host / 5432 container. Access DB only via `docker exec nba-ml-db psql -U nba_ml -d nba_ml -c "..."` (host has no psql). Use `--env-file .env` for compose commands.
- **Prop snapshots have no `hit` column** — outcome stored in `result` column and `actual_value`; use `mv_daily_hit_rates` matview instead.
- **`feature_importance_snapshots` column is `trained_at`** (NOT `snapshot_date`) and `model_name` (not `model_type`). Current τ values: stl=0.18, blk=0.35, tov=0.34, reb=0.38, pts=0.42, fg3m=0.45, ast=0.59 — all below 0.70.
- **PRA composite** is written in `src/inference/predictor.py:472-497` inside `store_predictions` after regular preds. Just skip the whole block when `'pra' in EXCLUDED_PROP_STATS`.
- **EXCLUDED_PROP_STATS cascades automatically** through `src/applications/edge_policy.py:46`, `src/evaluation/backtester.py:184-185,523`, `src/evaluation/edge_optimizer.py:90,165`. Adding `'pra'` to it handles most surfaces.
- **Minutes model pkl is missing everywhere** — not in container, not in `/opt/homelab/data/nba-ml/models/minutes/` (directory exists but empty). The registry entry `MinutesModel_minutes` version `20260413_115221` points at `/app/models/minutes/minutes_model.pkl` which does not exist. Fix path: SQL update to set `is_production=false` (restore is next-steps since it needs a minutes-only retrain, user said no retrains).
- **Model registry does NOT have `stat_name` column** — use `config_snapshot->>'stat'` or parse from `model_name` suffix pattern `<Model>Model_<stat>`.
- **Production promotion** happens in `src/training/trainer.py:976-998` inside `register_best_model`. Add artifact existence check right before line 985 (`entry = ModelRegistry(...)`). Skip promotion (keep previous) when `artifact_path` doesn't exist.
- **Lifespan hook** (`src/api/server.py:95-123`) is where to add the startup artifact validator — query all `is_production=True` entries, check `artifact_path` exists, log ERROR + count with a Prometheus metric if possible.
- **Dashboard fallback edge policy** at `dashboard-ui/server/src/index.ts:28-43` has a suspicious `excluded_stats: ['fg_pct', 'ft_pct', 'pts', 'ast']` — `pts` and `ast` should NOT be excluded; this may be stale/buggy. Add `'pra'` and clean up.
- **Tests**: suite is pytest-based, `.venv/bin/python -m pytest`. 346 tests pass post-Sprint 55. Test files named `tests/test_sprint<N>.py` by convention. Create `tests/test_sprint56.py`.
- **Git commit trailer required:** `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`
- **Deployment:** `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache <service> && up -d <service>`. Affected services: `nba-ml-api`, `nba-ml-dashboard`, `nba-ml-scheduler`.
- **Odds API status (per user):** monthly limit exhausted — just mark in report, no code change.
</technical_details>

<important_files>
- `docs/reports/comprehensive-ml-review_0416.md` — source of truth for Sprint 56 tasks. Phase 0 § enumerates P0-1 through P0-5.
- `tasks/PROGRESS-sprint56-no-retrain-fixes-0416.md` — sprint tracker, task list.
- `config.py` (lines 146, 200-232) — `CLASSIFIER_STATS`, `EXCLUDED_PROP_STATS`, `STAT_EDGE_THRESHOLDS`, `STAT_EDGE_ABSOLUTE`, `STAT_EDGE_MAX_ABSOLUTE`. Add `'pra'` to `EXCLUDED_PROP_STATS`; remove `fg_pct`/`ft_pct` entries from stat maps.
- `src/inference/predictor.py`
  - `:124-218` — `_load_production_models` + `_try_fallback_model`. Already does per-entry fallback; we'll extend with a validator summary.
  - `:472-497` — PRA composite write. Gate on `'pra' not in config.EXCLUDED_PROP_STATS`.
- `src/training/trainer.py`
  - `:394-406` — minutes model save/register.
  - `:412-430` — `_register_minutes_model`. Add artifact existence check before setting `is_production=True`.
  - `:976-998` — `register_best_model` final block. Add artifact existence check before registry insert.
- `src/api/server.py:95-123` — lifespan hook. Add `validate_production_artifacts()` call that logs ERROR per missing pkl and totals.
- `src/applications/edge_policy.py` — cascades `EXCLUDED_PROP_STATS`; no change needed but verify behavior.
- `dashboard-ui/server/src/index.ts:28-43` — `FALLBACK_EDGE_POLICY`. Add `'pra'` to `excluded_stats`, remove spurious `'pts'`/`'ast'` from excluded_stats (verify with user or keep conservative), consider removing `fg_pct`/`ft_pct` thresholds.
- `dashboard-ui/src/components/charts/FeatureImportancePanel.tsx:35` and `ImportanceComparisonPanel.tsx:36,46` — remove PRA option from dropdowns.
- `tests/test_sprint56.py` (to create) — tests for PRA exclusion, artifact validator, trainer gate.
- `tasks/lessons.md` — append lessons after sprint completion.
</important_files>

<next_steps>
Remaining work (in order):

1. **P0-1 Disable PRA:**
   - Edit `config.py`: add `'pra'` to `EXCLUDED_PROP_STATS` default.
   - Edit `src/inference/predictor.py:472-497`: skip PRA composite write when PRA in `EXCLUDED_PROP_STATS`.
   - Edit `dashboard-ui/server/src/index.ts` fallback policy, `FeatureImportancePanel.tsx`, `ImportanceComparisonPanel.tsx` — remove PRA entries.
   - SQL cleanup (live DB): `DELETE FROM predictions WHERE stat_name='pra' AND game_date >= CURRENT_DATE` to stop dashboard surfacing pending pra bets; refresh matviews.
   - Test.

2. **P0-3 Retire fg_pct/ft_pct:**
   - Edit `config.py`: remove `fg_pct`/`ft_pct` keys from `STAT_EDGE_THRESHOLDS`, `STAT_EDGE_ABSOLUTE`.
   - SQL: `UPDATE model_registry SET is_production=false WHERE model_name IN ('EnsembleModel_fg_pct','EnsembleModel_ft_pct')`.
   - Optional: `DELETE FROM predictions WHERE stat_name IN ('fg_pct','ft_pct') AND game_date >= CURRENT_DATE`.
   - Remove from dashboard fallback thresholds map.

3. **P0-2 Minutes demote + artifact validator:**
   - Add `validate_production_artifacts(session) -> list[tuple[str,Path]]` helper (location: new module `src/inference/registry_validator.py` or add to predictor). Call from `src/api/server.py` lifespan and log ERRORs + summary count.
   - SQL: `UPDATE model_registry SET is_production=false WHERE model_name='MinutesModel_minutes'` (since pkl missing; predictor already has median fallback via feature pipeline).
   - Tests.

4. **P0-5 Trainer artifact gate:**
   - In `src/training/trainer.py::register_best_model` (~line 982), before creating the `ModelRegistry` entry, check `Path(artifact_path).exists()`; if missing, log ERROR and `return` without demoting the prior production entry. Same pattern in `_register_minutes_model`.
   - Test with mocked path.

5. **P0-4 Document Odds API:** only affects results report — note monthly quota exhausted, renewal deferred to next billing cycle.

6. **Validation:**
   - Run `.venv/bin/python -m pytest tests/test_sprint56.py tests/test_sprint55.py tests/test_predictor.py` then full suite.
   - Rebuild + redeploy `nba-ml-api`, `nba-ml-scheduler`, `nba-ml-dashboard` containers.
   - Verify no PRA/fg_pct/ft_pct in today's predictions; artifact validator logs no errors after minutes demotion.

7. **Reporting:**
   - Write `docs/reports/sprint56-results.md` (follow sprint55 format). Include Odds API quota note in Executive Summary. Put P1-1..P1-5 + Phase 2/3 under "Next Steps (require retrain)".
   - Append 2-3 lessons to `tasks/lessons.md` (e.g., "production registry entries can silently drift from on-disk artifacts", "minutes model pkl must be persisted on homelab volume").
   - Commit, push, open PR, merge.

Immediate next action on resume: start with P0-1 (smallest, unblocks testing), then batch P0-3 alongside it since they touch overlapping files.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
