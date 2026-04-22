---
title: "KnightCrawler Gating Fix for Stremio Streams"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "62a3c4ffbf12d604468b3d8046bc22088aed94feabac8006f2b13c5583c1d345"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-knightcrawler-gating-fix-opencode-bash-config-b0a35301.md
quality_score: 69
concepts:
  - knightcrawler-gating-fix-for-stremio-streams
related:
  - "[[Copilot Session Checkpoint: KnightCrawler Gating Fix, Opencode Bash Config]]"
tier: hot
tags: [knightcrawler, stremio, caddy, reverse-proxy, docker-compose, url-patching]
---

# KnightCrawler Gating Fix for Stremio Streams

## Overview

This concept covers the root cause and resolution of 404 errors encountered in KnightCrawler streams on Stremio when domain gating is enabled via Caddy's handle_path directive. The fix involves injecting an access token prefix into URLs constructed by the KnightCrawler addon to align with Caddy's path stripping behavior.

## How It Works

The KnightCrawler addon builds absolute URLs for stream resolution using the host header from incoming requests. When Caddy's `handle_path /{KC_ACCESS_TOKEN}/*` is used for domain gating, it strips the token prefix from the request path before proxying to the addon. This causes a mismatch because the addon constructs URLs without the token prefix, leading Stremio to request URLs that Caddy does not recognize, resulting in 404 errors.

To fix this, the following steps were taken:

1. The `KC_ACCESS_TOKEN` environment variable was passed into the KnightCrawler addon container to make the token available at runtime.
2. A patch script (`patch-https-host.js`) was created and applied at container startup, which modifies the URL construction logic in the addon source code. Specifically, it replaces occurrences of `${i.protocol}://${i.headers.host}` with `https://${i.headers.host}/${KC_ACCESS_TOKEN}`, injecting the token prefix into all constructed URLs.
3. This ensures that URLs returned by the addon include the gating prefix, matching what Caddy expects and preventing 404 errors.

Additional validation included verifying the compose configuration, pushing changes to GitHub, and deploying the updated stack. The fix was confirmed by observing that gated manifest requests returned HTTP 200 OK, while ungated requests returned 404 as expected.

This fix requires careful coordination between reverse proxy path handling and upstream application URL generation, highlighting the importance of consistent URL prefixing in gated proxy environments.

## Key Properties

- **Environment Variable Propagation:** Passing KC_ACCESS_TOKEN into the addon container is essential to enable runtime URL patching.
- **Patch Injection:** The patch modifies the addon source at startup to inject the token prefix into URLs.
- **Caddy handle_path Behavior:** Caddy strips the matched path prefix before proxying, requiring upstream apps to be aware of the prefix.

## Limitations

This fix assumes control over the addon source code to apply runtime patches. If the addon updates or changes URL construction logic, the patch may need to be updated. It also depends on the environment variable being correctly set and accessible in the container. Additionally, this approach tightly couples the addon URL format to the proxy gating scheme, which may reduce flexibility.

## Example

Patch snippet in `patch-https-host.js`:
```js
// Original URL construction
const url = `${i.protocol}://${i.headers.host}`;

// Patched URL construction with token prefix
const url = `https://${i.headers.host}/${process.env.KC_ACCESS_TOKEN}`;
```

Docker Compose snippet passing env var:
```yaml
services:
  knightcrawler-addon:
    environment:
      - KC_ACCESS_TOKEN=${KC_ACCESS_TOKEN}
```


## Relationship to Other Concepts

- **Caddy handle_path Directive** — Explains the proxy path prefix stripping behavior that causes the gating issue.
- **Docker Compose Environment Variable Management** — Describes how environment variables are propagated into containers.

## Practical Applications

This fix is applicable in any reverse proxy setup where path-based gating or authentication prefixes are stripped before proxying, but upstream applications generate absolute URLs unaware of the prefix. It ensures seamless integration of gated streaming services like KnightCrawler with Stremio behind Caddy proxies.

## Sources

- [[Copilot Session Checkpoint: KnightCrawler Gating Fix, Opencode Bash Config]] — primary source for this concept
