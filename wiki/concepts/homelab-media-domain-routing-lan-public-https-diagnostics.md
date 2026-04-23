---
title: "Homelab Media Domain Routing: LAN and Public HTTPS Diagnostics"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9087cb7649f7304dd2917525af12c2fd1f436fd5b0eb12bcf0b6c9787bb8f3f4"
sources:
  - raw/2026-04-18-copilot-session-knightcrawler-done-routing-traced-7bbbddcd.md
quality_score: 64
concepts:
  - homelab-media-domain-routing-lan-public-https-diagnostics
related:
  - "[[Caddy handle_path Directive and Its Impact on Upstream URL Construction]]"
  - "[[Copilot Session Checkpoint: Knightcrawler done, routing traced]]"
tier: hot
tags: [homelab, routing, dns, cloudflare, caddy, media-services]
---

# Homelab Media Domain Routing: LAN and Public HTTPS Diagnostics

## Overview

A systematic approach to diagnosing and resolving media service routing issues in a homelab environment, focusing on the interplay between LAN DNS rewrites, Caddy proxy configuration, and Cloudflare tunnel/public DNS. The analysis distinguishes between LAN HTTP, LAN HTTPS, and public HTTPS access patterns.

## How It Works

The homelab media domain routing diagnostic process begins by mapping out the flow of requests for media services (Jellyfin, Plex, Riven, Seerr) across different access scenarios: LAN HTTP, LAN HTTPS, and public HTTPS. The environment uses AdGuard for DNS rewrites, Caddy as an HTTP-only reverse proxy (listening on port 80), and Cloudflare for public DNS and TLS termination.

On the LAN, DNS rewrites (via `config/adguard/dns-rewrites.json`) direct wildcard subdomains (e.g., `*.jbl-lab.com`) to the server's local IP (`192.168.1.238`). Caddy is intentionally configured to listen only on HTTP (`:80`), with no local TLS listener. As a result, LAN HTTP requests (e.g., `http://jellyfin.jbl-lab.com`) are routed correctly and succeed, while LAN HTTPS requests (e.g., `https://jellyfin.jbl-lab.com`) fail because there is no service listening on port 443.

For public access, Cloudflare manages DNS and terminates TLS. Public HTTPS requests are routed through Cloudflare's tunnel, which forwards them as HTTP to the Caddy proxy. This setup works as intended, with public HTTPS requests to media domains returning valid responses (or expected 401s for protected services like Plex).

The key diagnostic insight is that the observed failures are isolated to LAN HTTPS requests. These fail because the LAN DNS rewrite points to the server IP, but Caddy is not listening for HTTPS traffic. The recommended fix is to add exact-host Cloudflare DNS overrides for the affected media domains, ensuring that LAN clients using HTTPS are routed through Cloudflare (which handles TLS termination) rather than directly to the server's HTTP-only listener.

Throughout the process, the investigation employs a variety of tools: container status checks, DNS resolution tests, HTTP/HTTPS curls (with and without Host headers), Cloudflare DNS-over-HTTPS lookups, and direct HTTPS probes through Cloudflare IPs. This comprehensive approach ensures that each layer of the routing stack is validated and that the root cause is accurately identified.

## Key Properties

- **Layered Routing Analysis:** Distinguishes between LAN HTTP, LAN HTTPS, and public HTTPS, identifying where failures occur and why.
- **DNS Rewrite Control:** Uses AdGuard DNS rewrites to direct traffic for specific hostnames, with the ability to override wildcards for exact hosts.
- **Cloudflare TLS Termination:** Leverages Cloudflare to handle public HTTPS requests, forwarding them to the homelab's HTTP-only proxy.
- **Caddy HTTP-Only Design:** Caddy proxy is intentionally limited to HTTP on port 80, simplifying internal routing but requiring careful DNS management for HTTPS.

## Limitations

The approach relies on Cloudflare for public HTTPS and cannot support LAN HTTPS unless DNS is explicitly configured to route those requests through Cloudflare. Local HTTPS to the server IP will always fail unless Caddy is reconfigured to listen on 443 with valid certificates, which may not align with the intended architecture. DNS misconfiguration or incomplete overrides can result in inconsistent access patterns, confusing users.

## Example

A user on the LAN tries to access `https://jellyfin.jbl-lab.com` and the request fails. Investigation shows that the DNS rewrite points to the server IP, but Caddy is not listening on 443. Adding an exact-host DNS override for `jellyfin.jbl-lab.com` to point to the Cloudflare tunnel IP resolves the issue, allowing LAN HTTPS requests to succeed via Cloudflare.

## Visual

No diagrams or images are present in the source; the relationships are described textually.

## Relationship to Other Concepts

- **[[Caddy handle_path Directive and Its Impact on Upstream URL Construction]]** — Both involve Caddy's role in proxying and routing requests for homelab services.

## Practical Applications

This diagnostic and routing pattern is applicable to any homelab or self-hosted environment where services must be accessible both on the LAN and publicly, especially when using a reverse proxy and DNS-based routing. It is particularly relevant for media servers, dashboards, or any service with both local and remote users. The approach ensures consistent access and minimizes surprises due to protocol or DNS mismatches.

## Sources

- [[Copilot Session Checkpoint: Knightcrawler done, routing traced]] — primary source for this concept
