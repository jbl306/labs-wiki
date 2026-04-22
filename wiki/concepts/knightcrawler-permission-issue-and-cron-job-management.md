---
title: "KnightCrawler Permission Issue and Cron Job Management"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "94a3f24d84af863c5b7181b6b3955f897bb5554330e966d2f452d23543e6b2f4"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-homelab-monitoring-and-knightcrawler-fixes-a62133b0.md
quality_score: 67
concepts:
  - knightcrawler-permission-issue-and-cron-job-management
related:
  - "[[Knightcrawler Populate Files Cron Job]]"
  - "[[Knightcrawler Metadata Service and IMDB Data Refresh]]"
  - "[[Copilot Session Checkpoint: Homelab Monitoring and KnightCrawler Fixes]]"
tier: hot
tags: [cron, permissions, media-ingestion, docker, knightcrawler]
---

# KnightCrawler Permission Issue and Cron Job Management

## Overview

KnightCrawler is a media ingestion pipeline that scrapes and populates IMDB titles into a database. Proper execution permissions on its cron-triggered scripts are critical for timely data updates. This concept covers diagnosing permission-related failures in cron jobs, understanding the pipeline structure, and best practices for maintaining reliable scheduled tasks.

## How It Works

KnightCrawler operates through a pipeline involving multiple Docker containers and cron jobs. Two main cron scripts are involved: `kc-populate-files.sh`, which runs every 15 minutes to map torrents to files in the database, and `kc-scrape-recent.sh`, which runs every 6 hours to scrape recent IMDB titles. The `kc-populate-files.sh` script executes a 4-pass SQL process targeting different media types (movies, series episodes, single-season packs, multi-season packs) by copying SQL files into the container and running them with `psql -f`. 

A critical failure mode occurs when the script lacks execute permission (e.g., mode 644 instead of 755), causing repeated 'Permission denied' errors logged every 15 minutes. This leads to significant data coverage gaps, especially for recent years (e.g., 2025 and 2026 titles). Diagnosing this requires inspecting container health, cron job logs, and file system permissions. Fixing involves restoring execute permissions with `chmod +x` and verifying manual script execution. 

The pipeline's data coverage depends on upstream sources like DMM hashlists and Torrentio availability, so low coverage for future years is expected until upstream data matures. Maintaining cron job health requires monitoring logs, permissions, and container status regularly. Adding troubleshooting documentation and lessons learned helps prevent recurrence.

## Key Properties

- **Cron Job Frequency:** `kc-populate-files.sh` runs every 15 minutes; `kc-scrape-recent.sh` runs every 6 hours.
- **File Permissions:** Scripts must have execute permission (mode 755) to run under cron; missing this causes silent repeated failures.
- **Pipeline SQL Passes:** Four SQL passes target different media categories for comprehensive file population.
- **Data Coverage:** Dependent on upstream torrent availability; recent years may have low coverage until data propagates.

## Limitations

Permission issues can cause silent repeated failures without immediate alerts. The pipeline's effectiveness is limited by upstream data availability. Cron jobs running inside containers require careful permission and environment management to avoid execution failures. Manual intervention may be needed to restore functionality after permission changes.

## Example

To fix the permission issue:
```bash
chmod +x scripts/knightcrawler/automation/kc-populate-files.sh
# Run manually to verify
./scripts/knightcrawler/automation/kc-populate-files.sh
```
Then monitor logs to confirm successful execution and data population.

## Relationship to Other Concepts

- **[[Knightcrawler Populate Files Cron Job]]** — Specific cron job involved in the permission issue
- **[[Knightcrawler Metadata Service and IMDB Data Refresh]]** — Related service for metadata ingestion and data updates

## Practical Applications

Ensuring reliable media ingestion pipelines for home media servers or streaming addons that rely on timely and accurate metadata updates. Preventing silent failures in scheduled tasks by enforcing strict permission and monitoring policies. Documenting operational lessons to improve maintenance and troubleshooting efficiency.

## Sources

- [[Copilot Session Checkpoint: Homelab Monitoring and KnightCrawler Fixes]] — primary source for this concept
