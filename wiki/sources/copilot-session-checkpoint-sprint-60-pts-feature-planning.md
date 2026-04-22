---
title: "Copilot Session Checkpoint: Sprint 60 PTS Feature Planning"
type: source
created: 2026-04-19
last_verified: 2026-04-19
source_hash: "d9cea72e0198e7d3d24aa2f2351ac17ebe1246338b49cf42f47130ad7dc14949"
sources:
  - raw/2026-04-19-copilot-session-sprint-60-pts-feature-planning-abd21993.md
quality_score: 83
concepts:
  - pts-feature-engineering-opponent-defensive-rating-rolling-window
  - teammate-injured-usage-delta-feature
  - classifier-stats-extension-calibration-audit
related:
  - "[[PTS Feature Engineering With Opponent Defensive Rating Rolling Window]]"
  - "[[Teammate-Injured-Usage Delta Feature]]"
  - "[[Classifier Stats Extension and Calibration Audit]]"
  - "[[NBA ML Engine]]"
  - "[[SGO (SportsGameOdds) API]]"
tier: archive
tags: [checkpoint, agents, dashboard, nba-ml-engine, nba-ml, calibration, rolling-window, injury-impact, homelab, fileback, durable-knowledge, copilot-session, feature-engineering]
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: planned
---

# Copilot Session Checkpoint: Sprint 60 PTS Feature Planning

## Summary

This checkpoint documents the planning phase for Sprint 60 of the NBA ML Engine, focusing on implementing feature engineering and model improvements to lift prediction accuracy, especially for points (PTS) and classifier stats. The session includes a detailed audit of existing features, identification of gaps, and a prioritized action plan for code changes, calibration audits, and hygiene tasks. Odds API budget constraints block some prop-market expansion items, and the session sets up for code-only changes to be deployed with the next weekly retrain.

## Key Points

- Tier A focus on PTS feature engineering: opponent defensive rating rolling window, teammate-injured-usage delta, position-adjusted opponent points-allowed.
- Extending CLASSIFIER_STATS and calibration audit; hygiene tasks include snapshot retention pruning and ensemble pickle removal.
- Odds API quota exhausted, blocking prop-line backfill; strategy is to implement code-only changes for next retrain and run calibration audit immediately.

## Concepts Extracted

- **[[PTS Feature Engineering With Opponent Defensive Rating Rolling Window]]** — PTS feature engineering in Sprint 60 centers on introducing new features that capture opponent team defensive strength as a rolling window, and interactions with player usage. This approach aims to address gaps identified in prior SHAP analyses, where defensive matchup signals were underrepresented in points prediction models.
- **[[Teammate-Injured-Usage Delta Feature]]** — The teammate-injured-usage delta feature quantifies the impact of injured teammates on a player's opportunity, weighting each injured teammate by their recent usage percentage. This provides a more nuanced signal than simple counts, capturing shifts in team dynamics that affect individual player performance.
- **[[Classifier Stats Extension and Calibration Audit]]** — Sprint 60 includes extending classifier stats to new categories (fg_pct, ft_pct) and performing a calibration audit across all stat models. This ensures model outputs are well-calibrated and that classifier coverage aligns with available target columns.

## Entities Mentioned

- **[[NBA ML Engine]]** — The NBA ML Engine is a machine learning platform for predicting NBA player statistics, leveraging advanced feature engineering, classifier models, and calibration protocols. It supports modular feature pipelines, rolling window statistics, and integrates with external APIs for prop-line and odds data.
- **[[SGO (SportsGameOdds) API]]** — The SGO API provides prop-line and odds data for NBA games, used in the NBA ML Engine for feature engineering and market expansion. Data quality gates and API quota constraints are critical operational considerations.

## Notable Quotes

> "Sprint 60 recommendation #1 maps to: NEW opp_team_def_rating_roll_10 (opponent's recent defensive rating, rolling over their last 10 games) + interaction opp_team_def_rating_roll_10 × gadv_usg_pct." — Session summary
> "Sprint 59 SHAP findings drove Sprint 60 plan: PTS (Ridge wrapper) top features: predicted_minutes (13%), bbref_per (3.6%), minutes_roll_20_mean (3.0%) — usage/minutes dominates, defensive matchup signal underrepresented." — Technical details

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-19-copilot-session-sprint-60-pts-feature-planning-abd21993.md` |
| Type | note |
| Author | Unknown |
| Date | 2026-04-19 |
| URL | N/A |
