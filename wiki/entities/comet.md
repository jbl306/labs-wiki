---
title: Comet
type: entity
created: 2026-05-28
last_verified: 2026-05-28
source_hash: "19d1d1ddd02513bc8b25ce80e3889885005a92b153dda7f2b916e0ea4a1d408e"
sources:
  - raw/2026-05-28-copilot-session-swapping-real-debrid-for-comet-torbox-122ac146.md
concepts:
  - comet-resolver-workflow-torbox-backed-downloads
related:
  - "[[TorBox]]"
  - "[[Debrid Downloader Web]]"
  - "[[Homelab]]"
  - "[[KnightCrawler]]"
tier: hot
tags: [comet, torbox, stremio, debrid, homelab, media-ingest]
---

# Comet

## Overview

Comet is the self-hosted resolver layer that this checkpoint promotes into the center of the [[Debrid Downloader Web]] download path. Instead of behaving like a passive catalog source, it is used as an already-integrated decision and resolution service: the app sends a media lookup to Comet, Comet applies a TorBox-backed debrid configuration, and the response comes back with playback proxy URLs that can be treated as concrete download candidates.

In this source, Comet matters because it collapses several pieces of operational complexity that previously lived inside the application. The old Real-Debrid flow had to add a magnet, choose files, poll for readiness, and then unrestrict a final link. The Comet-based flow moves those concerns behind a single stream query and makes cache status visible through returned stream metadata such as the lightning-bolt marker and the presence of a `/playback/<hash>/...` URL.

The checkpoint also records that Comet is not just an abstract upstream project but a live homelab service with deployment-specific behavior. Because `CONFIGURE_PAGE_PASSWORD` is enabled, the usable API is prefixed with `/s/<PUBLIC_API_TOKEN>`, and the debrid provider choice is injected through a base64-encoded JSON config embedded directly in the request path. That makes Comet both a software component and a deployment contract: if the token, config encoding, or stream parsing logic changes, the whole resolver workflow changes with it.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | g0ldyy |
| URL | https://comet.jbl-lab.com |
| Status | Active |

## Resolver Model

The important thing about Comet in this checkpoint is that it returns resolved streams rather than raw acquisition instructions. A successful query produces stream objects with a user-facing `name`, a `description` that encodes filename, size, and seeders, optional `behaviorHints`, and a `url` that points at a playback proxy. For the debrid-backed streams the app cares about, the `url` includes `/playback/<40-hex-hash>/...`, which lets downstream code recover a stable info hash even when the payload does not include an explicit `infoHash` field.

That detail is what makes Comet reusable as a backend service for a downloader rather than only as a Stremio addon. The application can inspect the stream list, prefer cached entries, recover the hash, and persist the chosen playback URL as a ready-to-use artifact. In other words, Comet resolves enough state up front that the consumer no longer has to orchestrate a separate provider-specific job lifecycle.

## Integration Surface

The session identified a concrete interface that the downloader must honor:

- Base URL: `https://comet.jbl-lab.com`
- API prefix: `/s/<PUBLIC_API_TOKEN>` when configuration-page password gating is enabled
- Config payload: base64-encoded JSON including `debridService: "torbox"` and `debridApiKey: "<TORBOX key>"`
- Stream routes: `/stream/movie/{imdbId}.json` or `/stream/series/{imdbId}:{season}:{episode}.json`

This is a significant shift from the earlier RD integration. Instead of handing a magnet to a provider SDK and waiting for asynchronous readiness, the downloader now treats Comet as a stateless query interface whose URL fully captures the request context. That makes environment management and token pinning especially important, because a mismatched public token or config schema would break the resolver without any internal application fallback.

## Operational Constraints

The source records several constraints that define how Comet can be used safely in this stack:

- Only streams whose `url` contains `/playback/` should be treated as debrid-backed resolved results; P2P torrent streams must be filtered out.
- Cache state is inferred from stream naming markers such as `TB⚡` versus uncached indicators, not from a separate provider API call.
- The downloader should retain the info hash by storing it as `magnet:?xt=urn:btih:<hash>` so later status checks can look for the same stream again without a schema migration.
- The public API token should be pinned in homelab configuration to avoid invalidating existing Stremio installs or breaking stored app configuration.

Taken together, those constraints make Comet a strong fit for this homelab because it reduces API sprawl and reuse friction, but they also mean the surrounding app has to parse addon semantics carefully instead of assuming a generic torrent search response.

## Impact

Within this checkpoint, Comet is the piece that turns a debrid downloader from a job-submission client into a resolver-first client. That reduces the number of states the app has to model, aligns the workflow with the already self-hosted media stack, and gives the operator a clearer boundary between homelab infrastructure and provider behavior.
