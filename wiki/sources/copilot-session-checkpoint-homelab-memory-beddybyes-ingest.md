---
title: "Copilot Session Checkpoint: Homelab memory optimization + BeddyByes ingest"
type: source
created: '2026-04-24'
last_verified: '2026-04-24'
source_hash: 96f3fb59664d099a456f5080ba4d80ba8e177a8b0561c0bd77500383240cb3ee
sources:
  - raw/2026-04-24-copilot-session-homelab-memory-optimization-beddybyes-ingest-9a440dbe.md
tags: [copilot-session, checkpoint, homelab, docker, memory-optimization, media-ingest, yt-dlp, knightcrawler]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 74
checkpoint_class: durable-debugging
retention_mode: retain
concepts:
  - prometheus-guided-docker-right-sizing-startup-validation
  - broadcaster-extractor-fallback-missing-torrent-titles
  - docker-container-resource-auditing-and-optimization
  - real-debrid-instantavailability-api-playback-issues
related:
  - "[[Durable Copilot Session Checkpoint]]"
  - "[[Homelab]]"
  - "[[Docker]]"
  - "[[MemPalace]]"
  - "[[Debrid-First Acquisition vs Broadcaster Extractor Fallback]]"
---

# Copilot Session Checkpoint: Homelab memory optimization + BeddyByes ingest

## Summary

This checkpoint captures a multi-track homelab operations session whose durable value is twofold: a Prometheus-informed memory right-sizing pass across the Docker fleet, and a fallback media-ingest playbook for a show that does not exist in the public torrent swarm. It also preserves the reasoning that moved the workflow from a debrid-first approach to a direct `yt-dlp` plan against broadcaster sites such as RTÉ Player and BBC iPlayer.

## Key Points

- **Host symptom was hidden memory pressure, not CPU pressure**: the server had 31 GB RAM with only 16 GB used at the moment of inspection, but Prometheus 7-day history showed swap pinned at 7.92 GB average, a 0.55 GB minimum `MemAvailable`, and a recent OOM event while CPU sat at just 9.5% average and 28.6% p95.
- **The optimization pass was driven by observed utilization rather than nominal limits**: container working-set totals averaged 7.5 GB but peaked at 17.5 GB, and Flaresolverr was called out as the only uncapped container in the set that was actively examined.
- **Right-sizing was iterative, not one-shot**: after lowering limits across multiple services, `immich-server` and `immich-machine-learning` immediately ran at roughly 89-90% startup utilization, so both were bumped back up to 768 MB instead of leaving them in a fragile state.
- **Swap reclamation was part of the remediation loop**: `swapoff -a && swapon -a` cleared 8 GB of swap usage, turning a week-long sign of memory debt into a clean baseline before observing the newly capped containers.
- **The final capped set focused on waste-heavy services**: `nba-ml-api` moved from 18 GB to 12 GB, `flaresolverr` from uncapped to 512 MB, `jellyfin` and `riven` to 768 MB, `opencode` to 1.5 GB, and both Immich services to 768 MB.
- **The session also closed out operational debris**: three stale containers were pruned, and the checkpoint records a warning to re-check for MemPalace MCP zombie-process leaks before heavy follow-on work.
- **BeddyByes was identified precisely before acquisition work**: the target show is **BeddyByes** (2025 debut, IMDB `tt37276833`), a short-form kids show with roughly 11-minute episodes and Dawn French attached in the exported notes.
- **The torrent route was exhausted before pivoting**: Knightcrawler already knew the IMDB metadata, but `torrents` and `ingested_torrents` were empty for the title, and searches through Torrentio providers, TPB/apibay, 1337x, and DuckDuckGo found no usable public swarm.
- **The raw source preserves non-obvious acquisition gotchas**: apibay's "no results" sentinel returns a fake row with an all-zero `info_hash`, and Real-Debrid cannot be used by title alone because instant availability still requires an existing hash.
- **The durable fallback is broadcaster extraction, not more torrent searching**: probe RTÉ Player first, then BBC iPlayer/CBeebies if needed, account for geo restrictions, discover the canonical Plex/Jellyfin host path with `docker inspect`, and download into a normal media library rather than Riven-managed directories.

## Key Concepts

- [[Prometheus-Guided Docker Right-Sizing with Startup Validation]]
- [[Broadcaster Extractor Fallback for Missing Torrent Titles]]
- [[Docker Container Resource Auditing and Optimization]]
- [[Real-Debrid InstantAvailability API and Playback Issues]]

## Related Entities

- **[[Homelab]]** — The operating environment where the Docker memory audit, media-library placement, and follow-on automation decisions apply.
- **[[Docker]]** — The substrate whose per-service CPU and memory limits were adjusted based on Prometheus and cAdvisor observations.
- **[[MemPalace]]** — Referenced in the checkpoint as both a knowledge-system dependency and a process-hygiene concern because zombie MCP workers had previously leaked memory.
- **[[Durable Copilot Session Checkpoint]]** — The artifact class this raw export belongs to; the page is one more curated example of that promotion workflow.
