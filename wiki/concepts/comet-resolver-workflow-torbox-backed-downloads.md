---
title: "Comet Resolver Workflow for TorBox-Backed Downloads"
type: concept
created: 2026-05-28
last_verified: 2026-05-28
source_hash: "19d1d1ddd02513bc8b25ce80e3889885005a92b153dda7f2b916e0ea4a1d408e"
sources:
  - raw/2026-05-28-copilot-session-swapping-real-debrid-for-comet-torbox-122ac146.md
quality_score: 82
related:
  - "[[Real-Debrid InstantAvailability API and Playback Issues]]"
  - "[[KnightCrawler Gating Fix for Stremio Streams]]"
tier: hot
tags: [comet, torbox, debrid, stremio, workflow, media-ingest]
---

# Comet Resolver Workflow for TorBox-Backed Downloads

## Overview

The Comet resolver workflow is a downloader integration pattern where an application queries a self-hosted Comet addon, configured inline for TorBox, and treats the returned playback proxy URLs as the primary acquisition artifact. Instead of creating debrid jobs and waiting for a provider-specific state machine to converge, the app asks Comet for already-ranked stream candidates and uses that response as both discovery and resolution data.

This matters because it removes an entire layer of orchestration from the application. In the checkpoint source, adopting this workflow is what allows [[Debrid Downloader Web]] to delete its Real-Debrid helper, simplify task transitions, and move from imperative magnet lifecycle management toward a stateless re-query model.

## How It Works

At a high level, the workflow converts a debrid download problem into a stream-resolution problem. The application no longer starts with a magnet and then asks a provider to ingest it. Instead, it starts with a media identity such as an IMDb ID plus optional season and episode numbers. That identity is sent to Comet, not as a plain request, but as part of a structured URL that also carries the debrid backend choice. In the source checkpoint the effective route is:

```text
https://comet.jbl-lab.com/s/<PUBLIC_API_TOKEN>/<base64-config>/stream/{movie|series}/{id}.json
```

The `<base64-config>` segment encodes JSON like `{"debridService":"torbox","debridApiKey":"<TORBOX key>"}`. This is a crucial design choice. The provider context is embedded in the URL itself, which means the request is stateless from the server's point of view: if the client can reconstruct the same media ID and the same config, it can reconstruct the same lookup. The workflow therefore shifts complexity from long-lived debrid session state into deterministic request construction.

The next stage is response interpretation. Comet returns stream objects designed for Stremio-style consumption, but the downloader repurposes them for a file-oriented workflow. The checkpoint notes several fields that matter: `name`, `description`, `behaviorHints`, and especially `url`. The `name` can carry cache hints such as `TB⚡` for cached streams and a different marker for uncached ones. The `description` contains parseable fragments for filename, size, and seeder count. `behaviorHints` may also expose filename and video size. Most importantly, debrid-backed streams come back with a playback proxy `url` that includes a `/playback/<40-hex-hash>/...` segment. That path shape becomes the canonical source of the torrent hash, because the same response does not reliably include an explicit `infoHash` field for the debrid-backed path.

Once the response is parsed, the workflow becomes a ranking problem rather than a job-creation problem. The checkpoint's `chooseStream()` heuristic prefers a previously selected `info_hash` if one exists, then cached candidates, then higher-quality releases, and only then a more generic fallback. That ordering matters because it preserves continuity across repeated checks. If a multi-episode series job has already chosen a specific release family, later lookups can try to stay on the same hash. If a previously uncached task is checked again later, the system can prefer the exact same candidate once it flips into a cached state. The key idea is that stream selection is idempotent enough to support re-query, even though the underlying cache status can change over time.

The real simplification appears when comparing task execution semantics. In the older Real-Debrid model, the downloader had to run a pipeline like:

1. submit magnet
2. select files
3. poll provider state
4. unrestrict final link

Each step had its own API contract and failure surface. By contrast, the Comet resolver workflow collapses the cached path to a single success case: if the returned stream is already cached, the playback URL can be treated as a ready download URL immediately. The source explicitly records that requesting the playback URL returns an HTTP `302` redirect to a TorBox CDN address, which proves that the playback proxy is not just metadata but an actionable artifact. In other words, the app no longer needs a separate "convert stream into downloadable file" phase for cached results.

Uncached results still exist, but the workflow models them differently. Instead of creating a provider-side job object and polling that object's state, the downloader stores enough context to ask the same question again later. In the checkpoint, the chosen strategy is to keep the hash as a synthetic magnet URI such as `magnet:?xt=urn:btih:<hash>` without altering the database schema. A status endpoint can parse that stored hash, re-run `cometSearch()` for the same movie or episode, and then use `chooseStream()` with `preferInfoHash` to determine whether the same result has become cached. This is still polling in a broad sense, but it is polling the resolver surface, not a provider job surface. That distinction matters operationally because the state machine is narrower and the integration boundary is unified.

The workflow also depends on deployment-aware URL construction. Because the source instance enables `CONFIGURE_PAGE_PASSWORD`, the accessible API lives under `/s/<PUBLIC_API_TOKEN>`. That makes the request path token-gated in a way that resembles other Stremio addon gating patterns already present in the wiki, such as [[KnightCrawler Gating Fix for Stremio Streams]]. The difference is that here the token prefix is not only about access control; it is part of the stable contract the downloader must know in order to build valid resolver URLs. Pinning `COMET_PUBLIC_API_TOKEN` in compose therefore becomes part of the workflow design, not just a deployment nicety.

Finally, the workflow generalizes across movies, single episodes, and multi-episode acquisitions. For a movie, the app can take the chosen playback URL directly. For a single episode, it adds season and episode to the series lookup and chooses a single stream. For a multi-episode batch, it can repeatedly query Comet per episode while preferring the same release family, using filename parsing and info-hash continuity to avoid mixing unrelated releases. The result is a downloader that still reasons about torrents, quality, and cacheability, but does so through a single resolver abstraction instead of a stack of provider-specific calls.

## Key Properties

- **Stateless request construction**: Provider choice and credential routing are encoded in the request URL via a base64 JSON config rather than held in a provider job session.
- **Resolved-artifact output**: Cached results yield a playback proxy URL that can be consumed as a download candidate immediately after a successful stream query.
- **Hash recovery from URL path**: The workflow derives `info_hash` from `/playback/<hash>/...` when debrid-backed stream payloads do not expose it directly.
- **Re-query status model**: Uncached tasks move through a lightweight `debrid` state and are checked by repeating the same resolver query instead of polling a separate provider task API.
- **Cache-first ranking**: Stream selection prefers cached and hash-consistent candidates, which reduces churn across repeated status checks and episode batches.

## Limitations

The workflow depends heavily on Comet's response conventions. If naming markers, description formatting, or playback URL shapes change, parsers such as `parseQuality`, `parseSizeBytes`, and hash extraction logic may fail or silently degrade ranking quality. It also assumes that the returned playback proxy remains a stable and valid download entrypoint; if Comet or TorBox change redirect behavior, the downloader would need a new readiness model.

It is also less general than a pure torrent pipeline. The app is no longer interacting directly with a provider's full lifecycle API, so it has less visibility into intermediate states, file-selection controls, or provider-side errors. That trade-off is acceptable in this source because the operator explicitly prefers operational simplicity over deep provider introspection.

## Examples

A simplified version of the workflow looks like this:

```python
def resolve_download(media_id, season=None, episode=None, prefer_info_hash=None):
    config = b64json({
        "debridService": "torbox",
        "debridApiKey": TORBOX_API_TOKEN,
    })
    kind = "series" if season is not None else "movie"
    suffix = f"{media_id}:{season}:{episode}" if season is not None else media_id
    url = f"{COMET_URL}/s/{PUBLIC_API_TOKEN}/{config}/stream/{kind}/{suffix}.json"

    streams = parse_comet_streams(fetch_json(url))
    chosen = choose_stream(streams, prefer_info_hash=prefer_info_hash)
    if chosen.cached:
        return {"status": "ready", "download_url": chosen.url, "info_hash": chosen.info_hash}
    return {"status": "debrid", "info_hash": chosen.info_hash}
```

In practice the downloader keeps additional metadata such as filename, size, and quality so the UI can explain what was selected and later try to match the same release again.

## Practical Applications

This pattern fits homelab downloaders that already have a self-hosted addon layer and want to minimize direct provider coupling. It is especially useful when the same operator controls Comet, the downloader, and the TorBox credential surface, because that makes token pinning and env-first configuration manageable.

It also works well when the system's real need is not "manage every debrid detail" but "turn a media identifier into a trustworthy downloadable file with minimal delay." In that setting, a resolver workflow is often more robust than a magnet lifecycle workflow, because it narrows the number of moving parts the application itself has to own.

## Related Concepts

- **[[Real-Debrid InstantAvailability API and Playback Issues]]**: The older RD-centric pattern that this workflow replaces in the downloader app.
- **[[KnightCrawler Gating Fix for Stremio Streams]]**: Another example of Stremio-style addon contracts depending on tokenized path construction and deployment-aware URL handling.

## Sources

- [[Copilot Session Checkpoint: Swapping Real-Debrid for Comet+TorBox]] — primary source for the concrete request shape, stream parsing rules, and state-model change.
