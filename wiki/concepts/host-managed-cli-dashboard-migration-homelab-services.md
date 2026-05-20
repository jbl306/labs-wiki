---
title: "Host-Managed CLI Dashboard Migration for Homelab Services"
type: concept
created: 2026-05-20
last_verified: 2026-05-20
source_hash: "9f73322caa1e7dd1cde0a5e61345567b71dcecf2677b697c8afaf98b5e50b867"
sources:
  - raw/2026-05-11-copilot-session-hermes-dashboard-migration-09a570cf.md
related:
  - "[[Cloudflare Access Gating for Unauthenticated Homelab Dashboards]]"
  - "[[Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services]]"
  - "[[Durable Copilot Session Checkpoint Promotion]]"
tier: hot
tags: [homelab, systemd, dashboard, migration, gateway, operations]
---

# Host-Managed CLI Dashboard Migration for Homelab Services

## Overview

Host-managed CLI dashboard migration is the pattern of replacing an older containerized or community-maintained UI with the upstream application's own dashboard, terminal UI, and companion services, then managing them directly on the host with a service manager such as systemd. It matters in homelabs because many modern tools now ship rich CLI-native operational surfaces that work better as supervised host services than as ad hoc Docker wrappers.

## How It Works

The pattern starts with an architectural reclassification: the service is no longer treated as "a web app that happens to be deployed in Docker," but as "a host-native CLI system that may expose a dashboard." That change sounds subtle, but it affects almost every later decision. In the Hermes checkpoint, the old community `hermes-webui` Compose service stopped being the authoritative interface. The official Hermes dashboard, TUI, gateway, and Kanban flow became the source of truth instead. Once that happens, the migration target is not merely a new URL; it is a new control plane.

Next, the operator inventories which pieces belong to the new host-managed stack. In this checkpoint there were at least two: the dashboard itself and the gateway that feeds it runtime state and bridge integrations. The durable move was to create explicit user services for each one, rather than burying startup commands in shell notes or temporary terminals. This is where systemd user units matter: they define the execution command, the lifecycle expectations, and the environment that must be reproduced after reboots, deploys, and operator mistakes.

The crucial implementation detail is that upstream CLI tools often expose commands that look service-friendly but are actually administrative wrappers. Hermes surfaced that trap clearly. `hermes gateway start` sounds like the obvious launch command, but in practice it is a service-management action, not the long-lived foreground process that systemd should own. The stable command was `hermes gateway run --replace`. This is a general lesson for host-managed migrations: always distinguish **control commands** from **foreground runtime commands**. A service manager wants the latter.

Environment inheritance becomes the next major concern. Containers often hide runtime dependencies because their filesystem, PATH, and package layout are frozen into an image. When a service moves onto the host, that implicit environment has to be made explicit. Hermes Gateway needed `/home/jbl/.nvm/versions/node/v20.20.1/bin` in `PATH` so the WhatsApp bridge could work. Without that line, the unit could start and still fail at the application layer. This is why host-managed migrations should treat the environment as part of the design, not as an afterthought.

After the services exist, the migration has to rebalance the surrounding infrastructure. The obsolete container or Compose stanza should be removed so there is one authoritative runtime path. Monitoring and operator docs must pivot as well: Homepage should link to the new URL, health checks should target the new API, and troubleshooting docs should describe the new process model rather than the retired container. In the checkpoint, Uptime Kuma switched to the dashboard API, the `hermes-webui` service disappeared from Compose, and the service guide plus tunnel docs were rewritten around the new host-native model.

Finally, the pattern is only complete when network policy and reverse proxy behavior match the host-managed reality. Running on the host does not mean publishing directly to the internet. Hermes still lived behind Caddy, UFW, AdGuard, and Cloudflare Access. The dashboard bound to `0.0.0.0:9119`, but access to that port was constrained to the proxy path and specific subnets. This reveals the real intuition behind the pattern: the host becomes the runtime boundary, while the proxy and firewall remain the exposure boundary. A successful migration keeps those roles distinct.

## Key Properties

- **Foreground-first supervision**: the correct systemd target is the real long-lived process, not a convenience wrapper like `... start`.
- **Environment-explicit execution**: PATH entries, bridge dependencies, and interpreter locations must be encoded deliberately.
- **Single source of operational truth**: the old containerized surface is removed so operators and monitors do not straddle two runtimes.
- **Infrastructure fan-out**: docs, Homepage, monitoring, and firewall rules all change together because they depend on the new runtime model.
- **CLI-native alignment**: the migration captures upstream capabilities such as dashboard, TUI, and Kanban flow without waiting for community container lag.

## Limitations

This pattern assumes the host is trusted enough to run application services directly and that the operator is comfortable managing user units, PATH inheritance, and local firewall policy. It can increase coupling to the host environment, especially when Node.js, Python, or other user-scoped toolchains are required. It also works best for single-operator homelabs; in larger shared environments, containers may still be preferable for isolation, repeatability, or policy control.

## Examples

```ini
# systemd user unit pattern
[Service]
Environment="PATH=/home/jbl/.nvm/versions/node/v20.20.1/bin:/usr/local/bin:/usr/bin"
ExecStart=/home/jbl/projects/homelab/scripts/ops/hermes-gateway.sh
Restart=on-failure
```

```bash
# durable foreground command
hermes gateway run --replace
hermes dashboard --host 0.0.0.0 --port 9119 --no-open --insecure --tui
```

## Practical Applications

This concept applies whenever a homelab service graduates from an unofficial UI wrapper to an upstream-supported operational surface. Good candidates include dashboards bundled with CLIs, local-first agent platforms, workflow engines, and bridge processes that need host credentials or user-scoped runtimes. It is especially useful when the upstream tool already exposes health endpoints, terminal workflows, or service-oriented subcommands that make host supervision more natural than container packaging.

## Related Concepts

- **[[Cloudflare Access Gating for Unauthenticated Homelab Dashboards]]**: host-managed dashboards still need a secure publication model at the edge.
- **[[Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services]]**: once a dashboard is published, LAN and public routing must follow the same intended path.
- **[[Durable Copilot Session Checkpoint Promotion]]**: this migration pattern was preserved as durable operational knowledge via checkpoint ingestion.

## Sources

- [[Copilot Session Checkpoint: Hermes Dashboard Migration]] — captures the concrete Hermes migration, service units, launcher commands, and follow-on operational fixes.
