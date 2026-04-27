---
title: "Copilot Session Checkpoint: Homelab migration and tunnel fix"
type: source
created: '2026-04-27'
last_verified: '2026-04-27'
source_hash: f05f51c65d6378e15448fa0d095133e89e8748f012e2613260b283a03ff2836c
sources:
  - raw/2026-04-27-copilot-session-homelab-migration-and-tunnel-fix-78392c21.md
tags: [copilot-session, checkpoint, homelab, debrid-downloader, sqlite, cloudflare, adguard, deployment]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 78
checkpoint_class: durable-architecture
retention_mode: retain
concepts:
  - single-user-local-sqlite-migration-self-hosted-web-apps
  - native-module-safe-docker-builds-uid-aligned-sqlite-mounts
  - split-dns-routing-cloudflare-tunnel-overrides-homelab-services
  - durable-copilot-session-checkpoint-promotion
related:
  - "[[Debrid Downloader Web]]"
  - "[[Homelab]]"
  - "[[KnightCrawler]]"
  - "[[Cloudflare]]"
  - "[[AdGuard]]"
  - "[[MemPalace]]"
  - "[[Qdrant]]"
  - "[[Migrating Cloud-Dependent Web Apps Into a Homelab]]"
---

# Copilot Session Checkpoint: Homelab migration and tunnel fix

## Summary

This checkpoint captures a full-stack migration of **[[Debrid Downloader Web]]** from a Vercel/Supabase deployment model into the user's **[[Homelab]]**, followed by a production incident that initially looked like a tunnel failure but was actually a LAN DNS split-routing bug. It also preserves an unfinished but important follow-on thread: the design exploration for exposing MemPalace-oriented storage metrics in the Homepage Qdrant card without violating the active brainstorming gate.

## Key Points

- **The app migration changed the system boundary, not just the hosting target**: `debrid-downloader-web` stopped depending on `@nuxtjs/supabase`, Supabase auth, hosted database tables, and Vercel deployment assumptions, then moved to a single-user local deployment with SQLite-backed state.
- **State persistence was localized without breaking the app's internal API shape**: a new `server/utils/local-store.ts` backed `user_settings` and `download_tasks`, while `server/utils/supabase.ts` was retained as an encrypted settings facade so helpers like `getUserSetting()` and `setUserSetting()` could keep their original call sites.
- **Authentication was intentionally collapsed to a fixed local identity**: the deployed app now runs as one local user (`local-user`, `local@homelab`) rather than maintaining multi-user auth complexity that no longer fit the homelab use case.
- **Torrent acquisition became multi-source and opinionated**: the app now accepts configurable Torrentio-compatible sources, queries them through `getTorrentioSources()` and `torrentioSearchAll()`, and ranks `knightcrawler` ahead of public Torrentio, MediaFusion, and StremThru/Torz fallbacks.
- **Deployment hardening required two concrete fixes after the first "successful" migration**: `.dockerignore` had to exclude host build artifacts so container-built `better-sqlite3` binaries would not be overwritten, and `compose.web.yml` had to run the container as `${PUID}:${PGID}` so SQLite could open files under the mounted `/data` directory.
- **Validation showed the app was actually healthy after those fixes**: the Caddy route returned HTTP 200, `/api/settings` returned `{}`, the container reported healthy, and SQLite files existed under `/opt/homelab/data/debrid-downloader-web/`.
- **The tunnel incident was a DNS architecture problem, not a Cloudflare or Caddy outage**: public HTTPS for `dldebrid.jbl-lab.com` already worked, but LAN clients still resolved the hostname through an AdGuard wildcard to the local server IP, where Caddy intentionally serves HTTP only on port 80.
- **The durable routing lesson is exact-host override over wildcard rewrite**: adding `dldebrid.jbl-lab.com` as a Cloudflare-targeted entry in `homelab/config/adguard/dns-rewrites.json` fixed local HTTPS by forcing LAN clients onto the same Cloudflare-terminated path as public clients.
- **The final user request remained intentionally unimplemented**: exploration identified `homelab/homepage-db-stats/app.py` and `homelab/config/homepage/services.yaml` as the likely integration points for wings, halls, rooms, drawers, and tunnels, but the active brainstorming workflow correctly blocked code changes before design approval.

## Key Concepts

- [[Single-User Local SQLite Migration for Self-Hosted Web Apps]]
- [[Native-Module-Safe Docker Builds and UID-Aligned SQLite Mounts]]
- [[Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services]]
- [[Durable Copilot Session Checkpoint Promotion]]

## Related Entities

- **[[Debrid Downloader Web]]** — The migrated application whose architecture, persistence model, and deployment path anchor the checkpoint.
- **[[Homelab]]** — The target runtime environment where Compose wiring, Homepage integration, AdGuard rewrites, and Caddy exposure all had to align.
- **[[KnightCrawler]]** — The preferred Torrentio-compatible source after the migration, promoted above public providers in fallback ranking.
- **[[Cloudflare]]** — The public DNS and tunnel termination layer that was healthy during the outage and became the correct LAN override target.
- **[[AdGuard]]** — The LAN DNS source of truth whose wildcard rewrite caused the misleading local-only HTTPS failure.
- **[[MemPalace]]** — The knowledge system whose storage vocabulary (wings, halls, rooms, drawers, tunnels) motivated the still-pending Homepage metrics enhancement.
- **[[Qdrant]]** — The database card the user wanted to augment with MemPalace-oriented storage metrics during the final exploratory thread.
