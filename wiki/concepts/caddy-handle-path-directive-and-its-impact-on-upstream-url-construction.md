---
title: "Caddy handle_path Directive and Its Impact on Upstream URL Construction"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "62a3c4ffbf12d604468b3d8046bc22088aed94feabac8006f2b13c5583c1d345"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-resource-optimization-opencode-bash-fix-c00d8543.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-knightcrawler-gating-fix-opencode-bash-config-b0a35301.md
quality_score: 84
concepts:
  - caddy-handle-path-directive-and-its-impact-on-upstream-url-construction
related:
  - "[[KnightCrawler Gating Fix for Stremio Streams]]"
  - "[[Copilot Session Checkpoint: KnightCrawler Gating Fix, Opencode Bash Config]]"
tier: hot
tags: [caddy, reverse-proxy, handle_path, url-construction, domain-gating]
---

# Caddy handle_path Directive and Its Impact on Upstream URL Construction

## Overview

This concept explains the behavior of Caddy's `handle_path` directive, which strips the matched path prefix before proxying requests upstream. This behavior affects applications that build absolute URLs based on the incoming request path, requiring adjustments to URL construction to maintain correct routing.

## How It Works

Caddy's `handle_path` directive is used to match requests with a specific path prefix and then strip that prefix before forwarding the request to the upstream server. This means that the upstream server receives requests without the prefix and is unaware of it.

For example, if Caddy is configured with:
```
handle_path /token123/* {
  reverse_proxy upstream
}
```
A request to `/token123/api/data` will be proxied as `/api/data` to the upstream.

This behavior is beneficial for simplifying upstream routing but introduces challenges when the upstream application generates absolute URLs for clients. Since the upstream sees paths without the prefix, it builds URLs that omit the prefix, causing clients to request URLs that Caddy does not recognize, leading to 404 errors.

To address this, upstream applications must be made aware of the prefix or have their URL construction logic patched to include the prefix. This can be done by injecting environment variables with the prefix value and modifying URL-building code to prepend the prefix.

This concept is critical in scenarios involving domain gating, authentication tokens in URLs, or multi-tenant routing where path prefixes are used for access control.

## Key Properties

- **Prefix Stripping:** The matched path prefix is removed before proxying, making upstream unaware of it.
- **Upstream URL Construction Impact:** Upstream apps must compensate for missing prefix when building absolute URLs.
- **Use Cases:** Common in domain gating, token-based routing, and multi-tenant proxies.

## Limitations

This design requires careful synchronization between proxy configuration and upstream URL logic. If not handled, it causes broken links and 404 errors. It also complicates upstream application design, as they must be aware of proxy path manipulations or rely on patches, reducing modularity.

## Example

Caddy config snippet:
```
handle_path /${KC_ACCESS_TOKEN}/* {
  reverse_proxy knightcrawler-addon
}
```
Upstream patch snippet:
```js
const url = `https://${i.headers.host}/${process.env.KC_ACCESS_TOKEN}`;
```


## Relationship to Other Concepts

- **[[KnightCrawler Gating Fix for Stremio Streams]]** — Directly addresses the URL construction mismatch caused by handle_path prefix stripping.

## Practical Applications

Understanding this directive is essential for developers deploying services behind Caddy with path-based gating or routing. It informs how to design upstream applications and proxy configurations to ensure correct URL resolution and access control.

## Sources

- [[Copilot Session Checkpoint: KnightCrawler Gating Fix, Opencode Bash Config]] — primary source for this concept
- [[Copilot Session Checkpoint: Resource Optimization, Opencode Bash Fix]] — additional source
