---
title: "Copilot Session Checkpoint: Data Source Expansion Exploration"
type: source
created: 2026-03-20
last_verified: 2026-04-21
source_hash: "9f90b86f2aab32a86e7ca650c6477398444e04958726c5b3ca2ccd9f465e7581"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-data-source-expansion-exploration-b12f747f.md
quality_score: 90
concepts:
  - data-source-expansion-nba-ml-prediction-platform
  - homelab-server-deployment-nba-ml-platform
  - feature-engineering-pipeline-nba-ml-platform
related:
  - "[[Data Source Expansion for NBA ML Prediction Platform]]"
  - "[[Homelab Server Deployment Architecture for NBA ML Platform]]"
  - "[[Feature Engineering Pipeline for NBA ML Platform]]"
  - "[[NBA ML Engine]]"
  - "[[EnsembleModel]]"
  - "[[Homelab]]"
tier: hot
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, nba-ml-engine, dashboard, deployment, data ingestion, nba, feature engineering, machine learning, ensemble learning]
checkpoint_class: durable-workflow
retention_mode: retain
knowledge_state: validated
---

# Copilot Session Checkpoint: Data Source Expansion Exploration

## Summary

The user is running a multi-sprint improvement campaign on their NBA ML prediction platform (nba-ml-engine) deployed on a homelab server (beelink-gti13). The work spans three sessions: Sprint 1 (dashboard improvements, model retraining), Sprint 2 (cron updates, data validation, source evaluation report), and Sprint 3 (continuing data source expansion from a prior session's progress tracker, deploying, validating, and creating an evaluation report). We're working directly on the homelab server with Docker containers for the full stack.

## Key Points

- Phase 1A: Position backfill (537/537 active players, 7 bio columns added)
- Phase 1B: Starter CDN backfill (149,554/153,235 = 97.6% fill)
- Phase 1C partial: CDN advanced stats backfill (270,586 rows, 12,752 games)
- Starter features in builder (is_starter, starter_roll_5, minutes_starter_avg_10, minutes_bench_avg_10)
- Game-advanced rolling features in builder (7 stats × 2 windows = 14 features)
- Daily pipeline wired with CDN starters + positions + advanced stats

## Execution Snapshot

**Sprint 2 files modified (by us):**
- `/home/jbl/projects/homelab/compose/compose.nba-ml.yml`: Changed cron schedules to 3am ET
- `/home/jbl/projects/nba-ml-engine/docs/reports/data-validation-source-evaluation_0319.md`: Created comprehensive data/source evaluation report

**Sprint 3 status (current branch: `feature/data-source-expansion`):**

**Completed by prior session:**
- [x] Phase 1A: Position backfill (537/537 active players, 7 bio columns added)
- [x] Phase 1B: Starter CDN backfill (149,554/153,235 = 97.6% fill)
- [x] Phase 1C partial: CDN advanced stats backfill (270,586 rows, 12,752 games)
- [x] Starter features in builder (is_starter, starter_roll_5, minutes_starter_avg_10, minutes_bench_avg_10)
- [x] Game-advanced rolling features in builder (7 stats × 2 windows = 14 features)
- [x] Daily pipeline wired with CDN starters + positions + advanced stats
- [x] Alembic migration `7e1d92d75f3d` (6 new tables + 7 player columns)
- [x] Backfill CLI with --positions, --starters, --starters-cdn, --advanced-per-game, --advanced-per-game-cdn

**NOT yet done (from progress tracker):**
- [ ] Phase 1C: Run API overlay (--advanced-per-game) for individual ORTG/DRTG/NET (stats.nba.com is back up)
- [ ] Phase 1C: Verify ≥100,000 rows, no null key columns
- [ ] Phase 2A: Player tracking stats (BoxScorePlayerTrackV3) — table exists, no ingestion code
- [ ] Phase 2B: Basketball Reference integration — table exists, no scraper code
- [ ] Phase 2C: Hustle stats (LeagueHustleStatsPlayer) — table exists, no ingestion code
- [ ] Phase 3: Game lines, enhanced props, Rotowire lineups — tables exist, no code
- [ ] Phase 4: Clutch stats, defensive tracking, standings, rotations
- [ ] Cross-phase: tracking rolling features, hustle features, BBRef features, game-line features
- [ ] Model retraining with new features
- [ ] Evaluation report comparing before/after
- [ ] Deploy to homelab
- [ ] Create docs/reports evaluation report

**Current database state:**
| Table | Rows |
|-------|------|
| players | 5,122 (537 active) |
| game_logs | 153,235 |
| game_advanced_stats | 270,586 |
| player_advanced_stats | 6,442 |
| team_stats | 360 |
| injuries | 431 |
| prop_lines | 2,550 |
| predictions | 14,178 |
| model_registry (prod) | 9 |

**SQL todos table:** 4 items all done from Sprint 2. Need to create new todos for Sprint 3.

## Technical Details

- **We ARE the homelab server** (hostname: beelink-gti13). Docker containers run locally. No SSH needed.
- **Homelab compose:** `/home/jbl/projects/homelab/compose/compose.nba-ml.yml`. MUST use `--env-file ../.env` from homelab dir or env vars are blank (caused DB crash once).
- **Homelab compose command:** `cd /home/jbl/projects/homelab && docker compose --env-file .env -f compose/compose.nba-ml.yml up -d`
- **Container architecture:** nba-ml-db (TimescaleDB), nba-ml-mlflow (tracking), nba-ml-api (FastAPI + training), nba-ml-dashboard (Streamlit), nba-ml-scheduler (Ofelia cron)
- **Ofelia cron format:** 6-field with seconds: `sec min hour day month weekday`. Current: pipeline 08:00 UTC, props 08:15, predict 08:30.
- **NBA API rate limit:** 0.6s delay between requests. No hard limit but aggressive scraping gets IP-blocked.
- **NBA CDN:** cdn.nba.com (2019+) + data.nba.com (2015-18). 0.2s delay. Static JSON files, no rate limiting. Used as primary data source after stats.nba.com outage.
- **CDN advanced stats accuracy:** Exact for ts_pct/efg_pct/ast_tov/pie. ~95% for usg_pct/ast_pct/pace. Team proxy for off_rating/def_rating/net_rating (need stats.nba.com overlay for individual values).
- **stats.nba.com recovered** as of 2026-03-19 — BoxScoreAdvancedV3, BoxScorePlayerTrackV3, LeagueHustleStatsPlayer all confirmed working.
- **basketball_reference_web_scraper:** Installed in Docker image but no integration code yet. Provides PER, WS, BPM, VORP. Rate limit: ~20 req/min, use 3s delay.
- **Feature matrix:** Was 95K rows × 341 columns (307 features). New features (starter + game-advanced rolling) will increase to ~325+ features.
- **EnsembleModel:** Stacking meta-learner over XGBoost+LightGBM+RandomForest+Ridge. Won 8/9 categories. RidgeModel won BLK.
- **Test suite:** 30 tests, 28 pass, 2 fail (pre-existing libgomp.so.1 missing — LightGBM native lib not in host venv, works in Docker).
- **pandas FutureWarning:** DataFrameGroupBy.apply on home/away rolling features — cosmetic, not breaking.
- **Alembic migration chain:** `1b5f0d9ad7c1` → `7e1d92d75f3d`. A stub migration was added for `1b5f0d9ad7c1` to complete the revision chain.
- **Git remote:** `git@github.com:jbl306/nba-ml-engine.git`, homelab remote: `git@github.com:jbl306/homelab.git`
- **Key null fields fixed:** position (was 100% null, now 100% filled for active), starter (was 100% null, now 97.6% filled)
- **game_advanced_stats.ts_pct has 10,695 nulls** — likely zero-FGA games where TS% is undefined
- **API budget assessment:** Currently ~16 requests/day to nba_api. Can safely add ~33 more (total ~49/day).
- **The Odds API:** 500 requests/month free tier, ~8-10/day used. Markets: points, rebounds, assists, threes, steals, blocks.

## Important Files

- `docs/plan/progress_data-source-expansion.md`
- **THE primary progress tracker** for the current sprint — tracks all phases
- Shows Phase 1A-1C complete/partial, Phase 2-4 pending
- Contains deployment commands, accuracy tables, decision log

- `src/data/nba_ingest.py`
- Central data ingestion module — all NBA API, CDN, and backfill functions
- Key functions: daily_update(), sync_player_positions(), backfill_starters_cdn(), ingest_game_advanced_stats_cdn(), populate_starters_cdn()
- Still needs: tracking stats ingestion, hustle stats ingestion

- `src/features/builder.py` (~765 lines)
- Feature engineering pipeline — build_features() is main entry
- New: _add_starter_features() (4 features), _add_game_advanced_rolling() (14 features)
- Still needs: tracking rolling features, hustle features, BBRef features

- `src/db/models.py`
- All SQLAlchemy models including 6 new tables from migration
- GameAdvancedStats populated (270K rows), GameTrackingStats/HustleStats/BBRefAdvancedStats/GameLines/DailyLineups empty

- `main.py`
- CLI entry point — backfill command with --positions, --starters-cdn, --advanced-per-game-cdn flags
- Pipeline command runs 7-step daily process

- `config.py`
- Central configuration — STAT_EDGE_THRESHOLDS, EXCLUDED_PROP_STATS, all feature windows
- NBA_CDN_DELAY env var (0.2s default)

- `/home/jbl/projects/homelab/compose/compose.nba-ml.yml`
- Docker Compose for all services — crons at 3am ET
- Must use `--env-file ../.env` from homelab dir

- `alembic/versions/7e1d92d75f3d_add_data_source_expansion_tables_and_.py`
- Migration adding 6 tables + 7 player columns, all idempotent

- `docs/reports/data-validation-source-evaluation_0319.md`
- Comprehensive data validation + source evaluation report from Sprint 2
- Lists all 137 nba_api endpoints, priority recommendations, rate limit budget

## Next Steps

**User's explicit request for Sprint 3:**
"Check docs from today then continue implementation from progress_data-source-expansion.md and deploy to my homelab server. Then validate data was added correctly, validate the complete set of data, evaluate the prediction model implementation and suggest further improvements - create this in a report under docs/reports."

**Remaining work from progress tracker:**
1. **Phase 2A: Player Tracking Stats** — Implement `ingest_game_tracking_stats()` using BoxScorePlayerTrackV3 (speed, distance, touches, passes, contested shots). Table exists, need ingestion + backfill + builder features.
2. **Phase 2C: Hustle Stats** — Implement `ingest_hustle_stats()` using LeagueHustleStatsPlayer (deflections, contested shots, loose balls, box outs). Table exists, need ingestion + backfill + builder features.
3. **Phase 2B: Basketball Reference** — Implement `src/data/bbref.py` for WS/BPM/VORP. Table exists, need scraper + backfill + builder features.
4. **Wire new features into builder.py** — tracking rolling, hustle features, BBRef quality metrics.
5. **Deploy to homelab** — Build new Docker image, run migrations, execute backfills.
6. **Retrain all models** with expanded feature set.
7. **Validate all data** — null checks, coverage, integrity across all tables.
8. **Evaluate model performance** — compare R² before/after, especially STL/BLK (0.09 baseline).
9. **Create evaluation report** at `docs/reports/` with findings and improvement suggestions.

**Immediate next actions:**
- Set up SQL todos for Sprint 3 tasks
- Implement Phase 2A (tracking stats), 2C (hustle stats), 2B (BBRef) — these are the highest-value additions
- Add corresponding features to builder.py
- Deploy, backfill, retrain, evaluate
- Write comprehensive evaluation report

## Related Wiki Pages

- [[Data Source Expansion for NBA ML Prediction Platform]]
- [[Homelab Server Deployment Architecture for NBA ML Platform]]
- [[Feature Engineering Pipeline for NBA ML Platform]]
- [[NBA ML Engine]]
- [[EnsembleModel]]
- [[Homelab]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-data-source-expansion-exploration-b12f747f.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-03-20 |
| URL | N/A |
