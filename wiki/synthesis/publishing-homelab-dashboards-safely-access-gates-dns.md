---
title: "Publishing Homelab Dashboards Safely: Host Services, Access Gates, and DNS Pathing"
type: synthesis
created: 2026-05-20
last_verified: 2026-05-20
source_hash: "synthesis-generated"
sources:
  - raw/2026-05-11-copilot-session-hermes-dashboard-migration-09a570cf.md
  - raw/2026-04-07-jbl306homelab.md
  - raw/2026-04-20-copilot-session-scheduler-dns-agents-cleanup-2222559c.md
concepts:
  - host-managed-cli-dashboard-migration-homelab-services
  - cloudflare-access-gating-unauthenticated-homelab-dashboards
  - split-dns-routing-cloudflare-tunnel-overrides-homelab-services
related:
  - "[[Host-Managed CLI Dashboard Migration for Homelab Services]]"
  - "[[Cloudflare Access Gating for Unauthenticated Homelab Dashboards]]"
  - "[[Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services]]"
tier: hot
tags: [homelab, dashboard, systemd, cloudflare, caddy, dns]
quality_score: 79
---

# Publishing Homelab Dashboards Safely: Host Services, Access Gates, and DNS Pathing

## Question

What has to line up before a homelab dashboard can be both officially managed on the host and safely reachable from anywhere without exposing an unauthenticated origin?

## Summary

Three layers have to align at once: the service must run under the correct host-native supervision model, the public edge must require an access gate before proxying, and LAN DNS must preserve that same edge path instead of bypassing it. The Hermes checkpoint adds the missing middle layer to earlier homelab routing knowledge by showing that safe publication is not only about DNS and tunnels, but also about identity enforcement at the reverse proxy.

## Comparison

| Dimension | [[Host-Managed CLI Dashboard Migration for Homelab Services]] | [[Cloudflare Access Gating for Unauthenticated Homelab Dashboards]] | [[Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services]] |
|-----------|---------------|---------------|---------------|
| Primary concern | Runtime ownership and service supervision | Identity and public exposure control | Consistent pathing between LAN and public clients |
| Main failure if skipped | The dashboard exists, but the wrong command or environment makes it unstable | The dashboard is reachable without native auth or valid users get blocked by bad route order | HTTPS behaves differently on LAN than in public, causing misleading failures |
| Key implementation lever | systemd user units with foreground CLI commands | Caddy matcher on `Cf-Access-Jwt-Assertion` plus explicit `403` fallback | Exact-host DNS overrides to Cloudflare IPs instead of wildcard LAN rewrites |
| Representative symptom | `... start` works manually but fails under service supervision | Public route returns `403` too early or leaks the dashboard | Public URL works, LAN URL fails or bypasses the intended TLS/access path |
| Boundary being protected | Host process lifecycle | Reverse-proxy trust boundary | DNS/routing boundary |
| What success looks like | Official dashboard and gateway replace the old container cleanly | Only Access-authenticated requests reach the origin | Local and remote users experience the same secure route |

## Analysis

The older homelab routing concepts already established that DNS is often the hidden cause of "broken" self-hosted services. If a LAN client resolves a hostname differently from a public client, the operator can waste hours debugging the app or proxy when the real problem is split pathing. [[Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services]] captured that lesson well, but it assumed the destination service was already the right one and that the edge policy was conceptually settled.

The Hermes checkpoint extends that story by showing a different but complementary failure class: sometimes the service itself has moved. Replacing a community container UI with an official host-native dashboard changes the runtime model first. Now the operator has to think in systemd user services, foreground commands, PATH inheritance, and bridge dependencies. That is what [[Host-Managed CLI Dashboard Migration for Homelab Services]] contributes: before the hostname and edge can be trusted, the underlying process model must be trustworthy.

Once the runtime is correct, the checkpoint adds the missing security layer between "service is running" and "service is safe to publish." Hermes Dashboard had no native auth when bound beyond localhost, so public availability could not be treated as a simple reverse-proxy task. [[Cloudflare Access Gating for Unauthenticated Homelab Dashboards]] shows that the edge must become an identity gate, not just a router. The `Cf-Access-Jwt-Assertion` matcher and explicit `403` fallback embody that shift.

What makes this synthesis especially useful is that these three concepts are sequential rather than interchangeable. A host-managed dashboard without an access gate is operationally neat but unsafe. An access gate without correct DNS pathing is safe in theory but inconsistent in practice. Correct DNS pathing without the right host service model only routes users cleanly to the wrong or unstable runtime. The architecture works only when all three layers agree on the same intended request path.

This also explains why the unresolved "still seeing the old WebUI" report remained ambiguous. By the time that incident appeared, the origin looked healthy locally. That pushed the likely fault domain outward toward Cloudflare cache rules, public-hostname routing, or browser residue. In other words, once host services, access gates, and DNS pathing are layered correctly, the remaining failures become easier to localize because each layer has a clearer contract.

## Key Insights

1. **Safe dashboard publication is a three-layer problem, not a single reverse-proxy tweak** — the current Hermes checkpoint only makes full sense when combined with [[Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services]].
2. **Identity gating belongs at the edge when the app has no auth of its own** — supported by [[Cloudflare Access Gating for Unauthenticated Homelab Dashboards]] and the Hermes Caddy route design.
3. **Runtime supervision bugs and routing bugs can look similar from the browser** — the synthesis is useful because it separates service-lifecycle failures from pathing and cache failures.

## Open Questions

- When should a homelab operator choose local auth in the application instead of depending on Cloudflare Access at the edge?
- Which cache-control headers or Cloudflare cache rules are worth standardizing for authless admin dashboards to reduce stale-content incidents?

## Sources

- [[Copilot Session Checkpoint: Hermes Dashboard Migration]]
- [[Copilot Session Checkpoint: Homelab migration and tunnel fix]]
- [[jbl306/homelab]]
