---
title: Hermes Gateway
type: entity
created: 2026-05-20
last_verified: 2026-05-20
source_hash: "9f73322caa1e7dd1cde0a5e61345567b71dcecf2677b697c8afaf98b5e50b867"
sources:
  - raw/2026-05-11-copilot-session-hermes-dashboard-migration-09a570cf.md
concepts:
  - host-managed-cli-dashboard-migration-homelab-services
related:
  - "[[Hermes Dashboard]]"
  - "[[Homelab]]"
  - "[[Caddy]]"
tier: hot
tags: [hermes, gateway, homelab, systemd, nodejs, whatsapp]
---

# Hermes Gateway

## Overview

Hermes Gateway is the long-running Hermes service that backs the host-managed dashboard deployment captured in this checkpoint. In the migrated architecture it is no longer an incidental helper behind a community WebUI container; it is a first-class systemd-managed process whose health directly affects dashboard status and bridge functionality.

The checkpoint makes the gateway noteworthy because the initial systemd launch strategy was wrong. The durable fix was to run the gateway in the foreground with `hermes gateway run --replace`, which matches how a service manager expects to supervise a persistent process.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool / Service |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Execution Model

The gateway is managed by `config/systemd/user/hermes-gateway.service`, replacing the earlier assumption that `hermes gateway start` would behave like a normal daemon entry point. In practice that command is a service-management helper, not the correct long-lived foreground process for systemd supervision.

The stable command is:

```bash
hermes gateway run --replace
```

That distinction is operationally important because it determines whether systemd sees a real service process or a wrapper that exits after trying to manipulate some other runtime state.

## Runtime Requirements

The checkpoint also records an environmental requirement: the gateway needed `/home/jbl/.nvm/versions/node/v20.20.1/bin` in `PATH` so the WhatsApp bridge could start correctly. Without that explicit Node.js path, the gateway service would be present but functionally incomplete.

This makes Hermes Gateway a good example of a host-managed CLI component whose success depends on inheriting the right runtime environment, not just on having the right unit file name or binary installed.

## Role in the Migration

The gateway is tightly coupled to [[Hermes Dashboard]] in the final deployment. The dashboard became the visible control surface, but the gateway provided the runtime state that made the new Hermes stack credible as a replacement for the removed containerized WebUI.

In that sense, the checkpoint's real architectural move was to promote both dashboard and gateway into managed host services inside [[Homelab]], with the proxy and docs updated around that new center of gravity.
