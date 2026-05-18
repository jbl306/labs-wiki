---
title: "Trusted-Domain Scope for Reverse-Proxied Nextcloud Checks"
type: concept
created: 2026-05-18
last_verified: 2026-05-18
source_hash: "f1615c76dd0a7e0be29992b380c486942c47624fcf57a9e648a03b30912314f7"
sources:
  - raw/2026-05-18-copilot-session-homelab-nba-repairs-e405020e.md
quality_score: 84
related:
  - "[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]"
  - "[[Homelab Media Domain Routing: LAN and Public HTTPS Diagnostics]]"
  - "[[Task-Specific Feature Profiles for Memory-Bounded ML Training]]"
tier: hot
tags: [nextcloud, reverse-proxy, trusted-domains, homelab, diagnostics]
---

# Trusted-Domain Scope for Reverse-Proxied Nextcloud Checks

## Overview

Trusted-domain scope is the operational discipline of keeping a reverse-proxied Nextcloud deployment's `trusted_domains`, overwrite settings, and actual routing surface tightly aligned. It matters because Nextcloud's setup checks do not merely validate syntax; they actively probe the configured domains, so an overly broad trust list can create false security failures that look like data-directory exposure.

## How It Works

In a simple mental model, operators think of `trusted_domains` as a static allowlist: add every hostname or IP that might reach the app, and Nextcloud will be safer because it will reject unknown hosts. The checkpoint shows why that model is incomplete in a reverse-proxied environment. Nextcloud also uses those configured domains as part of its own environment validation. Once a host is trusted, the setup-check machinery treats it as part of the deployment surface worth probing.

That matters when the effective routing layer is broader than the application owner's intent. In the repaired homelab deployment, the public service was supposed to live at `cloud.jbl-lab.com`, with [[Caddy]] terminating traffic and forwarding requests to the Nextcloud container. But the configuration still trusted the LAN IP `192.168.1.238`. From an operator's perspective that IP felt harmless because it was "just local access." From Nextcloud's perspective, however, it was another first-class host to validate.

The probing behavior becomes dangerous when the reverse proxy has wildcard or catch-all rules. The checkpoint records that requests to the LAN IP could hit Caddy's wildcard route and return `HTTP 200` for a synthetic path aimed at `/var/www/data/.ocdata`. That does not mean the data directory was truly exposed to the intended public interface. It means the checker found one trusted route that made the path look reachable. The false positive arose because the configuration surface was wider than the canonical service surface.

The durable fix therefore was not "move the data directory again" or "disable the warning." The data mount had already been moved to `/var/www/data`, outside the document root, which is normally correct. The real repair was to reduce scope: keep `TRUSTED_PROXIES=172.20.1.0/24` so proxy headers remain valid, keep overwrite settings aimed at `cloud.jbl-lab.com`, and shrink `trusted_domains` to the hostname that actually represents the service boundary. Once the checker only probed the canonical hostname, the warning disappeared because the observable surface matched the intended one.

This concept is broader than Nextcloud alone. In any reverse-proxied application, health checks, admin diagnostics, or CSRF host validation can implicitly treat every configured ingress as equally real. Operators often add LAN IPs, temporary tunnels, or wildcard aliases for convenience during setup, then forget that these values influence later security checks. The result is an environment where the software is not wrong; it is reacting correctly to a broader declared scope than the operator meant to preserve.

The checkpoint also highlights a useful debugging pattern: when an application reports exposure despite an apparently correct storage layout, inspect which hostnames and IPs the application believes are authoritative, then trace how each one resolves through the proxy from inside the container. That reframes the problem from "Why is Nextcloud lying?" to "Which trusted route makes the warning true from the app's point of view?" In operational terms, trusted-domain lists are not passive metadata. They are executable assumptions about ingress.

## Key Properties

- **Probe-driven validation:** Setup checks evaluate reachable trusted hosts, not just textual config values.
- **Canonical-host preference:** A single public hostname is usually safer than mixing LAN IPs, wildcards, and convenience aliases into the trusted set.
- **Proxy-aware correctness:** `TRUSTED_PROXIES`, overwrite host/protocol settings, and the trusted-domain list must describe the same network story.
- **False-positive risk:** Broad trust scope can make a reverse proxy surface internal or synthetic routes that look like app-level exposure.

## Limitations

Narrowing trusted domains can remove convenient alternate access paths such as direct LAN-IP access from a browser. If the canonical public hostname is unavailable during local recovery, operators may need a temporary maintenance procedure rather than permanently broadening the trust list again. This approach also assumes the reverse proxy and DNS routing are understood well enough to trace which host/path combinations are actually reachable from inside the stack.

## Examples

```ini
# Safer pattern
TRUSTED_PROXIES=172.20.1.0/24
OVERWRITEHOST=cloud.jbl-lab.com
NEXTCLOUD_TRUSTED_DOMAINS=cloud.jbl-lab.com
```

In the checkpoint, the difference between the failing and passing states was not a new storage mount. It was the removal of `192.168.1.238` from the trusted-domain set so setup checks stopped probing a wildcard-routed LAN entry point that returned `200 OK` for a synthetic `.ocdata` path.

## Practical Applications

This concept applies to self-hosted Nextcloud, media apps, admin dashboards, and any reverse-proxied service that validates hostnames or derives security posture from ingress configuration. It is especially useful in homelabs where the same service may be reachable through public DNS, split-DNS LAN routing, wildcard Caddy rules, and direct IP access unless operators intentionally narrow the declared surface.

## Related Concepts

- **[[Homelab Media Domain Routing: LAN and Public HTTPS Diagnostics]]**: Both focus on how hostname choice changes what the routing stack actually does.
- **[[Task-Specific Feature Profiles for Memory-Bounded ML Training]]**: Both fix failures by reducing an over-broad effective scope rather than adding more capacity or exceptions.
- **[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]**: That concept explains resource failures; this one explains configuration-surface failures that can look like security regressions.

## Sources

- [[Copilot Session Checkpoint: Homelab NBA repairs]] — primary source for the trusted-domain false-positive diagnosis and fix.

