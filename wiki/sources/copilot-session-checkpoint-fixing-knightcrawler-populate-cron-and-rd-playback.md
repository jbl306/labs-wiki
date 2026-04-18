---
title: "Copilot Session Checkpoint: Fixing Knightcrawler Populate Cron and RD Playback"
type: source
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "ffde63a096f69c53f35e3e18b31bf69c28aa146571d441566ec26bba004c63d9"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-fixing-knightcrawler-populate-cron-and-rd-playba-85f07550.md
quality_score: 0
concepts:
  - knightcrawler-populate-files-cron-job
  - real-debrid-instantavailability-api-playback-issues
  - knightcrawler-metadata-service-imdb-data-refresh
related:
  - "[[Knightcrawler Populate Files Cron Job]]"
  - "[[Real-Debrid InstantAvailability API and Playback Issues]]"
  - "[[Knightcrawler Metadata Service and IMDB Data Refresh]]"
  - "[[Knightcrawler]]"
  - "[[Real-Debrid]]"
tier: hot
tags: [knightcrawler, fileback, streaming, checkpoint, cron-job, copilot-session, patches, homelab, imdb, durable-knowledge, metadata, real-debrid]
---

# Copilot Session Checkpoint: Fixing Knightcrawler Populate Cron and RD Playback

## Summary

This document details a troubleshooting and enhancement session for the Knightcrawler homelab setup, focusing on fixing playback issues with Real-Debrid (RD) streams and improving the cron job that populates torrent file metadata. The session involved diagnosing RD API changes, cleaning up junk torrents, refreshing IMDB metadata, and optimizing SQL queries to handle episode-only torrents.

## Key Points

- Diagnosed Real-Debrid playback issue caused by disabled instantAvailability API and .nfo file selection bug.
- Cleaned up junk torrents and pre-cached a correct torrent for Peaky Blinders S06E04.
- Fixed silent logging in the kc-populate-files cron job by removing quiet mode and adding timestamped logs.
- Refreshed IMDB metadata by rerunning knightcrawler-metadata service to update episode data.
- Added and optimized a new SQL Pass 5 to handle episode-only torrents for single-season shows using a CTE.

## Concepts Extracted

- **[[Knightcrawler Populate Files Cron Job]]** — The Knightcrawler populate files cron job is a scheduled task that runs every 15 minutes to populate the files table in the Knightcrawler database with metadata about torrent files. It maps ingested torrents to their corresponding video files and episode metadata, ensuring the system can correctly identify and serve media content. Proper logging and efficient SQL queries are critical for its reliable operation.
- **[[Real-Debrid InstantAvailability API and Playback Issues]]** — Real-Debrid (RD) provides a torrent caching service to speed up streaming. The instantAvailability API endpoint indicates whether a torrent is cached and ready for immediate playback. Its permanent disablement breaks cache checks, causing clients like Knightcrawler to misinterpret availability and select incorrect files, resulting in playback errors such as 'torrent is being downloaded'.
- **[[Knightcrawler Metadata Service and IMDB Data Refresh]]** — The Knightcrawler metadata service is a one-shot process that downloads IMDB TSV data dumps and imports episode metadata into the Knightcrawler database. It truncates existing metadata tables and fully refreshes them, providing up-to-date episode mappings necessary for torrent file population and playback matching. Due to upstream IMDB data quality issues, some shows lack complete episode-to-parent mappings.

## Entities Mentioned

- **[[Knightcrawler]]** — Knightcrawler is a self-hosted homelab media streaming backend that integrates with Stremio and Real-Debrid to provide torrent-based streaming. It includes components such as a metadata service that imports IMDB data, a populate files cron job to map torrents to episodes, and an addon that applies patches to handle Real-Debrid API changes and file selection bugs. Knightcrawler uses a PostgreSQL database schema with tables for torrents, files, ingested torrents, and IMDB metadata.
- **[[Real-Debrid]]** — Real-Debrid is a multi-hosting torrent caching service that allows faster and more reliable streaming by caching torrents on its servers. It provides an API, including an instantAvailability endpoint to check if a torrent is cached and ready for immediate playback. The permanent disablement of this API endpoint impacts clients relying on it for cache verification, requiring workarounds and manual torrent management.

## Notable Quotes

> "RD instantAvailability API permanently disabled (error_code 37). Knightcrawler addon patch marks all streams as [RD+] since cache can't be checked." — Technical Details
> "The .nfo-at-index-0 bug causes the addon to select .nfo files instead of video files for some torrents." — Technical Details
> "IMDB title.episode.tsv incompleteness causes ~4,900 season packs to remain unexpandable due to upstream data quality issues." — Technical Details

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-fixing-knightcrawler-populate-cron-and-rd-playba-85f07550.md` |
| Type | note |
| Author | Unknown |
| Date | 2026-04-18T03:23:51.483387Z |
| URL | N/A |
