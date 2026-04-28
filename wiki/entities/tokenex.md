---
title: "TokenEx"
type: entity
created: 2026-04-24
last_verified: 2026-04-24
source_hash: "9294e5dafaa1bb7496452061315c836e6cfee1bd1261a1c8030afb5195f275d4"
sources:
  - raw/2026-04-24-copilot-session-galloping-bot-payment-resilience-fix-114d6563.md
concepts:
  - resilient-payment-encryption-fallback-chains
related:
  - "[[Galloping-Bot]]"
  - "[[EZLinks API]]"
  - "[[Resilient Payment Encryption Fallback Chains]]"
  - "[[Copilot Session Checkpoint: Galloping bot payment resilience fix]]"
tier: hot
tags: [payments, tokenization, client-side-encryption, javascript, automation]
quality_score: 70
---

# TokenEx

## Overview

TokenEx is the client-side card-encryption dependency in the EZLinks booking flow used by [[Galloping-Bot]]. In this checkpoint it appears through the `TxEncrypt` browser function and the hosted script `https://htp.tokenex.com/Iframe/Iframe-v3.min.js`, which together form the JavaScript-facing surface the bot originally relied on for card encryption.

The source matters because it documents a concrete integration failure mode: the SPA stopped exposing `TxEncrypt` on the `#/preSearch` route even though booking still required TokenEx-compatible ciphertext later in the flow. That turned TokenEx from a background dependency into the operational bottleneck for all booking attempts, and forced the bot to treat payment encryption as a resilience problem instead of a single happy-path API call.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | https://htp.tokenex.com/Iframe/Iframe-v3.min.js |
| Status | Active |

## Payment Flow Role

The checkpoint shows TokenEx acting as the card-encryption layer between raw card input and the booking request submitted by the EZLinks flow. The old bot implementation assumed the browser page would already provide `TxEncrypt(pubKey, cardNum)`, and it invoked that function directly from a nodriver tab context.

That assumption held until the SPA changed its loading behavior. Once TokenEx moved behind a payment-only chunk or later route, the booking bot could still search tee times and reach booking attempts, but it could not produce the encrypted card payload required to complete the reservation. The resulting failure was systematic rather than intermittent: all attempts reached the same broken dependency boundary.

## Technical Characteristics

The source extracts several implementation details that are more useful than a generic product description:

- `TxEncrypt` wraps a JavaScript RSA implementation compatible with **PKCS#1 v1.5 padding**.
- The expected output is **base64-encoded ciphertext** rather than a structured token object.
- The upstream public key may arrive in multiple wire formats, including PEM, DER, JSON modulus/exponent form, and hex DER.
- A hosted TokenEx script can be injected dynamically when the page does not already expose the runtime.

These details are what made a Python-side replacement viable: the bot did not need privileged secrets from the browser, only the public key plus fidelity to TokenEx's encryption format.

## Failure Mode and Recovery

The key operational lesson from this entity is that browser-exposed vendor helpers are not stable contracts. The EZLinks SPA could remove `TxEncrypt` from one route without changing the higher-level business flow, leaving automation that depended on the function name broken while human checkout might still work.

The resilience response was to demote TokenEx from "single mandatory in-page primitive" to "one compatible implementation strategy inside a broader encryption chain." That preserved compatibility with the booking system while reducing dependence on one specific route and one specific JavaScript global.

## Related Work

- [[Galloping-Bot]] consumes TokenEx-compatible ciphertext during automated booking attempts.
- [[EZLinks API]] provides the surrounding booking flow and the `TokenExPublicKey` input used by the resilient implementation.
- [[Resilient Payment Encryption Fallback Chains]] explains how TokenEx was kept as one strategy inside a more durable design.

## Sources

- [[Copilot Session Checkpoint: Galloping bot payment resilience fix]] — primary checkpoint documenting the failure mode and recovery strategy

