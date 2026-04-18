---
title: "Copilot Session Checkpoint: Fixing Knightcrawler populate cron and RD playback"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab]
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Fixing Knightcrawler populate cron and RD playback
**Session ID:** `2e3d0a8c-0302-474f-a269-e28a5a23b123`
**Checkpoint file:** `/home/jbl/.copilot/session-state/2e3d0a8c-0302-474f-a269-e28a5a23b123/checkpoints/001-fixing-knightcrawler-populate.md`
**Checkpoint timestamp:** 2026-04-12T18:53:43.051253Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user reported two issues with their self-hosted Stremio/Knightcrawler homelab setup: (1) Peaky Blinders S06E04 not playing via Real-Debrid, showing "torrent is being downloaded", and (2) the kc-populate-files cron job not writing to its log file. I diagnosed both issues through container logs, database queries, and RD API inspection, then fixed the logging, added a new SQL pass for episode-only torrents, and refreshed the IMDB metadata.
</overview>

<history>
1. User reported Peaky Blinders S06E04 not playing in Stremio via Knightcrawler, getting "torrent is being downloaded"
   - Verified all knightcrawler and riven containers were healthy (up 2 weeks)
   - Checked addon logs: found hashes `496616d` (S06E05) and `3954c40` (S06E06) being tried — wrong episodes
   - Discovered RD's `instantAvailability` endpoint is disabled (error_code 37), so cache checks fail
   - The addon has a patch (`patch-rd-availability.js`) that marks all streams as `[RD+]` since cache can't be checked
   - Found the unrestricted links resolved to .nfo files (103 bytes) instead of video files — fileIndex 0 was the .nfo
   - Confirmed the HONE season pack (hash `8a1821...`) IS fully downloaded on RD with E04 at file ID 4 (7.2GB)
   - Advised user to use the HONE season pack stream which is cached and correct

2. User agreed to clean up junk RD torrents and pre-cache a good S06E04 torrent
   - Deleted 5 .nfo junk torrents (90-107 bytes each) across S03, S05, S06
   - Deleted 1 errored S06E05 torrent
   - Added magnet for `37e1d97c...` (Peaky.Blinders.S06.E04.Sapphire.REPACK.2160p.UPSCALE.BluRay) to RD
   - Confirmed it was instantly available: 18.1GB, status "downloaded"
   - Noted the video is at file ID 2 (not 0), so the .nfo-at-index-0 bug could still affect it

3. User asked about kc-populate-files cron — why isn't the log writing, and is it fully populated?
   - Found cron IS running every 15 minutes (verified via journalctl)
   - Log file was 42 bytes with only "Permission fixed, populate cron restored" from Apr 5
   - Root cause of empty log: script uses `psql -q` (quiet mode) which suppresses all output
   - Ran populate manually without -q: all 4 passes returned `INSERT 0 0`
   - Investigated why: 65,980 orphaned torrents total, 12,489 with IMDB data but no files
   - Breakdown: 4,906 single season packs (missing episode metadata), 4,539 no season/no episode, 2,973 episode-only no season, 71 multi-season packs
   - Root cause: `knightcrawler-metadata` service ran once at initial setup and never again — `imdb_metadata_episodes` was stale/incomplete for newer seasons

4. User agreed to fix logging, re-run metadata service, and add Pass 5
   - Started `knightcrawler-metadata` refresh — it truncates and reimports all IMDB data (~20 min)
   - Metadata service downloaded title.basics.tsv, title.akas.tsv, title.episode.tsv from IMDB
   - Episode count went from 9.5M to 8.4M (IMDB data cleanup), shows from 233K to 219K
   - Updated shell script: replaced `psql -q` with verbose output, added timestamped logging with per-pass row counts
   - Added Pass 5 to SQL: handles episode-only torrents (no season) for single-season shows using CTE
   - Initial Pass 5 implementation used correlated subquery — ran forever against 8M rows
   - Killed slow queries, rewrote Pass 5 with CTE pre-computing single-season shows — 35s execution
   - Final run results: Pass 3/4 inserted 72 rows (from metadata refresh), Pass 5 inserted 1,402 rows
   - Total: 1,474 new file rows. Files table went from 1,399,351 → 1,400,825
   - Verified logging works: "No new rows to insert" on subsequent run
   - Remaining gaps: 4,904 season packs (IMDB missing data), 1,571 multi-season episode-only, 4,539 unparseable
   - Committed changes to main branch (commit 84e9d8f)
</history>

<work_done>
Files updated:
- `scripts/knightcrawler/automation/kc-populate-files.sh`: Rewrote with proper bash conventions (set -euo pipefail, BASH_SOURCE), replaced `psql -q` with verbose mode, added timestamped logging with per-pass INSERT count parsing
- `scripts/knightcrawler/sql/kc-populate-files.sql`: Added Pass 5 (episode-only torrents for single-season shows using CTE), updated header comments

Database actions:
- Re-ran `knightcrawler-metadata` to refresh imdb_metadata_episodes from latest IMDB dump
- Populated 1,474 new rows in files table (72 from metadata refresh + 1,402 from Pass 5)

RD account cleanup:
- Deleted 5 junk .nfo torrents and 1 errored torrent from Real-Debrid
- Pre-cached Peaky.Blinders.S06.E04.Sapphire.REPACK.2160p (18.1GB) on RD

Work completed:
- [x] Diagnosed S06E04 playback issue (RD instantAvailability disabled + .nfo file selection)
- [x] Cleaned up junk RD torrents
- [x] Pre-cached good S06E04 torrent on RD
- [x] Fixed populate cron logging (was silent due to psql -q)
- [x] Refreshed IMDB metadata (knightcrawler-metadata re-run)
- [x] Added Pass 5 SQL for episode-only torrents
- [x] Optimized Pass 5 from timeout → 35s using CTE
- [x] Committed all changes (84e9d8f on main)

Current state:
- Populate cron runs every 15min, now logs timestamps and row counts to ~/logs/kc-populate.log
- ~11,000 orphan torrents remain but most are blocked by IMDB data quality issues (upstream, not fixable)
- Changes committed but NOT pushed to GitHub or deployed
</work_done>

<technical_details>
- **RD instantAvailability API permanently disabled** (error_code 37). Knightcrawler addon patch marks all streams as [RD+] since cache can't be checked. This means clicking a non-cached torrent triggers RD download → "torrent is being downloaded" in Stremio.
- **fileIndex 0 = .nfo bug**: Many REPACK/RH torrents have an .nfo file at index 0 and the .mkv at index 1+. Knightcrawler's DB stores fileIndex=0 for single-file torrents, which picks the .nfo. The episode-match patch (`patch-rd-episode-match.js`) tries to fix this by matching filenames instead.
- **knightcrawler-metadata** is a one-shot service (restart: "no") that downloads IMDB TSV dumps and imports them. It TRUNCATES all metadata tables first, so it's a full refresh not incremental. Takes ~20 minutes. Must be manually re-run for new seasons.
- **IMDB title.episode.tsv incompleteness**: Many streaming shows (From, Kindred, The Morning Show, etc.) have no episode-to-parent mappings in IMDB's data dump. This is an upstream data quality issue — ~4,900 season packs can't be expanded.
- **Pass 5 performance**: Correlated `count(DISTINCT season)` subquery against 8M+ imdb_metadata_episodes rows takes forever. CTE pre-computing single-season shows runs in ~35s.
- **Knightcrawler addon patches** are applied at container start via `scripts/knightcrawler/patches/apply-all.sh`. They modify `/app/dist/index.cjs` (minified bundle). Patches are applied in order, some depend on others.
- **Knightcrawler DB schema**: `torrents` (PK: infoHash), `files` (FK to torrents via infoHash, unique on infoHash+fileIndex), `ingested_torrents` (has rtn_response JSONB with parsed season/episode arrays), `imdb_metadata_episodes` (parent_id, season, episode — all text columns).
- **files table unique constraint**: `("infoHash", "fileIndex", "imdbId", "imdbSeason", "imdbEpisode", "kitsuId", "kitsuEpisode")` but also `("infoHash", "fileIndex")` — the latter is what ON CONFLICT uses.
</technical_details>

<important_files>
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
</important_files>

<next_steps>
Remaining work:
- Changes committed locally (84e9d8f) but NOT pushed to GitHub or deployed to server
- User should push and deploy when ready: `git push && ./scripts/ops/deploy.sh stremio`
- User should verify S06E04 now plays via the HONE season pack or the pre-cached individual torrent

No immediate action items unless user requests further work. The ~11,000 remaining orphan torrents are blocked by IMDB data quality (upstream issue, not fixable).
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
