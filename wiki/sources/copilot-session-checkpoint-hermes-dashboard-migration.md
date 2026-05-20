---
title: "Copilot Session Checkpoint: Hermes Dashboard Migration"
type: source
created: '2026-05-20'
last_verified: '2026-05-20'
source_hash: 9f73322caa1e7dd1cde0a5e61345567b71dcecf2677b697c8afaf98b5e50b867
sources:
  - raw/2026-05-11-copilot-session-hermes-dashboard-migration-09a570cf.md
tags: [copilot-session, checkpoint, homelab, hermes, dashboard, systemd, cloudflare-access, caddy]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 76
checkpoint_class: durable-architecture
retention_mode: retain
concepts:
  - host-managed-cli-dashboard-migration-homelab-services
  - cloudflare-access-gating-unauthenticated-homelab-dashboards
  - split-dns-routing-cloudflare-tunnel-overrides-homelab-services
  - durable-copilot-session-checkpoint-promotion
related:
  - "[[Hermes Dashboard]]"
  - "[[Hermes Gateway]]"
  - "[[Homelab]]"
  - "[[Cloudflare]]"
  - "[[Caddy]]"
  - "[[AdGuard]]"
  - "[[Uptime Kuma]]"
  - "[[Publishing Homelab Dashboards Safely: Host Services, Access Gates, and DNS Pathing]]"
---

# Copilot Session Checkpoint: Hermes Dashboard Migration

## Summary

This checkpoint captures the migration of Hermes in the homelab from the legacy community `hermes-webui` container to the official host-managed dashboard, TUI, gateway, and Kanban workflow. It preserves both the finished operational changes and the unfinished debugging thread around stale public content, making it useful as a durable runbook for future authless dashboard rollouts behind [[Cloudflare]] and [[Caddy]].

## Key Points

- **The migration changed the operating model, not just the UI**: Hermes stopped being served by a Compose-managed community WebUI and was rebuilt around official host services for the dashboard and gateway.
- **Two new user services became the control plane**: `config/systemd/user/hermes-dashboard.service` runs `hermes dashboard --host 0.0.0.0 --port 9119 --no-open --insecure --tui`, while `config/systemd/user/hermes-gateway.service` runs the gateway in the foreground.
- **The gateway command mattered operationally**: `hermes gateway start` was the wrong systemd target because it is a service-management wrapper; the durable fix was `hermes gateway run --replace`.
- **Runtime dependencies had to be aligned with the host**: the gateway needed `/home/jbl/.nvm/versions/node/v20.20.1/bin` in `PATH` so the WhatsApp bridge would work under systemd.
- **Public exposure was intentionally narrowed**: because Hermes Dashboard has no native authentication, the Caddy route requires a `Cf-Access-Jwt-Assertion` header and otherwise returns `403 Cloudflare Access required`.
- **Network policy had to match the proxy topology**: UFW needed an allow rule for the `proxy` Docker network `172.20.1.0/24` before the deny-all rule on port `9119`, not just an allow on `docker0`.
- **LAN and public access were kept on the same secure path**: AdGuard gained an exact-host rewrite for `hermes.jbl-lab.com` so clients could resolve to Cloudflare-managed endpoints instead of falling through to a local wildcard.
- **Operations and observability were updated together**: Homepage now points to `https://hermes.${DOMAIN}`, Uptime Kuma monitors `http://host.docker.internal:9119/api/status`, and the obsolete `hermes-webui` service was removed.
- **Deployment automation was hardened during the migration**: the DNS sync script was fixed to load `.env` credentials, and GitHub Actions now skips deploy cleanly when SSH secrets are missing.
- **The checkpoint preserves an unresolved incident hypothesis**: after public exposure was configured, the user still saw the old WebUI, and the stored debugging plan centered on Cloudflare cache rules, tunnel origin misrouting, or browser-level cached assets rather than the local Hermes origin.

## Key Concepts

- [[Host-Managed CLI Dashboard Migration for Homelab Services]]
- [[Cloudflare Access Gating for Unauthenticated Homelab Dashboards]]
- [[Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services]]
- [[Durable Copilot Session Checkpoint Promotion]]

## Related Entities

- **[[Hermes Dashboard]]** — The new official control surface exposed through Caddy and protected by Cloudflare Access.
- **[[Hermes Gateway]]** — The long-running companion process that had to be launched correctly for the dashboard and bridge integrations to work.
- **[[Homelab]]** — The host environment where systemd, UFW, AdGuard, Homepage, and Caddy all had to align.
- **[[Cloudflare]]** — The public DNS and access-control layer used to keep an authless dashboard off the open internet.
- **[[Caddy]]** — The reverse proxy whose matcher ordering determined whether authorized requests reached Hermes or were rejected early.
- **[[AdGuard]]** — The LAN DNS source of truth updated with an exact-host rewrite for `hermes.jbl-lab.com`.
- **[[Uptime Kuma]]** — The monitoring surface updated to watch the new dashboard API instead of the old WebUI.
