---
title: "Copilot Session Checkpoint: Dashboard Prop Line Debug"
type: source
created: '2026-04-26'
last_verified: '2026-04-26'
source_hash: c2c0b403ca84102b5639f0814e04189e2d2a50aa84ef2285c49382b8648be67b
sources:
  - raw/2026-04-26-copilot-session-dashboard-prop-line-debug-ccc0f19c.md
concepts:
  - source-priority-canonical-prop-ingestion
  - browser-backed-sportsbook-truth-validation
  - standard-over-under-vs-milestone-prop-market-identity
related:
  - "[[NBA ML Engine]]"
  - "[[MemPalace]]"
  - "[[DraftKings Sportsbook]]"
  - "[[FanDuel Sportsbook]]"
  - "[[SportsGameOdds (SGO) API]]"
  - "[[Architectural Source Priority vs Live Prop-Line Incident Diagnosis]]"
tags: [copilot-session, checkpoint, nba-ml-engine, prop-lines, sportsbook-data, dashboard, mempalace]
tier: hot
checkpoint_class: durable-debugging
retention_mode: retain
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 76
---

# Copilot Session Checkpoint: Dashboard Prop Line Debug

## Summary

This checkpoint preserves the state of a live [[NBA ML Engine]] incident after a large audit, implementation, deployment, and validation sprint had already landed on `main`. Its durable value is not just the open Josh Hart prop-line question, but the debugging frame it establishes: source-priority architecture can be correct on paper while the live dashboard still shows lower-trust rows if direct-book data is absent, stale, misclassified, or never ingested.

It also captures two adjacent operational lessons that matter for future incidents: sportsbook truth disputes must be traced across UI, provider, DB, and serving layers in order, and homelab reachability must distinguish LAN HTTP from public HTTPS instead of treating them as one validation surface.

## Key Points

- The broader sprint had already completed before this checkpoint: audit recommendations were implemented, merged to `main`, deployed to homelab, Alembic migrations were applied through `f4a1c7d9e2b0`, and materialized views were refreshed successfully.
- Live validation confirmed the current user-facing symptom: the dashboard and FastAPI still exposed two Josh Hart `stl` rows, `SGO_DK line=0.5` and `SGO_FD line=1.5`, despite the direct-source-priority architecture added in the prior ingestion work.
- The checkpoint preserves the explicit bookmaker/source trust ladder: `DK_WEB` and `FD_WEB` rank above `DK` and `FD`, which rank above `SGO_DK` and `SGO_FD`; unknown sources fall below all known bookmaker mappings.
- It records the key serving contract behind the issue: `mv_prop_lines_primary` chooses one row per `(player_id, game_date, stat_name, source_bookmaker)`, and the dashboard BFF `/api/props` reads from that view while FastAPI edge routes apply the same source-priority helpers directly.
- The source restates a crucial taxonomy lesson from earlier research: DraftKings **Steals O/U 0.5** and a user-visible **2+ steals** ladder are different market families, so a mismatch can reflect market identity rather than a bad canonical row.
- The checkpoint narrows the likely root causes to operational ones: direct DK/FD ingestion may not have run after deploy, direct fetches may have failed, direct rows may exist but not be selected, or the product may need clearer UX around standard O/U versus milestone markets.
- It preserves a precise incident workflow: query `prop_lines`, `mv_prop_lines_primary`, `prop_line_snapshots`, and generic sportsbook tables for Josh Hart; inspect runtime config and API logs; run a bounded direct-fetch smoke test; then decide whether the bug is ingestion freshness, query logic, or UI semantics.
- A separate but durable deployment lesson was added in the same checkpoint: LAN HTTP, local/container health, and public HTTPS are different validation layers, so public-edge failures should not invalidate a confirmed LAN-success path.
- The checkpoint also records environment-specific operational quirks that are easy to forget under pressure, including `PYTHONPATH=/app` for Alembic inside `nba-ml-api`, authenticated LAN FastAPI checks with `X-API-Key`, and the fact that view DDL changes require drop/recreate or migration rather than `CREATE MATERIALIZED VIEW IF NOT EXISTS`.

## Key Concepts

- [[Source-Priority Canonical Prop Ingestion]]
- [[Browser-Backed Sportsbook Truth Validation]]
- [[Standard Over/Under vs Milestone Prop Market Identity]]
- [[Architectural Source Priority vs Live Prop-Line Incident Diagnosis]]

## Related Entities

- **[[NBA ML Engine]]** — The production pipeline whose direct-book ingestion, materialized views, and dashboard serving path are being debugged.
- **[[DraftKings Sportsbook]]** — The bookmaker behind the contested `0.5` standard O/U versus `2+` milestone interpretation.
- **[[FanDuel Sportsbook]]** — The direct-book reference that had previously validated Josh Hart steals at `1.5`, making its live absence diagnostically important.
- **[[SportsGameOdds (SGO) API]]** — The lower-trust fallback feed whose `SGO_DK` and `SGO_FD` rows still surfaced live and therefore framed the incident.
- **[[MemPalace]]** — The memory system that preserved prior sportsbook-truth findings and helped this session resume from durable context instead of re-investigating from scratch.

