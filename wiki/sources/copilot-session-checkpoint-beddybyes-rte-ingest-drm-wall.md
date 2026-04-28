---
title: "Copilot Session Checkpoint: BeddyByes RTÉ ingest — DRM wall"
type: source
created: '2026-04-24'
last_verified: '2026-04-24'
source_hash: 0b91070796a27e3a52ea575bd23a33a2c56afbd86cdd89a5624a2c34063451fe
sources:
  - raw/2026-04-24-copilot-session-beddybyes-rt-ingest-drm-wall-179cf44c.md
tags: [copilot-session, checkpoint, homelab, media-ingest, rte-player, drm, yt-dlp, vpn]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 65
checkpoint_class: project-progress
retention_mode: compress
concepts:
  - broadcaster-extractor-fallback-missing-torrent-titles
  - anonymous-token-ip-bound-manifest-handoff
  - drm-wall-broadcaster-extraction-workflows
related:
  - "[[Durable Copilot Session Checkpoint]]"
  - "[[Homelab]]"
  - "[[Debrid-First Acquisition vs Broadcaster Extractor Fallback]]"
---

# Copilot Session Checkpoint: BeddyByes RTÉ ingest — DRM wall

## Summary

This checkpoint captures the second half of the BeddyByes acquisition attempt after the workflow had already pivoted away from torrent and debrid paths toward direct broadcaster extraction. The durable result is not a successful download but a precise technical boundary: RTÉ's catalog, geo bypass, anonymous auth, and manifest extraction all work, yet the final HLS and DASH streams are DRM-encrypted, which makes `yt-dlp` acquisition non-viable.

## Key Points

- **The fallback path progressed further than the earlier checkpoint**: the session moved from "try RTÉ Player next" to a fully working Ireland-based extraction pipeline using `gluetun-ie` and a `yt-dlp` sidecar.
- **Catalog discovery succeeded at scale**: the thePlatform feed exposed **52 English episodes** and **52 Irish-language episodes**, each with a `plmedia$publicUrl` that could be resolved into per-episode media references.
- **Geo bypass changed the failure mode cleanly**: requests initially failed with `GeoLocationBlocked`, then changed to `InvalidAuthToken` once traffic originated from the Irish VPN exit, proving region lock was solved before auth was solved.
- **Anonymous broadcaster auth was the key protocol breakthrough**: `https://www.rte.ie/servicelayer/api/anonymouslogin` returned an `mpx_token`, and the media selector accepted `auth=` or `token=` while rejecting `_token=` and `authToken=`.
- **Manifest extraction depended on network continuity**: the SMIL response produced an `.m3u8` URL containing `token1=...` and the VPN exit IP, so the request path had to stay on the same Irish egress for the stream to remain valid.
- **The technical blocker was DRM, not extractor support**: `yt-dlp` reached the manifest and then stopped with `ERROR: This video is DRM protected`, which is materially different from a broken extractor, a dead URL, or a bad token.
- **The HLS evidence is explicit**: the master playlist exposed `#EXT-X-SESSION-KEY:METHOD=SAMPLE-AES` with a FairPlay key delivery URL, while the DASH path exposed Widevine, FairPlay, and PlayReady entitlement.
- **Format probing confirmed there was no clean fallback**: `m3u` and `mpeg-dash` returned DRM-protected streams, while `m4m`, `flash`, `smil`, and `webm` variants collapsed to unavailable responses instead of clear media.
- **Operational gotchas were captured for reuse**: `gluetun` custom OpenVPN mode required the FastestVPN hostname to be pre-resolved to an IP address, which is exactly the kind of issue future homelab sessions would otherwise rediscover the hard way.
- **The checkpoint preserves a stop condition, not just a failure**: once catalog, geo, auth, and manifest retrieval all work but every media path is encrypted, the remaining options are policy decisions such as keeping the VPN tooling for future non-DRM sources, tearing it down, or switching to legal manual capture.

## Key Concepts

- [[Broadcaster Extractor Fallback for Missing Torrent Titles]]
- [[Anonymous Token to IP-Bound Manifest Handoff]]
- [[DRM Wall in Broadcaster Extraction Workflows]]

## Related Entities

- **[[Homelab]]** — The operational environment where the VPN sidecar, media-library paths, and follow-on cleanup decisions matter.
- **[[Docker]]** — The Compose substrate used to wire `gluetun-ie` and `ytdlp-ie` together as a manual-profile extraction stack.
- **[[ffmpeg]]** — Installed alongside `yt-dlp` as part of the extractor toolchain, even though the final media remained encrypted.
- **[[KnightCrawler]]** — The metadata system that knew the show existed but could not supply any torrent hashes, forcing the broadcaster pivot.
- **[[Durable Copilot Session Checkpoint]]** — The artifact type this page belongs to; the value is in preserving the learned boundary and protocol details.
