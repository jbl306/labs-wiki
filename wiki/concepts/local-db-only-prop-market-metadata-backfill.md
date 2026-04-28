---
title: "Local DB-Only Prop Market Metadata Backfill"
type: concept
created: 2026-04-25
last_verified: 2026-04-25
source_hash: "bb9e0e187a674b361745d7868096604ab473d7668e4150d2c9f287781caa7f56"
sources:
  - raw/2026-04-25-copilot-session-direct-sportsbook-ingestion-a78d087a.md
related:
  - "[[Source-Priority Canonical Prop Ingestion]]"
  - "[[Generic Sportsbook Market Storage for Non-Canonical Props]]"
  - "[[Free-Tier-Constrained Backfill Runner Design]]"
  - "[[Heuristic Cleanup vs Market-Aware Prop Ingestion]]"
tier: hot
tags: [sports-betting, backfill, data-migration, prop-lines, nba-ml-engine]
quality_score: 85
---

# Local DB-Only Prop Market Metadata Backfill

## Overview

Local DB-only prop market metadata backfill is a migration pattern for upgrading historical sportsbook rows without re-fetching external providers. Instead of spending sportsbook or aggregator quota to reconstruct metadata after a schema change, the system derives what it safely can from already stored local rows, exposes a dry-run by default, and makes the write step explicit with an `--apply` flag.

This matters when production data needs better semantics faster than external APIs can be queried safely. In the checkpoint, the immediate need was to classify existing canonical prop rows with bookmaker and market metadata while honoring the user's instruction to be careful with rate limits.

## How It Works

The trigger for this concept is a common operational trap: after improving the schema, the newest rows are rich but historical rows are semantically poor. The direct sportsbook ingestion work added `bookmaker`, `market_scope`, `market_class`, and related logic to the live pipeline, but the existing database still held a large body of older prop rows and snapshots that predated those columns. If left untouched, query code would have to treat old and new data differently, and historical dashboards would continue to reflect a weaker contract than the current ingestion path. The obvious brute-force answer would be to re-pull historical markets from external providers, but that would consume quota, amplify rate-limit risk, and likely fail to reproduce time-local sportsbook states anyway.

The backfill therefore works from the data already in hand. The new CLI entry point, `python main.py backfill-prop-market-metadata`, reads the local database and classifies rows using durable rules derived from the same ingestion architecture. Sources such as `DK_WEB`, `DK`, and `SGO_DK` imply bookmaker `draftkings`; `FD_WEB`, `FD`, and `SGO_FD` imply `fanduel`. For the rows being upgraded, the backfill sets `market_scope='player'` and `market_class='standard_ou'`, reflecting the new contract that canonical `prop_lines` holds only model-ready standard player over/under markets. This is not a speculative reconstruction of every missing historical market; it is a conservative semantic upgrade of rows the system already decided to keep as canonical.

Two design choices make the pattern operationally safe. First, the command is **dry-run by default**. Running `python main.py backfill-prop-market-metadata` reports what would change without mutating the database. An operator must add `--apply` to perform the update. That protects against accidental bulk writes during exploratory sessions and makes the tool suitable for staging, inspection, and later production use. Second, the command is explicitly **local DB-only**. The checkpoint calls out that it performs no external API calls, which preserves quota and respects the user's rate-limit concern. In other words, this is a metadata repair operation, not a historical market re-ingestion operation.

The checkpoint also documents an important implementation correction. The initial version loaded rows with an unbounded `.all()`, which worked functionally but created a memory-risk code path for large tables. A review flagged that as unsafe, and the final implementation switched to grouped counts and bulk updates per `source` instead. That change is not incidental; it is part of why the concept is durable. Backfills often fail not because the mapping logic is wrong, but because the implementation assumes the dataset is small enough to materialize all at once. By moving to source-grouped updates, the command aligns with the same philosophy as the rest of the checkpoint: explicit contracts, bounded resource use, and safe defaults.

The local-only approach also clarifies what backfill can and cannot do. It can reliably enrich canonical rows with bookmaker and market metadata when those attributes are implied by stored source labels and current architectural decisions. It cannot recreate non-canonical milestone or game markets that were never stored separately before the schema split. Nor can it reconstruct missing line-movement history that old snapshot keys collapsed. That limitation is acceptable because the purpose of the backfill is forward-compatibility, not historical perfection. It makes old rows participate cleanly in new queries, especially filters on `market_scope` and `market_class`, without pretending the system can recover information it never stored.

This concept fits into a broader migration pattern: when a schema becomes more semantically expressive, do the minimal truthful upgrade locally, and let future ingests populate richer detail natively. The database becomes more queryable immediately, the live pipeline remains quota-safe, and operators retain control over when the mutation is applied. That is a much more reliable operational posture than coupling schema rollout to uncertain historical re-fetching.

## Key Properties

- **Dry-run first:** The command does nothing destructive unless `--apply` is provided.
- **Quota-safe:** Classification is derived from local DB state, not external sportsbook or aggregator calls.
- **Bulk-update oriented:** The final implementation avoids unbounded `.all()` loading and updates rows in grouped batches.
- **Forward-compatible:** Historical rows are upgraded just enough to participate in the new canonical query contract.

## Limitations

Local classification can only infer what the stored source labels and current architecture make explicit. It cannot resurrect non-canonical markets that were previously dropped or recover per-fetch snapshot history that older schemas never preserved. It also assumes the source-to-bookmaker mapping remains historically valid for the rows being updated.

## Examples

```bash
# inspect impact only
python main.py backfill-prop-market-metadata

# apply metadata updates to existing canonical rows
python main.py backfill-prop-market-metadata --apply
```

## Practical Applications

This concept is useful whenever a live sports or ML system tightens its data model but cannot afford a full historical re-ingest. In the [[NBA ML Engine]], it provides the bridge between older prop rows and the new source-priority, market-aware serving contract without burning provider quota.

## Related Concepts

- **[[Generic Sportsbook Market Storage for Non-Canonical Props]]** — Defines the richer target schema that the backfill is trying to make historical rows compatible with.
- **[[Source-Priority Canonical Prop Ingestion]]** — Consumes the upgraded metadata to make better canonical-line decisions.
- **[[Free-Tier-Constrained Backfill Runner Design]]** — Shares the operational idea that backfill jobs should respect bounded external resources and prefer safe defaults.

## Sources

- [[Copilot Session Checkpoint: Direct Sportsbook Ingestion]] — primary source for the dry-run DB-only classifier, grouped bulk updates, and rate-limit-safe historical migration

