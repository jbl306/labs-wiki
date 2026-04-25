---
title: "Copilot Session Checkpoint: Direct Sportsbook Ingestion"
type: source
created: '2026-04-25'
last_verified: '2026-04-25'
source_hash: bb9e0e187a674b361745d7868096604ab473d7668e4150d2c9f287781caa7f56
sources:
  - raw/2026-04-25-copilot-session-direct-sportsbook-ingestion-a78d087a.md
concepts:
  - source-priority-canonical-prop-ingestion
  - generic-sportsbook-market-storage-non-canonical-props
  - local-db-only-prop-market-metadata-backfill
  - primary-prop-line-selection-to-avoid-alternate-line-contamination
related:
  - "[[Copilot Session Checkpoint: Direct Sportsbook Sources]]"
  - "[[Heuristic Prop-Line Selection vs Direct Sportsbook Validation]]"
  - "[[NBA ML Engine]]"
  - "[[DraftKings Sportsbook]]"
  - "[[FanDuel Sportsbook]]"
  - "[[Odds API]]"
  - "[[SportsGameOdds (SGO) API]]"
tags: [copilot-session, checkpoint, nba-ml-engine, sportsbook-data, prop-ingestion, draftkings, fanduel, durable-knowledge]
tier: hot
checkpoint_class: durable-workflow
retention_mode: retain
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 79
---

# Copilot Session Checkpoint: Direct Sportsbook Ingestion

## Summary

This checkpoint turns the earlier sportsbook-truth investigation into production ingestion architecture for the [[NBA ML Engine]]. It adds direct DraftKings and FanDuel adapters, explicit source-priority rules, market-aware storage that separates canonical player over/under rows from generic sportsbook markets, and a local DB-only backfill path that upgrades historical metadata without spending external API quota.

## Key Points

- The implementation stayed TDD-first on branch `feature/direct-sportsbook-ingestion`, using a dedicated worktree so the direct-book ingestion work could ship without disturbing the existing dashboard-accuracy branch flow.
- Source priority is now explicit and bookmaker-aware: `DK_WEB` and `FD_WEB` rank above `DK` and `FD`, which rank above `SGO_DK` and `SGO_FD`, while unknown vendors are isolated under synthetic bookmaker keys instead of shadowing trusted rows.
- `prop_lines` is intentionally narrowed to model-ready **standard player O/U** markets only; metadata columns `bookmaker`, `market_scope`, `market_class`, and `provider_market_id` make that contract explicit.
- A new generic storage layer, `sportsbook_markets` plus `sportsbook_market_snapshots`, captures milestone ladders, game props, spreads, totals, moneylines, and other sportsbook markets that are useful to retain but unsafe to treat as canonical model inputs.
- Direct adapters were added under `src/data/sportsbooks/`: FanDuel parses standard `MOVING_HANDICAP` player O/U markets, while DraftKings routes standard `Steals O/U` rows into `prop_lines` and sends milestone/game markets into the generic sportsbook tables.
- The DraftKings adapter defaults to subcategories `4511`, `13508`, and `16485`, so the pipeline can cover NBA main/game props, standard steals O/U, and steals milestone ladders in one pass.
- `fetch_prop_lines()` now settles snapshots, pulls direct sportsbook rows first, then [[Odds API]], then [[SportsGameOdds (SGO) API]], writes generic market rows, normalizes standard prop rows, applies validation filters, enforces source priority, deletes shadowed current rows, and finally upserts current props and snapshots.
- Historical cleanup was designed to respect rate limits: `python main.py backfill-prop-market-metadata` is dry-run by default, uses only local DB classification, and upgrades existing rows in bulk without calling external sportsbook or aggregator APIs.
- The serving layer was updated too: `mv_prop_lines_primary` and `src/applications/prop_finder.py` now filter to `market_scope='player'` and `market_class='standard_ou'`, then rank source priority before "closest to prediction" so user-facing lines reflect explicit bookmaker truth preference rather than a heuristic alone.
- Security and operational hardening were part of the same change set: FanDuel state hosts are whitelist-validated, DraftKings subcategory IDs must be numeric-only, provider failures log warnings without aborting fallback providers, and the final checkpoint recorded a clean full-suite result of **427 passed, 9 skipped, 14 deselected, 1 warning**.
- The only unfinished operational step at compaction was merging to `main`; the feature branch was committed and pushed, but merge was blocked by an unrelated dirty file in the main worktree that the session correctly avoided overwriting.

## Key Concepts

- [[Source-Priority Canonical Prop Ingestion]]
- [[Generic Sportsbook Market Storage for Non-Canonical Props]]
- [[Local DB-Only Prop Market Metadata Backfill]]
- [[Primary Prop Line Selection to Avoid Alternate Line Contamination]]

## Related Entities

- **[[NBA ML Engine]]** — The production system whose ingestion, query, and dashboard layers were upgraded to prefer direct sportsbook truth and preserve richer market taxonomy.
- **[[DraftKings Sportsbook]]** — Supplies the direct `DK_WEB` rows and the non-canonical milestone/game markets that now get stored separately instead of contaminating `prop_lines`.
- **[[FanDuel Sportsbook]]** — Supplies direct `FD_WEB` standard O/U rows and motivated host-validation hardening for state-specific `sbapi` endpoints.
- **[[Odds API]]** — Remains the higher-trust aggregator fallback once direct-book rows have been attempted and normalized.
- **[[SportsGameOdds (SGO) API]]** — Remains the lowest-priority fallback because it can contain mixed market families and stale or ambiguous bookmaker truth.

