---
title: "Copilot Session Checkpoint: Sprint 50 audit complete, ready to implement"
type: source
created: 2026-04-12
last_verified: 2026-04-21
source_hash: "6a0eb190ea7a53207f0c316c728aee4c8fa5fc528ed9cf9f639330214478cff3"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-50-audit-complete-ready-to-implement-404a98da.md
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

# Copilot Session Checkpoint: Sprint 50 audit complete, ready to implement

## Summary

The user is executing Sprint 50 for the NBA ML Engine project, implementing the high-priority next steps from Sprint 49's results report. The two main workstreams are: (1) investigating PTS stat underperformance (49.9% hit rate vs 52.4% vig breakeven), and (2) closing remaining data quality bugs 1-3. I've completed the audit phase — two explore agents analyzed PTS underperformance root causes and data bug status — and am now ready to plan and implement fixes.

## Key Points

- Sprint 48 was implemented and merged as PR #30 (prior session)
- All changes deployed and validated
- Sprint 49 was implemented and merged as PR #31 (prior session)
- Sprint orchestrator agent created
- AGENTS.md created, all agents optimized for Sprint 48 changes
- Fixed backtester SQL bug (g.minutes missing from GROUP BY)

## Execution Snapshot

No code changes yet for Sprint 50. All work so far is audit/investigation.

SQL todos from Sprint 49 are all marked 'done' (15/15). New Sprint 50 todos need to be created.

Current branch: `main` at commit 49d2d76 (Sprint 49 merged)
No sprint branch created yet for Sprint 50.

**Key audit findings ready to act on:**

**PTS Underperformance Root Causes:**
- Edge calculation `|pred - line| / line` is scale-dependent — PTS (line~25) needs 0.25pt accuracy for 1% edge, while AST (line~5) needs 0.05 for same threshold
- PTS edge threshold at 0.01 (1%) is too restrictive for high-value stats
- No PTS-specific CI calibration percentile override (uses default 10/90)
- No per-stat calibrator file exists for PTS (models/calibrators/per_stat/pts_calibrator.pkl missing)
- Inverse edge-accuracy persists: 0-1% edge hits 53.4%, 5%+ hits 47.9%
- PTS underperformance is PERSISTENT across Sprint 47, 48, 49 backtests (~49.9%)

**Data Quality Bug Status:**
- Bug 1 (timezone): PARTIALLY FIXED — Odds API path correct, SGO fallback path BROKEN (line 161 in game_lines.py missing `.astimezone(ZoneInfo("America/New_York"))`)
- Bug 2 (prop 0.0): ALREADY FIXED — `_coerce_float` returns None, downstream filters reject null lines
- Bug 3 (alt-line BFF): PARTIALLY FIXED — Overview and confidence queries fixed, but hit rate trend query (index.ts line 498) still missing `source` in DISTINCT ON

## Technical Details

- Server mode: hostname `beelink-gti13`, local containers
- Python 3.12 with `.venv/bin/python`, tests via `.venv/bin/python -m pytest`
- Homelab compose at `~/projects/homelab/compose/compose.nba-ml.yml`, env at `~/projects/homelab/.env`
- Build: `cd ~/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml build --no-cache nba-ml-api`
- Deploy: same path with `up -d nba-ml-api`
- Backtest command: `docker exec nba-ml-api python main.py backtest --start YYYY-MM-DD --end YYYY-MM-DD --min-edge 0.005` **Schema Facts:**
- `game_lines` table has NO `game_time` column — only `game_date` (date), `game_id`, team columns, spread/total/moneyline, `fetched_at`
- `predictions` table has NO `hit`, `settled`, or `confidence` columns — must JOIN to prop_line_snapshots for actual_value
- Predictions uses `confidence_high`/`confidence_low` columns (NOT `ci_upper`/`ci_lower`)
- SKILL.md data quality gate SQL for timezone check is wrong for this schema (references non-existent `game_time` column) **PTS Edge Calculation Problem:**
- Formula: `edge_pct = ABS(predicted - line) / NULLIF(line, 0)` used in backtester.py:150, predictor.py:414, edge_optimizer.py:99
- This creates asymmetric thresholds across stats: PTS (line~25) needs 0.25pt for 1% edge, AST (line~5) needs 0.05pt
- Recommendation from audit: Lower PTS threshold to 0.005 (0.5%) OR implement scale-aware edge metric
- PTS CI uses default 10th/90th percentiles, no override in STAT_CALIBRATION_PERCENTILES
- PTS is NOT in LOW_R2_STATS (feature_selector.py:23) — uses all ~350 features **SGO Timezone Bug Details:**
- game_lines.py line 161: `datetime.fromisoformat(starts_at.replace("Z", "+00:00")).date()` — extracts date from UTC without timezone conversion
- Compare to correct path at lines 297-305 which uses `.astimezone(ZoneInfo("America/New_York")).date()`
- Fix: add `.astimezone(ZoneInfo("America/New_York"))` before `.date()` **BFF Alt-Line Bug Details:**
- dashboard-ui/server/src/index.ts line 498: `DISTINCT ON (pl.player_id, pl.game_date, pl.stat_name)` missing `pl.source`
- Other queries (lines 397, 690, 1706) already fixed with `source` in DISTINCT ON
- Only hit rate trend endpoint still affected **Recent Lessons from lessons.md:**
- PropLineSnapshot upsert fix (UniqueViolation on re-run)
- Pipeline failure ntfy truncation (Apprise 4096-byte limit)
- Inverse edge-accuracy relationship documented in Sprint 47
- calibrator refit had wrong function name/signature in main.py

## Important Files

- `docs/reports/sprint49-results.md`
- Source report for Sprint 50 scope
- Next steps defined at lines 74-86 (high/medium/low priority)
- PTS at 49.9% hit rate documented at line 57

- `config.py`
- Central configuration, PTS edge threshold at line 199 (`"pts": 0.01`)
- STAT_CALIBRATION_PERCENTILES at lines 176-183 (no PTS override)
- VIG_BREAKEVEN_RATE=0.524 at line 196

- `src/evaluation/backtester.py`
- Edge calculation at line 150: `ABS(predicted - line) / NULLIF(line, 0) AS edge_pct`
- Per-stat threshold filtering at lines 169-179
- GROUP BY at line 135 (fixed in Sprint 49 to include g.minutes)

- `src/data/game_lines.py`
- Bug 1: SGO path timezone bug at lines 157-163
- Correct Odds API path at lines 297-305 for comparison
- Need to add `.astimezone(ZoneInfo("America/New_York"))` at line 161

- `src/data/prop_lines.py`
- Bug 2: ALREADY FIXED — `_coerce_float` returns None (lines 353-359)
- Validation chain at lines 32-40, 458-460, 790-799

- `dashboard-ui/server/src/index.ts`
- Bug 3: Hit rate trend query missing `source` in DISTINCT ON at line 498
- Fixed queries at lines 397 (overview), 690 (settlement), 1706 (confidence)

- `src/inference/predictor.py`
- Edge calculation at line 414 (signed edge, uses same `/line` normalization)
- CI generation at lines 260-271 (negative clamping handled)

- `src/evaluation/edge_optimizer.py`
- Edge calculation at line 99 (same formula as backtester)

- `src/models/base.py`
- CI calibration at lines 74-94 (PTS uses default 10/90 percentiles)

- `AGENTS.md`
- Root-level agent index created in Sprint 49
- Routing guide, file ownership, quality gates

- `.github/skills/execute-sprint-from-report/SKILL.md`
- Sprint execution workflow (14 steps after Sprint 49 improvements)
- Data quality gate SQL at step 3 references non-existent `game_time` column — needs fixing

## Next Steps

**Sprint 50 Scope (from Sprint 49 next steps, high priority):**

### Workstream A: PTS Underperformance Fix (feature-lab + model-calibration domains)
1. Lower PTS edge threshold from 0.01 to 0.005 in config.py
2. Consider scale-aware edge metric (absolute points instead of percentage) — needs investigation
3. Add PTS CI calibration percentile override to STAT_CALIBRATION_PERCENTILES (wider CIs)
4. Validate with 30-day backtest that PTS hit rate improves

### Workstream B: Data Quality Bugs (data-quality domain)
1. Fix Bug 1: Add `.astimezone(ZoneInfo("America/New_York"))` to game_lines.py line 161 (SGO path)
2. Mark Bug 2 as closed (already fixed)
3. Fix Bug 3: Add `pl.source` to DISTINCT ON in dashboard-ui/server/src/index.ts line 498
4. Update data-quality.md bug table to reflect current status

### Workstream C: SKILL.md Data Quality Gate Fix
1. Fix the timezone check SQL in SKILL.md step 3 — `game_time` column doesn't exist

**### Immediate Next Actions:**
1. Create branch `feature/sprint-50-pts-fix-data-quality`
2. Create plan in session plan.md
3. Insert SQL todos for all workstreams
4. Implement both workstreams (they're independent — can parallelize)
5. Write tests for timezone fix and PTS threshold change
6. Run full test suite + 30-day backtest
7. Deploy, verify, write report, create PR, merge

## Related Wiki Pages

- [[Homelab]]
- [[NBA ML Engine]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-50-audit-complete-ready-to-implement-404a98da.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-04-12 |
| URL | N/A |
