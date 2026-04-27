---
title: "Copilot Session Checkpoint: Weekly Retrain OOM Debugging"
type: text
captured: 2026-04-27T01:32:25.391857Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard]
checkpoint_class: durable-debugging
checkpoint_class_rule: "title:oom"
retention_mode: retain
status: success
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Weekly Retrain OOM Debugging
**Session ID:** `39cb6a8f-14d7-43a7-bad1-98ec00e06033`
**Checkpoint file:** `/home/jbl/.copilot/session-state/39cb6a8f-14d7-43a7-bad1-98ec00e06033/checkpoints/012-weekly-retrain-oom-debugging.md`
**Checkpoint timestamp:** 2026-04-27T01:31:05.003181Z
**Exported:** 2026-04-27T01:32:25.391857Z
**Checkpoint class:** `durable-debugging` (rule: `title:oom`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user’s goals in this segment were to stabilize the NBA ML weekly retrain on the homelab after repeated OOMs, verify the live Ofelia cron setup, manually trigger the weekly retrain, determine whether it actually completed, and then enhance logging and fix the retrain so it can run end-to-end safely. The approach was systematic debugging first: confirm the live scheduler/deploy state, inspect process/model-registry/artifact timelines, correlate with kernel OOM evidence, and then move into TDD-driven code changes that make the weekly retrain more observable and more memory-safe.
</overview>

<history>
1. The user asked to **implement the weekly-retrain OOM fix and validate**
   - Loaded `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `executing-plans`, `subagent-driven-development`, and `using-git-worktrees`.
   - Reviewed `plan.md`, queried SQL todos, inspected `nba-ml-engine/main.py`, `src/training/trainer.py`, `homelab/compose/compose.nba-ml.yml`, and the existing OOM guardrail tests.
   - Confirmed the new OOM was from the **weekly-retrain** Ofelia job (`python main.py train`), not the daily `pipeline --skip-training` job.
   - Created isolated worktrees for `nba-ml-engine` and `homelab`.
   - Added failing regression tests requiring:
     - `train --help` to expose `--memory-safe`
     - memory-safe weekly retrain orchestration
     - homelab weekly scheduler to call `python main.py train --memory-safe`
   - Implemented first-generation fix:
     - Added `--memory-safe` to `main.py train`
     - Memory-safe path ran isolated subprocess stages: `train-minutes`, one `train --stat <stat>` per stat, `resume --skip-cv`, `train-calibrator`
     - Suppressed child notifications
     - Added `train-minutes` and `train-calibrator` hidden commands
     - Extracted `train_confidence_calibrator()` helper in `src/training/trainer.py`
     - Updated `homelab/compose/compose.nba-ml.yml` weekly Ofelia command to `python main.py train --memory-safe`
   - Ran targeted tests and broader validation; both passed.
   - Ran a code-review agent on the fix.
   - The reviewer found two real issues:
     - memory-safe child subprocesses did not preserve the old `PIPELINE_TOTAL_TIMEOUT`
     - memory-safe path ignored `PIPELINE_SKIP_STATS`
   - Added failing tests for both review findings, then patched:
     - `subprocess.run(..., timeout=config.PIPELINE_TOTAL_TIMEOUT)`
     - skip-stat filtering mirrored from the original training path
   - Re-ran regressions and broader validation successfully.
   - Copied the validated worktree changes into the live repo files.
   - Validated in the live repos:
     - `nba-ml-engine`: `tests/test_dashboard_accuracy_followups.py tests/test_training_guardrails.py` → `40 passed`
     - `homelab`: `tests/test_nba_ml_oom_guardrails.py` → `2 passed`
     - compose config validated
     - `main.py train --help` in live repo/container showed `--memory-safe`
   - Deployed `nba-ml` with `./scripts/ops/deploy.sh nba-ml`
   - Verified:
     - scheduler label registered `weekly-retrain` as `python main.py train --memory-safe`
     - `pipeline-daily` still used `python main.py pipeline --skip-training`
     - `/health` returned `{"status":"ok", ...}`

2. The user asked **“are ofelia cronjobs still set up correctly?”**
   - Re-read `homelab/compose/compose.nba-ml.yml`
   - Inspected live `nba-ml-scheduler` labels via `docker inspect`
   - Confirmed deployed schedules/commands matched compose, including:
     - daily pipeline at `0 0 7 * * *`
     - props refresh at `0 0 20 * * *`
     - predict refresh at `0 15 22 * * *`
     - weekly retrain at `0 0 16 * * 0` with `python main.py train --memory-safe`
   - Responded that the cron jobs were still configured correctly.

3. The user asked to **start the weekly pipeline again**
   - Per homelab-deploy guidance, first checked the live deployed config and current host headroom.
   - Verified no active weekly retrain process was already running.
   - Noted host memory was tight and swap was still fully exhausted, making the run medium-risk.
   - Manually started the weekly retrain with:
     - `docker exec -d -w /app nba-ml-api python main.py train --memory-safe`
   - Verified active processes after launch:
     - parent `python main.py train --memory-safe`
     - child `/usr/local/bin/python /app/main.py train-minutes`
   - Checked `/training/status`; it still showed `Idle` because the first-generation memory-safe path did not update the status tracker.
   - Reported that the retrain was running at the process level despite `/training/status` not reflecting it.

4. The user asked **whether the full weekly retrain was done**
   - Checked active retrain processes: none were left.
   - Queried `model_registry` for rows after the manual trigger window; initially only saw:
     - `MinutesModel_minutes`
     - `CatBoostModel_pts`
   - Concluded at first that the retrain was not complete.
   - Then investigated further because this looked incomplete:
     - inspected model artifact modification times on disk under `/app/models`
     - discovered the run had actually progressed farther:
       - `minutes` model artifacts updated around 16:21-16:22 local
       - full `pts` artifact set updated through ensemble around 16:54 local
       - full `reb` artifact set updated through ensemble around 18:05 local
       - no new `ast` artifacts after that
   - This showed the run advanced beyond what the registry alone indicated, but still stopped before finishing all stats.

5. The user asked to **enhance logging and fix the full retrain pipeline, then validate and run it**
   - Returned to systematic debugging before changing code.
   - Gathered evidence:
     - `/training/status` implementation in `src/training/status.py`
     - `/training/status` API response assembly in `src/api/server.py`
     - `train_all()` / `_register_best_model()` internals in `src/training/trainer.py`
     - kernel OOM and Docker events since the manual retrain start
   - Found the decisive root cause:
     - kernel log at **Apr 26 18:15:19 EDT** showed another **global host OOM**
     - victim was `python` inside `nba-ml-api`, RSS about **10.3 GB**
     - artifact timeline showed the run finished `reb` model artifacts at about **18:05**, then died before `ast`
     - because the first-generation memory-safe path used `train --stat <stat>`, each stat child still ran the full `train_all()` logic for that stat, including **walk-forward CV**, which likely caused the post-`reb` OOM
   - Began the TDD fix:
     - rewrote/additional tests in `tests/test_dashboard_accuracy_followups.py` to require:
       - memory-safe weekly retrain to orchestrate **per-model** subprocesses, not per-stat subprocesses
       - each model child to use `--skip-register`, `--skip-cv`, and `--metrics-json`
       - parent-side best-model registration after aggregating model metrics
       - status tracker start/advance/complete/finish calls
       - failure path to record stage name and log-path context
     - confirmed the new tests failed first, initially because `MEMORY_SAFE_TRAINING_DIR` and the enhanced orchestration did not exist yet
     - then tightened expectations to require `--skip-cv` after realizing the likely killer was per-stat CV
   - Started implementing the new design (see Work Done / Current State below)
</history>

<work_done>
Files updated before the final compaction request:
- `nba-ml-engine/main.py`
  - **Previously completed and deployed**:
    - Added `train --memory-safe`
    - Added hidden `train-minutes` and `train-calibrator`
    - Added notification suppression helper
    - Added subprocess timeout preservation
    - Added skip-stat handling for memory-safe weekly retrain
  - **New in-progress edits at compaction time**:
    - Added `MEMORY_SAFE_TRAINING_DIR`
    - Added log/manifest helpers:
      - `_append_retrain_log()`
      - `_write_memory_safe_manifest()`
      - `_memory_safe_target_stats()`
    - Extended `_run_self_cli_subprocess()` to accept `log_path` and `stage_name`, and redirect child stdout/stderr into a persistent log file when requested
    - Reworked `_run_memory_safe_weekly_retrain()` toward:
      - live status tracking via `src.training.status`
      - per-model subprocess orchestration
      - parent-side best-model registration
      - persistent run log and manifest
      - error propagation with stage name + log path
    - Extended `train` CLI with hidden options:
      - `--skip-register`
      - `--skip-cv`
      - `--metrics-json`
      - temporary `USE_WALK_FORWARD_CV`/`USE_CV_MODEL_SELECTION` overrides for hidden child use
- `nba-ml-engine/src/training/trainer.py`
  - **Previously completed and deployed**:
    - Extracted `train_confidence_calibrator()`
  - **New in-progress edits at compaction time**:
    - `train_all()` signature extended with:
      - `register_best: bool = True`
      - `split_metadata_sink: dict[...] | None = None`
    - Split metadata is now written into the optional sink
    - best-model registration made conditional on `register_best`
- `nba-ml-engine/tests/test_dashboard_accuracy_followups.py`
  - **Previously completed and passing**:
    - Tests for `--memory-safe` help exposure
    - Tests for earlier memory-safe weekly retrain orchestration
    - Tests for timeout and skip-stat fixes
  - **New, currently failing or unvalidated after code patch**:
    - TDD tests requiring:
      - per-model memory-safe orchestration
      - `--skip-cv` in model children
      - parent-side best-model registration
      - status tracker lifecycle
      - failure stage/log-path reporting
- `homelab/compose/compose.nba-ml.yml`
  - Already updated and deployed:
    - weekly Ofelia command is `python main.py train --memory-safe`
    - daily job remains `python main.py pipeline --skip-training`
- `homelab/tests/test_nba_ml_oom_guardrails.py`
  - Already updated and passing:
    - asserts weekly retrain uses `--memory-safe`

Current state at compaction:
- **Completed and deployed**
  - First-generation weekly memory-safe retrain
  - Review fixes (timeout preservation, skip-stat honoring)
  - Live scheduler update + deployment
- **Investigated**
  - Manual weekly retrain still failed
  - Root cause narrowed to another host OOM during the stat-child path, almost certainly in/after `reb` due to per-stat child CV and memory pressure
- **Most recent active work**
  - Mid-implementation of a second-generation fix:
    - per-model subprocess weekly retrain
    - persistent run logs/manifests
    - live `/training/status` updates
    - hidden `--skip-cv`, `--skip-register`, `--metrics-json` child path
- **Not yet verified**
  - The newly patched `main.py` / `trainer.py` changes for per-model orchestration were **applied but not yet test-run** after the last `apply_patch`
  - No redeploy/run has happened for this second-generation fix yet

Tasks / SQL state:
- Existing completed todo count was 91 done before this segment.
- New todos created for current work:
  - `retrain-root-cause` — in progress at creation time
  - `retrain-tests` — pending
  - `retrain-fix` — pending
  - `retrain-validate-run` — pending
</work_done>

<technical_details>
- **Confirmed OOM progression**
  - Earlier weekly-retrain OOMs were host-level/global OOMs, not just clean cgroup limit breaches.
  - The first manual run of `train --memory-safe` also hit a new global OOM:
    - kernel timestamp: **Apr 26 18:15:19 EDT**
    - victim: `python` inside `nba-ml-api`
    - RSS: about **10.3 GB**
    - host swap was still fully exhausted
- **Critical artifact-vs-registry discovery**
  - `model_registry` under-reported actual progress during the failed manual retrain.
  - On-disk model mtimes under `/app/models` showed:
    - `minutes` finished around 16:21-16:22 local
    - `pts` finished all artifacts through ensemble around 16:54
    - `reb` finished all artifacts through ensemble around 18:05
    - nothing new for `ast` and later stats
  - This means the run got farther than the DB alone suggested.
- **Likely concrete failure point**
  - The first-generation memory-safe weekly retrain used:
    - `train-minutes`
    - `train --stat <stat>` per stat
  - But `train --stat <stat>` still routes into `train_all(stats=[stat], model_classes=...)`, and `train_all()` still performs:
    - all model-class training for that stat
    - and, when `USE_WALK_FORWARD_CV=true` and `USE_CV_MODEL_SELECTION=true`, **walk-forward CV** after the stat training loop
  - Because `reb` artifacts finished but `ast` never started, the likely failure zone is the **CV tail inside the `reb` child process**, not the parent or classifier stage.
- **Why the first memory-safe design was insufficient**
  - Per-stat isolation was not granular enough.
  - Even one stat child remained large enough to be OOM-killed.
  - That points at the need for **per-model subprocess isolation**, not just per-stat subprocess isolation.
- **Why `--skip-cv` matters**
  - For the new design, each model child should disable walk-forward CV entirely:
    - otherwise a “single-model child” still pays the CV memory cost
    - and would likely reproduce the same failure pattern
- **Status tracker behavior**
  - `/training/status` is backed by `src.training.status` writing an atomic JSON file, default `/tmp/training_status.json`.
  - Existing `train_pipeline()` updates this tracker.
  - The first-generation memory-safe weekly retrain did **not** call `start_pipeline` / `advance_stage` / `finish_pipeline`, so the API remained `Idle` even while processes were running.
  - The second-generation fix is being built to correct this.
- **Logging behavior quirk**
  - Manual `docker exec -d ... python main.py train --memory-safe` does not surface child logs in normal `docker logs nba-ml-api`.
  - This is why the first manual retrain was hard to diagnose after failure.
  - The second-generation fix is adding a dedicated log file under a persistent training directory so detached runs remain inspectable.
- **Registration behavior**
  - `_register_best_model()`:
    - decides the best model by configured metric
    - guards against >10% degradation vs current production
    - guards against negative R² / insufficient hit-rate
    - verifies the saved artifact exists
    - demotes previous production entries
    - writes the new `ModelRegistry` row and `commit()`s
  - For per-model orchestration, the parent must aggregate child metrics and call `_register_best_model()` once per stat.
- **Environment/runtime notes**
  - Host shell does not have `pytest` globally; project tests are run with `/home/jbl/projects/nba-ml-engine/.venv/bin/python -m pytest`.
  - `nba-ml-api` container provides working Python/pytest runtime for in-container introspection.
  - `nba-ml-api` `/health` is the correct unauthenticated health endpoint; `/healthz` returned 401 in this environment.
  - `docker top nba-ml-api` is more reliable than `ps` inside the container because the image shell lacked `ps`.
- **Live scheduler state already confirmed**
  - `nba-ml-scheduler` live labels matched compose:
    - weekly retrain: `python main.py train --memory-safe`
    - daily pipeline: `python main.py pipeline --skip-training`
    - props/predict/health/report/backup jobs all still present with expected schedules
</technical_details>

<important_files>
- `nba-ml-engine/main.py`
  - **Central orchestration point** for both daily and weekly training paths.
  - Already contains the first-generation `--memory-safe` implementation and review fixes.
  - Most recent in-progress edits for second-generation fix are here:
    - logging helpers
    - memory-safe stage planner
    - per-model orchestration
    - hidden child flags (`--skip-register`, `--skip-cv`, `--metrics-json`)
    - live status updates
  - Key sections:
    - top-of-file helper area around lines ~16-125
    - `train()` command around lines ~267-355
    - hidden `train-minutes` / `train-calibrator` commands around lines ~358-380

- `nba-ml-engine/src/training/trainer.py`
  - **Core training engine** and model-registration logic.
  - Contains:
    - `train_all()`
    - `_register_best_model()`
    - `train_pipeline()`
    - `train_confidence_calibrator()`
  - Most recent in-progress changes:
    - `train_all(... register_best=..., split_metadata_sink=...)`
    - conditional registration
    - split-metadata export for parent-side registration
  - Key sections:
    - `train_all()` around lines ~533-963
    - `_register_best_model()` around lines ~1067-1194
    - `train_pipeline()` around lines ~1298-1422
    - `train_confidence_calibrator()` below `train_pipeline()`

- `nba-ml-engine/src/training/status.py`
  - **Status tracker** used by `/training/status`.
  - Important because the second-generation fix is being wired to this file’s API:
    - `start_pipeline`
    - `advance_stage`
    - `complete_stage`
    - `finish_pipeline`
  - Key lines: ~19-96

- `nba-ml-engine/src/api/server.py`
  - **Public training-status endpoint** implementation.
  - Important to understand why the first-generation memory-safe run still displayed `Idle`.
  - Key section: `/training/status` endpoint around lines ~879-949

- `nba-ml-engine/tests/test_dashboard_accuracy_followups.py`
  - **Primary regression suite** for the weekly retrain work.
  - Earlier tests here passed for the first-generation fix and its review follow-ups.
  - New TDD tests now cover:
    - per-model memory-safe orchestration
    - skip-stat behavior
    - failure status/log-path reporting
  - This file is the main place to resume red/green validation.

- `homelab/compose/compose.nba-ml.yml`
  - **Live homelab scheduler config**.
  - Already changed and deployed to use:
    - weekly retrain → `python main.py train --memory-safe`
    - daily pipeline → `python main.py pipeline --skip-training`
  - Key section: Ofelia labels around lines ~124-170

- `homelab/tests/test_nba_ml_oom_guardrails.py`
  - **Homelab regression guardrails**.
  - Already passing in main repo:
    - daily pipeline skips training
    - weekly retrain uses `--memory-safe`

- `/tmp/copilot-tool-output-1777252268351-t6k009.txt`
  - Captured recent process/log inspection around the incomplete manual weekly retrain.
  - Used to confirm no active retrain processes and that normal API logs did not contain the child retrain output.

- In-container artifact paths under `/app/models/*`
  - Not code files, but operationally critical:
    - model artifact mtimes under `minutes/`, `pts/`, `reb/` were the key evidence that the retrain progressed farther than the DB showed.
</important_files>

<next_steps>
Remaining work:
1. **Run the new red/green cycle to completion after the last code patch**
   - The latest `main.py` / `trainer.py` changes were applied but **not yet test-run** before compaction.
   - First immediate step: run
     - `cd /home/jbl/projects/nba-ml-engine && .venv/bin/python -m pytest -q tests/test_dashboard_accuracy_followups.py -k 'memory_safe'`
   - Expect failures to have shifted from “feature missing” to any implementation mismatches.

2. **Fix any remaining test failures from the second-generation orchestration**
   - Likely areas if tests fail:
     - monkeypatch compatibility with newly added imports/helpers
     - `split_metadata_sink` handling
     - hidden CLI options integration
     - status lifecycle ordering / error message formatting
     - persistence-path assumptions

3. **Run broader validation after targeted tests pass**
   - `cd /home/jbl/projects/nba-ml-engine && .venv/bin/python -m pytest -q tests/test_dashboard_accuracy_followups.py tests/test_training_guardrails.py`
   - Re-run:
     - `cd /home/jbl/projects/homelab && /home/jbl/projects/nba-ml-engine/.venv/bin/python -m pytest -q tests/test_nba_ml_oom_guardrails.py`
   - Re-validate compose if homelab files change again:
     - `docker compose -f compose/compose.nba-ml.yml --env-file .env config --quiet`

4. **If validation passes, deploy the updated `nba-ml` stack again**
   - `cd /home/jbl/projects/homelab && ./scripts/ops/deploy.sh nba-ml`

5. **Re-run the weekly retrain after deploy**
   - Trigger manually (or wait for Ofelia) using the new second-generation memory-safe path.
   - This time verify:
     - `/training/status` shows live progress instead of `Idle`
     - a log file and manifest are created under the training log directory
     - per-model stages advance across all stats
     - no host OOM occurs
     - `model_registry` gets fresh rows across all weekly stats, plus classifier/calibrator completion

6. **Post-run verification**
   - Check active processes
   - Check `/training/status`
   - Inspect the persistent weekly retrain log/manifest
   - Query `model_registry` for fresh rows across all stats
   - Re-check kernel OOM logs after the run window

Open questions / potential blockers:
- Whether **per-model subprocesses + CV disabled** are sufficient to avoid the host OOM under current memory pressure.
- Whether preserving weekly walk-forward CV is still desired; current fix direction intentionally disables CV for the model children because it appears to be the likely killer. If the user later insists on weekly CV, it may need a separate dedicated/offline path.
- Whether the parent-side registration path needs any extra metadata beyond what `split_metadata_sink` now exports.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
