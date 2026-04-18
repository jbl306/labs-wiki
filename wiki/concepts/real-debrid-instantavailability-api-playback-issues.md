---
title: "Real-Debrid InstantAvailability API and Playback Issues"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "ffde63a096f69c53f35e3e18b31bf69c28aa146571d441566ec26bba004c63d9"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-fixing-knightcrawler-populate-cron-and-rd-playba-85f07550.md
quality_score: 100
concepts:
  - real-debrid-instantavailability-api-playback-issues
related:
  - "[[Copilot Session Checkpoint: Fixing Knightcrawler Populate Cron and RD Playback]]"
tier: hot
tags: [real-debrid, streaming, torrent, api, patch]
---

# Real-Debrid InstantAvailability API and Playback Issues

## Overview

Real-Debrid (RD) provides a torrent caching service to speed up streaming. The instantAvailability API endpoint indicates whether a torrent is cached and ready for immediate playback. Its permanent disablement breaks cache checks, causing clients like Knightcrawler to misinterpret availability and select incorrect files, resulting in playback errors such as 'torrent is being downloaded'.

## How It Works

Originally, Knightcrawler's addon queried RD's instantAvailability API to verify if a torrent was cached and instantly playable. When the API was disabled (error_code 37), the addon could no longer confirm cache status. To work around this, a patch (`patch-rd-availability.js`) was applied that marks all streams as '[RD+]', assuming availability.

However, this causes a problem: if a torrent is not cached, clicking it triggers RD to start downloading it, leading to a 'torrent is being downloaded' message in Stremio instead of immediate playback.

Additionally, many torrents have an .nfo file at fileIndex 0 and the actual video file at a higher index. Knightcrawler's database stores fileIndex=0 for single-file torrents, causing the addon to select the .nfo file mistakenly. A patch (`patch-rd-episode-match.js`) attempts to fix this by matching filenames with regex instead of relying on fileIndex.

The user cleaned up junk .nfo torrents and pre-cached a correct video torrent for Peaky Blinders S06E04, confirming the video file at file ID 2, avoiding the .nfo bug.

The combination of the disabled API and .nfo file indexing bug explains the playback failures observed.

## Key Properties

- **API Status:** RD instantAvailability API permanently disabled, returning error_code 37.
- **Addon Patch:** Marks all RD streams as cached ([RD+]) to bypass API unavailability.
- **.nfo File Bug:** Many torrents have .nfo files at index 0, causing incorrect file selection.
- **Playback Error:** 'Torrent is being downloaded' message occurs when a non-cached torrent is selected.

## Limitations

The patch marking all streams as cached is a workaround that can cause user confusion and playback delays. The .nfo file bug is a structural issue in how torrents are indexed and requires filename-based matching to mitigate, which may not be perfect. The upstream RD API disablement is outside user control and forces reliance on imperfect patches and manual torrent management.

## Example

Example of patch behavior:

- RD API call to instantAvailability fails with error_code 37.
- Addon marks all streams as '[RD+]'.
- User clicks on a torrent link.
- If torrent is not cached, RD starts downloading it.
- Stremio shows 'torrent is being downloaded' instead of playing.

Manual fix:
- Delete junk .nfo torrents.
- Add magnet link for a known good torrent.
- Confirm it is cached and video file is at correct file index.

## Relationship to Other Concepts

- **Knightcrawler Addon Patches** — Contain fixes for RD API disablement and file selection bugs

## Practical Applications

Understanding this issue is critical for maintaining smooth streaming experiences in setups using Real-Debrid with Knightcrawler and Stremio. Operators must manage torrents actively, apply patches, and pre-cache correct torrents to avoid playback errors caused by RD API changes and torrent file structure quirks.

## Sources

- [[Copilot Session Checkpoint: Fixing Knightcrawler Populate Cron and RD Playback]] — primary source for this concept
