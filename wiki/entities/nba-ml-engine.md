---
title: "NBA ML Engine"
type: entity
created: 2026-04-18
last_verified: 2026-04-25
source_hash: "665c60129067f8fba29792521cb202b0e0ab91fc22982f1f58081019b034c549"
sources:
  - raw/2026-04-25-copilot-session-backtest-completion-props-investigation-ed8d6cc6.md
  - raw/2026-04-20-copilot-session-scheduler-dns-agents-cleanup-2222559c.md
  - raw/2026-04-19-copilot-session-sprint-61-planning-audit-6c5cb258.md
  - raw/2026-04-19-copilot-session-sprint-60-pts-feature-planning-abd21993.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-12-complete-and-skills-installed-48a02b58.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-11-evaluation-and-report-5b560f0f.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-retrain-in-progress-742b0d94.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-implementation-and-deployment-693c9264.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-complete-and-deployed-cb380016.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-react-dashboard-scaffold-and-pages-built-2fe5dac8.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-rankings-page-and-performance-optimization-8063e05f.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-props-db-query-and-chart-refinement-402d70da.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-phases-1-4-implementation-and-deployment-16041f82.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-nba-ml-agents-and-homelab-fixes-646cf99a.md
  - raw/2026-04-18-copilot-session-training-status-tracker-and-oom-fix-6c60a486.md
  - raw/2026-04-18-copilot-session-sprint-55-planning-and-exploration-be98e3c5.md
  - raw/2026-04-18-copilot-session-sprint-55-implementation-and-deployment-2d04e4e0.md
  - raw/2026-04-18-copilot-session-sprint-58-shap-bug-planning-dfccfb5c.md
  - raw/2026-04-18-copilot-session-sprint-57-ensemble-save-diagnosis-e2943da5.md
quality_score: 95
concepts:
  - nba-ml-engine
related:
  - "[[Ensemble Model Save-Round-Trip Validation Gate]]"
  - "[[Root-Cause Analysis of Silent Ensemble Model Save Failures]]"
  - "[[Copilot Session Checkpoint: Sprint 57 Ensemble Save Diagnosis]]"
  - "[[Labs-Wiki]]"
  - "[[EnsembleModel]]"
tier: hot
tags: [ml-engine, nba, artifact-validation, ensemble-model]
---

# NBA ML Engine

## Overview

The NBA ML Engine is a machine learning pipeline used for training, validating, and deploying statistical models for NBA data analysis. It features ensemble modeling, artifact registry, and automated training loops, with robust mechanisms for artifact validation and promotion.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

Central to the session history, the NBA ML Engine keeps accumulating durability lessons about how model quality should be surfaced and validated in production. This later checkpoint adds two important ones: headline Backtesting metrics must reconcile to settled Props History at the same `player/date/stat` grain, and current-slate prop surfaces cannot be trusted unless sportsbook/provider/DB alignment has been validated explicitly.

## Associated Concepts

- **[[Ensemble Model Save-Round-Trip Validation Gate]]** — Validation gate is integrated into the NBA ML Engine's training loop.
- **[[Root-Cause Analysis of Silent Ensemble Model Save Failures]]** — Analysis targets silent failures in the NBA ML Engine's artifact saving process.
- **[[Canonical Settled-Prop Backtesting for Trustworthy ML Dashboards]]** — Defines the trust contract for the engine's Backtesting page.
- **[[Primary Prop Line Selection to Avoid Alternate Line Contamination]]** — Captures one of the engine's recurring sportsbook data-cleaning challenges.

## Related Entities

- **[[Labs-Wiki]]** — Destination for durable Copilot checkpoints and lessons learned.
- **[[EnsembleModel]]** — co-mentioned in source (Model)

## Sources

- [[Copilot Session Checkpoint: Sprint 57 Ensemble Save Diagnosis]] — where this entity was mentioned
- [[Copilot Session Checkpoint: Sprint 58 SHAP Bug Planning]] — additional source
- [[Copilot Session Checkpoint: Sprint 55 Implementation and Deployment]] — additional source
- [[Copilot Session Checkpoint: Sprint 55 Planning and Exploration]] — additional source
- [[Copilot Session Checkpoint: Training Status Tracker and OOM Fix]] — additional source
- [[Copilot Session Checkpoint: NBA-ML Agents and Homelab Fixes]] — additional source
- [[Copilot Session Checkpoint: Phases 1-4 Implementation and Deployment]] — additional source
- [[Copilot Session Checkpoint: Props DB Query and Chart Refinement]] — additional source
- [[Copilot Session Checkpoint: Rankings Page and Performance Optimization]] — additional source
- [[Copilot Session Checkpoint: React Dashboard Scaffold and Pages Built]] — additional source
- [[Copilot Session Checkpoint: Sprint 10 Complete and Deployed]] — additional source
- [[Copilot Session Checkpoint: Sprint 10 Implementation and Deployment]] — additional source
- [[Copilot Session Checkpoint: Sprint 10 Retrain In Progress]] — additional source
- [[Copilot Session Checkpoint: Sprint 11 Evaluation and Report]] — additional source
- [[Copilot Session Checkpoint: Sprint 12 Complete and Skills Installed]] — additional source
- [[Copilot Session Checkpoint: Sprint 60 PTS Feature Planning]] — additional source
- [[Copilot Session Checkpoint: Sprint 61 Planning + Audit]] — additional source
- [[Copilot Session Checkpoint: Scheduler DNS Agents Cleanup]] — additional source
- [[Copilot Session Checkpoint: Backtest Completion Props Investigation]] — completed backtest reconciliation and preserved the next prop-line integrity investigation
