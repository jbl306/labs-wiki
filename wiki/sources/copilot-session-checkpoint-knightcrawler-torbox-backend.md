---
title: "Copilot Session Checkpoint: Knightcrawler TorBox Backend"
type: source
created: '2026-05-18'
last_verified: '2026-05-18'
source_hash: "8a9b9dbaf30c3c2d83cfc01e74948879a6d4752c3a0272b6d4dc033af9d4d84c"
sources:
  - raw/2026-05-18-copilot-session-knightcrawler-torbox-backend-865a8571.md
concepts:
  - dual-surface-provider-registration-minified-addon-bundles
  - reliable-recent-scrape-automation-media-ingestion
related:
  - "[[KnightCrawler]]"
  - "[[TorBox]]"
  - "[[KnightCrawler Addon Customization vs Operational Reliability]]"
tags: [copilot-session, checkpoint, homelab, knightcrawler, torbox, stremio, runtime-patching, automation, reliability]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 76
---

# Copilot Session Checkpoint: Knightcrawler TorBox Backend

## Summary

This checkpoint captures a homelab session that added TorBox support to the KnightCrawler Stremio addon while also hardening the recent-scrape ingestion pipeline. It records both the successful backend integration work—provider patching, stream validation, recent-scrape durability, and dashboard metrics—and the active debugging insight that the configure UI still needed a second registration path beyond the runtime provider map.

## Key Points

- **TorBox runtime integration**: The session added `TORBOX_API_TOKEN` and patched KnightCrawler's minified addon bundle so the runtime provider map `ct` includes `torbox:{key:"torbox",instance:homelabTorbox,name:"TorBox",shortName:"TB",catalog:!1}`.
- **Patch location and strategy**: The addon image was `gabisonfire/knightcrawler-addon:2.0.28`, and the customization point was `/app/dist/index.cjs`, patched at container startup through `scripts/knightcrawler/patches/apply-all.sh`.
- **Backend validation succeeded**: After deployment, the live addon exposed the `TB` marker, TorBox stream lookup returned 14 streams for a known movie, and TorBox resolve returned HTTP `302` with a `Location` header.
- **Recent-scrape importer refactor**: The session introduced shared source-adapter utilities in `kc_stream_sources.py` and refactored `kc_import_recent.py` into a multi-source importer with compatibility wrappers for older entry points.
- **Durable recent-scrape state**: `kc-scrape-recent.sh` now stores its cursor under `${KC_RECENT_STATE_DIR:-/opt/homelab/state/knightcrawler}`, defaults to a rolling 2025+ window, records runs in `automation_scrape_recent_runs`, and supports a `--sources` selector.
- **Targeted cache invalidation**: Recent-scrape runs invalidate Redis keys matching the literal pipe-delimited pattern `knightcrawler-addon|stream:${imdb_id}*`, limiting cache churn to titles affected by new imports.
- **Homepage observability**: `homepage-db-stats/app.py` was extended to expose recent-scrape fields such as `scrape_year_cutoff`, `scrape_sources`, `processed`, `no_streams`, and `errors`, and the Homepage service card labels were updated to show that health data.
- **Deployment nuance**: Worktree-based deploys initially failed because sibling relative paths did not resolve from the worktree; redeploying from canonical `main` avoided that packaging problem.
- **Root cause of the remaining UI bug**: The runtime `ct` provider map was enough for backend stream and resolve behavior, but not enough for the configure screen; the session explicitly identified that the UI likely reads a separate provider schema or dropdown list.
- **Operational status**: Local `main` already contained commit `58e812c`, `origin/main` lagged behind, and the outstanding task was to finish the UI fix before pushing to GitHub.

## Key Concepts

- [[Dual-Surface Provider Registration in Minified Addon Bundles]]
- [[Reliable Recent-Scrape Automation for Media Ingestion]]

## Related Entities

- **[[KnightCrawler]]** — The self-hosted Stremio addon and ingestion stack that received both the TorBox provider extension and recent-scrape reliability work.
- **[[TorBox]]** — The newly integrated debrid provider whose runtime support worked before its configure-page controls were fully wired.

