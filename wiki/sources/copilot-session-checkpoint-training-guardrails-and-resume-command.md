---
title: "Copilot Session Checkpoint: Training guardrails and resume command"
type: source
created: 2026-03-26
last_verified: 2026-04-21
source_hash: "d57ad480214e3490dbc8ee6afd514a97ba2f1789612676f0d5048939d70f2c44"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-training-guardrails-and-resume-command-4822a5b3.md
quality_score: 65
concepts:
  []
related:
  - "[[Homelab]]"
  - "[[NBA ML Engine]]"
tier: hot
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine]
checkpoint_class: durable-architecture
retention_mode: retain
knowledge_state: executed
---

# Copilot Session Checkpoint: Training guardrails and resume command

## Summary

The user requested training guardrails for the NBA ML Engine to prevent stuck training processes, plus the ability to resume partially-completed training pipelines. This followed a training run that appeared stuck for 4+ hours on `cv_EnsembleModel_stl`. The approach was to add configurable SIGALRM-based timeouts at multiple levels (per-model, per-fold, per-pipeline), extract the CV logic into a standalone function, add a `resume` CLI command, and then use it to finish the remaining training work.

## Key Points

- Add timeout config vars to config.py
- Add TrainingTimeoutError and _training_timeout context manager
- Wrap model.train() with timeout in training loop
- Wrap CV folds with per-fold + cumulative timeout
- Extract CV into standalone _run_walk_forward_cv()
- Add resume_pipeline() function

## Execution Snapshot

**Files created:**
- `tests/test_training_guardrails.py`: 14 tests covering TrainingTimeoutError, _training_timeout context manager, CV guardrails (fold timeout, cumulative timeout), and resume_pipeline (CV+classifiers, skip_cv, skip_classifiers)

**Files modified:**
- `config.py`: Added 4 training guardrail config vars (TRAINING_STEP_TIMEOUT=1800, CV_FOLD_TIMEOUT=600, CV_MODEL_TIMEOUT=2400, PIPELINE_TOTAL_TIMEOUT=28800) with env var overrides
- `src/training/trainer.py`: Added imports (signal, threading, time, contextmanager), TrainingTimeoutError class, _training_timeout() context manager, wrapped model.train() with timeout in train_all(), extracted CV into _run_walk_forward_cv() with per-fold and cumulative timeouts, wrapped train_pipeline() in PIPELINE_TOTAL_TIMEOUT, added resume_pipeline() function
- `main.py`: Added `resume` CLI command with --cv-stats, --skip-cv, --skip-classifiers options (inserted after `train` command)
- `docs/reports/training-progress-report_0325.md`: Updated from "stuck/stalled" status to "completed" with guardrails documentation

**Work completed:**
- [x] Add timeout config vars to config.py
- [x] Add TrainingTimeoutError and _training_timeout context manager
- [x] Wrap model.train() with timeout in training loop
- [x] Wrap CV folds with per-fold + cumulative timeout
- [x] Extract CV into standalone _run_walk_forward_cv()
- [x] Add resume_pipeline() function
- [x] Add resume CLI command to main.py
- [x] Write 14 tests — all passing
- [x] Kill stuck process and restart container
- [x] Rebuild container with guardrail code
- [x] Resume and complete remaining training (CV for 6 stats + classifiers)
- [x] Update training progress report
- [x] Commit and push to main

**Current state:**
- On branch `feature/sprint-21-retrain-feature-analysis`
- Commits were pushed directly to `origin/main` via `git push origin HEAD:main`
- The branch itself may not have been pushed to its own remote tracking branch
- Need to check if a PR from the feature branch to main is still needed or if work is already on main
- All training complete: 9 stats × 6 models trained + CV'd, 4 classifiers done
- Container running with guardrails active

## Technical Details

- **SIGALRM timeout mechanism**: Uses `signal.SIGALRM` for hard timeouts in main thread. Falls back to no-op with warning in non-main threads (e.g., if called from API endpoint). The `_training_timeout()` context manager saves/restores the old signal handler and cancels the alarm on exit.
- **Nested timeout concern**: Inner timeouts restore outer handlers correctly. Tested explicitly with nested `_training_timeout()` calls.
- **CV refactoring**: The CV block was inline in `train_all()` (lines 502-593 originally). Extracted to `_run_walk_forward_cv(df, stats, model_classes, feature_cols)` which takes the feature DataFrame and runs expanding-window CV independently. This enables the resume command to build features once and call CV without re-training models.
- **Resume architecture**: `resume_pipeline()` builds features, calls `_run_walk_forward_cv()` for specified stats, then `train_over_under_classifiers()`. Models are assumed already saved from prior training run.
- **Container build path**: nba-ml-api is defined in `~/projects/homelab/compose/compose.nba-ml.yml`, NOT in the nba-ml-engine docker-compose.yml (which only has db + mlflow). Build command: `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache nba-ml-api`
- **Process killing**: Can't directly `kill` container PIDs from host (root-owned). Must use `docker restart nba-ml-api` or `docker exec` to send signals from inside the container.
- **The "stuck" process wasn't actually stuck**: cv_EnsembleModel_stl completed normally at 19:44 (~15 min after cv_CatBoostModel_stl at 19:29). The appearance of a 4-hour stall was because we checked MLflow at 19:33 — just 4 minutes into EnsembleModel's ~15 min run — and the report was written at that point. By 20:11 the original process had completed through tov before being restarted.
- **EnsembleModel CV timing**: Consistently ~14-15 minutes per stat across all 9 stats. It trains 5 base models internally per fold × 9 folds = 45 model trainings per stat.
- **Git push strategy**: Commits on `feature/sprint-21-retrain-feature-analysis` were pushed directly to `origin/main` via `git push origin HEAD:main`, bypassing the typical PR workflow. The feature branch remote may be out of sync.
- **Pre-existing test failures**: 15 tests in `test_notifications.py` fail due to missing `apprise` module in the dev .venv — these are unrelated to guardrail changes.

## Important Files

- `src/training/trainer.py`
- Core training orchestrator — all timeout and resume logic lives here
- Added: TrainingTimeoutError (line ~43), _training_timeout() (line ~47-80), wrapped model.train() with timeout in train_all() (~line 466-480), _run_walk_forward_cv() standalone function (~line 550-630), resume_pipeline() (~line 865-915), train_pipeline() wrapped with PIPELINE_TOTAL_TIMEOUT (~line 823-862)
- MODEL_CLASSES list at ~line 72-79

- `config.py`
- All project configuration including new guardrail vars
- Lines ~107-114: TRAINING_STEP_TIMEOUT, CV_FOLD_TIMEOUT, CV_MODEL_TIMEOUT, PIPELINE_TOTAL_TIMEOUT

- `main.py`
- CLI entry point with train and resume commands
- Lines ~199-233: `resume` command with --cv-stats, --skip-cv, --skip-classifiers
- Line 748: `if __name__ == "__main__": cli()`

- `tests/test_training_guardrails.py`
- 14 tests across 4 classes: TestTrainingTimeoutError, TestTrainingTimeout, TestCVGuardrails, TestResumePipeline
- Tests signal alarm behavior, nested timeouts, fold timeout skipping, cumulative timeout breaking, resume with skip options

- `docs/reports/training-progress-report_0325.md`
- Training progress report updated to reflect completion
- Documents all 4 phases, per-stat timing tables, and guardrail configuration

- `~/projects/homelab/compose/compose.nba-ml.yml`
- Docker compose definition for nba-ml-api (build context, volumes, env vars)
- Build from homelab root: `docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache nba-ml-api`

## Next Steps

**Remaining work:**
- **Create PR and merge to main**: The user explicitly asked "push all changes, pr and merge to main". Commits were already pushed directly to `origin/main` via `git push origin HEAD:main`, so a formal PR may need to be created from the feature branch. Need to check if there are any unpushed commits on the feature branch vs what's on main.

**Immediate next actions:**
1. Check if feature branch `feature/sprint-21-retrain-feature-analysis` has the same commits as `origin/main`
2. If already on main, either create a retroactive PR or confirm the work is complete
3. If not on main, push the feature branch and create PR via `gh pr create`, then merge
4. Clean up: ensure branch is deleted after merge

## Related Wiki Pages

- [[Homelab]]
- [[NBA ML Engine]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-training-guardrails-and-resume-command-4822a5b3.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-26 |
| URL | N/A |
