---
title: "Copilot Session Checkpoint: Sprint 58 SHAP bug planning"
type: text
captured: 2026-04-18T01:36:58.581806Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine]
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint 58 SHAP bug planning
**Session ID:** `af2982d2-180f-4871-ab07-ba61d03faf7d`
**Checkpoint file:** `/home/jbl/.copilot/session-state/af2982d2-180f-4871-ab07-ba61d03faf7d/checkpoints/003-sprint-58-shap-bug-planning.md`
**Checkpoint timestamp:** 2026-04-17T11:33:14.673283Z
**Exported:** 2026-04-18T01:36:58.581806Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
Sprint 58 work on NBA ML Engine: fix a SHAP-analysis bug introduced by schema drift, and implement Sprint 57's remaining next-steps that don't require another retrain. The user ran the weekly retrain successfully (atomic save hardening shipped in Sprint 57 worked — all 7 ensemble pkls landed on disk); only fallout was post-training SHAP skipped due to `ModelRegistry.stat_name` attribute error. Approach: fix SHAP dispatch, apply atomic-save defense to every base model, add a registry-health cron, verify prediction volume after tonight's refresh.
</overview>

<history>
1. User invoked `/execute-sprint-from-report` with: "i ran the weekly retrain. it completed with a non-fatal warning that post-training SHAP analysis was skipped due to ModelRegistry lacking stat_name. fix this bug and implement sprint 57 items."
   - Invoked the `execute-sprint-from-report` skill.
   - Verified git state: on `main`, Sprint 57 PR #41 merged as `d1644a3`.
   - Inspected post-retrain state:
     - All 7 ensemble pkls exist on disk (atomic save worked).
     - `_register_best_model` picked Ridge for pts/ast/fg3m (lower val_mse), Ensemble for reb/blk/tov, CatBoost for stl — legitimate selection, not drift.
     - `validate_production_artifacts` green at startup: 8 production models loaded.
   - Found the SHAP bug in `scripts/shap_analysis.py::load_production_model`:
     a. `ModelRegistry.stat_name` doesn't exist — stat is encoded in `model_name` suffix (`EnsembleModel_pts`).
     b. `model_row.model_path` doesn't exist — real column is `artifact_path`.
     c. `joblib.load(pkl)` returns a dict (all model classes save `{model, feature_names, params, residuals}` via custom `.save()`), not a raw regressor; `shap.TreeExplainer(dict)` would fail even if (a)/(b) were fixed.
   - Created branch `feature/sprint-58-shap-bug-next-steps` off main.
   - Wrote progress tracker `tasks/PROGRESS-sprint58-shap-bug-0417.md`.
   - Seeded 11 SQL todos (`s58-*`, `s58-shap-fix` marked `in_progress`).

   Compaction occurred before any source code was edited.
</history>

<work_done>
Files created:
- `tasks/PROGRESS-sprint58-shap-bug-0417.md` — Sprint 58 progress tracker with root cause, scope, task list.

Files not yet modified (all pending):
- `scripts/shap_analysis.py`
- `src/models/{catboost,xgboost,lightgbm,random_forest,ridge}_model.py`
- `tests/test_sprint58.py` (to be created)
- `~/projects/homelab/compose/compose.nba-ml.yml` (Ofelia cron label)
- `docs/reports/sprint58-results.md` (to be created)
- `tasks/lessons.md` (append)

Work completed:
- [x] Verify retrain actually succeeded (ensembles on disk, registry consistent)
- [x] Root-cause SHAP bug (3 issues, not 1)
- [x] Create Sprint 58 branch
- [x] Progress tracker
- [x] Seed SQL todo table with 11 tasks
- [ ] Fix SHAP `load_production_model` — filter by `model_name.like("%_{stat_name}")`, read `artifact_path`, dispatch to class-specific `.load()`, pass inner `.model` to TreeExplainer
- [ ] Graceful skip for non-tree models (Ridge, Ensemble) in SHAP
- [ ] Atomic save (tmp+fsync+replace) for CatBoost/XGBoost/LightGBM/RandomForest/Ridge
- [ ] Ofelia cron job for `validate_production_artifacts`
- [ ] `tests/test_sprint58.py`
- [ ] Full pytest
- [ ] Deploy + retry SHAP against real registry
- [ ] Live prediction-volume delta verification (tonight's 22:15 UTC `predict-refresh`)
- [ ] `docs/reports/sprint58-results.md`
- [ ] Append lessons
- [ ] PR + merge
</work_done>

<technical_details>
- **Post-retrain registry state (2026-04-17 02:53 version)**: EnsembleModel_{blk,reb,tov}, CatBoostModel_stl, RidgeModel_{pts,ast,fg3m}, MinutesModel_minutes. The Ridge wins are legitimate (lower val_mse) — NOT a drop from the round-trip gate. All 7 ensemble pkls exist on disk; atomic save from Sprint 57 worked correctly.

- **`ModelRegistry` schema** (`src/db/models.py:306-323`): columns are `id, model_name, version, trained_at, metrics (JSONB), artifact_path, is_production, config_snapshot`. There is **no** `stat_name` or `model_path` column. Stat is inferred from the `model_name` suffix (e.g. `EnsembleModel_pts` → `pts`).

- **Custom save format**: every model class (CatBoost, XGBoost, LightGBM, RandomForest, Ridge, Ensemble) pickles a dict (`{"model": ..., "feature_names": ..., "params": ..., "residual_lower/upper": ..., "residuals": ...}`) — not a raw sklearn estimator. So `joblib.load(pkl)` returns a dict, breaking any caller that expects a regressor. Must go through the class's `.load(path)` which sets `self.model`, `self.feature_names`, etc. Then pass `instance.model` to SHAP for tree-based explainers. `RidgeModel` and `EnsembleModel` are not supported by `TreeExplainer` — need to skip with a warning.

- **Model class resolution from `model_name`**: format is `<ClassName>_<stat>`. Build a lookup dict from `src.training.trainer.MODEL_CLASSES` (plus `EnsembleModel`, `MinutesModel`) keyed by `__name__`.

- **Atomic save pattern** (established Sprint 57 in `src/models/ensemble.py:189`):
  ```python
  fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
  tmp_path = Path(tmp_name)
  try:
      with os.fdopen(fd, "wb") as f:
          pickle.dump(payload, f); f.flush(); os.fsync(f.fileno())
      os.replace(tmp_path, path)
  except Exception:
      try: tmp_path.unlink()
      except FileNotFoundError: pass
      raise
  ```
  Apply verbatim to the base models. Their `save()` methods already pickle a dict into `open(path, "wb")`, so the change is minimal.

- **Weekly retrain cadence** (from homelab compose):
  - `pipeline-daily` — daily ingest/features/train/predict
  - `props-refresh` 22:00 UTC — re-fetch SGO props
  - `predict-refresh` 22:15 UTC — re-run predictions with fresh props
  - Sprint 58 needs to verify prediction volume increased after today's 22:15 run, since the ensemble fallback chain is now healthy.

- **Odds API quota exhausted** (carryover from Sprint 57 — will self-heal on monthly billing reset; no action needed).

- **Deployment pattern** (from memory + Sprint 57):
  ```
  cd ~/projects/homelab
  docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache nba-ml-api
  docker compose --env-file .env -f compose/compose.nba-ml.yml up -d nba-ml-api
  ```
  Ofelia scheduler runs `python main.py pipeline` via `docker exec nba-ml-api`, so rebuilding `nba-ml-api` is sufficient for scheduled jobs to pick up new code.

- **SHAP constraint**: `shap.TreeExplainer` supports XGBoost, LightGBM, CatBoost, RandomForest. Does NOT support Ridge (linear) or the custom EnsembleModel (meta-learner + fold base models). Plan is to skip gracefully, returning a stub result with `"skipped": True` and a reason.

- **Pytest command**: `.venv/bin/python -m pytest -x -q --ignore=tests/test_api_auth.py` — `test_api_auth` has a pre-existing failure unrelated to this sprint.

- **Sprint 57 Next-Steps re-classified**: #1 (full retrain) is DONE by user's weekly run. #2 (Odds API) unchanged. #3 (atomic base save), #4 (reconciliation cron), #5 (prediction volume) are in scope for Sprint 58.
</technical_details>

<important_files>
- `scripts/shap_analysis.py`
  - Primary fix target — lines 32-61 (`load_production_model`) and lines 75-114 (`run_shap_analysis`).
  - Three bugs to fix: `ModelRegistry.stat_name` → filter via `model_name.like(f"%\\_{stat}")`; `model_row.model_path` → `model_row.artifact_path`; `joblib.load()` → class-specific `.load()` then pass `.model` to TreeExplainer.
  - Also add early-return with warning for Ridge/Ensemble.

- `src/db/models.py:306-323`
  - `ModelRegistry` canonical schema reference. No `stat_name`/`model_path` columns.

- `src/models/ensemble.py:189-240` (Sprint 57)
  - Reference implementation of the atomic save pattern to replicate for base models.

- `src/models/{catboost,xgboost,lightgbm,random_forest,ridge}_model.py`
  - Each has a `save()` method that pickles a dict to `open(path, "wb")`. Need the atomic rewrite. Lines vary by file; grep `def save` to find.

- `src/training/trainer.py:204-214` (`MODEL_CLASSES` list)
  - Source of truth for model class names — use for building the name→class lookup dict in SHAP script.

- `src/inference/registry_health.py` (Sprint 56 + 57)
  - Already has `validate_production_artifacts(session)`. Sprint 58 cron simply calls this from a one-shot script.

- `~/projects/homelab/compose/compose.nba-ml.yml`
  - Add a new `ofelia.job-exec.registry-health.*` label set for nightly run.

- `tasks/PROGRESS-sprint58-shap-bug-0417.md`
  - Sprint 58 tracker — already written.

- `tests/test_sprint57.py`
  - Pattern reference for Sprint 58 tests (atomic save tests, error-path tests).

- `docs/reports/sprint57-results.md`
  - Source of Next Steps list being implemented.
</important_files>

<next_steps>
Immediate next steps (in order):

1. **Fix SHAP** (`scripts/shap_analysis.py`):
   - Replace filter with `ModelRegistry.model_name.like(f"%\\_{stat_name}")` plus `is_production=True`.
   - Replace `model_row.model_path` with `model_row.artifact_path`.
   - Build a `{class_name: class}` lookup from `MODEL_CLASSES` + `EnsembleModel` + `MinutesModel`.
   - Derive class name from `model_row.model_name.rsplit("_", 1)[0]`.
   - Instantiate, call `.load(path)`, return the instance (not a raw dict).
   - In `run_shap_analysis`: if the class is `RidgeModel` or `EnsembleModel`, log a warning and return `{"stat": stat_name, "skipped": True, "reason": f"TreeExplainer does not support {class_name}"}`.
   - Pass `instance.model` (the inner CatBoost/XGBoost/etc. estimator) to `shap.TreeExplainer`. Use `instance.feature_names` for alignment.

2. **Atomic base-model saves** — apply the Sprint 57 ensemble pattern to the `save()` method of CatBoost/XGBoost/LightGBM/RandomForest/Ridge models.

3. **Registry-health cron** — add Ofelia labels to `~/projects/homelab/compose/compose.nba-ml.yml`:
   ```
   ofelia.job-exec.registry-health.schedule: "0 0 12 * * *"  # 07:00 ET daily
   ofelia.job-exec.registry-health.container: nba-ml-api
   ofelia.job-exec.registry-health.command: "python -c 'from src.db.connection import get_session; from src.inference.registry_health import validate_production_artifacts; s=get_session(); validate_production_artifacts(s); s.close()'"
   ```

4. **Write `tests/test_sprint58.py`**:
   - SHAP: mocked registry row with `model_name="CatBoostModel_pts"`, assert the class is resolved correctly; mock `model_name="RidgeModel_pts"`, assert `run_shap_analysis` returns `skipped: True`; mock missing registry, assert `ValueError`.
   - Atomic save: for each base model class (using fitted-from-scratch fixtures), patch `pickle.dump` to raise, assert pre-existing file is byte-identical and no `.tmp` leftover.

5. **Full pytest**, then rebuild `nba-ml-api`, deploy.

6. **Manual SHAP retry** inside container: `docker exec nba-ml-api python scripts/shap_analysis.py --stat reb` (pick a tree-model stat; reb is Ensemble → should skip; pick one of the ensemble base models via `--model catboost` if CLI supports, else pick a CatBoost-backed stat — stl is CatBoost_stl → should work).

7. **Live prediction-volume check** after 22:15 UTC `predict-refresh`: compare prediction counts per stat vs. pre-retrain baseline.

8. **Write `docs/reports/sprint58-results.md`**, append lessons, commit, push, PR, merge, sync main.

Open questions:
- Whether the CLI of `scripts/shap_analysis.py` accepts `--model` to pick a specific base model for ensemble stats, or whether it always uses the production winner. Need to read the `main()` function when resuming.
- Whether there's a fitted-from-scratch fixture pattern in existing tests for base models that can be reused in `test_sprint58.py` atomic-save tests, or whether I need to build one (Sprint 57 used `_make_fitted_ensemble()` helper locally; same approach should work per-class).
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
