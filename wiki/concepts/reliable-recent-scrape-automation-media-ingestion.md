---
title: "Reliable Recent-Scrape Automation for Media Ingestion"
type: concept
created: 2026-05-18
last_verified: 2026-05-18
source_hash: "8a9b9dbaf30c3c2d83cfc01e74948879a6d4752c3a0272b6d4dc033af9d4d84c"
sources:
  - raw/2026-05-18-copilot-session-knightcrawler-torbox-backend-865a8571.md
related:
  - "[[Knightcrawler Cron Automation Monitoring and Status Tracking]]"
  - "[[Dual-Surface Provider Registration in Minified Addon Bundles]]"
  - "[[Copilot Session Checkpoint: Knightcrawler TorBox Backend]]"
tier: hot
tags: [automation, reliability, media-ingestion, knightcrawler, cron, cache-invalidation, observability]
---

# Reliable Recent-Scrape Automation for Media Ingestion

## Overview

Reliable recent-scrape automation is the pattern of treating "scrape the newest titles" as a durable, stateful ingestion system instead of a best-effort cron job. In the KnightCrawler TorBox session, that meant refactoring recent-title import logic into reusable source adapters, persisting scrape progress under a dedicated state directory, classifying outcomes in a database table, and exposing those results through Homepage metrics instead of relying on ad hoc operator checks.

## How It Works

The source shows a transition from a narrow scraper toward an operational pipeline. Earlier KnightCrawler work already had cron-driven automation, but this session made the recent-scrape path more robust in several specific ways. The first change was architectural: recent scraping stopped being implicitly tied to one upstream parser and was refactored into a multi-source ingestion flow. The new `scripts/knightcrawler/automation/kc_stream_sources.py` file centralizes parsing, sizing, seeder handling, and deduplication logic for upstream stream sources, while `kc_import_recent.py` becomes the shared importer that consumes those normalized source adapters.

That separation matters because recent-title ingestion tends to fail at the edges, not in the happy path. Different upstreams expose different metadata completeness, naming conventions, file sizes, and seeder signals. If source-specific logic lives inline inside one monolithic cron script, every new upstream or bug fix turns into a risky edit to the scheduler path itself. By moving those concerns into adapter utilities, the session made the ingestion core more deterministic: the scheduler chooses sources, the adapters normalize records, and the importer makes import decisions on a uniform shape.

The second reliability layer is **durable progress state**. The checkpoint notes that `kc-scrape-recent.sh` now stores its cursor under `${KC_RECENT_STATE_DIR:-/opt/homelab/state/knightcrawler}`. That change is subtle but important. A recent-scrape job works over a moving frontier of titles, often keyed by year windows or upstream offsets. If the offset only lives in a temp file or container-local ephemeral location, restarts or deployments can force the job to replay large windows, skip ahead incorrectly, or lose track of coverage. A dedicated state directory turns progress into durable operator-owned state.

The third layer is **bounded scope**. The script defaults to a rolling 2025+ window and adds a `--sources` selector. Both decisions improve reliability because they make the job explicit about what it is responsible for. Instead of attempting to scrape the entire catalog every run, it focuses on the part of the dataset most likely to change. Instead of hardcoding one upstream forever, the scheduler can say which source set it should evaluate. Those boundaries keep runtime predictable and make failures more diagnosable.

The fourth layer is **run accounting**. The migration `scripts/knightcrawler/sql/kc-scrape-status.sql` creates `automation_scrape_recent_runs`, and the cron script records each run there. This extends prior KnightCrawler monitoring work from coarse job status into run-level history. A single "last success" timestamp tells you whether something ran; a run table tells you what the job actually did. That distinction matters when a scrape exits zero but imports nothing, or when one source produces many `no_streams` classifications while another produces actual imports.

The fifth layer is **targeted invalidation**. After new recent imports, the pipeline invalidates Redis keys matching `knightcrawler-addon|stream:${imdb_id}*`. That is a reliability improvement because stale cache is one of the easiest ways for an otherwise correct ingestion run to look broken. If the cache survives after new streams are imported, operators and end users still see old "no streams" behavior. But the invalidation is intentionally narrow: it touches the literal pipe-delimited key namespace only for the affected IMDb ID. That preserves cache usefulness for unrelated titles while ensuring newly ingested results become visible promptly.

The sixth layer is **observability at the operator surface**. The checkpoint added recent-scrape fields such as `scrape_year_cutoff`, `scrape_sources`, `processed`, `no_streams`, and `errors` to `homepage-db-stats/app.py`, and updated Homepage labels to display those metrics. This is the difference between a pipeline that merely runs and a pipeline that can be operated. Once those counters are surfaced in the dashboard, the operator can tell whether the scraper is healthy, whether the selected source set changed, and whether the current bottleneck is upstream coverage, episode metadata completeness, or hard errors.

This reliability pattern also preserves compatibility while evolving the internals. The source notes two wrapper entry points, `kc-import-recent.py` and `kc-import-torrentio.py`, that continue to exist around the refactored importer. That is an operationally conservative move: external cron entries or scripts can continue calling old names while the implementation underneath becomes more modular. Reliability is not only about error handling; it is also about safe migration of entry points that other automation already depends on.

The deeper intuition is that recent scraping is a feedback loop, not a one-shot fetch. It touches upstream availability, local metadata coverage, cache freshness, dashboard interpretation, and operator confidence. The session improved each of those interfaces so the job could keep running across deploys, partial data, and evolving source mixes.

## Key Properties

- **Adapter-based normalization**: Source-specific parsing is separated from import decisions, making multi-source scraping extensible and testable.
- **Persistent cursor state**: Progress survives restarts through `${KC_RECENT_STATE_DIR}`, reducing replay and drift.
- **Run-level observability**: `automation_scrape_recent_runs` captures more than success/failure, enabling throughput and outcome analysis.
- **Narrow cache invalidation**: Only affected `knightcrawler-addon|stream:${imdb_id}*` keys are flushed, balancing freshness with cache efficiency.
- **Operator-visible metrics**: Homepage can show the year cutoff, source set, processed count, and error classes directly.

## Limitations

This pattern still depends on upstream content availability and local metadata completeness. The checkpoint explicitly notes that some validation targets lacked `imdb_metadata_episodes`, which means a series can be "recent" without being fully resolvable. Targeted invalidation also depends on cache-key conventions staying stable; if the key separator or prefix changes, invalidation quietly misses the intended entries. Finally, a rolling year window is an intentional bias toward freshness, so titles outside that window require separate backfill workflows.

## Examples

```bash
# Representative recent-scrape flow
KC_RECENT_STATE_DIR=/opt/homelab/state/knightcrawler \
kc-scrape-recent.sh --sources torrentio

# Resulting run metadata exposed through homepage-db-stats
scrape_year_cutoff=2025
scrape_sources=torrentio
processed=1
no_streams=1
errors=0
```

In the session, that shape of output was important because it made the job's health legible even when a chosen validation title produced no playable episode result.

## Practical Applications

This concept generalizes to any media-ingestion or catalog-refresh job that operates over a fast-moving recent subset rather than a static full dataset. Homelab operators can apply the same pattern to subtitle fetchers, artwork refreshers, sports schedule imports, or any cron-fed enrichment pipeline: normalize upstreams, persist cursors, classify outcomes, invalidate only the affected cache keys, and expose the resulting state through a dashboard. Within KnightCrawler specifically, it complements the addon-side TorBox patching work by ensuring that newly available streams actually make it from upstream source to visible addon result reliably.

## Related Concepts

- **[[Knightcrawler Cron Automation Monitoring and Status Tracking]]**: Earlier KnightCrawler work established database-backed automation visibility; this concept extends that mindset to recent-title ingestion and run-level freshness.
- **[[Dual-Surface Provider Registration in Minified Addon Bundles]]**: Covers the bundle-level customization side of the same session, where the challenge lived inside the addon rather than in cron orchestration.

## Sources

- [[Copilot Session Checkpoint: Knightcrawler TorBox Backend]] — primary source for the recent-scrape refactor, durable state, invalidation, and metrics details.

