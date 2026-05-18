---
title: "Nextcloud"
type: entity
created: 2026-05-18
last_verified: 2026-05-18
source_hash: "f1615c76dd0a7e0be29992b380c486942c47624fcf57a9e648a03b30912314f7"
sources:
  - raw/2026-05-18-copilot-session-homelab-nba-repairs-e405020e.md
concepts:
  - trusted-domain-scope-reverse-proxied-nextcloud-checks
related:
  - "[[Homelab]]"
  - "[[Caddy]]"
  - "[[Trusted-Domain Scope for Reverse-Proxied Nextcloud Checks]]"
tier: hot
tags: [nextcloud, homelab, reverse-proxy, storage, configuration]
---

# Nextcloud

## Overview

Nextcloud is the self-hosted cloud and file-sync service running in the [[Homelab]] cloud stack. In this checkpoint it appears not as an abstract app category but as a live operational system with concrete proxy, mount, and setup-check contracts that had drifted out of alignment.

The session matters because it records a failure mode that looks like an application-level database problem but was actually rooted in container file ownership and overly broad trusted-domain configuration. That makes this page useful as a practical operations reference for future repairs, not just a catalog entry for a familiar self-hosted tool.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | https://cloud.jbl-lab.com |
| Status | Active |

## Operational Context

The live deployment uses the official `nextcloud:29-apache` image and sits behind [[Caddy]] in the homelab's cloud stack. The checkpoint records several durable runtime expectations: the service should trust proxy traffic from `172.20.1.0/24`, use `cloud.jbl-lab.com` as its canonical overwrite host, store data outside the web root at `/var/www/data`, and run background jobs via cron rather than web requests.

These settings matter because Nextcloud's own setup checks inspect the effective deployment shape rather than only parsing config values. If the proxy, overwrite, and trusted-domain surfaces do not match the real serving topology, the admin UI can report misleading security or exposure warnings even when the underlying storage layout is otherwise correct.

## Failure Mode and Root Cause

The immediate runtime symptoms were `fopen(/var/www/html/config/config.php): Permission denied`, a complaint that configuration "was not read or initialized correctly", and follow-on SQLite-style fallback errors while rendering the failure page. The checkpoint establishes that these were secondary effects: because `config.php` could not be read, Nextcloud behaved as though core configuration had vanished.

The concrete root cause was a mount-ownership mismatch. The official image runs as `www-data` with UID/GID `33`, but the host-mounted config and data directories were owned by `1000:1000`, while `config.php` was mode `640`. That combination blocked the application from reading and updating its own configuration until ownership was corrected to `33:33` and the homelab setup script was changed to preserve that ownership model.

## Trusted Domain and Proxy Hygiene

After the permission fix, one warning remained: "Data directory protected" still failed even though the data mount had already been moved outside the web root. The durable lesson is that Nextcloud's setup checks probe every trusted domain, not only the public hostname the operator mentally treats as canonical.

In this case, `trusted_domains` still included the LAN IP `192.168.1.238`. From inside the container, probes against that address hit [[Caddy]]'s wildcard LAN routing and returned `HTTP 200` for a synthetic `/var/www/data/.ocdata` path, which made Nextcloud infer exposure that did not exist on the public service. Narrowing trusted domains to `cloud.jbl-lab.com` fixed the false positive because it aligned the checker's probe set with the intended external surface.

## Impact

This checkpoint turns Nextcloud into a durable example of configuration-surface discipline in self-hosted systems. The best fix was not a generic restart or broader allowlist, but a precise match between the app's filesystem permissions, reverse-proxy trust boundaries, and canonical hostname set.

## Sources

- [[Copilot Session Checkpoint: Homelab NBA repairs]] — documents the permission, proxy, and trusted-domain fixes applied to the live homelab deployment.

