---
title: "Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "8d4ffe804f00fc1786f05b552df93998c7e6bf7f3b353158464961c4edb4f8a3"
sources:
  - raw/2026-04-07-jbl306homelab.md
  - raw/2026-04-20-copilot-session-scheduler-dns-agents-cleanup-2222559c.md
quality_score: 64
concepts:
  - split-dns-routing-cloudflare-tunnel-overrides-homelab-services
related:
  - "[[Homelab Media Domain Routing: LAN and Public HTTPS Diagnostics]]"
  - "[[Copilot Session Checkpoint: Scheduler DNS Agents Cleanup]]"
tier: hot
tags: [dns, homelab, cloudflare, https, routing]
---

# Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services

## Overview

Split-DNS routing is a strategy for differentiating DNS answers between LAN and public access, enabling secure HTTPS routing for homelab services. Cloudflare tunnel overrides are used to ensure TLS-sensitive services resolve to public IPs even on LAN, preventing certificate errors and routing failures.

## How It Works

Homelab environments often require services to be accessible both locally (LAN) and remotely (public internet). Split-DNS routing achieves this by providing different DNS answers depending on the client’s network location. Typically, a wildcard DNS entry (e.g., `*.jbl-lab.com -> 192.168.1.238`) routes most LAN traffic directly to the local server, optimizing speed and reducing external dependency.

However, some services—especially those requiring HTTPS/TLS—need to resolve to public IPs (e.g., Cloudflare tunnel endpoints) even on LAN, because certificates are issued for public domains and browsers enforce strict certificate validation. If a service like `photos.jbl-lab.com` falls through to the LAN wildcard, it may route to a local HTTP-only path, causing HTTPS failures.

To address this, exact-host DNS overrides are added in the LAN DNS source-of-truth (e.g., AdGuard’s `dns-rewrites.json`). These overrides map specific hosts (like `photos.jbl-lab.com`) to Cloudflare IPs, ensuring LAN clients receive the same DNS answer as public clients for TLS-sensitive services. The process involves:

1. **Inventorying DNS Rewrites:** Review the `dns-rewrites.json` file to identify which services require Cloudflare tunnel routing.

2. **Adding Exact-Host Overrides:** Insert entries for hosts like `photos.jbl-lab.com` with Cloudflare IPs, overriding the wildcard.

3. **Syncing DNS Rewrites:** Run scripts (e.g., `sync-dns-rewrites.sh`) to propagate changes to the DNS server.

4. **Verification:** Use DNS tools to confirm LAN and public DNS answers match for overridden hosts. Test HTTPS access to ensure certificate validation succeeds.

5. **Documentation:** Update service guides and tunnel docs to reflect the override rationale and configuration.

This approach ensures seamless HTTPS access for TLS-sensitive homelab services regardless of client location, preventing routing failures and certificate errors.

## Key Properties

- **Wildcard LAN DNS Routing:** Routes most LAN traffic to local server IP for speed and reliability.
- **Exact-Host Cloudflare Overrides:** Overrides specific hosts to resolve to Cloudflare IPs, supporting HTTPS/TLS validation.
- **Sync and Verification Workflow:** Scripts and live DNS checks ensure configuration changes are propagated and validated.

## Limitations

Requires careful inventory of which services need Cloudflare routing; missing overrides cause HTTPS failures. DNS configuration drift can lead to inconsistent behavior. Overriding too many hosts may reduce LAN performance. Relies on Cloudflare tunnel health and correct certificate issuance.

## Example

```json
// Example AdGuard dns-rewrites.json entry
{
  "rewrites": [
    {"domain": "photos.jbl-lab.com", "answer": "104.21.4.183"},
    {"domain": "photos.jbl-lab.com", "answer": "172.67.132.88"}
  ]
}
```

## Relationship to Other Concepts

- **[[Homelab Media Domain Routing: LAN and Public HTTPS Diagnostics]]** — Split-DNS and tunnel overrides are mechanisms for robust media domain routing.

## Practical Applications

Used in homelab setups where services must be securely accessible via HTTPS both locally and remotely. Prevents certificate errors for TLS-sensitive apps like photo galleries, dashboards, or API endpoints. Supports hybrid LAN/public access patterns in modern self-hosted environments.

## Sources

- [[Copilot Session Checkpoint: Scheduler DNS Agents Cleanup]] — primary source for this concept
- [[jbl306/homelab]] — additional source
