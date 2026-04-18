---
title: "Knightcrawler Metadata Service and IMDB Data Refresh"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "ffde63a096f69c53f35e3e18b31bf69c28aa146571d441566ec26bba004c63d9"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-fixing-knightcrawler-populate-cron-and-rd-playba-85f07550.md
quality_score: 0
concepts:
  - knightcrawler-metadata-service-imdb-data-refresh
related:
  - "[[Knightcrawler Populate Files Cron Job]]"
  - "[[Copilot Session Checkpoint: Fixing Knightcrawler Populate Cron and RD Playback]]"
tier: hot
tags: [knightcrawler, metadata, imdb, data-refresh, episode-mapping]
---

# Knightcrawler Metadata Service and IMDB Data Refresh

## Overview

The Knightcrawler metadata service is a one-shot process that downloads IMDB TSV data dumps and imports episode metadata into the Knightcrawler database. It truncates existing metadata tables and fully refreshes them, providing up-to-date episode mappings necessary for torrent file population and playback matching. Due to upstream IMDB data quality issues, some shows lack complete episode-to-parent mappings.

## How It Works

The metadata service downloads several IMDB TSV files, including `title.basics.tsv`, `title.akas.tsv`, and `title.episode.tsv`. It then truncates the existing metadata tables in the database and imports fresh data from these files. This process takes approximately 20 minutes.

The refreshed data updates the `imdb_metadata_episodes` table, which stores episode information such as parent_id, season, and episode numbers as text columns. This metadata is crucial for the populate files cron job to correctly map torrents to episodes.

The service is configured with restart policy 'no', meaning it runs only once on demand and does not update incrementally or automatically. Users must manually trigger it to refresh metadata when new seasons or episodes are released.

The IMDB data itself has known incompleteness: many streaming shows lack episode-to-parent mappings in the `title.episode.tsv` file, causing thousands of season packs to remain unexpandable. This is an upstream data quality issue beyond Knightcrawler's control.

The metadata refresh reduced the episode count from 9.5 million to 8.4 million and shows from 233,000 to 219,000, reflecting IMDB data cleanup.

## Key Properties

- **Data Sources:** IMDB TSV files: title.basics.tsv, title.akas.tsv, title.episode.tsv
- **Process:** Full truncation and reimport of metadata tables; non-incremental
- **Duration:** Approximately 20 minutes per run
- **Restart Policy:** Configured as 'no' restart; manual trigger required
- **Data Quality Issues:** Upstream IMDB incompleteness causes missing episode mappings for many streaming shows

## Limitations

The service does not run automatically or incrementally, requiring manual intervention to keep metadata current. It depends on IMDB's data quality, which is incomplete for many streaming shows, limiting the ability to fully populate torrent metadata. The truncation approach means any local edits or augmentations to metadata are lost on refresh.

## Example

User triggers metadata refresh:

```bash
# Manually start the knightcrawler-metadata container or service
# It downloads IMDB TSV files and imports them
# Logs show episode counts before and after refresh
```

After refresh, the populate files cron job can insert new rows for recently added episodes or shows.

## Relationship to Other Concepts

- **[[Knightcrawler Populate Files Cron Job]]** — Relies on refreshed metadata for accurate file population

## Practical Applications

Maintaining up-to-date IMDB metadata is essential for accurate torrent-to-episode mapping in Knightcrawler, enabling correct playback and metadata display in clients. Operators must schedule or manually run the metadata service after new seasons release or when metadata inconsistencies are detected.

## Sources

- [[Copilot Session Checkpoint: Fixing Knightcrawler Populate Cron and RD Playback]] — primary source for this concept
