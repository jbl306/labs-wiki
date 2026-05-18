---
title: "Dual-Surface Provider Registration in Minified Addon Bundles"
type: concept
created: 2026-05-18
last_verified: 2026-05-18
source_hash: "8a9b9dbaf30c3c2d83cfc01e74948879a6d4752c3a0272b6d4dc033af9d4d84c"
sources:
  - raw/2026-05-18-copilot-session-knightcrawler-torbox-backend-865a8571.md
related:
  - "[[KnightCrawler Gating Fix for Stremio Streams]]"
  - "[[Reliable Recent-Scrape Automation for Media Ingestion]]"
  - "[[Copilot Session Checkpoint: Knightcrawler TorBox Backend]]"
tier: hot
tags: [runtime-patching, stremio, provider-registration, minified-bundles, knightcrawler, torbox]
---

# Dual-Surface Provider Registration in Minified Addon Bundles

## Overview

Dual-surface provider registration is the pattern of adding a new backend provider to a bundled application in two places instead of one: the runtime execution surface and the configure-user-interface surface. In the KnightCrawler TorBox session, backend functionality worked as soon as the minified provider map in `/app/dist/index.cjs` knew about TorBox, but the operator still could not select TorBox or enter its API key because the configure page was driven by a separate schema or provider list.

## How It Works

The core problem appears when an application is shipped as a compiled or minified artifact instead of an easily extensible source tree. In the checkpoint, the deployed addon image was `gabisonfire/knightcrawler-addon:2.0.28`, and the active code path lived in a single bundled file, `/app/dist/index.cjs`. That means the operator could not simply drop a new plugin into a clean extension directory or register a provider through a documented configuration hook. Instead, the system had to be customized in place by patching the bundled output at container startup.

The first surface is the **runtime provider registry**. The session identified the relevant minified anchor as a block that looked like `var Dy0=2*60*1e3,jy0=15,UOe=[],ct={realdebrid:{...},premiumize:{...},alldebrid:{...},debridlink:{...},offcloud:{...},putio:{...}},VOe={};`. The important part is `ct={...}`. That object is the internal provider map the bundle consults while serving backend operations such as stream lookup and resolve. The TorBox patch inserted a `homelabTorbox` module before that anchor and then injected a `torbox:{key:"torbox",instance:homelabTorbox,name:"TorBox",shortName:"TB",catalog:!1}` entry into `ct`. Once that happened, the backend had enough information to route requests through TorBox and expose TorBox-backed streams.

The second surface is the **configure UI schema**. The session's most durable debugging insight is that runtime success is not equivalent to user-facing completeness. Stream lookup returned 14 streams and resolve returned HTTP `302`, proving that the runtime map was active. Yet the configure UI still lacked a TorBox dropdown option and API-key field. That discrepancy implies the frontend configuration page is not generated directly from the same runtime object. Instead, it likely reads from a separate provider list, form schema, or serialized settings model somewhere else in the bundle.

This is why the pattern is "dual-surface" rather than just "provider registration." A bundled application often contains at least two independent representations of a capability:

1. **Execution representation** — the internal structures the server uses while doing work.
2. **Configuration representation** — the structures the UI uses to offer choices, labels, and input fields to an operator.

When developers control the source tree, those surfaces may be generated from one canonical definition. In minified production bundles, they can drift into separate literals, helper arrays, or compiled React/Vue fragments. The TorBox case shows what happens when only one side is patched: the system works for requests that already know how to invoke the provider, but the operator cannot discover or configure the provider through the official UI.

Mechanically, the workflow is usually:

1. Copy or inspect the live bundle from the running container.
2. Search for known provider names such as `realdebrid`, `premiumize`, or `putio`.
3. Find the smallest stable anchor that identifies the runtime registry.
4. Inject a new provider module and provider-map entry.
5. Search again for provider names in strings, dropdown arrays, form schemas, or default-setting builders.
6. Patch the configure surface so the new provider appears in the dropdown and its credential field is serialized consistently.
7. Keep the patch idempotent so repeated container starts do not duplicate entries.

The idempotency requirement is especially important in this kind of startup patching. In the source, patches are applied via `scripts/knightcrawler/patches/apply-all.sh` every time the addon container starts. If the patch simply appends raw text without checking for existing markers, restarts can corrupt the bundle or create duplicate provider entries. A safe patch looks for a precise anchor, inserts a uniquely named marker such as `homelabTorbox`, and exits cleanly if the marker is already present.

Why does this work at all? Because even heavily minified bundles still preserve enough literal structure to patch deterministically. Provider keys, labels, and object shapes remain as strings because the running application needs them. The challenge is less about deobfuscation than about identifying the minimal set of literals that define behavior on both the runtime and UI surfaces.

The trade-off is maintenance cost. Every upstream addon release can reshuffle minified variable names or move the configure schema. That is why validation must cover both surfaces: backend smoke tests for stream and resolve routes, and UI smoke tests that verify the dropdown and API-key field actually render.

## Key Properties

- **Two independent registration surfaces**: Backend provider maps and configure-page schemas can diverge, so patching one does not guarantee the other.
- **Anchor-driven patching**: Reliable runtime customization depends on stable string anchors such as provider keys, object literals, or uniquely named injected markers.
- **Idempotent startup application**: Because the patch runs on container startup, it must detect prior insertion and avoid duplicating code.
- **Validation across behavior and UI**: A correct patch requires both route-level verification (`stream`, `resolve`) and configure-page verification (dropdown plus credential field).

## Limitations

This pattern is brittle against upstream releases because minified bundles are not designed as a public extension API. Even a semantically neutral upstream refactor can rename or reorder literals enough to break the patch anchor. The configure surface is also harder to patch than the runtime surface because it may be expressed through compiled UI code rather than a neat data object. Finally, operational success can mask incompleteness: backend tests may pass while the human operator still lacks a usable configuration path.

## Examples

```js
// Pseudocode for the two required patch surfaces
patch(bundle)
  .insertBefore("UOe=[],ct={", "const homelabTorbox = ...;")
  .replace(
    'ct={realdebrid:{...},premiumize:{...}}',
    'ct={realdebrid:{...},premiumize:{...},torbox:{key:"torbox",instance:homelabTorbox,name:"TorBox",shortName:"TB",catalog:!1}}'
  )
  .replace(
    'providers:["realdebrid","premiumize"]',
    'providers:["realdebrid","premiumize","torbox"]'
  );
```

In the source session, only the runtime-map portion was confirmed, which is exactly why the backend worked while the configure dropdown stayed incomplete.

## Practical Applications

This concept applies whenever a homelab operator must extend a third-party binary or bundle that lacks a supported plugin system. It is especially relevant for self-hosted addons, Electron apps, bundled Node services, and frontend-heavy appliances where provider definitions appear in both execution code and configuration UX. In practical terms, it teaches that "feature enabled" and "feature configurable" are separate milestones. The TorBox checkpoint turns that lesson into a reusable rule for future KnightCrawler customization work and complements earlier bundle-level fixes like [[KnightCrawler Gating Fix for Stremio Streams]].

## Related Concepts

- **[[KnightCrawler Gating Fix for Stremio Streams]]**: Another example of startup-time patching inside the same addon bundle, but focused on URL construction rather than provider registration.
- **[[Reliable Recent-Scrape Automation for Media Ingestion]]**: Covers the operational side of the same session, where reliability work happened outside the bundle in scripts, SQL, and metrics.

## Sources

- [[Copilot Session Checkpoint: Knightcrawler TorBox Backend]] — primary source for the distinction between runtime provider registration and configure-page registration.

