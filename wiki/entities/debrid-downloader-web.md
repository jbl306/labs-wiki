---
title: Debrid Downloader Web
type: entity
created: 2026-04-27
last_verified: 2026-04-27
source_hash: f05f51c65d6378e15448fa0d095133e89e8748f012e2613260b283a03ff2836c
sources:
  - raw/2026-04-27-copilot-session-homelab-migration-and-tunnel-fix-78392c21.md
concepts:
  - single-user-local-sqlite-migration-self-hosted-web-apps
  - native-module-safe-docker-builds-uid-aligned-sqlite-mounts
related:
  - "[[Homelab]]"
  - "[[KnightCrawler]]"
  - "[[Caddy]]"
  - "[[Cloudflare]]"
  - "[[AdGuard]]"
tier: hot
tags: [self-hosted, nuxt, sqlite, torrentio, homelab, debrid]
---

# Debrid Downloader Web

## Overview

Debrid Downloader Web is a self-hostable web application for discovering torrents, pushing them through debrid flows, and tracking the resulting download tasks. In this checkpoint it stops being treated as a cloud-first Nuxt app and is reworked into a homelab-native service that persists its own local state, uses a fixed single-user identity, and plugs directly into the surrounding infrastructure.

The migration matters because it preserves the useful product behavior while deleting the operational assumptions that were hardest to justify in a private homelab deployment: hosted Supabase auth, remote table persistence, and Vercel-specific packaging. What remains is a simpler service that still exposes settings, search, and download flows, but now fits the trust model and ergonomics of a single-operator environment.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | jbl306 |
| URL | https://github.com/jbl306/debrid-downloader-web |
| Status | Active |

## Local Persistence Model

The app now stores its operational state in SQLite rather than remote Supabase tables. A new `server/utils/local-store.ts` owns schema creation and CRUD for `user_settings` and `download_tasks`, while the old `server/utils/supabase.ts` helper surface was preserved as an encrypted settings layer. That compatibility decision let the migration replace the storage backend without forcing a full rename-driven rewrite across every route that touched settings.

Authentication was also collapsed into a deliberate single-user model. Instead of sign-in, reset, and route-guard complexity, the runtime treats the operator as one fixed local account with the identity `local-user` / `local@homelab`. This makes the app fit the operational reality of a private homelab while keeping downstream UI and API behavior stable.

## Acquisition and Source Strategy

Debrid Downloader Web now queries multiple Torrentio-compatible providers instead of assuming a single upstream. The session added `getTorrentioSources()` and `torrentioSearchAll()` so source definitions can be supplied as a comma-separated `name=url` list, with homelab configuration ranking **[[KnightCrawler]]** first, then public Torrentio, then MediaFusion, and then StremThru/Torz-style fallbacks.

That source ordering is important because the app is not just "more configurable" after migration; it becomes explicitly biased toward the user's own infrastructure first. The checkpoint records that quality fallback ranking was updated so `knightcrawler` outranks public `torrentio`, giving the local stack first claim on search and acquisition decisions.

## Deployment Model

The service was packaged into a multi-stage Node 22 Docker image and added to `homelab/compose/compose.web.yml`. It joins the `proxy` and `stremio` networks, mounts `${HOMELAB_BASE}/data/debrid-downloader-web:/data`, and is exposed through **[[Caddy]]** at `http://dldebrid.${DOMAIN}` rather than by a direct host port.

Two production hardening lessons are central to the entity's current shape. First, `.dockerignore` had to exclude host `node_modules` and other build artifacts so the container's native `better-sqlite3` binary would not be overwritten and crash with a `NODE_MODULE_VERSION` mismatch. Second, the service had to run as `${PUID}:${PGID}` so the mounted SQLite database would be writable by the same ownership scheme the homelab uses elsewhere.

## Operational Lessons

The public-reachability incident after deployment was not caused by the app itself. Public Cloudflare HTTPS already worked; only LAN clients failed because **[[AdGuard]]** still resolved `dldebrid.jbl-lab.com` through a wildcard LAN rewrite to the local server IP, while **[[Caddy]]** intentionally had no HTTPS listener on 443. The durable fix was an exact-host Cloudflare override, not a code or proxy change inside the application.

That distinction makes the app a good example of why self-hosted services need to be analyzed across three layers at once: application state, container packaging, and network exposure. Debrid Downloader Web succeeded only once all three layers were aligned.
