---
title: "Copilot Session Checkpoint: Sprint 23 props dashboard fixes"
type: source
created: 2026-03-26
last_verified: 2026-04-21
source_hash: "fa1e59bcaa931fd7ea6b20b8dee62a77b76c4d294e36980cc4331bf90d27a7a1"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-23-props-dashboard-fixes-92176283.md
quality_score: 69
concepts:
  []
related:
  - "[[Homelab]]"
  - "[[NBA ML Engine]]"
tier: archive
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard]
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: validated
---

# Copilot Session Checkpoint: Sprint 23 props dashboard fixes

## Summary

The user invoked the `execute-sprint-from-report` skill to complete Sprint 22's next steps (post-retrain optimization), then immediately started Sprint 23 to fix critical dashboard issues: props showing 100% confidence and 200%+ edges, update production model assignments, and carry forward remaining Sprint 22 next steps. We're on the homelab server (beelink-gti13) in server mode with local containers. Sprint 22 is fully complete and merged. Sprint 23 is mid-implementation — BFF confidence/edge formulas are being fixed in `dashboard-ui/server/src/index.ts`.

## Key Points

- PROP_CONFIDENCE_SQL replaced with normal CDF logistic approximation (line ~58)
- Added PROP_EDGE_SQL constant with ±100% cap (line ~75)
- Added VALID_PROP_STATS, VALID_STATS_SQL, MIN_LINE_SQL constants (line ~78)
- Updated `/api/props` query (line ~487) — added stat filter + min line + capped edge
- Updated dashboard overview edge_pct (line ~327) to use PROP_EDGE_SQL
- Updated dashboard overview ORDER BY (line ~342) to use PROP_EDGE_SQL

## Execution Snapshot

### Sprint 22 (COMPLETE — merged to main)

**Files modified:**
- `src/models/ensemble.py`: Fixed feature_names mismatch bug
- `config.py`: ROLLING_WINDOWS now env-var configurable, default [5,20]
- `tests/test_features.py`: Updated rolling column assertion
- `~/projects/homelab/compose/compose.nba-ml.yml`: Added post-retrain-analysis Ofelia job
- `docs/reports/sprint22-post-retrain-optimization.md`: Sprint report
- `tasks/PROGRESS-sprint22-post-retrain-optimization-0326.md`: Progress tracker

Status: PR #24 merged to main, homelab compose pushed.

### Sprint 23 (IN PROGRESS)

**Files being modified:**
- `dashboard-ui/server/src/index.ts`: BFF props fixes (PARTIALLY DONE — see next steps)
- `tasks/PROGRESS-sprint23-props-dashboard-fixes-0326.md`: Created

**Files NOT yet modified but planned:**
- `src/applications/prop_finder.py`: Same confidence formula fix needed
- Production model assignments in DB (manual update if needed)

**Current state of index.ts edits:**
- [x] PROP_CONFIDENCE_SQL replaced with normal CDF logistic approximation (line ~58)
- [x] Added PROP_EDGE_SQL constant with ±100% cap (line ~75)
- [x] Added VALID_PROP_STATS, VALID_STATS_SQL, MIN_LINE_SQL constants (line ~78)
- [x] Updated `/api/props` query (line ~487) — added stat filter + min line + capped edge
- [x] Updated dashboard overview edge_pct (line ~327) to use PROP_EDGE_SQL
- [x] Updated dashboard overview ORDER BY (line ~342) to use PROP_EDGE_SQL
- [x] Updated dashboard overview avg_edge_pct (line ~353) to use PROP_EDGE_SQL
- [ ] Third instance at ~line 1169 still uses old uncapped edge formula
- [ ] Need to verify all edits compile correctly (no TypeScript build run yet)

**SQL todos status:**
- `fix-bff-filter`: in_progress
- `fix-confidence`: in_progress
- `fix-edge-display`: in_progress
- `update-prod-models`: in_progress
- `test-validate`: pending
- `deploy-verify`: pending
- `write-report`: pending

## Technical Details

- **100% Confidence**: Formula `min(|predicted - line| / (CI_width / 2), 1.0)` is a distance metric, not probability. When prediction is even moderately far from line relative to CI width, it clips to 1.0. Example: pred=18.3, line=2.5, CI_width=10 → 15.8/(5) = 3.16 → capped to 1.0.
- **200%+ Edges**: Formula `(predicted - line) / line`. Small/misclassified lines produce absurd values. Derrick White: (18.3 - 2.5) / 2.5 = 631%. The 2.5 "pts" line is actually a three-pointer line from SGO_FD.
- **BFF bypasses FastAPI**: The React dashboard's BFF (Express/TypeScript at port 3080) queries Postgres directly for `/api/props`, bypassing the FastAPI `/prop-edges` endpoint which DOES filter excluded stats. The `buildEdgeFilterClause` function exists in the BFF but is only used in the dashboard overview, not the props query. ### Fix Approach **Confidence** → Normal CDF via logistic approximation:
- σ = CI_width / (2 * 1.2816) where 1.2816 is the z-score for 10th/90th percentile
- z = |predicted - line| / σ
- P(correct direction) = 1 / (1 + exp(-1.7 * z)) — logistic approximation of Φ(z)
- Range: 0.5 (coin flip at z=0) to ~0.99 (very confident), never 1.0 **Edge** → Cap at ±100%: `LEAST(GREATEST((pred-line)/NULLIF(line,0), -1.0), 1.0)` **Stat filtering** → Only show stats we actually predict well for betting: `['reb', 'stl', 'blk', 'tov', 'fg3m']`. Excluded: pts, ast, fg_pct, ft_pct (config EXCLUDED_PROP_STATS), pra (not a predicted stat). **Line validation** → Per-stat minimum lines: pts≥5, reb≥1, ast≥1, fg3m≥0.5, else≥0.5. ### Production Model Assignments (Current) Auto-selected during Sprint 22 retrain by lowest val_mse:
- pts: LightGBMModel, reb: CatBoostModel, ast: EnsembleModel
- stl: CatBoostModel, blk: EnsembleModel, tov: CatBoostModel
- fg_pct: CatBoostModel, ft_pct: CatBoostModel, fg3m: EnsembleModel Holdout evaluation showed Ridge is best for stl/blk/tov on test set, but these are close margins. Trainer uses val_mse which may legitimately select differently. Need to decide if manual reassignment is warranted. ### Homelab Architecture
- Server: beelink-gti13 (hostname)
- API: nba-ml-api container (FastAPI, port 8000)
- Dashboard: nba-ml-dashboard container (React + Express BFF, port 8501 external, 3080 internal)
- Scheduler: nba-ml-scheduler container (Ofelia)
- MLflow: nba-ml-mlflow container (port 5000)
- DB: PostgreSQL (connection via DATABASE_URL in config.py)
- Deploy: `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache <service> && up -d` ### Data Quality Issue SGO_FD (FanDuel via SGO scraper) is storing some props with wrong stat_name. Example: three-pointer lines stored as "pts". This affects ~46 of 188 pts props (line < 5). The VALID_PROP_STATS filter + MIN_LINE_SQL will handle this at query time. ### Key Config Values
- `EXCLUDED_PROP_STATS = ['fg_pct', 'ft_pct', 'pts', 'ast']`
- `STAT_EDGE_THRESHOLDS`: pts=10%, reb=8%, ast=8%, stl=5%, blk=5%, tov=8%, fg_pct=15%, ft_pct=15%, fg3m=8%
- `CONFIDENCE_LOWER/UPPER_PERCENTILE`: 10/90
- `STAT_CALIBRATION_PERCENTILES`: stl=(7,93), blk=(8,92) ### Pre-existing Issues
- 15 tests in test_notifications.py fail due to missing `apprise` module — unrelated
- All other 163 tests pass

## Important Files

- `dashboard-ui/server/src/index.ts`
- **Primary file being edited for Sprint 23**
- BFF Express server with direct Postgres queries for props
- Changed `PROP_CONFIDENCE_SQL` (line ~58) to normal CDF logistic approximation
- Added `PROP_EDGE_SQL` (line ~75) with ±100% cap
- Added `VALID_PROP_STATS`, `VALID_STATS_SQL`, `MIN_LINE_SQL` constants (lines ~78-90)
- Updated `/api/props` query (line ~487) with stat filter, min line, capped edge
- Updated dashboard overview queries (lines ~327, 343, 353)
- **STILL NEEDS**: Third instance at ~line 1169 (confident props query) needs edge formula update
- Key functions: `getConfidenceTier` (line 115), `buildEdgeFilterClause` (line 158), `getEdgePolicy` (line 142), `getFeaturedPropSlate` (line 193)

- `src/applications/prop_finder.py`
- Backend prop edge finder — FastAPI `/prop-edges` uses this
- Has its own confidence formula (line 105-112) — needs same CDF fix
- Edge formula at line 96: `edge = (predicted - line) / line` — needs cap
- Already filters excluded stats (line 82) and applies thresholds (line 100)
- **NOT YET MODIFIED** for Sprint 23

- `config.py`
- Central config — EXCLUDED_PROP_STATS (line 191), STAT_EDGE_THRESHOLDS (line 179)
- ROLLING_WINDOWS (line ~66) — changed in Sprint 22 to env-var configurable [5,20]
- CONFIDENCE_LOWER/UPPER_PERCENTILE (lines 161-162)
- USE_VIF_PRUNING, VIF_THRESHOLD

- `src/models/ensemble.py`
- Fixed in Sprint 22: added `_align_for_base()`, `feature_names` attribute
- Critical for holdout evaluation working for all stats

- `~/projects/homelab/compose/compose.nba-ml.yml`
- Docker compose for all NBA ML services
- Sprint 22: Added post-retrain-analysis Ofelia job
- Dashboard container config needed for rebuild/deploy

- `docs/reports/sprint22-post-retrain-optimization.md`
- Sprint 22 report with baseline/post-retrain metrics comparison
- Next steps that drove Sprint 23 scope

- `tasks/PROGRESS-sprint23-props-dashboard-fixes-0326.md`
- Sprint 23 progress tracker (just created)

- `tasks/lessons.md`
- Extensive lessons learned file — checked before every sprint
- Key lessons: verify deployed dashboards by rendered page, rebuild Docker after code changes, preserve nested paths when syncing

## Next Steps

**### Immediate (was actively working on):**
1. **Fix third edge formula instance** (~line 1169 in index.ts) — the "confident props" query still uses old uncapped edge formula `((pb.predicted_value - pl.line) / NULLIF(pl.line, 0))`. Change to `(${PROP_EDGE_SQL})`.

2. **Verify all index.ts edits compile** — Run `cd dashboard-ui && npm run build` or equivalent TypeScript check.

**### Remaining Sprint 23 tasks:**
3. **Fix prop_finder.py confidence formula** — Replace distance-based `min(distance / (ci_width / 2), 1.0)` with normal CDF: `from math import erf, sqrt; confidence = 0.5 * (1 + erf(abs(predicted - line) / (ci_width / (2 * 1.2816)) / sqrt(2)))`. Cap edge at ±1.0 there too.

4. **Update production model assignments** — Check current DB assignments vs holdout best models. May need to manually update for stats where holdout-best differs from val_mse-best (stl→Ridge, blk→Ridge, tov→Ridge). Or decide the val_mse selection is fine.

5. **Run tests** — `cd /home/jbl/projects/nba-ml-engine && python -m pytest tests/ -x --timeout=30`

6. **Build and deploy dashboard** — `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache nba-ml-dashboard && docker compose --env-file .env -f compose/compose.nba-ml.yml up -d nba-ml-dashboard`

7. **Verify live props page** — `curl -s http://localhost:8501/api/props | python3 -c "..."` — confirm confidence in 50-95% range, edges capped at ±100%, no excluded stats showing.

8. **Write Sprint 23 report** — `docs/reports/sprint23-props-dashboard-fixes.md`

9. **Commit, push, PR, merge** — Same git workflow as Sprint 22.

**### Carry-forward next steps from Sprint 22:**
- Investigate blk over-coverage (86.8% vs 80% target) — Low priority
- Evaluate window [5,15] vs [5,20] — Low priority
- Monitor weekly post-retrain-analysis job — Low priority (runs next Sunday)

**### SQL todos:**
- `fix-bff-filter`: in_progress (mostly done, one instance remaining)
- `fix-confidence`: in_progress (BFF done, prop_finder.py pending)
- `fix-edge-display`: in_progress (BFF mostly done, prop_finder.py pending)
- `update-prod-models`: in_progress (investigation done, action pending)
- `test-validate`: pending (depends on above 4)
- `deploy-verify`: pending (depends on test-validate)
- `write-report`: pending (depends on deploy-verify)

**### Git state:**
- Branch: `feature/sprint-23-props-dashboard-fixes` (checked out)
- Base: main at commit 5fd498a (Sprint 22 merged)
- Working tree: modified `dashboard-ui/server/src/index.ts` + new progress tracker

## Related Wiki Pages

- [[Homelab]]
- [[NBA ML Engine]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-23-props-dashboard-fixes-92176283.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-26 |
| URL | N/A |
