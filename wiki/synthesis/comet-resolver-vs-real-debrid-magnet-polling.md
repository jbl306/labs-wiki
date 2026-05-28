---
title: "Comet Resolver Workflow vs Real-Debrid Magnet Polling"
type: synthesis
created: '2026-05-28'
last_verified: '2026-05-28'
source_hash: "synthesis-generated"
sources:
  - raw/2026-05-28-copilot-session-swapping-real-debrid-for-comet-torbox-122ac146.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-fixing-knightcrawler-populate-cron-and-rd-playba-85f07550.md
concepts:
  - comet-resolver-workflow-torbox-backed-downloads
  - real-debrid-instantavailability-api-playback-issues
related:
  - "[[Comet Resolver Workflow for TorBox-Backed Downloads]]"
  - "[[Real-Debrid InstantAvailability API and Playback Issues]]"
  - "[[Comet]]"
  - "[[Debrid Downloader Web]]"
tier: hot
tags: [comet, real-debrid, debrid, workflow, homelab, media-ingest]
quality_score: 83
---

# Comet Resolver Workflow vs Real-Debrid Magnet Polling

## Question

For a homelab downloader that needs a stable path from media IDs to usable files, is it better to resolve through a Comet-plus-TorBox stream surface or to keep driving a Real-Debrid-style magnet job pipeline?

## Summary

The Comet resolver workflow is better when the operator already controls a self-hosted addon that can return playable, debrid-backed URLs directly, because it collapses discovery, ranking, and readiness into one query surface. Real-Debrid magnet polling remains the more explicit provider-lifecycle model, but the wiki's existing evidence shows that it carries more failure modes around cache visibility, file selection, and multi-step orchestration.

## Comparison

| Dimension | [[Comet Resolver Workflow for TorBox-Backed Downloads]] | [[Real-Debrid InstantAvailability API and Playback Issues]] |
|-----------|----------------------------------------------------------|-------------------------------------------------------------|
| Primary input | IMDb-style media identifier plus optional season/episode | Magnet or torrent hash plus provider-side file selection |
| Core API shape | Single token-gated stream query with inline TorBox config | Multi-step provider pipeline plus cache-check endpoint |
| Cache signal | Returned stream metadata (`TB⚡`, `/playback/<hash>/...`) | InstantAvailability API response, which can disappear or degrade |
| Ready artifact | Playback proxy URL that 302-redirects to TorBox CDN | Unrestricted link only after add/select/poll/unrestrict succeeds |
| State management | Re-query the resolver using stored `info_hash` continuity | Poll provider job state and reconcile file indices |
| Dominant failure mode | URL/token/config drift or parser mismatch | Disabled cache API, wrong file index, non-cached torrent playback errors |

## Analysis

The deepest difference between these approaches is where system complexity lives. In the Real-Debrid model, the application owns a large amount of the acquisition lifecycle: it submits the torrent, selects files, waits for provider-side state transitions, and finally asks for a usable link. That gives the app direct control, but it also means the app inherits every failure mode of that lifecycle. The existing [[Real-Debrid InstantAvailability API and Playback Issues]] page shows exactly how brittle that can become when one upstream endpoint is disabled or when torrent file structure does not align with naive file-index assumptions.

The Comet resolver workflow relocates that complexity into the resolver surface. The application still has to parse and rank streams, but it no longer needs to create or manage a provider job object for the happy path. The checkpoint is strong evidence that this is not merely theoretical: the operator verified live that a Comet playback URL redirects to a TorBox CDN file. That means the downloader can treat the resolver response as a near-final artifact instead of as a hint for a second provider conversation.

That simplification also changes how failure is observed. In the RD flow, failure is often a mismatch between intended torrent state and actual provider state: cache lookup unavailable, wrong file chosen, torrent still downloading, or an `.nfo` file accidentally treated as the target. In the Comet flow, the dominant risk shifts to contract interpretation. If the tokenized path, base64 config, stream markers, or playback URL schema change, the app may lose its ability to recover cache state and info hashes correctly. The new workflow is therefore less exposed to provider job semantics but more exposed to resolver schema drift.

For a private homelab, that trade-off is favorable when the operator already runs the resolver. Self-hosting Comet makes the token, deployment, and compatibility questions tractable in a way they would not be for an external black-box service. It also aligns better with the user's stated goal in the checkpoint: stop carrying a large RD-specific orchestration layer inside [[Debrid Downloader Web]] and instead let the surrounding homelab media stack do more of the work.

The two approaches are not mutually exclusive in principle. A downloader could keep a fallback path that drops to direct provider APIs when the resolver fails. But the source makes a clear product choice: for this application, reducing moving parts and converging on one query surface is more valuable than retaining maximum provider-specific control. That is why the shift from magnet polling to resolver re-query is the durable lesson worth preserving.

## Key Insights

1. **Resolver-first design is a state-machine reduction strategy** — [[Comet Resolver Workflow for TorBox-Backed Downloads]] cuts the downloader's owned lifecycle down to query, choose, and occasionally re-query.
2. **RD problems in this wiki are mostly orchestration problems, not just vendor problems** — [[Real-Debrid InstantAvailability API and Playback Issues]] documents how disabled cache checks and wrong file indices can break an app that directly owns too much provider lifecycle logic.
3. **Self-hosted addon infrastructure can become a backend API, not just a playback accessory** — the checkpoint elevates [[Comet]] from "something Stremio uses" to a reusable internal resolver for downloader workflows.

## Open Questions

- Should [[Debrid Downloader Web]] keep any direct provider fallback path for cases where Comet returns no usable `/playback/` streams?
- How stable is Comet's stream payload contract across upgrades, and should the downloader pin or test specific response shapes before deployment?

## Sources

- [[Copilot Session Checkpoint: Swapping Real-Debrid for Comet+TorBox]]
- [[Copilot Session Checkpoint: Fixing Knightcrawler Populate Cron and RD Playback]]
