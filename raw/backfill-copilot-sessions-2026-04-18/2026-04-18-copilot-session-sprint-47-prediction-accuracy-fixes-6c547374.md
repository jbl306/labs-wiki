---
title: "Copilot Session Checkpoint: Sprint 47 prediction accuracy fixes"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard]
status: pending
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint 47 prediction accuracy fixes
**Session ID:** `3886f473-b7ba-404a-91b6-48620b845d83`
**Checkpoint file:** `/home/jbl/.copilot/session-state/3886f473-b7ba-404a-91b6-48620b845d83/checkpoints/001-sprint-47-prediction-accuracy.md`
**Checkpoint timestamp:** 2026-04-06T00:10:46.897001Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user requested a full evaluation sprint (Sprint 47) of the NBA ML Engine after a weekly retrain completed. The focus is on prediction accuracy lagging the vig (52.4% breakeven at -110 odds), checking for bugs, data accuracy, completeness, and stale code. I'm executing the "execute-sprint-from-report" skill workflow: auditing the system, creating a sprint branch, implementing fixes, testing, deploying, and writing a follow-up report. Environment is server mode (hostname beelink-gti13), operating directly on the homelab.
</overview>

<history>
1. User requested full ML engine and dashboard evaluation, noting predictions lag the vig
   - Invoked `execute-sprint-from-report` skill
   - Read AGENTS.md (doesn't exist), tasks/lessons.md, latest sprint report (sprint46), git state
   - Confirmed: server mode (beelink-gti13), on `main` branch, clean working tree, latest sprint is 46

2. Launched 5 parallel audit agents to comprehensively analyze the system:
   - `audit-model-performance` (task agent) — checked API health, DB stats, model files
   - `audit-prediction-pipeline` (explore agent) — code review of predictor, trainer, models
   - `audit-data-pipeline` (explore agent) — code review of ingestion, prop lines, features
   - `audit-dashboard-bff` (explore agent) — BFF SQL queries, dashboard display
   - `audit-evaluation-system` (explore agent) — evaluation gaps, backtesting, calibration

3. Ran direct DB queries to measure actual performance:
   - Discovered `predictions` table has `confidence_low`/`confidence_high` columns (NOT `confidence`)
   - DB connection module is `src.db.connection` (not `src.db.session`)
   - Got comprehensive 30-day hit rate data showing pts at 49.9%, reb at 51.2% — both below vig
   - **Critical finding**: Inverse edge-accuracy relationship (larger edges = WORSE hit rates)

4. Collected all 5 audit reports with extensive findings. Key issues:
   - **24 prediction pipeline issues** (3 HIGH, 11 MEDIUM, 10 LOW)
   - **11 data pipeline issues** (2 CRITICAL, 3 HIGH, 6 MEDIUM)
   - **9 BFF/dashboard issues** (1 CRITICAL, 2 HIGH, 6 MEDIUM)
   - **Comprehensive evaluation gaps** (CLV oversimplified, no walk-forward backtest, etc.)

5. Created sprint branch `feature/sprint-47-prediction-accuracy-audit` and progress tracker
   - Created `tasks/PROGRESS-sprint47-prediction-accuracy-0405.md`
   - Inserted 16 todos with dependencies into SQL tracking

6. Implemented fixes across 3 phases (12 tasks completed):
   - Phase 1: Critical prediction pipeline fixes (4 tasks)
   - Phase 2: BFF data accuracy fixes (4 tasks)
   - Phase 3: Model quality guardrails (3 tasks)
   - Phase 4: Stale code cleanup (1 task — fg_pct/ft_pct already excluded)

7. Ran validation:
   - pytest: 234 passed, 9 skipped, 14 deselected ✅
   - BFF TypeScript: `tsc --noEmit` clean ✅
   - Dashboard Vite build: successful ✅

8. Started deployment — `docker compose build --no-cache nba-ml-api` is currently running (shellId: 209)
</history>

<work_done>
Files modified:
- `src/inference/predictor.py`: Fixed negative prediction clamping — now shifts CI by same amount instead of breaking intervals. Fixed in 4 locations (single predict, batch predict, shadow production, challenger models).
- `src/data/game_lines.py`: Added `ZoneInfo("America/New_York")` import and conversion for game commence_time → game_date extraction. Prevents off-by-one for evening games.
- `src/data/prop_lines.py`: Changed default line from `0.0` to `None` (line 437). Upgraded prop rejection logging from DEBUG to INFO (line 592).
- `config.py`: Lowered MIN_EDGE_THRESHOLD from 0.08 to 0.02. Lowered MIN_CONFIDENCE_THRESHOLD from 0.65 to 0.55. Reduced all STAT_EDGE_THRESHOLDS (pts: 0.10→0.04, reb/ast: 0.08→0.03, stl/blk: 0.05→0.03, tov: 0.08→0.04, fg3m: 0.08→0.04).
- `src/applications/prop_finder.py`: Fixed CI sigma calculation to use per-stat percentile z-scores from `config.STAT_CALIBRATION_PERCENTILES` instead of hardcoded 1.2816 (which assumes 80% CI). Added `from scipy.stats import norm`.
- `src/training/trainer.py`: Added vig-adjusted guardrail in `_register_best_model()` — refuses promotion if test_r2 < 0.
- `src/evaluation/backtester.py`: Added `"minutes": "minutes"` to `_STAT_COLUMN_MAP`.
- `dashboard-ui/server/src/index.ts`: Fixed 2 primary_props CTEs (lines ~397, ~1693) to include `pl.source` in DISTINCT ON. Fixed hit rate trend query to deduplicate by source using CTE. Fixed settlement DISTINCT ON to include `pls.source`. Added error logging for settlement failures. Added starting balance point to bankroll simulation curve.

Files created:
- `tasks/PROGRESS-sprint47-prediction-accuracy-0405.md`: Sprint progress tracker

Work completed:
- [x] Fix negative prediction clamping (clamp before CI)
- [x] Fix game_lines timezone off-by-one
- [x] Fix prop line default 0.0 value
- [x] Fix BFF alt-line DISTINCT ON queries (2 locations)
- [x] Fix BFF hit rate query deduplication
- [x] Fix BFF settlement DISTINCT ON
- [x] Fix BFF bankroll simulation starting balance
- [x] Add vig-adjusted model promotion guardrail
- [x] Make edge thresholds vig-aware (lowered significantly)
- [x] Fix CI sigma for per-stat percentile ranges
- [x] Fix silent prop rejection logging
- [x] Add minutes to backtester stat map
- [x] Validation: pytest (234 passed), tsc clean, vite build clean

In progress:
- [ ] Deploy to homelab — `docker compose build --no-cache nba-ml-api` running (shellId: 209)
- [ ] Deploy dashboard container
- [ ] Verify live behavior
- [ ] Write sprint report
- [ ] Code review
- [ ] Commit and push
</work_done>

<technical_details>
**30-Day Performance Data (Critical Baseline):**
- pts: 49.9% hit rate (958 props, MAE 7.30) — BELOW 50%, highest volume
- reb: 51.2% (1244 props) — below 52.4% vig
- ast: 52.1% (756 props) — marginal
- fg3m: 54.2% (859 props) — above vig ✅
- stl: 66.4% (253 props) — above vig ✅
- blk: 55.4% (83 props) — above vig, small sample

**Inverse Edge-Accuracy (ROOT CAUSE of lagging vig):**
- 0-1 edge: 53.4% (3088 bets) — BEST bucket
- 1-2 edge: 52.5% (640 bets)
- 2-3 edge: 48.5% (198 bets) — below random!
- 5+ edge: 47.9% (163 bets) — WORST
This means the old 8% threshold was filtering OUT the best bets and keeping the worst.

**Schema details:**
- `predictions` table: player_id, game_date, model_name, stat_name, model_version, predicted_value, confidence_low, confidence_high, created_at (NO `confidence` column)
- DB connection: `from src.db.connection import SessionLocal` (not `src.db.session`)
- Container workdir is `/app`, Python 3.12.13

**Environment:**
- Server mode: hostname beelink-gti13
- Homelab compose: `~/projects/homelab/compose/compose.nba-ml.yml`
- Deploy command: `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache <service>`
- API container: nba-ml-api, Dashboard container: nba-ml-dashboard
- Dashboard uses `Dockerfile.dashboard-react`
- Models volume: `/opt/homelab/data/nba-ml/models:/app/models`
- API key auth blocks evaluation endpoints (NBA_ML_API_KEY env var empty)

**Key gotchas discovered:**
- Docker exec needs to run from `/app` inside container
- Multiple clamping locations in predictor.py (single predict, batch predict, shadow, challenger) — 4 total
- BFF has 2 separate primary_props CTEs (overview ~397, rankings ~1693) — both needed fixing
- The `edit` tool can't handle multiple identical code blocks — had to use Python script for batch replacement
- prop_lines.py line 437: `_coerce_float(...) or 0.0` silently converts None to 0.0 line value
- Game lines use UTC dates but prop lines use Eastern — timezone mismatch causes feature join failures for evening games
- stl percentiles are (7,93) and blk are (8,92) — NOT the default 80% CI, so z-score of 1.2816 was wrong
- TOV model is 281MB (28x others) — may indicate overfitting, flagged for investigation
- fg_pct/ft_pct have no prop lines but still train models — already excluded via EXCLUDED_PROP_STATS

**Audit report files saved to /tmp (may be expired):**
- `/tmp/1775433615302-copilot-tool-output-gx47d0.txt` — evaluation system audit (40KB)
</technical_details>

<important_files>
- `src/inference/predictor.py`
   - Core prediction generation — both single-player and batch
   - Fixed negative prediction clamping in 4 locations (lines ~176, ~263, ~528, ~558)
   - CI shift logic: `shift = -pred; pred = 0; low = max(0, low+shift); high += shift`

- `src/data/game_lines.py`
   - Game line fetching from Odds API + SGO fallback
   - Added ZoneInfo import (line 12) and ET conversion (lines 297-303)

- `src/data/prop_lines.py`
   - Prop line fetching from SGO and Odds API
   - Fixed default line None (line 437), logging level (line 592)

- `config.py`
   - All edge thresholds and confidence settings
   - Key changes at lines 188-202: lowered thresholds dramatically based on data

- `src/applications/prop_finder.py`
   - Edge detection and prop finding logic
   - Fixed sigma calculation (line ~170) to use per-stat percentile z-scores
   - Added scipy.stats.norm import for dynamic z-score calculation

- `src/training/trainer.py`
   - Model training and registration
   - Added R² guardrail in `_register_best_model()` (after line ~875)

- `dashboard-ui/server/src/index.ts`
   - BFF server — all dashboard data queries
   - Fixed DISTINCT ON in 3 queries, fixed hit rate dedup, added settlement logging, fixed bankroll curve
   - Key locations: ~397 (overview primary_props), ~496 (hit rate trend), ~682 (settlement), ~1029 (bankroll), ~1693 (rankings primary_props)

- `src/evaluation/backtester.py`
   - Backtesting framework
   - Added minutes to _STAT_COLUMN_MAP (line ~32)

- `tasks/PROGRESS-sprint47-prediction-accuracy-0405.md`
   - Sprint progress tracker with checklists
</important_files>

<next_steps>
**Currently running:**
- Docker build of nba-ml-api (shellId: 209) — need to `read_bash` to check completion

**Remaining deployment steps:**
1. Wait for nba-ml-api build to complete, check output
2. Build nba-ml-dashboard: `docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache nba-ml-dashboard`
3. Bring up containers: `docker compose --env-file .env -f compose/compose.nba-ml.yml up -d nba-ml-api nba-ml-dashboard`
4. Verify API health: `curl -s http://localhost:8000/health`
5. Verify dashboard loads: `curl -s http://localhost:3000 | head -5`

**Post-deployment verification (superpowers:verification-before-completion):**
- Check API health endpoint responds
- Check dashboard loads without errors
- Verify hit rate queries return accurate (deduplicated) data
- Check container logs for errors

**Sprint completion tasks:**
- Write Sprint 47 follow-up report in `docs/reports/sprint47-prediction-accuracy-audit.md`
- Add lessons to `tasks/lessons.md`
- Invoke `superpowers:requesting-code-review` on the diff
- Git commit with all changes
- Push to origin
- Open PR, run automated review

**Future sprint items identified (not for this sprint):**
- Walk-forward backtesting (no time-series leakage)
- True CLV tracking (not oversimplified hit_rate proxy)
- Risk-adjusted metrics (Sharpe, Sortino, Calmar)
- Bayesian edge credibility weighting
- Dynamic threshold management (Thompson Sampling)
- A/B testing framework for model comparison
- Feature builder missing team column (Finding #1 from data audit — needs investigation)
- Game_id validation in nba_ingest.py
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
