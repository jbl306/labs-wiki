---
title: "Copilot Session Checkpoint: Galloping bot CF clearance recovery"
type: source
created: '2026-05-01'
last_verified: '2026-05-01'
source_hash: "d78a6b607a140fec577d5a90939b312f86de85606841c25efaca1fb03a4f05ca"
sources:
  - raw/2026-05-01-copilot-session-galloping-bot-cf-clearance-recovery-e0655b3d.md
concepts:
  - api-cloudflare-clearance-keepalive-403-recovery
  - browser-backed-http-anti-bot-session-fidelity
related:
  - "[[API-Level Cloudflare Clearance Keepalive and 403 Recovery]]"
  - "[[Browser-Backed HTTP for Anti-Bot Session Fidelity]]"
  - "[[Galloping-Bot Boundary Resilience Patterns]]"
  - "[[Galloping-Bot]]"
  - "[[EZLinks API]]"
  - "[[Cloudflare]]"
  - "[[Resilient Payment Encryption Fallback Chains]]"
  - "[[Durable Copilot Session Checkpoint]]"
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 76
tags: [copilot-session, checkpoint, durable-knowledge, homelab, galloping-bot, cloudflare, automation, debugging]
checkpoint_class: durable-debugging
retention_mode: retain
---

# Copilot Session Checkpoint: Galloping bot CF clearance recovery

## Summary

This checkpoint captures a concrete anti-bot reliability failure in [[Galloping-Bot]]: page login and prewarm succeeded, but the EZLinks search API's own Cloudflare clearance expired during the idle countdown before the release window. The fix turned that diagnosis into two durable mechanisms: proactive API-clearance refresh during countdown and one-shot in-request recovery when `POST /api/search/search` returns a 403.

## Key Points

- The failing run showed a split-brain success pattern: FlareSolverr prewarm, page-level Cloudflare clearance, API priming, dummy search, and login all succeeded around 11:55, but the real release search failed at 12:00:02 with `PermissionError ... 403 (CF blocked)`.
- The root cause was not a total session loss. The source identifies a narrower failure boundary: the EZLinks API path `/api/search/search` appears to require its own Cloudflare clearance, and that API-specific clearance can go stale during a multi-minute idle wait.
- `src/session.py` was refactored so `_prime_api` became public `prime_api`, `fetch()` gained a `_fetch_once` helper, and a 403 path now re-primes the API and retries exactly once before surfacing failure.
- `src/booking.py` changed the countdown behavior so the bot refreshes API clearance every 60 seconds while waiting and forces one final refresh inside the last 15 seconds before the tee-time release.
- The checkpoint preserves an important architectural detail: `StealthSession` uses nodriver + Chromium plus browser-backed synchronous XMLHttpRequest, so requests inherit browser cookies and fingerprinting characteristics instead of using a plain Python HTTP client.
- The browser-backed transport has a caveat the session explicitly calls out: synchronous XHR cannot use `xhr.timeout`, so the `timeout` parameter on `fetch()` is not enforced at the transport layer.
- The reliability story is cumulative across incidents. This session references the earlier TokenEx/payment hardening work and extends the bot's resilience from payment-path recovery to anti-bot clearance recovery.
- Validation in the source was strong but bounded: 17/17 pytest tests passed, Docker build succeeded, and the image was rebuilt, but the new user request to run a real booking had not yet been executed at checkpoint time.
- The checkpoint also records operational caution: a real booking would create an actual paid reservation, and outside the natural Friday/Saturday release window a "live booking" may not exercise the intended code path meaningfully.

## Key Concepts

- [[API-Level Cloudflare Clearance Keepalive and 403 Recovery]]
- [[Browser-Backed HTTP for Anti-Bot Session Fidelity]]
- [[Resilient Payment Encryption Fallback Chains]]
- [[Durable Copilot Session Checkpoint Promotion]]

## Related Entities

- **[[Galloping-Bot]]** — The golf tee-time sniper whose release-window flow exposed the API-clearance expiry failure.
- **[[EZLinks API]]** — The booking backend whose `/api/search/search` endpoint appears to enforce a separate Cloudflare challenge boundary from the page shell.
- **[[Cloudflare]]** — The protection layer whose clearance behavior shaped the failure mode and the remediation strategy.
- **[[TokenEx]]** — Earlier Galloping-Bot hardening work on TokenEx provides the prior resilience pattern this checkpoint extends.
- **[[Durable Copilot Session Checkpoint]]** — The session artifact type being promoted into reusable operational knowledge.

