---
title: "Copilot Session Checkpoint: Backtest Completion Props Investigation"
type: source
created: '2026-04-25'
last_verified: '2026-04-25'
source_hash: b92cfc3a79758f18c7c3a60e9fb494eaf9c494ca4efe8d3fc80f6ab05e168d93
sources:
  - raw/2026-04-25-copilot-session-backtest-completion-props-investigation-ed8d6cc6.md
concepts:
  - canonical-settled-prop-backtesting-trustworthy-ml-dashboards
  - broad-diagnostic-backtesting-secondary-model-evidence
  - primary-prop-line-selection-to-avoid-alternate-line-contamination
  - sportsgameodds-sgo-api-data-extraction-challenges
related:
  - "[[NBA ML Engine]]"
  - "[[SportsGameOdds (SGO) API]]"
  - "[[FastAPI]]"
  - "[[Express.js]]"
  - "[[MemPalace]]"
  - "[[Copilot CLI]]"
tags: [copilot-session, checkpoint, nba-ml-engine, backtesting, prop-lines, sportsgameodds, dashboard, data-integrity]
tier: hot
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 78
---

# Copilot Session Checkpoint: Backtest Completion Props Investigation

## Summary

This checkpoint captures the completed implementation, validation, deployment, and live reconciliation of the [[NBA ML Engine]] Backtesting page redesign, then pivots into a new high-priority investigation of sportsbook prop-line integrity. Its durable value is twofold: canonical headline backtest metrics must align with Props History at the same grain, and sportsbook truth problems cannot be "fixed" safely by heuristics alone without checking provider payloads, production tables, and real bookmaker UI.

The source closes the backtest thread with a concrete production validation result, then preserves the open debugging frame for the Josh Hart / DraftKings / FanDuel mismatch so a future investigation can resume with the right evidence chain and prior-art warnings in place.

## Key Points

- The backtest redesign was completed end-to-end: canonical settled props now drive the headline page, while the broad `predictions × game_logs × prop_lines` view remains a secondary diagnostic.
- Validation covered Python tests, TypeScript contract tests, React build, and homelab deployment; the work was reported under `reports/2026-04-25-backtest-accuracy-page-status.md` and pushed to GitHub `main`.
- A late live-validation bug exposed the real canonical grain: the initial endpoint ranked one row per `player_id/game_date/stat_name/source`, which inflated `canonical_total` to **8,394** while Props History stayed at **4,197**.
- The fix was to partition canonical ranking by `snap.player_id, snap.game_date, snap.stat_name` only, making the canonical population source-agnostic while still preserving the chosen row's source as descriptive metadata.
- After redeploy, live numbers aligned exactly: Backtest canonical total **4,197**, Props History total **4,197**, hit rate **0.5282**, and flat P&L **237**.
- Broad diagnostics still intentionally differ after the fix: the broader materialized-view evidence remained **11,400** calls and is useful for monitoring but not for the dashboard's headline trust claim.
- BFF hardening in the same session included `days` validation/clamping to `1..365`, semantic sorting for broad edge buckets, and explicit TypeScript-safe broad diagnostic rows.
- The new active incident is a prop-line integrity mismatch: the user reported Josh Hart steals showing **2+** on the DraftKings UI, while the live dashboard/API showed `SGO_DK stl line=0.5` and `SGO_FD stl line=1.5`.
- Prior durable context from [[MemPalace]] matters here: SportsGameOdds has previously mixed standard over/under props with alternate or game-prop markets, and the extractor historically let the first `(player_id, date, source, stat_name)` row win.
- The checkpoint explicitly warns against jumping straight to a fix: the right validation chain is sportsbook UI -> raw provider payload -> `prop_lines` / `prop_line_snapshots` -> `/api/props`, followed by a report, not immediate code changes.

## Key Concepts

- [[Canonical Settled-Prop Backtesting for Trustworthy ML Dashboards]]
- [[Broad Diagnostic Backtesting as Secondary Model Evidence]]
- [[Primary Prop Line Selection to Avoid Alternate Line Contamination]]
- [[SportsGameOdds (SGO) API Data Extraction Challenges]]
- [[Canonical Settled Backtests vs Broad Diagnostic Backtests]]

## Related Entities

- **[[NBA ML Engine]]** — The production system whose backtest architecture was finalized and whose prop-line integrity is now under audit.
- **[[SportsGameOdds (SGO) API]]** — The external odds provider implicated in alternate-line contamination and current DK/FD validation work.
- **[[FastAPI]]** — Serves `/evaluation/backtest/canonical` and `/prop-edges`, the main backend surfaces discussed in the checkpoint.
- **[[Express.js]]** — The BFF layer that proxies `/api/backtest` and `/api/props` to the dashboard.
- **[[MemPalace]]** — Preserved earlier lessons about SGO alternate-line contamination that shaped the current investigation.
- **[[Copilot CLI]]** — The agent runtime used to implement, validate, deploy, and checkpoint the work.
