---
title: "Knightcrawler Populate Files Cron Job"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "ffde63a096f69c53f35e3e18b31bf69c28aa146571d441566ec26bba004c63d9"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-fixing-knightcrawler-populate-cron-and-rd-playba-85f07550.md
quality_score: 0
concepts:
  - knightcrawler-populate-files-cron-job
related:
  - "[[Knightcrawler Metadata Service]]"
  - "[[Real-Debrid Playback Handling]]"
  - "[[Copilot Session Checkpoint: Fixing Knightcrawler Populate Cron and RD Playback]]"
tier: hot
tags: [knightcrawler, cron-job, sql, metadata, logging]
---

# Knightcrawler Populate Files Cron Job

## Overview

The Knightcrawler populate files cron job is a scheduled task that runs every 15 minutes to populate the files table in the Knightcrawler database with metadata about torrent files. It maps ingested torrents to their corresponding video files and episode metadata, ensuring the system can correctly identify and serve media content. Proper logging and efficient SQL queries are critical for its reliable operation.

## How It Works

The cron job executes a shell script (`kc-populate-files.sh`) which runs a SQL script (`kc-populate-files.sql`) containing multiple passes that insert rows into the files table based on data from the ingested_torrents and imdb_metadata_episodes tables. The process involves:

1. Running multiple SQL passes to handle different torrent types and metadata scenarios.
2. Using unique constraints on the files table to avoid duplicate entries.
3. Logging the number of inserted rows per pass for monitoring.

Originally, the cron job used `psql -q` (quiet mode), which suppressed all output and caused the log file to remain nearly empty. This was fixed by removing quiet mode and adding timestamped logging with parsing of INSERT counts.

A new Pass 5 was added to handle episode-only torrents for single-season shows, which previously were not properly populated due to incomplete IMDB metadata. The initial correlated subquery implementation for Pass 5 was too slow (running indefinitely on 8M+ rows), so it was rewritten using a Common Table Expression (CTE) to precompute single-season shows, reducing execution time to about 35 seconds.

The cron job now reliably logs its activity, inserts new rows correctly, and handles edge cases involving incomplete or missing season metadata.

## Key Properties

- **Schedule:** Runs every 15 minutes as a cron job.
- **Logging:** Timestamped logs with per-pass INSERT counts written to ~/logs/kc-populate.log.
- **SQL Passes:** Five passes including the new Pass 5 for episode-only torrents.
- **Performance:** Optimized Pass 5 using CTE reduces query time from indefinite to ~35 seconds.
- **Database Constraints:** Files table unique constraint on (infoHash, fileIndex) ensures no duplicate file entries.

## Limitations

The cron job depends heavily on the completeness and quality of IMDB metadata. Upstream data quality issues, such as missing episode-to-parent mappings in IMDB's title.episode.tsv, cause thousands of orphan torrents to remain unpopulated. The knightcrawler-metadata service must be manually rerun to refresh metadata; it does not run incrementally or automatically. Additionally, the cron job's SQL logic assumes certain schema constraints and may require updates if the database schema changes.

## Example

Example snippet from the updated shell script logging logic:

```bash
set -euo pipefail
LOG_FILE=~/logs/kc-populate.log
{
  echo "$(date) - Starting populate"
  psql -f scripts/knightcrawler/sql/kc-populate-files.sql | tee -a $LOG_FILE
  echo "$(date) - Populate complete"
} >> $LOG_FILE 2>&1
```

Example of Pass 5 SQL (simplified):

```sql
WITH single_season_shows AS (
  SELECT imdbId
  FROM imdb_metadata_episodes
  GROUP BY imdbId
  HAVING COUNT(DISTINCT season) = 1
)
INSERT INTO files (...)
SELECT ...
FROM ingested_torrents
JOIN single_season_shows ON ...
WHERE ...;
```

## Relationship to Other Concepts

- **[[Knightcrawler Metadata Service]]** — Provides refreshed IMDB metadata that the populate cron job relies on
- **[[Real-Debrid Playback Handling]]** — The populate cron job ensures correct file metadata that supports playback resolution

## Practical Applications

Used in the Knightcrawler homelab setup to maintain an up-to-date mapping of torrent files to media episodes, enabling reliable playback in clients like Stremio. Proper operation ensures that users can stream content without errors caused by missing or incorrect file metadata. The cron job's logging and performance optimizations facilitate maintenance and troubleshooting.

## Sources

- [[Copilot Session Checkpoint: Fixing Knightcrawler Populate Cron and RD Playback]] — primary source for this concept
