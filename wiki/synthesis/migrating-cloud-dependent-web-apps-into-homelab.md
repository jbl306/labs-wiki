---
title: "Migrating Cloud-Dependent Web Apps Into a Homelab"
type: synthesis
created: 2026-04-27
last_verified: 2026-04-27
source_hash: "synthesis-generated"
sources:
  - raw/2026-04-27-copilot-session-homelab-migration-and-tunnel-fix-78392c21.md
  - raw/2026-04-07-jbl306homelab.md
  - raw/2026-04-20-copilot-session-scheduler-dns-agents-cleanup-2222559c.md
concepts:
  - single-user-local-sqlite-migration-self-hosted-web-apps
  - native-module-safe-docker-builds-uid-aligned-sqlite-mounts
  - split-dns-routing-cloudflare-tunnel-overrides-homelab-services
related:
  - "[[Single-User Local SQLite Migration for Self-Hosted Web Apps]]"
  - "[[Native-Module-Safe Docker Builds and UID-Aligned SQLite Mounts]]"
  - "[[Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services]]"
tier: hot
tags: [homelab, migration, deployment, sqlite, docker, cloudflare]
quality_score: 75
---

# Migrating Cloud-Dependent Web Apps Into a Homelab

## Question

What has to change when a cloud-dependent web app is turned into a reliable homelab service: the application model, the container packaging, the network edge, or all three?

## Summary

The answer is **all three, in sequence**. A successful homelab migration starts by simplifying the app into a local-first single-user service, then hardens the container so native modules and SQLite mounts behave correctly, and finally fixes edge routing so public and LAN access follow the intended HTTPS path instead of an accidental local shortcut.

## Comparison

| Dimension | [[Single-User Local SQLite Migration for Self-Hosted Web Apps]] | [[Native-Module-Safe Docker Builds and UID-Aligned SQLite Mounts]] | [[Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services]] |
|-----------|---------------|---------------|---------------|
| Primary layer | Application and data model | Build and runtime packaging | DNS and edge routing |
| Core problem | Hosted auth/storage assumptions no longer fit a private operator model | The app builds, but native binaries or database files fail at runtime | HTTPS works publicly but fails locally because DNS resolves to the wrong path |
| Main intervention | Replace multi-user cloud state with local SQLite plus a fixed operator identity | Exclude host artifacts from Docker context and align runtime UID/GID with bind-mounted data | Add exact-host overrides so LAN clients resolve TLS-sensitive hosts through Cloudflare |
| Representative symptom | Auth pages, Supabase modules, and remote table logic feel unnecessary or fragile | `NODE_MODULE_VERSION` mismatch or `SQLITE_CANTOPEN` after deploy | `connection refused` on LAN HTTPS while public HTTPS already returns 200 |
| What success looks like | The app still works, but no longer needs SaaS-era scaffolding | Container is healthy and the SQLite file exists and is writable in `/data` | Public and LAN HTTPS both resolve through the intended Cloudflare-terminated route |
| Failure if skipped | You keep cloud complexity without cloud value | The migration looks done until production traffic exercises native modules or SQLite | Users misdiagnose a DNS split-brain issue as an app or proxy outage |

## Analysis

The most important synthesis insight is that "self-hosting" is not a single operation. Teams often talk about migrating an app as if moving it behind Docker and a reverse proxy were enough. This checkpoint shows that the hosting change is actually distributed across multiple layers that fail for different reasons. First the app has to stop expecting a SaaS trust boundary. Then the package has to survive real container execution. Then the hostname has to resolve the same way users expect, both inside and outside the LAN.

The application-layer move is usually the highest leverage. If a private service still behaves like a cloud product—multi-user auth, hosted persistence assumptions, remote-first helpers—every later deployment step inherits unnecessary complexity. That is why [[Single-User Local SQLite Migration for Self-Hosted Web Apps]] comes first in the sequence. It collapses the problem into a form the homelab can actually support cleanly: local state, one operator, fewer moving parts, and integrations that prefer local infrastructure such as [[KnightCrawler]].

But simplifying the application is not enough if packaging discipline is weak. [[Native-Module-Safe Docker Builds and UID-Aligned SQLite Mounts]] shows the next trap: once SQLite and native Node modules enter the picture, correctness depends on build context purity and volume ownership. These bugs are especially dangerous because they appear *after* a nominally successful migration. The artifact can build, the container can start, and the system can still be broken. This is why a homelab migration should treat build hygiene and bind-mount identity as first-class design concerns, not post-hoc debugging chores.

Finally, the checkpoint demonstrates that deployment success can still be undermined at the network edge. The app and container were both healthy when `dldebrid.jbl-lab.com` failed locally. The actual problem lived in DNS policy: a wildcard **[[AdGuard]]** LAN rewrite bypassed the Cloudflare TLS path and sent HTTPS clients to an HTTP-only **[[Caddy]]** listener. [[Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services]] completes the picture by showing that some services need exact-host public routing even on the LAN. Without that final layer, users experience a broken product even though the application and container are correct.

Taken together, these concepts suggest a practical order of operations for future migrations: simplify the app model, harden the package, then validate the edge. Reversing the order creates noise. Edge debugging is misleading when the app is still cloud-shaped; packaging bugs are harder to interpret when state and auth are still entangled with remote services.

## Key Insights

1. **Homelab migrations fail most often at layer boundaries, not inside one layer** — the current source shows app-state simplification, packaging hardening, and DNS edge correction as separate but sequentially necessary moves.
2. **SQLite is only "simple" when packaging and permissions are also simple** — the local-database win depends on `.dockerignore` correctness and `${PUID}:${PGID}` alignment, not just on choosing SQLite.
3. **Public success does not imply LAN success** — supported by [[Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services]] and the current checkpoint's `dldebrid.jbl-lab.com` incident.

## Open Questions

- When should a homelab migration keep multi-user auth instead of collapsing to a single trusted operator?
- Which Homepage or monitoring signals best indicate that a migrated service is healthy at the application, container, and edge-routing layers simultaneously?

## Sources

- [[Copilot Session Checkpoint: Homelab migration and tunnel fix]]
- [[jbl306/homelab]]
- [[Copilot Session Checkpoint: Scheduler DNS Agents Cleanup]]
