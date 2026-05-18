---
title: TorBox
type: entity
created: 2026-05-18
last_verified: 2026-05-18
source_hash: "8a9b9dbaf30c3c2d83cfc01e74948879a6d4752c3a0272b6d4dc033af9d4d84c"
sources:
  - raw/2026-05-18-copilot-session-knightcrawler-torbox-backend-865a8571.md
concepts:
  - dual-surface-provider-registration-minified-addon-bundles
related:
  - "[[KnightCrawler]]"
  - "[[Real-Debrid InstantAvailability API and Playback Issues]]"
  - "[[Copilot Session Checkpoint: Knightcrawler TorBox Backend]]"
tier: hot
tags: [torbox, debrid, streaming, knightcrawler, homelab]
---

# TorBox

## Overview

TorBox is the debrid provider added to the user's self-hosted [[KnightCrawler]] deployment during this session. In the checkpoint, it appears as a concrete integration target rather than an abstract vendor mention: the homelab stack gained a new `TORBOX_API_TOKEN` environment surface, a provider implementation in `scripts/knightcrawler/provider-src/torbox.js`, and a runtime patch that injects TorBox into the addon bundle's provider registry.

The source matters because it shows TorBox crossing the line from planned support to validated backend behavior. The patched addon exposed the short name `TB`, returned 14 TorBox-backed streams for a known movie, and resolved a selected stream with HTTP `302`. At the same time, the source captured the remaining integration gap: backend registration alone did not populate KnightCrawler's configure dropdown or API-key field, so TorBox also became the case study for why provider support in bundled apps often has to touch both runtime and UI schema surfaces.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | 2026-05-18 |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Integration Surface

The session wired TorBox through several layers of the homelab stack:

- `.env.example` gained `TORBOX_API_TOKEN` so operators know the credential surface.
- `compose/compose.stremio.yml` injects that token into `knightcrawler-addon`.
- `scripts/knightcrawler/provider-src/torbox.js` acts as the source-of-truth implementation for provider behavior.
- `scripts/knightcrawler/patches/patch-torbox-provider.js` patches `/app/dist/index.cjs` so the runtime bundle recognizes TorBox as a provider.

That last point is the most instructive one. The checkpoint explicitly notes that adding TorBox to the minified `ct` provider map was sufficient for backend stream lookup and resolve routes, but not for the configure UI. TorBox therefore represents an integration that is operationally live on the backend while still incomplete on the user-facing configuration surface.

## Operational Behavior

From the checkpoint's validation results, TorBox behaved like a working backend provider once the runtime patch was applied:

- The addon emitted a `shortName:"TB"` marker.
- Stream lookup returned 14 results for a known movie with files.
- Resolve returned an HTTP `302` response with a populated `Location` header.

Those results make TorBox more than a placeholder. In this wiki, it should be understood as an actively integrated debrid backend with a known UI-registration defect, not as an unimplemented future idea.

## Related Work

TorBox enters a stack that previously relied on Real-Debrid-specific behavior and patches such as [[Real-Debrid InstantAvailability API and Playback Issues]]. The important architectural lesson is not that TorBox replaces Real-Debrid; it is that KnightCrawler's addon customization path now has to support multiple provider-specific surfaces consistently.

