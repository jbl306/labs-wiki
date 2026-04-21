---
title: "Copilot Session Checkpoint: Fixing Knightcrawler Populate Cron and RD Playback"
type: source
created: 2026-04-12
last_verified: 2026-04-21
source_hash: "ffde63a096f69c53f35e3e18b31bf69c28aa146571d441566ec26bba004c63d9"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-fixing-knightcrawler-populate-cron-and-rd-playba-85f07550.md
quality_score: 100
concepts:
  - knightcrawler-populate-files-cron-job
  - real-debrid-instantavailability-api-playback-issues
  - knightcrawler-metadata-service-imdb-data-refresh
related:
  - "[[Knightcrawler Populate Files Cron Job]]"
  - "[[Real-Debrid InstantAvailability API and Playback Issues]]"
  - "[[Knightcrawler Metadata Service and IMDB Data Refresh]]"
  - "[[Knightcrawler]]"
  - "[[Homelab]]"
tier: hot
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, knightcrawler, streaming, cron-job, patches, imdb, metadata, real-debrid]
checkpoint_class: durable-workflow
retention_mode: retain
knowledge_state: validated
---

# Copilot Session Checkpoint: Fixing Knightcrawler Populate Cron and RD Playback

## Summary

The user reported two issues with their self-hosted Stremio/Knightcrawler homelab setup: (1) Peaky Blinders S06E04 not playing via Real-Debrid, showing "torrent is being downloaded", and (2) the kc-populate-files cron job not writing to its log file. I diagnosed both issues through container logs, database queries, and RD API inspection, then fixed the logging, added a new SQL pass for episode-only torrents, and refreshed the IMDB metadata.

## Key Points

- Diagnosed S06E04 playback issue (RD instantAvailability disabled + .nfo file selection)
- Cleaned up junk RD torrents
- Pre-cached good S06E04 torrent on RD
- Fixed populate cron logging (was silent due to psql -q)
- Refreshed IMDB metadata (knightcrawler-metadata re-run)
- Added Pass 5 SQL for episode-only torrents

## Execution Snapshot

**Files updated:**
- `scripts/knightcrawler/automation/kc-populate-files.sh`: Rewrote with proper bash conventions (set -euo pipefail, BASH_SOURCE), replaced `psql -q` with verbose mode, added timestamped logging with per-pass INSERT count parsing
- `scripts/knightcrawler/sql/kc-populate-files.sql`: Added Pass 5 (episode-only torrents for single-season shows using CTE), updated header comments

**Database actions:**
- Re-ran `knightcrawler-metadata` to refresh imdb_metadata_episodes from latest IMDB dump
- Populated 1,474 new rows in files table (72 from metadata refresh + 1,402 from Pass 5)

**RD account cleanup:**
- Deleted 5 junk .nfo torrents and 1 errored torrent from Real-Debrid
- Pre-cached Peaky.Blinders.S06.E04.Sapphire.REPACK.2160p (18.1GB) on RD

**Work completed:**
- [x] Diagnosed S06E04 playback issue (RD instantAvailability disabled + .nfo file selection)
- [x] Cleaned up junk RD torrents
- [x] Pre-cached good S06E04 torrent on RD
- [x] Fixed populate cron logging (was silent due to psql -q)
- [x] Refreshed IMDB metadata (knightcrawler-metadata re-run)
- [x] Added Pass 5 SQL for episode-only torrents
- [x] Optimized Pass 5 from timeout → 35s using CTE
- [x] Committed all changes (84e9d8f on main)

**Current state:**
- Populate cron runs every 15min, now logs timestamps and row counts to ~/logs/kc-populate.log
- ~11,000 orphan torrents remain but most are blocked by IMDB data quality issues (upstream, not fixable)
- Changes committed but NOT pushed to GitHub or deployed

## Technical Details

- **RD instantAvailability API permanently disabled** (error_code 37). Knightcrawler addon patch marks all streams as [RD+] since cache can't be checked. This means clicking a non-cached torrent triggers RD download → "torrent is being downloaded" in Stremio.
- **fileIndex 0 = .nfo bug**: Many REPACK/RH torrents have an .nfo file at index 0 and the .mkv at index 1+. Knightcrawler's DB stores fileIndex=0 for single-file torrents, which picks the .nfo. The episode-match patch (`patch-rd-episode-match.js`) tries to fix this by matching filenames instead.
- **knightcrawler-metadata** is a one-shot service (restart: "no") that downloads IMDB TSV dumps and imports them. It TRUNCATES all metadata tables first, so it's a full refresh not incremental. Takes ~20 minutes. Must be manually re-run for new seasons.
- **IMDB title.episode.tsv incompleteness**: Many streaming shows (From, Kindred, The Morning Show, etc.) have no episode-to-parent mappings in IMDB's data dump. This is an upstream data quality issue — ~4,900 season packs can't be expanded.
- **Pass 5 performance**: Correlated `count(DISTINCT season)` subquery against 8M+ imdb_metadata_episodes rows takes forever. CTE pre-computing single-season shows runs in ~35s.
- **Knightcrawler addon patches** are applied at container start via `scripts/knightcrawler/patches/apply-all.sh`. They modify `/app/dist/index.cjs` (minified bundle). Patches are applied in order, some depend on others.
- **Knightcrawler DB schema**: `torrents` (PK: infoHash), `files` (FK to torrents via infoHash, unique on infoHash+fileIndex), `ingested_torrents` (has rtn_response JSONB with parsed season/episode arrays), `imdb_metadata_episodes` (parent_id, season, episode — all text columns).
- **files table unique constraint**: `("infoHash", "fileIndex", "imdbId", "imdbSeason", "imdbEpisode", "kitsuId", "kitsuEpisode")` but also `("infoHash", "fileIndex")` — the latter is what ON CONFLICT uses.

## Important Files

- `scripts/knightcrawler/automation/kc-populate-files.sh`
- Cron job entry point, runs every 15min
- Rewrote: proper bash conventions, timestamped logging, INSERT count parsing
- Full file, ~40 lines

- `scripts/knightcrawler/sql/kc-populate-files.sql`
- SQL executed by the populate cron — 5 passes mapping ingested_torrents → files
- Added Pass 5 (lines 82-106): CTE-based episode-only torrent handling
- Full file, ~106 lines

- `compose/compose.stremio.yml`
- Knightcrawler stack definition: postgres, redis, lavinmq, migrator, metadata, addon, producer, consumer, debridcollector (disabled)
- knightcrawler-metadata: restart "no", one-shot IMDB import
- knightcrawler-addon: custom patches via entrypoint, port 7000

- `scripts/knightcrawler/patches/apply-all.sh`
- Orchestrates 9 addon patches in order at container start
- Key patches: rd-availability, rd-resolve, rd-episode-match, rd-select-all

- `scripts/knightcrawler/patches/patch-rd-episode-match.js`
- Fixes season pack episode matching by filename regex instead of fileIndex+1
- 3 sub-patches: _createOrFindTorrentId, _selectTorrentFiles, _unrestrictLink

- `scripts/knightcrawler/patches/patch-rd-availability.js`
- Works around disabled RD instantAvailability API
- Marks all streams as cached when API unavailable

- `config/knightcrawler/stack.env`
- Knightcrawler environment config, references RD_API_TOKEN from root .env

## Next Steps

**Remaining work:**
- Changes committed locally (84e9d8f) but NOT pushed to GitHub or deployed to server
- User should push and deploy when ready: `git push && ./scripts/ops/deploy.sh stremio`
- User should verify S06E04 now plays via the HONE season pack or the pre-cached individual torrent

No immediate action items unless user requests further work. The ~11,000 remaining orphan torrents are blocked by IMDB data quality (upstream issue, not fixable).

## Related Wiki Pages

- [[Knightcrawler Populate Files Cron Job]]
- [[Real-Debrid InstantAvailability API and Playback Issues]]
- [[Knightcrawler Metadata Service and IMDB Data Refresh]]
- [[Knightcrawler]]
- [[Homelab]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-fixing-knightcrawler-populate-cron-and-rd-playba-85f07550.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-04-12 |
| URL | N/A |
