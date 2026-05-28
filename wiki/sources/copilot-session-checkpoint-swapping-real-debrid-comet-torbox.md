---
title: "Copilot Session Checkpoint: Swapping Real-Debrid for Comet+TorBox"
type: source
created: '2026-05-28'
last_verified: '2026-05-28'
source_hash: 19d1d1ddd02513bc8b25ce80e3889885005a92b153dda7f2b916e0ea4a1d408e
sources:
  - raw/2026-05-28-copilot-session-swapping-real-debrid-for-comet-torbox-122ac146.md
concepts:
  - comet-resolver-workflow-torbox-backed-downloads
  - real-debrid-instantavailability-api-playback-issues
related:
  - "[[Comet]]"
  - "[[Debrid Downloader Web]]"
  - "[[TorBox]]"
  - "[[Real-Debrid InstantAvailability API and Playback Issues]]"
tags: [copilot-session, checkpoint, debrid-downloader-web, comet, torbox, homelab, media-ingest]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 77
---

# Copilot Session Checkpoint: Swapping Real-Debrid for Comet+TorBox

## Summary

This checkpoint captures a durable architecture shift in [[Debrid Downloader Web]]: instead of sending magnets through a multi-step [[Real-Debrid InstantAvailability API and Playback Issues]] style pipeline, the app is reworked to query self-hosted [[Comet]] with a TorBox-backed configuration and consume already-resolved playback URLs directly. The source is valuable because it records the exact runtime contract, status model, file-level implementation plan, and homelab deployment constraints needed to finish or revisit the migration later.

## Key Points

- **Architecture decision**: The chosen integration replaces the full Real-Debrid `addMagnet -> selectFiles -> poll -> unrestrict` flow with a Comet resolver path that returns ready download URLs from a TorBox-configured Stremio addon.
- **Validated live contract**: The session verified that the live Comet instance returns stream objects whose `url` field is already a playback proxy and that requesting that URL redirects with HTTP `302` to a TorBox CDN download.
- **Token-gated endpoint shape**: Because `CONFIGURE_PAGE_PASSWORD` is enabled, the usable addon base is `/s/<PUBLIC_API_TOKEN>`, so stream requests must target `https://comet.jbl-lab.com/s/<TOKEN>/<b64config>/stream/{movie|series}/{id}.json`.
- **Inline provider configuration**: The Comet request embeds a base64-encoded JSON config containing at least `{"debridService":"torbox","debridApiKey":"<TORBOX key>"}`, which makes provider selection part of the URL rather than a separate session state.
- **Stream parsing rule**: Debrid-backed Comet streams do not expose `infoHash` directly; the hash has to be extracted from `/playback/<40-hex-hash>/...` in the returned URL, while true P2P torrent streams should be skipped.
- **Selection heuristic**: The new `chooseStream()` path prefers matching `info_hash`, then cached streams, then higher-quality candidates, then a first acceptable fallback, which preserves continuity across status checks and multi-episode jobs.
- **State-model simplification**: Cached streams can become `ready` immediately because the playback URL already resolves to a concrete file, while uncached streams remain `debrid` and are re-checked by querying Comet again rather than polling a debrid API job.
- **Implementation surface**: New work was centered in `server/utils/comet.ts` and `server/utils/episode-matching.ts`, while `server/api/torrents/search.get.ts` and `server/api/downloads/index.post.ts` were rewritten and the old `server/utils/real-debrid.ts` was deleted.
- **Configuration migration**: The app's settings and env surface were shifted from `RD_API_TOKEN` toward `TORBOX_API_TOKEN`, `COMET_URL`, and `COMET_API_TOKEN`, with env-first fallback semantics and a plan to pin `COMET_PUBLIC_API_TOKEN` in homelab compose.
- **Outstanding risk at checkpoint time**: `server/api/downloads/[id]/status.get.ts`, `server/api/user.get.ts`, onboarding/settings UI, docs, compose files, and verification work still needed completion when the session compacted.

## Key Concepts

- [[Comet Resolver Workflow for TorBox-Backed Downloads]]
- [[Real-Debrid InstantAvailability API and Playback Issues]]

## Related Entities

- **[[Comet]]** — The self-hosted addon queried as the new resolver layer and the core new entity introduced by this checkpoint.
- **[[Debrid Downloader Web]]** — The application being reworked from an RD-centric acquisition model into a Comet-plus-TorBox flow.
- **[[TorBox]]** — The debrid backend injected into Comet via the encoded request config and homelab environment.
- **[[Homelab]]** — The deployment environment that already hosted the Comet instance and the TorBox credential surface.
