---
title: "Copilot Session Checkpoint: NBA ML pipeline OOM fixes"
type: text
captured: 2026-04-23T14:32:44.011176Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, mempalace, agents, dashboard]
checkpoint_class: durable-debugging
checkpoint_class_rule: "title:oom"
retention_mode: retain
status: success
---

# Copilot Session Checkpoint Export

**Checkpoint title:** NBA ML pipeline OOM fixes
**Session ID:** `703fd4bc-b327-45db-be21-124154d3f32a`
**Checkpoint file:** `/home/jbl/.copilot/session-state/703fd4bc-b327-45db-be21-124154d3f32a/checkpoints/001-nba-ml-pipeline-oom-fixes.md`
**Checkpoint timestamp:** 2026-04-23T14:30:24.685760Z
**Exported:** 2026-04-23T14:32:44.011176Z
**Checkpoint class:** `durable-debugging` (rule: `title:oom`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
Operating the homelab nba-ml-engine stack. Across this session: (1) fixed a syntax-error outage in `main.py` that had silently disabled all ofelia crons for ~2 days, (2) recovered from an OOM kill of the daily pipeline by manually completing post-training steps, (3) executed three follow-ups: cleaned up leaked mempalace MCP zombies, lowered the nba-ml-api container memory limit, and decoupled walk-forward CV from the daily pipeline so model registration is no longer gated on it. Current task: update documentation and push all changes to GitHub.
</overview>

<history>
1. User asked why nba-ml-api wasn't running ingest/training and whether ofelia crons were disabled.
   - Found crons were firing on schedule but every job failed with `SyntaxError` at `main.py:844` — a stray patch-format dump (`*** Add File: ...` markers + raw JSON of `.vscode/settings.json` and `.vscode/extensions.json`) had been pasted mid-`pipeline()` between Step 4 (Props) and Step 4b (Game Lines).
   - Confirmed `.vscode/` files already existed properly. Removed lines 844–867, rebuilt image (source baked in, not bind-mounted), recreated container, verified syntax + ran `health-check` end-to-end.

2. User reported nba-ml-api OOM and asked to diagnose, fix, and continue the run instead of restarting.
   - Container was actually still alive; only the ofelia-spawned `python main.py pipeline` subprocess was killed by host **global OOM** (`CONSTRAINT_NONE`, not memcg). Pipeline ran 07:00→12:46 UTC, completed Steps 1–4b and trained all 7 stat models (pts/reb/ast/stl/blk/tov/fg3m), died during walk-forward CV on `pts` window 2.
   - Resumed by running `docker exec nba-ml-api python main.py predict --store` (4168 predictions stored), then matview refresh + QA via inline python (all 9 matviews refreshed; 2 expected staleness errors).
   - Diagnosed root cause: 5 leaked mempalace MCP processes eating ~3.5 GB combined; mlflow at 1.2 GB; pipeline at 9.7 GB; Plex tuner triggered the kill. Suggested 3 follow-ups.

3. User asked to validate training finished and execute the recommended follow-ups.
   - **Validation finding (critical):** Disk artifacts complete for all 7 stats, BUT `model_registry` table latest entry is **2026-04-19** — registration was deferred behind the killed walk-forward CV (per `trainer.py:822`: registration only happens if NOT (USE_CV_MODEL_SELECTION AND USE_WALK_FORWARD_CV); both are True). Today's 4168 stored predictions used 4-day-old production models.
   - Discovered 24 mempalace processes (not 5). Killed 21 that were 1+ day old (SIGTERM then SIGKILL for survivors); spared 3 from today. Memory: 21→16 GB used, 9.7→14 GB available (5 GB freed).
   - Lowered `nba-ml-api` memory limit 18 GB → 12 GB in `compose/compose.nba-ml.yml`. Verified at `12884901888` bytes.
   - For walk-forward CV separation, chose cleaner approach: instead of new cron, modified `pipeline()` in `main.py` to override `USE_WALK_FORWARD_CV=False` and `USE_CV_MODEL_SELECTION=False` for the daily run. Weekly Sunday `train` cron (16:00 UTC) still does CV with selection. Side benefit: fixes the registration bug.
   - Rebuilt image and recreated container. Verified pipeline override present in container.
   - Offered 3 options to fix today's stale-prediction issue; user said no.

4. User asked to update documentation with the latest changes and push all changes to GitHub.
   - Checked git status of both repos. `homelab` has 3 modified files (only `compose.nba-ml.yml` is mine; `compose.web.yml` and `services.yaml` are pre-existing unrelated changes — leaving untouched). `nba-ml-engine` has only `main.py` modified.
   - Searched both repos for relevant documentation files.
   - Found relevant docs:
     - `/home/jbl/projects/homelab/docs/05-service-guide.md` lines 762–773 — Ofelia pipeline table
     - `/home/jbl/projects/nba-ml-engine/docs/05-training-pipeline.md` lines 33–101 — Nightly Pipeline section with cron table and step pseudocode
     - `/home/jbl/projects/nba-ml-engine/.github/skills/nba-ml-pipeline/SKILL.md` (referenced WF CV but not yet inspected)
     - `/home/jbl/projects/nba-ml-engine/docs/04-model-layer.md` (mentions walk-forward but not yet inspected for needed updates)
     - `/home/jbl/projects/nba-ml-engine/docs/07-deployment.md` (line 30 mentions scheduler jobs)
   - Was about to draft documentation updates and commit when conversation was compacted.
</history>

<work_done>
Files modified (uncommitted, unpushed):
- `/home/jbl/projects/homelab/compose/compose.nba-ml.yml`: nba-ml-api memory limit `18G` → `12G` (around line 111)
- `/home/jbl/projects/nba-ml-engine/main.py`: pipeline() now also saves/overrides/restores `USE_WALK_FORWARD_CV` and `USE_CV_MODEL_SELECTION` (set both False during daily pipeline). Edit is around lines 859–880. Earlier fix (already committed? NO — `git status` showed only main.py modified; earlier syntax-error removal of lines 844–867 also is part of this same uncommitted diff).

Verified: container running on new image with 12 GB limit, syntax OK, override present.

Operational work completed (already done, no action needed):
- [x] Killed 21 leaked mempalace MCP processes (PIDs from prior conversation: 269325, 391081, 887865, 2265499, 2394724, 2623241, 2627585, 2632863, 2652744, 2899558, 2927900, 3088122, 3406265, 3410471, 3535620, 3747285, 4022983, 4038278, 4039180, 4135390, 4188797). 5 GB freed.
- [x] 4168 predictions stored for today (2026-04-23) using stale 04-19 production models (acknowledged, not fixed per user's call).
- [x] Materialized views refreshed; QA ran (2 expected staleness errors).

Work in progress when compacted:
- [ ] Update `homelab/docs/05-service-guide.md` to mention 12 GB memory limit and that daily pipeline skips WF CV
- [ ] Update `nba-ml-engine/docs/05-training-pipeline.md` to reflect that daily `pipeline` no longer runs WF CV / CV-based selection (clearly note weekly `train` retains it)
- [ ] Possibly update `nba-ml-engine/docs/04-model-layer.md` and `.github/skills/nba-ml-pipeline/SKILL.md` if they describe WF CV as part of daily flow
- [ ] Commit + push `nba-ml-engine` (main.py + doc updates) — branch `main`, remote already configured (`origin/main` exists per log)
- [ ] Commit + push `homelab` (only `compose.nba-ml.yml` + doc updates; explicitly NOT staging `compose.web.yml` or `config/homepage/services.yaml` — those are pre-existing unrelated changes)
</work_done>

<technical_details>
- **Host topology:** CWD `/home/jbl/projects` is on the homelab server itself (not a dev machine). Docker commands and file edits affect production directly. There is no SSH hop.
- **nba-ml-engine source is baked into image** (not bind-mounted) — must `docker compose -f compose/compose.nba-ml.yml --env-file .env build nba-ml-api && ... up -d nba-ml-api` after every `main.py` edit. Models/yahoo data ARE bind-mounted at `/opt/homelab/data/nba-ml/{models,yahoo}`.
- **Registration deferral bug** (now fixed): `src/training/trainer.py:822` — `if not config.USE_CV_MODEL_SELECTION or not config.USE_WALK_FORWARD_CV: _register_best_model(...)`. With both True, registration only happens at the bottom of `train_all` after `_run_walk_forward_cv` completes. Any failure during WF CV (OOM, timeout, exception) leaves all freshly-trained models unregistered. Daily pipeline now sets both False; weekly `train` still uses defaults (both True) for CV-based selection.
- **OOM constraint type matters:** `CONSTRAINT_NONE` in dmesg = host global OOM (sum of all containers + host services exceeded RAM+swap). `CONSTRAINT_MEMCG` = container hit its own cgroup limit. The 18 GB container limit was never hit (process was at 9.7 GB anon-rss); the host (31 GB total + 8 GB swap, both saturated) was the constraint. Lowering container limit to 12 GB makes nba-ml-api the preferred OOM victim, protecting Plex/MLflow/etc.
- **Mempalace MCP leak:** Each Copilot CLI session starts a `mempalace.mcp_server` process via pipx. Many fail to clean up on session exit. Found 24 alive, 21 over a day old. Big offenders were 400 MB–982 MB each (likely accumulated chromadb caches in memory). Cleanup is safe via SIGTERM+SIGKILL by PID — never use `pkill`/`killall` (forbidden by tool rules).
- **Ofelia auto-detects container restarts** via docker socket; no scheduler reload needed after `docker compose up -d nba-ml-api`.
- **`TARGET_STATS = ["pts", "reb", "ast", "stl", "blk", "tov", "fg3m"]`** in `config.py:73`. Each stat trains 6 models (XGBoost, LightGBM, RandomForest, Ridge, CatBoost, LSTM) + Ensemble. Ensemble uses 3 folds × 5 base models = 15 base model files per stat.
- **Pipeline timing on host:** Full daily training (without WF CV) takes ~3-4 hours; with WF CV adds ~5 hours. Memory peak during training ~9.7 GB, climbs further during WF CV.
- **Schedule (UTC):** `pipeline-daily` 07:00, `props-refresh` 20:00, `predict-refresh` 22:15, `health-check` 23:00, `db-backup` 05:00, `registry-health` 12:00, `prune-registry-snapshots` 12:30, `weekly-retrain` Sun 16:00, `post-retrain-analysis` Sun 20:00, `weekly-report` Mon 14:00, `backup-verify` 1st of month 06:00.
- **Today's predictions are slightly stale** — used 04-19 production models (per user's choice not to re-register). Tomorrow's 07:00 UTC pipeline will retrain and register cleanly with the new code. Disk artifacts from today's training are intact for all 7 stats but unpromoted.
- **Pre-existing uncommitted changes in homelab** (NOT mine, leave untouched): `compose/compose.web.yml` (giniecode block being commented out) and `config/homepage/services.yaml`.
- **Git commit trailer required** by user instructions: `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`
- **Remote config:** `homelab` has `origin/main` and `origin/HEAD` (default). `nba-ml-engine` has `origin` per log (commit `0cd8051` on `main`) — verify with `git remote -v` before push.
</technical_details>

<important_files>
- `/home/jbl/projects/nba-ml-engine/main.py`
   - The Click CLI entry point. Contains `pipeline()` command (line 783+) with all 8 daily steps.
   - Modified: lines 844–867 stray patch-marker block removed (earlier in session); lines ~859–880 now save/override/restore `USE_WALK_FORWARD_CV` and `USE_CV_MODEL_SELECTION` alongside the existing OPTUNA overrides.
   - All changes uncommitted.

- `/home/jbl/projects/homelab/compose/compose.nba-ml.yml`
   - Defines `nba-ml-db`, `nba-ml-mlflow`, `nba-ml-api`, `nba-ml-scheduler` (ofelia), `nba-ml-dashboard`. Ofelia cron jobs are docker labels on `nba-ml-scheduler` (lines ~125–170).
   - Modified: line ~111 `memory: 18G` → `memory: 12G` for nba-ml-api.
   - Uncommitted; do NOT also stage `compose.web.yml` or `config/homepage/services.yaml`.

- `/home/jbl/projects/homelab/docs/05-service-guide.md`
   - Service operator's guide. NBA ML section starts around line 760. Ofelia cron table at 766–771.
   - **Needs doc update:** mention 12 GB memory limit; note daily pipeline skips WF CV (weekly does it).

- `/home/jbl/projects/nba-ml-engine/docs/05-training-pipeline.md`
   - Phase 4 training pipeline doc. Cron table lines 37–42. Pipeline pseudocode lines 44–101 lists steps 1–8 including PROMOTE/PRUNE.
   - **Needs doc update:** clarify that daily `pipeline` no longer runs walk-forward CV nor CV-based selection (registration is now immediate via single-split val_mse); weekly `train` retains both. Possibly add a note explaining why (OOM resilience + registration-blocking bug).

- `/home/jbl/projects/nba-ml-engine/docs/04-model-layer.md`
   - Mentions walk-forward CV (per earlier grep). Not yet inspected for whether updates are needed.

- `/home/jbl/projects/nba-ml-engine/.github/skills/nba-ml-pipeline/SKILL.md`
   - Skill description for the agent. Mentions WF CV. Not yet inspected.

- `/home/jbl/projects/nba-ml-engine/src/training/trainer.py`
   - The deferred-registration logic lives at line 822 (`if not USE_CV_MODEL_SELECTION or not USE_WALK_FORWARD_CV`). Walk-forward CV invocation at line 833+. Useful reference; not modified.

- `/home/jbl/projects/nba-ml-engine/config.py`
   - `TARGET_STATS` line 73; `PIPELINE_OPTUNA_TRIALS`/`PIPELINE_OPTUNA_TIMEOUT` lines 103–104; `PIPELINE_TOTAL_TIMEOUT` line 125 (43200 = 12h). Not modified.
</important_files>

<next_steps>
Remaining work (in order):

1. **Update `nba-ml-engine/docs/05-training-pipeline.md`** — modify the Nightly Pipeline section (around lines 33–42 + the step list) to note:
   - Daily `pipeline` runs without walk-forward CV and CV-based selection (registration is immediate via single-split val_mse selection per stat)
   - Weekly Sunday `train` still uses WF CV + CV selection for the canonical promotion check
   - Brief rationale: avoids 5+ hour runtime, prevents registration starvation if CV fails

2. **Optionally update `nba-ml-engine/docs/04-model-layer.md` and `.github/skills/nba-ml-pipeline/SKILL.md`** — only if they describe WF CV as part of daily flow. View them first; only edit if inaccurate.

3. **Update `homelab/docs/05-service-guide.md`** — around the NBA ML section (line 760+) note the 12 GB container memory limit and mirror the WF CV daily/weekly split clarification.

4. **Commit + push `nba-ml-engine`:**
   ```
   cd /home/jbl/projects/nba-ml-engine
   git add main.py docs/05-training-pipeline.md  [+ any other docs touched]
   git commit -m "fix(pipeline): remove stray patch markers; skip walk-forward CV in daily pipeline
   
   - Remove accidentally-pasted '*** Add File' markers + .vscode JSON dump that
     broke main.py syntax and silently failed all ofelia crons for ~2 days
   - In pipeline(), override USE_WALK_FORWARD_CV=False and USE_CV_MODEL_SELECTION=False
     so daily training registers models immediately (was deferred behind WF CV per
     trainer.py:822, leading to unpromoted models when CV OOM'd or timed out).
     Weekly Sunday 'train' cron retains CV+selection for canonical promotion.
   
   Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
   git push origin main
   ```

5. **Commit + push `homelab`:** stage ONLY `compose/compose.nba-ml.yml` and any doc edits — explicitly skip `compose/compose.web.yml` and `config/homepage/services.yaml` (pre-existing unrelated work).
   ```
   cd /home/jbl/projects/homelab
   git add compose/compose.nba-ml.yml docs/05-service-guide.md
   git commit -m "compose(nba-ml): lower nba-ml-api memory limit 18G→12G
   
   Tighter cgroup makes nba-ml-api the preferred OOM victim instead of
   triggering host global OOM that affected Plex/MLflow/etc. Today's
   training peak was ~9.7GB (well under 12G); WF CV peaks higher but
   has been moved to weekly-only so daily pipeline stays comfortably
   within the new limit.
   
   Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
   git push origin main
   ```

Open questions / blockers:
- None. User has explicitly approved the doc-update + push.
- Git push will go via whatever auth the user has configured (likely SSH); no action needed unless push fails.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
