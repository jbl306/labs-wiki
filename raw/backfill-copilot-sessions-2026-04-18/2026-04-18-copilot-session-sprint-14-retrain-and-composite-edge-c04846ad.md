---
title: "Copilot Session Checkpoint: Sprint 14 retrain and composite edge"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, dashboard]
status: pending
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint 14 retrain and composite edge
**Session ID:** `94eedf26-380e-451c-89d2-f703046de219`
**Checkpoint file:** `/home/jbl/.copilot/session-state/94eedf26-380e-451c-89d2-f703046de219/checkpoints/010-sprint-14-retrain-and-composit.md`
**Checkpoint timestamp:** 2026-03-23T21:22:54.825832Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user is building an NBA ML prediction engine with a React dashboard. This session focuses on Sprint 14: validating Sprint 13 model improvements (minutes model, edge optimizer, dynamic ensemble, O/U classifiers), triggering a pipeline retrain, implementing composite edge signals, and generating an evaluation report with per-stat improvement analysis. We're on the homelab server directly, implementing code changes while a pipeline-mode retrain runs in the background.
</overview>

<history>
1. Prior context (from compaction): Built NBA ML Engine across sprints 9-13. Sprint 13 added MinutesModel, edge threshold optimizer with Kelly criterion, dynamic ensemble weighting, binary over/under classifiers, and training speed optimization. All code was committed but never retrained — production models are still from Sprint 12 (3/22). React dashboard replaced Streamlit. Rankings/backtest pages optimized (22.5s→0.7s→1ms cached). All merged to main.

2. User asked to validate Sprint 13 features in model metadata, create new branch/plan from Sprint 13 next steps, implement with progress tracker, deploy, validate, and generate report
   - Validated: NO Sprint 13 features reflected in models — no retrain happened since 3/22
   - Found weekly retrain missed: scheduler started at 13:39 UTC, retrain cron at 16:00 UTC Sunday, but API container was recreated at 18:25 UTC (after retrain window), likely killing the running retrain
   - Only MinutesModel_minutes was in registry from a prior partial run (R²=0.536)
   - No over/under classifiers, no dynamic ensemble weights in production models
   - Explored codebase: read sprint13 report next steps, main.py train command, trainer.py, config.py, edge_optimizer.py, predictor.py, prop_finder.py, server.py, dashboard BFF
   - Created Sprint 14 plan with 22 todos across 6 phases
   - Merged Sprint 13 PR (already merged), pulled main, created `feature/sprint-14-evaluation-improvements` branch from main (commit 5669637)
   - Wired `main.py train` command to use `train_pipeline()` by default (full pipeline: minutes → stats → classifiers), with `--stat`/`--model` flags falling back to `train_all()`
   - Added `--full-pipeline` flag to train command
   - Rebuilt API container and started it
   - Discovered 2 stale training processes (from earlier aborted runs) competing for 99% CPU each
   - Killed stale processes by restarting the container
   - Started clean pipeline-mode retrain: `docker exec -d -e PIPELINE_MODE=true -e PYTHONUNBUFFERED=1 nba-ml-api bash -c "python main.py train > /tmp/train.log 2>&1"`
   - Training is actively running: Minutes model completed (R²=0.536), now in Step 2 (stat models), currently training XGBoost/pts with Optuna (10 trials/60s timeout in pipeline mode)
   - While training runs, implemented composite edge signal:
     - Added `get_classifier_prob()` and `_ensure_classifiers_loaded()` to Predictor class
     - Modified `prop_finder.py` to compute `composite_edge` (60% regression + 40% classifier signal) and include `classifier_prob`
     - Updated `PropEdge` pydantic model in server.py with `composite_edge` and `classifier_prob` fields
     - Updated prop-edges FastAPI endpoint to pass through new fields
     - Added `optimize-edges` CLI command to main.py
   - Was about to check training progress and continue with dashboard BFF updates when compaction triggered
</history>

<work_done>
Files modified this session:
- `main.py` — Rewired `train()` command to use `train_pipeline()` by default; added `--full-pipeline` flag; added `optimize-edges` CLI command
- `src/inference/predictor.py` — Added `_classifiers` dict to __init__, `_ensure_classifiers_loaded()` lazy loader, `get_classifier_prob()` method
- `src/applications/prop_finder.py` — Added composite edge calculation (60% regression + 40% classifier), `classifier_prob` field, sort by `composite_edge`
- `src/api/server.py` — Added `composite_edge: float | None` and `classifier_prob: float | None` to `PropEdge` model; updated prop-edges endpoint response

Files NOT yet modified (planned):
- `dashboard-ui/server/src/index.ts` — BFF still uses regression-only edge from SQL; composite edge available via FastAPI only

Work completed:
- [x] Phase 0: Merge Sprint 13, create branch, wire train_pipeline
- [x] Phase 4a: Composite edge signal implementation
- [x] Phase 4b: Predictor composite edge integration
- [x] Partial Phase 4c: FastAPI endpoint updated (BFF not yet)
- [x] Added optimize-edges CLI command

Work in progress:
- [ ] Phase 1: Pipeline retrain RUNNING (~17:17 UTC start, currently training stat models with Optuna)
- [ ] Phase 4c: Dashboard BFF wire-up for composite edge (not started)

Work pending:
- [ ] Phase 2: Evaluate Sprint 13 impact (needs retrain completion)
- [ ] Phase 3: Edge threshold tuning (needs retrain completion)
- [ ] Phase 5: Deploy, validate, report

Current state:
- Training IS running in background inside nba-ml-api container (PID 1629367, 99% CPU)
- Training log at /tmp/train.log inside container — last output shows Optuna tuning XGBoost/pts
- Minutes model already registered (MinutesModel_minutes, R²=0.536, MAE=4.78)
- API container has OLD code (before this session's changes) — needs rebuild after training completes
- Code changes are on local branch `feature/sprint-14-evaluation-improvements` but NOT committed yet
- Dashboard container (port 8501) is running with old code
</work_done>

<technical_details>
**Architecture:**
- Two repos: `homelab` (/home/jbl/projects/homelab) manages Docker compose; `nba-ml-engine` (/home/jbl/projects/nba-ml-engine) is the ML + dashboard codebase
- BFF pattern: Express server at dashboard-ui/server/ proxies some calls to FastAPI and queries PostgreSQL directly
- Docker: multi-stage build, ports 8000 (FastAPI API) and 8501 (dashboard BFF + React)
- Caddy reverse proxy in front

**Training pipeline:**
- `train_pipeline()` orchestrates: minutes model → stat models → O/U classifiers
- PIPELINE_MODE uses 10 Optuna trials / 60s timeout (vs 50/300s full mode), skips fg_pct/ft_pct
- Training env var must be set on the `docker exec` command: `-e PIPELINE_MODE=true`
- Checking config from a separate `docker exec python -c` won't see the env var (different process)
- Full training: ~12 hours. Pipeline mode: estimated 1-3 hours
- Training output is buffered by docker exec — must use `> /tmp/train.log 2>&1` with `-d` flag and tail the log

**Killing container processes:**
- Container has no `kill` or `ps` commands (slim Python image)
- Can use `docker exec python -c "import os, signal; os.kill(PID, signal.SIGTERM)"` but PID namespace differs
- Host PIDs shown by `docker top` require sudo to kill
- Safest: `docker compose restart nba-ml-api` to kill all stale processes

**DB Schema (learned hard way):**
- `predictions.stat_name` (not stat_type), `prop_lines.stat_name` (not stat_type)
- `model_registry` has NO `stat_name` column — stat is embedded in `model_name` field (e.g., "EnsembleModel_pts")
- `game_logs.player_id` joins to `players.id` (auto-increment PK), NOT `players.nba_api_id`
- pg NUMERIC/ROUND returns strings — must use `numericRow()` helper in BFF

**Edge calculation flow:**
- FastAPI `/prop-edges`: calls `prop_finder.find_edges()` → uses Predictor + PropLine join → regression edge = `(predicted - line) / line`
- BFF `/api/props`: queries predictions + prop_lines directly from PostgreSQL, calculates edge in SQL
- Two separate edge paths — FastAPI now has composite_edge, BFF still uses regression-only
- Edge thresholds: per-stat from `config.STAT_EDGE_THRESHOLDS`, overridden by `OPTIMIZED_EDGE_THRESHOLDS`
- EdgePolicy: served from FastAPI `/edge-policy`, cached 10min in BFF

**Composite edge formula:**
```python
composite_edge = 0.6 * abs_edge + 0.4 * classifier_signal
# where classifier_signal = abs(P(over) - 0.5) * 2  (0-1 scale)
```

**Current production baseline (pre-Sprint 14 retrain):**
- Overall prop hit rate: 52.8% (2,299 props)
- Best: STL 64.6%, BLK 61.3%  
- Worst: PTS 50.6%, AST 51.6%
- High-edge (≥2.0) hit rate: 51.3% — flat threshold doesn't help
- 9 production models, all from 3/21-3/22

**Deployment:**
```bash
cd /home/jbl/projects/homelab && docker compose -f compose/compose.nba-ml.yml --env-file .env build --no-cache nba-ml-api && docker compose -f compose/compose.nba-ml.yml --env-file .env up -d nba-ml-api
```

**Node.js:** v20.20.1 via nvm. Must source: `export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"`

**Main branch state:** commit 5669637, includes Sprint 13 code + waiver/yahoo features + confidence metrics
</technical_details>

<important_files>
- `main.py` (~480 lines)
  - CLI entry point — train, evaluate, pipeline, predict, optimize-edges commands
  - MODIFIED: train() now uses train_pipeline() by default, added optimize-edges command
  - Key: lines 114-163 (train command), lines 358-381 (optimize-edges)

- `src/inference/predictor.py` (~340 lines)
  - Loads production models, generates predictions, edge thresholds
  - MODIFIED: Added _classifiers lazy dict, _ensure_classifiers_loaded(), get_classifier_prob()
  - Key: lines 70-74 (init with _classifiers), lines 278-338 (classifier methods)

- `src/applications/prop_finder.py` (~195 lines)  
  - Finds prop edges by comparing predictions vs sportsbook lines
  - MODIFIED: Added composite_edge calculation, classifier_prob field, sort by composite_edge
  - Key: lines 105-149 (composite edge block)

- `src/api/server.py` (~400 lines)
  - FastAPI application with all endpoints
  - MODIFIED: PropEdge model + prop-edges endpoint include composite_edge and classifier_prob
  - Key: lines 83-95 (PropEdge model), lines 361-375 (prop-edges response)

- `src/training/trainer.py` (~730 lines)
  - Training orchestration — train_all(), train_pipeline(), train_minutes_model(), train_over_under_classifiers()
  - Not modified this session (was modified in Sprint 13)
  - Key: lines 636-675 (train_pipeline), lines 202-250 (train_all)

- `config.py` (~200 lines)
  - All configuration flags including Sprint 13 additions
  - Not modified this session
  - Key flags: PIPELINE_MODE, USE_MINUTES_MODEL, USE_OVER_UNDER_CLASSIFIER, ENSEMBLE_WEIGHT_MODE, USE_OPTIMIZED_THRESHOLDS

- `dashboard-ui/server/src/index.ts` (~1200 lines)
  - Express BFF server with cached() helper, all dashboard API endpoints
  - NOT YET modified — still uses regression-only edge from SQL
  - Key: lines 470-530 (props query with edge_pct), lines 142-156 (edge policy fetch)

- `src/evaluation/edge_optimizer.py` (221 lines)
  - Walk-forward CV threshold optimization + Kelly criterion
  - Not modified this session (created in Sprint 13)
  - Key: optimize_thresholds(), kelly_bet_size(), format_optimized_thresholds()

- `src/models/over_under_model.py` (252 lines)
  - Binary over/under classifier with isotonic calibration
  - Not modified this session (created in Sprint 13)
</important_files>

<next_steps>
**Immediate (training still running):**
1. Monitor training log: `docker exec nba-ml-api tail -20 /tmp/train.log`
   - Training started ~17:17 UTC, currently on stat models (XGBoost/pts Optuna)
   - Estimated completion: 1-3 hours from start (pipeline mode)

**After training completes:**
2. Phase 1b-1e: Validate retrain results
   - Check model_registry for new models trained today (3/23)
   - Verify MinutesModel registered, stat models have predicted_minutes feature
   - Check if over/under classifiers were trained
   - Check ensemble config_snapshot for weight_mode

3. Phase 2: Evaluate Sprint 13 impact
   - Compare R²/MAE per stat (Sprint 12 baseline vs Sprint 14 models)
   - Run feature importance to check predicted_minutes ranking
   - Evaluate classifier AUC if classifiers trained

4. Phase 3: Edge threshold tuning
   - Run `optimize-edges` command (walk-forward CV)
   - Set per-stat optimized thresholds
   - Backtest with optimized vs flat thresholds

5. Phase 5: Deploy and validate
   - Commit all Sprint 14 code changes
   - Rebuild API container with new code (main.py, predictor.py, prop_finder.py, server.py changes)
   - Rebuild dashboard container if BFF changes needed
   - Test all endpoints
   - Generate sprint 14 report under docs/reports/

**SQL Todo Status:**
- 3 done (0a, 0b, 0c)
- 3 in_progress (1a, 4a, 4b)
- 16 pending (blocked on retrain completion)

**Uncommitted local changes on feature/sprint-14-evaluation-improvements:**
- main.py (train command rewrite + optimize-edges)
- src/inference/predictor.py (classifier loading + get_classifier_prob)
- src/applications/prop_finder.py (composite edge)
- src/api/server.py (PropEdge model + endpoint)
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
