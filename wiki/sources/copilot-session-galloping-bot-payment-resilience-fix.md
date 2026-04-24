---
title: "Copilot Session Checkpoint: Galloping bot payment resilience fix"
type: source
created: '2026-04-24'
last_verified: '2026-04-24'
source_hash: "9294e5dafaa1bb7496452061315c836e6cfee1bd1261a1c8030afb5195f275d4"
sources:
  - raw/2026-04-24-copilot-session-galloping-bot-payment-resilience-fix-114d6563.md
concepts:
  - resilient-payment-encryption-fallback-chains
  - error-pattern-alert-escalation-zero-exit-automation-failures
related:
  - "[[Resilient Payment Encryption Fallback Chains]]"
  - "[[Error-Pattern Alert Escalation for Zero-Exit Automation Failures]]"
  - "[[TokenEx]]"
  - "[[Galloping-Bot]]"
  - "[[EZLinks API]]"
  - "[[Ntfy]]"
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 76
tags: [copilot-session, checkpoint, galloping-bot, payments, resilience, homelab, notifications, automation]
checkpoint_class: durable-debugging
retention_mode: retain
---

# Copilot Session Checkpoint: Galloping bot payment resilience fix

## Summary

This checkpoint captures a root-cause analysis and partial implementation pass for a failed [[Galloping-Bot]] tee-time booking run. It shows how a fragile browser-only payment encryption step broke when EZLinks stopped exposing TokenEx's `TxEncrypt` function on the pre-search view, then documents a layered recovery design that hardens both the booking path and the wrapper-script alerting path.

## Key Points

- The 2026-04-24 cron run targeted Saturday 2026-05-09 correctly, cleared Cloudflare, found **122 tee times**, and still failed every booking attempt because `TxEncrypt` was undefined.
- The root cause was a frontend integration drift: the EZLinks SPA no longer exposed TokenEx on `#/preSearch`, so the old `tab.evaluate("TxEncrypt(...)")` call in `src/api_client.py` failed on every booking attempt.
- The payment fix introduced a four-strategy fallback chain in `src/encryption.py`: **Python RSA**, **browser-native TokenEx**, **browser navigation to payment-bearing routes**, and **browser script injection**.
- The new Python-first path handles four public-key wire formats: full PEM, base64 DER SubjectPublicKeyInfo, JSON modulus/exponent, and hex DER.
- The checkpoint records a critical implementation detail: TokenEx's `TxEncrypt` behavior matches **RSA with PKCS#1 v1.5 padding**, not OAEP, and returns base64 ciphertext.
- `cryptography>=42.0.0` was added to the bot's requirements, and `tests/test_encryption.py` covered the chain with **15 passing tests** including RSA round-trips and fallback-order behavior.
- The session also found an observability bug in `galloping-snipe.sh`: the wrapper treated a zero process exit as success even when every booking attempt logged a fatal error.
- The wrapper fix added error-pattern detection for lines such as `Booking error`, `Card encryption failed`, `Cloudflare challenge did not clear`, and `Fatal:` so ntfy sends a high-priority **All Attempts Errored** alert instead of a misleading no-bookings message.
- Offline wrapper validation passed **4/5 cases**; the remaining failure was traced to an outdated test expectation, not to incorrect wrapper behavior.
- At checkpoint time, the implementation work was substantially complete but still needed cleanup steps such as updating lessons, committing both branches, opening PRs, merging, and restoring a stashed homelab worktree.

## Key Concepts

- [[Resilient Payment Encryption Fallback Chains]]
- [[Error-Pattern Alert Escalation for Zero-Exit Automation Failures]]
- [[Durable Copilot Session Checkpoint Promotion]]

## Related Entities

- **[[TokenEx]]** — The client-side encryption dependency whose missing `TxEncrypt` surface caused the booking failures.
- **[[Galloping-Bot]]** — The booking automation that consumed the new encryption chain and the wrapper alerting fix.
- **[[EZLinks API]]** — The booking backend whose SPA and payment flow exposed the brittle browser dependency.
- **[[Ntfy]]** — The notification channel used to escalate failures after wrapper-side semantic error detection.

