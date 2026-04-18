---
title: "Copilot Session Checkpoint: Training status tracker and OOM fix"
type: text
captured: 2026-04-18T01:37:38.386572Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, dashboard]
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Training status tracker and OOM fix
**Session ID:** `ec0258d6-d944-425d-b53d-e471288a1230`
**Checkpoint file:** `/home/jbl/.copilot/session-state/ec0258d6-d944-425d-b53d-e471288a1230/checkpoints/002-training-status-tracker-and-oo.md`
**Checkpoint timestamp:** 2026-04-13T15:52:12.003536Z
**Exported:** 2026-04-18T01:37:38.386572Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user is managing a homelab (Beelink i9-13900HK/32GB/914GB) running ~43 Docker containers. This conversation segment focused on three things: (1) fixing Qdrant showing as "down" on the Homepage dashboard, (2) building a real-time NBA ML training pipeline status tracker with a Homepage card, and (3) handling an OOM crash on the nba-ml-api container during training. The approach involved diagnosing network connectivity issues, building a new status tracking system across the nba-ml-engine codebase, and responding to memory pressure during full model training.
</overview>

<history>
1. User reported Qdrant showing as down on homepage despite running
   - Diagnosed: Homepage container is on `proxy` network, Qdrant is on `compose_memory` network — hostname `qdrant:6333` couldn't resolve
   - Fixed `siteMonitor` in services.yaml from `http://qdrant:6333` to `http://{{HOMEPAGE_VAR_SERVER_IP}}:6333` (uses host-mapped port)
   - Deployed via rsync + container restart, committed as `14bd900` to homelab repo

2. User requested a training pipeline status card under Analytics on homepage
   - Investigated NBA ML pipeline structure: 12 stages total (Minutes Model → 9 stat models → Over/Under Classifiers → Confidence Calibrator)
   - Created `src/training/status.py` — lightweight JSON file tracker with atomic writes to `/tmp/training_status.json`
   - Modified `src/training/trainer.py` — added status hooks into `train_pipeline()` and `train_all()` to track per-stage progress
   - Added `GET /training/status` endpoint to `src/api/server.py` — public endpoint returning pre-formatted fields (`status_label`, `stage_display` like "5/12", `stage_name`, `elapsed_minutes`, `last_trained`)
   - Added `/training/status` to `_PUBLIC_PATHS` so Homepage can hit it without API key auth
   - Added Training Pipeline card to Analytics section in homepage services.yaml using `customapi` widget
   - Rebuilt nba-ml-api Docker image (`docker compose build nba-ml-api`) and restarted container
   - Verified endpoint returns correct idle state with last training date from model_registry
   - Committed to nba-ml-engine (`6c01391`) and homelab (`d119ab0`)

3. User asked to check if training is active and continue if killed
   - Discovered training was NOT running — our container rebuild killed the process that had been running since ~7am UTC daily cron
   - The April 11 training had completed all 9 stat models; no April 13 models existed in registry
   - First mistakenly started `python main.py pipeline` which restarts from Step 1 (data ingestion)
   - User caught this — pointed out training had been running since before 8am EDT
   - Stopped the pipeline, started `python main.py train --full-pipeline` instead (skips ingestion, goes straight to training)
   - Verified status tracker showed "Training · 1/12 · Minutes Model" and progressed to "2/12 · Stat: pts"

4. User reported nba-ml-api container OOM notification
   - Confirmed: `OOMKilled: true`, training process dead (docker exec -d doesn't survive container restart)
   - Status file still showed "running: true" because `finish_pipeline()` never called
   - Minutes Model completed and saved (`MinutesModel_minutes` version `20260413_113421`), OOM happened during Stat: pts
   - Root cause: `PIPELINE_MODE=false` — full Optuna tuning with uncapped trials on pts stat exceeded 14GB limit
   - Host swap fully exhausted (8.0/8.0 GB)
   - Applied runtime fix: `docker update --memory 18g --memory-swap 20g nba-ml-api`
   - Was about to add `PIPELINE_MODE=true` to compose env and persist memory bump when compaction occurred
</history>

<work_done>
Files created:
- `/home/jbl/projects/nba-ml-engine/src/training/status.py`: New training status tracker module

Files modified:
- `/home/jbl/projects/nba-ml-engine/src/training/trainer.py`: Added status tracking hooks to `train_pipeline()` and `train_all()`
- `/home/jbl/projects/nba-ml-engine/src/api/server.py`: Added `/training/status` endpoint, added to `_PUBLIC_PATHS`
- `/home/jbl/projects/homelab/config/homepage/services.yaml`: Fixed Qdrant siteMonitor, added Training Pipeline card
- `/home/jbl/projects/homelab/compose/compose.nba-ml.yml`: **NOT YET MODIFIED** — needs memory bump + PIPELINE_MODE

Git commits pushed:
- homelab `14bd900`: Fix Qdrant siteMonitor to use host IP
- nba-ml-engine `6c01391`: Training status tracker + API endpoint
- homelab `d119ab0`: Training Pipeline card in Analytics section

Runtime changes applied but NOT persisted to compose:
- `docker update --memory 18g --memory-swap 20g nba-ml-api` (compose still says 14G)

Current state:
- Training process is DEAD (OOM killed during Stat: pts)
- Only MinutesModel_minutes saved from today's run
- Container is running (restarted by Docker) at 5.3GB/18GB memory
- Status file incorrectly shows "running: true" — needs cleanup before restarting
- `PIPELINE_MODE` is still `false` — must be enabled to prevent another OOM
- Homepage card is deployed and working (showing stale "Training" state from status file)

Work in progress:
- [ ] Persist memory bump (14G → 18G) in compose.nba-ml.yml
- [ ] Add `PIPELINE_MODE=true` to compose.nba-ml.yml environment
- [ ] Clear stale status file
- [ ] Restart training with pipeline mode enabled
- [ ] Verify training completes without OOM
</work_done>

<technical_details>
- **Training pipeline stages**: 12 total in full mode: Minutes Model → pts, reb, ast, stl, blk, tov, fg_pct, ft_pct, fg3m → Over/Under Classifiers → Confidence Calibrator. In PIPELINE_MODE, fg_pct and ft_pct are skipped (10 stages), and Optuna uses lighter settings (10 trials, 60s timeout).
- **PIPELINE_MODE env var**: `config.PIPELINE_MODE = os.getenv("PIPELINE_MODE", "false").lower() == "true"`. Controls: (1) which stats to skip (`PIPELINE_SKIP_STATS`), (2) Optuna trial count/timeout, (3) lighter tuning overall. NOT set by `--full-pipeline` CLI flag — it's purely an env var.
- **OOM root cause**: Full Optuna tuning (uncapped trials) on pts stat with 14GB limit. The feature matrix for all 587 players across seasons + multiple concurrent Optuna trials exceeded memory. PIPELINE_MODE (10 trials, 60s timeout) should prevent this.
- **Status tracker design**: Writes JSON atomically to `/tmp/training_status.json` via temp file + `os.replace()`. The API endpoint reads this file + enriches with `model_registry` data for last training date. Limitation: if process is OOM-killed, `finish_pipeline()` never runs and status file shows stale "running: true".
- **docker exec -d limitation**: Background processes started via `docker exec -d` don't survive container restarts. If the container OOMs and restarts, the training process is gone.
- **Homepage customapi widget**: Uses simple field string mappings. Complex display formatting must be done server-side. The API returns pre-formatted `status_label` ("Training"/"Idle"/"Failed"), `stage_display` ("5/12" or "Last: 2d ago"), and `stage_name`.
- **Network isolation issue**: Homepage is on `proxy` network. Services on other networks (like `compose_memory` for Qdrant) are unreachable by hostname. Use `{{HOMEPAGE_VAR_SERVER_IP}}:<host_port>` for siteMonitor URLs when networks don't overlap.
- **nba-ml-api image is built, not pulled**: Source at `${NBA_ML_ENGINE_PATH}` (resolves to `../../nba-ml-engine` relative to compose dir). Changes to Python source require `docker compose build nba-ml-api` + restart. Models/data are bind-mounted, but code is baked into image.
- **Host memory state**: 32GB total, ~16GB used, swap 8.0/8.0 GB exhausted. With nba-ml-api at 18GB limit, total container memory limits likely exceed physical RAM. Need to be careful about concurrent heavy workloads.
- **`train --full-pipeline` vs `pipeline`**: `pipeline` runs the full 8-step daily flow (ingest → injuries → props → lines → **train** → predict → matview → health). `train --full-pipeline` calls `train_pipeline()` directly (minutes → stats → classifiers → calibrator). Use `train` when data is already fresh.
- **`resume` command**: Only does CV + classifiers — skips stat model training entirely. Only useful when stat models are already trained and saved. Not suitable for recovering from an OOM mid-training.
- **Compose env file**: `/home/jbl/projects/homelab/.env` — loaded by deploy.sh with `set -a && source .env`. Must be sourced before running docker compose commands manually.
</technical_details>

<important_files>
- `/home/jbl/projects/nba-ml-engine/src/training/status.py`
   - New file: training pipeline status tracker
   - Provides `start_pipeline()`, `advance_stage()`, `complete_stage()`, `finish_pipeline()`, `read_status()`
   - Writes atomically to `/tmp/training_status.json`
   - ~90 lines

- `/home/jbl/projects/nba-ml-engine/src/training/trainer.py`
   - Core training orchestrator, ~1340 lines
   - `train_pipeline()` at line ~1078: added status tracking imports, stage list builder, try/except wrapper with `finish_pipeline(error=...)` on failure
   - `train_all()` at line ~425: added `_status_offset` and `_stages` kwargs for per-stat tracking; calls `advance_stage()`/`complete_stage()` in the stat loop
   - Key indentation fix: the `with _training_timeout` block under the new `try:` wrapper needed 12-space indent (3 levels: function + try + with)

- `/home/jbl/projects/nba-ml-engine/src/api/server.py`
   - FastAPI server, ~1600+ lines
   - `_PUBLIC_PATHS` at line 67: added `/training/status`
   - `training_status()` endpoint at line ~757: reads status file, enriches with model_registry last_trained, formats display fields
   - Returns: `status_label`, `stage_display`, `stage_name`, `current_stage`, `total_stages`, `completed`, `elapsed_minutes`, `error`, `last_trained`

- `/home/jbl/projects/homelab/config/homepage/services.yaml`
   - Homepage dashboard config, ~300 lines
   - Line ~106: Fixed Qdrant siteMonitor URL (was `http://qdrant:6333`, now `http://{{HOMEPAGE_VAR_SERVER_IP}}:6333`)
   - Line ~113: New Training Pipeline card with customapi widget pointing to `http://nba-ml-api:8000/training/status`, 30s refresh

- `/home/jbl/projects/homelab/compose/compose.nba-ml.yml`
   - NBA ML stack compose, ~180 lines
   - nba-ml-api service at line 65: needs `PIPELINE_MODE=true` added to environment (~line 93) and memory bumped from 14G to 18G (line 110)
   - **NOT YET MODIFIED** — runtime docker update applied but compose not updated

- `/home/jbl/projects/homelab/.env`
   - Line 130: `NBA_ML_ENGINE_PATH=../../nba-ml-engine` — build context for nba-ml-api
   - Must source this before manual docker compose commands

- `/home/jbl/projects/nba-ml-engine/config.py`
   - Line 73: `TARGET_STATS` — the 9 stats that define training stages
   - Line 113: `PIPELINE_MODE` env var check
   - Line 117-118: `PIPELINE_SKIP_STATS` defaults to "fg_pct,ft_pct"
</important_files>

<next_steps>
Remaining work (in order):
1. **Persist compose changes**: Update `compose.nba-ml.yml` — bump nba-ml-api memory from `14G` to `18G` (line 110), add `PIPELINE_MODE=true` to environment section (after line 93)
2. **Clear stale status file**: `docker exec nba-ml-api rm /tmp/training_status.json` or write an idle status
3. **Restart training**: `docker exec -d nba-ml-api python main.py train --full-pipeline` — with PIPELINE_MODE now true, it'll use 10 trials/60s Optuna and skip fg_pct/ft_pct (10 stages instead of 12)
4. **Wait, but PIPELINE_MODE is baked into the image** — need to either: (a) add env var to compose and redeploy (which rebuilds/restarts), or (b) pass it directly: `docker exec -d -e PIPELINE_MODE=true nba-ml-api python main.py train --full-pipeline`
5. **Monitor**: Verify training passes Stat: pts without OOM, check Homepage card updates
6. **Commit compose changes**: After verifying training completes, commit updated compose.nba-ml.yml

Key concern: With 18GB limit on nba-ml-api + other containers, total memory limits may exceed 32GB physical. Swap is already exhausted. May need to evaluate if 18GB is actually needed with PIPELINE_MODE enabled (lighter Optuna = less memory), or if 16GB would suffice.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
