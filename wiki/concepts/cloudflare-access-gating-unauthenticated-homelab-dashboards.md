---
title: "Cloudflare Access Gating for Unauthenticated Homelab Dashboards"
type: concept
created: 2026-05-20
last_verified: 2026-05-20
source_hash: "9f73322caa1e7dd1cde0a5e61345567b71dcecf2677b697c8afaf98b5e50b867"
sources:
  - raw/2026-05-11-copilot-session-hermes-dashboard-migration-09a570cf.md
related:
  - "[[Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services]]"
  - "[[Homelab Media Domain Routing: LAN and Public HTTPS Diagnostics]]"
  - "[[Systematic Debugging and Test-Driven Development for UI Regression]]"
tier: hot
tags: [cloudflare, access, caddy, homelab, dashboard, security]
---

# Cloudflare Access Gating for Unauthenticated Homelab Dashboards

## Overview

Cloudflare Access gating for unauthenticated homelab dashboards is the pattern of publishing a local dashboard through a reverse proxy only when the request arrives with an identity token already issued by Cloudflare Access. It matters when the dashboard itself has no native authentication but still needs to be available remotely, because it lets the origin stay simple while moving trust, policy, and public TLS termination to the network edge.

## How It Works

The core idea is to separate **application reachability** from **user authorization**. A dashboard like Hermes can listen locally on plain HTTP and still remain safe for public use if the public route is not the dashboard itself, but a gate in front of it. In the checkpoint, the public hostname `hermes.jbl-lab.com` flows through Cloudflare and then into Caddy on port `80`. Only requests that already passed Cloudflare Access should reach the Hermes origin on `host.docker.internal:9119`.

The practical enforcement point is a header-based contract at the reverse proxy. Caddy was configured with a matcher on `Cf-Access-Jwt-Assertion`, the header Cloudflare injects after authenticating the user. Requests with that header are proxied upstream. Requests without it receive a deterministic `403 Cloudflare Access required`. This arrangement is useful because it keeps the policy boundary obvious: the dashboard should never decide who may log in, because it has no login system. The proxy decides whether the caller may reach the dashboard at all.

Ordering is the non-obvious detail that makes the pattern work. The checkpoint records that an earlier route structure caused Caddy to return `403` before the matcher-specific reverse proxy could run. The durable fix was to make the authorized route explicit and to place the fallback deny behavior after it. This is an important general lesson: security gates are not just about *what* you match, but also *when* your proxy engine evaluates that match. A correct policy expressed in the wrong order can still produce the wrong behavior.

Network path consistency is the next requirement. If LAN clients resolve the dashboard hostname differently from public clients, they may bypass the Cloudflare Access gate entirely or hit an unintended local listener. That is why this pattern pairs naturally with exact-host DNS overrides in AdGuard. Instead of letting `hermes.jbl-lab.com` fall through a wildcard LAN rewrite, the checkpoint pins it to Cloudflare-managed IPs so LAN and public clients traverse the same access-control path. Identity policy only works reliably when the route into the service is consistent.

Validation also changes under this pattern. Since the Caddy container image lacks common shell tools, the checkpoint uses plain `curl` against the published port `:80` with a `Host` header and, for local smoke tests, a synthetic `Cf-Access-Jwt-Assertion` value. That does **not** validate Cloudflare's JWT semantics end-to-end; it validates the local routing logic that decides whether a request with the expected header shape reaches the upstream service. This distinction matters: edge authentication and origin routing are separate layers, and both must be checked.

Finally, the checkpoint shows why this concept often blends security with debugging discipline. When the user later reported still seeing the old Hermes WebUI, the leading hypotheses were Cloudflare cache rules, a stale tunnel origin, or browser-side caching, not a local Hermes failure. That is exactly the kind of failure mode this pattern creates: if the edge is responsible for identity and caching, then stale behavior can persist even after the origin is correct. Operators have to debug the edge as seriously as they debug the service.

## Key Properties

- **Edge-authenticated origin access**: the service trusts the proxy boundary rather than implementing its own login flow.
- **Header-based gatekeeping**: `Cf-Access-Jwt-Assertion` acts as the proxy-visible signal that the request passed Cloudflare Access.
- **Deterministic deny behavior**: requests without the required header return a clear `403` instead of leaking the dashboard.
- **Route-order sensitivity**: allow rules must be evaluated before the deny fallback or the proxy will reject valid traffic.
- **Shared LAN/public pathing**: exact-host DNS overrides keep local clients on the same Cloudflare-protected path as remote clients.

## Limitations

This pattern depends on correct Cloudflare configuration, correct tunnel routing, and correct local DNS behavior; a mistake in any one of those layers can make the dashboard appear broken or accidentally exposed. Header presence checks at the origin do not themselves verify token authenticity; they assume the dashboard is only reachable through the trusted proxy path. Cached HTML, assets, or service workers can also make operators think the origin is stale when the real problem is at the edge or in the browser.

## Examples

```text
caddy.@cf_access.header: Cf-Access-Jwt-Assertion *
caddy.route.0_reverse_proxy: "@cf_access host.docker.internal:9119"
caddy.route.1_respond: "Cloudflare Access required" 403
```

```bash
# local route validation through Caddy
curl -fsS \
  -H 'Host: hermes.jbl-lab.com' \
  -H 'Cf-Access-Jwt-Assertion: smoke' \
  http://127.0.0.1/api/status
```

## Practical Applications

This approach fits admin dashboards, media-control panels, local AI tools, and other homelab services that are valuable remotely but were never designed to authenticate arbitrary internet users. It is especially useful when the operator already depends on Cloudflare for DNS and TLS termination and wants a consistent security pattern across multiple self-hosted services without modifying each application.

## Related Concepts

- **[[Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services]]**: ensures LAN DNS does not bypass the edge-authenticated route.
- **[[Homelab Media Domain Routing: LAN and Public HTTPS Diagnostics]]**: provides the broader routing-debug methodology for mixed LAN and public access paths.
- **[[Systematic Debugging and Test-Driven Development for UI Regression]]**: complements this pattern when stale edge behavior looks like an application regression.

## Sources

- [[Copilot Session Checkpoint: Hermes Dashboard Migration]] — documents the exact header gate, route-order failure mode, AdGuard rewrite, UFW rules, and debugging hypotheses.
