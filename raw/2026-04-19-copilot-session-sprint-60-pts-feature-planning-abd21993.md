---
title: "Copilot Session Checkpoint: Sprint 60 PTS feature planning"
type: text
captured: 2026-04-19T15:32:47.756805Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, agents, dashboard]
checkpoint_class: project-progress
checkpoint_class_rule: "title:sprint 60"
retention_mode: compress
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Sprint 60 PTS feature planning
**Session ID:** `af2982d2-180f-4871-ab07-ba61d03faf7d`
**Checkpoint file:** `/home/jbl/.copilot/session-state/af2982d2-180f-4871-ab07-ba61d03faf7d/checkpoints/005-sprint-60-pts-feature-planning.md`
**Checkpoint timestamp:** 2026-04-19T15:24:56.536956Z
**Exported:** 2026-04-19T15:32:47.756805Z
**Checkpoint class:** `project-progress` (rule: `title:sprint 60`)
**Retention mode:** `compress`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
Sprint 60 on NBA ML Engine: implement Sprint 59's recommended next-steps to lift prediction accuracy across all stat categories. Tier A focus is PTS feature engineering (opponent def-rating roll, teammate-injured-usage delta, position-adjusted opponent points-allowed) plus extending CLASSIFIER_STATS, calibration audit, and finishing Tier C hygiene (snapshot retention, ensemble pickle removal). Constraint: Odds API budget exhausted for the month, so SGO/prop-line backfill items remain blocked. Strategy: implement code-only changes that take effect on the next weekly retrain (~2026-04-24), plus run diagnostic calibration audit now.
</overview>

<history>
1. User invoked `/execute-sprint-from-report implement sprint 60`.
   - Loaded the execute-sprint-from-report skill.
   - Confirmed environment: hostname `beelink-gti13` (server), git on clean main, Sprint 59 PR #43 already merged, latest commit `03757da` (AGENTS.md knowledge-base ladder).
   - Read Sprint 59 next-steps from `docs/reports/sprint59-results.md`:
     - Tier A.1 PTS feature engineering (opponent def rating × usage, opp pts-allowed-by-position roll-10, teammate-injured-usage delta)
     - Tier A.2 per-stat model re-selection for PTS/AST
     - Tier A.3 calibration audit after 2026-04-17 retrain
     - Tier B.4 extend CLASSIFIER_STATS to fg_pct, ft_pct
     - Tier B.5 prop-market expansion (BLOCKED – Odds API exhausted)
     - Tier B.6 ensemble SHAP timing budget
     - Tier C.7 snapshot retention pruning
     - Tier C.8 ensemble SHAP meta-ridge surfacing
     - Tier C.9 drop pickle import from ensemble.py once load() moves to shared helper
   - Audited `config.py`: `TARGET_STATS = [pts, reb, ast, stl, blk, tov, fg3m]`, `CLASSIFIER_STATS` env-driven defaults to same 7. Note: `fg_pct`/`ft_pct` are NOT in TARGET_STATS, so adding them to CLASSIFIER_STATS may need feature-side work.
   - Audited `src/features/builder.py`:
     - Existing: `opp_vs_pos_pts_avg/reb/ast` (expanding mean by opponent+position with leakage-safe shift)
     - Existing: `_add_teammate_availability_features` produces only `teammates_injured` (count) and `opportunity_boost` (count/5) — no usage-weighted delta
     - Existing: `gadv_off_rating_roll_5/10`, `gadv_def_rating_roll_5/10` are PER-PLAYER (own performance), NOT opponent-team rolls
     - Existing: `opp_drtg`, `opp_pace` exist as static team-season values from `_load_team_stats` (no rolling)
     - Existing interaction: `opp_pace_x_usage = opp_pace × gadv_usg_pct` (line 496)
     - Missing: opponent team's defensive rating ROLLED over recent games (e.g., last 10 opponent games), and opp_def_roll × player_usage interaction
   - Conversation was compacted before plan/branch/implementation.
</history>

<work_done>
Files inspected (no edits yet this session):
- `config.py` — TARGET_STATS / CLASSIFIER_STATS layout
- `src/features/builder.py` — confirmed `_add_opp_vs_position_features` (line 563), `_add_teammate_availability_features` (line 617), `_add_game_advanced_rolling` (line 973), context features with `opp_drtg`/`opp_pace` (line 454, 486-496)

Work completed:
- [x] Skill loaded
- [x] Environment + git state verified (server, clean main)
- [x] Sprint 59 next-steps re-read
- [x] Existing feature-builder audit — identified what's already there vs. genuinely new
- [ ] Branch creation
- [ ] Plan + progress tracker
- [ ] SQL todos seeded
- [ ] Data quality gate
- [ ] Implementation
- [ ] Tests
- [ ] Deploy
- [ ] Report
- [ ] Lessons
- [ ] PR + merge

No code changes made this session.
</work_done>

<technical_details>
- **Environment**: server (`beelink-gti13`). Deploy via `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache <service> && up -d <service>`. Always `--env-file .env`.
- **Migrations**: `docker cp <migration> nba-ml-api:/app/alembic/versions/ && docker exec -e PYTHONPATH=/app nba-ml-api alembic upgrade head` (PYTHONPATH required, alembic.ini uses `version_table = nba_ml_alembic_version`).
- **Latest alembic head**: `b935d2e7ef11` (Sprint 59 registry_health_snapshots).

- **Sprint 59 SHAP findings drove Sprint 60 plan**:
  - PTS (Ridge wrapper) top features: predicted_minutes (13%), bbref_per (3.6%), minutes_roll_20_mean (3.0%) — usage/minutes dominates, defensive matchup signal underrepresented.
  - REB (Ensemble): reb_ewma_20 (8.4%), then `gadv_off_rating_roll_10`/`gadv_def_rating_roll_10` (3.2% each) — but these are own-player ratings, not opponent rolling.

- **Feature-builder gap analysis**:
  - `gadv_def_rating_roll_10` is the player's own def_rating rolling window — useful but not the opponent-team feature Sprint 59 recommended.
  - Sprint 59 recommendation #1 maps to: NEW `opp_team_def_rating_roll_10` (opponent's recent defensive rating, rolling over their last 10 games) + interaction `opp_team_def_rating_roll_10 × gadv_usg_pct`.
  - Sprint 59 recommendation #2 (`pts_allowed_position_opp_roll_10`) — a rolling-window variant exists implicitly in `opp_vs_pos_pts_avg` but it's an EXPANDING mean, not a 10-game rolling. Could either replace or augment.
  - Sprint 59 recommendation #3 (`teammate_injured_usage_delta`) — current `teammates_injured` is just a count. Need to weight by each injured teammate's recent usage% (e.g., `gadv_usg_pct` rolling), summed across out/doubtful teammates, then deltaed against team baseline.

- **Quirks to recall**:
  - SGO data quality gate from skill must run BEFORE planning (timezone, no 0.0 lines, prop freshness).
  - prop_lines table has NO id column; composite key (player_id, game_date, source, stat_name).
  - `pickle.load` is still used in `EnsembleModel.load()` (Sprint 59 only refactored save). Tier C.9 means moving load to a shared helper too.
  - `models/_io.py:atomic_pickle_dump(payload, path)` is the canonical save helper.
  - For ML changes: 10-point pre-deployment protocol from `agents/backtest-lab.md` is required before deploy. Most Sprint 60 items are feature-engineering code that takes effect on next retrain — the protocol may not block deploy of pure feature additions, but calibration audit + classifier extension WILL need it once retrained.

- **Open questions**:
  - Does `fg_pct`/`ft_pct` exist as a target column in `build_features` output? If not, adding to CLASSIFIER_STATS won't auto-train — need to investigate.
  - Should we trigger an off-cycle retrain to materialize Sprint 60 features now, or wait for the 2026-04-24 weekly cron?
  - Snapshot retention: simple `DELETE FROM registry_health_snapshots WHERE checked_at < NOW() - INTERVAL '90 days'` via Ofelia, or a Python script with logging?
</technical_details>

<important_files>
- `docs/reports/sprint59-results.md`
   - Sprint 60 source — defines all Tier A/B/C items.

- `config.py:73-146`
   - `TARGET_STATS` (line 73), `CLASSIFIER_STATS` (line 146) — Tier B.4 edits live here.

- `src/features/builder.py`
   - The big enchilada for Tier A.1.
   - Line 434: `_add_context_features` — where `opp_drtg`/`opp_pace` get merged. New rolling opp def rating belongs nearby.
   - Line 486-496: existing interactions (`home_x_opp_pace`, `opp_pace_x_usage`). New `opp_def_roll_x_usage` should follow this pattern.
   - Line 563-614: `_add_opp_vs_position_features` — uses expanding mean. Sprint 60 rec #2 may add 10-game rolling variant `opp_vs_pos_pts_roll_10`.
   - Line 617-685: `_add_teammate_availability_features` — currently produces `teammates_injured` count only. Sprint 60 rec #3 extends to usage-weighted delta.
   - Line 967-970: `_GADV_ROLL_COLS`/`_GADV_ROLL_WINDOWS` — pattern for new opponent-team rolling.

- `src/models/ensemble.py`
   - `load()` still uses raw `pickle.load`; Tier C.9 refactor to a `models/_io.py:atomic_pickle_load` helper.

- `src/models/_io.py`
   - Add `atomic_pickle_load` companion to `atomic_pickle_dump` for Tier C.9.

- `scripts/shap_analysis.py`
   - Tier C.8: surface meta-ridge weight in `_shap_values_ensemble`.
   - Tier B.6: timing budget — may need `--max-samples-ensemble` flag.

- `~/projects/homelab/compose/compose.nba-ml.yml`
   - Tier C.7: add Ofelia job for snapshot pruning (mirror `registry-health` cron at 12:05 UTC).

- `tasks/lessons.md`
   - Append Sprint 60 lessons at end.

- Files NOT yet created (to do):
   - Sprint 60 branch (`feature/sprint-60-pts-features-classifier-extension`)
   - `tasks/PROGRESS-sprint60-pts-features-MMDD.md`
   - `tests/test_sprint60.py`
   - `docs/reports/sprint60-results.md`
   - Possibly `alembic/versions/<rev>_add_classifier_stats.py` if classifier extension needs schema work
</important_files>

<next_steps>
Immediate next steps (in priority order):

1. **Branch + tracker**: `git checkout -b feature/sprint-60-pts-features-classifier-extension`. Create `tasks/PROGRESS-sprint60-pts-features-0419.md`. Update `plan.md` with Sprint 60 todos.

2. **Data quality gate**: run the 3 SGO/prop checks from skill before planning. Block on failures.

3. **Seed SQL todos** for Sprint 60:
   - `s60-opp-def-roll` — add opponent team def_rating rolling 10-game feature + usage interaction
   - `s60-opp-vs-pos-roll` — add `opp_vs_pos_{stat}_roll_10` (10-game rolling complement to expanding mean)
   - `s60-teammate-usage-delta` — extend `_add_teammate_availability_features` to compute usage-weighted delta
   - `s60-classifier-extend` — add fg_pct/ft_pct to CLASSIFIER_STATS (verify target columns exist first)
   - `s60-calibration-audit` — run per-stat ECE on 2026-04-17 retrained models, write JSON report
   - `s60-snapshot-retention` — Ofelia job + script to prune `registry_health_snapshots` > 90 days
   - `s60-atomic-pickle-load` — add `atomic_pickle_load` helper, refactor `EnsembleModel.load()`
   - `s60-meta-ridge-shap` — surface meta-ridge weight in ensemble SHAP
   - `s60-tests` — `tests/test_sprint60.py` covering each new feature
   - `s60-deploy-verify` — rebuild API + dashboard, smoke test
   - `s60-report-merge` — sprint60-results.md + lessons + PR

4. **Investigate fg_pct/ft_pct target availability** before promising classifier extension. If columns don't exist in build_features output, scope shrinks to just calibration + features.

5. **Implement features** (Tier A.1 pieces) — TDD with synthetic fixtures in `tests/test_sprint60.py` first.

6. **Calibration audit script** — invoke existing `src/evaluation/calibration.py` per-stat against current production models; if any stat ECE > 0.05, fit Platt and save to `models/calibrators/per_stat/`.

7. **Tier C hygiene** items — atomic_pickle_load, snapshot pruning, meta-ridge SHAP.

8. **Pytest, deploy, report, lessons, PR, merge** — standard close-out.

Open blockers:
- Odds API exhausted (Tier B.5) — document in report, not implementing.
- Whether to trigger off-cycle retrain or wait for 2026-04-24 weekly — consult user if features are ready before then.
- fg_pct/ft_pct target column availability — must verify before committing to classifier extension.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
