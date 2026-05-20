---
title: Hermes Dashboard
type: entity
created: 2026-05-20
last_verified: 2026-05-20
source_hash: "9f73322caa1e7dd1cde0a5e61345567b71dcecf2677b697c8afaf98b5e50b867"
sources:
  - raw/2026-05-11-copilot-session-hermes-dashboard-migration-09a570cf.md
concepts:
  - host-managed-cli-dashboard-migration-homelab-services
  - cloudflare-access-gating-unauthenticated-homelab-dashboards
  - split-dns-routing-cloudflare-tunnel-overrides-homelab-services
related:
  - "[[Hermes Gateway]]"
  - "[[Cloudflare]]"
  - "[[Caddy]]"
  - "[[AdGuard]]"
  - "[[Homelab]]"
  - "[[Uptime Kuma]]"
tier: hot
tags: [hermes, dashboard, homelab, systemd, caddy, cloudflare-access]
---

# Hermes Dashboard

## Overview

Hermes Dashboard is the official host-managed web and TUI surface adopted in the homelab to replace the older community `hermes-webui` container. In this checkpoint it became the new operational front end for Hermes, exposed on port `9119` and paired with the gateway service so the dashboard could report live status and support the native Hermes workflow.

The migration mattered because it aligned the deployment with the upstream Hermes CLI instead of depending on a separate community-maintained container. That reduced drift, made the gateway and Kanban flow first-class, and turned the service into a host runtime concern managed through systemd rather than Docker Compose.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool / Service |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Operational Model

The dashboard is launched by a dedicated user unit, `config/systemd/user/hermes-dashboard.service`, which runs:

```bash
hermes dashboard --host 0.0.0.0 --port 9119 --no-open --insecure --tui
```

That command makes the dashboard reachable to the local reverse proxy while keeping the deployment rooted in the official Hermes CLI. The `--tui` flag signals that the migration was not just about a browser page; it also adopted Hermes' host-native interaction model.

## Security and Exposure

The checkpoint explicitly notes that Hermes Dashboard has **no native authentication** when bound beyond localhost. Because of that, it is only published through a [[Caddy]] route that checks for the `Cf-Access-Jwt-Assertion` header, allowing requests to pass through only after [[Cloudflare]] Access has already authenticated the user.

This design keeps the origin on plain local HTTP while shifting identity and public TLS concerns to the edge. The route also depends on [[AdGuard]] exact-host DNS rewrites so LAN users follow the same safe public path instead of falling through to an unintended local route.

## Monitoring and Impact

The dashboard became the canonical Hermes status surface in the homelab after the migration. Homepage was updated to link to `https://hermes.${DOMAIN}`, [[Uptime Kuma]] was updated to probe `http://host.docker.internal:9119/api/status`, and the prior `hermes-webui` container was removed entirely.

That combination makes Hermes Dashboard a good example of a host-managed service that still behaves like part of the broader homelab control plane: it has a systemd lifecycle, a proxy contract, a DNS requirement, and a monitoring contract.
