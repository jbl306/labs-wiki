---
title: "Point-in-Time Prop Snapshot Identity"
type: concept
created: 2026-05-31
last_verified: 2026-05-31
source_hash: "4789cd410f350d2cdd568e54d1046ea32d670d8e84f60dd954754b706b61ec98"
sources:
  - raw/2026-05-31-copilot-session-sprint-accuracy-planning-8edf737a.md
  - raw/2026-05-31-copilot-session-canonical-props-implementation-c9632506.md
quality_score: 87
related:
  - "[[Generic Sportsbook Market Storage for Non-Canonical Props]]"
  - "[[Source-Priority Canonical Prop Ingestion]]"
  - "[[Dashboard Duplicate Predictions Fix in ML Systems]]"
  - "[[Canonical Settled-Prop Backtesting for Trustworthy ML Dashboards]]"
tier: hot
tags: [sports-betting, data-modeling, snapshots, time-series, data-integrity, nba-ml-engine]
---

# Point-in-Time Prop Snapshot Identity

## Overview

Point-in-time prop snapshot identity is the rule that each captured sportsbook line should be stored as its own immutable historical event rather than being merged into a coarse "latest known line" key. In the [[NBA ML Engine]], that means `prop_line_snapshots` should preserve every distinct `fetched_at` observation for a player/stat/source combination instead of letting later captures overwrite earlier evidence.

This matters because downstream evaluation logic treats snapshots as historical truth. If the storage layer silently collapses multiple captures into one row, every later metric built on that table inherits fake history: line movement disappears, settlement matching loses provenance, and calibration or backtest joins can only reason over a distorted record of what the system actually saw.

## How It Works

The checkpoint records the failure mode in unusually concrete terms. `prop_line_snapshots` had **24,421** rows and **24,421** coarse identities under the older uniqueness contract. That one-to-one ratio sounds clean at first, but it is actually evidence that repeat captures were not surviving. If a snapshot table is supposed to preserve time-varying line movement, some subset of rows should share the same player, game date, stat, and source while differing in fetch time or prices. Instead, the old constraint effectively said: for a given `player_id`, `game_date`, `stat_name`, and `source`, there can be only one stored snapshot. A structure named "snapshots" was behaving like a shadow copy of a mutable current table.

The new identity rule corrects that by making time part of the key rather than incidental metadata. Conceptually, the identity becomes

$$
\text{snapshot\_id} = (\text{player\_id}, \text{game\_date}, \text{source}, \text{stat\_name}, \text{fetched\_at})
$$

The key idea is not that `fetched_at` is merely recorded. It must participate in uniqueness. Once that is true, two captures of the same DraftKings rebounds line at different times are allowed to coexist, while an exact duplicate replay of the same capture becomes safely idempotent.

This change has both a schema layer and a write-path layer. At the schema level, the checkpoint adds an Alembic migration that removes the older coarse constraint and replaces it with a point-in-time unique index on `player_id / game_date / source / stat_name / fetched_at`. At the write path, `src/data/prop_lines.py` changes `_build_snapshot_upsert_statement` to `on_conflict_do_nothing`. That choice is subtle and important. An upsert that updates existing rows would still allow later runs to mutate prior history. `do_nothing` says something stronger: if this exact point-in-time capture already exists, treat the ingest as a replay and keep history unchanged.

The operational flow therefore becomes much more like event capture than state replacement. A fetch run produces normalized prop rows, attaches the observation timestamp, applies validation and suspicious-line quarantine, writes the current-surface tables used for live serving, and independently inserts snapshot rows keyed by the point-in-time identity. Current rows may legitimately change because the system needs a "latest" view for serving. Snapshot rows should not. They are the historical ledger that later analytics depend on.

Why does this matter so much downstream? Because the rest of the checkpoint moves critical logic away from mutable `prop_lines` joins and toward `prop_line_snapshots`. The canonical settled-prop helper picks one settled snapshot per `player_id / game_date / stat_name` using source priority. Calibration and model-health consumers then reuse that same settled evidence. If the snapshot table does not actually preserve line history, those later consumers are forced to reason over whatever state happened to survive last, which breaks the claim that they are analyzing the line that existed when the system captured it.

Point-in-time identity also makes certain debugging questions answerable at all. Without it, an engineer cannot reliably ask: "Did DraftKings move Josh Hart from 2.5 to 7.5 rebounds across fetches?" or "Was the suspicious `0.5` steals row a transient provider glitch or the only line we ever stored?" With it, those become ordinary time-series queries instead of impossible counterfactuals. That is why the concept is not just a database nicety. It is an observability contract for sportsbook truth.

There is also a clean separation-of-concerns benefit. The old coarse key forced one table to represent both *current canonical line* and *historical captures*, two jobs with incompatible semantics. Point-in-time snapshot identity lets the system keep a mutable current layer and an immutable history layer side by side. The dashboard can still ask "what is the current line?", while evaluation can ask "what settled line did we actually observe?", and the answers do not need to come from the same mutating row.

Finally, the checkpoint shows that this identity fix is the prerequisite for more trustworthy selection logic, not a substitute for it. Source priority, market classification, suspicious-line quarantine, and canonical settled-population ranking all still matter. But each of those mechanisms assumes the underlying history is real. Point-in-time snapshot identity provides that substrate.

## Key Properties

- **Identity includes time**: `fetched_at` is part of the unique key, so repeated captures at different times coexist instead of colliding.
- **Idempotent replay**: exact duplicate inserts can safely no-op via `on_conflict_do_nothing` without mutating prior evidence.
- **Immutable history layer**: snapshot rows become an append-only audit trail even when current-line tables continue to change.
- **Downstream fidelity**: backtests, calibration, and settled-population selection can reason over observed history rather than a rewritten approximation.
- **Debuggable line movement**: engineers can query when and how a line changed across captures, not just what value survived last.

## Limitations

Point-in-time identity does not recover history that was already lost under the older coarse constraint. It also assumes `fetched_at` is trustworthy and stable enough to distinguish captures correctly; if timestamps are missing, rounded too aggressively, or duplicated across semantically different rows, the protection weakens. The concept also does not decide whether a captured line is the right market, the right sportsbook truth, or a suspicious provider artifact. It preserves more evidence, but other validation layers still have to judge that evidence.

## Examples

```sql
ALTER TABLE prop_line_snapshots
DROP CONSTRAINT IF EXISTS uq_prop_line_snapshot;

CREATE UNIQUE INDEX uq_prop_line_snapshots_point
ON prop_line_snapshots (
  player_id,
  game_date,
  source,
  stat_name,
  fetched_at
);
```

```python
snapshot_key = (
    row.player_id,
    row.game_date,
    row.source,
    row.stat_name,
    row.fetched_at,
)

insert(snapshot_key).on_conflict_do_nothing()
```

## Practical Applications

This concept is useful anywhere an analytics system needs to distinguish between current state and observed historical evidence. In the [[NBA ML Engine]], it supports line-movement analysis, settled backtests, calibration joins, suspicious-line investigations, and any future attempt to explain why a prop edge looked legitimate at one moment and misleading at another. More broadly, any ingest pipeline that samples changing external state can use point-in-time identity to keep its historical record honest.

## Related Concepts

- **[[Generic Sportsbook Market Storage for Non-Canonical Props]]**: that concept first highlighted that generic sportsbook snapshots already had richer temporal identity than canonical prop snapshots.
- **[[Source-Priority Canonical Prop Ingestion]]**: source priority chooses among valid candidate rows; point-in-time identity ensures those candidates were preserved historically in the first place.
- **[[Dashboard Duplicate Predictions Fix in ML Systems]]**: both concepts care about relational grain, but snapshot identity fixes storage grain while that concept addresses join grain at query time.
- **[[Canonical Settled-Prop Backtesting for Trustworthy ML Dashboards]]**: trustworthy settled backtests depend on the snapshot table being a real history ledger rather than a mutable proxy.

## Sources

- [[Copilot Session Checkpoint: Canonical Props Implementation]] — records the 24,421-row identity failure, the new migration, and the append-only snapshot ingest rule.
- [[Copilot Session Checkpoint: Sprint Accuracy Planning]] — preserves the earlier audit that first identified the one-row-per-coarse-identity failure and framed immutable snapshot identity as the prerequisite for trustworthy downstream analytics.
