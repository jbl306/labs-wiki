---
title: "Copilot Session Checkpoint: OOM Mitigation and Follow-Up"
type: text
captured: 2026-04-26T19:11:00.550078Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, mempalace, dashboard]
checkpoint_class: durable-debugging
checkpoint_class_rule: "title:oom"
retention_mode: retain
status: pending
---

# Copilot Session Checkpoint Export

**Checkpoint title:** OOM Mitigation and Follow-Up
**Session ID:** `39cb6a8f-14d7-43a7-bad1-98ec00e06033`
**Checkpoint file:** `/home/jbl/.copilot/session-state/39cb6a8f-14d7-43a7-bad1-98ec00e06033/checkpoints/011-oom-mitigation-and-follow-up.md`
**Checkpoint timestamp:** 2026-04-26T19:09:26.926806Z
**Exported:** 2026-04-26T19:11:00.550078Z
**Checkpoint class:** `durable-debugging` (rule: `title:oom`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user’s goals in this segment were to stabilize the NBA ML homelab deployment after repeated OOM incidents, review an unpushed homelab galloping-bot fix commit and decide whether to push or delete it, and then investigate a new NBA ML API OOM recurrence. The approach was systematic debugging first: inspect kernel OOM logs, Docker/container state, scheduler commands, and live workload timing before making changes; then use TDD for any behavior changes and deploy only after validation.
</overview>

<history>
1. The user reported: **“Container killed by kernel OOM on beelink-gti13. Consider increasing memory limits.”**
   - Loaded `systematic-debugging` and `homelab-deploy`.
   - Queried MemPalace for prior homelab/NBA ML OOM context and previous lessons.
   - Inspected kernel logs, Docker inspect state, container limits, restart state, live memory usage, scheduler logs, and the homelab infrastructure reference.
   - Determined the killed container was `nba-ml-api`, but the kernel message showed a **global host OOM** (`constraint=CONSTRAINT_NONE`) rather than a clean container cgroup breach.
   - Traced the OOM to Ofelia job `pipeline-daily` running `python main.py pipeline`; the API server itself stayed alive and continued serving `/metrics`.
   - Found the job ran ~3h18m, finished model training/calibration, and was killed during prediction generation after building features for 532 active players; killed Python RSS was ~10.8 GB while host swap was effectively exhausted.
   - Concluded that **raising the 12 GB API limit alone would be the wrong fix** because the problem was daily full-model training on a shared 32 GB host, despite weekly retrain already existing.

2. To fix that OOM path, I implemented a daily-pipeline guardrail with TDD.
   - Loaded `test-driven-development`.
   - Added failing tests in `nba-ml-engine/tests/test_dashboard_accuracy_followups.py` to require:
     - a new `pipeline --skip-training` CLI flag,
     - and behavior where the pipeline can ingest/predict/QA using existing production models without invoking training or recalibration.
   - Added a homelab scheduler guardrail test in `homelab/tests/test_nba_ml_oom_guardrails.py` asserting the daily Ofelia command includes `--skip-training`.
   - Verified the new tests failed for the expected reasons before touching production code.
   - Implemented the minimal fix:
     - `nba-ml-engine/main.py`: added `--skip-training` to `pipeline`; when enabled, skip training, prune, and calibrator refit, and continue into predictions/QA using existing production models.
     - `homelab/compose/compose.nba-ml.yml`: changed Ofelia daily command from `python main.py pipeline` to `python main.py pipeline --skip-training`.
   - Ran targeted tests, then the full NBA backend test suite (`473 passed, 9 skipped, 14 deselected, 2 warnings`).
   - Validated homelab compose config with `docker compose ... config --quiet`.
   - Updated session `plan.md` to record the OOM incident and mitigation rationale.
   - Committed/pushed NBA change:
     - `dc892bd` `fix: let daily pipeline skip training`
   - Committed homelab scheduler changes locally:
     - `2a9782f` `fix: skip NBA daily training to avoid OOM`
     - `e92d612` `test: avoid yaml dependency in OOM guardrail`
   - Deployed the `nba-ml` stack with `./scripts/ops/deploy.sh nba-ml`.
   - Verified:
     - `nba-ml-api` health OK,
     - deployed CLI shows `--skip-training`,
     - Ofelia label now reads `python main.py pipeline --skip-training`.

3. The user then asked: **“check the unpushed galloping bot commit on homelab and see if should be committed and pushed, then push or delete”**
   - Loaded `code-reviewer`.
   - Inspected homelab repo state and unpushed commits.
   - Found `homelab/main` was ahead by 3 commits:
     - `6d4425a` `fix(galloping): auto-build image before every cron run`
     - `2a9782f` NBA daily OOM scheduler fix
     - `e92d612` OOM guardrail test cleanup
   - Reviewed `6d4425a` in detail:
     - it modifies only `scripts/ops/galloping-snipe.sh`,
     - adds a cached `compose build galloping-bot` before `compose run`,
     - falls back to existing image on build failure,
     - shell syntax passed `bash -n`,
     - and the change matched prior RCA stored in MemPalace (cron had used a stale week-old image because `compose run` doesn’t rebuild if the image already exists).
   - Determined the galloping commit should be **kept and pushed**, not deleted.
   - Pushed `homelab/main` to `origin/main`; all 3 ahead commits were published.
   - Final homelab remote state after push:
     - `e92d612`
     - `2a9782f`
     - `6d4425a`
   - Noted unrelated dirty homelab files remained uncommitted locally:
     - `compose/compose.web.yml`
     - `config/homepage/services.yaml`

4. The user then asked: **“investigate nba ml api container oom again”**
   - Reloaded `systematic-debugging` and `homelab-deploy`.
   - Queried MemPalace again for post-fix context.
   - Re-checked container inspect state, kernel OOM logs since the last deployment, Docker events, scheduler label, scheduler/API logs, and current memory.
   - Found this was **a new OOM after the `--skip-training` mitigation**:
     - kernel log at **2026-04-26 15:05:17 EDT** showed another **global host OOM**,
     - victim process was again Python inside a Docker scope that maps to `nba-ml-api`,
     - killed process RSS was ~11.4 GB,
     - `nba-ml-api` container still running with `.State.OOMKilled=true`,
     - scheduler label was still correctly `python main.py pipeline --skip-training`.
   - Important new clue:
     - recent scheduler logs still contained **full training activity** (multiple model training logs around 13:59, including XGBoost/RandomForest/etc.), which strongly suggests some other scheduler/job path or running process is still executing training despite the updated daily label.
   - At compaction time, I had **not yet finished root-causing this second OOM**. Investigation was active, and one long shell command (`shellId: 1870`) was still running/unfinished when the summary request arrived.
</history>

<work_done>
Files updated in `nba-ml-engine`:
- `main.py`
  - Added `pipeline --skip-training`.
  - Daily pipeline can now skip training/pruning/calibration and still generate predictions/QA from current production models.
- `tests/test_dashboard_accuracy_followups.py`
  - Added regression tests for:
    - `pipeline --help` exposing `--skip-training`
    - `pipeline --skip-training` not invoking training/calibration and still executing predictions + matview refresh + notifications.

Files updated in `homelab`:
- `compose/compose.nba-ml.yml`
  - Changed Ofelia daily job command to `python main.py pipeline --skip-training`.
- `tests/test_nba_ml_oom_guardrails.py`
  - Added a simple text-based guardrail test asserting the daily scheduler command includes `--skip-training`.
- `scripts/ops/galloping-snipe.sh`
  - Reviewed, not modified during the review step; already changed by `6d4425a` to build `galloping-bot` before each cron-run execution.

Session plan updated:
- `/home/jbl/.copilot/session-state/39cb6a8f-14d7-43a7-bad1-98ec00e06033/plan.md`
  - Added OOM incident details and rationale for skip-training mitigation.

Commits created/pushed:
- `nba-ml-engine`:
  - `dc892bd` `fix: let daily pipeline skip training` — pushed to `origin/main`
- `homelab`:
  - `2a9782f` `fix: skip NBA daily training to avoid OOM` — pushed to `origin/main`
  - `e92d612` `test: avoid yaml dependency in OOM guardrail` — pushed to `origin/main`
  - `6d4425a` `fix(galloping): auto-build image before every cron run` — pushed to `origin/main`

Validation completed:
- NBA full backend test suite passed:
  - `473 passed, 9 skipped, 14 deselected, 2 warnings`
- Homelab scheduler guardrail test passed.
- `docker compose -f compose/compose.nba-ml.yml --env-file .env config --quiet` passed.
- `nba-ml` stack redeployed successfully.
- API health endpoint returned OK after deploy.
- Ofelia scheduler label confirmed deployed:
  - `python main.py pipeline --skip-training`

Current state:
- **Completed:** first OOM mitigation, homelab push review, pushing the galloping commit and related homelab commits.
- **Most recent active work:** investigating a **new** NBA ML API OOM that occurred even after the skip-training deploy.
- **Open issue:** new OOM at 15:05 EDT is not yet explained; recent scheduler logs still show training activity, which may indicate another job path or stale/external execution route still performing full training.
</work_done>

<technical_details>
- First OOM root cause:
  - Not a simple container-limit breach.
  - Kernel log showed:
    - `constraint=CONSTRAINT_NONE`
    - `global_oom`
  - This means the host ran out of memory/swap globally; simply increasing `nba-ml-api` memory would increase risk rather than safely contain it.
- First OOM happened in an Ofelia `docker exec` job inside `nba-ml-api`, not by crashing the API server container itself.
- `nba-ml-api` container limit:
  - `12G`
- First OOM killed Python process:
  - ~10.8 GB RSS
- Host conditions during first OOM:
  - swap effectively exhausted
  - several large non-Docker processes on host also consuming memory (multiple Copilot/MemPalace processes were visible in `ps -eo ... --sort=-rss` during investigation).
- Daily pipeline behavior before fix:
  - `main.py pipeline` still performed full model training, prune, calibrator refit, prediction generation, QA, matview refresh, health checks.
- Weekly retrain already exists separately in `compose.nba-ml.yml`:
  - Ofelia weekly job runs `python main.py train`.
- Decision/rationale:
  - Daily job should not also perform full training.
  - Daily job now uses existing production models for prediction freshness; weekly retrain remains the heavy training path.
- Homelab deploy/security assessment for this change:
  - No new image, no new ports, no new mounts, no new credentials, no additional external exposure.
  - Low-risk scheduler command change in existing `nba-ml` stack.
- Galloping bot review findings:
  - `docker compose run` does **not** rebuild an existing image; it only builds when the image is missing.
  - For manual-profile, build-based jobs like `galloping-bot`, this means cron can silently run stale code unless the wrapper explicitly builds.
  - `6d4425a` solves that by running `compose build galloping-bot` before every wrapper execution; BuildKit cache makes unchanged runs cheap.
- New OOM investigation (unfinished):
  - New kernel OOM at **15:05:17 EDT** after the skip-training mitigation had already been deployed.
  - Victim was again Python inside a Docker scope mapped to `nba-ml-api`.
  - Killed RSS was now ~11.4 GB.
  - Scheduler label still correctly showed `python main.py pipeline --skip-training`.
  - Yet scheduler logs still showed model training output around ~13:59, implying some remaining job/process path still trains.
- Likely unresolved questions:
  1. Are there other Ofelia jobs or manual processes still invoking `python main.py pipeline` without `--skip-training`?
  2. Is the running scheduler log tail including pre-deploy/previous-job output rather than a current post-fix run?
  3. Is a different command path (`train`, `resume_pipeline`, manual `docker exec`, or another cron) causing the new OOM?
  4. Is `.State.OOMKilled=true` on `nba-ml-api` still reflecting the earlier OOM, or was it updated by the new one? Need tighter event/log correlation.
- Tool/runtime note:
  - The model switched from `gpt-5.5` to `gpt-5.4` during the session.
- Shell/session note:
  - There was a long-running shell command still active when compaction was requested:
    - `shellId: 1870`
</technical_details>

<important_files>
- `nba-ml-engine/main.py`
  - Central to the OOM mitigation.
  - Changed `pipeline()` to accept `--skip-training`.
  - Key area: pipeline command around lines ~854-1100.
  - Important because this is where daily training/pruning/calibration were skipped for memory safety.

- `nba-ml-engine/tests/test_dashboard_accuracy_followups.py`
  - Added regression tests for the new daily pipeline behavior.
  - Important because it proves daily pipeline can reuse production models without invoking training.
  - Key new tests near the top of the file after the existing ingest-help test.

- `homelab/compose/compose.nba-ml.yml`
  - Source of truth for NBA ML homelab services and Ofelia scheduler labels.
  - Changed the daily job command from:
    - `python main.py pipeline`
    - to `python main.py pipeline --skip-training`
  - Key section: `nba-ml-scheduler` labels around lines ~126-145.

- `homelab/tests/test_nba_ml_oom_guardrails.py`
  - New homelab regression/guardrail test.
  - Important because it prevents drift back to the training-heavy daily command.
  - Final version is a simple text assertion to avoid a PyYAML dependency.

- `homelab/scripts/ops/galloping-snipe.sh`
  - Central to the galloping commit review.
  - Already changed by `6d4425a`.
  - Key section: build-before-run logic around lines ~142-151.
  - Important because it fixes stale-image cron drift for a manual-profile build-based job.

- `/home/jbl/.copilot/session-state/39cb6a8f-14d7-43a7-bad1-98ec00e06033/plan.md`
  - Updated with the OOM incident summary and mitigation rationale.
  - Important for resuming the investigation context.

- `homelab/.env.example` and `homelab/compose/docker-compose.yml`
  - Read per homelab-deploy assessment rules; no changes made in this segment.
  - Important as homelab source-of-truth references for deployment/troubleshooting.

- `/tmp/copilot-tool-output-1777230416666-m70iq8.txt`
  - Captured recent scheduler/API logs and stats during the second OOM investigation.
  - Important because it appears to show training activity after the `--skip-training` deployment and should be inspected further.

- Prior logs captured during first OOM analysis:
  - `/tmp/copilot-tool-output-1777203682729-mt1lnf.txt`
  - `/tmp/copilot-tool-output-1777203695097-hzl8d7.txt`
  - Contain the first OOM timeline, scheduler tail, and host memory state.
</important_files>

<next_steps>
Remaining work:
1. **Finish root cause analysis for the new OOM at 15:05 EDT.**
   - Determine whether this was:
     - a new daily pipeline run still somehow training,
     - a weekly retrain/manual training path,
     - or stale log interpretation plus a different Python workload inside `nba-ml-api`.
2. **Correlate the new kernel OOM with exact Docker/process activity.**
   - Map the new Docker scope/container ID precisely.
   - Check if `nba-ml-api` `.State.OOMKilled=true` changed due to this new event or is just sticky from the prior incident.
3. **Inspect current/next scheduler executions after deploy.**
   - Verify what actual command Ofelia runs at execution time, not just the stored label.
   - Check for any alternate jobs or manual invocations that still call training paths.
4. **If the second OOM is a different path, create a second guardrail/fix with TDD.**
   - Possibilities include:
     - another scheduler command change,
     - stronger process isolation,
     - preventing heavy training inside the shared API container entirely,
     - or adding explicit memory-safe process separation.
5. **Re-check host memory pressure beyond Docker.**
   - The host had significant non-container Copilot/MemPalace memory usage during the first investigation; if still true, global OOM risk remains even with better container behavior.

Immediate next steps when resuming:
- Read `/tmp/copilot-tool-output-1777230416666-m70iq8.txt` in detail.
- Continue reading output from running shell session `1870` if still active.
- Compare scheduler/API logs timestamps before/after the 11:45 deploy to determine whether the training logs seen near 13:59 belong to a post-fix run.
- Inspect homelab cron/Ofelia jobs for any command besides `pipeline-daily` that could still trigger full training in `nba-ml-api`.

Blockers/open questions:
- The second OOM investigation is incomplete.
- It is not yet proven whether the new OOM came from the updated daily pipeline path or another process.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
